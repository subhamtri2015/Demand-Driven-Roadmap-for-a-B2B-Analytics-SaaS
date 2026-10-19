-- Plan, no results. Run against a validated event table with the schema in schema.sql.
WITH starts AS (
    SELECT workspace_id, MIN(occurred_at) AS started_at
    FROM theme_events
    WHERE event_name = 'theme_config_started'
    GROUP BY workspace_id
), publishes AS (
    SELECT workspace_id, MIN(occurred_at) AS published_at
    FROM theme_events
    WHERE event_name = 'theme_published'
    GROUP BY workspace_id
), workspace_metrics AS (
    SELECT starts.workspace_id, starts.started_at, publishes.published_at,
           date_diff('minute', starts.started_at, publishes.published_at) AS elapsed_minutes
    FROM starts LEFT JOIN publishes USING (workspace_id)
)
SELECT COUNT(*) AS started_workspaces,
       COUNT(published_at) AS published_workspaces,
       100.0 * COUNT(published_at) / NULLIF(COUNT(*), 0) AS publish_rate_pct,
       median(CASE WHEN elapsed_minutes >= 0 THEN elapsed_minutes END) AS median_minutes_to_publish
FROM workspace_metrics;