"""Pull every regular-season pitch for a season from Savant, one request per day.

Usage: python savant.py <season> [--update]
--update keeps an existing file and only pulls days with games it doesn't have yet,
plus the last 3 days (late corrections).
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
update = "--update" in sys.argv
path = DATA / f"savant_pitches_{season}.parquet"
games = final_games(season)
dates = sorted({g["date"] for g in games})
frames, empty = [], []
if update and path.exists():
    old = pd.read_parquet(path)
    have = set(pd.to_numeric(old["game_pk"]).astype(int))
    redo = sorted({g["date"] for g in games if g["game_pk"] not in have} | set(dates[-3:]))
    frames.append(old[~old["game_date"].astype(str).str[:10].isin(redo)])
    print(f"update: keeping {len(frames[0]):,} pitches, pulling {len(redo)} days: {redo}", flush=True)
    dates = redo
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
out.to_parquet(path, index=False)
print(f"Done: {len(out):,} pitches, {out['game_pk'].nunique()} games, "
      f"{len(dates)} dates, empty dates: {empty}")
