class YouTubePublishingPlanner:
    def prepare_upload(self, video_id: str, seo: dict, thumbnail_asset_id: str | None = None) -> dict:
        return {
            "video_id": video_id,
            "title": seo["title"][:100],
            "description": seo["description"],
            "tags": seo.get("tags", [])[:500],
            "chapters": seo.get("chapters", []),
            "thumbnail_asset_id": thumbnail_asset_id,
            "privacy_status": "scheduled",
            "requires_oauth_scopes": ["youtube.upload"],
        }
