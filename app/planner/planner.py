from app.adaptive.analytics import LearningAnalytics
from app.adaptive.forgetting import ForgettingModel
from app.adaptive.mastery import MasteryModel
from app.adaptive.scorer import AdaptiveScorer

from app.planner.loader import RevisionLoader
from app.planner.scheduler import RevisionScheduler
from app.planner.session import StudySessionTracker


def main():

    # ----------------------------------------
    # Initialize components
    # ----------------------------------------

    loader = RevisionLoader()

    scorer = AdaptiveScorer()

    scheduler = RevisionScheduler()

    tracker = StudySessionTracker()

    mastery_model = MasteryModel()

    forgetting_model = ForgettingModel()

    analytics = LearningAnalytics()

    # ----------------------------------------
    # Load study resources
    # ----------------------------------------

    items = loader.load()

    if not items:

        print("No revision items found.")

        return

    # ----------------------------------------
    # Compute adaptive priorities
    # ----------------------------------------

    items = scorer.score_all(items)

    # ----------------------------------------
    # Build today's study session
    # ----------------------------------------

    session = scheduler.schedule(
        items,
        available_minutes=60,
    )

    print()

    print("=" * 70)
    print("Today's Adaptive Revision Plan")
    print("=" * 70)

    if not session.items:

        print("No tasks scheduled.")

    else:

        for index, item in enumerate(
            session.items,
            start=1,
        ):

            mastery = mastery_model.estimate(
                item.course,
                item.title,
            )

            retention = forgetting_model.estimate(
                item.course,
                item.title,
            )

            print(
                f"{index}. {item.course} - {item.title}"
            )

            print(
                f"   Priority   : {item.priority:.2f}/100"
            )

            print(
                f"   Mastery    : {mastery:.1f}%"
            )

            print(
                f"   Retention  : {retention:.1f}%"
            )

            print(
                f"   Difficulty : {item.difficulty_score}/5"
            )

            print(
                f"   Duration   : {item.estimated_minutes} min"
            )

            print()

    print("-" * 70)

    print(
        f"Total Study Time : {session.total_minutes} minutes"
    )

    # ----------------------------------------
    # Record study feedback
    # ----------------------------------------

    if session.items:

        tracker.record(session)

    # ----------------------------------------
    # Learning Analytics
    # ----------------------------------------

    print()

    print("=" * 70)
    print("Learning Analytics")
    print("=" * 70)

    average_mastery = analytics.average_mastery(items)

    average_retention = analytics.average_retention(items)

    print(
        f"Average Mastery   : {average_mastery:.1f}%"
    )

    print(
        f"Average Retention : {average_retention:.1f}%"
    )

    print()

    weakest = analytics.weakest_items(items)

    print("Weakest Topics")

    if weakest:

        for topic, score in weakest:

            print(
                f"  {topic:<45} {score:.1f}%"
            )

    else:

        print("  None")

    print()

    strongest = analytics.strongest_items(items)

    print("Strongest Topics")

    if strongest:

        for topic, score in strongest:

            print(
                f"  {topic:<45} {score:.1f}%"
            )

    else:

        print("  None")

    print()

    print("=" * 70)


if __name__ == "__main__":

    main()
