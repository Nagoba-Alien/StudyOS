from pathlib import Path

from app.adaptive.scorer import AdaptiveScorer
from app.models import RevisionItem


def test_adaptive_scorer():

    scorer = AdaptiveScorer()

    item = RevisionItem(

        course="CL 207",

        title="Assignment 1",

        pdf_path=Path("a.pdf"),

        text_path=Path("a.txt"),

        summary_path=Path("summary.md"),

        notes_path=Path("notes.md"),

        flashcards_path=Path("cards.json"),

        topics_path=Path("topics.json"),

        difficulty_path=Path("difficulty.json"),

        word_count=400,

        estimated_minutes=20,

        difficulty_score=3,

    )

    score = scorer.score(item)

    assert score >= 0
