from pathlib import Path

from app.storage.revision_store import RevisionStore
from app.models.revision_item import RevisionItem


def test_revision_store(tmp_path):

    store = RevisionStore(
        tmp_path / "revision_items.json"
    )

    item = RevisionItem(

        course="CL 207",

        title="Thermodynamics",

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

        word_count=500,

        estimated_minutes=20,

        difficulty_score=3,

    )

    store.save(
        [item]
    )

    items = store.load()

    assert len(items) == 1
    assert items[0].course == "CL 207"
    assert items[0].title == "Thermodynamics"
