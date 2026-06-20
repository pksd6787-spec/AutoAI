from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class ProviderHealthSnapshot:
    name: str
    healthy: bool
    priority: int
    quota_remaining: float
    latency_ms: int | None = None
    checked_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    reason: str | None = None


class ProviderHealthMonitor:
    def snapshot(self, providers: list) -> list[ProviderHealthSnapshot]:
        snapshots: list[ProviderHealthSnapshot] = []
        for provider in providers:
            healthy = bool(provider.healthy and provider.quota_remaining > 0)
            reason = None if healthy else "disabled, unhealthy, or quota exhausted"
            snapshots.append(ProviderHealthSnapshot(
                name=provider.name,
                healthy=healthy,
                priority=provider.priority,
                quota_remaining=provider.quota_remaining,
                reason=reason,
            ))
        return snapshots


class ProviderCostEstimator:
    def estimate(self, input_tokens: int, output_tokens: int, input_rate: float, output_rate: float) -> float:
        return round((input_tokens / 1000 * input_rate) + (output_tokens / 1000 * output_rate), 6)
