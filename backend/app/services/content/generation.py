from dataclasses import dataclass

@dataclass
class DocumentaryScript:
    title: str
    hook: str
    introduction: str
    act_1: str
    act_2: str
    act_3: str
    conclusion: str
    call_to_action: str

class ScriptGenerator:
    def generate(self, topic: str, research: list[dict], language: str = "hinglish") -> DocumentaryScript:
        facts = "; ".join(item.get("content", item.get("title", "")) for item in research[:5]) or "verified research notes"
        return DocumentaryScript(
            title=f"The Untold Documentary of {topic}",
            hook=f"What if everything you know about {topic} is only the surface?",
            introduction=f"Today we investigate {topic} using documented timelines, evidence, and expert context.",
            act_1=f"Act 1 establishes the origin story and the first turning point: {facts}.",
            act_2="Act 2 follows the conflict, incentives, hidden decisions, and public consequences.",
            act_3="Act 3 connects the aftermath to what is happening now and why audiences should care.",
            conclusion="The final lesson is that every viral story has deeper systems beneath the headline.",
            call_to_action="Subscribe for more evidence-led documentaries that explain the stories shaping our world.",
        )

class HumanizationEngine:
    def humanize(self, script: DocumentaryScript, language: str = "hinglish") -> str:
        sections = [script.hook, script.introduction, script.act_1, script.act_2, script.act_3, script.conclusion, script.call_to_action]
        pause = "\n\n[dramatic pause]\n"
        if language.lower() == "hindi":
            prefix = "Sochiye... "
        elif language.lower() == "english":
            prefix = "Imagine this... "
        else:
            prefix = "Sochiye... imagine this... "
        return prefix + pause.join(sections)

class ScenePlanner:
    def plan(self, script_text: str, target_scene_seconds: int = 20) -> list[dict]:
        paragraphs = [p.strip() for p in script_text.split("\n") if p.strip() and not p.startswith("[")]
        scenes: list[dict] = []
        for index, paragraph in enumerate(paragraphs, start=1):
            scenes.append({
                "scene_number": index,
                "duration_seconds": target_scene_seconds,
                "visual_description": f"Cinematic documentary visual for: {paragraph[:140]}",
                "voiceover": paragraph,
                "transition": "slow cinematic crossfade",
                "motion_plan": "subtle push-in, parallax layers, lower-third facts",
                "sound_effects": ["low impact", "ambient texture"],
                "music_requirements": "tense cinematic documentary bed with ducking under narration",
            })
        return scenes

class SEOGenerator:
    def generate(self, topic: str, scenes: list[dict]) -> dict:
        chapters = []
        elapsed = 0
        for scene in scenes:
            minutes, seconds = divmod(elapsed, 60)
            chapters.append({"time": f"{minutes:02d}:{seconds:02d}", "title": f"Part {scene['scene_number']}"})
            elapsed += scene["duration_seconds"]
        return {
            "title": f"The Untold Story of {topic} | Documentary",
            "description": f"A fact-based documentary exploring {topic}, its timeline, key people, consequences, and future implications.",
            "tags": [topic, "documentary", "explained", "history", "analysis"],
            "hashtags": ["#documentary", "#explained", "#history"],
            "chapters": chapters,
        }
