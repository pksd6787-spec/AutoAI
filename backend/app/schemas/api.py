from pydantic import BaseModel, Field
from uuid import UUID

class OpportunityCreate(BaseModel):
    project_id: UUID
    topic: str
    source: str = "manual"
    growth_rate: float = 0
    search_demand: float = 0
    audience_interest: float = 0
    trend_velocity: float = 0

class OpportunityRead(OpportunityCreate):
    id: UUID
    status: str
    viral_score: float | None = None
    opportunity_score: float | None = None
    monetization_score: float | None = None
    model_config = {"from_attributes": True}

class DailyDecision(BaseModel):
    project_id: UUID
    question: str = "What documentary should I create today to maximize views, retention, subscribers, and revenue?"
    selected_topic: str | None = None
    scores: dict = Field(default_factory=dict)
    rationale: list[str] = Field(default_factory=list)
