import pytest

from scripts.analysis_utils import rice_score


# TEST FIXTURE: inputs are hand-written solely for formula validation.
TEST_FIXTURE = {"reach": 12, "impact": 2, "confidence": 0.8, "effort": 2}


def test_rice_math():
    assert rice_score(**TEST_FIXTURE) == pytest.approx(9.6)