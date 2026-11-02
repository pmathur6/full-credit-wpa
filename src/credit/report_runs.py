"""Checks and leaderboards for the context-neutral (runs) version of a season's credits.

Same split as the wins version, valued in run expectancy (every play counts the same,
whatever the score or inning). Each half-inning is valued on its own, so a team's run
credits equal, summed over its half-innings, runs scored + expected runs at the end of the
half - expected runs at the start (0 at three outs), batting minus fielding.

Writes:
  reports/credit_report_runs_<season>.md
  output/players_runs_<season>.csv   same columns as players_<season>.csv, in runs
  output/coaching_runs_<season>.csv
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

season = sys.argv[1]
BUILD = Path(sys.argv[2] if len(sys.argv) > 2 else "data/build")
CREDIT = Path(sys.argv[3] if len(sys.argv) > 3 else "data/credit")
for d in ("reports", "output"):
    Path(d).mkdir(exist_ok=True)

cr = pd.read_parquet(CREDIT / f"credits_runs_{season}.parquet")
ev = pd.read_parquet(BUILD / f"events_{season}.parquet")
L = [f"# Credit report (runs, context-neutral): {season}", ""]

# ---- identities
key = ["game_pk", "at_bat_index", "play_index", "kind"]
s = cr.groupby(key + ["side"])["credit"].sum().unstack(fill_value=0).join(ev.set_index(key)["d_re_bat"], how="right").fillna(0)
off_gap = (s["off"] - s["d_re_bat"]).abs()
def_gap = (s["def"] + s["d_re_bat"]).abs()

pa = ev[ev.kind.eq("pa")]
h = pa.groupby(["game_pk", "inning", "half"], sort=False).agg(
    bat=("batting_team", "first"), fld=("fielding_team", "first"), start=("re_before", "first"),
    end=("re_after", "last"), half_=("half", "first"))
sign = np.where(h.half_.eq("bottom"), 1.0, -1.0)
h["val"] = (h.end - h.start) * sign  # batting team's runs + RE change over the half
target = h.groupby("bat")["val"].sum().sub(h.groupby("fld")["val"].sum(), fill_value=0)
games = pa.groupby("game_pk").agg(h=("home_after", "last"), a=("away_after", "last"))
home = pa[pa.half.eq("bottom")].groupby("game_pk")["batting_team"].first()
away = pa[pa.half.eq("top")].groupby("game_pk")["batting_team"].first()
games = games.join(home.rename("home")).join(away.rename("away")).dropna()
rd = pd.concat([pd.DataFrame({"team": games.home, "rd": games.h - games.a}),
                pd.DataFrame({"team": games.away, "rd": games.a - games.h})]).groupby("team")["rd"].sum()
tc = cr.groupby("team")["credit"].sum()
tt = pd.DataFrame({"credited": tc, "target": target, "run_diff": rd})
tt["gap"] = (tt.credited - tt.target).abs()
L += ["## 1. Accounting identities (must hold exactly)", "",
      f"- Events: {len(s):,}. Offense credits equal the event's change on {(off_gap < 1e-9).mean():.3%}; "
      f"defense credits equal minus the change on {(def_gap < 1e-9).mean():.3%} (max gaps {off_gap.max():.2e} / {def_gap.max():.2e})",
      f"- Teams whose total equals their half-inning run values (runs + expected-runs change, batting minus fielding): "
      f"{(tt.gap < 1e-6).sum()} of {len(tt)} (max gap {tt.gap.max():.2e})",
      f"- Correlation of team run credit with run differential: {tt.credited.corr(tt.run_diff):.3f}",
      "", "| Team | Run diff | Credited (runs) |", "|---|---|---|"]
for t, r in tt.sort_values("run_diff", ascending=False).iterrows():
    L.append(f"| {t} | {r.run_diff:+.0f} | {r.credited:+.1f} |")

# ---- players (positions, team, name, PA/BF from the wins version)
p = cr.dropna(subset=["player_id"]).pivot_table(index="player_id", columns="bucket", values="credit", aggfunc="sum", fill_value=0)
for b in ("batting", "baserunning", "fielding", "pitching"):
    if b not in p:
        p[b] = 0.0
p = p[["batting", "baserunning", "fielding", "pitching"]]
p["total"] = p.sum(axis=1)
p["trad_bat"] = pa.groupby("batter")["d_re_bat"].sum()
p["trad_pit"] = -ev.groupby("pitcher")["d_re_bat"].sum()
p = p.fillna(0)
p.index = p.index.astype(int)
wins = Path(f"output/players_{season}.csv")
if wins.exists():
    w = pd.read_csv(wins, index_col=0)
    w.index = w.index.astype(int)
    p = p.join(w[["pa", "bf", "positions", "team", "name"]])
p.round(3).to_csv(f"output/players_runs_{season}.csv")
coach = cr[cr.bucket.eq("coaching")].pivot_table(index="team", columns="role", values="credit", aggfunc="sum", fill_value=0)
coach["total"] = coach.sum(axis=1)
coach.round(3).sort_values("total", ascending=False).to_csv(f"output/coaching_runs_{season}.csv")


def table(df, cols, title, n=10, asc=False):
    out = ["", f"### {title}", "", "| Player | Pos | Team | " + " | ".join(cols) + " |", "|---|---|---|" + "---|" * len(cols)]
    for _, r in df.sort_values(cols[0], ascending=asc).head(n).iterrows():
        out.append(f"| {r.get('name', '-')} | {r.get('positions', '-')} | {r.get('team', '-')} | " + " | ".join(f"{r[c]:+.1f}" for c in cols) + " |")
    return out


L += ["", "## 2. Leaderboards (runs)", "", "Hitters 300+ PA, pitchers 300+ batters faced. `trad` = RE24 (batter / pitcher gets the whole play)."]
if "pa" in p:
    L += table(p[p.pa >= 300], ["total", "batting", "baserunning", "fielding", "trad_bat"], "Hitters: top 10 total")
    L += table(p[p.bf >= 300], ["pitching", "fielding", "trad_pit"], "Pitchers: top 10")
L += table(p, ["fielding"], "Fielding: top 10")
L += table(p, ["baserunning"], "Baserunning: top 10")
L += ["", "### Coaching (team, runs)", ""] + [f"- {t}: {v:+.1f}" for t, v in coach.total.sort_values(ascending=False).items()]
Path(f"reports/credit_report_runs_{season}.md").write_text("\n".join(L) + "\n")
print("\n".join(L[:8]))
