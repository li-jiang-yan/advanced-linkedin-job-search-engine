from urllib.parse import urlencode

import requests
from bs4 import BeautifulSoup


def search_jobs(request):
    params = request.args.to_dict(flat=True)
    number = int(params.pop("number", 1))
    query = urlencode(params)

    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    results = []

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    start = 0
    while start < number:
        url = f"{base_url}?{query}&start={start}"
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            result = BeautifulSoup(response.text, "html.parser").find_all("li")
            results += [str(elem) for elem in result]
            start += len(result)
        else:
            start += 1

    return {"results": results}, 200
