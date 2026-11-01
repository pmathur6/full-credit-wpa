# External checks: 2023

Our numbers are wins weighted by game situation; Savant's are context-neutral runs. Correlations measure whether the two rank players the same way. Typical leverage noise alone keeps a perfect-in-substance match below 1.0.

## Correlations

| Comparison | Players | Correlation | Note |
|---|---|---|---|
| Batting vs traditional batter WPA (200+ PA) | 363 | 0.986 | same plays, runners' share removed |
| Batting + baserunning vs traditional batter WPA | 363 | 0.966 |  |
| Pitching vs traditional pitcher WPA (200+ BF) | 376 | 0.903 | fielders' share removed |
| Baserunning vs Savant baserunning run value | 187 | 0.656 | Savant: extra bases + steals |
|   ...vs Savant extra-base runs only | 187 | 0.538 |  |
|   ...vs Savant stolen-base runs only | 187 | 0.569 |  |
| Fielding vs Savant fielding run value (all non-pitchers) | 550 | 0.575 |  |
|   Outfielders vs Savant range + arm | 204 | 0.629 |  |
|   Infielders vs Savant range + arm + DP | 261 | 0.728 |  |
|   Catchers vs Savant throwing + blocking | 85 | 0.690 | framing is not in our numbers |
|   Catchers vs Savant total catching | 85 | 0.306 | includes framing |

Biggest disagreements, baserunning (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| José Ramírez | 3B/DH | +1.18 wins | +0.7 runs |
| Enrique Hernández | SS/2B/CF/3B/LF/1B | +0.80 wins | -1.6 runs |
| Dominic Smith | 1B | +0.28 wins | -5.1 runs |
| Esteury Ruiz | CF/LF/RF | +0.16 wins | +5.8 runs |
| CJ Abrams | SS | +0.49 wins | +8.0 runs |
| Bobby Witt Jr. | SS | +0.64 wins | +8.5 runs |

Biggest disagreements, outfield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Masataka Yoshida | LF/DH | -0.36 wins | -11.2 runs |
| Ian Happ | LF | +0.07 wins | -4.4 runs |
| Randy Arozarena | LF/DH | -0.24 wins | -6.8 runs |
| Lane Thomas | RF/CF | -1.57 wins | +1.6 runs |
| Teoscar Hernández | RF/DH | -1.54 wins | +1.8 runs |
| Myles Straw | CF | -1.34 wins | +3.3 runs |

Biggest disagreements, infield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Adam Frazier | 2B | -0.13 wins | -11.5 runs |
| Alec Bohm | 3B/1B | +0.76 wins | -3.8 runs |
| Pete Alonso | 1B/DH | +1.09 wins | -0.8 runs |
| Andrés Giménez | 2B | +0.47 wins | +15.2 runs |
| Ezequiel Tovar | SS | +0.25 wins | +13.3 runs |
| Bryson Stott | 2B | +0.16 wins | +10.1 runs |

## Sources

```
savant_brv: ok, 187 rows, columns: player_id, entity_name, team_name, start_year, end_year, runner_runs_tot, runner_runs_XB, runner_runs_SBX, N_runner_moved, runner_runs_XB_swipe, runner_runs_XB_snipe, runner_runs_XB_freeze, N_runner_moved_XB, runner_runs_SB2, runner_runs_SB3, simple_stolen_on_running_act_SB2, simple_stolen_on_running_act_SB3, N_runner_moved_SBX
savant_frv: ok, 646 rows, columns: name, id, total_runs, inf_of_runs, range_runs, arm_runs, dp_runs, fielding_runs_prevented_on_rec1b, catching_runs, framing_runs, throwing_runs, blocking_runs, abs_runs, outs_total, outs_2, outs_3, outs_4, outs_5, outs_6, outs_7, outs_8, outs_9
```
