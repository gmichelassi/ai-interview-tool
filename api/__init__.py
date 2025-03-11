from flask import Blueprint

from .health import health_blueprint
from .schedule_interview import schedule_interview_blueprint

blueprint = Blueprint('app', __name__)

blueprint.register_blueprint(health_blueprint, url_prefix='/')
blueprint.register_blueprint(schedule_interview_blueprint, url_prefix='/schedule_interview')
