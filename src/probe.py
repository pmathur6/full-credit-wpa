"""Probe: pull one day of data from each source and report which fields exist.

Run by .github/workflows/probe.yml. Writes probe/report.md plus small samples.
"""
import io
import json
import sys
from pathlib import Path

import pandas as pd
import requests

DATE = sys.argv[1] if len(sys.argv) > 1 else "2025-07-04"
OUT = Path("probe")
OUT.mkdir(exist_ok=True)
HEADERS = {"User-Agent": "full-credit-wpa research (github.com/pmathur6/full-credit-wpa)"}

SAVANT_CSV = (
    "https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfGT=R%7C"
    "&game_date_gt={d}&game_date_lt={d}&type=details&player_type=pitcher"
    "&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&sort_order=desc"
)
SCHEDULE = "https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={d}"
LIVE_FEED = "https://statsapi.mlb.com/api/v1.1/game/{pk}/feed/live"
SAVANT_GF = "https://baseballsavant.mlb.com/gf?game_pk={pk}"

# Fields the credit engine needs from the Savant pitch file
WANTED = {
    "game state": ["game_pk", "at_bat_number", "pitch_number", "inning", "inning_topbot",
                   "outs_when_up", "balls", "strikes", "home_score", "away_score",
                   "bat_score", "fld_score", "post_bat_score"],
    "runners": ["on_1b", "on_2b", "on_3b"],
    "players": ["batter", "pitcher"] + [f"fielder_{i}" for i in range(2, 10)],
    "outcome": ["events", "description", "des", "type", "bb_type"],
    "batted ball": ["launch_speed", "launch_angle", "hc_x", "hc_y", "hit_location",
                    "hit_distance_sc", "estimated_ba_using_speedangle",
                    "estimated_woba_using_speedangle"],
    "win/run value": ["delta_home_win_exp", "delta_run_exp", "home_win_exp", "bat_win_exp"],
    "alignment": ["if_fielding_alignment", "of_fielding_alignment"],
    "pitch location": ["plate_x", "plate_z", "zone", "sz_top", "sz_bot"],
}


def get(url):
    r = requests.get(url, headers=HEADERS, timeout=120)
    r.raise_for_status()
    return r


def find_keys(obj, words, path="", found=None, limit=40):
    """Recursively collect key paths containing any of `words`."""
    found = found if found is not None else set()
    if len(found) >= limit:
        return found
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if any(w in k.lower() for w in words):
                found.add(p.replace(".0.", "[]."))
            find_keys(v, words, p, found, limit)
    elif isinstance(obj, list) and obj:
        find_keys(obj[0], words, f"{path}.0", found, limit)
    return found


lines = [f"# Probe report: {DATE}", ""]

# ---- 1. Savant pitch-level CSV ----
lines.append("## Savant pitch-level CSV")
try:
    df = pd.read_csv(io.StringIO(get(SAVANT_CSV.format(d=DATE)).text), low_memory=False)
    lines.append(f"- Rows (pitches): {len(df):,}; columns: {len(df.columns)}; "
                 f"games: {df['game_pk'].nunique() if 'game_pk' in df else '?'}")
    lines.append("")
    lines.append("| Group | Field | Present | Non-null % |")
    lines.append("|---|---|---|---|")
    for group, cols in WANTED.items():
        for c in cols:
            if c in df.columns:
                lines.append(f"| {group} | `{c}` | yes | {df[c].notna().mean():.0%} |")
            else:
                lines.append(f"| {group} | `{c}` | **no** | - |")
    if "events" in df.columns:
        ev = df["events"].value_counts()
        lines += ["", "Event counts:", "", "| Event | n |", "|---|---|"]
        lines += [f"| {k} | {v} |" for k, v in ev.items()]
    extra = sorted(set(df.columns) - {c for cols in WANTED.values() for c in cols})
    lines += ["", "Other columns: " + ", ".join(f"`{c}`" for c in extra)]
    df.head(300).to_csv(OUT / "savant_sample.csv", index=False)
except Exception as e:  # report and keep going
    lines.append(f"- FAILED: {e!r}")
lines.append("")

# ---- 2. MLB Stats API live feed ----
lines.append("## MLB Stats API live feed")
game_pks = []
try:
    sched = get(SCHEDULE.format(d=DATE)).json()
    game_pks = [g["gamePk"] for d in sched.get("dates", []) for g in d["games"]]
    lines.append(f"- Games on {DATE}: {len(game_pks)}")
    pk = game_pks[0]
    feed = get(LIVE_FEED.format(pk=pk)).json()
    plays = feed["liveData"]["plays"]["allPlays"]
    lines.append(f"- Sample game {pk}: {len(plays)} plays")
    n_runner_moves = sum(len(p.get("runners", [])) for p in plays)
    credit_types, movement_reasons, event_types = {}, {}, {}
    for p in plays:
        for ev in p.get("playEvents", []):
            et = ev.get("details", {}).get("eventType")
            if et:
                event_types[et] = event_types.get(et, 0) + 1
        for r in p.get("runners", []):
            reason = r.get("details", {}).get("movementReason")
            if reason:
                movement_reasons[reason] = movement_reasons.get(reason, 0) + 1
            for c in r.get("credits", []):
                k = f"{c.get('credit')} ({c.get('position', {}).get('abbreviation')})"
                credit_types[k] = credit_types.get(k, 0) + 1
    lines.append(f"- Runner movements: {n_runner_moves}")
    lines += ["", "Fielding credits on runner movements:", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(credit_types.items())]
    lines += ["", "Runner movement reasons (mid-PA events):", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(movement_reasons.items())] or ["- none"]
    lines += ["", "Mid-PA event types (playEvents):", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(event_types.items())] or ["- none"]
    hit = next((ev["hitData"] for p in plays for ev in p.get("playEvents", [])
                if "hitData" in ev), None)
    lines += ["", f"- hitData fields: {sorted(hit.keys()) if hit else 'none'}"]
    if hit and "coordinates" in hit:
        lines.append(f"- hitData.coordinates: {sorted(hit['coordinates'].keys())}")
    (OUT / "livefeed_sample_play.json").write_text(
        json.dumps(next((p for p in plays if p.get("runners") and len(p["runners"]) > 1),
                        plays[0]), indent=2))
except Exception as e:
    lines.append(f"- FAILED: {e!r}")
lines.append("")

# ---- 3. Savant game feed (per-play catch probability?) ----
lines.append("## Savant game feed (gf endpoint)")
try:
    if not game_pks:
        raise RuntimeError("no game_pk from schedule")
    gf = get(SAVANT_GF.format(pk=game_pks[0])).json()
    lines.append(f"- Top-level keys: {sorted(gf.keys())[:40]}")
    hits = find_keys(gf, ["catch", "prob", "oaa", "success", "hang", "sprint", "arm"])
    lines += ["", "Keys mentioning catch / prob / oaa / success / hang / sprint / arm:", ""]
    lines += [f"- `{k}`" for k in sorted(hits)] or ["- none found"]
    (OUT / "savant_gf_keys.json").write_text(json.dumps(sorted(find_keys(gf, [""], limit=400)), indent=1))
except Exception as e:
    lines.append(f"- FAILED: {e!r}")

(OUT / "report.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
