from app.planner.loader import RevisionLoader
from app.planner.scorer import RevisionScorer
from app.planner.scheduler import RevisionScheduler
from app.planner.session import StudySessionTracker


def main():

    loader = RevisionLoader()

    scorer = RevisionScorer()

    scheduler = RevisionScheduler()

    tracker = StudySessionTracker()

    # Load revision items

    items = loader.load()

    # Calculate priorities

    items = scorer.score_all(
        items
    )

    # Generate today's plan

    session = scheduler.schedule(
        items,
        available_minutes=60,
    )

    print()

    print("=" * 70)
    print("Today's Revision Plan")
    print("=" * 70)

    if not session.items:

        print(
            "No revision items available."
        )

    else:

        for index, item in enumerate(
            session.items,
            start=1,
        ):

            print(
                f"{index}. "
                f"{item.course} - "
                f"{item.title}"
            )

            print(
                f"   Priority : "
                f"{item.priority:.2f}"
            )

            print(
                f"   Duration : "
                f"{item.estimated_minutes} min"
            )

            print()

    print("-" * 70)

    print(
        f"Total Time : "
        f"{session.total_minutes} minutes"
    )

    # Collect user feedback

    if session.items:

        tracker.record(
            session
        )


if __name__ == "__main__":
    main()
