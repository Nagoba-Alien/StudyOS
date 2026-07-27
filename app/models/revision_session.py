from dataclasses import dataclass, field

from app.models.revision_item import RevisionItem


@dataclass
class RevisionSession:
    """
    Represents one generated study session.
    """

    date: str

    items: list[RevisionItem] = field(
        default_factory=list
    )

    total_minutes: int = 0
