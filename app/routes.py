"""HTTP routes for the application."""

from flask import (
    Blueprint,
    render_template,
)

main = Blueprint("main", __name__)


@main.route("/")
def hello():
    """Return a simple hello page."""
    return render_template("index.html")


@main.route("/health")
def health():
    """Return a health-check sequence."""
    return {"status": "ok"}, 200
