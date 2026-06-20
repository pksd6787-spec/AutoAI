class AnalyticsInsightEngine:
    def summarize(self, snapshots: list[dict]) -> dict:
        if not snapshots:
            return {"status": "insufficient_data", "insights": []}
        latest = snapshots[-1]
        insights = []
        if latest.get("ctr", 0) < 4:
            insights.append("CTR is below target; test stronger curiosity-gap thumbnails and titles.")
        if latest.get("retention", 0) < 45:
            insights.append("Retention is below target; shorten intro and move payoff earlier.")
        if latest.get("rpm", 0) > 4:
            insights.append("RPM is strong; prioritize adjacent advertiser-friendly topics.")
        return {"status": "ok", "latest": latest, "insights": insights}
