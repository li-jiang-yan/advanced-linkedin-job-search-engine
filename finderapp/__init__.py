"""Flask application factory for the LinkedIn job finder."""

from flask import Flask

from finderapp.routes import main


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.register_blueprint(main)
    return app
