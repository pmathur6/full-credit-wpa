"""Probe: look for per-play catch probability on Baseball Savant.

Fetches player fielding pages and candidate data endpoints, then reports status,
size and every key/snippet that mentions catch probability or related fields.
Writes probe/fielding_report.md.
"""
import re
import sys
from pathlib import Path

import requests

SEASON = sys.argv[1] if len(sys.argv) > 1 else "2025"
PLAYER = sys.argv[2] if len(sys.argv) > 2 else "691718"  # default: Pete Crow-Armstrong
SLUG = sys.argv[3] if len(sys.argv) > 3 else "pete-crow-armstrong"
OUT = Path("probe")
OUT.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (full-credit-wpa research; github.com/pmathur6/full-credit-wpa)"}
S = "https://baseballsavant.mlb.com"

CANDIDATES = {
    "player page (OF fielding)": f"{S}/savant-player/{SLUG}-{PLAYER}?stats=statcast-r-fielding-of",
    "player page (fielding)": f"{S}/savant-player/{SLUG}-{PLAYER}?stats=statcast-r-fielding",
    "catch prob leaderboard csv": f"{S}/leaderboard/catch_probability?type=player&year={SEASON}&total=0&min=q&csv=true",
    "OAA leaderboard csv": f"{S}/leaderboard/outs_above_average?type=Fielder&startYear={SEASON}&endYear={SEASON}&split=no&team=&range=year&min=q&pos=&roles=&viz=hide&csv=true",
    "player-services range": f"{S}/player-services/range?playerId={PLAYER}&season={SEASON}&playerType=fielder",
    "player-services range (infield)": f"{S}/player-services/range?playerId={PLAYER}&season={SEASON}&playerType=fielder&type=infield",
    "player-services infield": f"{S}/player-services/infield?playerId={PLAYER}&season={SEASON}",
    "player page (IF fielding)": f"{S}/savant-player/{SLUG}-{PLAYER}?stats=statcast-r-fielding-if",
    "statcast_catch_probability": f"{S}/statcast_catch_probability",
    "fielding run value csv": f"{S}/leaderboard/fielding-run-value?gameType=Regular&seasonStart={SEASON}&seasonEnd={SEASON}&type=fielder&position=&minInnings=0&minResults=1&csv=true",
}
TERMS = re.compile(r"catch_prob|catchprob|catch_probability|catch_rank|oaa|opportunity_time|"
                   r"distance_covered|start_distance|starting_position|est_success|"
                   r"intercept|hang_time|jump", re.I)


def snippets(text, n=12, width=160):
    out, seen = [], set()
    for m in TERMS.finditer(text):
        s = max(0, m.start() - width)
        snip = text[s:m.end() + width].replace("\n", " ")
        key = m.group(0).lower()
        if (key, len(out)) in seen:
            continue
        out.append(snip)
        seen.add((key, len(out)))
        if len(out) >= n:
            break
    return out


lines = [f"# Fielding probe ({SEASON}, player {PLAYER})", ""]
for name, url in CANDIDATES.items():
    lines.append(f"## {name}")
    lines.append(f"- URL: `{url}`")
    try:
        r = requests.get(url, headers=HEADERS, timeout=90)
        text = r.text
        lines.append(f"- Status {r.status_code}, {r.headers.get('content-type')}, {len(text):,} chars")
        # endpoints referenced from the page
        eps = sorted(set(re.findall(r"""["'](/(?:player-services|leaderboard|visuals|statcast|gf|services|api)[^"'\s]{0,120})["']""", text)))
        if eps:
            lines.append("- Endpoints referenced: " + ", ".join(f"`{e}`" for e in eps[:40]))
        # JSON-ish keys that match
        keys = sorted(set(k.lower() for k in re.findall(r'"([A-Za-z_]*(?:catch|oaa|prob|opportunity|distance|success|jump|start)[A-Za-z_]*)"\s*:', text, re.I)))
        if keys:
            lines.append("- Matching JSON keys: " + ", ".join(f"`{k}`" for k in keys[:60]))
        if text[:200].count(",") > 3 and "<html" not in text[:500].lower():
            lines.append("- CSV header: `" + text.splitlines()[0][:600] + "`")
            lines.append(f"- CSV rows: {len(text.splitlines()) - 1}")
        snips = snippets(text)
        if snips:
            lines += ["- Snippets:", ""] + [f"  - `{s}`" for s in snips]
    except Exception as e:
        lines.append(f"- FAILED: {e!r}")
    lines.append("")

(OUT / f"fielding_report_{PLAYER}.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
