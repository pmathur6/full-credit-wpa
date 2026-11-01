"""Checks, leaderboards and the edge-case audit for a season's credits.

Writes:
  reports/credit_report_<season>.md   accounting identities, Savant OAA comparison, top/bottom lists
  reports/audit_<season>.md           plain-English sample of unusual plays and who got what
  output/players_<season>.csv         one row per player: buckets, traditional WPA, positions, team
  output/coaching_<season>.csv        one row per team: coaching bucket by type
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

season = sys.argv[1]
BUILD = Path(sys.argv[2] if len(sys.argv) > 2 else "data/build")
CREDIT = Path(sys.argv[3] if len(sys.argv) > 3 else "data/credit")
REF = Path("reference")
for d in ("reports", "output"):
    Path(d).mkdir(exist_ok=True)

cr = pd.read_parquet(CREDIT / f"credits_{season}.parquet")
ev = pd.read_parquet(BUILD / f"events_{season}.parquet")
names = {}
if (REF / f"players_{season}.csv").exists():
    names = pd.read_csv(REF / f"players_{season}.csv").set_index("player_id")["name"].to_dict()


def nm(pid):
    return "-" if pd.isna(pid) else names.get(int(pid), str(int(pid)))


L = [f"# Credit report: {season}", ""]

# ---------------------------------------------------------------- 1. accounting identities
key = ["game_pk", "at_bat_index", "play_index", "kind"]
e = ev.set_index(key)["d_we_bat"]
s = cr.groupby(key + ["side"])["credit"].sum().unstack(fill_value=0)
s = s.join(e, how="right").fillna(0)
off_gap = (s["off"] - s["d_we_bat"]).abs()
def_gap = (s["def"] + s["d_we_bat"]).abs()
g = ev.groupby("game_pk").agg(start=("we_before", "first"), h=("home_after", "last"), a=("away_after", "last"),
                               home=("batting_team", lambda x: None))
first = ev.sort_values(["game_pk", "at_bat_index"]).groupby("game_pk").first()
home_team = ev[ev.half.eq("bottom")].groupby("game_pk")["batting_team"].first()
away_team = ev[ev.half.eq("top")].groupby("game_pk")["batting_team"].first()
games = pd.DataFrame({"home": home_team, "away": away_team, "start": first["we_before"],
                      "h": g["h"], "a": g["a"]}).dropna(subset=["home", "away"])
games["home_result"] = np.where(games.h > games.a, 1.0, np.where(games.h < games.a, 0.0, 0.5))
team_target = pd.concat([
    pd.DataFrame({"team": games.home, "target": games.home_result - games.start, "w": games.home_result}),
    pd.DataFrame({"team": games.away, "target": (1 - games.home_result) - (1 - games.start), "w": 1 - games.home_result}),
]).groupby("team").agg(target=("target", "sum"), wins=("w", "sum"), games=("w", "size"))
team_credit = cr.groupby("team")["credit"].sum()
team_target["credited"] = team_credit
team_target["gap"] = (team_target.credited - team_target.target).abs()
L += ["## 1. Accounting identities (must hold exactly)", "",
      f"- Events: {len(s):,}. Offense credits equal the event's change on {(off_gap < 1e-9).mean():.3%}; "
      f"defense credits equal minus the change on {(def_gap < 1e-9).mean():.3%} (max gaps {off_gap.max():.2e} / {def_gap.max():.2e})",
      f"- Events with no credit rows: {int(s.index.difference(cr.set_index(key).index.unique()).size)}; "
      f"events with no change in win probability (decided games): {int((s['d_we_bat'].abs() < 1e-12).sum()):,}",
      f"- Teams whose total credit equals wins minus summed starting win probability: "
      f"{(team_target.gap < 1e-6).sum()} of {len(team_target)} (max gap {team_target.gap.max():.2e})",
      f"- Credit rows with no player (coaching buckets): {cr.player_id.isna().sum():,}; "
      f"non-coaching rows with no player: {(cr.player_id.isna() & cr.bucket.ne('coaching')).sum():,}",
      "", "| Team | W | G | Credited | Wins - starting WP |", "|---|---|---|---|---|"]
for t, r in team_target.sort_values("wins", ascending=False).iterrows():
    L.append(f"| {t} | {r.wins:.0f} | {r.games:.0f} | {r.credited:+.2f} | {r.target:+.2f} |")

# ---------------------------------------------------------------- 2. outfield vs Savant OAA
pa = ev[ev.kind.eq("pa")]
cp = pa[pa.catch_prob.notna()]
fld = cr[(cr.kind == "pa") & (cr.bucket == "fielding") & cr.role.isin(["LF", "CF", "RF", "OF"])]
resp = fld.drop_duplicates(["game_pk", "at_bat_index"]).set_index(["game_pk", "at_bat_index"])["player_id"]
cpi = cp.set_index(["game_pk", "at_bat_index"])
same = (resp.reindex(cpi.index) == cpi.cp_player).mean()
ours = cp.assign(oae=cp.cp_out - cp.catch_prob).groupby("cp_player")["oae"].sum()
L += ["", "## 2. Outfield vs Savant OAA", "",
      f"- Outfield catch chances credited to the same fielder Savant names: {same:.2%}"]
if (REF / f"oaa_{season}.csv").exists():
    oaa = pd.read_csv(REF / f"oaa_{season}.csv")
    oaa = oaa[oaa.primary_pos_formatted.isin(["LF", "CF", "RF"])].set_index("player_id")
    j = oaa.join(ours.rename("ours"), how="inner")
    r_ = np.corrcoef(j.outs_above_average, j.ours)[0, 1]
    L += [f"- Outfielders (primary position LF/CF/RF) compared: {len(j)}; correlation of our outs-above-expected "
          f"with Savant OAA: **{r_:.3f}**; mean absolute difference {np.abs(j.outs_above_average - j.ours).mean():.2f} outs",
          "", "Largest differences (Savant OAA includes direction/arm adjustments and other positions):", "",
          "| Player | Savant OAA | Ours (outs - catch prob) |", "|---|---|---|"]
    j["d"] = (j.outs_above_average - j.ours).abs()
    for pid, r in j.sort_values("d", ascending=False).head(8).iterrows():
        L.append(f"| {nm(pid)} | {r.outs_above_average:+.0f} | {r.ours:+.1f} |")
else:
    L.append("- Savant OAA reference not available in this run")

# ---------------------------------------------------------------- 2b. steals vs Savant
st = cr[cr.event_type.str.match(r"^(stolen_base|caught_stealing)_", na=False) & cr.side.eq("def")]
L += ["", "## 2b. Stolen-base defense vs Savant", ""]
for role, fname, col, label in (("C", "catcher_throwing", "catcher_stealing_runs", "catcher stealing runs"),
                                ("pitcher", "pitcher_running", "runs_prevented_on_running_attr", "pitcher running-game runs")):
    f = REF / f"{fname}_{season}.csv"
    if not f.exists():
        L.append(f"- {label}: reference not available")
        continue
    ref = pd.read_csv(f)
    if "key_target_base" in ref:
        ref = ref[ref.key_target_base.eq("All")]
    ref = ref.groupby("player_id")[col].sum()
    ours_s = st[st.role.eq(role)].groupby("player_id")["credit"].sum()
    j = pd.concat([ref.rename("savant"), ours_s.rename("ours")], axis=1, join="inner")
    j = j[(j.savant != 0) | (j.ours != 0)]
    L.append(f"- {label}: {len(j)} players; correlation of our steal-attempt credit (wins, leverage-weighted) "
             f"with Savant's (runs): **{np.corrcoef(j.savant, j.ours)[0, 1]:.3f}**")

# ---------------------------------------------------------------- per-player table
p = cr.dropna(subset=["player_id"]).pivot_table(index="player_id", columns="bucket", values="credit",
                                                 aggfunc="sum", fill_value=0)
for b in ("batting", "baserunning", "fielding", "pitching"):
    if b not in p:
        p[b] = 0.0
p["total"] = p[["batting", "baserunning", "fielding", "pitching"]].sum(axis=1)
pa_rows = ev[ev.kind.eq("pa")]
p["trad_bat"] = pa_rows.groupby("batter")["d_we_bat"].sum()
p["trad_pit"] = -ev.groupby("pitcher")["d_we_bat"].sum()
p["pa"] = pa_rows.groupby("batter").size()
p["bf"] = pa_rows.groupby("pitcher").size()
p = p.fillna(0)
# positions: 10+ appearances (games) at a position, ordered by games
app = pd.concat([ev[["game_pk", f"f{i}"]].rename(columns={f"f{i}": "pid"}).assign(pos=n)
                 for i, n in zip(range(2, 10), ["C", "1B", "2B", "3B", "SS", "LF", "CF", "RF"])]
                + [ev[["game_pk", "pitcher"]].rename(columns={"pitcher": "pid"}).assign(pos="P")])
app = app.dropna().drop_duplicates()
gp = app.groupby(["pid", "pos"]).size().rename("g").reset_index()
pos = (gp[gp.g >= 10].sort_values(["pid", "g"], ascending=[True, False])
       .groupby("pid")["pos"].agg("/".join))
p["positions"] = pos.reindex(p.index)
# DH: 10+ games batting without playing the field that game
bat_g = ev[ev.kind.eq("pa")][["game_pk", "batter"]].drop_duplicates().rename(columns={"batter": "pid"})
fld_g = app[app.pos.ne("P")][["game_pk", "pid"]].drop_duplicates()
dh = bat_g.merge(fld_g, how="left", indicator=True).query("_merge == 'left_only'").groupby("pid").size()
dh = dh[dh >= 10].index
p.loc[p.index.isin(dh), "positions"] = [f"{x}/DH" if isinstance(x, str) else "DH" for x in p.loc[p.index.isin(dh), "positions"]]
p["positions"] = p["positions"].fillna("-")
team = cr.dropna(subset=["player_id"]).groupby(["player_id", "team"]).size().reset_index()
team = team.sort_values(["player_id", 0], ascending=[True, False])
p["team"] = team.groupby("player_id")["team"].agg(lambda x: "/".join(x))
p["name"] = [nm(i) for i in p.index]
p.round(4).to_csv(f"output/players_{season}.csv")

coach = cr[cr.bucket.eq("coaching")].pivot_table(index="team", columns="role", values="credit", aggfunc="sum", fill_value=0)
coach["total"] = coach.sum(axis=1)
coach.round(4).sort_values("total", ascending=False).to_csv(f"output/coaching_{season}.csv")


def table(df, cols, title, n=10, asc=False, sort=None):
    out = ["", f"### {title}", "", "| Player | Pos | Team | " + " | ".join(cols) + " |",
           "|---|---|---|" + "---|" * len(cols)]
    for pid, r in df.sort_values(sort or cols[0], ascending=asc).head(n).iterrows():
        out.append(f"| {r['name']} | {r.positions} | {r.team} | " + " | ".join(f"{r[c]:+.2f}" for c in cols) + " |")
    return out


hit = p[p.pa >= 300]
pit = p[p.bf >= 300]
L += ["", "## 3. Leaderboards (eye test)", "",
      "Wins added. Hitters 300+ PA, pitchers 300+ batters faced. `trad` = traditional WPA (batter / pitcher gets the whole play)."]
L += table(hit, ["total", "batting", "baserunning", "fielding", "trad_bat"], "Hitters: top 10 total")
L += table(hit, ["total", "batting", "baserunning", "fielding", "trad_bat"], "Hitters: bottom 10 total", asc=True)
fl = p[~p.positions.isin(["P", "DH", "-"])]
L += table(fl, ["fielding"], "Fielding: top 10")
L += table(fl, ["fielding"], "Fielding: bottom 10", asc=True)
L += table(p, ["baserunning"], "Baserunning: top 10")
L += table(p, ["baserunning"], "Baserunning: bottom 10", asc=True)
L += table(pit, ["pitching", "fielding", "trad_pit"], "Pitchers: top 10")
L += table(pit, ["pitching", "fielding", "trad_pit"], "Pitchers: bottom 10", asc=True)
pit2 = pit.assign(gap=pit.pitching - pit.trad_pit)
L += table(pit2, ["gap", "pitching", "trad_pit"], "Pitchers hurt most by their defense (our pitching credit above traditional WPA: fielders took some blame)")
L += table(pit2, ["gap", "pitching", "trad_pit"], "Pitchers helped most by their defense (our pitching credit below traditional WPA: fielders took some credit)", asc=True)
L += ["", "### Coaching (team)", "", "| Team | " + " | ".join(coach.columns) + " |", "|---|" + "---|" * len(coach.columns)]
for t, r in coach.sort_values("total", ascending=False).iterrows():
    L.append(f"| {t} | " + " | ".join(f"{v:+.2f}" for v in r.values) + " |")
L += ["", "### Bucket totals (league)", ""]
for b, v in cr.groupby(["side", "bucket"])["credit"].sum().items():
    L.append(f"- {b[0]} / {b[1]}: {v:+.1f}")
Path(f"reports/credit_report_{season}.md").write_text("\n".join(L) + "\n")
print("\n".join(L[:12]))

# ---------------------------------------------------------------- 4. edge-case audit
A = [f"# Edge-case audit: {season}", "",
     "Random sample of unusual plays (fixed seed). Credits are in the player's own team's win probability.", ""]
evk = ev.set_index(key)
crk = cr.set_index(key).sort_index()
mv = pd.read_parquet(BUILD / f"runner_moves_{season}.parquet")
stretch = mv[mv.is_pa_result & mv.is_batter & mv.is_out & mv.event_type.isin(["single", "double", "triple"])]
thrown_home = mv[mv.is_pa_result & ~mv.is_batter & mv.is_out & mv.out_base.eq("4B") & mv.event_type.isin(["single", "double", "sac_fly"])]
cases = {
    "Batter thrown out stretching a hit": ev.merge(stretch[["game_pk", "at_bat_index"]].drop_duplicates()),
    "Runner thrown out at home on a hit / sac fly": ev.merge(thrown_home[["game_pk", "at_bat_index"]].drop_duplicates()),
}
for et in ["field_error", "grounded_into_double_play", "strikeout_double_play", "sac_bunt", "intent_walk",
           "catcher_interf", "fielders_choice", "triple_play", "stolen_base_home", "caught_stealing_home",
           "pickoff_error_1b", "pickoff_caught_stealing_2b", "passed_ball", "wild_pitch", "balk",
           "defensive_indiff", "other_out", "truncated_pa"]:
    cases[et] = ev[ev.event_type.eq(et)]
cases["Outfield catch with catch probability under 30%"] = ev[(ev.catch_prob < 0.3) & (ev.cp_out == 1)]
cases["Outfield drop with catch probability over 90%"] = ev[(ev.catch_prob > 0.9) & (ev.cp_out == 0)]
for title, df in cases.items():
    df = df[df.kind.eq("pa")] if title.startswith(("Batter", "Runner")) else df
    if df.empty:
        continue
    A += [f"## {title} ({len(df):,} plays)", ""]
    for r in df.sample(min(len(df), 6 if len(df) < 50 else 10), random_state=7).itertuples(index=False):
        k = (r.game_pk, r.at_bat_index, r.play_index, r.kind)
        c = crk.loc[[k]] if k in crk.index else pd.DataFrame()
        hdr = (f"**{r.inning}{'T' if r.half == 'top' else 'B'}, {r.outs_before} out, {r.batting_team} vs {r.fielding_team}** "
               f"- {r.description} (change {r.d_we_bat:+.3f} for the offense")
        if r.kind == "pa" and r.estimated_ba_using_speedangle == r.estimated_ba_using_speedangle and r.estimated_ba_using_speedangle is not None:
            hdr += f"; xBA {r.estimated_ba_using_speedangle:.3f}"
        if r.kind == "pa" and r.catch_prob == r.catch_prob and r.catch_prob is not None:
            hdr += f"; catch prob {r.catch_prob:.2f}"
        A.append(hdr + ")")
        for x in c.itertuples():
            who = f"{x.team} coaching" if pd.isna(x.player_id) else nm(x.player_id)
            A.append(f"  - {who} ({x.role}, {x.bucket}): {x.credit:+.4f}")
        A.append("")
Path(f"reports/audit_{season}.md").write_text("\n".join(A) + "\n")
print(f"audit: {sum(1 for l in A if l.startswith('**'))} plays")
