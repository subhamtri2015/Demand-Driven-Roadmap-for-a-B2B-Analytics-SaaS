-- 0. Load
CREATE OR REPLACE TABLE fr AS
SELECT number, title, state, CAST(created_at AS TIMESTAMP) AS created_at, CAST(closed_at AS TIMESTAMP) AS closed_at,
       comments, reactions_plus1, milestone, array_to_string(labels, '|') AS labels_str,
       (milestone IS NOT NULL) AS has_milestone,
       (array_to_string(labels, '|') LIKE '%Priority:P%') AS has_priority,
       (array_to_string(labels, '|') LIKE '%.Needs Triage%') AS needs_triage
FROM read_json_auto('data/raw/feature_requests.json');
-- 1. Overview
SELECT COUNT(*) AS n, SUM((state='open')::INT) AS open_n, ROUND(100.0*AVG((state='closed')::INT),1) AS pct_closed,
  ROUND(100.0*AVG(has_priority::INT),1) AS pct_priority, ROUND(100.0*AVG(has_milestone::INT),1) AS pct_milestone,
  ROUND(median(CASE WHEN state='open' THEN date_diff('day', created_at, current_date) END),0) AS median_age_open_days,
  ROUND(median(CASE WHEN state='closed' THEN date_diff('day', created_at, closed_at) END),0) AS median_days_to_close
FROM fr;
-- 2. Demand concentration
WITH r AS (SELECT reactions_plus1 AS p, ROW_NUMBER() OVER (ORDER BY reactions_plus1 DESC, number) AS rn, COUNT(*) OVER () AS n FROM fr)
SELECT ROUND(100.0*AVG((p=0)::INT),1) AS pct_zero, ROUND(100.0*SUM(CASE WHEN rn<=n*0.10 THEN p END)/SUM(p),1) AS top10pct_share,
       ROUND(100.0*SUM(CASE WHEN rn<=n*0.01 THEN p END)/SUM(p),1) AS top1pct_share FROM r;
-- 3. Does demand predict planning?
SELECT CASE WHEN reactions_plus1=0 THEN '0' WHEN reactions_plus1<=2 THEN '1-2' WHEN reactions_plus1<=9 THEN '3-9' ELSE '10+' END AS bucket,
  COUNT(*) AS requests, ROUND(100.0*AVG(has_milestone::INT),1) AS pct_milestone, ROUND(100.0*AVG((state='closed')::INT),1) AS pct_closed,
  ROUND(100.0*AVG(has_priority::INT),1) AS pct_priority
FROM fr GROUP BY 1 ORDER BY MIN(reactions_plus1);
-- 4. Demand by product area (a request can sit in several areas)
WITH a AS (SELECT DISTINCT f.number, f.state, f.has_milestone, f.reactions_plus1, split_part(l,'/',1) AS area
  FROM fr f, UNNEST(string_split(f.labels_str,'|')) AS t(l)
  WHERE l LIKE '%/%' AND l NOT LIKE '.%' AND l NOT LIKE 'Type:%' AND l NOT LIKE 'Priority:%')
SELECT area, COUNT(*) AS requests, SUM(reactions_plus1) AS total_plus1, ROUND(AVG(reactions_plus1),2) AS mean_plus1,
  ROUND(100.0*AVG((state='closed')::INT),1) AS pct_closed
FROM a GROUP BY area HAVING COUNT(*)>=20 ORDER BY total_plus1 DESC;
-- 5. AI share of new requests over time
SELECT CASE WHEN created_at < TIMESTAMP '2025-10-01' THEN 'Oct24-Sep25' ELSE 'Oct25-onwards' END AS period,
  COUNT(*) AS requests, SUM((labels_str LIKE '%Metabot%')::INT) AS ai_requests,
  ROUND(100.0*AVG((labels_str LIKE '%Metabot%')::INT),1) AS ai_share_pct
FROM fr GROUP BY 1 ORDER BY 1;
-- 6. Top open requests
SELECT number, title, reactions_plus1, comments FROM fr WHERE state='open' ORDER BY reactions_plus1 DESC, comments DESC LIMIT 8;
-- 7. Lifecycle signals (not strict stages)
SELECT COUNT(*) AS requested, SUM(has_priority::INT) AS priority_labelled, SUM(has_milestone::INT) AS milestone_assigned,
  SUM((state='closed')::INT) AS closed, SUM((state='closed' AND has_milestone)::INT) AS closed_with_milestone FROM fr;
-- 8. Lead time of closed requests by milestone
SELECT has_milestone, COUNT(*) AS n, median(date_diff('day', created_at, closed_at)) AS median_days,
  quantile_cont(date_diff('day', created_at, closed_at), 0.25) AS p25, quantile_cont(date_diff('day', created_at, closed_at), 0.75) AS p75
FROM fr WHERE state='closed' GROUP BY 1;