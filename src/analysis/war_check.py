"""Correlate our WAR scale with published WAR (Baseball-Reference bWAR; FanGraphs fWAR if reachable).

Usage: python src/analysis/war_check.py <site_data_dir> <season> [<season> ...]
Reads <site_data_dir>/<season>/leaderboard.json; writes reports/war_check.md.
"""
import io
import json
import sys
from pathlib import Path

import pandas as pd
import requests

D = Path(sys.argv[1])
SEASONS = [int(s) for s in sys.argv[2:]]
UA = {"User-Agent": "Mozilla/5.0 (full-credit-wpa research; github.com/pmathur6/full-credit-wpa)"}
status = []


def fetch_csv(url, **kw):
    r = requests.get(url, headers=UA, timeout=120)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), **kw)


# ---- Baseball-Reference daily WAR files (one row per player-season-stint)
bref_bat = bref_pit = None
try:
    bref_bat = fetch_csv("https://www.baseball-reference.com/data/war_daily_bat.txt", low_memory=False)
    bref_pit = fetch_csv("https://www.baseball-reference.com/data/war_daily_pitch.txt", low_memory=False)
    status.append(f"bWAR: ok ({len(bref_bat):,} batting rows, {len(bref_pit):,} pitching rows)")
except Exception as e:
    status.append(f"bWAR: unavailable ({e})")


def bref(season):
    if bref_bat is None:
        return None
    out = {}
    for df, col in ((bref_bat, "bwar_bat"), (bref_pit, "bwar_pit")):
        x = df[df.year_ID.eq(season)].copy()
        x["WAR"] = pd.to_numeric(x.WAR, errors="coerce")
        x["mlb_ID"] = pd.to_numeric(x.mlb_ID, errors="coerce")
        out[col] = x.dropna(subset=["mlb_ID"]).groupby("mlb_ID")["WAR"].sum()
    return pd.DataFrame(out).fillna(0)


# ---- FanGraphs leaderboard API
def fangraphs(season):
    out = {}
    for stats, col in (("bat", "fwar_bat"), ("pit", "fwar_pit")):
        url = (f"https://www.fangraphs.com/api/leaders/major-league/data?age=&pos=all&stats={stats}&lg=all&qual=0"
               f"&season={season}&season1={season}&startdate=&enddate=&month=0&hand=&team=0&pageitems=5000&pagenum=1"
               f"&ind=0&rost=0&players=&type=8&sortdir=default&sortstat=WAR")
        r = requests.get(url, headers=UA, timeout=120)
        r.raise_for_status()
        rows = r.json()["data"]
        x = pd.DataFrame(rows)
        x["xMLBAMID"] = pd.to_numeric(x["xMLBAMID"], errors="coerce")
        out[col] = x.dropna(subset=["xMLBAMID"]).groupby("xMLBAMID")["WAR"].sum()
    return pd.DataFrame(out).fillna(0)


L = ["# Our WAR scale vs published WAR", "",
     "Pearson r between our WAR-scale column (runs view on WAR's footing; see README) and Baseball-Reference / FanGraphs WAR,",
     "matched by MLBAM id. Hitters: our hitting WAR scale vs batting WAR (300+ PA). Pitchers: our pitching WAR scale vs",
     "pitching WAR (300+ batters faced). All: hitting + pitching vs total, players with 10+ games.", ""]
fg_status = None
rows = []
detail = []
for season in SEASONS:
    lb = json.loads((D / str(season) / "leaderboard.json").read_text())
    d = pd.DataFrame(lb["players"], columns=lb["cols"]).set_index("id")
    d["war"] = d.warbat + d.warpit
    refs = {}
    b = bref(season)
    if b is not None:
        refs["bWAR"] = b.rename(columns={"bwar_bat": "bat", "bwar_pit": "pit"})
    try:
        refs["fWAR"] = fangraphs(season).rename(columns={"fwar_bat": "bat", "fwar_pit": "pit"})
        fg_status = fg_status or "fWAR: ok"
    except Exception as e:
        fg_status = f"fWAR: unavailable ({e})"
    for src, ref in refs.items():
        j = d.join(ref, how="inner")
        j["tot"] = j.bat + j.pit
        for grp, sub, ours, theirs in (("Hitters (300+ PA)", j[j.pa >= 300], "warbat", "bat"),
                                       ("Pitchers (300+ BF)", j[j.bf >= 300], "warpit", "pit"),
                                       ("All players (10+ games)", j, "war", "tot")):
            if len(sub) > 5:
                diff = sub[ours] - sub[theirs]
                rows.append([season, src, grp, len(sub), sub[ours].corr(sub[theirs]), diff.mean(), diff.abs().mean()])
        h = j[j.pa >= 300].assign(gap=lambda x: x.warbat - x.bat)
        detail.append((season, src, h.sort_values("gap").head(5), h.sort_values("gap").tail(5)))
    # benchmark: how closely the two published versions agree with each other on the same players
    if len(refs) == 2:
        bb, ff = refs["bWAR"], refs["fWAR"]
        j = d.join(bb, how="inner").join(ff, how="inner", rsuffix="_f")
        for grp, sub, x, y in (("Hitters (300+ PA)", j[j.pa >= 300], "bat", "bat_f"),
                               ("Pitchers (300+ BF)", j[j.bf >= 300], "pit", "pit_f"),
                               ("All players (10+ games)", j, None, None)):
            xs = sub[x] if x else sub.bat + sub.pit
            ys = sub[y] if y else sub.bat_f + sub.pit_f
            rows.append([season, "bWAR vs fWAR (benchmark)", grp, len(sub), xs.corr(ys), (xs - ys).mean(), (xs - ys).abs().mean()])
status.append(fg_status or "fWAR: not tried")

t = pd.DataFrame(rows, columns=["season", "source", "group", "n", "r", "mean_diff", "mean_abs_diff"])
L += ["| Season | Source | Group | Players | r | Ours minus theirs (mean) | Mean abs. difference |", "|---|---|---|---|---|---|---|"]
for r in t.itertuples():
    L.append(f"| {r.season} | {r.source} | {r.group} | {r.n} | {r.r:.3f} | {r.mean_diff:+.2f} | {r.mean_abs_diff:.2f} |")
if len(t):
    L += ["", "Pooled across seasons:", "", "| Source | Group | Player-seasons | r |", "|---|---|---|---|"]
    for (src, grp), g in t.groupby(["source", "group"]):
        L.append(f"| {src} | {grp} | {g.n.sum()} | {(g.r * g.n).sum() / g.n.sum():.3f} (n-weighted) |")
L += ["", "## Largest hitter gaps (ours minus theirs)", ""]
for season, src, lo, hi in detail:
    fmt = lambda df: ", ".join(f"{n} {o:.1f} vs {t_:.1f}" for n, o, t_ in zip(df.name, df.warbat, df.bat))
    L += [f"- {season} {src}: below: {fmt(lo)}", f"- {season} {src}: above: {fmt(hi)}"]
L += ["", "## Sources", ""] + [f"- {s}" for s in status]
Path("reports").mkdir(exist_ok=True)
Path("reports/war_check.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
