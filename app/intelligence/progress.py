from datetime import date
from pathlib import Path
import json


class ProgressTracker:
    """
    Tracks learning progress over time.
    """

    def __init__(
        self,
        path: Path | str = Path(
            "data/progress.json"
        ),
    ):

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.history = self.load()

    def load(self) -> dict:
        """
        Load stored progress history.
        """

        if not self.path.exists():

            return {}

        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    def save(self):
        """
        Save progress history.
        """

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.history,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def record(
        self,
        course: str,
        title: str,
        mastery: float,
        retention: float,
    ):
        """
        Store a learning progress snapshot.
        """

        key = f"{course}/{title}"

        if key not in self.history:

            self.history[key] = []

        self.history[key].append(
            {
                "date": str(date.today()),

                "mastery": mastery,

                "retention": retention,
            }
        )

        self.save()

    def get_history(
        self,
        course: str,
        title: str,
    ) -> list:
        """
        Retrieve stored progress history.
        """

        key = f"{course}/{title}"

        return self.history.get(
            key,
            [],
        )

    def improvement(
        self,
        course: str,
        title: str,
    ) -> float:
        """
        Calculate mastery improvement
        from first recorded value.
        """

        history = self.get_history(
            course,
            title,
        )

        if len(history) < 2:

            return 0.0

        first_mastery = history[0]["mastery"]

        latest_mastery = history[-1]["mastery"]

        return round(
            latest_mastery - first_mastery,
            2,
        )
