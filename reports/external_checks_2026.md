# External checks: 2026

Our numbers are wins weighted by game situation; Savant's are context-neutral runs. Correlations measure whether the two rank players the same way. Typical leverage noise alone keeps a perfect-in-substance match below 1.0.

## Correlations

| Comparison | Players | Correlation | Note |
|---|---|---|---|
| Batting vs traditional batter WPA (200+ PA) | 361 | 0.984 | same plays, runners' share removed |
| Batting + baserunning vs traditional batter WPA | 361 | 0.961 |  |
| Pitching vs traditional pitcher WPA (200+ BF) | 343 | 0.913 | fielders' share removed |
| Baserunning vs Savant baserunning run value | 234 | 0.658 | Savant: extra bases + steals |
|   ...vs Savant extra-base runs only | 234 | 0.526 |  |
|   ...vs Savant stolen-base runs only | 234 | 0.550 |  |
| Fielding vs Savant fielding run value (all non-pitchers) | 543 | 0.678 |  |
|   Outfielders vs Savant range + arm | 209 | 0.735 |  |
|   Infielders vs Savant range + arm + DP | 235 | 0.793 |  |
|   Catchers vs Savant throwing + blocking | 99 | 0.492 | framing is not in our numbers |
|   Catchers vs Savant total catching | 99 | 0.099 | includes framing |

Biggest disagreements, baserunning (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Seiya Suzuki | RF/DH | +0.48 wins | -3.2 runs |
| Mauricio Dubón | LF/SS/CF | +0.68 wins | -1.0 runs |
| Yandy Díaz | DH | +0.50 wins | -2.4 runs |
| Nico Hoerner | 2B/SS | +0.25 wins | +5.6 runs |
| Zach Neto | SS | -0.32 wins | +1.0 runs |
| Willi Castro | 2B/3B/SS/1B | -0.39 wins | +0.5 runs |

Biggest disagreements, outfield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Isaac Collins | LF | +0.66 wins | -0.4 runs |
| Daniel Schneemann | CF/3B/2B | +1.28 wins | +5.5 runs |
| Davis Schneider | LF/2B | +0.24 wins | -3.2 runs |
| Pete Crow-Armstrong | CF | +0.76 wins | +26.3 runs |
| Lane Thomas | CF/LF/RF | -2.03 wins | -3.4 runs |
| Dane Myers | CF/DH | -1.35 wins | -0.7 runs |

Biggest disagreements, infield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Alex Bregman | 3B/DH | +2.15 wins | +6.7 runs |
| Mookie Betts | SS | +2.00 wins | +5.9 runs |
| Willy Adames | SS | -0.40 wins | -13.8 runs |
| JJ Wetherholt | 2B/SS | +1.62 wins | +23.4 runs |
| Nasim Nuñez | 2B/SS | -0.12 wins | +7.8 runs |
| Alex Freeland | 2B | -0.73 wins | +1.5 runs |

## Sources

```
savant_brv: ok, 234 rows, columns: player_id, entity_name, team_name, start_year, end_year, runner_runs_tot, runner_runs_XB, runner_runs_SBX, N_runner_moved, runner_runs_XB_swipe, runner_runs_XB_snipe, runner_runs_XB_freeze, N_runner_moved_XB, runner_runs_SB2, runner_runs_SB3, simple_stolen_on_running_act_SB2, simple_stolen_on_running_act_SB3, N_runner_moved_SBX
savant_frv: ok, 654 rows, columns: name, id, total_runs, inf_of_runs, range_runs, arm_runs, dp_runs, fielding_runs_prevented_on_rec1b, catching_runs, framing_runs, throwing_runs, blocking_runs, abs_runs, outs_total, outs_2, outs_3, outs_4, outs_5, outs_6, outs_7, outs_8, outs_9
```
