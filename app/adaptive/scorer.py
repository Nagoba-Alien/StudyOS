from app.adaptive.forgetting import ForgettingModel
from app.adaptive.mastery import MasteryModel
from app.exams.calendar import ExamCalendar
from app.models import RevisionItem


class AdaptiveScorer:
    """
    Calculates adaptive revision priorities
    and normalises them to a 0–100 scale.
    """

    def __init__(self):

        self.mastery = MasteryModel()

        self.forgetting = ForgettingModel()

        self.calendar = ExamCalendar()

    def score(
        self,
        item: RevisionItem,
    ) -> float:
        """
        Calculates the raw priority score.
        """

        mastery = self.mastery.estimate(
            item.course,
            item.title,
        )

        retention = self.forgetting.estimate(
            item.course,
            item.title,
        )

        weakness = 100 - mastery

        forgetting = 100 - retention

        try:

            days = self.calendar.days_until_exam(
                item.course,
            )

            if days <= 7:

                exam_bonus = 40

            elif days <= 14:

                exam_bonus = 25

            elif days <= 30:

                exam_bonus = 10

            else:

                exam_bonus = 0

        except Exception:

            exam_bonus = 0

        difficulty = (
            item.difficulty_score * 15
        )

        reading = min(
            item.estimated_minutes,
            30,
        )

        raw_score = (

            difficulty

            + weakness

            + forgetting

            + exam_bonus

            + reading

        )

        return round(
            raw_score,
            2,
        )

    def score_all(
        self,
        items: list[RevisionItem],
    ) -> list[RevisionItem]:
        """
        Scores every item and normalises
        priorities to a 0–100 scale.
        """

        if not items:

            return items

        raw_scores = []

        for item in items:

            score = self.score(
                item
            )

            raw_scores.append(
                score
            )

            item.priority = score

        max_score = max(
            raw_scores
        )

        if max_score > 0:

            for item in items:

                item.priority = round(

                    (
                        item.priority
                        / max_score
                    )
                    * 100,

                    2,

                )

        items.sort(

            key=lambda x: x.priority,

            reverse=True,

        )

        return items
