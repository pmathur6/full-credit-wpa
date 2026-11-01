"""Fetch outside metrics to compare against: FanGraphs (WPA, BsR, fielding, batting runs)
and Savant (baserunning run value, fielding run value).

Writes reference/{fg_bat,fg_pit,savant_brv,savant_frv}_<season>.csv plus
reference/external_status_<season>.txt (which sources worked). Each source is optional.
"""
import io
import sys
from pathlib import Path

import pandas as pd
import requests

season = sys.argv[1]
OUT = Path("reference")
OUT.mkdir(exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0 Safari/537.36 (full-credit-wpa research)",
     "Accept": "application/json, text/csv, */*"}
status = []


def fg(stats):
    url = ("https://www.fangraphs.com/api/leaders/major-league/data"
           f"?age=&pos=all&stats={stats}&lg=all&qual=0&season={season}&season1={season}"
           "&startdate=&enddate=&month=0&hand=&team=0&pageitems=2000000&pagenum=1&ind=0&rost=0&players=&type=8")
    r = requests.get(url, headers=H, timeout=120)
    r.raise_for_status()
    df = pd.DataFrame(r.json()["data"])
    return df.drop(columns=[c for c in df.columns if df[c].astype(str).str.contains("<a ", regex=False).any()])


def savant(url):
    r = requests.get(url, headers=H, timeout=120)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")))


S = "https://baseballsavant.mlb.com/leaderboard"
sources = {
    "fg_bat": lambda: fg("bat"),
    "fg_pit": lambda: fg("pit"),
    "savant_brv": lambda: savant(f"{S}/baserunning-run-value?game_type=Regular&season_start={season}&season_end={season}"
                                 "&sortColumn=runner_runs_tot&sortDirection=desc&split=no&n=0&team=&type=Run&with_team_only=1&csv=true"),
    "savant_frv": lambda: savant(f"{S}/fielding-run-value?gameType=Regular&seasonStart={season}&seasonEnd={season}"
                                 "&type=fielder&position=&minInnings=0&minResults=1&csv=true"),
}
for name, fn in sources.items():
    try:
        df = fn()
        df.to_csv(OUT / f"{name}_{season}.csv", index=False)
        status.append(f"{name}: ok, {len(df)} rows, columns: {', '.join(map(str, df.columns[:60]))}")
    except Exception as e:
        status.append(f"{name}: FAILED {e!r}"[:400])
(OUT / f"external_status_{season}.txt").write_text("\n".join(status) + "\n")
print("\n".join(status))
