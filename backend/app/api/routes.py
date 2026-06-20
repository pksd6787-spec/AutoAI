from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.domain import Opportunity
from app.schemas.api import DailyDecision, OpportunityCreate, OpportunityRead
from app.services.agents.core_agents import MonetizationPredictionAgent, TopicSelectionAgent, ViralPredictionAgent
from app.services.workflows.engine import WorkflowEngine
from app.schemas.api import AnalyticsInsightRequest, AnalyticsInsightResponse, ContentPipelineRequest, ContentPipelineResponse, OAuthUrlResponse
from app.services.analytics.insights import AnalyticsInsightEngine
from app.services.auth.google_oauth import SCOPES, build_google_oauth_url
from app.services.content.generation import HumanizationEngine, SEOGenerator, ScenePlanner, ScriptGenerator
from app.services.media.pipeline import ImagePromptGenerator, RenderPlanGenerator, SubtitleGenerator, VoicePlanGenerator

router = APIRouter(prefix="/api/v1")

@router.get("/health")
async def health():
    return {"status": "ok", "service": "docuforge-autonomous"}

@router.post("/opportunities", response_model=OpportunityRead)
async def create_opportunity(payload: OpportunityCreate, db: AsyncSession = Depends(get_db)):
    item = Opportunity(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.get("/opportunities", response_model=list[OpportunityRead])
async def list_opportunities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Opportunity).limit(100))
    return result.scalars().all()

@router.post("/decisions/daily", response_model=DailyDecision)
async def daily_decision(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Opportunity).where(Opportunity.project_id == project_id))
    candidates = []
    viral = ViralPredictionAgent()
    money = MonetizationPredictionAgent()
    for opp in result.scalars().all():
        base = {"topic": opp.topic, "growth_rate": float(opp.growth_rate), "search_demand": float(opp.search_demand), "audience_interest": float(opp.audience_interest), "trend_velocity": float(opp.trend_velocity), "opportunity_score": float(opp.opportunity_score or 70)}
        base.update(await viral.run(base))
        base.update(await money.run(base))
        candidates.append(base)
    selected = (await TopicSelectionAgent().run({"candidates": candidates}))["selected"]
    return DailyDecision(project_id=project_id, selected_topic=selected["topic"] if selected else None, scores=selected or {}, rationale=["Selected highest approved blend of viral, opportunity, and monetization scores."])

@router.get("/workflows/daily-plan")
async def daily_plan(project_id: str):
    return {"project_id": project_id, "jobs": WorkflowEngine().plan_daily_documentary(project_id)}


@router.get("/auth/google/url", response_model=OAuthUrlResponse)
async def google_oauth_url(client_id: str, redirect_uri: str, state: str):
    return OAuthUrlResponse(url=build_google_oauth_url(client_id, redirect_uri, state), scopes=SCOPES)

@router.post("/content/pipeline", response_model=ContentPipelineResponse)
async def content_pipeline(payload: ContentPipelineRequest):
    script = ScriptGenerator().generate(payload.topic, payload.research, payload.language)
    humanized = HumanizationEngine().humanize(script, payload.language)
    scenes = ScenePlanner().plan(humanized)
    seo = SEOGenerator().generate(payload.topic, scenes)
    image_prompts = [ImagePromptGenerator().prompt_for_scene(scene) for scene in scenes]
    voice_plans = [VoicePlanGenerator().plan_voiceover(scene, payload.language) for scene in scenes]
    subtitles = SubtitleGenerator().generate_srt(scenes)
    render_plan = RenderPlanGenerator().build_render_plan(scenes)
    return ContentPipelineResponse(
        script=script.__dict__,
        humanized_script=humanized,
        scenes=scenes,
        seo=seo,
        subtitles_srt=subtitles,
        render_plan=render_plan,
        image_prompts=image_prompts,
        voice_plans=voice_plans,
    )

@router.post("/analytics/insights", response_model=AnalyticsInsightResponse)
async def analytics_insights(payload: AnalyticsInsightRequest):
    return AnalyticsInsightEngine().summarize(payload.snapshots)
