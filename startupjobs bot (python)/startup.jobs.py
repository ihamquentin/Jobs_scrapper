import json
import webbrowser
import requests

if __name__ == "__main__":
    roles = ["rust engineer", "rust developer", "blockchain developer", "blockchain engineer"]
    try:
        notify = True
        db = json.loads(open("jobs.db.json").read())
    except FileNotFoundError:
        db = dict()
        notify = False
    notify = True
    url = "https://4cqmtmmk73-dsn.algolia.net/1/indexes/Post_production/query"
    headers = {
        "Origin": "https://startup.jobs",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15",
        "Referer": "https://startup.jobs/",
        "Content-Type": "application/json"
    }
    params = {
        "x-algolia-agent": "Algolia for JavaScript (4.14.2); Browser (lite)",
        "x-algolia-api-key": "17cd9f3c024650820efaa17c39ea2b1d",
        "x-algolia-application-id": "4CQMTMMK73"
    }
    for role in roles:
        payload = json.dumps({
            "query": role,
            "attributesToRetrieve": [
                "path",
                "company_slug",
                "company_logo_url",
                "title",
                "company_name",
                "_tags",
                "remote",
                "location",
                "location_html"
            ],
            "hitsPerPage": 25,
            "page": 0,
            "facets": [
                "commitment"
            ],
            "filters": "",
            "tagFilters": [
                ""
            ],
            "facetFilters": [
                [
                    "commitment:Full-Time",
                    "commitment:Part-Time",
                    "commitment:Internship",
                    "commitment:Contractor"
                ],
                "remote:true"
            ],
            "ruleContexts": [],
            "analyticsTags": [
                "frontend"
            ]
        })
        response = requests.request("POST", url, headers=headers,
params=params, data=payload).json()
        for job in response["hits"]:
            if job["path"] not in db:
                db[job["path"]] = {
                    "href": "https://startup.jobs" + job["path"],
                    "company": job["company_name"],
                    "role": job["title"]
                }
                if notify:
                    webbrowser.open_new_tab("https://startup.jobs" +
job["path"])
    open("jobs.db.json", "w").write(json.dumps(db, indent=4))
