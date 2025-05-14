# from typing import Dict, Any, Optional, List
# class StoryGenerator:
#     def __init__(self, client, collection=None):
#         self.client = client
#         self.collection = collection

#     def get_story_from_llm(self, user_prompt):
#         system_prompt = (
#                 """You are StoryWeaverGPT, a creative AI designed to craft engaging, coherent, and imaginative narratives on demand.

# System Instructions:

# Tone & Style

# Adapt tone to user’s request: whimsical for fairy tales; suspenseful for thrillers; warm for slice-of-life.

# Use vivid imagery and sensory details.

# Maintain consistent voice and pacing.

# Structure

# Follow a three-act arc:

# Setup – Introduce characters, setting, and conflict.

# Confrontation – Escalate stakes, develop tension.

# Resolution – Provide satisfying payoff or twist.

# Characters & Dialogue

# Give major characters clear goals, motivations, and flaws.

# Write dialogue that feels natural and reveals personality.

# Show, don’t tell: reveal emotions through action and speech.

# World-Building

# Integrate setting details seamlessly.

# Define any special rules (magic systems, technology) concisely.

# Avoid info-dump; reveal background gradually.

# User Interaction

# If the user specifies genre, length, or style, follow those constraints.

# If the user provides prompts or characters, weave them organically into the plot.

# Offer to expand, continue, or revise on request.

# Quality & Safety

# Avoid graphic violence, hate speech, or disallowed content.

# For mature themes, include a brief content warning.

# Ensure coherent grammar and spelling.

# When Responding:

# Begin with a short “scene-setting” paragraph.

# Then proceed through the three acts.

# End with a question or prompt inviting user feedback or continuation."""
#             )
        
#         messages = [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
        
#         response = self.client.chat.completions.create(
#             model="gpt-4o",  # or another model of choice
#             temperature=0.7,
#             messages=messages
#         )
        
#         # Extract and return the story content
#         return response.choices[0].message.content.strip()

#     def generate_story(self, user_prompt):
#         final_prompt = user_prompt
        
#         story = self.get_story_from_llm(
#             user_prompt=final_prompt,
#         )
        
#         return {
#             "prompt_used": final_prompt,
#             "story": story
#         }


# ── backend/story_writer.py ──
import uuid
from typing import List, Dict, Optional

class StoryGenerator:
    def __init__(self, client, model: str = "gpt-4o", temperature: float = 0.7):
        self.client = client
        self.model = model
        self.temperature = temperature
        self.sessions: Dict[str, List[Dict[str, str]]] = {}

    def start_story(
        self,
        prompt: str,
        num_chapters: Optional[int],
        chapter_length: Optional[int]
    ) -> (str, List[str]):
        session_id = str(uuid.uuid4())
        system_msg = (
            # instructs the model to begin with character intros
            "You are StoryWeaverGPT. First, introduce each main character briefly, then craft an engaging story using lots of dialogue. "
            "Keep the language simple and easy"
            "Adjust chapter count and length as specified."
        )
        user_prompt = self._build_prompt(prompt, num_chapters, chapter_length)
        self.sessions[session_id] = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_prompt}
        ]
        chapters = self._generate_and_parse(session_id)
        return session_id, chapters

    def continue_story(
        self,
        session_id: str,
        next_chapters: int,
        chapter_length: Optional[int]
    ) -> List[str]:
        if session_id not in self.sessions:
            raise KeyError("Session not found")
        length_clause = (
            f"Ensure each new chapter is around {chapter_length} words." if chapter_length
            else "Maintain the same chapter length as before."
        )
        user_msg = {
            "role": "user",
            "content": f"Continue the story for {next_chapters} more chapter(s). {length_clause}"
        }
        self.sessions[session_id].append(user_msg)
        return self._generate_and_parse(session_id)

    def _build_prompt(
        self,
        user_prompt: str,
        num_chapters: Optional[int],
        chapter_length: Optional[int],
    ) -> str:
        style = (
            "Use simple, easy-to-understand language with plenty of dialogue."
        )
        length_part = (
            f"Each chapter should be approximately {chapter_length} words long."
            if chapter_length
            else "Chapters can vary in length."
        )
        if num_chapters:
            return (
                f"{user_prompt}\nDivide the narrative into {num_chapters} chapters."
                f" {length_part} {style}"
            )
        return (
            f"{user_prompt}\nWrite a long-form story and feel free to extend as needed."
            f" {length_part} {style}"
        )

    def _generate_and_parse(self, session_id: str) -> List[str]:
        messages = self.sessions[session_id]
        resp = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=messages
        )
        text = resp.choices[0].message.content.strip()
        self.sessions[session_id].append({"role": "assistant", "content": text})
        chapters: List[str] = []
        parts = [p.strip() for p in text.split("Chapter ") if p.strip()]
        for part in parts:
            idx, _, body = part.partition(":")
            chapter_title = f"## Chapter {idx.strip()}"  # Markdown header
            chapter_body = body.strip() if body else part
            chapters.append(f"{chapter_title}\n\n{chapter_body}")
        return chapters