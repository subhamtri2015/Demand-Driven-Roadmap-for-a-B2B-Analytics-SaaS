import datetime as dt
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


TOKEN = os.environ.get("GITHUB_TOKEN")


def months(a, b):
    cur = a
    while cur <= b:
        nxt = (cur.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        yield cur, min(nxt - dt.timedelta(days=1), b)
        cur = nxt


def get(url):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "demand-roadmap-study",
    }
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    for _ in range(6):
        try:
            with urllib.request.urlopen(
                urllib.request.Request(url, headers=headers), timeout=30
            ) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            if error.code in (403, 429):
                time.sleep(30)
                continue
            raise
    raise RuntimeError("retries exhausted")


if not TOKEN:
    raise SystemExit("GITHUB_TOKEN is missing from the process environment")
if len(sys.argv) != 3:
    raise SystemExit("usage: python scripts/fetch_requests.py <start> <end>")

start, end = (dt.date.fromisoformat(value) for value in sys.argv[1:3])
os.makedirs("data/raw", exist_ok=True)
path = "data/raw/feature_requests.json"
rows = json.load(open(path)) if os.path.exists(path) else []
seen = {row["number"] for row in rows}

for start_month, end_month in months(start, end):
    page = 1
    while True:
        query = (
            f'repo:metabase/metabase is:issue label:"Type:New Feature" '
            f"created:{start_month}..{end_month}"
        )
        url = (
            "https://api.github.com/search/issues?q="
            f"{urllib.parse.quote(query)}&per_page=100&page={page}"
        )
        data = get(url)
        for item in data.get("items", []):
            if item["number"] in seen:
                continue
            seen.add(item["number"])
            rows.append(
                {
                    "number": item["number"],
                    "title": item["title"],
                    "state": item["state"],
                    "created_at": item["created_at"],
                    "closed_at": item["closed_at"],
                    "comments": item["comments"],
                    "reactions_plus1": item["reactions"]["+1"],
                    "labels": [label["name"] for label in item["labels"]],
                    "milestone": (item.get("milestone") or {}).get("title"),
                }
            )
        with open(path, "w") as output:
            json.dump(rows, output)
        print(
            start_month,
            end_month,
            page,
            len(data.get("items", [])),
            flush=True,
        )
        if len(data.get("items", [])) < 100:
            break
        page += 1
        time.sleep(6.5)
    time.sleep(6.5)