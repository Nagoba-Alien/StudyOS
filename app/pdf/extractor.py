from pathlib import Path

import fitz


def extract_text(pdf_path: Path) -> str:
    """
    Extract all text from a PDF.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Extracted text as a string.
    """

    document = fitz.open(pdf_path)

    text = []

    for page in document:
        text.append(page.get_text())

    document.close()

    return "\n".join(text)


def save_text(text: str, output_path: Path):
    """
    Save extracted text to a file.
    """

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_path,
        "w",
        encoding="utf-8",
    ) as file:

        file.write(text)
