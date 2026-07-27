import json
from datetime import date
from pathlib import Path


HISTORY_FILE = Path(
    "data/revision_history.json"
)


class RevisionHistory:
    """
    Handles storage and retrieval of
    revision progress.
    """

    def __init__(self):

        self.history = self.load()

    def load(self) -> dict:
        """
        Load revision history from disk.
        """

        if not HISTORY_FILE.exists():

            return {}

        with open(
            HISTORY_FILE,
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def save(self):
        """
        Save revision history to disk.
        """

        HISTORY_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.history,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def get_key(
        self,
        course: str,
        title: str,
    ) -> str:
        """
        Creates a unique identifier
        for a study resource.
        """

        return f"{course}/{title}"

    def get(
        self,
        course: str,
        title: str,
    ) -> dict:

        key = self.get_key(
            course,
            title,
        )

        return self.history.get(
            key,
            {
                "last_reviewed": None,
                "review_count": 0,
                "confidence": None,
                "completed": False,
            },
        )

    def update(
        self,
        course: str,
        title: str,
        confidence: int | None = None,
        completed: bool | None = None,
    ):
        """
        Update revision information.
        """

        key = self.get_key(
            course,
            title,
        )

        if key not in self.history:

            self.history[key] = {
                "last_reviewed": None,
                "review_count": 0,
                "confidence": None,
                "completed": False,
            }

        entry = self.history[key]

        entry["last_reviewed"] = (
            str(date.today())
        )

        entry["review_count"] += 1

        if confidence is not None:

            entry["confidence"] = confidence

        if completed is not None:

            entry["completed"] = completed

        self.save()
