import os

from dotenv import load_dotenv
from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS

from api import blueprint
from api.errors import internal_error_handler, not_found_error_handler
from application import ApplicationConfig
from scheduler import register_jobs
from utils import flask_scheduler

load_dotenv()

server = Flask(__name__)
server.config.from_object(ApplicationConfig())
server.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

flask_scheduler.init_app(server)
flask_scheduler.start()

server.register_blueprint(blueprint, url_prefix='/api')
server.register_error_handler(404, not_found_error_handler)
server.register_error_handler(500, internal_error_handler)

register_jobs(flask_scheduler)

CORS(server)


if __name__ == '__main__':
    server.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", default="5001")))
