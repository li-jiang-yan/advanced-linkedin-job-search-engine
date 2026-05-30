"""Flask application factory for the LinkedIn job search engine."""

from flask import Flask

from app.routes import main


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
