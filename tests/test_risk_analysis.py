from pathlib import Path

from app.intelligence.risk_analysis import (
    RiskAnalyzer,
)

from app.models.revision_item import RevisionItem


def test_risk_analysis():

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

        difficulty_score=5,

        priority=90,

    )

    analyzer = RiskAnalyzer()

    result = analyzer.analyze(
        [item]
    )

    assert len(result) == 1

    assert result[0]["course"] == "CL 207"

    assert "risk_score" in result[0]

    assert "reasons" in result[0]
