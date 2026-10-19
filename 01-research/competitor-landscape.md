# Competitor Landscape

Facts below are limited to the sources listed. “Not found in docs read” is not evidence that a capability does not exist.

| Capability | Power BI Embedded | Apache Superset | Metabase SDK (public requests only) | Looker | Tableau |
|---|---|---|---|---|
| Embed theming mechanism | `IReportTheme` in embed configuration | Version 6.0 token-based theming on Ant Design v5 | Public issue #59237 requests CSS variables; no support claim | Custom themes for embedded dashboards and Explores; Looker Embed SDK supports embedding content | Embedding API v3 web components for views; no theme mechanism found in docs read |
| CSS-variable theming | Not found in docs read | Not found in docs read for embeds | Public request #59237 only; no support claim | Not found in docs read | Not found in docs read |
| Runtime theme change | `applyTheme`; `resetTheme` resets it | Vendor blog says themes can be passed dynamically via Embedded SDK | Not researched | `theme` and `_theme` URL arguments select/override embed theme settings; live post-load change not found in docs read | No theme change found; workbook parameters can be changed interactively |
| Per-dashboard or per-report theme | Report theme JSON sets defaults for report visuals | Per-dashboard themes | Not researched | `theme=` selects a theme for a dashboard or Explore; custom themes are not supported on embedded Looks | Embedded view selected with `src`; per-view theme not found in docs read |
| Theme management API | Not researched | Theme Management interface; REST endpoints including `POST /api/v1/theme/` | Not researched | Themes admin page manages themes; docs reference Theme API schema for `_theme` properties | Not found in docs read |
| Evidence of theme-precedence problems | Not found in docs read | PR #40763 describes SDK-set theme ignored when dashboard has own theme and proposes a fix; status not verified | Not researched | Docs specify precedence: default theme, then custom `theme`, then specified `_theme` properties | Not found in docs read |

## Where a CSS-variable approach would differ (hypothesis)

A CSS-variable interface could be easier for host applications to connect to existing design tokens, but the useful scope, isolation rules, and precedence behavior require user validation. This is a product hypothesis, not a claim about current SDK support.

## Sources

- https://learn.microsoft.com/en-us/javascript/api/overview/powerbi/apply-report-themes
- https://superset.apache.org/docs/configuration/theming
- https://preset.io/blog/superset-6-theming/
- https://github.com/apache/superset/pull/40763
- https://github.com/metabase/metabase/issues/59237
- https://docs.cloud.google.com/looker/docs/themes-for-embedded-dashboards-and-explores (checked 2026-10-19)
- https://docs.cloud.google.com/looker/docs/embed-sdk-intro (checked 2026-10-19)
- https://docs.cloud.google.com/looker/docs/reference/looker-api/latest/methods/Theme/create_theme (checked 2026-10-19)
- https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_configure.html (checked 2026-10-19)
- https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_parameters.html (checked 2026-10-19)
- https://help.tableau.com/current/api/embedding_api/en-us/docs/embedding_api_auth.html (checked 2026-10-19)