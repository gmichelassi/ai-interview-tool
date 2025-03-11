from flask import jsonify


def not_found_error_handler(_):
    return jsonify({"error": "The requested URL was not found on the server. Please contact an admin or try again later."}), 404


def internal_error_handler(_):
    return jsonify({"error": "Something unexpected happened. Please contact an admin or try again later."}), 500
