import csv
import os


def main():
    reaches = {key: 0 for key in "ABCDE"}
    with open("data/processed/reach_inputs.csv", newline="") as source:
        for row in csv.DictReader(source):
            reaches[row["initiative"]] += int(row["reach_plus1"])
    with open("03-strategy/rice.csv", newline="") as source:
        assumptions = list(csv.DictReader(source))
    scored = []
    for row in assumptions:
        reach = reaches[row["initiative"]]
        impact = float(row["impact"])
        confidence = float(row["confidence"])
        effort = float(row["effort"])
        scored.append(
            {
                "initiative": row["initiative"],
                "reach": reach,
                "impact": impact,
                "confidence": confidence,
                "effort": effort,
                "score": round(reach * impact * confidence / effort, 4),
            }
        )
    scored.sort(key=lambda item: (-item["score"], item["initiative"]))
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/rice_scores.csv", "w", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=list(scored[0]))
        writer.writeheader()
        writer.writerows(scored)
    by_id = {row["initiative"]: row for row in scored}
    c_confidence = by_id["C"]["reach"] * by_id["C"]["impact"] * 0.70 / by_id["C"]["effort"]
    a_effort = by_id["A"]["reach"] * by_id["A"]["impact"] * by_id["A"]["confidence"] / 3
    top = scored[0]
    second = scored[1]
    with open("03-strategy/rice.md", "w") as output:
        output.write(
            "# RICE Prioritization\n\n"
            "Reach is the sum of 👍 on qualifying **open** public issues, calculated from "
            "`data/processed/reach_inputs.csv`. Reach is a vocal-user proxy, not customer count. "
            "Impact, confidence, and effort are assumptions; scores are decision aids, not measured outcomes.\n\n"
            "| Rank | Initiative | Reach (👍 proxy) | Impact (assumption) | Confidence (assumption) | Effort (assumption) | Score |\n"
            "|---:|---|---:|---:|---:|---:|---:|\n"
        )
        names = {
            "A": "Embedding SDK theming with CSS variables",
            "B": "Warehouse connector gaps",
            "C": "Granular permissions and controlled access",
            "D": "Dashboard filters and parameters",
            "E": "Remote sync with multiple branches",
        }
        for rank, row in enumerate(scored, 1):
            output.write(
                f"| {rank} | {names[row['initiative']]} | {row['reach']} | {row['impact']:g} "
                f"| {row['confidence']:.0%} | {row['effort']:g} | {row['score']:.2f} |\n"
            )
        output.write(
            f"\nThe lead between first and second is {top['score'] - second['score']:.2f} score points "
            f"({100 * (top['score'] - second['score']) / top['score']:.1f}% of the top score), "
            "so the rank is not robust to small assumption changes.\n\n"
            "## Sensitivity\n\n"
            "| Case | Recalculated score | Interpretation |\n|---|---:|---|\n"
            f"| C confidence changed to 70% | {c_confidence:.2f} | Permissions moves above the base A score. |\n"
            f"| A effort changed to 3 | {a_effort:.2f} | A no longer leads; this case changes the ordering. |\n\n"
            "These scenarios vary assumptions only. They do not change the observed reach values. "
            "Use Now as a discovery recommendation, not a delivery commitment.\n"
        )
    print("RICE scores written from reach_inputs.csv and stated assumptions.")


if __name__ == "__main__":
    main()