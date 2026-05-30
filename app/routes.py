"""HTTP routes for the application."""

from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def hello():
    """Return a simple hello page."""
    return "Hello, World!"


@main.route("/health")
def health():
    """Return a health-check sequence."""
    return {"status": "ok"}, 200
