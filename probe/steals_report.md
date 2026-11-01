# Steal-timing probe (2025)

## catcher-throwing (player=)
- URL: `https://baseballsavant.mlb.com/player-services/catcher-throwing?player=672275&season=2025`
- Status 200, text/html; charset=utf-8, 96,550 chars
- Matching JSON keys in page: []
- Endpoints referenced: ['/leaderboard/catcher-throwing']
  - `catcher_throwing` context: `<h2><span><a href=#catcher_throwing name="catcher_throwing">Statcast Catcher Throwing</a></span> </h2> <div class="divider"></div> <div     id="table-catcher-throwing"     class="table-savant"     style="position: relative; overflow-y: hidden !important" >     <table i`

## catcher-throwing (player=, year=)
- URL: `https://baseballsavant.mlb.com/player-services/catcher-throwing?player=672275&year=2025`
- Status 200, text/html; charset=utf-8, 96,550 chars
- Matching JSON keys in page: []
- Endpoints referenced: ['/leaderboard/catcher-throwing']
  - `catcher_throwing` context: `<h2><span><a href=#catcher_throwing name="catcher_throwing">Statcast Catcher Throwing</a></span> </h2> <div class="divider"></div> <div     id="table-catcher-throwing"     class="table-savant"     style="position: relative; overflow-y: hidden !important" >     <table i`

## catcher-throwing (player=, no season)
- URL: `https://baseballsavant.mlb.com/player-services/catcher-throwing?player=672275`
- Status 200, text/html; charset=utf-8, 96,550 chars
- Matching JSON keys in page: []
- Endpoints referenced: ['/leaderboard/catcher-throwing']
  - `catcher_throwing` context: `<h2><span><a href=#catcher_throwing name="catcher_throwing">Statcast Catcher Throwing</a></span> </h2> <div class="divider"></div> <div     id="table-catcher-throwing"     class="table-savant"     style="position: relative; overflow-y: hidden !important" >     <table i`

## pitcher running game leaderboard
- URL: `https://baseballsavant.mlb.com/leaderboard/pitcher-running-game?game_type=Regular&n=1&season_start=2025&season_end=2025&split=no&team=&pitch_hand=&runner_moved=&target_base=All&prior_pk=All&with_team_only=1&csv=true`
- Status 200, text/csv; charset=utf-8, 191,589 chars
- CSV rows: 869
- Header: `﻿"player_id","player_name","team_name","start_year","end_year","key_target_base","runs_prevented_on_running_attr","n_pitcher_cs_aa","n_init","rate_sbx","n_sb","n_cs","n_pk","n_bk","n_fb","n_plus","n_minus","net_attr_plus","net_attr_minus","r_primary_lead","r_secondary_lead","r_sec_minus_prim_lead","r_primary_lead_sbx","r_secondary_lead_sbx","r_sec_minus_prim_lead_sbx"`
- First row: `690990,"Horton, Cade","CHC",2025,2025,"All",1.0421637996528075,0.7285414042941517,635,0.02047244094488189,8,5,2,0,0,8,7,-2.7177163034316005,3.5237934674202895,"11.661825424","15.674788136","4.012962712","12.058","22.581769231","10.523769231"`

## pitcher running game page
- URL: `https://baseballsavant.mlb.com/leaderboard/pitcher-running-game`
- Status 200, text/html; charset=utf-8, 550,782 chars
- Matching JSON keys in page: ['n_pitcher_cs_aa', 'r_primary_lead', 'r_primary_lead_sbx', 'r_sec_minus_prim_lead', 'r_sec_minus_prim_lead_sbx', 'r_secondary_lead', 'r_secondary_lead_sbx']
- Endpoints referenced: ['/leaderboard/abs-challenges', '/leaderboard/active-spin', '/leaderboard/arm-strength', '/leaderboard/baserunning', '/leaderboard/baserunning-run-value', '/leaderboard/basestealing-run-value', '/leaderboard/bat-tracking', '/leaderboard/bat-tracking/swing-path-attack-angle', '/leaderboard/bat-tracking/swing-timing-miss-distance', '/leaderboard/batted-ball', '/leaderboard/catch_probability', '/leaderboard/catcher-blocking', '/leaderboard/catcher-framing', '/leaderboard/catcher-stance', '/leaderboard/catcher-throwing', '/leaderboard/custom', '/leaderboard/expected_statistics', '/leaderboard/fielding-run-value', '/leaderboard/first-base-scoops-receiving', '/leaderboard/home-runs', '/leaderboard/hot-stove', '/leaderboard/outfield_directional_outs_above_average', '/leaderboard/outfield_jump', '/leaderboard/outs_above_average', '/leaderboard/percentile-rankings', '/leaderboard/pitch-arsenal-stats', '/leaderboard/pitch-arsenals', '/leaderboard/pitch-movement', '/leaderboard/pitch-tempo', '/leaderboard/pitch-timer-infractions', '/leaderboard/pitcher-arm-angles', '/leaderboard/pitcher-running-game', '/leaderboard/poptime', '/leaderboard/rolling', '/leaderboard/rolling#pitching-rolling', '/leaderboard/running_splits', '/leaderboard/spin-direction-pitches', '/leaderboard/sprint_speed', '/leaderboard/statcast', '/leaderboard/statcast-park-factors', '/leaderboard/statcast-year-to-year', '/leaderboard/swing-take', '/leaderboard/top-performers', '/leaderboard/weighted-score']
  - `running_game` context: `gin-bottom: 0.25rem;   }    #leaderboard .dropdown {     margin-bottom: 0.25rem;   }    #leaderboard .dropdown {     font-size: 14px;   }    #pitcher_running_game .th-tooltip {     color: #666;     max-width: 180px;     white-space: normal;   }    /* Hack */   .tr-data {     height: 31px;   }    :root {     --catcher-throw-legend-size: 300px;     --catcher-throw-search-size: 370px;     --catcher-t`
  - `poptime` context: `                                 </li>                                         <li>                                             <a href="/leaderboard/poptime">                                                 Catcher Pop Time                                             </a>                                         </li>                                         <li>                                    `
  - `basestealing` context: ` <li class="leaderboard-sub-level">                                             <a                                                 href="/leaderboard/basestealing-run-value"                                             >                                             ▸ Basestealing Run Value                                             </a>                                         </li>                 `
  - `throws` context: `* Hack */   .tr-data {     height: 31px;   }    :root {     --catcher-throw-legend-size: 300px;     --catcher-throw-search-size: 370px;     --catcher-throws-menu-padding: 10px;     --table-margin: 2rem;   }    </style>   <script>   const data = [{"entity_name":"Pintaro, Jonathan","entity_id":702752,"start_year":2026,"end_year":2026,"key_target_base":"All","pitch_hand":"R","key_pitch_hand":"All","r`

## basestealing run value (type=Pitcher)
- URL: `https://baseballsavant.mlb.com/leaderboard/basestealing-run-value?game_type=Regular&n=1&target_base=All&split=no&team=&type=Pitcher&with_team_only=1&season_start=2025&season_end=2025&csv=true`
- Status 200, text/csv; charset=utf-8, 134,611 chars
- CSV rows: 655
- Header: `﻿"player_id","player_name","team_name","start_year","end_year","key_target_base","runs_stolen_on_running_act","n_init","rate_sbx","n_sb","n_cs","n_pk","n_bk","n_fb","n_plus","n_minus","net_act_plus","net_act_minus","r_primary_lead","r_secondary_lead","r_sec_minus_prim_lead","r_primary_lead_sbx","r_secondary_lead_sbx","r_sec_minus_prim_lead_sbx"`
- First row: `681807,"Fry, David","CLE",2025,2025,"All",-0.39853216186827617,105,0,0,0,1,1,0,1,1,-0.38987015461138336,-0.7123514021022211,"11.263446602","14.694514563","3.431067961",,,`

## basestealing run value (type=Catcher)
- URL: `https://baseballsavant.mlb.com/leaderboard/basestealing-run-value?game_type=Regular&n=1&target_base=All&split=no&team=&type=Catcher&with_team_only=1&season_start=2025&season_end=2025&csv=true`
- Status 200, text/csv; charset=utf-8, 134,611 chars
- CSV rows: 655
- Header: `﻿"player_id","player_name","team_name","start_year","end_year","key_target_base","runs_stolen_on_running_act","n_init","rate_sbx","n_sb","n_cs","n_pk","n_bk","n_fb","n_plus","n_minus","net_act_plus","net_act_minus","r_primary_lead","r_secondary_lead","r_sec_minus_prim_lead","r_primary_lead_sbx","r_secondary_lead_sbx","r_sec_minus_prim_lead_sbx"`
- First row: `681807,"Fry, David","CLE",2025,2025,"All",-0.39853216186827617,105,0,0,0,1,1,0,1,1,-0.38987015461138336,-0.7123514021022211,"11.263446602","14.694514563","3.431067961",,,`

## catcher throwing leaderboard page
- URL: `https://baseballsavant.mlb.com/leaderboard/catcher-throwing`
- Status 200, text/html; charset=utf-8, 1,745,003 chars
- Matching JSON keys in page: ['arm_strength', 'cs_raa', 'exchange_time', 'generic_time_to_target', 'n_cs_aa', 'n_xcs_with_accuracy', 'n_xcs_with_accuracy_over_xcs', 'n_xcs_with_exchange_over_xcs', 'n_xcs_with_flight_over_xcs', 'n_xcs_with_ground_other_over_xcs', 'n_xcs_with_onfly_other_over_xcs', 'n_xcs_with_other_over_xcs', 'n_xcs_with_untracked_other_over_xcs', 'n_xcs_without_catchrel', 'n_xcs_without_flight', 'pop', 'pop_time', 'rate_cs_aa', 'rate_cs_raa', 'rate_throw_tracked', 'rate_xcs_with_accuracy', 'rate_xcs_with_accuracy_over_xcs', 'rate_xcs_with_exchange_over_xcs', 'rate_xcs_with_flight_over_xcs', 'rate_xcs_with_ground_other_over_xcs', 'rate_xcs_with_onfly_other_over_xcs', 'rate_xcs_with_other_over_xcs', 'rate_xcs_with_untracked_other_over_xcs', 'rate_xcs_without_catchrel', 'rate_xcs_without_flight', 'time_to_target']
- Endpoints referenced: ['/leaderboard/abs-challenges', '/leaderboard/active-spin', '/leaderboard/arm-strength', '/leaderboard/baserunning', '/leaderboard/baserunning-run-value', '/leaderboard/basestealing-run-value', '/leaderboard/bat-tracking', '/leaderboard/bat-tracking/swing-path-attack-angle', '/leaderboard/bat-tracking/swing-timing-miss-distance', '/leaderboard/batted-ball', '/leaderboard/catch_probability', '/leaderboard/catcher-blocking', '/leaderboard/catcher-framing', '/leaderboard/catcher-stance', '/leaderboard/catcher-throwing', '/leaderboard/custom', '/leaderboard/expected_statistics', '/leaderboard/fielding-run-value', '/leaderboard/first-base-scoops-receiving', '/leaderboard/home-runs', '/leaderboard/hot-stove', '/leaderboard/outfield_directional_outs_above_average', '/leaderboard/outfield_jump', '/leaderboard/outs_above_average', '/leaderboard/percentile-rankings', '/leaderboard/pitch-arsenal-stats', '/leaderboard/pitch-arsenals', '/leaderboard/pitch-movement', '/leaderboard/pitch-tempo', '/leaderboard/pitch-timer-infractions', '/leaderboard/pitcher-arm-angles', '/leaderboard/pitcher-running-game', '/leaderboard/poptime', '/leaderboard/rolling', '/leaderboard/rolling#pitching-rolling', '/leaderboard/running_splits', '/leaderboard/spin-direction-pitches', '/leaderboard/sprint_speed', '/leaderboard/statcast', '/leaderboard/statcast-park-factors', '/leaderboard/statcast-year-to-year', '/leaderboard/swing-take', '/leaderboard/top-performers', '/leaderboard/weighted-score']
  - `running_game` context: `="pitch_movement">Pitch Movement</option>                   <option value="pitch_tempo">Pitch Tempo</option>                   <option value="pitcher_running_game">Running Game</option>                   <option value="pitching_run_value">Run Value</option>                   <option value="spin_direction_compare">Spin Direction - Comparison</option>                   <option value="spin_direction_`
  - `catcher_throwing` context: `     margin-bottom: 0.25rem;   }    #leaderboard .dropdown {     margin-bottom: 0.25rem;   }    #leaderboard .dropdown {     font-size: 14px;   }    #catcher_throwing_table .th-tooltip {     color: #666;     max-width: 180px;     white-space: normal;   }    /* Hack */   .tr-data {     height: 31px;   }    :root {     --catcher-throw-legend-size: 300px;     --catcher-throw-search-size: 370px;     -`
  - `poptime` context: `                                 </li>                                         <li>                                             <a href="/leaderboard/poptime">                                                 Catcher Pop Time                                             </a>                                         </li>                                         <li>                                    `
  - `basestealing` context: ` <li class="leaderboard-sub-level">                                             <a                                                 href="/leaderboard/basestealing-run-value"                                             >                                             ▸ Basestealing Run Value                                             </a>                                         </li>                 `
  - `throws` context: `* Hack */   .tr-data {     height: 31px;   }    :root {     --catcher-throw-legend-size: 300px;     --catcher-throw-search-size: 370px;     --catcher-throws-menu-padding: 10px;     --table-margin: 2rem;   }    </style>   <script>   const data = [{"entity_choice":"C","entity_code":"Cat","entity_id":543510,"entity_name":"McCann, James","key_game_type":"Regular","key_target_base":"All","timeframe":20`

