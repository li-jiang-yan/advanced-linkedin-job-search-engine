from urllib.parse import urlencode


def search_jobs(request):
    params = request.args.to_dict(flat=True)
    number = int(params.pop("number", 1))
    query = urlencode(params)
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
    urls = []

    for start in range(number):
        if query:
            url = f"{base_url}?{query}&start={start}"
        else:
            url = f"{base_url}?start={start}"
        urls.append(url)

    return {"urls": urls}, 200
