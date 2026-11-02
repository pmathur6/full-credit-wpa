# External checks: 2025

Our numbers are wins weighted by game situation; Savant's are context-neutral runs. Correlations measure whether the two rank players the same way. Typical leverage noise alone keeps a perfect-in-substance match below 1.0.

## Correlations

| Comparison | Players | Correlation | Note |
|---|---|---|---|
| Batting vs traditional batter WPA (200+ PA) | 348 | 0.987 | same plays, runners' share removed |
| Batting + baserunning vs traditional batter WPA | 348 | 0.960 |  |
| Pitching vs traditional pitcher WPA (200+ BF) | 356 | 0.910 | fielders' share removed |
| Baserunning vs Savant baserunning run value | 253 | 0.705 | Savant: extra bases + steals |
|   ...vs Savant extra-base runs only | 253 | 0.602 |  |
|   ...vs Savant stolen-base runs only | 253 | 0.532 |  |
| Fielding vs Savant fielding run value (all non-pitchers) | 552 | 0.625 |  |
|   Outfielders vs Savant range + arm | 210 | 0.699 |  |
|   Infielders vs Savant range + arm + DP | 256 | 0.748 |  |
|   Catchers vs Savant throwing + blocking | 86 | 0.606 | framing is not in our numbers |
|   Catchers vs Savant total catching | 86 | 0.434 | includes framing |

Biggest disagreements, baserunning (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Fernando Tatis Jr. | RF | +1.78 wins | +4.7 runs |
| Taylor Walls | SS | +0.80 wins | +0.3 runs |
| Willson Contreras | 1B/DH | +0.37 wins | -2.2 runs |
| Jung Hoo Lee | CF | -0.30 wins | +2.8 runs |
| Corbin Carroll | RF | +0.74 wins | +10.1 runs |
| Jarren Duran | LF/CF | +0.34 wins | +7.2 runs |

Biggest disagreements, outfield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| James Wood | LF/DH | +0.21 wins | -6.3 runs |
| Lars Nootbaar | LF/RF/CF | +0.45 wins | -3.8 runs |
| Brooks Baldwin | LF/CF/RF/3B/2B/SS | -0.47 wins | -10.4 runs |
| Alek Thomas | CF | -1.97 wins | +0.0 runs |
| Corbin Carroll | RF | -1.01 wins | +6.5 runs |
| Victor Scott II | CF | -0.28 wins | +12.1 runs |

Biggest disagreements, infield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Bo Bichette | SS | +0.09 wins | -10.3 runs |
| Matt Chapman | 3B | +1.78 wins | +4.1 runs |
| Isaac Paredes | 3B/DH | +0.79 wins | -2.6 runs |
| Marcus Semien | 2B | -1.10 wins | +5.6 runs |
| Daniel Schneemann | 2B/3B/CF/RF/SS | +0.19 wins | +8.2 runs |
| Jonathan Aranda | 1B/DH | -0.60 wins | +1.8 runs |

## Sources

```
savant_brv: ok, 253 rows, columns: player_id, entity_name, team_name, start_year, end_year, runner_runs_tot, runner_runs_XB, runner_runs_SBX, N_runner_moved, runner_runs_XB_swipe, runner_runs_XB_snipe, runner_runs_XB_freeze, N_runner_moved_XB, runner_runs_SB2, runner_runs_SB3, simple_stolen_on_running_act_SB2, simple_stolen_on_running_act_SB3, N_runner_moved_SBX
savant_frv: ok, 662 rows, columns: name, id, total_runs, inf_of_runs, range_runs, arm_runs, dp_runs, fielding_runs_prevented_on_rec1b, catching_runs, framing_runs, throwing_runs, blocking_runs, abs_runs, outs_total, outs_2, outs_3, outs_4, outs_5, outs_6, outs_7, outs_8, outs_9
```
