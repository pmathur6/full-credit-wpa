"""Pull Savant's per-play outfield catch probability for every outfielder in a season.

Outfielders = anyone who appears as fielder_7/8/9 in the season's pitch data.
Output: data/raw/of_catch_prob_{season}.parquet
"""
import sys

import pandas as pd

from common import DATA, get

URL = ("https://baseballsavant.mlb.com/player-services/range"
       "?playerId={pid}&season={season}&playerType=fielder")

season = sys.argv[1]
pitches = pd.read_parquet(DATA / f"savant_pitches_{season}.parquet",
                          columns=["fielder_7", "fielder_8", "fielder_9"])
ids = sorted(set(pd.concat([pitches[c] for c in pitches.columns]).dropna().astype(int)))
print(f"{len(ids)} outfielders", flush=True)

rows, failed = [], []
for i, pid in enumerate(ids, 1):
    try:
        rows += get(URL.format(pid=pid, season=season)).json()
    except Exception as e:
        failed.append((pid, repr(e)))
    if i % 50 == 0:
        print(f"{i}/{len(ids)}, {len(rows):,} plays", flush=True)

df = pd.DataFrame(rows)
for c in ["distance", "opportunity_time", "catch_rate", "sprint_speed"]:
    if c in df:
        df[c] = pd.to_numeric(df[c], errors="coerce")
df.to_parquet(DATA / f"of_catch_prob_{season}.parquet", index=False)
print(f"Done: {len(df):,} plays from {df['player_id'].nunique() if len(df) else 0} players; "
      f"failed: {failed}")
