# External checks: 2023

Our numbers are wins weighted by game situation; Savant's are context-neutral runs. Correlations measure whether the two rank players the same way. Typical leverage noise alone keeps a perfect-in-substance match below 1.0.

## Correlations

| Comparison | Players | Correlation | Note |
|---|---|---|---|
| Batting vs traditional batter WPA (200+ PA) | 363 | 0.988 | same plays, runners' share removed |
| Batting + baserunning vs traditional batter WPA | 363 | 0.968 |  |
| Pitching vs traditional pitcher WPA (200+ BF) | 376 | 0.902 | fielders' share removed |
| Baserunning vs Savant baserunning run value | 187 | 0.664 | Savant: extra bases + steals |
|   ...vs Savant extra-base runs only | 187 | 0.539 |  |
|   ...vs Savant stolen-base runs only | 187 | 0.584 |  |
| Fielding vs Savant fielding run value (all non-pitchers) | 550 | 0.588 |  |
|   Outfielders vs Savant range + arm | 204 | 0.650 |  |
|   Infielders vs Savant range + arm + DP | 261 | 0.734 |  |
|   Catchers vs Savant throwing + blocking | 85 | 0.692 | framing is not in our numbers |
|   Catchers vs Savant total catching | 85 | 0.308 | includes framing |

Biggest disagreements, baserunning (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| José Ramírez | 3B/DH | +1.16 wins | +0.7 runs |
| Dominic Smith | 1B | +0.36 wins | -5.1 runs |
| Bryan De La Cruz | LF/RF | +0.37 wins | -3.6 runs |
| CJ Abrams | SS | +0.39 wins | +8.0 runs |
| Esteury Ruiz | CF/LF/RF | +0.14 wins | +5.8 runs |
| Bobby Witt Jr. | SS | +0.64 wins | +8.5 runs |

Biggest disagreements, outfield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Masataka Yoshida | LF/DH | -0.50 wins | -11.2 runs |
| Isiah Kiner-Falefa | CF/LF/3B | +0.84 wins | +2.4 runs |
| Ian Happ | LF | +0.12 wins | -4.4 runs |
| Lane Thomas | RF/CF | -1.61 wins | +1.6 runs |
| Teoscar Hernández | RF/DH | -1.49 wins | +1.8 runs |
| Mickey Moniak | CF/RF/LF | -1.24 wins | +2.7 runs |

Biggest disagreements, infield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Alec Bohm | 3B/1B | +0.77 wins | -3.8 runs |
| Pete Alonso | 1B/DH | +1.09 wins | -0.8 runs |
| Adam Frazier | 2B | -0.18 wins | -11.5 runs |
| Andrés Giménez | 2B | +0.48 wins | +15.2 runs |
| Ezequiel Tovar | SS | +0.26 wins | +13.3 runs |
| Bryson Stott | 2B | +0.11 wins | +10.1 runs |

## Sources

```
savant_brv: ok, 187 rows, columns: player_id, entity_name, team_name, start_year, end_year, runner_runs_tot, runner_runs_XB, runner_runs_SBX, N_runner_moved, runner_runs_XB_swipe, runner_runs_XB_snipe, runner_runs_XB_freeze, N_runner_moved_XB, runner_runs_SB2, runner_runs_SB3, simple_stolen_on_running_act_SB2, simple_stolen_on_running_act_SB3, N_runner_moved_SBX
savant_frv: ok, 646 rows, columns: name, id, total_runs, inf_of_runs, range_runs, arm_runs, dp_runs, fielding_runs_prevented_on_rec1b, catching_runs, framing_runs, throwing_runs, blocking_runs, abs_runs, outs_total, outs_2, outs_3, outs_4, outs_5, outs_6, outs_7, outs_8, outs_9
```
