from pathlib import Path

from googleapiclient.http import MediaIoBaseDownload

from app.auth.auth import authenticate


def get_drive_service():
    """
    Return an authenticated Google Drive service.
    """
    return authenticate()


def download_pdf(service, file_id: str, destination: Path):
    """
    Download a PDF from Google Drive.

    Args:
        service: Authenticated Google Drive service.
        file_id: Google Drive file ID.
        destination: Local destination.
    """

    destination.parent.mkdir(parents=True, exist_ok=True)

    request = service.files().get_media(fileId=file_id)

    with open(destination, "wb") as file:

        downloader = MediaIoBaseDownload(file, request)

        done = False

        while not done:

            status, done = downloader.next_chunk()

            if status:
                print(
                    f"{destination.name}: "
                    f"{int(status.progress()*100)}%"
                )

    print(f"✓ Downloaded {destination.name}")
