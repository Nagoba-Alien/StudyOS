from pathlib import Path

from app.models import DailyBriefing


class DailyReportGenerator:
    """
    Generates a Markdown report from a
    DailyBriefing object.

    This class contains NO planning logic.
    It only formats data for presentation.
    """

    def generate(
        self,
        briefing: DailyBriefing,
    ) -> str:

        report = []

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        report.append("# 📚 StudyOS Daily Briefing")
        report.append("")
        report.append(f"**Date:** {briefing.date}")
        report.append("")

        report.append("---")
        report.append("")

        # -------------------------------------------------
        # Revision Plan
        # -------------------------------------------------

        report.append("## 🎯 Today's Revision Plan")
        report.append("")

        if not briefing.items:

            report.append(
                "No revision scheduled today."
            )

        else:

            report.append(
                f"Total study time: **{briefing.total_minutes} minutes**"
            )

            report.append("")

            for index, item in enumerate(
                briefing.items,
                start=1,
            ):

                report.append(
                    f"### {index}. {item.course} — {item.title}"
                )

                report.append(
                    f"- Priority: **{item.priority:.1f}/100**"
                )

                report.append(
                    f"- Difficulty: **{item.difficulty_score}/5**"
                )

                report.append(
                    f"- Estimated Time: **{item.estimated_minutes} min**"
                )

                if item.topics:

                    report.append("- Topics:")

                    for topic in item.topics:

                        report.append(
                            f"  - {topic}"
                        )

                report.append("")

        report.append("---")
        report.append("")

        # -------------------------------------------------
        # Recommendations
        # -------------------------------------------------

        report.append("## 💡 Recommendations")
        report.append("")

        if briefing.recommendations:

            for recommendation in briefing.recommendations:

                report.append(
                    f"### {recommendation['course']} — {recommendation['title']}"
                )

                report.append(
                    f"- Priority: **{recommendation['priority']:.1f}/100**"
                )

                report.append("- Reasons:")

                for reason in recommendation["reason"]:

                    report.append(
                        f"  - {reason}"
                    )

                report.append("")

        else:

            report.append(
                "No recommendations available."
            )

        report.append("---")
        report.append("")

        # -------------------------------------------------
        # Risk Analysis
        # -------------------------------------------------

        report.append("## ⚠️ Risk Analysis")
        report.append("")

        if briefing.risks:

            for risk in briefing.risks:

                report.append(
                    f"### {risk['course']} — {risk['title']}"
                )

                report.append(
                    f"- Risk Score: **{risk['risk_score']:.1f}/100**"
                )

                report.append(
                    f"- Mastery: **{risk['mastery']:.1f}%**"
                )

                report.append(
                    f"- Retention: **{risk['retention']:.1f}%**"
                )

                if risk["reasons"]:

                    report.append("- Reasons:")

                    for reason in risk["reasons"]:

                        report.append(
                            f"  - {reason}"
                        )

                report.append("")

        else:

            report.append(
                "No academic risks detected."
            )

        report.append("---")
        report.append("")

        # -------------------------------------------------
        # Statistics
        # -------------------------------------------------

        report.append("## 📈 Learning Statistics")
        report.append("")

        report.append(
            f"- Average Mastery: **{briefing.average_mastery:.1f}%**"
        )

        report.append(
            f"- Average Retention: **{briefing.average_retention:.1f}%**"
        )

        report.append("")

        report.append("---")
        report.append("")

        # -------------------------------------------------
        # Insights
        # -------------------------------------------------

        report.append("## 🧠 AI Insights")
        report.append("")

        if briefing.insights:

            for insight in briefing.insights:

                report.append(
                    f"- {insight}"
                )

        else:

            report.append(
                "- No additional insights."
            )

        report.append("")
        report.append("---")
        report.append("")
        report.append(
            "_Generated automatically by StudyOS._"
        )

        return "\n".join(report)

    def save(
        self,
        report: str,
        output_path: Path,
    ):

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path.write_text(
            report,
            encoding="utf-8",
        )
