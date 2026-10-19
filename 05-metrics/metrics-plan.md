# Metrics Plan

**Plan, no results.** No feature-usage events or workspace-level adoption data are available in the public source dataset.

## North Star (proposed)

Share of eligible embedding workspaces that publish a theme and continue to render successfully during the observation window. This is an assumption; the window and eligible-workspace definition require validation.

## Inputs

- Theme configuration started.
- At least one supported variable set.
- Preview viewed.
- Theme published.

## Guardrails

- Theme-related rendering errors per publishing workspace.
- Rollback rate after publication.
- Time-to-publish distribution, segmented by workspace and SDK version.

## Definitions

Publish rate = distinct workspaces with `theme_published` / distinct workspaces with `theme_config_started` in the same cohort. Median configuration time = median elapsed minutes from first configuration start to first successful publish per workspace. Deduplicate retries by workspace and event identity; exclude negative durations and flag missing starts.

All targets and event availability are assumptions until instrumentation is implemented and validated. No results are claimed.