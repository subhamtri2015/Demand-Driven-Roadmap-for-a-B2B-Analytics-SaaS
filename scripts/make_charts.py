import datetime as dt
import os
import re
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd


PULL_DATE = dt.date.today().isoformat()
OUT = "assets"
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update(
    {
        "svg.fonttype": "none",
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "font.family": ["Arial"],
        "text.color": "#17242d",
        "axes.labelcolor": "#33434d",
        "xtick.color": "#33434d",
        "ytick.color": "#33434d",
        "axes.edgecolor": "#c9d2d8",
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)


def read(name):
    return pd.read_csv(f"data/processed/{name}.csv")


def save(fig, filename):
    fig.tight_layout()
    output_path = Path(OUT) / filename
    fig.savefig(output_path, format="svg", bbox_inches="tight")
    svg = output_path.read_text()
    svg = re.sub(r"<!DOCTYPE svg PUBLIC.*?>\s*", "", svg, flags=re.DOTALL)
    svg = re.sub(r" <metadata>.*?</metadata>\s*", "\n", svg, flags=re.DOTALL)
    svg = svg.replace(
        "<svg ",
        '<svg aria-labelledby="chart-title chart-desc" ',
        1,
    )
    chart_metadata = {
        "demand-concentration.svg": ("Demand concentration", "Positive reactions across feature requests; shares are computed from the processed public issue dataset."),
        "demand-vs-planning.svg": ("Demand and planning signal", "Milestone proportions by positive-reaction bucket; group sample sizes are labeled."),
        "area-demand.svg": ("Demand by labeled product area", "Total positive reactions by area label; requests with multiple area labels can count in multiple areas."),
        "ai-share-trend.svg": ("AI-area label share over time", "Monthly Metabot-labeled feature request share; labeling practice may have changed."),
        "lifecycle-signals.svg": ("Lifecycle signals, not strict stages", "Counts of requested, priority-labeled, milestone-assigned, closed, and closed-with-milestone issues."),
        "lead-time.svg": ("Closed-request lead time", "Median days from creation to close with interquartile ranges, grouped by milestone presence."),
        "sdk-release-train.svg": ("SDK stable minor-line release train", "First stable publish date and number of published versions by minor line; bubble size represents versions."),
        "merged-prs-monthly.svg": ("Merged PRs per month", "Monthly GitHub Search API merged pull request totals; counts include bots and backports."),
    }
    title, description = chart_metadata[filename]
    svg = svg.replace(
        "<defs>",
        f'<title id="chart-title">{title}</title>\n'
        f'<desc id="chart-desc">{description}</desc>\n'
        ' <rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>\n'
        ' <style>text{font-family:Inter,-apple-system,"Segoe UI",Arial,sans-serif}</style>\n'
        "<defs>",
        1,
    )
    svg = svg.replace("'DejaVu Sans'", "Arial")
    output_path.write_text(svg)
    plt.close(fig)


overview = read("overview").iloc[0]
count = int(overview["n"])
metadata = f"n={count:,} | pulled {PULL_DATE}"

concentration = read("concentration").iloc[0]
fig, ax = plt.subplots(figsize=(7, 4))
labels = ["Top 1%", "Top 10%", "Zero reactions"]
values = [
    concentration["top1pct_share"],
    concentration["top10pct_share"],
    concentration["pct_zero"],
]
bars = ax.bar(labels, values, color=["#167d78", "#38a69b", "#e0a144"])
ax.bar_label(bars, fmt="%.1f%%", padding=4)
ax.set_ylim(0, max(values) * 1.25)
ax.set_ylabel("Share (%)")
ax.set_title(f"Demand concentration\n{metadata}")
save(fig, "demand-concentration.svg")

demand = read("demand_vs_action")
fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.bar(demand["bucket"], demand["pct_milestone"], color="#167d78")
ax.bar_label(
    bars,
    labels=[f"{row.pct_milestone:.1f}%\nn={int(row.requests)}" for row in demand.itertuples()],
    padding=4,
    fontsize=9,
)
ax.set_ylim(0, demand["pct_milestone"].max() * 1.5)
ax.set_xlabel("Positive reactions on request")
ax.set_ylabel("Requests with milestone (%)")
ax.set_title(f"Demand and planning signal\n{metadata}")
ax.text(0.99, 0.98, "Small-n groups are descriptive", ha="right", va="top", transform=ax.transAxes, fontsize=9)
save(fig, "demand-vs-planning.svg")

areas = read("area_demand").sort_values("total_plus1")
fig, ax = plt.subplots(figsize=(9, 6))
ax.barh(areas["area"], areas["total_plus1"], color="#38a69b")
ax.set_xlim(0, areas["total_plus1"].max() * 1.12)
ax.set_xlabel("Total positive reactions (multi-area labels can count across areas)")
ax.set_title(f"Demand by labeled product area\nn={count:,} requests | pulled {PULL_DATE}")
save(fig, "area-demand.svg")

monthly_ai = read("ai_share_monthly")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(monthly_ai["month"], monthly_ai["ai_share_pct"], color="#c45c35", marker="o", markersize=3)
ax.set_ylabel("Requests labeled Metabot (%)")
ax.set_title(f"AI-area label share over time\nn={int(monthly_ai['requests'].sum()):,} requests | pulled {PULL_DATE}")
ax.text(0.02, 0.96, "Labeling practice may have changed", ha="left", va="top", transform=ax.transAxes, fontsize=9)
ax.set_xticks(monthly_ai.index[::2])
ax.set_xticklabels(monthly_ai["month"].iloc[::2], rotation=45, ha="right", fontsize=8)
ax.margins(x=0.04)
save(fig, "ai-share-trend.svg")

lifecycle = read("lifecycle_signals").iloc[0]
fig, ax = plt.subplots(figsize=(8, 4.5))
life_labels = ["Requested", "Priority label", "Milestone", "Closed", "Closed + milestone"]
life_values = [
    lifecycle["requested"],
    lifecycle["priority_labelled"],
    lifecycle["milestone_assigned"],
    lifecycle["closed"],
    lifecycle["closed_with_milestone"],
]
bars = ax.bar(life_labels, life_values, color=["#167d78", "#38a69b", "#e0a144", "#7192a3", "#c45c35"])
ax.bar_label(bars, fmt="%.0f", padding=3)
ax.set_title(f"Lifecycle signals, not strict stages\n{metadata}")
ax.tick_params(axis="x", labelrotation=20)
save(fig, "lifecycle-signals.svg")

lead = read("lead_time")
fig, ax = plt.subplots(figsize=(7, 4.5))
for index, row in lead.iterrows():
    color = "#167d78" if bool(row["has_milestone"]) else "#c45c35"
    ax.errorbar(
        index,
        row["median_days"],
        yerr=[[row["median_days"] - row["p25"]], [row["p75"] - row["median_days"]]],
        fmt="o",
        capsize=6,
        color=color,
        markersize=9,
    )
ax.set_xticks(range(len(lead)))
ax.set_xticklabels(["No milestone", "Has milestone"])
ax.set_ylabel("Days from creation to close")
ax.set_title(f"Closed-request lead time: median and IQR\nn={int(lead['n'].sum()):,} closed requests | pulled {PULL_DATE}")
save(fig, "lead-time.svg")

release_lines = pd.read_csv("data/processed/sdk_release_lines.csv", dtype={"minor_line": str})
release_lines["date"] = pd.to_datetime(release_lines["first_stable_date"])
dates = release_lines["date"].sort_values()
median_gap = statistics.median([(b - a).days for a, b in zip(dates, dates.iloc[1:])])
fig, ax = plt.subplots(figsize=(12, 4.5))
y = [1] * len(release_lines)
ax.scatter(release_lines["date"], y, s=release_lines["versions_published"] * 12, color="#167d78", alpha=0.8)
for row in release_lines.itertuples():
    ax.annotate(
        f"{row.minor_line}\n{row.versions_published} vers",
        (row.date, 1),
        xytext=(0, 12 if int(row.minor_line.split(".")[1]) % 2 else -30),
        textcoords="offset points",
        ha="center",
        fontsize=7,
    )
ax.set_yticks([])
ax.set_ylim(0.45, 1.55)
ax.set_xlim(dates.min() - pd.Timedelta(days=35), dates.max() + pd.Timedelta(days=55))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
ax.margins(x=0.02)
ax.tick_params(axis="x", labelsize=8)
ax.set_title(f"SDK stable minor-line release train\nmedian gap {median_gap:.0f} days | {len(release_lines)} lines | pulled {PULL_DATE}")
save(fig, "sdk-release-train.svg")

merged = read("merged_prs_monthly")
fig, ax = plt.subplots(figsize=(12, 4.5))
bars = ax.bar(merged["month"], merged["merged_prs"], color="#7192a3")
for bar, partial in zip(bars, merged["partial"]):
    if bool(partial):
        bar.set_hatch("///")
ax.set_ylabel("Merged PRs (search total_count)")
ax.set_title(f"Merged PRs per month\n{len(merged)} months | pulled {PULL_DATE}")
ax.text(0.99, 0.97, "includes bots and backports", ha="right", va="top", transform=ax.transAxes, fontsize=9)
ax.set_xlim(-0.7, len(merged) - 0.3)
ax.tick_params(axis="x", labelrotation=55, labelsize=8)
save(fig, "merged-prs-monthly.svg")