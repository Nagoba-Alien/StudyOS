from app.adaptive.forgetting import ForgettingModel
from app.adaptive.mastery import MasteryModel
from app.models import RevisionItem


class RiskAnalyzer:
    """
    Identifies academically risky topics.
    """

    def __init__(self):

        self.mastery = MasteryModel()

        self.forgetting = ForgettingModel()

    def analyze(
        self,
        items: list[RevisionItem],
    ) -> list[dict]:
        """
        Calculate risk scores for all items.
        """

        risks = []

        for item in items:

            mastery = self.mastery.estimate(
                item.course,
                item.title,
            )

            retention = self.forgetting.estimate(
                item.course,
                item.title,
            )

            risk_score = 0

            reasons = []

            # Low mastery contribution
            if mastery < 50:

                risk_score += (
                    50 - mastery
                )

                reasons.append(
                    f"Low mastery ({mastery:.1f}%)"
                )

            # Forgetting contribution
            if retention < 50:

                risk_score += (
                    50 - retention
                )

                reasons.append(
                    f"Low retention ({retention:.1f}%)"
                )

            # Priority contribution

            if item.priority > 75:

                risk_score += 20

                reasons.append(
                    "High revision priority"
                )

            # Difficulty contribution

            if item.difficulty_score >= 4:

                risk_score += 10

                reasons.append(
                    "Difficult topic"
                )

            risks.append(
                {
                    "course": item.course,

                    "title": item.title,

                    "risk_score": round(
                        min(risk_score, 100),
                        2,
                    ),

                    "mastery": mastery,

                    "retention": retention,

                    "reasons": reasons,
                }
            )

        risks.sort(
            key=lambda x: x["risk_score"],
            reverse=True,
        )

        return risks
