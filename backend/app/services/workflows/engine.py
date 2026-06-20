from enum import StrEnum

class JobStatus(StrEnum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    paused = "paused"
    canceled = "canceled"
    retrying = "retrying"

class WorkflowEngine:
    def plan_daily_documentary(self, project_id: str) -> list[dict]:
        return [
            {"job_type": "trend_discovery", "parallel": False},
            {"job_type": "topic_expansion", "parallel": True},
            {"job_type": "research", "parallel": True},
            {"job_type": "fact_verification", "parallel": False},
            {"job_type": "competition_analysis", "parallel": True},
            {"job_type": "viral_prediction", "parallel": True},
            {"job_type": "monetization_prediction", "parallel": True},
            {"job_type": "topic_selection", "parallel": False},
            {"job_type": "script_generation", "parallel": False},
            {"job_type": "humanization", "parallel": False},
            {"job_type": "scene_planning", "parallel": False},
            {"job_type": "media_generation", "parallel": True},
            {"job_type": "voice_generation", "parallel": True},
            {"job_type": "render_video", "parallel": False},
            {"job_type": "thumbnail_seo", "parallel": True},
            {"job_type": "youtube_publish", "parallel": False},
            {"job_type": "analytics_learning", "parallel": False},
        ]
