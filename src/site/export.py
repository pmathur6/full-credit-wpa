"""Export a season's credits to small JSON files for the static site.

Usage: python src/site/export.py <season> <build_dir> <credit_dir> <raw_dir> <out_dir>

Writes <out_dir>/<season>/:
  leaderboard.json        every player with 10+ games, buckets in wins and runs, plus team coaching
  games.json              index of games: id, date, away, home, scores
  players/<id>.json       season summary, fielding by position, game log
  games/<id>.json         every event with its win-probability and run changes and every credit

Numbers are stored as compact arrays with a `cols` header to keep files small.
"""
import json
import time
import sys
from pathlib import Path

import numpy as np
import pandas as pd

season = sys.argv[1]
T0 = time.time()


def tick(msg):
    print(f"[{time.time() - T0:6.1f}s] {msg}", flush=True)


BUILD, CREDIT, RAW, OUT = (Path(a) for a in sys.argv[2:6])
OUT = OUT / season
for d in ("players", "games"):
    (OUT / d).mkdir(parents=True, exist_ok=True)
REF = Path("reference")
MIN_GAMES = 10
BUCKETS = ["batting", "baserunning", "fielding", "pitching"]
POS = {2: "C", 3: "1B", 4: "2B", 5: "3B", 6: "SS", 7: "LF", 8: "CF", 9: "RF"}


def r4(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 4)


def dump(path, obj):
    path.write_text(json.dumps(obj, separators=(",", ":"), ensure_ascii=False))


ev = pd.read_parquet(BUILD / f"events_{season}.parquet")
cw = pd.read_parquet(CREDIT / f"credits_{season}.parquet")
cr = pd.read_parquet(CREDIT / f"credits_runs_{season}.parquet")
names = {}
if (REF / f"players_{season}.csv").exists():
    names = pd.read_csv(REF / f"players_{season}.csv").set_index("player_id")["name"].to_dict()

# ---- games: date, teams, final score
dates = {}
try:
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pull"))
    from common import final_games  # noqa: E402
    dates = {g["game_pk"]: g["date"] for g in final_games(int(season))}
except Exception as e:  # schedule API unreachable: fall back to Savant game dates
    print(f"schedule API unavailable ({e}); using Savant dates")
if not dates or not set(ev.game_pk.unique()) <= set(dates):
    sp = pd.read_parquet(RAW / f"savant_pitches_{season}.parquet", columns=["game_pk", "game_date"]).drop_duplicates("game_pk")
    for g, d in zip(sp.game_pk, sp.game_date):
        dates.setdefault(int(g), str(d)[:10])
pa = ev[ev.kind.eq("pa")]
gm = pa.groupby("game_pk").agg(hs=("home_after", "last"), as_=("away_after", "last"), inn=("inning", "max"))
gm["home"] = ev[ev.half.eq("bottom")].groupby("game_pk")["batting_team"].first()
gm["home"] = gm["home"].fillna(ev[ev.half.eq("top")].groupby("game_pk")["fielding_team"].first())
gm["away"] = ev[ev.half.eq("top")].groupby("game_pk")["batting_team"].first()
gm["date"] = [dates.get(int(g), "") for g in gm.index]
gm = gm.sort_values(["date"]).reset_index()
dump(OUT / "games.json", {"cols": ["id", "date", "away", "home", "away_runs", "home_runs", "innings"],
                          "rows": [[int(r.game_pk), r.date, r.away, r.home, int(r.as_), int(r.hs), int(r.inn)]
                                   for r in gm.itertuples()]})
G = gm.set_index("game_pk")

# ---- one row per (event, player/coaching, bucket, role) with wins and runs side by side
key = ["game_pk", "at_bat_index", "play_index", "kind"]
grp = key + ["player_id", "team", "side", "bucket", "role"]
note = cw.groupby(grp, dropna=False)["note"].agg(lambda s: next((x for x in s if isinstance(x, str) and x != "positioning transfer"), None))
c = (cw.groupby(grp, dropna=False)["credit"].sum().rename("w").to_frame()
     .join(cr.groupby(grp, dropna=False)["credit"].sum().rename("r"), how="outer")
     .join(note).fillna({"w": 0.0, "r": 0.0}).reset_index())
c = c.merge(ev[key + ["pitcher"]], on=key, how="left")

# ---- per player per game
pg = c.dropna(subset=["player_id"]).pivot_table(index=["player_id", "game_pk"], columns="bucket",
                                                values=["w", "r"], aggfunc="sum", fill_value=0)
pg.columns = [f"{b}_{u}" for u, b in pg.columns]
for u in ("w", "r"):
    for b in BUCKETS:
        if f"{b}_{u}" not in pg:
            pg[f"{b}_{u}"] = 0.0
# defense behind a pitcher: other fielders and coaching on the defensive side of his events
d = c[c.side.eq("def") & (c.player_id.isna() | c.player_id.ne(c.pitcher))]
beh = d.groupby(["pitcher", "game_pk"])[["w", "r"]].sum()
beh.index.names = ["player_id", "game_pk"]
pg = pg.join(beh.rename(columns={"w": "behind_w", "r": "behind_r"}), how="left").fillna(0)
# traditional WPA / RE24: batter and pitcher take the whole play
trad = pd.concat([
    pa.groupby(["batter", "game_pk"])[["d_we_bat", "d_re_bat"]].sum().rename_axis(["player_id", "game_pk"]),
    -ev.groupby(["pitcher", "game_pk"])[["d_we_bat", "d_re_bat"]].sum().rename_axis(["player_id", "game_pk"]),
]).groupby(level=[0, 1]).sum().rename(columns={"d_we_bat": "trad_w", "d_re_bat": "trad_r"})
pg = pg.join(trad, how="outer").fillna(0)
pg = pg.join(pa.groupby(["batter", "game_pk"]).size().rename("pa").rename_axis(["player_id", "game_pk"]), how="left")
pg = pg.join(pa.groupby(["pitcher", "game_pk"]).size().rename("bf").rename_axis(["player_id", "game_pk"]), how="left")
pg = pg.fillna({"pa": 0, "bf": 0}).reset_index()
pg["player_id"] = pg.player_id.astype(int)
team_of = c.dropna(subset=["player_id"]).groupby(["player_id", "game_pk"])["team"].first()
team_of.index = team_of.index.set_levels([team_of.index.levels[0].astype(int), team_of.index.levels[1]])
bt = pd.concat([pa[["batter", "game_pk", "batting_team"]].set_axis(["player_id", "game_pk", "team"], axis=1),
                ev[["pitcher", "game_pk", "fielding_team"]].set_axis(["player_id", "game_pk", "team"], axis=1)]
               ).drop_duplicates(["player_id", "game_pk"]).set_index(["player_id", "game_pk"])["team"]
pg["team"] = [team_of.get((p, g), bt.get((p, g))) for p, g in zip(pg.player_id, pg.game_pk)]

# ---- appearances by position (fielding lineup per event)
app = pd.concat([ev[["game_pk", f"f{i}"]].rename(columns={f"f{i}": "pid"}).assign(pos=n) for i, n in POS.items()]
                + [ev[["game_pk", "pitcher"]].rename(columns={"pitcher": "pid"}).assign(pos="P")]).dropna().drop_duplicates()
app["pid"] = app.pid.astype(int)
gp = app.groupby(["pid", "pos"]).size()
games_played = pd.concat([app[["pid", "game_pk"]], pa[["batter", "game_pk"]].rename(columns={"batter": "pid"})]
                         ).drop_duplicates().groupby("pid").size()


# DH: 10+ games batting without playing the field that game
_bat_g = pa[["game_pk", "batter"]].drop_duplicates().rename(columns={"batter": "pid"})
_fld_g = app[app.pos.ne("P")][["game_pk", "pid"]].drop_duplicates()
_dh = _bat_g.merge(_fld_g, how="left", indicator=True).query("_merge == 'left_only'").groupby("pid").size()
DH = set(_dh[_dh >= 10].index.astype(int))


def positions(pid):
    s = gp.get(pid)
    ok = []
    if s is not None:
        s = s.sort_values(ascending=False)
        ok = [p for p, n in s.items() if n >= 10] or [s.index[0]]
    if pid in DH:
        ok.append("DH")
    return "/".join(ok) or "-"


fld_pos = c[c.bucket.eq("fielding")].dropna(subset=["player_id"]).groupby(["player_id", "role"])[["w", "r"]].sum()

# ---- season totals and leaderboard
cols = [f"{b}_{u}" for u in ("w", "r") for b in BUCKETS + ["behind", "trad"]]
tot = pg.groupby("player_id")[cols + ["pa", "bf"]].sum()
tot["team"] = pg.groupby("player_id")["team"].agg(lambda s: "/".join(dict.fromkeys(x for x in s if x)))
tot["g"] = games_played.reindex(tot.index).fillna(0).astype(int)
trad_bat = pa.groupby("batter")[["d_we_bat", "d_re_bat"]].sum()
trad_pit = -ev.groupby("pitcher")[["d_we_bat", "d_re_bat"]].sum()


def name(pid):
    return names.get(int(pid), str(int(pid)))


# ---- WAR scale: the runs view on WAR's footing (replacement level + positional adjustment)
# Runs per win (FanGraphs formula): 9 x league runs per inning x 1.5 + 3.
# Replacement level: 1,000 WAR per season, 570 to position players (per PA), 430 to pitchers (per batter faced).
# Positional adjustment (FanGraphs, runs per full season), pro-rated by defensive PAs at each position;
# DH by PAs in games he batted without fielding.
POS_ADJ = {"C": 12.5, "1B": -12.5, "2B": 2.5, "3B": 2.5, "SS": 7.5, "LF": -7.5, "CF": 2.5, "RF": -7.5}
DH_ADJ = -17.5
n_pa = len(pa)
runs_lg = float(G.hs.sum() + G.as_.sum())
innings_lg = float(ev.loc[ev.kind.eq("pa")].groupby(["game_pk", "inning", "half"]).ngroups)
RPW = 9 * runs_lg / innings_lg * 1.5 + 3
REP_PA = 570 * RPW / n_pa
REP_BF = 430 * RPW / n_pa
team_pa = n_pa / 30  # defensive PAs in a full team season = one full season at a position
def_pa = pd.concat([pa[[f"f{i}"]].rename(columns={f"f{i}": "pid"}).assign(pos=n) for i, n in POS.items()]).dropna()
def_pa = def_pa.assign(pid=def_pa.pid.astype(int)).groupby(["pid", "pos"]).size()
pos_runs = (def_pa * def_pa.index.get_level_values(1).map(POS_ADJ).values / team_pa).groupby(level=0).sum()
_dh_pa = pa.merge(_bat_g.merge(_fld_g, how="left", indicator=True).query("_merge == 'left_only'")[["game_pk", "pid"]],
                  left_on=["game_pk", "batter"], right_on=["game_pk", "pid"]).groupby("batter").size()
pos_runs = pos_runs.add(_dh_pa * DH_ADJ / (team_pa / 9), fill_value=0)
# league adjustment (as FanGraphs): positional runs sum to zero across the league, spread per PA
POS_LG = float(pos_runs.sum()) / n_pa
pos_runs = pos_runs.sub(pa.groupby("batter").size() * POS_LG, fill_value=0)
fld_p = fld_pos.xs("P", level=1)["r"] if "P" in fld_pos.index.get_level_values(1) else pd.Series(dtype=float)
# Like WAR, each component is measured against the league average: our buckets carry small
# league-wide offsets (e.g. runners as a group beat "standard advancement"), so re-center
# batting+baserunning per PA, pitching per batter faced, and fielding per defensive PA (pitchers
# per batter faced). Coaching stays with the team and is not part of any player's WAR scale.
def_pa_tot = def_pa.groupby(level=0).sum()
OFF_MEAN = float((tot.batting_r + tot.baserunning_r).sum()) / n_pa
PIT_MEAN = float(tot.pitching_r.sum()) / n_pa
FLDP_MEAN = float(fld_p.sum()) / n_pa
FLD_MEAN = float(tot.fielding_r.sum() - fld_p.sum()) / float(def_pa_tot.sum())


def war_scale(pid, r):
    """(hitting, pitching) on WAR's scale, in wins."""
    pr = float(pos_runs.get(pid, 0.0))
    fp = float(fld_p.get(pid, 0.0))
    fld = (r.fielding_r - fp) - FLD_MEAN * float(def_pa_tot.get(pid, 0))
    off = r.batting_r + r.baserunning_r - OFF_MEAN * r.pa
    hit = (off + fld + REP_PA * r.pa + pr) / RPW if (r.pa > 0 or r.bf == 0) else 0.0
    pit = (r.pitching_r - PIT_MEAN * r.bf + fp - FLDP_MEAN * r.bf + REP_BF * r.bf) / RPW if r.bf > 0 else 0.0
    return hit, pit, pr


print(f"WAR scale centering per PA: offense {OFF_MEAN:+.4f}, pitching {PIT_MEAN:+.4f}, P fielding {FLDP_MEAN:+.4f}; per defensive PA: fielding {FLD_MEAN:+.5f}")
print(f"WAR scale: {RPW:.2f} runs per win; replacement {REP_PA * 600:.1f} runs per 600 PA, {REP_BF * 700:.1f} per 700 BF")

LB_COLS = ["id", "name", "team", "pos", "g", "pa", "bf",
           "bat_w", "br_w", "fld_w", "pit_w", "tradbat_w", "tradpit_w",
           "bat_r", "br_r", "fld_r", "pit_r", "tradbat_r", "tradpit_r", "warbat", "warpit"]
lb = []
for pid, r in tot.iterrows():
    if r.g < MIN_GAMES:
        continue
    tb = trad_bat.loc[pid].values if pid in trad_bat.index else (0, 0)
    tp = trad_pit.loc[pid].values if pid in trad_pit.index else (0, 0)
    lb.append([int(pid), name(pid), r.team, positions(pid), int(r.g), int(r.pa), int(r.bf),
               *[r4(r[f"{b}_w"]) for b in BUCKETS], r4(tb[0]), r4(tp[0]),
               *[r4(r[f"{b}_r"]) for b in BUCKETS], r4(tb[1]), r4(tp[1]), *[r4(x) for x in war_scale(pid, r)[:2]]])
coach = c[c.bucket.eq("coaching")].pivot_table(index="team", columns="role", values=["w", "r"], aggfunc="sum", fill_value=0)
roles = sorted({b for _, b in coach.columns})
dump(OUT / "leaderboard.json", {
    "season": int(season), "min_games": MIN_GAMES, "cols": LB_COLS, "players": lb,
    "war_scale": {"runs_per_win": round(RPW, 3), "rep_runs_per_600_pa": round(REP_PA * 600, 2),
                  "rep_runs_per_700_bf": round(REP_BF * 700, 2), "pos_adj": POS_ADJ, "dh_adj": DH_ADJ, "league_pos_adj_per_pa": round(-POS_LG, 5),
                  "center": {"offense_per_pa": round(OFF_MEAN, 5), "pitching_per_bf": round(PIT_MEAN, 5),
                             "p_fielding_per_bf": round(FLDP_MEAN, 5), "fielding_per_def_pa": round(FLD_MEAN, 6)}},
    "coaching": {"roles": roles, "cols": ["team"] + [f"{x}_w" for x in roles] + [f"{x}_r" for x in roles],
                 "rows": [[t] + [r4(coach.loc[t, ("w", x)]) for x in roles] + [r4(coach.loc[t, ("r", x)]) for x in roles]
                          for t in coach.index]},
})

tick("leaderboard written")
# ---- player files (every player, so game pages can always link)
LOG_COLS = ["game", "date", "opp", "res", "pa", "bf",
            "bat_w", "br_w", "fld_w", "pit_w", "behind_w", "trad_w",
            "bat_r", "br_r", "fld_r", "pit_r", "behind_r", "trad_r"]


def opp_res(team, g):
    x = G.loc[g]
    home = team == x.home
    us, them = (x.hs, x.as_) if home else (x.as_, x.hs)
    res = "W" if us > them else "L" if us < them else "T"
    return (f"vs {x.away}" if home else f"@ {x.home}"), f"{res} {int(us)}-{int(them)}"


n_players = 0
for pid, df in pg.sort_values(["player_id", "game_pk"]).groupby("player_id"):
    df = df.assign(date=[G.loc[g, "date"] for g in df.game_pk]).sort_values(["date", "game_pk"])
    rows = []
    for r in df.itertuples():
        o, res = opp_res(r.team, r.game_pk) if r.team else ("", "")
        rows.append([int(r.game_pk), r.date, o, res, int(r.pa), int(r.bf),
                     *[r4(getattr(r, f"{b}_w")) for b in BUCKETS], r4(r.behind_w), r4(r.trad_w),
                     *[r4(getattr(r, f"{b}_r")) for b in BUCKETS], r4(r.behind_r), r4(r.trad_r)])
    t = tot.loc[pid]
    fp = {}
    if pid in fld_pos.index.get_level_values(0):
        for role, v in fld_pos.loc[pid].iterrows():
            fp[role] = {"g": int(gp.get((pid, role), 0)), "w": r4(v.w), "r": r4(v.r)}
    tb = trad_bat.loc[pid].values if pid in trad_bat.index else (0, 0)
    tp = trad_pit.loc[pid].values if pid in trad_pit.index else (0, 0)
    dump(OUT / "players" / f"{pid}.json", {
        "id": int(pid), "name": name(pid), "season": int(season), "team": t.team, "pos": positions(pid),
        "g": int(t.g), "pa": int(t.pa), "bf": int(t.bf), "qualified": bool(t.g >= MIN_GAMES),
        "totals": {u: {**{b: r4(t[f"{b}_{u}"]) for b in BUCKETS + ["behind"]},
                       "trad_bat": r4(tb[0 if u == "w" else 1]), "trad_pit": r4(tp[0 if u == "w" else 1])}
                   for u in ("w", "r")},
        "fielding_by_pos": fp,
        "war_scale": dict(zip(("hitting", "pitching", "pos_runs"), (r4(x) for x in war_scale(pid, t)))) | {
            "rep_runs_hit": r4(REP_PA * t.pa), "rep_runs_pit": r4(REP_BF * t.bf), "runs_per_win": round(RPW, 3)},
        "log": {"cols": LOG_COLS, "rows": rows},
    })
    n_players += 1

tick("player files written")
# ---- game files
EV_COLS = ["key", "kind", "type", "inning", "half", "outs", "bases", "away", "home", "balls", "strikes",
           "desc", "batter", "pitcher", "wp_before", "wp_after", "d_w", "d_r"]
CR_COLS = ["player", "team", "bucket", "role", "w", "r", "note"]
ev = ev.sort_values(["game_pk", "at_bat_index", "kind", "play_index"],
                    key=lambda s: s.map({"mid": 0, "pa": 1}) if s.name == "kind" else s)
CR = {}
for x in c.itertuples(index=False):
    pid = None if pd.isna(x.player_id) else int(x.player_id)
    CR.setdefault((x.game_pk, x.at_bat_index, -1 if pd.isna(x.play_index) else x.play_index, x.kind), []).append(
        [pid, x.team, x.bucket, x.role, r4(x.w), r4(x.r), x.note if isinstance(x.note, str) else None])
for g, e in ev.groupby("game_pk", sort=False):
    out, people = [], set()
    for r in e.itertuples():
        cl = CR.get((g, r.at_bat_index, -1 if pd.isna(r.play_index) else r.play_index, r.kind), [])
        people.update(x[0] for x in cl if x[0])
        bases = int(pd.notna(r.on_1b)) + 2 * int(pd.notna(r.on_2b)) + 4 * int(pd.notna(r.on_3b))
        people.update(int(v) for v in (r.batter, r.pitcher) if pd.notna(v))
        out.append([f"{r.at_bat_index}.{int(r.play_index) if pd.notna(r.play_index) else 0}.{r.kind}",
                    r.kind, r.event_type, int(r.inning), r.half, int(r.outs_before), bases,
                    int(r.away_before), int(r.home_before), int(r.balls), int(r.strikes), r.description,
                    int(r.batter) if pd.notna(r.batter) else None, int(r.pitcher) if pd.notna(r.pitcher) else None,
                    r4(r.we_before), r4(r.we_after), r4(r.d_we_bat), r4(r.d_re_bat), cl])
    x = G.loc[g]
    dump(OUT / "games" / f"{g}.json", {
        "id": int(g), "date": x.date, "away": x.away, "home": x.home, "away_runs": int(x.as_),
        "home_runs": int(x.hs), "innings": int(x.inn), "names": {str(p): name(p) for p in sorted(people)},
        "cols": EV_COLS + ["credits"], "credit_cols": CR_COLS, "events": out,
    })

size = sum(f.stat().st_size for f in OUT.rglob("*.json"))
print(f"{season}: {len(lb)} leaderboard players, {n_players} player files, {len(gm)} games, {size / 1e6:.1f} MB")
