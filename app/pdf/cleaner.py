import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text.
    """

    # Remove Windows line endings
    text = text.replace("\r", "")

    # Remove repeated spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove multiple blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces before newlines
    text = re.sub(r" +\n", "\n", text)

    # Strip leading/trailing whitespace
    text = text.strip()

    return text
