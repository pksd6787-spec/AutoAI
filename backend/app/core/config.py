from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "DocuForge Autonomous"
    database_url: str = "postgresql+asyncpg://docuforge:docuforge@postgres:5432/docuforge"
    redis_url: str = "redis://redis:6379/0"
    jwt_secret: str = "change-me"
    viral_threshold: float = 70
    opportunity_threshold: float = 65
    monetization_threshold: float = 60

settings = Settings()
