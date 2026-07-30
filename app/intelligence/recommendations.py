from app.adaptive.forgetting import ForgettingModel
from app.adaptive.mastery import MasteryModel
from app.models import RevisionItem


class RecommendationEngine:
    """
    Generates personalized study recommendations.
    """

    def __init__(self):

        self.mastery = MasteryModel()

        self.forgetting = ForgettingModel()

    def recommend(
        self,
        items: list[RevisionItem],
        limit: int = 3,
    ) -> list[dict]:
        """
        Generate top study recommendations.
        """

        recommendations = []

        for item in items:

            mastery = self.mastery.estimate(
                item.course,
                item.title,
            )

            retention = self.forgetting.estimate(
                item.course,
                item.title,
            )

            reasons = []

            if mastery < 50:

                reasons.append(
                    f"Low mastery ({mastery:.1f}%)"
                )

            if retention < 50:

                reasons.append(
                    f"Low retention ({retention:.1f}%)"
                )

            if item.priority > 75:

                reasons.append(
                    "High adaptive priority"
                )

            if not reasons:

                reasons.append(
                    "Regular revision recommended"
                )

            recommendations.append(
                {
                    "course": item.course,

                    "title": item.title,

                    "priority": item.priority,

                    "mastery": mastery,

                    "retention": retention,

                    "reason": reasons,
                }
            )

        recommendations.sort(
            key=lambda x: x["priority"],
            reverse=True,
        )

        return recommendations[:limit]
