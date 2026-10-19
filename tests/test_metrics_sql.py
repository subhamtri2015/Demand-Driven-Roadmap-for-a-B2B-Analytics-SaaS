from pathlib import Path

import pytest

import duckdb


def test_metrics_sql_on_test_fixture():
    connection = duckdb.connect()
    connection.execute(
        """
        CREATE TABLE theme_events AS
        SELECT * FROM read_csv_auto('tests/metrics_fixture.csv', header=true)
        """
    )
    query = Path("05-metrics/metrics.sql").read_text()
    row = connection.execute(query).fetchone()
    assert row[0] == 3
    assert row[1] == 2
    assert row[2] == pytest.approx(100.0 * 2 / 3)
    assert row[3] == 15