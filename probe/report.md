# Probe report: 2025-07-04

## Savant pitch-level CSV
- Rows (pitches): 4,424; columns: 119; games: 15

| Group | Field | Present | Non-null % |
|---|---|---|---|
| game state | `game_pk` | yes | 100% |
| game state | `at_bat_number` | yes | 100% |
| game state | `pitch_number` | yes | 100% |
| game state | `inning` | yes | 100% |
| game state | `inning_topbot` | yes | 100% |
| game state | `outs_when_up` | yes | 100% |
| game state | `balls` | yes | 100% |
| game state | `strikes` | yes | 100% |
| game state | `home_score` | yes | 100% |
| game state | `away_score` | yes | 100% |
| game state | `bat_score` | yes | 100% |
| game state | `fld_score` | yes | 100% |
| game state | `post_bat_score` | yes | 100% |
| runners | `on_1b` | yes | 30% |
| runners | `on_2b` | yes | 19% |
| runners | `on_3b` | yes | 9% |
| players | `batter` | yes | 100% |
| players | `pitcher` | yes | 100% |
| players | `fielder_2` | yes | 100% |
| players | `fielder_3` | yes | 100% |
| players | `fielder_4` | yes | 100% |
| players | `fielder_5` | yes | 100% |
| players | `fielder_6` | yes | 100% |
| players | `fielder_7` | yes | 100% |
| players | `fielder_8` | yes | 100% |
| players | `fielder_9` | yes | 100% |
| outcome | `events` | yes | 26% |
| outcome | `description` | yes | 100% |
| outcome | `des` | yes | 26% |
| outcome | `type` | yes | 100% |
| outcome | `bb_type` | yes | 18% |
| batted ball | `launch_speed` | yes | 33% |
| batted ball | `launch_angle` | yes | 33% |
| batted ball | `hc_x` | yes | 18% |
| batted ball | `hc_y` | yes | 18% |
| batted ball | `hit_location` | yes | 23% |
| batted ball | `hit_distance_sc` | yes | 33% |
| batted ball | `estimated_ba_using_speedangle` | yes | 18% |
| batted ball | `estimated_woba_using_speedangle` | yes | 26% |
| win/run value | `delta_home_win_exp` | yes | 100% |
| win/run value | `delta_run_exp` | yes | 99% |
| win/run value | `home_win_exp` | yes | 100% |
| win/run value | `bat_win_exp` | yes | 100% |
| alignment | `if_fielding_alignment` | yes | 99% |
| alignment | `of_fielding_alignment` | yes | 99% |
| pitch location | `plate_x` | yes | 99% |
| pitch location | `plate_z` | yes | 99% |
| pitch location | `zone` | yes | 99% |
| pitch location | `sz_top` | yes | 99% |
| pitch location | `sz_bot` | yes | 99% |

Event counts:

| Event | n |
|---|---|
| field_out | 473 |
| strikeout | 254 |
| single | 159 |
| walk | 85 |
| double | 49 |
| home_run | 48 |
| force_out | 24 |
| hit_by_pitch | 15 |
| grounded_into_double_play | 14 |
| field_error | 10 |
| sac_fly | 7 |
| intent_walk | 5 |
| sac_bunt | 4 |
| triple | 3 |
| double_play | 2 |
| fielders_choice | 2 |
| truncated_pa | 2 |
| fielders_choice_out | 2 |
| catcher_interf | 1 |

Other columns: `age_bat`, `age_bat_legacy`, `age_pit`, `age_pit_legacy`, `api_break_x_arm`, `api_break_x_batter_in`, `api_break_z_with_gravity`, `arm_angle`, `attack_angle`, `attack_direction`, `away_team`, `ax`, `ay`, `az`, `babip_value`, `bat_score_diff`, `bat_speed`, `batter_days_since_prev_game`, `batter_days_until_next_game`, `break_angle_deprecated`, `break_length_deprecated`, `delta_pitcher_run_exp`, `effective_speed`, `estimated_slg_using_speedangle`, `game_date`, `game_type`, `game_year`, `home_score_diff`, `home_team`, `hyper_speed`, `intercept_ball_minus_batter_pos_x_inches`, `intercept_ball_minus_batter_pos_y_inches`, `iso_value`, `launch_speed_angle`, `miss_distance`, `n_priorpa_thisgame_player_at_bat`, `n_thruorder_pitcher`, `p_throws`, `pfx_x`, `pfx_z`, `pitch_name`, `pitch_type`, `pitcher_days_since_prev_game`, `pitcher_days_until_next_game`, `player_name`, `post_away_score`, `post_fld_score`, `post_home_score`, `release_extension`, `release_pos_x`, `release_pos_y`, `release_pos_z`, `release_speed`, `release_spin_rate`, `spin_axis`, `spin_dir`, `spin_rate_deprecated`, `stand`, `sv_id`, `swing_length`, `swing_path_tilt`, `tfs_deprecated`, `tfs_zulu_deprecated`, `umpire`, `vx0`, `vy0`, `vz0`, `woba_denom`, `woba_value`

## MLB Stats API live feed
- Games on 2025-07-04: 15
- Sample game 777245: 84 plays
- Runner movements: 129

Fielding credits on runner movements:

- f_assist (1B): 1
- f_assist (2B): 8
- f_assist (SS): 6
- f_deflection (2B): 1
- f_fielded_ball (2B): 1
- f_fielded_ball (3B): 2
- f_fielded_ball (CF): 7
- f_fielded_ball (LF): 3
- f_fielded_ball (RF): 7
- f_fielded_ball (SS): 2
- f_putout (1B): 10
- f_putout (2B): 3
- f_putout (3B): 2
- f_putout (C): 17
- f_putout (CF): 8
- f_putout (LF): 6
- f_putout (RF): 4
- f_putout (SS): 4

Runner movement reasons (mid-PA events):

- r_adv_force: 20
- r_adv_play: 15
- r_force_out: 6
- r_stolen_base_2b: 4

Mid-PA event types (playEvents):

- batter_timeout: 14
- defensive_substitution: 2
- game_advisory: 3
- mound_visit: 6
- pitching_substitution: 6
- stolen_base_2b: 4

- hitData fields: ['coordinates', 'hardness', 'launchAngle', 'launchSpeed', 'location', 'totalDistance', 'trajectory']
- hitData.coordinates: ['coordX', 'coordY']

## Savant game feed (gf endpoint)
- Top-level keys: ['away_batters', 'away_lineup', 'away_pitcher_lineup', 'away_pitchers', 'away_team_data', 'boxscore', 'cacheKey', 'cache_hit', 'exit_velocity', 'gameDate', 'game_date', 'game_status', 'game_status_code', 'gamedayType', 'hasAbs', 'home_batters', 'home_lineup', 'home_pitcher_lineup', 'home_pitchers', 'home_team_data', 'players', 'scoreboard', 'team_away', 'team_away_id', 'team_home', 'team_home_id', 'venue_id']

Keys mentioning catch / prob / oaa / success / hang / sprint / arm:

- `away_batters.596115[].catcher`
- `away_batters.596115[].catcher_name`
- `away_batters.647351[].catcher`
- `away_batters.647351[].catcher_name`
- `away_batters.665966[].catcher`
- `away_batters.665966[].catcher_name`
- `away_batters.666152[].catcher`
- `away_batters.666152[].catcher_name`
- `away_batters.677800[].catcher`
- `away_batters.677800[].catcher_name`
- `home_pitchers.605177[].catcher`
- `home_pitchers.605177[].catcher_name`
- `home_pitchers.647336[].catcher`
- `home_pitchers.647336[].catcher_name`
- `home_pitchers.674285[].catcher`
- `home_pitchers.674285[].catcher_name`
- `home_pitchers.694350[].catcher`
- `home_pitchers.694350[].catcher_name`
- `home_pitchers.702795[].catcher`
- `home_pitchers.702795[].catcher_name`
- `scoreboard.currentPlay.awayTeamWinProbability`
- `scoreboard.currentPlay.homeTeamWinProbability`
- `scoreboard.currentPlay.homeTeamWinProbabilityAdded`
- `scoreboard.currentPlay.playEvents[].defense.catcher`
- `scoreboard.linescore.defense.catcher`
- `scoreboard.probablePitchers`
- `scoreboard.stats.exitVelocity.lastEV[].hitProbability`
- `scoreboard.stats.exitVelocity.lastEV[].hitProbabilityFormatted`
- `scoreboard.stats.exitVelocity.lastEV[].launchAngle`
- `scoreboard.stats.exitVelocity.topDistance[].hitProbability`
- `scoreboard.stats.exitVelocity.topDistance[].hitProbabilityFormatted`
- `scoreboard.stats.exitVelocity.topDistance[].launchAngle`
- `scoreboard.stats.exitVelocity.top[].hitProbability`
- `scoreboard.stats.exitVelocity.top[].hitProbabilityFormatted`
- `scoreboard.stats.exitVelocity.top[].launchAngle`
- `scoreboard.stats.wpa.gameWpa[].awayTeamWinProbability`
- `scoreboard.stats.wpa.gameWpa[].homeTeamWinProbability`
- `scoreboard.stats.wpa.gameWpa[].homeTeamWinProbabilityAdded`
- `team_home[].catcher`
- `team_home[].catcher_name`
