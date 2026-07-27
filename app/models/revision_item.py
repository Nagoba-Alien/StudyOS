from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RevisionItem:
    """
    Represents one study resource that can
    be scheduled for revision.
    """

    course: str
    title: str

    pdf_path: Path
    text_path: Path

    summary_path: Path
    notes_path: Path
    flashcards_path: Path
    topics_path: Path
    difficulty_path: Path

    word_count: int
    estimated_minutes: int

    difficulty_score: int

    topics: list[str] = field(default_factory=list)

    priority: float = 0.0

    last_reviewed: str | None = None
