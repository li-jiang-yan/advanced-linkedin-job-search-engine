"""Helpers for the findapp Flask app."""

import html
import json
import re
import unicodedata
from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer

try:
    import ftfy
except ImportError:  # pragma: no cover - optional dependency fallback
    ftfy = None

LINKEDIN_API_URL = (
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


def fetch_urls(params):
    """Fetch LinkedIn job post URLs for the provided query parameters"""
    query_params = dict(params)
    query_string = urlencode(query_params)
    api_url = f"{LINKEDIN_API_URL}?{query_string}"
    while True:
        try:
            response = requests.get(api_url, headers=DEFAULT_HEADERS, timeout=30)
            response.raise_for_status()
        except Exception as _:
            pass
        else:
            soup = BeautifulSoup(response.text, "html.parser")
            job_cards = soup.find_all("li")
            return [_get_link_href(job_card) for job_card in job_cards]


def _get_link_href(job_card):
    """Get the full link href of a given job card"""
    return job_card.select_one(".base-card__full-link").get("href")


def match_tokens(url, tokens):
    """
    Check the job description in the given URL and find any word tokens matching what
    is given.
    """
    result = {"url": url, "matches": []}
    for _ in range(10):
        try:
            response = requests.get(url, headers=DEFAULT_HEADERS, timeout=30)
            soup = BeautifulSoup(response.text, "html.parser")
            json_script = json.loads(
                soup.find("script", {"type": "application/ld+json"}).string
            )
            title = json_script["title"]
            hirer = json_script["hiringOrganization"]["name"]
            description = _clean_description(json_script["description"])
            matches = list(_tokenize(description).intersection(tokens))
        except Exception as _:
            pass
        else:
            result.update(
                {"title": title, "hiringOrganization": hirer, "matches": matches}
            )
            return result
    return result


def _clean_description(description):
    """Cleans the given description string to be optimized for NLP analysis."""
    if not description:
        return ""

    text = html.unescape(str(description))
    text = BeautifulSoup(text, "html.parser").get_text(" ")
    text = _fix_text(text)
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


def _fix_text(text):
    """Fix mojibake and other text encoding issues when ftfy is available."""
    if not text:
        return ""

    if ftfy is not None:
        return ftfy.fix_text(text)

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
    return set(tokenizer(text))
