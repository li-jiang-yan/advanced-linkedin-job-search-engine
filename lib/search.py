"""Search helpers for LinkedIn job listings."""

from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup

LINKEDIN_SEARCH_URL = (
    "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def search_jobs(params):
    """Fetch LinkedIn job cards for the provided query parameters."""
    query_params = dict(params)
    number = int(query_params.pop("number", 1))
    query_string = urlencode(query_params)
    jobs = []

    start = 0
    while start < number:
        url = _build_search_url(query_string, start)
        response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        jobs.extend(str(element) for element in soup.find_all("li"))
        start += len(soup.find_all("li"))

    return jobs


def _build_search_url(query_string, start):
    if query_string:
        return f"{LINKEDIN_SEARCH_URL}?{query_string}&start={start}"
    return f"{LINKEDIN_SEARCH_URL}?start={start}"
