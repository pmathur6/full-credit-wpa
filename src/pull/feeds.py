"""Pull the MLB Stats API live feed for every final regular-season game.

Keeps only liveData.plays (all plays, runners, credits, play events, reviews) plus
game info and boxscore positions, gzipped as one JSON line per game.
Output: data/raw/feeds_{season}.jsonl.gz
"""
import gzip
import json
import sys
from concurrent.futures import ThreadPoolExecutor

from common import DATA, final_games, get

URL = "https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live"


def fetch(pk):
    feed = get(URL.format(pk=pk)).json()
    box = feed["liveData"].get("boxscore", {}).get("teams", {})
    return {
        "game_pk": pk,
        "game": feed["gameData"].get("game"),
        "datetime": feed["gameData"].get("datetime"),
        "teams": {k: {"id": v.get("id"), "abbreviation": v.get("abbreviation")}
                  for k, v in feed["gameData"].get("teams", {}).items()},
        "positions": {side: {pid: p.get("allPositions") for pid, p in t.get("players", {}).items()}
                      for side, t in box.items()},
        "plays": feed["liveData"]["plays"]["allPlays"],
    }


season = sys.argv[1]
games = final_games(season)
print(f"{len(games)} final games", flush=True)
failed = []
with gzip.open(DATA / f"feeds_{season}.jsonl.gz", "wt") as fh, ThreadPoolExecutor(6) as pool:
    futures = {pool.submit(fetch, g["game_pk"]): g["game_pk"] for g in games}
    for i, (fut, pk) in enumerate(futures.items(), 1):
        try:
            fh.write(json.dumps(fut.result(), separators=(",", ":")) + "\n")
        except Exception as e:
            failed.append((pk, repr(e)))
        if i % 200 == 0:
            print(f"{i}/{len(games)}", flush=True)
print(f"Done: {len(games) - len(failed)} games written, failed: {failed}")
