from app.storage.history import RevisionHistory


class MasteryModel:
    """
    Estimates how well a student has
    learned a study resource.
    """

    def __init__(self):

        self.history = RevisionHistory()

    def estimate(
        self,
        course: str,
        title: str,
    ) -> float:
        """
        Returns a mastery score
        between 0 and 100.
        """

        record = self.history.get(
            course,
            title,
        )

        confidence = (
            record["confidence"]
            if record["confidence"] is not None
            else 1
        )

        review_count = record[
            "review_count"
        ]

        completed = record[
            "completed"
        ]

        confidence_score = (
            confidence / 5
        ) * 60

        review_bonus = min(
            review_count * 5,
            30,
        )

        completion_bonus = (
            10 if completed else 0
        )

        mastery = (
            confidence_score
            + review_bonus
            + completion_bonus
        )

        return round(
            min(mastery, 100),
            2,
        )
