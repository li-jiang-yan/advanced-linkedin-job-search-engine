"""HTTP routes for the application."""

from flask import (
    Blueprint,
    render_template,
    request,
)

from lib.search import search_jobs

main = Blueprint("main", __name__)


@main.route("/")
def hello():
    """Return a simple hello page."""
    return render_template("index.html")


@main.route("/health")
def health():
    """Return a health-check sequence."""
    return {"status": "ok"}, 200


@main.route("/search", methods=["GET"])
def search():
    """Search for jobs with the LinkedIn API"""
    return search_jobs(request)
