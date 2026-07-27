from pathlib import Path

from app.models import RevisionItem, AIArtifact


class RevisionItemGenerator:
    """
    Converts processed AI artifacts into
    revision items for the planner.
    """

    def generate(
        self,
        course: str,
        title: str,
        pdf_path: Path,
        text_path: Path,
        summary_path: Path,
        notes_path: Path,
        flashcards_path: Path,
        topics_path: Path,
        difficulty_path: Path,
        artifact: AIArtifact,
        word_count: int,
    ) -> RevisionItem:
        """
        Create a revision item from
        a processed document.
        """

        estimated_minutes = self.estimate_time(
            word_count,
            artifact.difficulty.score,
        )

        return RevisionItem(

            course=course,

            title=title,

            pdf_path=pdf_path,

            text_path=text_path,

            summary_path=summary_path,

            notes_path=notes_path,

            flashcards_path=flashcards_path,

            topics_path=topics_path,

            difficulty_path=difficulty_path,

            word_count=word_count,

            estimated_minutes=estimated_minutes,

            difficulty_score=(
                artifact.difficulty.score
            ),

            topics=artifact.topics,
        )

    def estimate_time(
        self,
        word_count: int,
        difficulty: int,
    ) -> int:
        """
        Estimate revision duration.
        """

        reading_time = (
            word_count / 200
        )

        difficulty_multiplier = (
            1 + (difficulty * 0.1)
        )

        return max(
            5,
            round(
                reading_time
                * difficulty_multiplier
            ),
        )
