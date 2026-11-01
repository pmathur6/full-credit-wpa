"""Compare our buckets with outside metrics. Writes reports/external_checks_<season>.md.

Ours are wins, weighted by game situation; Savant's are runs, context-neutral. So
agreement is measured by correlation (direction and ranking), not by level.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

season = sys.argv[1]
REF = Path("reference")
p = pd.read_csv(f"output/players_{season}.csv").set_index("player_id")
L = [f"# External checks: {season}", "",
     "Our numbers are wins weighted by game situation; Savant's are context-neutral runs. "
     "Correlations measure whether the two rank players the same way. "
     "Typical leverage noise alone keeps a perfect-in-substance match below 1.0.", ""]


def corr(a, b):
    j = pd.concat([a, b], axis=1, join="inner").dropna()
    return (np.nan, 0) if len(j) < 5 else (np.corrcoef(j.iloc[:, 0], j.iloc[:, 1])[0, 1], len(j))


def line(label, a, b, note=""):
    r, n = corr(a, b)
    L.append(f"| {label} | {n} | {r:.3f} | {note} |")


def top_gaps(ours, theirs, title, k=6):
    j = pd.concat([ours.rename("ours"), theirs.rename("savant")], axis=1, join="inner").dropna()
    if len(j) < 10:
        return
    z = (j - j.mean()) / j.std()
    j["gap"] = z.ours - z.savant
    L.extend(["", f"Biggest disagreements, {title} (standardized; + = we rate higher):", "",
              "| Player | Pos | Ours | Savant |", "|---|---|---|---|"])
    for pid, r in pd.concat([j.nlargest(k // 2, "gap"), j.nsmallest(k // 2, "gap")]).iterrows():
        L.append(f"| {p.at[pid, 'name']} | {p.at[pid, 'positions']} | {r.ours:+.2f} wins | {r.savant:+.1f} runs |")


L += ["## Correlations", "", "| Comparison | Players | Correlation | Note |", "|---|---|---|---|"]

# ---- internal: our buckets vs traditional WPA
hit = p[p.pa >= 200]
pit = p[p.bf >= 200]
line("Batting vs traditional batter WPA (200+ PA)", hit.batting, hit.trad_bat, "same plays, runners' share removed")
line("Batting + baserunning vs traditional batter WPA", hit.batting + hit.baserunning, hit.trad_bat)
line("Pitching vs traditional pitcher WPA (200+ BF)", pit.pitching, pit.trad_pit, "fielders' share removed")

# ---- Savant baserunning run value
f = REF / f"savant_brv_{season}.csv"
if f.exists():
    brv = pd.read_csv(f).groupby("player_id")[["runner_runs_tot", "runner_runs_XB", "runner_runs_SBX"]].sum()
    line("Baserunning vs Savant baserunning run value", p.baserunning, brv.runner_runs_tot,
         "Savant: extra bases + steals")
    line("  ...vs Savant extra-base runs only", p.baserunning, brv.runner_runs_XB)
    line("  ...vs Savant stolen-base runs only", p.baserunning, brv.runner_runs_SBX)
else:
    L.append("| Baserunning vs Savant | - | - | reference not available |")

# ---- Savant fielding run value
f = REF / f"savant_frv_{season}.csv"
if f.exists():
    frv = pd.read_csv(f).rename(columns={"id": "player_id"}).groupby("player_id").sum(numeric_only=True)
    nonp = p[~p.positions.isin(["P", "DH", "-"])]
    of = nonp[nonp.positions.str.split("/").str[0].isin(["LF", "CF", "RF"])]
    inf = nonp[nonp.positions.str.split("/").str[0].isin(["1B", "2B", "3B", "SS"])]
    cat = nonp[nonp.positions.str.split("/").str[0].eq("C")]
    line("Fielding vs Savant fielding run value (all non-pitchers)", nonp.fielding, frv.total_runs)
    line("  Outfielders vs Savant range + arm", of.fielding, frv.range_runs + frv.arm_runs)
    line("  Infielders vs Savant range + arm + DP", inf.fielding, frv.range_runs + frv.arm_runs + frv.dp_runs)
    line("  Catchers vs Savant throwing + blocking", cat.fielding, frv.throwing_runs + frv.blocking_runs,
         "framing is not in our numbers")
    line("  Catchers vs Savant total catching", cat.fielding, frv.catching_runs, "includes framing")
else:
    L.append("| Fielding vs Savant | - | - | reference not available |")

if (REF / f"savant_brv_{season}.csv").exists():
    top_gaps(p.baserunning, brv.runner_runs_tot, "baserunning")
if (REF / f"savant_frv_{season}.csv").exists():
    top_gaps(of.fielding, frv.range_runs + frv.arm_runs, "outfield")
    top_gaps(inf.fielding, frv.range_runs + frv.arm_runs + frv.dp_runs, "infield")

st = REF / f"external_status_{season}.txt"
if st.exists():
    L += ["", "## Sources", "", "```", st.read_text().strip()[:3000], "```"]
Path("reports").mkdir(exist_ok=True)
Path(f"reports/external_checks_{season}.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
