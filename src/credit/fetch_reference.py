"""Fetch reference data: player names, Savant OAA (checks), and Savant's catcher throwing
and pitcher running-game leaderboards (used to split stolen-base attempts).

Writes reference/{players,oaa,catcher_throwing,pitcher_running}_<season>.csv (small; committed).
"""
import io
import sys
from pathlib import Path

import pandas as pd
import requests

season = sys.argv[1]
BUILD = Path(sys.argv[2] if len(sys.argv) > 2 else "data/build")
OUT = Path("reference")
OUT.mkdir(exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (full-credit-wpa research; github.com/pmathur6/full-credit-wpa)"}

ev = pd.read_parquet(BUILD / f"events_{season}.parquet",
                     columns=["batter", "pitcher"] + [f"f{i}" for i in range(2, 10)])
mv = pd.read_parquet(BUILD / f"runner_moves_{season}.parquet", columns=["runner_id"])
ids = sorted(set(pd.concat([ev[c] for c in ev.columns] + [mv.runner_id]).dropna().astype(int)))
rows = []
for i in range(0, len(ids), 150):
    chunk = ",".join(map(str, ids[i:i + 150]))
    r = requests.get(f"https://statsapi.mlb.com/api/v1/people?personIds={chunk}", headers=H, timeout=60)
    r.raise_for_status()
    rows += [{"player_id": p["id"], "name": p["fullName"],
              "primary_position": p.get("primaryPosition", {}).get("abbreviation")} for p in r.json()["people"]]
pd.DataFrame(rows).to_csv(OUT / f"players_{season}.csv", index=False)
print(f"{len(rows)} players")

url = ("https://baseballsavant.mlb.com/leaderboard/outs_above_average?type=Fielder"
       f"&startYear={season}&endYear={season}&split=no&team=&range=year&min=1&pos=&roles=&viz=hide&csv=true")
try:
    r = requests.get(url, headers=H, timeout=120)
    r.raise_for_status()
    oaa = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")))
    oaa.to_csv(OUT / f"oaa_{season}.csv", index=False)
    print(f"{len(oaa)} OAA rows")
except Exception as e:  # optional: checks and infield positioning skip without it
    print(f"OAA: FAILED {e!r}")


S = "https://baseballsavant.mlb.com/leaderboard"
for name, url in {
    "catcher_throwing": f"{S}/catcher-throwing?game_type=Regular&n=1&season_start={season}&season_end={season}"
                        "&split=no&team=&type=Cat&with_team_only=1&csv=true",
    "sprint_speed": f"{S}/sprint_speed?min_season={season}&max_season={season}&position=&team=&min=0&csv=true",
    "pitcher_running": f"{S}/pitcher-running-game?game_type=Regular&n=1&season_start={season}&season_end={season}"
                       "&split=no&team=&pitch_hand=&runner_moved=&target_base=All&prior_pk=All&with_team_only=1&csv=true",
}.items():
    try:
        r = requests.get(url, headers=H, timeout=120)
        r.raise_for_status()
        df = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")))
        if df.empty:
            raise ValueError("empty leaderboard")
    except Exception as e:  # optional: the engine falls back when a leaderboard is missing
        print(f"{name}: FAILED {e!r}")
        continue
    if name == "sprint_speed" and "player_id" not in df.columns:
        df = df.rename(columns={c: "player_id" for c in df.columns if c in ("runner_id", "entity_id")})
    df.to_csv(OUT / f"{name}_{season}.csv", index=False)
    print(f"{name}: {len(df)} rows")
