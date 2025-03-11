from flask import Blueprint, jsonify

health_blueprint = Blueprint('health', __name__)


@health_blueprint.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})
