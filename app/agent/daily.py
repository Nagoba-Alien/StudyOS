from datetime import date
from pathlib import Path

from app.agent.report import DailyReportGenerator
from app.planner.service import PlannerService


def main():

    print("=" * 60)
    print("StudyOS Daily Agent")
    print("=" * 60)
    print()

    # ----------------------------------------
    # Build today's study briefing
    # ----------------------------------------

    planner = PlannerService()

    briefing = planner.build_daily_briefing(
        available_minutes=60,
    )

    # ----------------------------------------
    # Generate markdown report
    # ----------------------------------------

    generator = DailyReportGenerator()

    report = generator.generate(
        briefing
    )

    # ----------------------------------------
    # Save report
    # ----------------------------------------

    reports_dir = Path("reports")

    reports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_path = (
        reports_dir
        / f"{date.today()}.md"
    )

    generator.save(
        report,
        report_path,
    )

    # ----------------------------------------
    # Console summary
    # ----------------------------------------

    print("Daily report generated successfully.")
    print()

    print(f"Date: {briefing.date}")

    print(
        f"Revision items: {len(briefing.items)}"
    )

    print(
        f"Total study time: {briefing.total_minutes} minutes"
    )

    print(
        f"Average mastery: {briefing.average_mastery:.1f}%"
    )

    print(
        f"Average retention: {briefing.average_retention:.1f}%"
    )

    print()

    print("Saved to:")

    print(report_path.resolve())


if __name__ == "__main__":

    main()
