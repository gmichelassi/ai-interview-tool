from integrations.google import GoogleCalendar
from integrations.google.calendar import MeetingAttendee, MeetingTime

from flask import Blueprint, jsonify, request
from utils import flask_scheduler
from scheduler.jobs import perform_interview

from logger import Log

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
        attendees=[MeetingAttendee(email=candidate_email)],
        start_time=MeetingTime(dateTime=start_time, timeZone= 'America/Sao_Paulo'),
        end_time=MeetingTime(dateTime=end_time, timeZone= 'America/Sao_Paulo'),
        title="Interview",
        description="Interview with the candidate"
    )
    log.info(f"Event created succesfully")

    flask_scheduler.add_job(id='1234', func=perform_interview, trigger='date', run_date=start_time, args=[candidate_email], replace_existing=True)

    return jsonify({"event": meeting.get('htmlLink'), "googleMeet": meeting['conferenceData']['entryPoints'][0]['uri']}), 200
