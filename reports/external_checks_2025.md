# External checks: 2025

Our numbers are wins weighted by game situation; Savant's are context-neutral runs. Correlations measure whether the two rank players the same way. Typical leverage noise alone keeps a perfect-in-substance match below 1.0.

## Correlations

| Comparison | Players | Correlation | Note |
|---|---|---|---|
| Batting vs traditional batter WPA (200+ PA) | 348 | 0.986 | same plays, runners' share removed |
| Batting + baserunning vs traditional batter WPA | 348 | 0.957 |  |
| Pitching vs traditional pitcher WPA (200+ BF) | 356 | 0.909 | fielders' share removed |
| Baserunning vs Savant baserunning run value | 253 | 0.702 | Savant: extra bases + steals |
|   ...vs Savant extra-base runs only | 253 | 0.594 |  |
|   ...vs Savant stolen-base runs only | 253 | 0.537 |  |
| Fielding vs Savant fielding run value (all non-pitchers) | 552 | 0.585 |  |
|   Outfielders vs Savant range + arm | 210 | 0.762 |  |
|   Infielders vs Savant range + arm + DP | 256 | 0.648 |  |
|   Catchers vs Savant throwing + blocking | 86 | 0.663 | framing is not in our numbers |
|   Catchers vs Savant total catching | 86 | 0.452 | includes framing |

Biggest disagreements, baserunning (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Fernando Tatis Jr. | RF | +1.79 wins | +4.7 runs |
| Mookie Betts | SS | +0.79 wins | +0.3 runs |
| Taylor Walls | SS | +0.78 wins | +0.3 runs |
| Corbin Carroll | RF | +0.76 wins | +10.1 runs |
| Jung Hoo Lee | CF | -0.30 wins | +2.8 runs |
| Jarren Duran | LF/CF | +0.38 wins | +7.2 runs |

Biggest disagreements, outfield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Lourdes Gurriel Jr. | LF/DH | +0.46 wins | -2.8 runs |
| Brandon Marsh | CF/LF | +0.76 wins | +1.1 runs |
| Brooks Baldwin | LF/CF/RF/3B/2B/SS | -0.42 wins | -10.4 runs |
| Alek Thomas | CF | -1.65 wins | +0.0 runs |
| Oneil Cruz | CF | -0.93 wins | +3.9 runs |
| Kyle Tucker | RF/DH | -1.30 wins | -0.0 runs |

Biggest disagreements, infield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Bo Bichette | SS | +1.22 wins | -10.3 runs |
| Trevor Story | SS | +1.01 wins | -7.9 runs |
| J.P. Crawford | SS | +0.32 wins | -8.7 runs |
| Marcus Semien | 2B | -0.73 wins | +5.6 runs |
| Ke'Bryan Hayes | 3B | +1.29 wins | +17.1 runs |
| Jonathan Aranda | 1B/DH | -0.92 wins | +1.8 runs |

## Sources

```
fg_bat: FAILED HTTPError('403 Client Error: Forbidden for url: https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=bat&lg=all&qual=0&season=2025&season1=2025&startdate=&enddate=&month=0&hand=&team=0&pageitems=2000000&pagenum=1&ind=0&rost=0&players=&type=8')
fg_pit: FAILED HTTPError('403 Client Error: Forbidden for url: https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats=pit&lg=all&qual=0&season=2025&season1=2025&startdate=&enddate=&month=0&hand=&team=0&pageitems=2000000&pagenum=1&ind=0&rost=0&players=&type=8')
savant_brv: ok, 253 rows, columns: player_id, entity_name, team_name, start_year, end_year, runner_runs_tot, runner_runs_XB, runner_runs_SBX, N_runner_moved, runner_runs_XB_swipe, runner_runs_XB_snipe, runner_runs_XB_freeze, N_runner_moved_XB, runner_runs_SB2, runner_runs_SB3, simple_stolen_on_running_act_SB2, simple_stolen_on_running_act_SB3, N_runner_moved_SBX
savant_frv: ok, 662 rows, columns: name, id, total_runs, inf_of_runs, range_runs, arm_runs, dp_runs, fielding_runs_prevented_on_rec1b, catching_runs, framing_runs, throwing_runs, blocking_runs, abs_runs, outs_total, outs_2, outs_3, outs_4, outs_5, outs_6, outs_7, outs_8, outs_9
```
