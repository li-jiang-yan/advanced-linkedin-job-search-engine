"""HTTP routes for the application."""

import json

from flask import (
    Blueprint,
    jsonify,
    render_template,
    request,
)

from lib.findapp import fetch_urls, match_tokens

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


@main.route("/urls", methods=["GET"])
def urls():
    """Get job post URLs to look from"""
    query_params = request.args.to_dict(flat=True)
    result = fetch_urls(query_params)
    return jsonify(result)


@main.route("/tokens", methods=["GET"])
def tokens():
    """Get matching tokens present in the job description in a given URL"""
    url = request.args.get("url")
    tokens = json.loads(request.args.get("tokens"))
    result = match_tokens(url, tokens)
    return jsonify(result)
