from logger import Log
from services import join_meeting

log = Log()


def perform_interview(candidate_email: str, meeting_url: str):
    log.info(f'Starting interview with {candidate_email}!')
    meeting_controller = join_meeting(meeting_url=meeting_url)

    import time
    time.sleep(60 * 60)

    meeting_controller.quit()
