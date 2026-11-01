# Signal vs noise by bucket

Seasons: 2023, 2024, 2025, 2026. Split-half = alternating games within a season, averaged over seasons. Full-season reliability = Spearman-Brown of the split-half. Year to year = same players, consecutive seasons. Stabilizes at = opportunities where reliability reaches 0.5.

| Bucket | Split-half r | Full-season reliability | Year-to-year r | Stabilizes at | Players (split / y-to-y) |
|---|---|---|---|---|---|
| batting | 0.21 | 0.35 | 0.34 | ~958 PA | 275 / 200 |
| baserunning | 0.33 | 0.49 | 0.40 | ~526 PA | 275 / 200 |
| pitching | 0.30 | 0.46 | 0.32 | ~650 batters faced | 182 / 114 |
| fielding | 0.26 | 0.41 | 0.41 | ~149 games in the field | 273 / 189 |
| fielding (outs above expected) | 0.33 | 0.50 | 0.52 | ~106 games in the field | 273 / 189 |
|   outfield (outs above expected) | 0.60 | 0.75 | 0.64 | ~35 games in the field | 273 / 189 |
|   infield (outs above expected) | 0.19 | 0.32 | 0.43 | ~224 games in the field | 273 / 189 |
| coaching (team) | 0.58 | 0.74 | 0.43 | - | 30 / 29 |

Split-half by season:

- batting: 2023 0.30, 2024 0.27, 2025 0.08, 2026 0.19
- baserunning: 2023 0.28, 2024 0.45, 2025 0.33, 2026 0.24
- pitching: 2023 0.14, 2024 0.35, 2025 0.29, 2026 0.41
- fielding: 2023 0.20, 2024 0.23, 2025 0.30, 2026 0.32
- fielding (outs above expected): 2023 0.25, 2024 0.31, 2025 0.37, 2026 0.39
-   outfield (outs above expected): 2023 0.51, 2024 0.60, 2025 0.65, 2026 0.63
-   infield (outs above expected): 2023 0.13, 2024 0.14, 2025 0.21, 2026 0.28
- coaching (team): 2023 0.73, 2024 0.52, 2025 0.46, 2026 0.62

Notes:

- Our buckets are wins, weighted by game situation. A big hit in a close late game counts far more than the same hit in a blowout, and those moments are scattered, so win-based numbers are much noisier than context-neutral stats. That's expected for any WPA-style measure: it records what happened and how much it mattered, not a player's true talent.
- Fielding, leverage-free (outs above expected) vs win-weighted shows how much the game situation adds noise.
- Outfield uses Savant's catch probability from each fielder's actual starting spot; infield uses our model, which can't see where the fielder stood. That gap is the main reason infield is less reliable.
- Coaching's split-half is partly built in: infield positioning is calibrated to each player's season Savant OAA and spread evenly across his chances, so both halves carry the same share. Year to year is the fairer read on whether positioning persists.

Minimums: each half at least 150 PA / 150 batters faced / 30 games in the field; year to year at least double that in both seasons. Coaching is team-level (30 teams).
