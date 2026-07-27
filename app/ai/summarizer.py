from pathlib import Path

from app.ai.client import GeminiClient


class Summarizer:
    """
    Generate a concise study summary from a cleaned text file.
    """

    def __init__(self):

        self.client = GeminiClient()

    def summarize_text(self, text: str) -> str:
        """
        Generate a structured study summary.
        """

        prompt = f"""
You are an expert university teaching assistant.

Your task is to produce concise, high-quality study summaries.

Summarise the following lecture notes.

Requirements:

- Begin with a short overview.
- Include the most important concepts.
- Use bullet points where appropriate.
- Preserve technical accuracy.
- Omit unnecessary details.
- Write in Markdown.
- Do NOT invent information.
- Keep the summary between 300 and 600 words.

Lecture Notes:

{text}
"""

        return self.client.generate(prompt)

    def summarize_file(
        self,
        input_file: Path,
        output_file: Path,
    ):
        """
        Read a text file, generate a summary,
        and save it as Markdown.
        """

        with open(
            input_file,
            "r",
            encoding="utf-8",
        ) as file:

            text = file.read()

        summary = self.summarize_text(text)

        output_file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as file:

            file.write(summary)

        print(
            f"✓ Summary saved to {output_file}"
        )


if __name__ == "__main__":

    input_path = Path("output/test.txt")

    output_path = Path("output/test_summary.md")

    summarizer = Summarizer()

    summarizer.summarize_file(
        input_path,
        output_path,
    )
