-- Plan, no results. Proposed event schema; not connected to a live event source.
CREATE TABLE IF NOT EXISTS theme_events (
    event_id VARCHAR NOT NULL,
    workspace_id VARCHAR NOT NULL,
    event_name VARCHAR NOT NULL,
    occurred_at TIMESTAMP NOT NULL,
    sdk_version VARCHAR,
    variable_name VARCHAR,
    value_type VARCHAR,
    error_category VARCHAR
);