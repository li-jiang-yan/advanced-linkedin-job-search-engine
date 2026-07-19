"""HTTP routes for the application."""

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from lib.search import search_jobs

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/search")
def hello():
    """Return a simple hello page."""
    return render_template("index.html")


@main.route("/health")
def health():
    """Return a health-check sequence."""
    return {"status": "ok"}, 200


@main.route("/run", methods=["GET"])
def run():
    """Search for jobs with the LinkedIn API"""
    query_params = request.args.to_dict(flat=True)
    result = search_jobs(query_params)
    return jsonify(result)
