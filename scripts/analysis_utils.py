def demand_bucket(reactions):
    if reactions == 0:
        return "0"
    if reactions <= 2:
        return "1-2"
    if reactions <= 9:
        return "3-9"
    return "10+"


def concentration_share(reactions, top_fraction):
    ordered = sorted(reactions, reverse=True)
    total = sum(ordered)
    if not ordered or total == 0:
        return 0.0
    top_count = max(1, int(len(ordered) * top_fraction))
    return 100.0 * sum(ordered[:top_count]) / total


def parse_areas(labels):
    ignored_prefixes = ("Type:", "Priority:", ".")
    areas = set()
    for label in labels:
        if "/" not in label or label.startswith(ignored_prefixes):
            continue
        areas.add(label.split("/", 1)[0])
    return areas


def lifecycle_counts(rows):
    return {
        "requested": len(rows),
        "priority_labelled": sum(bool(row["priority"]) for row in rows),
        "milestone_assigned": sum(bool(row["milestone"]) for row in rows),
        "closed": sum(row["state"] == "closed" for row in rows),
        "closed_with_milestone": sum(
            row["state"] == "closed" and bool(row["milestone"]) for row in rows
        ),
    }


def rice_score(reach, impact, confidence, effort):
    return reach * impact * confidence / effort