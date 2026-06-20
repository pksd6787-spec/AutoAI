class ChannelBrainEngine:
    def learn(self, analytics: list[dict]) -> dict:
        preferences: dict[str, float] = {}
        for row in analytics:
            topic = row.get("topic", "unknown")
            score = row.get("ctr", 0) * 2 + row.get("retention", 0) + row.get("rpm", 0) * 5
            preferences[topic] = preferences.get(topic, 0) + score
        return {"preferences": dict(sorted(preferences.items(), key=lambda x: x[1], reverse=True))}

    def boost_opportunity(self, opportunity: dict, profile: dict) -> dict:
        topic = opportunity.get("topic", "").lower()
        boost = sum(weight for key, weight in profile.get("preferences", {}).items() if key.lower() in topic)
        opportunity["channel_brain_boost"] = boost
        opportunity["opportunity_score"] = opportunity.get("opportunity_score", 0) + min(boost, 20)
        return opportunity
