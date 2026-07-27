from dataclasses import dataclass
from typing import List


@dataclass
class Flashcard:
    """
    Represents one flashcard.
    """

    question: str
    answer: str


@dataclass
class Difficulty:
    """
    Difficulty estimate for a document.
    """

    score: float
    reason: str


@dataclass
class AIArtifact:
    """
    Complete AI output for one document.
    """

    summary: str
    notes: str
    flashcards: List[Flashcard]
    topics: List[str]
    difficulty: Difficulty
