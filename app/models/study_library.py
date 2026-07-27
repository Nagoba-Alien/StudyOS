from dataclasses import dataclass, field

from app.models.semester import Semester


@dataclass
class StudyLibrary:
    """
    Root object of the entire StudyOS library.
    """

    semesters: list[Semester] = field(default_factory=list)
