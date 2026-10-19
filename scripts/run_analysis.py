import csv
import json
import os

import duckdb


OUTPUTS = {
    1: "overview.csv",
    2: "concentration.csv",
    3: "demand_vs_action.csv",
    4: "area_demand.csv",
    5: "ai_share_period.csv",
    6: "top_open.csv",
    7: "lifecycle_signals.csv",
    8: "lead_time.csv",
}


def write_reach_inputs(connection):
    rows = connection.execute(
        """
        SELECT number, title, reactions_plus1, labels_str
        FROM fr WHERE state = 'open' ORDER BY number
        """
    ).fetchall()
    initiatives = {key: [] for key in ("A", "B", "C", "D", "E")}
    for number, title, likes, labels in rows:
        label_list = labels.split("|") if labels else []
        label_text = "|".join(label_list)
        if "Embedding" in label_text and any(
            term in title.lower()
            for term in ("theme", "theming", "css", "branding", "white-label", "font", "color")
        ):
            initiatives["A"].append((number, likes))
        if number in (59486, 55763):
            initiatives["B"].append((number, likes))
        if "Administration/Permissions" in label_text:
            initiatives["C"].append((number, likes))
        if "Filters & Parameters" in label_text:
            initiatives["D"].append((number, likes))
        if number == 66680:
            initiatives["E"].append((number, likes))
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/reach_inputs.csv", "w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["initiative", "issue_number", "reach_plus1"])
        for initiative, issue_rows in initiatives.items():
            for issue_number, reach in issue_rows:
                writer.writerow([initiative, issue_number, reach])


def main():
    with open("scripts/analysis.sql") as source:
        statements = [part.strip() for part in source.read().split(";") if part.strip()]
    connection = duckdb.connect()
    query_number = 0
    for statement in statements:
        if statement.startswith("-- 0. Load"):
            connection.execute(statement)
            continue
        query_number += 1
        result = connection.execute(statement).fetchdf()
        output_path = os.path.join("data/processed", OUTPUTS[query_number])
        os.makedirs("data/processed", exist_ok=True)
        result.to_csv(output_path, index=False)

    monthly = connection.execute(
        """
        SELECT strftime(created_at, '%Y-%m') AS month,
               COUNT(*) AS requests,
               SUM((labels_str LIKE '%Metabot%')::INT) AS ai_requests,
               ROUND(100.0 * AVG((labels_str LIKE '%Metabot%')::INT), 1) AS ai_share_pct
        FROM fr GROUP BY 1 ORDER BY 1
        """
    ).fetchdf()
    monthly.to_csv("data/processed/ai_share_monthly.csv", index=False)
    connection.execute(
        """
        SELECT number, title, reactions_plus1, comments, state, has_milestone,
               labels_str
        FROM fr ORDER BY reactions_plus1 DESC, comments DESC LIMIT 15
        """
    ).fetchdf().to_csv("data/processed/top_feedback.csv", index=False)
    connection.execute(
        """
        SELECT CASE WHEN labels_str LIKE '%Metabot%' THEN 'Metabot-labeled' ELSE 'Other' END AS group_name,
               COUNT(*) AS requests,
               ROUND(AVG(reactions_plus1), 2) AS mean_plus1,
               median(reactions_plus1) AS median_plus1
        FROM fr GROUP BY 1 ORDER BY 1
        """
    ).fetchdf().to_csv("data/processed/ai_area_demand.csv", index=False)
    write_reach_inputs(connection)

    with open("data/raw/feature_requests.json") as source:
        issue_numbers = {row["number"] for row in json.load(source)}
    with open("data/processed/reach_inputs.csv", newline="") as source:
        for row in csv.DictReader(source):
            if int(row["issue_number"]) not in issue_numbers:
                raise ValueError(f"RICE issue #{row['issue_number']} missing from source data")
    print("Analysis CSVs written; reach issue numbers verified against raw data.")


if __name__ == "__main__":
    main()