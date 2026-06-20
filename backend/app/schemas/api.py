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

class ContentPipelineRequest(BaseModel):
    topic: str
    language: str = "hinglish"
    research: list[dict] = Field(default_factory=list)

class ContentPipelineResponse(BaseModel):
    script: dict
    humanized_script: str
    scenes: list[dict]
    seo: dict
    subtitles_srt: str
    render_plan: dict
    image_prompts: list[dict]
    voice_plans: list[dict]

class OAuthUrlResponse(BaseModel):
    url: str
    scopes: list[str]

class AnalyticsInsightRequest(BaseModel):
    snapshots: list[dict] = Field(default_factory=list)

class AnalyticsInsightResponse(BaseModel):
    status: str
    latest: dict | None = None
    insights: list[str] = Field(default_factory=list)

class WorkflowRunRequest(BaseModel):
    project_id: str
    input: dict = Field(default_factory=dict)

class WorkflowJobRead(BaseModel):
    id: str
    workflow_id: str
    job_type: str
    status: str
    parallel: bool
    attempts: int
    max_attempts: int
    output: dict = Field(default_factory=dict)
    error_message: str | None = None

class WorkflowRunRead(BaseModel):
    id: str
    project_id: str
    workflow_type: str
    status: str
    input: dict = Field(default_factory=dict)
    output: dict = Field(default_factory=dict)
    jobs: list[WorkflowJobRead]

class ProviderHealthRead(BaseModel):
    name: str
    healthy: bool
    priority: int
    quota_remaining: float
    latency_ms: int | None = None
    reason: str | None = None
