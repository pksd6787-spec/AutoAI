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

class ResearchAgent(Agent):
    name = "research"
    async def run(self, payload: dict) -> dict:
        topic = payload["topic"]
        return {"items": [
            {"item_type": "timeline", "title": f"Origins of {topic}", "content": f"Establish the earliest documented context for {topic}.", "confidence_score": 0.72},
            {"item_type": "key_event", "title": f"Turning point in {topic}", "content": "Identify the decision or event that changed public attention.", "confidence_score": 0.68},
            {"item_type": "reference", "title": "Source bundle", "content": "Collect primary sources, reputable news, public data, and archive material.", "confidence_score": 0.75},
        ]}

class FactVerificationAgent(Agent):
    name = "fact_verification"
    async def run(self, payload: dict) -> dict:
        items = payload.get("items", [])
        verified = [item for item in items if item.get("confidence_score", 0) >= 0.6]
        score = round(sum(item.get("confidence_score", 0) for item in verified) / max(len(verified), 1), 2)
        return {"verified_items": verified, "removed_count": len(items) - len(verified), "verification_score": score}

class CompetitionAnalysisAgent(Agent):
    name = "competition_analysis"
    async def run(self, payload: dict) -> dict:
        views = payload.get("median_views", 100_000)
        channels = payload.get("competing_channels", 12)
        freshness = payload.get("freshness_days", 30)
        competition_score = min(100, channels * 5 + max(0, 30 - freshness))
        opportunity_score = max(0, min(100, views / 5000 - competition_score / 3 + 60))
        return {"competition_score": round(competition_score, 2), "opportunity_score": round(opportunity_score, 2)}

class ThumbnailAgent(Agent):
    name = "thumbnail"
    async def run(self, payload: dict) -> dict:
        topic = payload["topic"]
        variants = [
            {"label": "mystery", "text": "They Hid This", "prompt": f"high contrast shocked face, dark mystery background, {topic}", "predicted_ctr": 7.8},
            {"label": "evidence", "text": "Proof Found", "prompt": f"documentary evidence board, red strings, archival photo, {topic}", "predicted_ctr": 6.9},
            {"label": "scale", "text": "Bigger Than You Think", "prompt": f"massive cinematic scale, tiny human silhouette, {topic}", "predicted_ctr": 7.2},
        ]
        return {"variants": variants, "selected": max(variants, key=lambda item: item["predicted_ctr"])}
