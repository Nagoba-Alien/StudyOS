from app.models import (
    RevisionItem,
    RevisionSession,
)


class RevisionScheduler:
    """
    Builds a study session from
    a priority-ranked list.
    """

    def schedule(
        self,
        items: list[RevisionItem],
        available_minutes: int,
    ) -> RevisionSession:

        session = RevisionSession(
            date="Today"
        )

        remaining = available_minutes

        for item in items:

            if item.estimated_minutes <= remaining:

                session.items.append(item)

                session.total_minutes += (
                    item.estimated_minutes
                )

                remaining -= item.estimated_minutes

        return session
