from app.auth.auth import authenticate

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
    Build the StudyOS folder hierarchy.

    Structure:

    StudyOS
        ├── Semester
        │      ├── Course
        │      │      ├── PDFs
    """

    service = get_drive_service()

    study_root = find_folder(service, "StudyOS")

    if study_root is None:
        raise FileNotFoundError(
            "StudyOS folder not found in Google Drive."
        )

    tree = {
        "id": study_root["id"],
        "name": study_root["name"],
        "semesters": [],
    }

    semester_folders = list_subfolders(
        service,
        study_root["id"],
    )

    for semester in semester_folders:

        semester_node = {
            "id": semester["id"],
            "name": semester["name"],
            "courses": [],
        }

        course_folders = list_subfolders(
            service,
            semester["id"],
        )

        for course in course_folders:

            course_node = {
                "id": course["id"],
                "name": course["name"],
                "pdfs": [],
            }

            pdfs = list_pdfs(
                service,
                course["id"],
            )

            for pdf in pdfs:

                course_node["pdfs"].append(
                    {
                        "id": pdf["id"],
                        "name": pdf["name"],
                    }
                )

            semester_node["courses"].append(course_node)

        tree["semesters"].append(semester_node)

    return tree


def print_tree(tree):
    """
    Pretty-print the Drive hierarchy.
    """

    print(f"\n📁 {tree['name']}")

    for semester in tree["semesters"]:

        print(f"\n├── 📂 {semester['name']}")

        for course in semester["courses"]:

            print(f"│   ├── 📘 {course['name']}")

            for pdf in course["pdfs"]:

                print(f"│   │   ├── 📄 {pdf['name']}")


if __name__ == "__main__":

    try:

        drive_tree = build_drive_tree()

        print_tree(drive_tree)

    except FileNotFoundError as e:

        print(e)
