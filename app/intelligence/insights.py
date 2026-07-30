from app.adaptive.forgetting import ForgettingModel
from app.adaptive.mastery import MasteryModel

from app.intelligence.progress import (
    ProgressTracker,
)

from app.models import RevisionItem


class InsightGenerator:
    """
    Generates personalized academic insights.
    """

    def __init__(self):

        self.mastery = MasteryModel()

        self.forgetting = ForgettingModel()

        self.progress = ProgressTracker()

    def generate(
        self,
        items: list[RevisionItem],
    ) -> list[str]:
        """
        Generate insights from learning data.
        """

        insights = []

        for item in items:

            mastery = self.mastery.estimate(
                item.course,
                item.title,
            )

            retention = self.forgetting.estimate(
                item.course,
                item.title,
            )

            improvement = self.progress.improvement(
                item.course,
                item.title,
            )

            topic = (
                f"{item.course} - "
                f"{item.title}"
            )

            # Low mastery warning

            if mastery < 40:

                insights.append(
                    f"{topic}: "
                    f"Mastery is low "
                    f"({mastery:.1f}%). "
                    f"Prioritize concept revision."
                )

            # Retention warning

            if retention < 40:

                insights.append(
                    f"{topic}: "
                    f"Retention is low "
                    f"({retention:.1f}%). "
                    f"Increase revision frequency."
                )

            # Improvement tracking

            if improvement > 0:

                insights.append(
                    f"{topic}: "
                    f"Mastery improved by "
                    f"{improvement:.1f}%."
                )

        if not insights:

            insights.append(
                "Your learning progress is stable. "
                "Continue your current revision strategy."
            )

        return insights
