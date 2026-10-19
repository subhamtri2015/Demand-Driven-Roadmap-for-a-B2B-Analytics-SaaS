import collections
import csv
import datetime as dt
import json
import os
import re
import statistics
import urllib.request


url = "https://registry.npmjs.org/@metabase/embedding-sdk-react"
with urllib.request.urlopen(url, timeout=30) as response:
    package_data = json.load(response)
versions = {
    version: published
    for version, published in package_data["time"].items()
    if re.fullmatch(r"0\.\d+\.\d+", version)
}
os.makedirs("data/processed", exist_ok=True)
with open("data/processed/sdk_releases.csv", "w", newline="") as output:
    writer = csv.writer(output)
    writer.writerow(["version", "published_at"])
    for version, published in sorted(versions.items(), key=lambda item: item[1]):
        writer.writerow([version, published])

lines = collections.defaultdict(list)
for version, published in versions.items():
    lines[int(version.split(".")[1])].append(
        dt.datetime.fromisoformat(published.replace("Z", "+00:00"))
    )
rows = []
for minor in sorted(lines):
    if minor < 50:
        continue
    releases = sorted(lines[minor])
    rows.append(
        [
            f"0.{minor}",
            releases[0].date().isoformat(),
            len(releases),
            (releases[-1] - releases[0]).days,
        ]
    )
with open("data/processed/sdk_release_lines.csv", "w", newline="") as output:
    writer = csv.writer(output)
    writer.writerow(
        ["minor_line", "first_stable_date", "versions_published", "days_first_to_last"]
    )
    writer.writerows(rows)

first_dates = [dt.date.fromisoformat(row[1]) for row in rows]
median_gap = statistics.median(
    [(later - earlier).days for earlier, later in zip(first_dates, first_dates[1:])]
)
with open("data/processed/sdk_release_gap.csv", "w", newline="") as output:
    writer = csv.writer(output)
    writer.writerow(["minor_lines", "intervals", "median_gap_days"])
    writer.writerow([len(first_dates), len(first_dates) - 1, median_gap])
print("median days between minor lines:", median_gap)