"""Coverage report for a season's raw pulls. Writes reports/data_{season}.md."""
import gzip
import json
import sys
from collections import Counter
from pathlib import Path

import pandas as pd

from common import DATA, final_games

season = sys.argv[1]
L = [f"# Data coverage: {season}", ""]
sched = {g["game_pk"] for g in final_games(season)}
L.append(f"- Final regular-season games on the schedule: **{len(sched):,}**")

# --- Savant pitches ---
p = pd.read_parquet(DATA / f"savant_pitches_{season}.parquet")
p_games = set(p["game_pk"].astype(int))
L += ["", "## Savant pitches",
      f"- Pitches: {len(p):,}; games: {len(p_games):,} "
      f"({len(p_games & sched) / len(sched):.1%} of schedule)",
      f"- Plate appearances (rows with an event): {p['events'].notna().sum():,}"]
key = ["delta_home_win_exp", "fielder_2", "fielder_9", "on_1b", "hc_x",
       "estimated_ba_using_speedangle", "if_fielding_alignment"]
bip = p["type"].eq("X")
L.append(f"- Balls in play: {bip.sum():,}; with spray coords: {p.loc[bip, 'hc_x'].notna().mean():.1%}; "
         f"with xBA: {p.loc[bip, 'estimated_ba_using_speedangle'].notna().mean():.1%}")
L.append(f"- Pitches with win-prob change: {p['delta_home_win_exp'].notna().mean():.1%}; "
         f"with all 8 fielders: {p[[f'fielder_{i}' for i in range(2, 10)]].notna().all(axis=1).mean():.1%}")
missing = sorted(sched - p_games)
if missing:
    L.append(f"- Scheduled games missing from Savant ({len(missing)}): {missing[:30]}")

# --- Game feeds ---
f_games, n_plays, play_ids, events, reasons, reviews = set(), 0, set(), Counter(), Counter(), Counter()
with gzip.open(DATA / f"feeds_{season}.jsonl.gz", "rt") as fh:
    for line in fh:
        g = json.loads(line)
        f_games.add(g["game_pk"])
        for play in g["plays"]:
            n_plays += 1
            if play.get("reviewDetails"):
                rd = play["reviewDetails"]
                reviews[(rd.get("reviewType"), rd.get("isOverturned"))] += 1
            for ev in play.get("playEvents", []):
                if ev.get("playId"):
                    play_ids.add(ev["playId"])
                if not ev.get("isPitch") and ev.get("details", {}).get("eventType"):
                    events[ev["details"]["eventType"]] += 1
            for r in play.get("runners", []):
                reasons[r.get("details", {}).get("movementReason")] += 1
L += ["", "## MLB game feeds",
      f"- Games: {len(f_games):,} ({len(f_games & sched) / len(sched):.1%} of schedule); plays: {n_plays:,}",
      f"- Games in feeds but not Savant: {len(f_games - p_games)}; in Savant but not feeds: {len(p_games - f_games)}",
      "", "Non-pitch events (top 25):", ""]
L += [f"- {k}: {v:,}" for k, v in events.most_common(25)]
L += ["", "Runner movement reasons:", ""]
L += [f"- {k}: {v:,}" for k, v in reasons.most_common()]
L += ["", "Replay reviews (type, overturned):", ""]
L += [f"- {k}: {v:,}" for k, v in reviews.most_common(15)]

# --- Outfield catch probability ---
c = pd.read_parquet(DATA / f"of_catch_prob_{season}.parquet")
joined = c["play_id"].isin(play_ids).mean() if len(c) else 0
L += ["", "## Outfield catch probability",
      f"- Plays: {len(c):,}; outfielders: {c['player_id'].nunique():,}; games: {c['game_pk'].nunique():,}",
      f"- Plays whose play_id matches a game-feed event: **{joined:.1%}**",
      f"- Catch rate actual {c['out'].mean():.3f} vs expected {c['catch_rate'].mean():.3f}",
      f"- Plays by star level: {dict(sorted(Counter(c['stars']).items()))}",
      f"- Outfield balls in play in Savant (hit_location 7-9): "
      f"{(bip & p['hit_location'].astype('Float64').between(7, 9)).sum():,}"]

Path("reports").mkdir(exist_ok=True)
Path(f"reports/data_{season}.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
