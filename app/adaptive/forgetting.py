from datetime import date, datetime
from math import exp

from app.adaptive.mastery import MasteryModel
from app.storage.history import RevisionHistory


class ForgettingModel:
    """
    Estimates retained knowledge after
    forgetting over time.
    """

    def __init__(self):

        self.history = RevisionHistory()

        self.mastery = MasteryModel()

        self.decay_rate = 0.08

    def estimate(
        self,
        course: str,
        title: str,
    ) -> float:
        """
        Returns estimated retained knowledge
        between 0 and 100.
        """

        mastery = self.mastery.estimate(
            course,
            title,
        )

        record = self.history.get(
            course,
            title,
        )

        if record["last_reviewed"] is None:

            return mastery

        last_review = datetime.strptime(
            record["last_reviewed"],
            "%Y-%m-%d",
        ).date()

        days = (
            date.today() - last_review
        ).days

        retention = mastery * exp(
            -self.decay_rate * days
        )

        return round(
            max(retention, 0),
            2,
        )
