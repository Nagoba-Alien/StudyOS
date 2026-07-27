import json
from datetime import date
from pathlib import Path


EXAMS_FILE = Path(
    "data/exams.json"
)


class ExamCalendar:
    """
    Handles exam dates.
    """

    def __init__(self):

        self.exams = self.load()

    def load(self):

        if not EXAMS_FILE.exists():

            return {}

        with open(
            EXAMS_FILE,
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def save(self):

        EXAMS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            EXAMS_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.exams,
                file,
                indent=4,
            )

    def add_exam(
        self,
        course: str,
        exam_date: str,
    ):

        self.exams[course] = {
            "exam_date": exam_date
        }

        self.save()

    def days_until_exam(
        self,
        course: str,
    ):

        if course not in self.exams:

            return None

        exam_date = date.fromisoformat(
            self.exams[course]["exam_date"]
        )

        return (
            exam_date - date.today()
        ).days
