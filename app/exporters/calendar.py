from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar",
]


class CalendarExporter:
    """
    Exports StudyOS revision sessions
    to Google Calendar.
    """

    def __init__(
        self,
        credentials_path: Path = Path("credentials.json"),
        token_path: Path = Path("calendar_token.json"),
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

        if creds is None or not creds.valid:

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
            "calendar",
            "v3",
            credentials=creds,
        )

    def export(
        self,
        session,
        calendar_id: str = "primary",
        start_hour: int = 9,
        break_minutes: int = 5,
    ):

        service = self._authenticate()

        current = datetime.now().replace(
            hour=start_hour,
            minute=0,
            second=0,
            microsecond=0,
        )

        for item in session.items:

            start = current

            end = start + timedelta(
                minutes=item.estimated_minutes
            )

            event = {

                "summary": (
                    f"{item.course} — {item.title}"
                ),

                "description": (
                    f"Difficulty: {item.difficulty_score}\n"
                    f"Priority: {item.priority:.2f}\n"
                    f"Estimated Time: "
                    f"{item.estimated_minutes} minutes"
                ),

                "start": {

                    "dateTime": start.isoformat(),

                    "timeZone": "Asia/Kolkata",

                },

                "end": {

                    "dateTime": end.isoformat(),

                    "timeZone": "Asia/Kolkata",

                },

            }

            service.events().insert(

                calendarId=calendar_id,

                body=event,

            ).execute()

            print(
                f"Created calendar event: "
                f"{item.course} - {item.title}"
            )

            current = end + timedelta(
                minutes=break_minutes
            )
