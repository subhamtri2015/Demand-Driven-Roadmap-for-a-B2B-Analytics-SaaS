import csv
import re
from pathlib import Path


ROOT = Path(".")


def csv_rows(path):
    with path.open(newline="") as source:
        return list(csv.DictReader(source))


def check_backlog():
    rows = csv_rows(ROOT / "06-delivery/backlog.csv")
    points = sum(int(row["points_assumption"]) for row in rows)
    expected_points = {"S-1": 3, "S-2": 5, "S-3": 3, "S-4": 5, "S-5": 8, "S-6": 5, "S-7": 3, "S-8": 3}
    actual_points = {row["id"]: int(row["points_assumption"]) for row in rows}
    if actual_points != expected_points or points != 35:
        raise AssertionError(f"backlog points invalid: {actual_points}, total={points}")
    if any(row["status"] != "Planned not executed" for row in rows):
        raise AssertionError("backlog status must remain Planned not executed")
    acceptance = sum(bool(row["acceptance_summary"].strip()) for row in rows)
    estimates = sum(bool(row["points_assumption"].strip()) for row in rows)
    links = sum(bool(row["linked_issue"].strip()) for row in rows)
    output = (
        "# Backlog Health\n\n"
        "**Planned, not executed.** Computed from `backlog.csv`; this describes artifact completeness, not delivery progress.\n\n"
        f"- Acceptance summaries present: {acceptance}/{len(rows)} ({100*acceptance/len(rows):.0f}%).\n"
        f"- Point assumptions present: {estimates}/{len(rows)} ({100*estimates/len(rows):.0f}%).\n"
        f"- Linked public issues: {links}/{len(rows)} ({100*links/len(rows):.0f}%).\n"
        f"- Total planned point assumptions: {points}.\n"
    )
    (ROOT / "06-delivery/backlog-health.md").write_text(output)
    plan = (ROOT / "06-delivery/sprint-plan.md").read_text()
    if "16 assumption points" not in plan or "19 assumption points" not in plan:
        raise AssertionError("sprint-plan allocation does not match the backlog plan")
    print("Backlog: 35 points; planned Sprint 1/2 allocations match.")


def check_readme_data():
    readme = (ROOT / "README.md").read_text()
    overview = csv_rows(ROOT / "data/processed/overview.csv")[0]
    concentration = csv_rows(ROOT / "data/processed/concentration.csv")[0]
    lead = csv_rows(ROOT / "data/processed/lead_time.csv")
    ai = csv_rows(ROOT / "data/processed/ai_share_period.csv")
    requirements = [
        f"{int(overview['n']):,}",
        f"{int(float(overview['open_n'])):,}",
        f"{float(concentration['pct_zero']):.1f}%",
        f"{float(concentration['top10pct_share']):.1f}%",
        f"{float(overview['pct_milestone']):.1f}%",
        f"{float(lead[1]['median_days']):g}",
        f"{float(lead[0]['median_days']):g}",
        f"{float(ai[0]['ai_share_pct']):.1f}%",
        f"{float(ai[1]['ai_share_pct']):.1f}%",
    ]
    missing = [value for value in requirements if value not in readme]
    if missing:
        raise AssertionError(f"README missing CSV-backed figures: {missing}")
    for path in (ROOT / "README.md", ROOT / "02-analysis/findings.md", ROOT / "06-delivery/sprint-plan.md"):
        if re.search(r"\{\{[A-Z0-9_]+\}\}", path.read_text()):
            raise AssertionError(f"unrendered data placeholder in {path}")
    print("README: key figures match processed CSVs.")


def check_links():
    pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    failures = []
    markdown_files = list(ROOT.rglob("*.md"))
    for markdown in markdown_files:
        text = markdown.read_text()
        for target in pattern.findall(text):
            target = target.strip().split()[0].strip("<>")
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            local_target = target.split("#", 1)[0].split("?", 1)[0]
            if not local_target:
                continue
            resolved = (markdown.parent / local_target).resolve()
            if not resolved.exists():
                failures.append(f"{markdown}: {target}")
    if failures:
        raise AssertionError("Broken local Markdown links:\n" + "\n".join(failures))
    print(f"Markdown links: resolved local targets across {len(markdown_files)} files.")


def main():
    check_backlog()
    check_readme_data()
    check_links()
    print("Consistency checks passed.")


if __name__ == "__main__":
    main()