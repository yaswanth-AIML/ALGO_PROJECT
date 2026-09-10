"""AlgoBench — Application factory and entry point."""
import logging
import os
from flask import Flask
from config import Config
from errors import register_error_handlers
from routes import register_blueprints


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    application = Flask(__name__)
    application.config.from_object(config_class)

    logging.basicConfig(
        level=logging.DEBUG if application.config["DEBUG"] else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    register_blueprints(application)
    register_error_handlers(application)
    return application


app = create_app()


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=debug, host="127.0.0.1", port=port)
