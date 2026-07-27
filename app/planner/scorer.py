from datetime import date

from app.models import RevisionItem
from app.storage.history import RevisionHistory
from app.exams.calendar import ExamCalendar


class RevisionScorer:
    """
    Calculates priority scores for revision items.

    Factors:
    - Difficulty
    - Reading time
    - Document size
    - Revision history
    - Confidence
    - Completion status
    - Upcoming exams
    """

    def __init__(self):

        self.history = RevisionHistory()

        self.exam_calendar = ExamCalendar()

    def exam_bonus(
        self,
        course: str,
    ) -> int:
        """
        Adds priority based on upcoming exams.
        """

        days = self.exam_calendar.days_until_exam(
            course
        )

        if days is None:
            return 0

        if days < 3:
            return 50

        elif days < 7:
            return 30

        elif days < 14:
            return 15

        return 0

    def score(
        self,
        item: RevisionItem,
    ) -> float:
        """
        Calculate priority score for one revision item.
        """

        # Base importance

        base_score = (
            item.difficulty_score * 20
            + item.estimated_minutes
            + item.word_count / 100
        )

        priority = (
            base_score
            + self.exam_bonus(
                item.course
            )
        )

        history = self.history.get(
            item.course,
            item.title,
        )

        # -------------------------
        # Forgetting factor
        # -------------------------

        last_reviewed = history[
            "last_reviewed"
        ]

        if last_reviewed is None:

            priority += 30

        else:

            last_date = date.fromisoformat(
                last_reviewed
            )

            days_since_review = (
                date.today() - last_date
            ).days

            if days_since_review > 7:

                priority += 20

            elif days_since_review > 3:

                priority += 10

        # -------------------------
        # Confidence factor
        # -------------------------

        confidence = history[
            "confidence"
        ]

        confidence_bonus = {
            None: 10,
            1: 20,
            2: 15,
            3: 10,
            4: 5,
            5: 0,
        }

        priority += confidence_bonus.get(
            confidence,
            10,
        )

        # -------------------------
        # Completion factor
        # -------------------------

        if history["completed"]:

            priority -= 50

        return round(
            max(priority, 0),
            2,
        )

    def score_all(
        self,
        items: list[RevisionItem],
    ) -> list[RevisionItem]:
        """
        Score and sort all revision items.
        """

        for item in items:

            item.priority = self.score(
                item
            )

        items.sort(
            key=lambda x: x.priority,
            reverse=True,
        )

        return items
