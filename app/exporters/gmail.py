from __future__ import annotations

import base64
from email.message import EmailMessage
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
]


class GmailExporter:
    """
    Sends StudyOS reports using the Gmail API.
    """

    def __init__(
        self,
        credentials_path: Path = Path("credentials.json"),
        token_path: Path = Path("token.json"),
    ):

        self.credentials_path = credentials_path
        self.token_path = token_path

    def _authenticate(self):

        creds = None

        if self.token_path.exists():

            creds = Credentials.from_authorized_user_file(
                self.token_path,
                SCOPES,
            )

        if (
            creds is None
            or not creds.valid
        ):

            if (
                creds
                and creds.expired
                and creds.refresh_token
            ):

                creds.refresh(
                    Request()
                )

            else:

                flow = (
                    InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path,
                        SCOPES,
                    )
                )

                creds = flow.run_local_server(
                    port=0
                )

            self.token_path.write_text(
                creds.to_json(),
                encoding="utf-8",
            )

        return build(
            "gmail",
            "v1",
            credentials=creds,
        )

    def export(
        self,
        sender: str,
        recipient: str,
        subject: str,
        body: str,
    ):

        service = self._authenticate()

        message = EmailMessage()

        message["To"] = recipient
        message["From"] = sender
        message["Subject"] = subject

        message.set_content(body)

        encoded_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        service.users().messages().send(

            userId="me",

            body={
                "raw": encoded_message
            },

        ).execute()

        print(
            f"Email sent successfully to {recipient}"
        )
