from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.domain import Opportunity
from app.schemas.api import DailyDecision, OpportunityCreate, OpportunityRead
from app.services.agents.core_agents import MonetizationPredictionAgent, TopicSelectionAgent, ViralPredictionAgent
from app.services.workflows.engine import WorkflowEngine

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
