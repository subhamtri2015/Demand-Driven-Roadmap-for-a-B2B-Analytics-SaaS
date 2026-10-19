# Competitor Landscape

Facts below are limited to the sources listed. “Not found in docs read” is not evidence that a capability does not exist.

| Capability | Power BI Embedded | Apache Superset | Metabase SDK (public requests only) | Looker | Tableau |
|---|---|---|---|---|
| Embed theming mechanism | IReportTheme object in embed configuration | From version 6.0, token-based theming built on Ant Design v5 | Public issue #59237 requests CSS variables for SDK theming; no support claim | Not researched | Not researched |
| CSS-variable theming | Not found in docs read | Not found in docs read for embeds | Public request #59237 only; no support claim | Not researched | Not researched |
| Runtime theme change | `applyTheme`; `resetTheme` resets it | Vendor blog says themes can be passed dynamically via Embedded SDK | Not researched | Not researched | Not researched |
| Per-dashboard or per-report theme | Report theme JSON sets defaults for report visuals | Per-dashboard themes | Not researched | Not researched | Not researched |
| Theme management API | Not researched | Theme Management interface; REST endpoints including `POST /api/v1/theme/` | Not researched | Not researched | Not researched |
| Evidence of theme-precedence problems | Not found in docs read | PR #40763 describes SDK-set theme ignored when dashboard has own theme and proposes a fix; status not verified | Not researched | Not researched | Not researched |

## Where a CSS-variable approach would differ (hypothesis)

A CSS-variable interface could be easier for host applications to connect to existing design tokens, but the useful scope, isolation rules, and precedence behavior require user validation. This is a product hypothesis, not a claim about current SDK support.

## Sources

- https://learn.microsoft.com/en-us/javascript/api/overview/powerbi/apply-report-themes
- https://superset.apache.org/docs/configuration/theming
- https://preset.io/blog/superset-6-theming/
- https://github.com/apache/superset/pull/40763
- https://github.com/metabase/metabase/issues/59237