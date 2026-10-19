# RICE Prioritization

Reach is the sum of 👍 on qualifying **open** public issues, calculated from `data/processed/reach_inputs.csv`. Reach is a vocal-user proxy, not customer count. Impact, confidence, and effort are assumptions; scores are decision aids, not measured outcomes.

| Rank | Initiative | Reach (👍 proxy) | Impact (assumption) | Confidence (assumption) | Effort (assumption) | Score |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Embedding SDK theming with CSS variables | 36 | 2 | 80% | 2 | 28.80 |
| 2 | Warehouse connector gaps | 56 | 2 | 70% | 3 | 26.13 |
| 3 | Granular permissions and controlled access | 79 | 3 | 50% | 5 | 23.70 |
| 4 | Dashboard filters and parameters | 90 | 2 | 40% | 4 | 18.00 |
| 5 | Remote sync with multiple branches | 30 | 2 | 60% | 3 | 12.00 |

The lead between first and second is 2.67 score points (9.3% of the top score), so the rank is not robust to small assumption changes.

## Sensitivity

| Case | Recalculated score | Interpretation |
|---|---:|---|
| C confidence changed to 70% | 33.18 | Permissions moves above the base A score. |
| A effort changed to 3 | 19.20 | A no longer leads; this case changes the ordering. |

These scenarios vary assumptions only. They do not change the observed reach values. Use Now as a discovery recommendation, not a delivery commitment.
