from dataclasses import dataclass, field

from app.models.course import Course


@dataclass
class Semester:
    """
    Represents one semester.
    """

    name: str

    courses: list[Course] = field(default_factory=list)
