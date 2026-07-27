from app.storage.history import RevisionHistory
from app.models import RevisionSession


class StudySessionTracker:
    """
    Handles user feedback after a study session.
    """

    def __init__(self):

        self.history = RevisionHistory()

    def record(
        self,
        session: RevisionSession,
    ):

        print()

        print("=" * 70)
        print("Study Session Feedback")
        print("=" * 70)

        for item in session.items:

            print()

            print(
                f"{item.course} - "
                f"{item.title}"
            )

            completed_input = input(
                "Completed? (y/n): "
            )

            completed = (
                completed_input.lower()
                == "y"
            )

            confidence = int(
                input(
                    "Confidence (1-5): "
                )
            )

            self.history.update(
                item.course,
                item.title,
                confidence=confidence,
                completed=completed,
            )

            print(
                "✓ Updated"
            )
