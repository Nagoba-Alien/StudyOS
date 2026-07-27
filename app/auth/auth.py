from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these scopes, delete token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Authentication files
CREDENTIALS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "token.json"


def authenticate():
    """
    Authenticate the user with Google OAuth and return
    an authenticated Google Drive service.
    """

    creds = None

    # Load existing token if available
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If there are no valid credentials, ask the user to log in
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save the credentials for future runs
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    return service


if __name__ == "__main__":
    print("Authenticating with Google Drive...")

    service = authenticate()

    print("Authentication successful!")
    print(f"Service: {service}")
