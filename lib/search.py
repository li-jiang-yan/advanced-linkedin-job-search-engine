"""Search helpers for LinkedIn job listings."""

import html
import json
import re
import unicodedata
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

LINKEDIN_SEARCH_URL = (
    "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
)

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

_BOILERPLATE_PHRASES = (
    "summary",
    "description",
    "job description",
    "role description",
    "job overview",
    "about the team",
    "what the role is",
    "what you will be working on",
    "what we are looking for",
    "responsibilities",
    "requirements",
    "minimum qualifications",
    "preferred qualifications",
    "must have",
    "nice to have",
    "key responsibilities",
)

_WORD_FIXES = ((r"\bdisterent\b", "different"),)


def search_jobs(params):
    """Fetch LinkedIn job cards for the provided query parameters."""
    query_params = dict(params)
    number = int(query_params.pop("number", 1))
    query_string = urlencode(query_params)
    jobs = []

    start = 0
    while len(jobs) < number:  # make sure we have parsed the given number of jobs
        try:
            url = _build_search_url(query_string, start)
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
            response.raise_for_status()
        except Exception as _:
            # When we reached an exception (especially at requests.get), we
            # simply increment start and try again
            start += 1
        else:
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
        result["description"] = _clean_description(result["description"])
        result["tokens"] = _tokenize(result["description"])
    except Exception as _:
        return None
    else:
        return result


def _clean_description(description):
    if not description:
        return ""

    text = html.unescape(str(description))
    text = BeautifulSoup(text, "html.parser").get_text(" ")
    text = _repair_mojibake(text)
    text = unicodedata.normalize("NFKC", text)
    text = text.translate(
        str.maketrans(
            {
                "\u2018": "'",
                "\u2019": "'",
                "\u201c": '"',
                "\u201d": '"',
                "\u2013": "-",
                "\u2014": "-",
            }
        )
    )
    text = text.replace("\xa0", " ")
    text = re.sub(r"[\r\n\t]+", " ", text)

    boilerplate_pattern = (
        r"\b(?:"
        + "|".join(re.escape(phrase) for phrase in _BOILERPLATE_PHRASES)
        + r")\b[:\s-]*"
    )
    text = re.sub(boilerplate_pattern, " ", text, flags=re.IGNORECASE)
    text = re.sub(r"[^0-9A-Za-z\s']", " ", text)
    for pattern, replacement in _WORD_FIXES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def _repair_mojibake(text):
    """Best-effort repair for UTF-8 text decoded as Latin-1/CP1252."""
    if not text:
        return ""

    for encoding in ("cp1252", "latin1"):
        try:
            return text.encode(encoding).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue

    return text


def _tokenize(text):
    """Converts a given text string to individual word tokens."""
    vectorizer = CountVectorizer()
    tokenizer = vectorizer.build_tokenizer()
    return list(tokenizer(text))
