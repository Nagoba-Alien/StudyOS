from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class DailyBriefing:
    """
    Contains everything needed to generate
    today's study report.
    """

    date: str

    items: list["RevisionItem"] = field(
        default_factory=list
    )

    recommendations: list[dict] = field(
        default_factory=list
    )

    risks: list[dict] = field(
        default_factory=list
    )

    insights: list[str] = field(
        default_factory=list
    )

    total_minutes: int = 0

    average_mastery: float = 0.0

    average_retention: float = 0.0
