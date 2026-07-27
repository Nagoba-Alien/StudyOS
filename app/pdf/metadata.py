import fitz

from app.config import WORDS_PER_MINUTE
from app.models import PDFDocument


def populate_metadata(pdf: PDFDocument):
    """
    Populate metadata for a PDFDocument.
    """

    document = fitz.open(pdf.local_pdf_path)

    pdf.page_count = len(document)

    text = []

    for page in document:
        text.append(page.get_text())

    document.close()

    full_text = "\n".join(text)

    pdf.character_count = len(full_text)

    pdf.word_count = len(full_text.split())

    pdf.estimated_read_time = max(
        1,
        round(pdf.word_count / WORDS_PER_MINUTE),
    )
