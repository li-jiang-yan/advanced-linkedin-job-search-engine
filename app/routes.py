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
    return _render_index([])


@main.route("/health")
def health():
    """Return a health-check sequence."""
    return {"status": "ok"}, 200


@main.route("/search", methods=["GET"])
def search():
    """Search for jobs with the LinkedIn API"""
    query_params = request.args.to_dict(flat=True)
    jobs = search_jobs(query_params)
    return _render_index(jobs, query_params)


def _render_index(jobs, query_params=None):
    """Render the search page with a consistent template context."""
    return render_template(
        "index.html",
        jobs=jobs,
        query=query_params or {},
    )
