# full-credit-wpa

Win Probability Added that credits **every player involved in a play**, not just the batter and pitcher.

Traditional WPA hands the whole swing in win probability to the batter and the pitcher. This project splits each play's swing across the batter, baserunners, pitcher, catcher and fielders, using Statcast to decide the split, and sums those shares into season totals.

## Credit rules

1. **Results, not expectations.** Every play is scored on what actually happened. The offense receives the actual change in win probability and the defense receives exactly the opposite, so every play (and every game) sums to zero. Players eat their own bad luck.
2. **Statcast decides only the split.** Expected values (xBA, catch probability, expected runner advancement) are used to divide each side's actual share among the players on that side. They never add or remove credit.
3. **Defense on a ball in play** splits in two stages:
   - *Contact* (pitcher): start-of-PA win probability → expected win probability given the batted ball.
   - *Conversion* (fielders): expected → actual. A fielder who makes a play gets (1 − catch probability) × the value of the out; a missed play costs catch probability × that value.
4. **Offense with runners on base**: the batter gets the value of his hit at standard advancement; runners get credit or blame for advancing beyond or short of that.
5. **Non-PA events** (steals, pickoffs, wild pitches, passed balls, balks) are their own plays.

### Worked example

Bottom 7th, tie, 1 out, bases empty (win probability .560). Line drive, .700 xBA, shortstop makes a diving catch (.535 after the out; a single would have been .600).

| Player | Credit | Why |
|---|---|---|
| Batter | −.025 | Actual result: .560 → .535 |
| Pitcher | −.0205 | Allowed contact worth .5805 (.700 × .600 + .300 × .535) |
| Shortstop | +.0455 | .70 × (.600 − .535): converted a ball caught 30% of the time |

Defense nets +.025, matching the batter's −.025.

### Buckets

Every credit lands in one of four buckets:

- **Batting**: the batter's share of each plate appearance, at standard advancement.
- **Baserunning**: what a player does as a runner — steals, extra bases, advancing on fly balls and wild pitches (positive); caught stealing, pickoffs, thrown out advancing, doubled off (negative). Includes the batter-runner's own trip, e.g. a single stretched into an out at second.
- **Fielding**: catches, misses, throws that cut down runners, and catcher work (SB defense, passed balls).
- **Pitching**: the pitcher's share of each plate appearance, plus wild pitches, balks and pickoffs.

### Edge cases

| Scenario | Rule |
|---|---|
| SB / CS | Runner takes the offense's share; defense splits catcher vs pitcher (50/50 until timing data is available) |
| WP / PB, pickoff, balk | Pitcher or catcher vs runners |
| Error | Charged fielder absorbs actual minus expected |
| Double play / fielder's choice | Fielders credited for turning it beyond the expected DP chance |
| Robbed HR | Fielder via catch probability |
| Ground-rule double | Runner held by the rule gets no blame |
| Dropped third strike | Strikeout as normal; reaching base is a WP/PB |
| Catcher's interference, obstruction | The offending fielder |
| Batter's / runner's interference, runner hit by batted ball | That offensive player |
| Pitch-clock violation | Whoever committed it |
| Intentional walk | Manager bucket |
| Extra-innings automatic runner | No credit for being placed |
| Walk-off | Win probability is capped at 1, so extra runs are worth 0 |
| Mid-play substitutions | Whoever was on the field for that event |

## Website

**https://pmathur6.github.io/full-credit-wpa/** — plain HTML/JS in `site/`, published by the `site` workflow (GitHub Pages) with each season's exported data.

- **Leaderboard**: hitters and pitchers on one board (or separately), team coaching; wins or runs; season, team, position, minimum PA/BF, search; sortable, shareable URLs.
- **Player page**: summary tiles, cumulative chart, fielding by position, game log where each game expands to every play he was part of and his share (pitchers: the defense behind him). Two-way players switch between hitting and pitching.
- **Game page**: team totals, win-probability chart, the split of any play across every player, collapsible play-by-play.
- **Games index** and a plain-English **How it works** page.

## Data sources

- **Savant pitch-level search**: game state, all fielders, batted balls, xBA, MLB win-probability change per pitch.
- **MLB Stats API game feed**: runner movements with putout/assist/error credits, non-pitch events, replay reviews.
- **Savant `player-services/range`**: per-play outfield catch probability (from the fielder's actual starting spot).
- **Infield**: no public per-play success probability, so we build our own and check it against Savant's infield OAA totals.

## Play table

`events_<season>.parquet` has one row per win-probability-changing event:

- `kind = pa`: every plate appearance, with the batted ball and outfield catch probability.
- `kind = mid`: every event between pitches that moves a runner (steals, caught stealing, wild pitches, passed balls, pickoffs, balks, errors).

Win probability is MLB's own model, which is a fixed function of inning, half, outs, bases, count and score; we rebuild it as a lookup so states between pitches have values too. A `mid` event is measured at the count when it happened; a `pa` row keeps everything else in that plate appearance (including count changes), so each game's changes sum exactly to the final result. Savant's own per-pitch changes drop some between-pitch events and add up correctly in only ~73% of games.

`runner_moves_<season>.parquet` has one row per runner movement with the putout/assist/error credits.

## Credit engine (v1)

`src/credit/engine.py` splits every event's change in win probability. Offense: the batter gets the value of his result at standard advancement; runners get advancement beyond (or short of) that. Defense on a ball in play: the pitcher gets the contact (league-average defense), coaching gets positioning (outfield: Savant catch probability vs the average catch probability for balls hit like it), and the responsible fielder gets the conversion; runners cut down by throws go to the fielders on those outs.

Infield ground balls use our own model (`src/model/infield.py`, report in `reports/infield_model_<season>.md`): the probability an average infield converts the ball, from exit velocity, launch angle, spray angle, batter handedness and sprint speed, and the base/out state; fitted with and without the infield alignment, whose difference is infield positioning credit. Errors count as failed conversions. Outs go to the infielder who made the play; a hit is shared by the infielders in proportion to how often each makes the play at that spray angle. Because the model only knows the alignment type, each infielder's season gap to his Savant OAA (which judges him from where he actually stood) is treated as positioning and moved to his team's coaching, spread over his chances by each play's value.

Stolen-base attempts: baseline league caught-stealing rate, then the pitcher's and the catcher's season effect (Savant pitcher running game and catcher throwing), each credited with their piece; the rest splits 50/50.

Still simplified: air balls with no tracked catch chance (infield liners and popups, outfield hits Savant doesn't count as chances) stay with the pitcher. The fielder who handled the ball is still recorded, with zero credit.

Win probability for rare lopsided states missing from the season's table (e.g. down 5 in the 12th) is interpolated across score margins for the same inning, outs, bases and count, in log-odds.

### Runs version (context-neutral)

The same engine, run with `engine.py <season> data/build data/credit runs`, values every state by run expectancy instead of win probability: expected runs for the rest of the half-inning by outs, bases and count (innings 1-8 of the same season, `re_lookup_<season>.parquet`), plus runs already scored. Score and inning don't matter, so a play is worth the same in a blowout as in a tie game. Each half-inning is valued on its own (three outs = 0 expected runs). Output `credits_runs_<season>.parquet`; checks in `reports/credit_report_runs_<season>.md`; player table `output/players_runs_<season>.csv`.

## How it runs

Everything runs as GitHub Actions; nothing runs locally.

| Workflow | What it does |
|---|---|
| `reliability` | Signal-vs-noise report across all seasons (`reports/reliability.md`) |
| `nightly` | During the season (March–October), every morning: pulls new games for the current season (update mode), rebuilds, re-credits, re-exports and republishes the site. Can also be run by hand for any season. |
| `site` | Publishes the website to GitHub Pages from `site/` and every season's exported data. Runs on changes to `site/` and after each export. |
| `pipeline` | Runs a whole season end to end (pull, build, credit, external checks, site export). Use this to add a season; tick *skip pull* to rebuild from the data already pulled. |
| `probe` | Pulls one day of Savant pitch data and MLB game feeds and writes a field-coverage report to `probe/` |
| `probe-fielding` | Checks Savant for per-play catch probability for one player |
| `build-season` | Builds the master play tables (`events`, `runner_moves`, `we_lookup`) from a season's raw pulls into the same release and commits `reports/build_report_<season>.md` |
| `export-season` | Writes the site's JSON (leaderboard, one file per player and per game, wins and runs) with `src/site/export.py`, checks it against the credit outputs (`reports/site_export_<season>.md`) and uploads `site_<season>.tar.gz` to the release |
| `credit-season` | Runs the credit engine, fetches names and Savant OAA, and commits `reports/credit_report_<season>.md`, `reports/audit_<season>.md` and `output/` (player and coaching tables) |
| `pull-season` | Pulls a full season (Savant pitches, MLB game feeds, outfield catch probability) into the `data-<season>` release and commits `reports/data_<season>.md` |

## Status

- [x] Credit rules agreed
- [x] Confirm data fields (probe)
- [x] Data pull pipeline (2025)
- [x] Master play table (2025)
- [ ] Infield success-probability model
- [x] Credit engine v1 (2025; infield uses 1 - xBA as a stand-in)
- [x] Infield model (ground balls)
- [x] Seasons 2023-2026
- [x] Correlation checks vs Savant (FanGraphs blocks automated access)
- [x] Split-half and year-to-year reliability
- [ ] Site
