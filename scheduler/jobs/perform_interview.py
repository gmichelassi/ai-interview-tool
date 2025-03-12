import asyncio

from logger import Log
from services import RealtimeConversation, join_meeting

log = Log()


def perform_interview(candidate_email: str, meeting_url: str):
    log.info(f'Starting interview with {candidate_email}!')
    meeting_controller = join_meeting(meeting_url=meeting_url)

    log.warning('The realtime conversation should happen here.')

    meeting_controller.quit()
