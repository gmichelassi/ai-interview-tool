import os
from typing import Literal

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pydantic import BaseModel


class MeetingTime(BaseModel):
    dateTime: str
    timeZone: Literal['America/Sao_Paulo'] = 'America/Sao_Paulo'


class MeetingAttendee(BaseModel):
    email: str


class GoogleCalendar:
    def __init__(self):
        SCOPES = ['https://www.googleapis.com/auth/calendar']
        CREDS_PATH = 'credentials/google-client.json'
        TOKEN_PATH = 'credentials/token.json'

        self.creds = None

        if os.path.exists(TOKEN_PATH):
            self.creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

        if not self.creds or not self.creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_PATH, SCOPES)
            creds = flow.run_local_server(host='localhost', port=8080, open_browser=True, browser='safari')

            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())

        self.service = build('calendar', 'v3', credentials=self.creds)

    def create_event(
            self,
            attendees: list[MeetingAttendee],
            start_time: MeetingTime,
            end_time: MeetingTime,
            title: str,
            description: str
    ):
        event_metadata = {
            'summary': title,
            'location': 'Online',
            'description': description,
            'start': start_time.model_dump(),
            'end': end_time.model_dump(),
            'conferenceData': {
                'createRequest': {
                    'requestId': 'unique-request-id'
                }
            },
            'attendees': [attendee.model_dump() for attendee in attendees],
        }

        event = self.service.events().insert(calendarId='primary', body=event_metadata, conferenceDataVersion=1).execute()

        return event
