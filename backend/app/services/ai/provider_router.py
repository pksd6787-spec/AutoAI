from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class Provider:
    name: str
    priority: int
    cost_weight: float = 1.0
    healthy: bool = True
    quota_remaining: float = 1_000_000
    provider_type: str = "openai_compatible"
    model: str = "default"
    base_url: str | None = None
    api_key: str | None = None
    rate_limit_per_minute: int = 60
    input_cost_per_1k: float = 0.0
    output_cost_per_1k: float = 0.0
    consecutive_failures: int = 0
    circuit_open_until: float = 0.0


@dataclass
class UsageEvent:
    provider: str
    task: str
    input_tokens: int
    output_tokens: int
    cost: float
    latency_ms: int
    success: bool
    error: str | None = None
    created_at: float = field(default_factory=time.time)


class ProviderTransport(Protocol):
    async def generate(self, provider: Provider, prompt: str, task: str) -> dict:
        raise NotImplementedError


class SimulatedProviderTransport:
    async def generate(self, provider: Provider, prompt: str, task: str) -> dict:
        await asyncio.sleep(0)
        return {
            "provider": provider.name,
            "model": provider.model,
            "task": task,
            "text": f"[{provider.name}] generated {task} output",
            "input_tokens": max(int(len(prompt) / 4), 1),
            "output_tokens": 128,
        }


class RateLimiter:
    def __init__(self):
        self._events: dict[str, list[float]] = {}

    def allow(self, provider: Provider, now: float | None = None) -> bool:
        now = now or time.time()
        window_start = now - 60
        events = [timestamp for timestamp in self._events.get(provider.name, []) if timestamp >= window_start]
        self._events[provider.name] = events
        if len(events) >= provider.rate_limit_per_minute:
            return False
        events.append(now)
        return True


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, cooldown_seconds: int = 60):
        self.failure_threshold = failure_threshold
        self.cooldown_seconds = cooldown_seconds

    def can_call(self, provider: Provider, now: float | None = None) -> bool:
        now = now or time.time()
        return provider.circuit_open_until <= now

    def record_success(self, provider: Provider) -> None:
        provider.consecutive_failures = 0
        provider.circuit_open_until = 0
        provider.healthy = True

    def record_failure(self, provider: Provider, now: float | None = None) -> None:
        now = now or time.time()
        provider.consecutive_failures += 1
        if provider.consecutive_failures >= self.failure_threshold:
            provider.healthy = False
            provider.circuit_open_until = now + self.cooldown_seconds


class UsageLedger:
    def __init__(self):
        self.events: list[UsageEvent] = []

    def record(self, event: UsageEvent) -> None:
        self.events.append(event)

    def total_cost(self) -> float:
        return round(sum(event.cost for event in self.events), 6)


class AIProviderRouter:
    def __init__(
        self,
        providers: list[Provider] | None = None,
        transport: ProviderTransport | None = None,
        rate_limiter: RateLimiter | None = None,
        circuit_breaker: CircuitBreaker | None = None,
        usage_ledger: UsageLedger | None = None,
    ):
        self.providers = providers or [
            Provider("groq", 1, model="llama-3.3-70b-versatile", input_cost_per_1k=0.00059, output_cost_per_1k=0.00079),
            Provider("nvidia", 2, model="nvidia/llama-3.1-nemotron", input_cost_per_1k=0.0006, output_cost_per_1k=0.0008),
            Provider("openrouter", 3, model="openrouter/auto", input_cost_per_1k=0.001, output_cost_per_1k=0.001),
            Provider("local-qwen", 4, cost_weight=0, provider_type="local", model="qwen", input_cost_per_1k=0, output_cost_per_1k=0),
            Provider("local-llama", 5, cost_weight=0, provider_type="local", model="llama", input_cost_per_1k=0, output_cost_per_1k=0),
        ]
        self.transport = transport or SimulatedProviderTransport()
        self.rate_limiter = rate_limiter or RateLimiter()
        self.circuit_breaker = circuit_breaker or CircuitBreaker()
        self.usage_ledger = usage_ledger or UsageLedger()

    async def generate(self, prompt: str, task: str, max_retries: int = 2) -> dict:
        errors: list[str] = []
        for provider in sorted(self.providers, key=lambda p: (p.priority, p.cost_weight)):
            if not self._eligible(provider):
                continue
            for attempt in range(max_retries + 1):
                started = time.time()
                try:
                    result = await self._call_provider(provider, prompt, task)
                    latency_ms = int((time.time() - started) * 1000)
                    self._record_usage(provider, task, result, latency_ms, True)
                    self.circuit_breaker.record_success(provider)
                    return result
                except Exception as exc:
                    latency_ms = int((time.time() - started) * 1000)
                    self.circuit_breaker.record_failure(provider)
                    self._record_usage(provider, task, {"input_tokens": self._estimate_tokens(prompt), "output_tokens": 0}, latency_ms, False, str(exc))
                    errors.append(f"{provider.name}: {exc}")
                    await asyncio.sleep(0.25 * (2 ** attempt))
        raise RuntimeError("All AI providers failed: " + "; ".join(errors))

    def _eligible(self, provider: Provider) -> bool:
        if provider.quota_remaining <= 0:
            return False
        if not provider.healthy:
            return False
        if not self.circuit_breaker.can_call(provider):
            return False
        return self.rate_limiter.allow(provider)

    async def _call_provider(self, provider: Provider, prompt: str, task: str) -> dict:
        result = await self.transport.generate(provider, prompt, task)
        input_tokens = int(result.get("input_tokens", self._estimate_tokens(prompt)))
        output_tokens = int(result.get("output_tokens", self._estimate_tokens(result.get("text", ""))))
        provider.quota_remaining -= max(input_tokens + output_tokens, 1)
        result["input_tokens"] = input_tokens
        result["output_tokens"] = output_tokens
        result["cost"] = self._estimate_cost(provider, input_tokens, output_tokens)
        return result

    def _record_usage(self, provider: Provider, task: str, result: dict, latency_ms: int, success: bool, error: str | None = None) -> None:
        input_tokens = int(result.get("input_tokens", 0))
        output_tokens = int(result.get("output_tokens", 0))
        self.usage_ledger.record(UsageEvent(
            provider=provider.name,
            task=task,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=self._estimate_cost(provider, input_tokens, output_tokens),
            latency_ms=latency_ms,
            success=success,
            error=error,
        ))

    def _estimate_tokens(self, text: str) -> int:
        return max(int(len(text) / 4), 1)

    def _estimate_cost(self, provider: Provider, input_tokens: int, output_tokens: int) -> float:
        return round((input_tokens / 1000 * provider.input_cost_per_1k) + (output_tokens / 1000 * provider.output_cost_per_1k), 6)
