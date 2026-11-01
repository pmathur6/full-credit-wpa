# External checks: 2026

Our numbers are wins weighted by game situation; Savant's are context-neutral runs. Correlations measure whether the two rank players the same way. Typical leverage noise alone keeps a perfect-in-substance match below 1.0.

## Correlations

| Comparison | Players | Correlation | Note |
|---|---|---|---|
| Batting vs traditional batter WPA (200+ PA) | 361 | 0.984 | same plays, runners' share removed |
| Batting + baserunning vs traditional batter WPA | 361 | 0.958 |  |
| Pitching vs traditional pitcher WPA (200+ BF) | 343 | 0.914 | fielders' share removed |
| Baserunning vs Savant baserunning run value | 234 | 0.642 | Savant: extra bases + steals |
|   ...vs Savant extra-base runs only | 234 | 0.521 |  |
|   ...vs Savant stolen-base runs only | 234 | 0.526 |  |
| Fielding vs Savant fielding run value (all non-pitchers) | 543 | 0.673 |  |
|   Outfielders vs Savant range + arm | 209 | 0.727 |  |
|   Infielders vs Savant range + arm + DP | 235 | 0.791 |  |
|   Catchers vs Savant throwing + blocking | 99 | 0.489 | framing is not in our numbers |
|   Catchers vs Savant total catching | 99 | 0.093 | includes framing |

Biggest disagreements, baserunning (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Seiya Suzuki | RF/DH | +0.52 wins | -3.2 runs |
| Jakob Marsee | CF | +1.01 wins | +0.6 runs |
| Mauricio Dubón | LF/SS/CF | +0.69 wins | -1.0 runs |
| Nico Hoerner | 2B/SS | +0.25 wins | +5.6 runs |
| Zach Neto | SS | -0.32 wins | +1.0 runs |
| Jake McCarthy | LF/CF/RF/DH | +0.50 wins | +7.2 runs |

Biggest disagreements, outfield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Daniel Schneemann | CF/3B/2B | +1.27 wins | +5.5 runs |
| Davis Schneider | LF/2B | +0.27 wins | -3.2 runs |
| Isaac Collins | LF | +0.57 wins | -0.4 runs |
| Pete Crow-Armstrong | CF | +0.68 wins | +26.3 runs |
| Lane Thomas | CF/LF/RF | -2.01 wins | -3.4 runs |
| Mike Trout | CF/DH | -1.76 wins | -3.8 runs |

Biggest disagreements, infield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Mookie Betts | SS | +1.99 wins | +5.9 runs |
| Alex Bregman | 3B/DH | +2.06 wins | +6.7 runs |
| Gunnar Henderson | SS | +1.20 wins | +0.4 runs |
| Nasim Nuñez | 2B/SS | -0.21 wins | +7.8 runs |
| JJ Wetherholt | 2B/SS | +1.61 wins | +23.4 runs |
| Luke Keaschall | 2B/RF/CF | -2.31 wins | -11.4 runs |

## Sources

```
savant_brv: ok, 234 rows, columns: player_id, entity_name, team_name, start_year, end_year, runner_runs_tot, runner_runs_XB, runner_runs_SBX, N_runner_moved, runner_runs_XB_swipe, runner_runs_XB_snipe, runner_runs_XB_freeze, N_runner_moved_XB, runner_runs_SB2, runner_runs_SB3, simple_stolen_on_running_act_SB2, simple_stolen_on_running_act_SB3, N_runner_moved_SBX
savant_frv: ok, 654 rows, columns: name, id, total_runs, inf_of_runs, range_runs, arm_runs, dp_runs, fielding_runs_prevented_on_rec1b, catching_runs, framing_runs, throwing_runs, blocking_runs, abs_runs, outs_total, outs_2, outs_3, outs_4, outs_5, outs_6, outs_7, outs_8, outs_9
```
