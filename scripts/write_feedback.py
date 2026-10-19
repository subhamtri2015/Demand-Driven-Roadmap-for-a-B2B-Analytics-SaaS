import csv

from analysis_utils import parse_areas


def main():
    with open("data/processed/top_feedback.csv", newline="") as source:
        rows = list(csv.DictReader(source))
    with open("02-analysis/feedback-log.md", "w") as output:
        output.write(
            "# Customer Voice: Public Issue Signals\n\n"
            "This ranked list is a public issue signal, not interview evidence or a representative customer sample. "
            "It contains no issue bodies or author names. 👍 is a vocal-user proxy, not customer demand.\n\n"
            "| Issue | Request | 👍 | Comments | State | Milestone? | Area label |\n"
            "|---|---|---:|---:|---|---|---|\n"
        )
        for row in rows:
            issue_number = int(row["number"])
            title = row["title"].replace("|", "\\|").replace("\n", " ")
            areas = parse_areas(row["labels_str"].split("|") if row["labels_str"] else [])
            area = ", ".join(sorted(areas)) or "Not labeled"
            has_milestone = "Yes" if row["has_milestone"] == "True" else "No"
            output.write(
                f"| [#{issue_number}](https://github.com/metabase/metabase/issues/{issue_number}) "
                f"| {title} | {row['reactions_plus1']} | {row['comments']} | {row['state']} "
                f"| {has_milestone} | {area} |\n"
            )


if __name__ == "__main__":
    main()