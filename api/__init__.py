from flask import Blueprint

from .health import health_blueprint

blueprint = Blueprint('app', __name__)

blueprint.register_blueprint(health_blueprint, url_prefix='/')
