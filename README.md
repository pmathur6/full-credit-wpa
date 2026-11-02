# full-credit-wpa

Win Probability Added that credits **every player involved in a play**, not just the batter and pitcher.

**Website: https://pmathur6.github.io/full-credit-wpa/**

Traditional WPA hands the whole swing in win probability to the batter and the pitcher. This project splits each play's swing across the batter, the runners, the pitcher, the catcher, the fielders and the team's coaching staff, using Statcast to decide the split, and sums those shares into season totals. Seasons covered: 2023–2026, updated nightly during the season.

## Credit rules

1. **Results, not expectations.** Every play is scored on what actually happened. The batting team receives the actual change in win probability and the fielding team exactly the opposite, so every play (and every game) sums to zero. Players eat their own bad luck.
2. **Statcast decides only the split.** Expected values (xBA, outfield catch probability, our infield model, typical runner advancement) divide each side's actual share among the players on that side. They never add or remove credit.
3. **Defense on a ball in play** is split in stages:
   - *Contact* → **pitcher**: start of the PA → the expected value of the ball he allowed against an average defense.
   - *Positioning* → **coaching**: how much easier or harder the fielders' starting spots made the play.
   - *Conversion* → **fielder**: out or not, given how hard the play was from where he stood.
   - *Type of out or hit* (single vs double, one out vs two) → back to the **pitcher**.
   - *Runner advancement* → the throwers who cut a runner down (assists, incl. relays), otherwise the fielder who fielded the ball. Errors stay whole with the fielder charged.
4. **Offense with runners on base**: the batter gets the value of his result at standard advancement; runners get credit or blame for advancing beyond or short of that.
5. **Events between pitches** (steals, pickoffs, wild pitches, passed balls, balks, defensive indifference) are their own plays, measured at the count when they happened.

### Worked example

May 22, 2026, Guardians at Phillies, top 1st, 1 out, bases empty. José Ramírez lines out to left fielder Brandon Marsh: 102 mph at 17°, a ball that usually falls for a hit, but Marsh started almost where it landed (99% catch probability). Philadelphia's win probability rose by .016.

| Player | Stage | Out chance | Credit |
|---|---|---|---|
| Ramírez (batter) | Actual result | | −.016 |
| Sánchez (pitcher) | Typical outfield chance at that speed/angle | 0 → ~21% | +.003 |
| Phillies coaching | Marsh's starting spot | ~21% → 99% | +.012 |
| Marsh (LF) | Made a 99% catch | 99% → 100% | +.0005 |

The defense nets +.016, matching the batter's −.016. On the site, credit under .001 wins shows as *negligible*.

### Buckets

Every player credit lands in one of four buckets; teams also get a coaching bucket.

- **Batting**: the batter's share of each plate appearance, at standard advancement.
- **Baserunning**: steals, extra bases, advancing on fly balls and wild pitches (positive); caught stealing, pickoffs, thrown out advancing, doubled off (negative). Includes the batter-runner's own trip, e.g. a single stretched into an out at second.
- **Fielding**: catches, misses, throws that cut down runners, errors, and catcher work (steals, passed balls). One number per player across all positions.
- **Pitching**: the pitcher's share of each plate appearance, plus wild pitches, balks, pickoffs and his effect on base stealers.
- **Coaching** (team): defensive positioning (outfield and infield), intentional walks (the defense's whole share), sacrifice bunt calls (batting team) and defensive indifference.

For a pitcher, *pitching + his own fielding + the defense behind him* (other fielders and coaching on his plays) always equals his traditional WPA.

### Edge cases

| Scenario | Rule |
|---|---|
| Stolen base / caught stealing | Runner takes the offense's share. Defense: league caught-stealing rate for that base, then the pitcher's and catcher's season effect (Savant pitcher running game, catcher throwing), each credited with their piece; the rest 50/50. Double steals: 50/50 |
| Wild pitch, balk, pickoff | Pitcher vs the runners |
| Passed ball | Catcher vs the runners |
| Error | The fielder charged absorbs the defensive share of what went wrong |
| Double play / force out | Conversion to the fielder; one out vs two (type of out) to the pitcher for now |
| Runner thrown out on a hit or sac fly | The throwers (assists, incl. relays) |
| Robbed home run | Fielder via catch probability |
| Ground-rule double | Runner held by the rule gets no blame |
| Dropped third strike | Strikeout as normal; reaching base is a WP/PB |
| Catcher's interference, obstruction | The offending fielder |
| Batter's / runner's interference, runner hit by batted ball | That offensive player |
| Intentional walk | Batter keeps the offense's share; the defense's share goes to coaching |
| Sacrifice bunt | The bunt call (vs a normal PA) goes to the batting team's coaching |
| Extra-innings automatic runner | No credit for being placed |
| Walk-off | Win probability is capped at 1, so extra runs are worth 0 |
| Mid-play substitutions | Whoever was on the field for that event |

### Known limitations

- Infield line drives and popups have no public catch probability, so the pitcher keeps the play; the fielder who caught it is recorded with zero credit.
- Turning a double play is credited to the pitcher (type of out) until a pivot/relay model exists.
- Outfield catch probability is measured from where the fielder started: his jump and route are his, his starting spot is coaching, even when he positioned himself.
- Win-weighted numbers are noisy (see `reports/reliability.md`); the runs view is better for judging skill.

## Wins vs runs

Every credit is computed twice:

- **Wins**: MLB's win-probability model (Savant `home_win_exp`), rebuilt as a lookup by inning, half, outs, bases, count and score. Rare lopsided states missing from a season's table (e.g. down 5 in the 12th) are interpolated across score margins in log-odds.
- **Runs (context-neutral)**: run expectancy by outs, bases and count (innings 1–8 of the same season) plus runs scored. Score and inning don't matter. Each half-inning is valued on its own (three outs = 0). The traditional comparison is RE24.

### WAR scale

An optional leaderboard column (and player-page tile) puts the runs view on WAR's footing, computed in `src/site/export.py`: each bucket re-centered on the league average (offense per PA, pitching per batter faced, fielding per defensive PA), plus replacement level (1,000 WAR a season: 570 to hitters per PA, 430 to pitchers per batter faced), plus FanGraphs positional adjustments pro-rated by defensive PAs (DH by PAs in games without fielding) with a league adjustment, divided by runs per win (9 × league runs per inning × 1.5 + 3). No park adjustment; one replacement level for starters and relievers; coaching excluded.

## Website

Plain HTML/JS (no build step) in `site/`, published to GitHub Pages by the `site` workflow together with each season's exported data.

- **Leaderboard** (`index.html`): hitters and pitchers on one board or separately (Hitters total = batting + baserunning + fielding; Pitchers total = pitching + fielding), plus team coaching. Wins or runs; season, team, position (OF = LF/CF/RF), minimum PA/BF, accent-insensitive search, clear and reset buttons, optional WAR-scale column; sortable columns; every view is a shareable URL. Players with 10+ games; positions with 10+ appearances, most games first, plus DH for 10+ games batting without fielding.
- **Player page** (`player.html?id=&season=`): summary tiles with ranks, cumulative chart (tap a game), fielding by position, game log (best / worst / recent / all) where each game expands to every play he was part of and his share. Pitchers also see the defense behind him per play. Two-way players switch between hitting and pitching.
- **Game page** (`game.html?id=&season=`): team bucket totals and top/bottom players, win-probability (or expected-run) chart, the split of any play across every player with the two-team cancellation check, collapsible play-by-play by half-inning.
- **Games index** (`games.html`): every game by date; filter by team, month, extra innings, one-run games.
- **How it works** (`about.html`): the rules and examples in plain English.

## Data sources

- **Savant pitch-level search**: game state, all fielders and alignment, batted balls, xBA, MLB win probability.
- **MLB Stats API game feed**: runner movements with putout/assist/error credits, events between pitches, replay reviews; schedule (game dates).
- **Savant `player-services/range`**: per-play outfield catch probability from the fielder's actual starting spot.
- **Savant leaderboards** (in `reference/`): Outs Above Average, catcher throwing, pitcher running game, sprint speed, fielding and baserunning run value, player names.
- **Infield**: no public per-play success probability, so we build our own (`src/model/infield.py`) and calibrate it to Savant's infield OAA.

## Pipeline

### Play table (`src/build/plays.py`)

`events_<season>.parquet`, one row per win-probability-changing event:

- `kind = pa`: every plate appearance, with the batted ball, outfield catch probability, and the state at the start, at the result and after.
- `kind = mid`: every event between pitches that moves a runner.

Bases, outs and score are tracked independently from the MLB feed (pinch runners, automatic runners and multi-runner plays handled) and match Savant at the first pitch of 100% of PAs. A `mid` event is measured at the count when it happened; a `pa` row keeps the rest of that PA (including count changes), so each game's changes sum exactly to the final result; each half-inning's run values likewise sum exactly. Also writes `runner_moves_<season>.parquet` (every runner movement with fielding credits), `we_lookup_<season>.parquet` and `re_lookup_<season>.parquet`.

### Credit engine (`src/credit/engine.py`)

Splits every event's change by the rules above: `engine.py <season> data/build data/credit` (wins) and `... runs` (runs). Outfield positioning compares Savant catch probability with the average catch probability for balls hit like it among outfield chances. Infield ground balls use the infield model (exit velocity, launch angle, spray, batter hand, sprint speed, base/out state; with and without the alignment, whose difference is positioning). Each infielder's season gap to Savant OAA is treated as positioning and moved to his team's coaching. Infield hits are shared across infielders by how often each makes the play at that spray angle.

Outputs `credits_<season>.parquet` and `credits_runs_<season>.parquet`: one row per (event, player or team coaching, bucket, role).

### Checks and reports

| Report | What it shows |
|---|---|
| `reports/data_<season>.md` | Raw pull coverage |
| `reports/build_report_<season>.md` | State tracking vs Savant, game and half-inning tie-outs, win-probability fallbacks |
| `reports/infield_model_<season>.md` | Infield model fit (AUC, calibration) |
| `reports/credit_report_<season>.md` | Accounting identities (every play and team ties out), outfield/infield vs Savant OAA, catcher/pitcher steal effects vs Savant, leaderboards |
| `reports/credit_report_runs_<season>.md` | Same identities and leaderboards for the runs version |
| `reports/audit_<season>.md` | Plain-English sample of unusual plays and who got what |
| `reports/external_checks_<season>.md` | Correlations with traditional WPA and Savant run values |
| `reports/site_export_<season>.md` | Site data checked against the credit outputs |
| `reports/reliability.md` | Split-half, year-to-year and stabilization by bucket |

Player and team tables: `output/players_<season>.csv`, `output/players_runs_<season>.csv`, `output/coaching_<season>.csv`, `output/coaching_runs_<season>.csv`.

### Repository layout

```
src/pull/      raw pulls (Savant pitches, MLB feeds, catch probability) + coverage report
src/build/     win-probability / run-expectancy lookups and the play table
src/model/     infield conversion model
src/credit/    reference fetches, credit engine, reports, external checks
src/site/      site JSON export and its check
src/analysis/  reliability
site/          the website (HTML, CSS, JS)
reports/ output/ reference/   committed results
```

Large data lives in GitHub releases named `data-<season>` (raw pulls, play tables, credits, and `site_<season>.tar.gz`), not in git.

## How it runs

Everything runs as GitHub Actions; nothing runs locally.

| Workflow | What it does |
|---|---|
| `nightly` | March–October, every morning (~10:17 UTC): pulls new games for the current season (incremental), rebuilds, re-credits, re-exports and republishes the site. Skips if the season hasn't started. Can be run by hand for any season. |
| `pipeline` | A whole season end to end: pull, build, credit, external checks, site export. Use it to add a season; tick *skip pull* to rebuild from the data already pulled. |
| `pull-season` | Pulls Savant pitches, MLB game feeds and outfield catch probability into the `data-<season>` release; *update* keeps what's there and pulls only new games plus the last 3 days |
| `build-season` | Builds the play table and lookups, commits `reports/build_report_<season>.md` |
| `credit-season` | Fetches reference data, fits the infield model, runs the engine in wins and runs, commits reports and `output/` |
| `external-checks` | Correlations with traditional WPA and Savant run values |
| `export-season` | Writes the site JSON (leaderboard, one file per player and per game, wins and runs), checks it, uploads `site_<season>.tar.gz`, triggers `site` |
| `site` | Publishes the website to GitHub Pages from `site/` plus every season's exported data. Runs on changes to `site/` and after each export. |
| `reliability` | Signal-vs-noise report across all seasons |
| `probe`, `probe-fielding`, `probe-steals` | One-off data-field probes |

To add a past season: run `pipeline` with the season. A new season is picked up by `nightly` automatically once games are final.

## Status

- [x] Credit rules agreed
- [x] Data pull pipeline and play table (100% state match, all games tie out)
- [x] Credit engine with outfield catch probability, infield model, staged steals, coaching bucket
- [x] Seasons 2023–2026
- [x] Runs (context-neutral) version
- [x] Checks vs Savant and traditional WPA; reliability
- [x] Website: leaderboard, player pages, game pages, games index, how it works
- [x] Nightly in-season updates
- [ ] Double-play turning model
- [ ] Infield line drive / popup catch model
- [ ] Outs above expected on the player page
