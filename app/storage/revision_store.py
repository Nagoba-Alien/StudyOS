import json
from pathlib import Path

from app.models.revision_item import RevisionItem


class RevisionStore:
    """
    Persistent storage for revision items.
    """

    def __init__(
        self,
        path: Path = Path(
            "data/revision_items.json"
        ),
    ):

        self.path = path

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        items: list[RevisionItem],
    ):
        """
        Add new revision items while
        preserving existing ones.
        """

        existing = self.load()

        for item in items:

            existing = self.remove_duplicate(
                existing,
                item,
            )

            existing.append(item)

        self.write(existing)

    def load(self) -> list[RevisionItem]:
        """
        Load stored revision items.
        """

        if not self.path.exists():

            return []

        with open(
            self.path,
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return [
            self.deserialize(item)
            for item in data
        ]

    def remove_duplicate(
        self,
        items: list[RevisionItem],
        new_item: RevisionItem,
    ) -> list[RevisionItem]:
        """
        Prevent duplicate revision items.
        """

        return [
            item
            for item in items
            if not (
                item.course == new_item.course
                and
                item.title == new_item.title
            )
        ]

    def write(
        self,
        items: list[RevisionItem],
    ):
        """
        Save revision items.
        """

        data = [
            self.serialize(item)
            for item in items
        ]

        with open(
            self.path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False,
            )

    def serialize(
        self,
        item: RevisionItem,
    ) -> dict:
        """
        Convert RevisionItem into JSON.
        """

        return {

            "course": item.course,

            "title": item.title,

            "pdf_path": str(
                item.pdf_path
            ),

            "text_path": str(
                item.text_path
            ),

            "summary_path": str(
                item.summary_path
            ),

            "notes_path": str(
                item.notes_path
            ),

            "flashcards_path": str(
                item.flashcards_path
            ),

            "topics_path": str(
                item.topics_path
            ),

            "difficulty_path": str(
                item.difficulty_path
            ),

            "word_count": item.word_count,

            "estimated_minutes":
                item.estimated_minutes,

            "difficulty_score":
                item.difficulty_score,

            "topics": item.topics,

            "priority": item.priority,

            "last_reviewed":
                item.last_reviewed,
        }

    def deserialize(
        self,
        data: dict,
    ) -> RevisionItem:
        """
        Convert JSON back into RevisionItem.
        """

        return RevisionItem(

            course=data["course"],

            title=data["title"],

            pdf_path=Path(
                data["pdf_path"]
            ),

            text_path=Path(
                data["text_path"]
            ),

            summary_path=Path(
                data["summary_path"]
            ),

            notes_path=Path(
                data["notes_path"]
            ),

            flashcards_path=Path(
                data["flashcards_path"]
            ),

            topics_path=Path(
                data["topics_path"]
            ),

            difficulty_path=Path(
                data["difficulty_path"]
            ),

            word_count=data["word_count"],

            estimated_minutes=data[
                "estimated_minutes"
            ],

            difficulty_score=data[
                "difficulty_score"
            ],

            topics=data.get(
                "topics",
                [],
            ),

            priority=data.get(
                "priority",
                0.0,
            ),

            last_reviewed=data.get(
                "last_reviewed"
            ),
        )
