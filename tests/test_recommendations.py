from pathlib import Path

from app.intelligence.recommendations import (
    RecommendationEngine,
)

from app.models.revision_item import RevisionItem


def test_recommendations():

    item = RevisionItem(

        course="CL 207",

        title="Entropy",

        pdf_path=Path("test.pdf"),

        text_path=Path("test.txt"),

        summary_path=Path("summary.md"),

        notes_path=Path("notes.md"),

        flashcards_path=Path("cards.json"),

        topics_path=Path("topics.json"),

        difficulty_path=Path("difficulty.json"),

        word_count=500,

        estimated_minutes=30,

        difficulty_score=4,

        priority=90,

    )

    engine = RecommendationEngine()

    result = engine.recommend(
        [item]
    )

    assert len(result) == 1

    assert result[0]["course"] == "CL 207"

    assert result[0]["priority"] == 90
