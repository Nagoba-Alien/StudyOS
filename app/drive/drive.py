from pathlib import Path

from app.auth.auth import authenticate
from app.models import (
    Course,
    PDFDocument,
    Semester,
    StudyLibrary,
)

FOLDER_MIME = "application/vnd.google-apps.folder"


def get_drive_service():
    """
    Return an authenticated Google Drive service.
    """
    return authenticate()


def find_folder(service, folder_name):
    """
    Find a folder by name.
    Returns the first matching folder or None.
    """

    results = (
        service.files()
        .list(
            q=(
                f"mimeType='{FOLDER_MIME}' "
                f"and name='{folder_name}' "
                "and trashed=false"
            ),
            fields="files(id, name)",
            pageSize=10,
        )
        .execute()
    )

    folders = results.get("files", [])

    if not folders:
        return None

    return folders[0]


def list_subfolders(service, parent_id):
    """
    List all folders directly inside a parent folder.
    """

    results = (
        service.files()
        .list(
            q=(
                f"'{parent_id}' in parents "
                f"and mimeType='{FOLDER_MIME}' "
                "and trashed=false"
            ),
            fields="files(id, name)",
            pageSize=100,
            orderBy="name",
        )
        .execute()
    )

    return results.get("files", [])


def list_pdfs(service, parent_id):
    """
    List all PDFs directly inside a folder.
    """

    results = (
        service.files()
        .list(
            q=(
                f"'{parent_id}' in parents "
                "and mimeType='application/pdf' "
                "and trashed=false"
            ),
            fields="files(id, name)",
            pageSize=100,
            orderBy="name",
        )
        .execute()
    )

    return results.get("files", [])


def build_drive_tree():
    """
    Build the StudyOS library from Google Drive.
    """

    service = get_drive_service()

    study_root = find_folder(service, "StudyOS")

    if study_root is None:
        raise FileNotFoundError(
            "StudyOS folder not found in Google Drive."
        )

    library = StudyLibrary()

    semester_folders = list_subfolders(
        service,
        study_root["id"],
    )

    for semester_folder in semester_folders:

        semester = Semester(
            name=semester_folder["name"]
        )

        course_folders = list_subfolders(
            service,
            semester_folder["id"],
        )

        for course_folder in course_folders:

            course = Course(
                name=course_folder["name"]
            )

            pdfs = list_pdfs(
                service,
                course_folder["id"],
            )

            for pdf in pdfs:

                pdf_document = PDFDocument(
                    file_id=pdf["id"],
                    name=pdf["name"],
                    drive_path=(
                        f"{semester.name}/"
                        f"{course.name}/"
                        f"{pdf['name']}"
                    ),
                    local_pdf_path=(
                        Path("output")
                        / semester.name
                        / course.name
                        / pdf["name"]
                    ),
                    local_text_path=(
                        Path("output")
                        / semester.name
                        / course.name
                        / f"{Path(pdf['name']).stem}.txt"
                    ),
                )

                course.pdfs.append(pdf_document)

            semester.courses.append(course)

        library.semesters.append(semester)

    return library


def print_tree(library: StudyLibrary):
    """
    Pretty-print the StudyOS library.
    """

    print("\n📚 StudyOS")

    for semester in library.semesters:

        print(f"\n├── 📂 {semester.name}")

        for course in semester.courses:

            print(f"│   ├── 📘 {course.name}")

            for pdf in course.pdfs:

                print(f"│   │   ├── 📄 {pdf.name}")


if __name__ == "__main__":

    try:

        library = build_drive_tree()

        print_tree(library)

    except FileNotFoundError as e:

        print(e)

    except Exception as e:

        print(f"Unexpected error: {e}")
