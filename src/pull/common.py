"""Shared helpers for the data pulls."""
import time
from pathlib import Path

import requests

HEADERS = {"User-Agent": "Mozilla/5.0 (full-credit-wpa research; github.com/pmathur6/full-credit-wpa)"}
DATA = Path("data/raw")
DATA.mkdir(parents=True, exist_ok=True)
SCHEDULE = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&season={season}&gameType=R"

_session = requests.Session()
_session.headers.update(HEADERS)


def get(url, tries=5, timeout=120):
    """GET with exponential backoff. Returns the Response or raises after `tries`."""
    for i in range(tries):
        try:
            r = _session.get(url, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code == 404:
                r.raise_for_status()
        except requests.RequestException:
            if i == tries - 1:
                raise
        time.sleep(2 ** i)
    r.raise_for_status()
    return r


def final_games(season):
    """Regular-season games that reached Final, one row per gamePk (suspended games deduped)."""
    sched = get(SCHEDULE.format(season=season)).json()
    games = {}
    for d in sched.get("dates", []):
        for g in d["games"]:
            if g["status"]["abstractGameState"] == "Final":
                games[g["gamePk"]] = {"game_pk": g["gamePk"], "date": d["date"],
                                     "status": g["status"]["detailedState"]}
    return sorted(games.values(), key=lambda g: (g["date"], g["game_pk"]))
