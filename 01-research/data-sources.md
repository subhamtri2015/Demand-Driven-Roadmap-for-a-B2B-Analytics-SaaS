# Data Sources

Independent analysis of public information; not affiliated with or endorsed by Metabase.

| Source | Endpoint / query | Pull date | Fields kept | Fields dropped | Notes |
|---|---|---|---|---|---|
| GitHub feature requests | `https://api.github.com/search/issues`; `repo:metabase/metabase is:issue label:"Type:New Feature" created:<month window>` | 2026-10-19 | number, title, state, created_at, closed_at, comments, reactions +1, labels, milestone title | bodies, author names | Four date windows; requests are deduplicated by issue number. Commit aggregates only. |
| GitHub merged PRs | `https://api.github.com/search/issues`; `repo:metabase/metabase is:pr is:merged merged:<month window>` | 2026-10-19 | `total_count` only | PR bodies, identities, titles, individual PR records | Monthly aggregate. Counts include bots and backports; not velocity. |
| npm package metadata | `https://registry.npmjs.org/@metabase/embedding-sdk-react`; package `time` map | 2026-10-19 | stable `0.x.y` versions and publish timestamps | package metadata not used for release-line calculation | npm only shows published versions. |
| npm downloads | `https://api.npmjs.org/downloads/range/<start>:<end>/@metabase/embedding-sdk-react` | Not pulled | None | All | Pull manually; optional API not queried in this run. |
| Power BI Embedded | https://learn.microsoft.com/en-us/javascript/api/overview/powerbi/apply-report-themes | 2026-10-18 | Facts listed in competitor-landscape.md | Other product claims | Read for this independent case study. |
| Apache Superset | https://superset.apache.org/docs/configuration/theming ; https://preset.io/blog/superset-6-theming/ ; https://github.com/apache/superset/pull/40763 | 2026-10-18 | Facts listed in competitor-landscape.md | Other product claims | PR status not verified. |
| Customer interviews | Not applicable | Not conducted | None | None | Blank template only; no interviews or quotes are represented. |
| Screenshots | Not applicable | Not provided | None | None | User will add real Jira, Confluence, and Figma screenshots. |

GitHub credentials were read from the local environment only and were not written to project files. Metabase's repository licence, GitHub API terms and npm registry terms must be checked before publishing; only aggregates are committed.