"""Search helpers for LinkedIn job listings."""

import json
import re
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
        for element in soup.find_all("li"):
            job = _parse_job_html(element)
            if job:
                jobs.append(job)
        start += len(soup.find_all("li"))

    return jobs


def _build_search_url(query_string, start):
    if query_string:
        return f"{LINKEDIN_SEARCH_URL}?{query_string}&start={start}"
    return f"{LINKEDIN_SEARCH_URL}?start={start}"


def _parse_job_html(soup):
    try:
        result = {}

        # Extract info from input soup
        link_el = soup.select_one(".base-card__full-link").get("href")
        result["link"] = link_el

        # Extract info from soup obtained from link_el
        response = requests.get(link_el, headers=DEFAULT_HEADERS, timeout=30)
        soup = BeautifulSoup(response.text, "html.parser")
        result.update(
            json.loads(soup.find("script", {"type": "application/ld+json"}).string)
        )
        criteria = {
            item.select_one(".description__job-criteria-subheader")
            .get_text()
            .strip()
            .lower(): item.select_one(".description__job-criteria-text")
            .get_text()
            .strip()
            for item in soup.select(".description__job-criteria-item")
        }
        result["seniority"] = criteria["seniority level"]
        result["function"] = criteria["job function"]
        result["industry"] = re.split(r",(?=\S)", result["industry"])

    except Exception as _:
        return None
    else:
        return result
