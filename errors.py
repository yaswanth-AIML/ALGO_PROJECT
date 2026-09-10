"""Global HTTP error handlers."""

from flask import jsonify


def register_error_handlers(app):
    """Register JSON error handlers for common HTTP errors."""

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"success": False, "error": "Resource not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        return jsonify({"success": False, "error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"success": False, "error": "Internal server error."}), 500
