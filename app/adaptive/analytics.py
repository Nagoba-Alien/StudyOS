from app.adaptive.forgetting import ForgettingModel
from app.adaptive.mastery import MasteryModel
from app.models import RevisionItem


class LearningAnalytics:
    """
    Computes statistics about the user's
    current learning progress.
    """

    def __init__(self):

        self.mastery = MasteryModel()

        self.forgetting = ForgettingModel()

    def average_mastery(
        self,
        items: list[RevisionItem],
    ) -> float:

        if not items:

            return 0

        total = sum(
            self.mastery.estimate(
                item.course,
                item.title,
            )
            for item in items
        )

        return round(
            total / len(items),
            2,
        )

    def average_retention(
        self,
        items: list[RevisionItem],
    ) -> float:

        if not items:

            return 0

        total = sum(
            self.forgetting.estimate(
                item.course,
                item.title,
            )
            for item in items
        )

        return round(
            total / len(items),
            2,
        )

    def weakest_items(
        self,
        items: list[RevisionItem],
        limit: int = 5,
    ) -> list[tuple[str, float]]:

        data = []

        for item in items:

            mastery = self.mastery.estimate(
                item.course,
                item.title,
            )

            data.append(
                (
                    f"{item.course} - {item.title}",
                    mastery,
                )
            )

        data.sort(
            key=lambda x: x[1]
        )

        return data[:limit]

    def strongest_items(
        self,
        items: list[RevisionItem],
        limit: int = 5,
    ) -> list[tuple[str, float]]:

        data = []

        for item in items:

            mastery = self.mastery.estimate(
                item.course,
                item.title,
            )

            data.append(
                (
                    f"{item.course} - {item.title}",
                    mastery,
                )
            )

        data.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        return data[:limit]
