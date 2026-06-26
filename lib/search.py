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
        jobs.extend(
            _parse_job_html(element)
            for element in soup.find_all("li")
            if _parse_job_html(element)
        )
        start += len(soup.find_all("li"))

    return jobs


def _build_search_url(query_string, start):
    if query_string:
        return f"{LINKEDIN_SEARCH_URL}?{query_string}&start={start}"
    return f"{LINKEDIN_SEARCH_URL}?start={start}"


def _parse_job_html(soup):
    try:
        link_el = soup.select_one(".base-card__full-link").get("href")
        title_el = soup.select_one(".base-search-card__title").get_text().strip()
        company_el = soup.select_one(".base-search-card__subtitle").get_text().strip()
        location_el = soup.select_one(".job-search-card__location").get_text().strip()
        date_el = soup.select_one(".job-search-card__listdate").get("datetime")
    except Exception as _:
        return None
    else:
        return {
            "link": link_el,
            "title": title_el,
            "company": company_el,
            "location": location_el,
            "date_posted": date_el,
        }
