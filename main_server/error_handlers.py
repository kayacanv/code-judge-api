from flask import jsonify
from custom_exceptions import InvalidInputError, MissingParameterError


def register_error_handlers(app):
    @app.errorhandler(InvalidInputError)
    def handle_invalid_input_error(e):
        response = jsonify({"error": "Invalid input", "message": e.message})
        response.status_code = 400
        return response

    @app.errorhandler(MissingParameterError)
    def handle_missing_parameter_error(e):
        response = jsonify(
            {"error": "Missing parameter", "message": e.message})
        response.status_code = 400
        return response

    @app.errorhandler(500)
    def handle_internal_server_error(e):
        response = jsonify(
            {"error": "Internal server error", "details": str(e)})
        response.status_code = 500
        return response
