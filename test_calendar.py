from pathlib import Path

from app.exporters.calendar import CalendarExporter
from app.models import RevisionItem, RevisionSession


def main():

    session = RevisionSession(
        date="Today"
    )

    item = RevisionItem(

        course="StudyOS",

        title="Google Calendar Integration Test",

        pdf_path=Path(
            "data/test.pdf"
        ),

        text_path=Path(
            "data/test.txt"
        ),

        summary_path=Path(
            "data/test_summary.md"
        ),

        notes_path=Path(
            "data/test_notes.md"
        ),

        flashcards_path=Path(
            "data/test_flashcards.json"
        ),

        topics_path=Path(
            "data/test_topics.json"
        ),

        difficulty_path=Path(
            "data/test_difficulty.json"
        ),

        word_count=1000,

        estimated_minutes=30,

        difficulty_score=3,

        priority=100,

    )

    session.items.append(
        item
    )

    exporter = CalendarExporter()

    exporter.export(
        session=session,
    )

    print(
        "\nCalendar integration test completed successfully."
    )


if __name__ == "__main__":

    main()
