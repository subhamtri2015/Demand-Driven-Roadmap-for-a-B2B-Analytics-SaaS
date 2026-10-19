import csv
from pathlib import Path


def rows(filename):
    with open(Path("data/processed") / filename, newline="") as source:
        return list(csv.DictReader(source))


def fmt(value, digits=1):
    return f"{float(value):.{digits}f}"


def main():
    overview = rows("overview.csv")[0]
    concentration = rows("concentration.csv")[0]
    lifecycle = rows("lifecycle_signals.csv")[0]
    lead = {str(row["has_milestone"]): row for row in rows("lead_time.csv")}
    buckets = {row["bucket"]: row for row in rows("demand_vs_action.csv")}
    ai_periods = {row["period"]: row for row in rows("ai_share_period.csv")}
    ai_areas = {row["group_name"]: row for row in rows("ai_area_demand.csv")}
    top_area = rows("area_demand.csv")[0]
    release = rows("sdk_release_gap.csv")[0]
    first_minor = rows("sdk_release_lines.csv")[0]["minor_line"]
    prs = sorted(int(row["merged_prs"]) for row in rows("merged_prs_monthly.csv"))
    median_prs = (prs[len(prs) // 2 - 1] + prs[len(prs) // 2]) / 2 if len(prs) % 2 == 0 else prs[len(prs) // 2]

    values = {
        "N_REQUESTS": f"{int(float(overview['n'])):,}",
        "N_OPEN": f"{int(float(overview['open_n'])):,}",
        "OPEN_SHARE": fmt(100 * float(overview["open_n"]) / float(overview["n"])),
        "PCT_CLOSED": fmt(overview["pct_closed"]),
        "PRIORITY_SHARE": fmt(overview["pct_priority"]),
        "MILESTONE_SHARE": fmt(overview["pct_milestone"]),
        "CLOSED_WITH_MILESTONE": f"{int(float(lifecycle['closed_with_milestone'])):,}",
        "ZERO_SHARE": fmt(concentration["pct_zero"]),
        "TOP10_SHARE": fmt(concentration["top10pct_share"]),
        "TOP1_SHARE": fmt(concentration["top1pct_share"]),
        "TOP_AREA": top_area["area"],
        "TOP_AREA_REQUESTS": f"{int(float(top_area['requests'])):,}",
        "TOP_AREA_LIKES": f"{int(float(top_area['total_plus1'])):,}",
        "AI_MEAN": fmt(ai_areas["Metabot-labeled"]["mean_plus1"], 2),
        "OTHER_MEAN": fmt(ai_areas["Other"]["mean_plus1"], 2),
        "AI_EARLY": fmt(ai_periods["Oct24-Sep25"]["ai_share_pct"]),
        "AI_LATE": fmt(ai_periods["Oct25-onwards"]["ai_share_pct"]),
        "FIRST_MINOR": first_minor,
        "RELEASE_GAP": fmt(release["median_gap_days"], 0),
        "PR_MEDIAN": fmt(median_prs, 0),
        "MILESTONE_MEDIAN": fmt(lead["True"]["median_days"], 1),
        "NO_MILESTONE_MEDIAN": fmt(lead["False"]["median_days"], 1),
        "OVERALL_CLOSE_MEDIAN": fmt(overview["median_days_to_close"], 0),
        "H3_B0": fmt(buckets["0"]["pct_milestone"]),
        "H3_B12": fmt(buckets["1-2"]["pct_milestone"]),
        "H3_B39": fmt(buckets["3-9"]["pct_milestone"]),
        "H3_B10": fmt(buckets["10+"]["pct_milestone"]),
        "H4_B0": fmt(buckets["0"]["pct_priority"]),
        "H4_B12": fmt(buckets["1-2"]["pct_priority"]),
        "H4_B39": fmt(buckets["3-9"]["pct_priority"]),
        "H4_B10": fmt(buckets["10+"]["pct_priority"]),
    }
    files = [
        Path("README.md"),
        Path("02-analysis/findings.md"),
        Path("06-delivery/sprint-plan.md"),
    ]
    for path in files:
        text = path.read_text()
        for key, value in values.items():
            text = text.replace("{{" + key + "}}", value)
        unresolved = [key for key in values if "{{" + key + "}}" in text]
        if unresolved:
            raise ValueError(f"unresolved values in {path}: {unresolved}")
        path.write_text(text)
    print("README, findings, and sprint-plan figures rendered from processed CSVs.")


if __name__ == "__main__":
    main()