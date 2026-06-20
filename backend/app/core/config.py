import os
from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "DocuForge Autonomous")
    database_url: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://docuforge:docuforge@postgres:5432/docuforge")
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379/0")
    jwt_secret: str = os.getenv("JWT_SECRET", "change-me")
    viral_threshold: float = float(os.getenv("VIRAL_THRESHOLD", "70"))
    opportunity_threshold: float = float(os.getenv("OPPORTUNITY_THRESHOLD", "65"))
    monetization_threshold: float = float(os.getenv("MONETIZATION_THRESHOLD", "60"))

settings = Settings()
