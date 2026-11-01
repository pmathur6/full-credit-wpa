# External checks: 2024

Our numbers are wins weighted by game situation; Savant's are context-neutral runs. Correlations measure whether the two rank players the same way. Typical leverage noise alone keeps a perfect-in-substance match below 1.0.

## Correlations

| Comparison | Players | Correlation | Note |
|---|---|---|---|
| Batting vs traditional batter WPA (200+ PA) | 365 | 0.988 | same plays, runners' share removed |
| Batting + baserunning vs traditional batter WPA | 365 | 0.966 |  |
| Pitching vs traditional pitcher WPA (200+ BF) | 368 | 0.912 | fielders' share removed |
| Baserunning vs Savant baserunning run value | 180 | 0.656 | Savant: extra bases + steals |
|   ...vs Savant extra-base runs only | 180 | 0.569 |  |
|   ...vs Savant stolen-base runs only | 180 | 0.488 |  |
| Fielding vs Savant fielding run value (all non-pitchers) | 534 | 0.618 |  |
|   Outfielders vs Savant range + arm | 199 | 0.711 |  |
|   Infielders vs Savant range + arm + DP | 253 | 0.768 |  |
|   Catchers vs Savant throwing + blocking | 82 | 0.534 | framing is not in our numbers |
|   Catchers vs Savant total catching | 82 | 0.213 | includes framing |

Biggest disagreements, baserunning (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Masyn Winn | SS | +1.42 wins | +2.2 runs |
| Nico Hoerner | 2B/SS | +1.58 wins | +4.9 runs |
| Tyler Fitzgerald | SS | +1.27 wins | +2.8 runs |
| Corbin Carroll | CF/RF | +1.08 wins | +12.4 runs |
| Jake McCarthy | RF/CF/LF | +0.05 wins | +4.2 runs |
| CJ Abrams | SS | +0.00 wins | +3.8 runs |

Biggest disagreements, outfield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Mauricio Dubón | LF/2B/CF/1B/RF/3B | +1.39 wins | +7.1 runs |
| Randy Arozarena | LF | -0.07 wins | -7.4 runs |
| Jason Heyward | RF | +0.52 wins | +1.0 runs |
| Jacob Young | CF | -0.03 wins | +16.7 runs |
| Jake McCarthy | RF/CF/LF | -1.16 wins | +4.8 runs |
| Leody Taveras | CF | -0.98 wins | +5.0 runs |

Biggest disagreements, infield (standardized; + = we rate higher):

| Player | Pos | Ours | Savant |
|---|---|---|---|
| Isaac Paredes | 3B/1B/DH | +1.03 wins | -0.6 runs |
| Emmanuel Rivera | 3B/1B | +0.74 wins | -2.6 runs |
| José Ramírez | 3B/DH | +1.28 wins | +1.9 runs |
| Oneil Cruz | SS/CF/DH | -1.02 wins | +0.2 runs |
| Carlos Santana | 1B | +0.54 wins | +11.2 runs |
| Ketel Marte | 2B/DH | +0.16 wins | +7.6 runs |

## Sources

```
savant_brv: ok, 180 rows, columns: player_id, entity_name, team_name, start_year, end_year, runner_runs_tot, runner_runs_XB, runner_runs_SBX, N_runner_moved, runner_runs_XB_swipe, runner_runs_XB_snipe, runner_runs_XB_freeze, N_runner_moved_XB, runner_runs_SB2, runner_runs_SB3, simple_stolen_on_running_act_SB2, simple_stolen_on_running_act_SB3, N_runner_moved_SBX
savant_frv: ok, 640 rows, columns: name, id, total_runs, inf_of_runs, range_runs, arm_runs, dp_runs, fielding_runs_prevented_on_rec1b, catching_runs, framing_runs, throwing_runs, blocking_runs, abs_runs, outs_total, outs_2, outs_3, outs_4, outs_5, outs_6, outs_7, outs_8, outs_9
```
