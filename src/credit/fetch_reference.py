"""Fetch reference data for the credit checks: player names and Savant OAA.

Writes reference/players_<season>.csv and reference/oaa_<season>.csv (small; committed).
"""
import io
import sys
from pathlib import Path

import pandas as pd
import requests

season = sys.argv[1]
credits = Path(sys.argv[2] if len(sys.argv) > 2 else "data/credit") / f"credits_{season}.parquet"
OUT = Path("reference")
OUT.mkdir(exist_ok=True)
H = {"User-Agent": "Mozilla/5.0 (full-credit-wpa research; github.com/pmathur6/full-credit-wpa)"}

ids = sorted(pd.read_parquet(credits, columns=["player_id"])["player_id"].dropna().astype(int).unique())
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
r = requests.get(url, headers=H, timeout=120)
r.raise_for_status()
oaa = pd.read_csv(io.StringIO(r.content.decode("utf-8-sig")))
oaa.to_csv(OUT / f"oaa_{season}.csv", index=False)
print(f"{len(oaa)} OAA rows")
