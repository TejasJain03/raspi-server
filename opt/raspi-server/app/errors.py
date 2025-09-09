from flask import jsonify

class APIError(Exception):
    status_code = 400

    def __init__(self, error="bad_request", message="Bad request", status_code=None, payload=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code
        self.error = error
        self.message = message
        self.payload = payload or {}

    def to_dict(self):
        rv = dict(self.payload)
        rv["error"] = self.error
        rv["message"] = self.message
        return rv


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(e: APIError):
        resp = jsonify(e.to_dict())
        resp.status_code = e.status_code
        return resp

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({"error": "not_found", "message": "Resource not found"}), 404

    @app.errorhandler(405)
    def handle_405(e):
        return jsonify({"error": "method_not_allowed", "message": "Method not allowed"}), 405

    @app.errorhandler(413)
    def handle_413(e):
        return jsonify({"error": "payload_too_large", "message": "Request payload too large"}), 413

    @app.errorhandler(Exception)
    def handle_exception(e):
        # In production you might want to hide internal errors
        message = str(e)
        return jsonify({"error": "internal_server_error", "message": message}), 500
