from flask import Blueprint, jsonify, request

from integrations.google import GoogleCalendar
from integrations.google.calendar import MeetingAttendee, MeetingTime
from logger import Log
from scheduler.jobs import perform_interview
from utils import flask_scheduler

log = Log()

schedule_interview_blueprint = Blueprint('schedule_interview', __name__)


@schedule_interview_blueprint.route('/', methods=['POST'])
def schedule_interview_endpoint():
    candidate_email: str = request.json.get('candidateEmail')
    start_time = request.json.get('startTime')
    end_time = request.json.get('endTime')

    if not candidate_email:
        return jsonify({"error": "You must give a non-empty candidate_email"}), 400

    if not start_time or not end_time:
        return jsonify({"error": "You must give a non-empty start_time and end_time"}), 400

    meeting = GoogleCalendar().create_event(
        attendees=[MeetingAttendee(email='gabrielmichelassi78@gmail.com'), MeetingAttendee(email=candidate_email)],
        start_time=MeetingTime(dateTime=start_time, timeZone= 'America/Sao_Paulo'),
        end_time=MeetingTime(dateTime=end_time, timeZone= 'America/Sao_Paulo'),
        title="Interview",
        description="Interview with the candidate"
    )
    log.info(f"Event created succesfully")

    event_url = meeting.get('htmlLink')
    meeting_url = meeting['conferenceData']['entryPoints'][0]['uri']

    log.info(f"Event URL: {event_url} | Meeting URL: {meeting_url}")

    flask_scheduler.add_job(id='1234', func=perform_interview, trigger='date', run_date=start_time, args=[candidate_email, meeting_url], replace_existing=True)

    return jsonify({"event": event_url, "googleMeet": meeting_url}), 200
