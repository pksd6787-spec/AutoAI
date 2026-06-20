class ImagePromptGenerator:
    def prompt_for_scene(self, scene: dict, style: str = "cinematic documentary") -> dict:
        return {
            "provider_candidates": ["flux-schnell", "flux-dev", "sdxl"],
            "prompt": f"{style}, high contrast, realistic, 16:9, {scene['visual_description']}",
            "negative_prompt": "low quality, blurry, distorted text, watermark",
        }

class VoicePlanGenerator:
    def plan_voiceover(self, scene: dict, language: str = "hinglish") -> dict:
        return {
            "provider_candidates": ["kokoro", "coqui"],
            "language": language,
            "text": scene["voiceover"],
            "format": ["wav", "mp3"],
            "voice_direction": "warm, serious, suspenseful documentary narrator",
        }

class SubtitleGenerator:
    def generate_srt(self, scenes: list[dict]) -> str:
        rows: list[str] = []
        elapsed = 0
        for index, scene in enumerate(scenes, start=1):
            start = self._format_time(elapsed)
            elapsed += scene["duration_seconds"]
            end = self._format_time(elapsed)
            rows.append(f"{index}\n{start} --> {end}\n{scene['voiceover']}\n")
        return "\n".join(rows)

    def _format_time(self, seconds: int) -> str:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d},000"

class RenderPlanGenerator:
    def build_render_plan(self, scenes: list[dict]) -> dict:
        return {
            "engine_candidates": ["ffmpeg", "moviepy", "remotion"],
            "resolution": "1920x1080",
            "fps": 30,
            "timeline": [
                {
                    "scene_number": scene["scene_number"],
                    "duration_seconds": scene["duration_seconds"],
                    "visual_layers": ["generated_image", "parallax_depth", "lower_third"],
                    "audio_layers": ["voiceover", "music_bed", "sfx"],
                    "transition": scene["transition"],
                }
                for scene in scenes
            ],
            "loudness_target_lufs": -14,
        }
