"""Check a season's site export against the credit outputs; exits non-zero on a mismatch.

Usage: python src/site/check_export.py <season> <site_data_dir>
"""
import json
import sys
from pathlib import Path

import pandas as pd

season = sys.argv[1]
D = Path(sys.argv[2]) / season
fail = []
lb = json.loads((D / "leaderboard.json").read_text())
d = pd.DataFrame(lb["players"], columns=lb["cols"]).set_index("id")
out = [f"# Site export check: {season}", ""]
for f, u in ((f"output/players_{season}.csv", "w"), (f"output/players_runs_{season}.csv", "r")):
    p = pd.read_csv(f, index_col=0)
    j = d.join(p, how="left", rsuffix="_o")
    for a, b in (("bat", "batting"), ("br", "baserunning"), ("fld", "fielding"), ("pit", "pitching")):
        gap = (j[f"{a}_{u}"] - j[b]).abs().max()
        if gap > 0.002:
            fail.append(f"leaderboard {a}_{u} differs from {f} by {gap:.4f}")
games = json.loads((D / "games.json").read_text())["rows"]
n_ev = gaps = 0
for gid, *_ in games:
    g = json.loads((D / "games" / f"{gid}.json").read_text())
    for e in g["events"]:
        bt = g["home"] if e[4] == "bottom" else g["away"]
        n_ev += 1
        for i, k in ((4, 16), (5, 17)):
            off = sum(c[i] for c in e[18] if c[1] == bt)
            if abs(off - e[k]) > 0.002:
                gaps += 1
if gaps:
    fail.append(f"{gaps} events whose batting-team credits differ from the event's change")
logs = 0
for f in (D / "players").glob("*.json"):
    p = json.loads(f.read_text())
    rows = pd.DataFrame(p["log"]["rows"], columns=p["log"]["cols"])
    for u in ("w", "r"):
        for a, b in (("bat", "batting"), ("br", "baserunning"), ("fld", "fielding"), ("pit", "pitching"), ("behind", "behind")):
            if abs(rows[f"{a}_{u}"].sum() - p["totals"][u][b]) > 0.002:
                logs += 1
if logs:
    fail.append(f"{logs} player totals that don't equal their game logs")
size = sum(f.stat().st_size for f in D.rglob("*.json"))
out += [f"- Leaderboard players (10+ games): {len(d):,}",
        f"- Player files: {len(list((D / 'players').glob('*.json'))):,}; game files: {len(games):,}; events: {n_ev:,}",
        f"- Size: {size / 1e6:.1f} MB",
        f"- Result: {'OK' if not fail else 'FAILED'}"] + [f"  - {x}" for x in fail]
print("\n".join(out))
sys.exit(1 if fail else 0)
