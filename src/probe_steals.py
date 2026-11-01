"""Probe: look for stolen-base timing on Baseball Savant (pop time, time to plate, leads),
ideally per attempt, otherwise per player-season. Writes probe/steals_report.md.
"""
import json
import re
import sys
from pathlib import Path

import requests

SEASON = sys.argv[1] if len(sys.argv) > 1 else "2025"
S = "https://baseballsavant.mlb.com"
H = {"User-Agent": "Mozilla/5.0 (full-credit-wpa research; github.com/pmathur6/full-credit-wpa)"}
CATCHER, C_SLUG = "672275", "patrick-bailey"
PITCHER, P_SLUG = "669373", "tarik-skubal"
RUNNER, R_SLUG = "682829", "elly-de-la-cruz"
GAME = "776135"

CANDIDATES = {
    "catcher-throwing (player=)": f"{S}/player-services/catcher-throwing?player={CATCHER}&season={SEASON}",
    "catcher-throwing (player=, year=)": f"{S}/player-services/catcher-throwing?player={CATCHER}&year={SEASON}",
    "catcher-throwing (player=, no season)": f"{S}/player-services/catcher-throwing?player={CATCHER}",
    "pitcher running game leaderboard": f"{S}/leaderboard/pitcher-running-game?game_type=Regular&n=1&season_start={SEASON}&season_end={SEASON}&split=no&team=&pitch_hand=&runner_moved=&target_base=All&prior_pk=All&with_team_only=1&csv=true",
    "pitcher running game page": f"{S}/leaderboard/pitcher-running-game",
    "basestealing run value (type=Pitcher)": f"{S}/leaderboard/basestealing-run-value?game_type=Regular&n=1&target_base=All&split=no&team=&type=Pitcher&with_team_only=1&season_start={SEASON}&season_end={SEASON}&csv=true",
    "basestealing run value (type=Catcher)": f"{S}/leaderboard/basestealing-run-value?game_type=Regular&n=1&target_base=All&split=no&team=&type=Catcher&with_team_only=1&season_start={SEASON}&season_end={SEASON}&csv=true",
    "catcher throwing leaderboard page": f"{S}/leaderboard/catcher-throwing",
}
TERMS = re.compile(r"pop|time_to|to_plate|lead|steal|sb_|cs_|throw|exchange|arm_|jump|secondary|primary|attempt", re.I)


def keys(obj, found, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if TERMS.search(k):
                found.add(re.sub(r"\.\d+", "[]", f"{path}.{k}".strip(".")))
            keys(v, found, f"{path}.{k}")
    elif isinstance(obj, list) and obj:
        keys(obj[0], found, f"{path}.0")


lines = [f"# Steal-timing probe ({SEASON})", ""]
for name, url in CANDIDATES.items():
    lines += [f"## {name}", f"- URL: `{url}`"]
    try:
        r = requests.get(url, headers=H, timeout=90)
        t = r.text
        ctype = r.headers.get("content-type", "")
        lines.append(f"- Status {r.status_code}, {ctype}, {len(t):,} chars")
        if "csv" in ctype or (t[:300].count(",") > 5 and "<html" not in t[:500].lower()):
            rows = t.splitlines()
            lines += [f"- CSV rows: {len(rows) - 1}", f"- Header: `{rows[0][:900]}`"]
            if len(rows) > 1:
                lines.append(f"- First row: `{rows[1][:500]}`")
        elif "json" in ctype:
            found = set()
            keys(json.loads(t), found)
            lines.append(f"- Matching keys: {sorted(found)[:60]}")
            lines.append(f"- Start: `{t[:500]}`")
        else:
            ks = sorted(set(m.lower() for m in re.findall(r'"([a-z_]*(?:pop|time_to|lead|steal|sb_|cs_|throw|exchange|arm_|attempt)[a-z_]*)"\s*:', t, re.I)))
            lines.append(f"- Matching JSON keys in page: {ks[:80]}")
            eps = sorted(set(re.findall(r"""["'`](/(?:player-services|leaderboard|services|api)/[^"'`\s?]{0,80})""", t)))
            lines.append(f"- Endpoints referenced: {eps[:60]}")
            for v in ("runningGame", "running_game", "catcher_throwing", "poptime", "basestealing", "throws"):
                i = t.find(v)
                if i >= 0:
                    lines.append(f"  - `{v}` context: `{t[max(0, i - 150):i + 250].replace(chr(10), ' ')}`")
    except Exception as e:
        lines.append(f"- FAILED: {e!r}")
    lines.append("")
Path("probe").mkdir(exist_ok=True)
Path("probe/steals_report.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
