from scripts.analysis_utils import (
    concentration_share,
    demand_bucket,
    lifecycle_counts,
    parse_areas,
)


# TEST FIXTURE: hand-written values exist only to validate calculations.
TEST_FIXTURE = [
    {"likes": 0, "state": "open", "priority": False, "milestone": None, "labels": ["Query/Builder"]},
    {"likes": 1, "state": "closed", "priority": True, "milestone": "M1", "labels": ["Type:New Feature"]},
    {"likes": 2, "state": "open", "priority": False, "milestone": None, "labels": ["Administration/Permissions"]},
    {"likes": 3, "state": "closed", "priority": False, "milestone": None, "labels": ["Filters & Parameters/URL"]},
    {"likes": 4, "state": "open", "priority": False, "milestone": None, "labels": ["Priority:P2"]},
    {"likes": 5, "state": "closed", "priority": True, "milestone": "M2", "labels": ["Embedding/SDK"]},
    {"likes": 6, "state": "open", "priority": False, "milestone": None, "labels": ["Data/Modeling"]},
    {"likes": 7, "state": "closed", "priority": False, "milestone": None, "labels": ["Type:New Feature"]},
    {"likes": 9, "state": "open", "priority": False, "milestone": None, "labels": ["Query/Builder"]},
    {"likes": 10, "state": "closed", "priority": True, "milestone": "M3", "labels": ["Administration/Permissions"]},
]


def test_demand_bucket_boundaries():
    assert [demand_bucket(value) for value in (0, 1, 2, 3, 9, 10)] == [
        "0", "1-2", "1-2", "3-9", "3-9", "10+"
    ]


def test_concentration_math():
    values = [row["likes"] for row in TEST_FIXTURE]
    assert round(concentration_share(values, 0.1), 2) == 21.28


def test_area_parsing():
    assert parse_areas(
        ["Embedding/SDK", "Type:New Feature", "Priority:P2", ".Needs Triage"]
    ) == {"Embedding"}


def test_lifecycle_counts():
    counts = lifecycle_counts(
        [
            {
                "state": row["state"],
                "priority": row["priority"],
                "milestone": row["milestone"],
            }
            for row in TEST_FIXTURE
        ]
    )
    assert counts == {
        "requested": 10,
        "priority_labelled": 3,
        "milestone_assigned": 3,
        "closed": 5,
        "closed_with_milestone": 3,
    }