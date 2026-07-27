from dataclasses import dataclass
from pathlib import Path


@dataclass
class PDFDocument:
    """
    Represents a single PDF in the StudyOS library.
    """

    file_id: str
    name: str

    drive_path: str

    local_pdf_path: Path
    local_text_path: Path

    page_count: int = 0
    word_count: int = 0
    character_count: int = 0
    estimated_read_time: int = 0
