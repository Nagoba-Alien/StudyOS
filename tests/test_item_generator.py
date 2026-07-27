from pathlib import Path

from app.models.ai_artifact import (
    AIArtifact,
    Difficulty,
)

from app.planner.item_generator import (
    RevisionItemGenerator,
)


def test_item_generator():

    artifact = AIArtifact(

        summary="Thermodynamics summary",

        notes="Detailed thermodynamics notes",

        flashcards=[],

        topics=[
            "Entropy",
            "Nozzle Flow",
        ],

        difficulty=Difficulty(
            score=3,
            reason="Medium difficulty",
        ),
    )

    generator = RevisionItemGenerator()

    item = generator.generate(

        course="CL 207",

        title="Assignment 1",

        pdf_path=Path(
            "test.pdf"
        ),

        text_path=Path(
            "test.txt"
        ),

        summary_path=Path(
            "summary.md"
        ),

        notes_path=Path(
            "notes.md"
        ),

        flashcards_path=Path(
            "cards.json"
        ),

        topics_path=Path(
            "topics.json"
        ),

        difficulty_path=Path(
            "difficulty.json"
        ),

        artifact=artifact,

        word_count=382,
    )

    assert item.course == "CL 207"
    assert item.title == "Assignment 1"
    assert item.difficulty_score == 3
    assert "Entropy" in item.topics
