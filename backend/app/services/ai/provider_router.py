from dataclasses import dataclass
import asyncio

@dataclass
class Provider:
    name: str
    priority: int
    cost_weight: float = 1.0
    healthy: bool = True
    quota_remaining: float = 1_000_000

class AIProviderRouter:
    def __init__(self, providers: list[Provider] | None = None):
        self.providers = providers or [
            Provider("groq", 1), Provider("nvidia", 2), Provider("openrouter", 3),
            Provider("local-qwen", 4, cost_weight=0), Provider("local-llama", 5, cost_weight=0),
        ]

    async def generate(self, prompt: str, task: str, max_retries: int = 2) -> dict:
        errors: list[str] = []
        for provider in sorted(self.providers, key=lambda p: (p.priority, p.cost_weight)):
            if not provider.healthy or provider.quota_remaining <= 0:
                continue
            for attempt in range(max_retries + 1):
                try:
                    return await self._call_provider(provider, prompt, task)
                except Exception as exc:
                    errors.append(f"{provider.name}: {exc}")
                    await asyncio.sleep(0.25 * (2 ** attempt))
        raise RuntimeError("All AI providers failed: " + "; ".join(errors))

    async def _call_provider(self, provider: Provider, prompt: str, task: str) -> dict:
        provider.quota_remaining -= max(len(prompt) / 4, 1)
        return {"provider": provider.name, "task": task, "text": f"[{provider.name}] generated {task} output"}
