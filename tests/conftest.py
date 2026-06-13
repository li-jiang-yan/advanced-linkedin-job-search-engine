"""Pytest fixtures for the Flask application."""

import pytest

from app import create_app


@pytest.fixture
def app():
    """Create a configured Flask app for tests."""
    app = create_app()
    app.config.update(TESTING=True)

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    """Provide a Flask test client."""
    with app.test_client() as client:
        yield client
