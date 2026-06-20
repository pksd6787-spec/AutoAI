import uuid
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(Text)
    slug: Mapped[str] = mapped_column(Text, unique=True)
    plan: Mapped[str] = mapped_column(Text, default="starter")
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)

class Project(Base):
    __tablename__ = "projects"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"))
    name: Mapped[str] = mapped_column(Text)
    channel_id: Mapped[str | None] = mapped_column(Text)
    language: Mapped[str] = mapped_column(Text, default="hinglish")
    niche: Mapped[str | None] = mapped_column(Text)
    settings: Mapped[dict] = mapped_column(JSONB, default=dict)

class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"))
    topic: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(Text)
    growth_rate: Mapped[float] = mapped_column(Numeric, default=0)
    search_demand: Mapped[float] = mapped_column(Numeric, default=0)
    audience_interest: Mapped[float] = mapped_column(Numeric, default=0)
    trend_velocity: Mapped[float] = mapped_column(Numeric, default=0)
    expansion: Mapped[dict] = mapped_column(JSONB, default=dict)
    competition_score: Mapped[float | None] = mapped_column(Numeric)
    opportunity_score: Mapped[float | None] = mapped_column(Numeric)
    viral_score: Mapped[float | None] = mapped_column(Numeric)
    predicted_ctr: Mapped[float | None] = mapped_column(Numeric)
    predicted_retention: Mapped[float | None] = mapped_column(Numeric)
    monetization_score: Mapped[float | None] = mapped_column(Numeric)
    estimated_rpm: Mapped[float | None] = mapped_column(Numeric)
    brand_safety_score: Mapped[float | None] = mapped_column(Numeric)
    status: Mapped[str] = mapped_column(Text, default="discovered")

class Workflow(Base):
    __tablename__ = "workflows"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("projects.id"))
    workflow_type: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(Text, default="pending")
    input: Mapped[dict] = mapped_column(JSONB, default=dict)
    output: Mapped[dict] = mapped_column(JSONB, default=dict)
    scheduled_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
