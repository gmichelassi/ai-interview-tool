from datetime import datetime, timedelta

import requests

from logger import Log
from services import RealtimeConversation
from utils.interview_prompt import interview_prompt, position_info, candidate_info

log = Log()


BASE_URL = 'http://localhost:5001'


def health():
    request_url = 'api/health'
    response = requests.get(f'{BASE_URL}/{request_url}')

    log.info(f'Health Response {response.json()}')


def create_meeting():
    request_url = 'api/schedule_interview'
    response = requests.post(f'{BASE_URL}/{request_url}', json={
        'candidateEmail': 'gabrielmichelassi@usp.br',
        'startTime': (datetime.now() + timedelta(seconds=30)).isoformat(),
        'endTime': (datetime.now() + timedelta(hours=1)).isoformat()
    })

    log.info(response.json())

def realtime_conversation_with_assistant():
    system_prompt = interview_prompt.format(position="Junior Frontend Developer", candidate_info=candidate_info, position_info=position_info)

    conversation = RealtimeConversation(system_prompt=system_prompt)
    conversation.run()



if __name__ == '__main__':
    health()
    create_meeting()

    input('Press Enter to start the conversation')
    realtime_conversation_with_assistant()
