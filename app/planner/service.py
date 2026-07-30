from datetime import date

from app.adaptive.forgetting import ForgettingModel
from app.adaptive.mastery import MasteryModel
from app.adaptive.scorer import AdaptiveScorer

from app.intelligence.insights import (
    InsightGenerator,
)

from app.intelligence.recommendations import (
    RecommendationEngine,
)

from app.intelligence.risk_analysis import (
    RiskAnalyzer,
)

from app.models import DailyBriefing

from app.planner.loader import RevisionLoader
from app.planner.scheduler import RevisionScheduler


class PlannerService:
    """
    Central coordinator for the
    StudyOS planning pipeline.
    """

    def __init__(self):

        self.loader = RevisionLoader()

        self.scorer = AdaptiveScorer()

        self.scheduler = RevisionScheduler()

        self.mastery = MasteryModel()

        self.forgetting = ForgettingModel()

        self.recommendations = (
            RecommendationEngine()
        )

        self.risks = RiskAnalyzer()

        self.insights = InsightGenerator()

    def build_daily_briefing(
        self,
        available_minutes: int = 60,
    ) -> DailyBriefing:

        items = self.loader.load()

        items = self.scorer.score_all(
            items
        )

        session = self.scheduler.schedule(
            items,
            available_minutes,
        )

        briefing = DailyBriefing(

            date=str(
                date.today()
            ),

            items=session.items,

            total_minutes=session.total_minutes,

            recommendations=self.recommendations.recommend(
                session.items
            ),

            risks=self.risks.analyze(
                session.items
            ),

            insights=self.insights.generate(
                session.items
            ),
        )

        if briefing.items:

            briefing.average_mastery = round(

                sum(

                    self.mastery.estimate(
                        item.course,
                        item.title,
                    )

                    for item in briefing.items

                )

                / len(briefing.items),

                2,

            )

            briefing.average_retention = round(

                sum(

                    self.forgetting.estimate(
                        item.course,
                        item.title,
                    )

                    for item in briefing.items

                )

                / len(briefing.items),

                2,

            )

        return briefing
