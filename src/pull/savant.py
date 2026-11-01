"""Pull every regular-season pitch for a season from Savant, one request per day.

Output: data/raw/savant_pitches_{season}.parquet
"""
import io
import sys

import pandas as pd

from common import DATA, final_games, get

URL = ("https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfGT=R%7C"
       "&game_date_gt={d}&game_date_lt={d}&type=details&player_type=pitcher"
       "&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&sort_order=desc")

season = sys.argv[1]
dates = sorted({g["date"] for g in final_games(season)})
frames, empty = [], []
for i, d in enumerate(dates, 1):
    text = get(URL.format(d=d)).text
    df = pd.read_csv(io.StringIO(text), low_memory=False) if text.strip() else pd.DataFrame()
    if df.empty:
        empty.append(d)
    else:
        frames.append(df)
    if i % 20 == 0:
        print(f"{i}/{len(dates)} days, {sum(len(f) for f in frames):,} pitches", flush=True)

out = pd.concat(frames, ignore_index=True)
# Savant mixes types within a column across days; store mixed object columns as strings
for c in out.columns:
    if out[c].dtype == object:
        out[c] = out[c].astype("string")
out.to_parquet(DATA / f"savant_pitches_{season}.parquet", index=False)
print(f"Done: {len(out):,} pitches, {out['game_pk'].nunique()} games, "
      f"{len(dates)} dates, empty dates: {empty}")
