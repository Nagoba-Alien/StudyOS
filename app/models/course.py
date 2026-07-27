from dataclasses import dataclass, field

from app.models.pdf_document import PDFDocument


@dataclass
class Course:
    """
    Represents one course.
    """

    name: str

    pdfs: list[PDFDocument] = field(default_factory=list)
