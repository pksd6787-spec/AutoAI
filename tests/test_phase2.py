import asyncio

from app.services.agents.core_agents import FactVerificationAgent, TopicSelectionAgent, ViralPredictionAgent
from app.services.ai.provider_router import AIProviderRouter, Provider
from app.services.content.generation import HumanizationEngine, ScenePlanner, ScriptGenerator
from app.services.media.pipeline import RenderPlanGenerator, SubtitleGenerator


def test_provider_router_falls_back_to_healthy_provider():
    router = AIProviderRouter([Provider("groq", 1, healthy=False), Provider("nvidia", 2)])
    result = asyncio.run(router.generate("hello", "unit_test"))
    assert result["provider"] == "nvidia"


def test_topic_selection_requires_all_thresholds():
    candidates = [
        {"topic": "weak", "viral_score": 90, "opportunity_score": 80, "monetization_score": 10},
        {"topic": "strong", "viral_score": 90, "opportunity_score": 80, "monetization_score": 80},
    ]
    result = asyncio.run(TopicSelectionAgent().run({"candidates": candidates}))
    assert result["selected"]["topic"] == "strong"


def test_fact_verification_filters_low_confidence_items():
    result = asyncio.run(FactVerificationAgent().run({"items": [{"confidence_score": 0.9}, {"confidence_score": 0.2}]}))
    assert result["removed_count"] == 1
    assert result["verification_score"] == 0.9


def test_content_pipeline_building_blocks():
    script = ScriptGenerator().generate("space race", [{"content": "Verified launch timeline"}], "english")
    humanized = HumanizationEngine().humanize(script, "english")
    scenes = ScenePlanner().plan(humanized, target_scene_seconds=12)
    subtitles = SubtitleGenerator().generate_srt(scenes)
    render_plan = RenderPlanGenerator().build_render_plan(scenes)
    assert "Imagine this" in humanized
    assert scenes
    assert "00:00:00,000" in subtitles
    assert render_plan["engine_candidates"] == ["ffmpeg", "moviepy", "remotion"]


def test_viral_prediction_outputs_expected_fields():
    result = asyncio.run(ViralPredictionAgent().run({"growth_rate": 80, "search_demand": 70, "audience_interest": 75, "trend_velocity": 60}))
    assert result["viral_score"] > 60
    assert result["predicted_watch_time_seconds"] > 300

from app.services.ai.health import ProviderCostEstimator, ProviderHealthMonitor
from app.services.workflows.runtime import RuntimeStatus, WorkflowRuntime


def test_workflow_runtime_create_enqueue_and_complete():
    runtime = WorkflowRuntime()
    workflow = runtime.create_daily_workflow("project-1", {"seed": "space"})
    assert len(workflow.jobs) >= 10
    runtime.enqueue(workflow.id)
    completed = runtime.run_next()
    assert completed is not None
    assert completed.status == RuntimeStatus.completed
    assert completed.output["completed_jobs"] == len(completed.jobs)


def test_workflow_runtime_pause_resume_cancel():
    runtime = WorkflowRuntime()
    workflow = runtime.create_daily_workflow("project-1")
    runtime.enqueue(workflow.id)
    assert runtime.pause(workflow.id).status == RuntimeStatus.paused
    assert runtime.resume(workflow.id).status == RuntimeStatus.queued
    assert runtime.cancel(workflow.id).status == RuntimeStatus.canceled


def test_provider_health_and_cost_estimator():
    providers = [Provider("groq", 1, quota_remaining=10), Provider("nvidia", 2, healthy=False)]
    snapshots = ProviderHealthMonitor().snapshot(providers)
    assert snapshots[0].healthy is True
    assert snapshots[1].healthy is False
    assert ProviderCostEstimator().estimate(1000, 500, 0.01, 0.02) == 0.02

from app.services.ai.provider_router import CircuitBreaker, RateLimiter, UsageLedger


class FailingTransport:
    async def generate(self, provider, prompt, task):
        raise RuntimeError("provider exploded")


def test_provider_router_records_usage_cost_and_tokens():
    ledger = UsageLedger()
    router = AIProviderRouter([Provider("groq", 1, input_cost_per_1k=1, output_cost_per_1k=1)], usage_ledger=ledger)
    result = asyncio.run(router.generate("hello world", "script"))
    assert result["input_tokens"] > 0
    assert result["output_tokens"] == 128
    assert ledger.events[0].success is True
    assert ledger.total_cost() > 0


def test_rate_limiter_blocks_after_provider_limit():
    limiter = RateLimiter()
    provider = Provider("groq", 1, rate_limit_per_minute=1)
    assert limiter.allow(provider, now=1000) is True
    assert limiter.allow(provider, now=1001) is False
    assert limiter.allow(provider, now=1062) is True


def test_circuit_breaker_opens_after_failures():
    breaker = CircuitBreaker(failure_threshold=2, cooldown_seconds=30)
    provider = Provider("groq", 1)
    breaker.record_failure(provider, now=100)
    assert breaker.can_call(provider, now=101) is True
    breaker.record_failure(provider, now=102)
    assert provider.healthy is False
    assert breaker.can_call(provider, now=103) is False
    assert breaker.can_call(provider, now=133) is True


def test_provider_router_falls_back_after_transport_failure():
    router = AIProviderRouter([Provider("groq", 1), Provider("nvidia", 2)], transport=FailingTransport(), circuit_breaker=CircuitBreaker(failure_threshold=1))
    try:
        asyncio.run(router.generate("hello", "failing", max_retries=0))
    except RuntimeError as exc:
        assert "All AI providers failed" in str(exc)
    assert all(provider.healthy is False for provider in router.providers)
    assert len(router.usage_ledger.events) == 2
