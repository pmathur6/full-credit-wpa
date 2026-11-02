# Our WAR scale vs published WAR

Pearson r between our WAR-scale column (runs view on WAR's footing; see README) and Baseball-Reference / FanGraphs WAR,
matched by MLBAM id. Hitters: our hitting WAR scale vs batting WAR (300+ PA). Pitchers: our pitching WAR scale vs
pitching WAR (300+ batters faced). All: hitting + pitching vs total, players with 10+ games.

| Season | Source | Group | Players | r | Ours minus theirs (mean) | Mean abs. difference |
|---|---|---|---|---|---|---|
| 2023 | bWAR | Hitters (300+ PA) | 293 | 0.893 | -0.08 | 0.71 |
| 2023 | bWAR | Pitchers (300+ BF) | 199 | 0.900 | -0.16 | 0.55 |
| 2023 | bWAR | All players (10+ games) | 1177 | 0.911 | +0.00 | 0.47 |
| 2023 | fWAR | Hitters (300+ PA) | 293 | 0.912 | -0.00 | 0.64 |
| 2023 | fWAR | Pitchers (300+ BF) | 199 | 0.842 | -0.30 | 0.65 |
| 2023 | fWAR | All players (10+ games) | 1177 | 0.905 | +0.01 | 0.47 |
| 2023 | bWAR vs fWAR (benchmark) | Hitters (300+ PA) | 293 | 0.926 | +0.07 | 0.57 |
| 2023 | bWAR vs fWAR (benchmark) | Pitchers (300+ BF) | 199 | 0.824 | -0.13 | 0.73 |
| 2023 | bWAR vs fWAR (benchmark) | All players (10+ games) | 1177 | 0.912 | +0.01 | 0.46 |
| 2024 | bWAR | Hitters (300+ PA) | 286 | 0.900 | -0.02 | 0.72 |
| 2024 | bWAR | Pitchers (300+ BF) | 186 | 0.869 | -0.14 | 0.64 |
| 2024 | bWAR | All players (10+ games) | 1137 | 0.907 | +0.00 | 0.49 |
| 2024 | fWAR | Hitters (300+ PA) | 286 | 0.928 | +0.01 | 0.61 |
| 2024 | fWAR | Pitchers (300+ BF) | 186 | 0.844 | -0.30 | 0.66 |
| 2024 | fWAR | All players (10+ games) | 1137 | 0.915 | +0.02 | 0.46 |
| 2024 | bWAR vs fWAR (benchmark) | Hitters (300+ PA) | 286 | 0.934 | +0.03 | 0.55 |
| 2024 | bWAR vs fWAR (benchmark) | Pitchers (300+ BF) | 186 | 0.791 | -0.16 | 0.80 |
| 2024 | bWAR vs fWAR (benchmark) | All players (10+ games) | 1137 | 0.907 | +0.01 | 0.48 |
| 2025 | bWAR | Hitters (300+ PA) | 277 | 0.887 | -0.04 | 0.71 |
| 2025 | bWAR | Pitchers (300+ BF) | 187 | 0.907 | -0.16 | 0.63 |
| 2025 | bWAR | All players (10+ games) | 1174 | 0.910 | +0.00 | 0.48 |
| 2025 | fWAR | Hitters (300+ PA) | 277 | 0.923 | +0.01 | 0.60 |
| 2025 | fWAR | Pitchers (300+ BF) | 187 | 0.845 | -0.27 | 0.68 |
| 2025 | fWAR | All players (10+ games) | 1174 | 0.910 | +0.01 | 0.48 |
| 2025 | bWAR vs fWAR (benchmark) | Hitters (300+ PA) | 277 | 0.924 | +0.05 | 0.57 |
| 2025 | bWAR vs fWAR (benchmark) | Pitchers (300+ BF) | 187 | 0.810 | -0.11 | 0.83 |
| 2025 | bWAR vs fWAR (benchmark) | All players (10+ games) | 1174 | 0.906 | +0.01 | 0.48 |
| 2026 | bWAR | Hitters (300+ PA) | 268 | 0.863 | -0.02 | 0.78 |
| 2026 | bWAR | Pitchers (300+ BF) | 207 | 0.877 | -0.15 | 0.64 |
| 2026 | bWAR | All players (10+ games) | 1155 | 0.900 | +0.00 | 0.49 |
| 2026 | fWAR | Hitters (300+ PA) | 268 | 0.906 | +0.06 | 0.64 |
| 2026 | fWAR | Pitchers (300+ BF) | 207 | 0.820 | -0.25 | 0.71 |
| 2026 | fWAR | All players (10+ games) | 1155 | 0.898 | +0.02 | 0.49 |
| 2026 | bWAR vs fWAR (benchmark) | Hitters (300+ PA) | 268 | 0.921 | +0.07 | 0.54 |
| 2026 | bWAR vs fWAR (benchmark) | Pitchers (300+ BF) | 207 | 0.823 | -0.10 | 0.79 |
| 2026 | bWAR vs fWAR (benchmark) | All players (10+ games) | 1155 | 0.912 | +0.01 | 0.45 |

Pooled across seasons:

| Source | Group | Player-seasons | r |
|---|---|---|---|
| bWAR | All players (10+ games) | 4643 | 0.907 (n-weighted) |
| bWAR | Hitters (300+ PA) | 1124 | 0.886 (n-weighted) |
| bWAR | Pitchers (300+ BF) | 779 | 0.888 (n-weighted) |
| bWAR vs fWAR (benchmark) | All players (10+ games) | 4643 | 0.909 (n-weighted) |
| bWAR vs fWAR (benchmark) | Hitters (300+ PA) | 1124 | 0.927 (n-weighted) |
| bWAR vs fWAR (benchmark) | Pitchers (300+ BF) | 779 | 0.812 (n-weighted) |
| fWAR | All players (10+ games) | 4643 | 0.907 (n-weighted) |
| fWAR | Hitters (300+ PA) | 1124 | 0.917 (n-weighted) |
| fWAR | Pitchers (300+ BF) | 779 | 0.838 (n-weighted) |

## Largest hitter gaps (ours minus theirs)

- 2023 bWAR: below: Kevin Kiermaier 1.0 vs 3.8, Fernando Tatis Jr. 3.1 vs 5.2, Gabriel Moreno 2.3 vs 4.3, Daulton Varsho 1.6 vs 3.6, Randal Grichuk -0.6 vs 1.4
- 2023 bWAR: above: Jonah Heim 5.1 vs 3.1, Elly De La Cruz 2.9 vs 0.7, TJ Friedl 5.9 vs 3.6, Maikel Garcia 3.4 vs 1.1, Brandon Crawford 1.6 vs -1.2
- 2023 fWAR: below: Francisco Alvarez 0.6 vs 3.0, Alejandro Kirk 0.0 vs 2.3, Jordan Walker -1.2 vs 1.0, Michael Harris II 1.9 vs 3.9, William Contreras 3.8 vs 5.8
- 2023 fWAR: above: Salvador Perez 1.3 vs -0.3, Keibert Ruiz 1.1 vs -0.5, TJ Friedl 5.9 vs 4.1, Ezequiel Tovar 3.8 vs 1.7, Elias Díaz 2.8 vs -0.1
- 2024 bWAR: below: Jarren Duran 6.2 vs 9.0, Matt Vierling 0.6 vs 2.8, Tyler O'Neill 0.8 vs 2.9, Jose Siri -0.2 vs 1.8, Adolis García -1.4 vs 0.7
- 2024 bWAR: above: Spencer Steer 3.6 vs 1.5, Jonathan India 4.0 vs 1.7, Brandon Nimmo 4.7 vs 2.2, Bobby Witt Jr. 12.2 vs 9.6, Willy Adames 6.4 vs 3.2
- 2024 fWAR: below: Patrick Bailey 1.0 vs 4.4, Colton Cowser 1.8 vs 4.0, Jose Siri -0.2 vs 1.8, Tyler O'Neill 0.8 vs 2.6, Whit Merrifield -1.3 vs 0.4
- 2024 fWAR: above: Bobby Witt Jr. 12.2 vs 10.5, Spencer Steer 3.6 vs 1.8, Brandon Nimmo 4.7 vs 2.7, Ryan McMahon 4.4 vs 2.0, José Ramírez 8.8 vs 6.3
- 2025 bWAR: below: Adolis García -0.3 vs 2.7, Carson Kelly 1.2 vs 3.5, Randy Arozarena 1.6 vs 3.9, Michael Harris II 0.1 vs 2.3, Danny Jansen 0.7 vs 2.8
- 2025 bWAR: above: Salvador Perez 2.6 vs 0.5, Austin Wells 2.3 vs 0.1, Bobby Witt Jr. 9.6 vs 7.1, Masyn Winn 4.7 vs 2.2, Joey Ortiz 2.8 vs 0.2
- 2025 fWAR: below: Alejandro Kirk 2.4 vs 4.7, Cal Raleigh 7.1 vs 9.1, Patrick Bailey 1.6 vs 3.2, Alek Thomas -1.2 vs 0.5, Wenceel Pérez 0.0 vs 1.7
- 2025 fWAR: above: Bobby Witt Jr. 9.6 vs 8.0, Christian Yelich 4.1 vs 2.5, Gleyber Torres 4.2 vs 2.5, Otto Lopez 4.3 vs 2.3, Salvador Perez 2.6 vs 0.5
- 2026 bWAR: below: Wilyer Abreu 1.8 vs 5.8, Cole Young 1.5 vs 4.4, Junior Caminero 3.5 vs 5.7, Andruw Monasterio -1.5 vs 0.6, Seiya Suzuki 3.0 vs 5.1
- 2026 bWAR: above: Jake McCarthy 3.7 vs 1.9, Kyle Karros 3.3 vs 1.4, Elly De La Cruz 7.9 vs 5.6, Alec Bohm 2.7 vs -0.2, Bryson Stott 5.0 vs 1.8
- 2026 fWAR: below: Junior Caminero 3.5 vs 5.3, Austin Wells -0.1 vs 1.7, Cam Smith -0.3 vs 1.4, Victor Caratini -0.9 vs 0.7, Freddie Freeman 1.0 vs 2.6
- 2026 fWAR: above: Mauricio Dubón 4.5 vs 2.4, Kevin McGonigle 7.5 vs 5.4, Nick Kurtz 5.0 vs 2.6, Alec Bohm 2.7 vs 0.2, Brice Turang 9.1 vs 5.9

## Sources

- bWAR: ok (126,547 batting rows, 57,884 pitching rows)
- fWAR: ok
