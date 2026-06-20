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
