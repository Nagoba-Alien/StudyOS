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

from app.planner.item_generator import (
    RevisionItemGenerator,
)

from app.storage.revision_store import (
    RevisionStore,
)


def process_library():
    """
    Download every PDF, extract text,
    clean it, save it,
    populate metadata,
    generate AI artifacts,
    and create revision items.
    """

    service = get_drive_service()

    library = build_drive_tree()

    ai_generator = AIArtifactGenerator()

    revision_generator = RevisionItemGenerator()

    revision_store = RevisionStore()

    total = 0
    successful = 0
    failed = 0

    for semester in library.semesters:

        print(f"\n===== {semester.name} =====")

        for course in semester.courses:

            print(f"\nCourse: {course.name}")

            for pdf in course.pdfs:

                print(f"\nProcessing: {pdf.name}")

                try:

                    # ----------------------------------------
                    # Download PDF
                    # ----------------------------------------

                    download_pdf(
                        service,
                        pdf.file_id,
                        pdf.local_pdf_path,
                    )

                    # ----------------------------------------
                    # Extract text
                    # ----------------------------------------

                    raw_text = extract_text(
                        pdf.local_pdf_path
                    )

                    # ----------------------------------------
                    # Clean text
                    # ----------------------------------------

                    cleaned_text = clean_text(
                        raw_text
                    )

                    # ----------------------------------------
                    # Save cleaned text
                    # ----------------------------------------

                    save_text(
                        cleaned_text,
                        pdf.local_text_path,
                    )

                    # ----------------------------------------
                    # Populate metadata
                    # ----------------------------------------

                    populate_metadata(pdf)

                    print(
                        f"✓ Pages      : {pdf.page_count}"
                    )

                    print(
                        f"✓ Words      : {pdf.word_count}"
                    )

                    print(
                        f"✓ Characters : {pdf.character_count}"
                    )

                    print(
                        f"✓ Read Time  : "
                        f"{pdf.estimated_read_time} min"
                    )

                    # ----------------------------------------
                    # Generate AI artifacts
                    # ----------------------------------------

                    print(
                        "\nGenerating AI artifacts..."
                    )

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

                    print(
                        "✓ AI artifacts generated."
                    )

                    # ----------------------------------------
                    # Create Revision Item
                    # ----------------------------------------

                    revision_item = (
                        revision_generator.generate(

                            course=course.name,

                            title=stem,

                            pdf_path=(
                                pdf.local_pdf_path
                            ),

                            text_path=(
                                pdf.local_text_path
                            ),

                            summary_path=(
                                ai_output_dir
                                / f"{stem}_summary.md"
                            ),

                            notes_path=(
                                ai_output_dir
                                / f"{stem}_notes.md"
                            ),

                            flashcards_path=(
                                ai_output_dir
                                / f"{stem}_flashcards.json"
                            ),

                            topics_path=(
                                ai_output_dir
                                / f"{stem}_topics.json"
                            ),

                            difficulty_path=(
                                ai_output_dir
                                / f"{stem}_difficulty.json"
                            ),

                            artifact=artifact,

                            word_count=(
                                pdf.word_count
                            ),
                        )
                    )

                    revision_store.save(
                        [revision_item]
                    )

                    print(
                        "✓ Revision item created."
                    )

                    successful += 1

                except Exception as e:

                    failed += 1

                    print(
                        "\n" + "-" * 60
                    )

                    print(
                        f"✗ Failed to process: {pdf.name}"
                    )

                    print(
                        f"Error Type : {type(e).__name__}"
                    )

                    print(
                        f"Reason     : {e}"
                    )

                    print(
                        "-" * 60
                    )

                finally:

                    total += 1

    print(
        "\n" + "=" * 60
    )

    print(
        "Pipeline Finished"
    )

    print(
        "=" * 60
    )

    print(
        f"Successful : {successful}"
    )

    print(
        f"Failed     : {failed}"
    )

    print(
        f"Total      : {total}"
    )

    print(
        "=" * 60
    )


if __name__ == "__main__":

    process_library()
