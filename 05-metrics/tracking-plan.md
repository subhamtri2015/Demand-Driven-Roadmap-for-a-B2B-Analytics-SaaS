# Tracking Plan

**Plan, no results.** Events below are proposed, not observed.

| Event | Trigger | Properties |
|---|---|---|
| `theme_config_started` | User enters theme configuration | workspace_id, sdk_version, entry_point, occurred_at |
| `theme_variable_set` | A supported variable value is changed | workspace_id, variable_name, value_type, sdk_version, occurred_at |
| `theme_preview_viewed` | Preview is rendered and displayed | workspace_id, sdk_version, preview_mode, occurred_at |
| `theme_published` | Theme configuration is accepted for use | workspace_id, sdk_version, variable_count, occurred_at |
| `theme_error` | Theme application or validation fails | workspace_id, sdk_version, error_category, occurred_at |

Do not send raw theme values, user-entered content, or personal data. Confirm consent, retention, access controls, and aggregation requirements with privacy and engineering before implementation.