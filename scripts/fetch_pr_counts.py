import csv
import datetime as dt
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request


TOKEN = os.environ.get("GITHUB_TOKEN")


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

today = dt.date.today()
current = dt.date(2024, 10, 1)
rows = []
while current <= today:
    next_month = (current.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    month_end = next_month - dt.timedelta(days=1)
    last = min(month_end, today)
    query = (
        "repo:metabase/metabase is:pr is:merged "
        f"merged:{current}..{last}"
    )
    url = (
        "https://api.github.com/search/issues?q="
        f"{urllib.parse.quote(query)}&per_page=1"
    )
    data = get(url)
    rows.append(
        {
            "month": current.strftime("%Y-%m"),
            "merged_prs": data["total_count"],
            "partial": last < month_end,
        }
    )
    print(rows[-1], flush=True)
    time.sleep(6.5)
    current = next_month

os.makedirs("data/processed", exist_ok=True)
with open("data/processed/merged_prs_monthly.csv", "w", newline="") as output:
    writer = csv.DictWriter(output, fieldnames=["month", "merged_prs", "partial"])
    writer.writeheader()
    writer.writerows(rows)