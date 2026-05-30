"""HTTP routes for the application."""

from flask import Blueprint

main = Blueprint("main", __name__)


@main.route("/")
def hello():
    """Return a simple hello page."""
    return "Hello, World!"
