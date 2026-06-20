from app.core.config import settings
from app.services.agents.base import Agent

class TrendDiscoveryAgent(Agent):
    name = "trend_discovery"
    async def run(self, payload: dict) -> dict:
        seed = payload.get("seed", "documentary")
        return {"opportunities": [{"topic": f"The hidden story of {seed}", "source": "public_trends", "growth_rate": 72, "search_demand": 68, "audience_interest": 75, "trend_velocity": 70}]}

class TopicExpansionAgent(Agent):
    name = "topic_expansion"
    async def run(self, payload: dict) -> dict:
        topic = payload["topic"]
        result = await self.router.generate(f"Expand documentary topic: {topic}", self.name)
        return {"related_topics": [topic + " origins", topic + " consequences"], "model": result}

class ViralPredictionAgent(Agent):
    name = "viral_prediction"
    async def run(self, payload: dict) -> dict:
        score = min(100, payload.get("growth_rate", 0)*0.25 + payload.get("search_demand", 0)*0.25 + payload.get("audience_interest", 0)*0.2 + payload.get("trend_velocity", 0)*0.2 + payload.get("curiosity_gap", 70)*0.1)
        return {"viral_score": round(score, 2), "predicted_ctr": round(score/10, 2), "predicted_retention": round(35 + score/2, 2), "predicted_watch_time_seconds": int(300 + score*12)}

class MonetizationPredictionAgent(Agent):
    name = "monetization_prediction"
    async def run(self, payload: dict) -> dict:
        brand_safety = payload.get("brand_safety", 80)
        rpm = 1.5 + brand_safety / 20
        return {"monetization_score": brand_safety, "estimated_rpm": rpm, "brand_safety_score": brand_safety}

class TopicSelectionAgent(Agent):
    name = "topic_selection"
    async def run(self, payload: dict) -> dict:
        candidates = payload.get("candidates", [])
        approved = [c for c in candidates if c.get("viral_score", 0) > settings.viral_threshold and c.get("opportunity_score", 0) > settings.opportunity_threshold and c.get("monetization_score", 0) > settings.monetization_threshold]
        approved.sort(key=lambda c: (c["viral_score"] + c["opportunity_score"] + c["monetization_score"]), reverse=True)
        return {"approved": approved, "selected": approved[0] if approved else None}
