import json
from pathlib import Path

from app.ai.client import GeminiClient
from app.models.ai_artifact import (
    AIArtifact,
    Difficulty,
    Flashcard,
)


class AIArtifactGenerator:
    """
    Generates all AI study artifacts using
    a single Gemini request.
    """

    def __init__(self):

        self.client = GeminiClient()

    def generate(self, text: str) -> AIArtifact:

        prompt = f"""
You are an expert university teaching assistant.

Return ONLY valid JSON.

Generate:

1. summary
2. concise study notes
3. flashcards
4. topics
5. difficulty estimate

JSON format:

{{
  "summary": "...",
  "notes": "...",
  "flashcards": [
      {{
        "question": "...",
        "answer": "..."
      }}
  ],
  "topics": [
      "..."
  ],
  "difficulty": {{
      "score": 0,
      "reason": "..."
  }}
}}

Lecture:

{text}
"""

        response = self.client.generate(
            prompt,
            response_mime_type="application/json"
        )

        data = json.loads(response)

        flashcards = [
            Flashcard(
                question=item["question"],
                answer=item["answer"],
            )
            for item in data["flashcards"]
        ]

        difficulty = Difficulty(
            score=data["difficulty"]["score"],
            reason=data["difficulty"]["reason"],
        )

        return AIArtifact(
            summary=data["summary"],
            notes=data["notes"],
            flashcards=flashcards,
            topics=data["topics"],
            difficulty=difficulty,
        )

    def save(
        self,
        artifact: AIArtifact,
        output_dir: Path,
        stem: str,
    ):

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        (output_dir / f"{stem}_summary.md").write_text(
            artifact.summary,
            encoding="utf-8",
        )

        (output_dir / f"{stem}_notes.md").write_text(
            artifact.notes,
            encoding="utf-8",
        )

        with open(
            output_dir / f"{stem}_flashcards.json",
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                [
                    {
                        "question": c.question,
                        "answer": c.answer,
                    }
                    for c in artifact.flashcards
                ],
                file,
                indent=4,
                ensure_ascii=False,
            )

        with open(
            output_dir / f"{stem}_topics.json",
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                artifact.topics,
                file,
                indent=4,
                ensure_ascii=False,
            )

        with open(
            output_dir / f"{stem}_difficulty.json",
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                {
                    "score": artifact.difficulty.score,
                    "reason": artifact.difficulty.reason,
                },
                file,
                indent=4,
                ensure_ascii=False,
            )


if __name__ == "__main__":

    input_file = Path("output/test.txt")

    output_dir = Path("output/ai")

    text = input_file.read_text(
        encoding="utf-8"
    )

    generator = AIArtifactGenerator()

    artifact = generator.generate(text)

    generator.save(
        artifact,
        output_dir,
        "test",
    )

    print("✓ AI artifacts generated successfully.")
