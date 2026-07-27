from pathlib import Path

from app.ai.artifact_generator import AIArtifactGenerator
from app.drive.drive import build_drive_tree
from app.pdf.cleaner import clean_text
from app.pdf.downloader import (
    download_pdf,
    get_drive_service,
)
from app.pdf.extractor import (
    extract_text,
    save_text,
)
from app.pdf.metadata import populate_metadata


def process_library():
    """
    Download every PDF, extract text,
    clean it, save it,
    populate metadata,
    and generate AI study artifacts.
    """

    service = get_drive_service()

    library = build_drive_tree()

    ai_generator = AIArtifactGenerator()

    total = 0

    for semester in library.semesters:

        print(f"\n===== {semester.name} =====")

        for course in semester.courses:

            print(f"\nCourse: {course.name}")

            for pdf in course.pdfs:

                print(f"\nProcessing: {pdf.name}")

                # ----------------------------------------
                # Download PDF
                # ----------------------------------------

                download_pdf(
                    service,
                    pdf.file_id,
                    pdf.local_pdf_path,
                )

                # ----------------------------------------
                # Extract & clean text
                # ----------------------------------------

                raw_text = extract_text(
                    pdf.local_pdf_path
                )

                cleaned_text = clean_text(
                    raw_text
                )

                save_text(
                    cleaned_text,
                    pdf.local_text_path,
                )

                # ----------------------------------------
                # Populate metadata
                # ----------------------------------------

                populate_metadata(pdf)

                print(f"✓ Pages      : {pdf.page_count}")
                print(f"✓ Words      : {pdf.word_count}")
                print(f"✓ Characters : {pdf.character_count}")
                print(
                    f"✓ Read Time  : "
                    f"{pdf.estimated_read_time} min"
                )

                # ----------------------------------------
                # Generate AI artifacts
                # ----------------------------------------

                print("Generating AI artifacts...")

                artifact = ai_generator.generate(
                    cleaned_text
                )

                ai_output_dir = (
                    Path(pdf.local_text_path).parent
                    / "ai"
                )

                stem = Path(
                    pdf.local_text_path
                ).stem

                ai_generator.save(
                    artifact,
                    ai_output_dir,
                    stem,
                )

                print("✓ AI artifacts generated.")

                total += 1

    print("\n" + "=" * 60)
    print(f"Successfully processed {total} PDF(s).")
    print("=" * 60)


if __name__ == "__main__":
    process_library()
