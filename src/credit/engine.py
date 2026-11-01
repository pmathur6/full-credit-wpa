"""Credit engine v1: split every event's win-probability change across players.

Inputs (data/build/): events_, runner_moves_, we_lookup_<season>.parquet
Output: data/credit/credits_<season>.parquet, one row per (event, player or coaching
bucket) with `credit` in that player's own team's win probability.

All arithmetic is in the batting team's win probability ("bat"), then negated for the
defense. Every event: offense credits sum to the event's change, defense credits to
minus it.

Plate appearance, with
  res   = value at the moment of the result (after any earlier mid-PA events)
  act   = value right after the result
  E_evt = expected value given the batter's actual event type at standard advancement
  E_x   = expected value given the batted ball (xBA), league-average defense
  E_cp  = expected value given catch probability from where the fielder stood
  drift = the rest of the PA's change (count movement around mid-PA events)

  Offense: batter  = (E_evt - res) + drift          [batting]
           runners = act - E_evt, split by advancement beyond expected   [baserunning]
  Defense (ball in play): pitcher   = -(E_x - res) - drift   [pitching]
                          coaching  = -(E_cp - E_x)          [positioning; outfield only in v1]
                          fielder   = -(E_evt - E_cp)        [fielding: converting the ball]
                          advancement -(act - E_evt) to fielders who cut down runners,
                          else the responsible fielder (or the pitcher with no ball in play)
  Defense (no ball in play / home run): pitcher gets -(E_evt - res) - drift.
  Coaching: intentional walks (defense), sacrifice bunts (offense gets E_evt - res).
  Catcher's interference: catcher gets the whole defensive share.

Infield ground balls: our own model (src/model/infield.py) gives the probability an
average infield converts the ball, without and with the infield alignment; the alignment's
effect is infield positioning credit to coaching. Falls back to 1 - xBA if the model
output is missing.
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "build"))
from winprob import WinProb  # noqa: E402

season = sys.argv[1]
BUILD = Path(sys.argv[2] if len(sys.argv) > 2 else "data/build")
OUT = Path(sys.argv[3] if len(sys.argv) > 3 else "data/credit")
OUT.mkdir(parents=True, exist_ok=True)

ev = pd.read_parquet(BUILD / f"events_{season}.parquet")
IFP = {}
if (BUILD / f"infield_prob_{season}.parquet").exists():
    _ifp = pd.read_parquet(BUILD / f"infield_prob_{season}.parquet")
    IFP = {(g_, a_): (x_, p_) for g_, a_, x_, p_ in _ifp[["game_pk", "at_bat_index", "p_out_x", "p_out_pos"]].itertuples(index=False)}
# a few events (e.g. a pickoff before any pitch) have no fielder ids: carry them from the
# same team's neighbouring events
FCOLS = [f"f{i}" for i in range(2, 10)]
ev[FCOLS] = ev.groupby(["game_pk", "fielding_team"])[FCOLS].transform(lambda c: c.ffill().bfill())
mv = pd.read_parquet(BUILD / f"runner_moves_{season}.parquet")
WP = WinProb(pd.read_parquet(BUILD / f"we_lookup_{season}.parquet"))

HITS = ["single", "double", "triple", "home_run"]
OUTS = {"field_out", "force_out", "grounded_into_double_play", "double_play", "fielders_choice_out",
        "sac_fly", "sac_fly_double_play", "triple_play", "sac_bunt", "fielders_choice"}
NO_BIP = {"strikeout", "strikeout_double_play", "walk", "intent_walk", "hit_by_pitch",
          "catcher_interf", "truncated_pa"}
POS_NAME = {1: "P", 2: "C", 3: "1B", 4: "2B", 5: "3B", 6: "SS", 7: "LF", 8: "CF", 9: "RF"}


def bat(w, half):
    return w if half == "bottom" else 1.0 - w


def bmask(a, b, c):
    return (a == a and a is not None) * 1 + (b == b and b is not None) * 2 + (c == c and c is not None) * 4


# ---------------------------------------------------------------- PA prep
pa = ev[ev.kind.eq("pa")].copy()
pa["r_mask"] = [bmask(*x) for x in pa[["r_on_1b", "r_on_2b", "r_on_3b"]].itertuples(index=False)]
pa["a_mask"] = [bmask(*x) for x in pa[["a_on_1b", "a_on_2b", "a_on_3b"]].itertuples(index=False)]
pa["runs"] = np.where(pa.half.eq("bottom"), pa.home_after - pa.r_home, pa.away_after - pa.r_away)
pa["outs_add"] = pa.outs_after.clip(upper=3) - pa.r_outs
pa["bbt"] = pa["bb_type"].fillna("")
pa["res_bat"] = [bat(w, h) for w, h in zip(pa.we_res, pa.half)]
pa["act_bat"] = [bat(w, h) for w, h in zip(pa.we_after, pa.half)]
pa["d_bat"] = pa["d_we_bat"]
pa["drift"] = pa["d_bat"] - (pa["act_bat"] - pa["res_bat"])

# outcome distributions: (runs, end bases, outs added) by event, batted-ball type and start state
dist = defaultdict(Counter)
for r in pa[["event_type", "bbt", "r_mask", "r_outs", "runs", "a_mask", "outs_add"]].itertuples(index=False):
    o = (r.runs, r.a_mask, r.outs_add)
    dist[("e", r.event_type, r.bbt, r.r_mask, r.r_outs)][o] += 1
    dist[("e", r.event_type, "*", r.r_mask, r.r_outs)][o] += 1
    if r.event_type in OUTS and r.bbt:
        dist[("out", r.bbt, r.r_mask, r.r_outs)][o] += 1


_cache = {}


def expected(keys, row):
    """Expected batting-team value over the outcome distribution of the first key with data."""
    ck = (tuple(keys), row.inning, row.half, row.r_outs, row.r_home, row.r_away)
    if ck in _cache:
        return _cache[ck]
    _cache[ck] = v = _expected(keys, row)
    return v


def _expected(keys, row):
    for k in keys:
        d = dist.get(k)
        if d and sum(d.values()) >= 5:
            break
    else:
        return None
    n = sum(d.values())
    tot = 0.0
    for (runs, amask, oadd), c in d.items():
        h, a = row.r_home, row.r_away
        if row.half == "bottom":
            h += runs
        else:
            a += runs
        w = WP.state(row.inning, row.half, row.r_outs + oadd, amask, h, a)
        tot += c * bat(w, row.half)
    return tot / n


# hit-type mix given a hit, by batted-ball bucket (exit velocity / launch angle)
bip = pa[pa.bbt.ne("") & pa.event_type.isin(HITS)].copy()
bip["ev5"] = (bip.launch_speed // 5 * 5).fillna(-1)
bip["la5"] = (bip.launch_angle // 5 * 5).fillna(-99)
mix_bucket = bip.groupby(["bbt", "ev5", "la5"])["event_type"].value_counts().unstack(fill_value=0)
mix_type = bip.groupby("bbt")["event_type"].value_counts().unstack(fill_value=0)


def hit_mix(row):
    k = (row.bbt, -1 if pd.isna(row.launch_speed) else row.launch_speed // 5 * 5,
         -99 if pd.isna(row.launch_angle) else row.launch_angle // 5 * 5)
    m = mix_bucket.loc[k] if k in mix_bucket.index and mix_bucket.loc[k].sum() >= 10 else mix_type.loc[row.bbt]
    return (m / m.sum()).to_dict()


# ---------------------------------------------------------------- runner moves per event
mv["end_code"] = np.select([mv.is_out.fillna(False).astype(bool).values, mv.end.eq("score").fillna(False).astype(bool).values], [0, 4],
                           mv.end.map({"1B": 1, "2B": 2, "3B": 3}).fillna(-1)).astype(int)
START = {None: 0, "1B": 1, "2B": 2, "3B": 3}
groups = defaultdict(list)
for m in mv.itertuples(index=False):
    groups[(m.game_pk, m.at_bat_index, m.play_index)].append({
        "runner": int(m.runner_id), "is_batter": bool(m.is_batter), "is_out": bool(m.is_out),
        "start": START.get(m.start, 0), "end": int(m.end_code), "reason": m.movement_reason,
        "credits": json.loads(m.credits)})


def credits_of(g, kinds, where=lambda m: True):
    return [c for m in (g or []) if where(m) for c in m["credits"] if c["credit"] in kinds]


def runner_outcomes(row):
    """Final position of each runner (incl. batter) on the PA result: {runner: [start, end, forced]}.
    end: 0 = out, 1-3 = base, 4 = scored."""
    res = {}
    for b, col in ((1, "r_on_1b"), (2, "r_on_2b"), (3, "r_on_3b")):
        rid = getattr(row, col)
        if rid == rid and rid is not None:
            res[int(rid)] = [b, b, False]
    res[int(row.batter)] = [0, None, False]
    for m in groups.get((row.game_pk, row.at_bat_index, row.play_index), []):
        cur = res.setdefault(m["runner"], [m["start"], m["start"], False])
        if cur[1] != 0:  # once out, stays out
            cur[1] = m["end"]
        if m["is_out"] and m["reason"] == "r_force_out":
            cur[2] = True
    if res[int(row.batter)][1] is None:
        res[int(row.batter)][1] = 0
    return res


# expected end position for each runner by event, start state and his start base
adv = defaultdict(list)
pa_runners = {}
for row in pa.itertuples(index=False):
    if row.event_type == "truncated_pa":
        continue
    ro = runner_outcomes(row)
    pa_runners[(row.game_pk, row.at_bat_index)] = ro
    for rid, (s, e, forced) in ro.items():
        adv[(row.event_type, row.r_mask, row.r_outs, s)].append(e)
adv_mean = {k: float(np.mean(v)) for k, v in adv.items()}

# ---------------------------------------------------------------- allocate
rows = []
stats = Counter()


def add(row, pid, team, side, bucket, role, credit, oae=np.nan):
    rows.append((row.game_pk, row.at_bat_index, row.play_index, row.kind, row.event_type,
                 None if pid is None or pid != pid else int(pid), team, side, bucket, role, float(credit), oae))


def fielder_id(row, pos):
    if pos == 1:
        return row.pitcher
    v = getattr(row, f"f{pos}", None)
    return None if v is None or v != v else int(v)


def spray_angle(x, y):
    return np.degrees(np.arctan2(x - 125.42, 198.27 - y))


# infield zones learned from the data: for each 2-degree spray-angle bin, each infielder's
# share of the ground-ball outs made there; a ground-ball hit through that bin is charged to
# the infielders in those shares (so a fielder's expected hits charged match his outs made)
_gb = pa[(pa.bbt == "ground_ball") & pa.event_type.isin(OUTS) & pa.hc_x.notna()]
_zone_rows = []
for r in _gb[["game_pk", "at_bat_index", "play_index", "hc_x", "hc_y"]].itertuples(index=False):
    c = [x["pos"] for m in groups.get((r.game_pk, r.at_bat_index, r.play_index), []) if m["is_batter"]
         for x in m["credits"] if x["credit"] in ("f_assist", "f_putout") and x["pos"] in ("P", "1B", "2B", "3B", "SS")]
    if c:
        _zone_rows.append((int(spray_angle(r.hc_x, r.hc_y) // 2 * 2), c[0]))
_z = pd.DataFrame(_zone_rows, columns=["bin", "pos"])
_zc = _z.groupby(["bin", "pos"]).size().unstack(fill_value=0)
_zc = _zc[_zc.sum(axis=1) >= 30]
ZONE_SHARE = {b: {pos: n / row.sum() for pos, n in row.items() if n / row.sum() >= 0.05}
              for b, row in _zc.iterrows()}
ZONE_SHARE = {b: {k: v / sum(d.values()) for k, v in d.items()} for b, d in ZONE_SHARE.items()}
ZONE = {b: max(d, key=d.get) for b, d in ZONE_SHARE.items()}
ZBINS = np.array(sorted(ZONE))
POS_NUM = {"P": 1, "1B": 3, "2B": 4, "3B": 5, "SS": 6}


def zone_shares(row):
    """[(fielder id, position, share)] for a ground-ball hit, from the spray-angle bin."""
    if pd.isna(row.hc_x) or pd.isna(row.hc_y):
        return []
    b = int(spray_angle(row.hc_x, row.hc_y) // 2 * 2)
    b = b if b in ZONE_SHARE else int(ZBINS[np.abs(ZBINS - b).argmin()])
    return [(fielder_id(row, POS_NUM[pos]), pos, sh) for pos, sh in ZONE_SHARE[b].items()]



# average catch probability among outfield chances, by batted-ball bucket
_cpb = pa[pa.catch_prob.notna()].assign(ev5=lambda d: d.launch_speed // 5 * 5, la5=lambda d: d.launch_angle // 5 * 5)
CP_B = _cpb.groupby(["ev5", "la5"])["catch_prob"].agg(["mean", "size"])
CP_B = CP_B[CP_B["size"] >= 20]["mean"].to_dict()
CP_LA = _cpb.groupby("la5")["catch_prob"].mean().to_dict()
CP_ALL = float(_cpb.catch_prob.mean())


def cp_avg(row):
    ev5 = None if pd.isna(row.launch_speed) else row.launch_speed // 5 * 5
    la5 = None if pd.isna(row.launch_angle) else row.launch_angle // 5 * 5
    return CP_B.get((ev5, la5), CP_LA.get(la5, CP_ALL))


def responsible_ground(row, g, err):
    """Infielder who owns a ground ball: error > fielder who made the play > zone it went through."""
    if err:
        return err[0]["id"], err[0]["pos"]
    for kind in ({"f_assist"}, {"f_putout"}):
        c = [x for x in credits_of(g, kind) if x["pos"] in ("P", "C", "1B", "2B", "3B", "SS")]
        if c:
            return c[0]["id"], c[0]["pos"]
    sh = zone_shares(row)
    if sh:
        return sh  # a hit: shared by the infielders who own this spray angle
    if row.hit_location == row.hit_location and row.hit_location is not None and int(row.hit_location) <= 6:
        hl = int(row.hit_location)
        return fielder_id(row, hl), POS_NAME[hl]
    return None, None

for row in pa.itertuples(index=False):
    off, deff = row.batting_team, row.fielding_team
    res, act, drift = row.res_bat, row.act_bat, row.drift
    et = row.event_type
    g = groups.get((row.game_pk, row.at_bat_index, row.play_index), [])

    if et == "truncated_pa":
        add(row, row.batter, off, "off", "batting", "batter", row.d_bat)
        add(row, row.pitcher, deff, "def", "pitching", "pitcher", -row.d_bat)
        continue

    e_evt = expected([("e", et, row.bbt, row.r_mask, row.r_outs), ("e", et, "*", row.r_mask, row.r_outs)], row)
    if e_evt is None:
        e_evt = act
        stats["no event baseline"] += 1

    # ---- offense
    base = e_evt - res
    if et in ("sac_bunt",):
        add(row, None, off, "off", "coaching", "bunt call", base)
        add(row, row.batter, off, "off", "batting", "batter", drift)
    else:
        add(row, row.batter, off, "off", "batting", "batter", base + drift)
    R = act - e_evt
    ro = pa_runners.get((row.game_pk, row.at_bat_index), {})
    devs = {}
    for rid, (s, e, forced) in ro.items():
        exp = adv_mean.get((et, row.r_mask, row.r_outs, s))
        devs[rid] = 0.0 if (forced or exp is None) else e - exp
    match = {rid: d for rid, d in devs.items() if d * R > 0}
    if abs(R) > 1e-12:
        if match:
            tot = sum(match.values())
            for rid, d in match.items():
                add(row, rid, off, "off", "baserunning", "batter-runner" if rid == row.batter else "runner", R * d / tot)
        else:
            add(row, row.batter, off, "off", "batting", "batter", R)
            stats["runner residual to batter"] += 1

    # ---- defense
    if et == "catcher_interf":
        add(row, row.f2, deff, "def", "fielding", "C", -(act - res) - drift)
        continue
    if et == "intent_walk":
        add(row, None, deff, "def", "coaching", "intentional walk", -(act - res) - drift)
        continue
    if et in NO_BIP or et == "home_run" or row.bbt == "":
        add(row, row.pitcher, deff, "def", "pitching", "pitcher", -(e_evt - res) - drift)
        adv_def = -R
        cut = credits_of(g, {"f_putout", "f_assist", "f_assist_of"}, lambda m: m["is_out"] and not m["is_batter"])
        if adv_def > 0 and cut and et == "strikeout_double_play":
            for c in cut:
                add(row, c["id"], deff, "def", "fielding", c["pos"], adv_def / len(cut))
        else:
            add(row, row.pitcher, deff, "def", "pitching", "pitcher", adv_def)
        continue

    # ball in play
    xba = row.estimated_ba_using_speedangle
    has_xba = xba == xba and xba is not None
    has_cp = row.catch_prob == row.catch_prob and row.catch_prob is not None
    v_out = expected([("out", row.bbt, row.r_mask, row.r_outs)], row)
    err = credits_of(g, {"f_fielding_error", "f_throwing_error", "f_error_dropped_ball"})
    fid = fpos = None
    of_air_no_cp = False  # kept for the advancement step below

    def v_hit_of(mix):
        return sum(sh * (expected([("e", k, row.bbt, row.r_mask, row.r_outs),
                                   ("e", k, "*", row.r_mask, row.r_outs)], row) or act)
                   for k, sh in mix.items() if sh > 0)

    if has_cp and v_out is not None:
        # outfield catch chance: a hit here means the ball stayed in the park, so no home runs
        # in the hit mix; positioning is measured against the average catch probability for
        # balls hit like this one among outfield chances
        mix = {k: v for k, v in hit_mix(row).items() if k != "home_run"}
        mix = {k: v / sum(mix.values()) for k, v in mix.items()} if sum(mix.values()) > 0 else {"single": 1.0}
        v_hit = v_hit_of(mix)
        pbar = cp_avg(row)
        e_x = pbar * v_out + (1 - pbar) * v_hit
        e_cp = row.catch_prob * v_out + (1 - row.catch_prob) * v_hit
        fid, fpos = (err[0]["id"], err[0]["pos"]) if err else \
            (int(row.cp_player), POS_NAME.get(int(row.cp_pos), "OF") if row.cp_pos == row.cp_pos else "OF")
    elif row.bbt == "ground_ball" and (row.game_pk, row.at_bat_index) in IFP and v_out is not None:
        # infield model: conversion by an average infield, without and with the alignment
        px, ppos = IFP[(row.game_pk, row.at_bat_index)]
        v_hit = v_hit_of(hit_mix(row))
        e_x = px * v_out + (1 - px) * v_hit
        e_cp = ppos * v_out + (1 - ppos) * v_hit
        rg = responsible_ground(row, g, err)
        fid, fpos = (rg, None) if isinstance(rg, list) else rg
    elif row.bbt == "ground_ball" and has_xba and v_out is not None:
        e_x = e_cp = xba * v_hit_of(hit_mix(row)) + (1 - xba) * v_out
        rg = responsible_ground(row, g, err)
        fid, fpos = (rg, None) if isinstance(rg, list) else rg
        stats["ground ball without infield model: 1 - xBA"] += 1
    elif err:
        e_x = e_cp = (xba * v_hit_of(hit_mix(row)) + (1 - xba) * v_out) if (has_xba and v_out is not None) else e_evt
        fid, fpos = err[0]["id"], err[0]["pos"]
    else:
        # air ball with no catch chance tracked (infield liners/popups, uncatchable outfield
        # hits): no fielder is credited in v1, the pitcher keeps the whole play
        e_x = e_cp = e_evt
        stats["air ball without catch chance: all to pitcher"] += 1
    add(row, row.pitcher, deff, "def", "pitching", "pitcher", -(e_x - res) - drift)
    if e_cp != e_x:
        add(row, None, deff, "def", "coaching", "positioning", -(e_cp - e_x))
    conv = -(e_evt - e_cp)
    # outs above expected on this play (leverage-free), for comparison with Savant OAA
    if has_cp:
        p_conv = row.catch_prob
    elif row.bbt == "ground_ball" and (row.game_pk, row.at_bat_index) in IFP:
        p_conv = IFP[(row.game_pk, row.at_bat_index)][1]
    else:
        p_conv = None
    made_out = (row.outs_after if row.outs_after < 3 else 3) - row.r_outs > 0
    oae = np.nan if p_conv is None else (1.0 if made_out else 0.0) - p_conv
    if has_cp and row.cp_out == row.cp_out:
        oae = row.cp_out - row.catch_prob
    if isinstance(fid, list):  # ground-ball hit shared across infielders
        shares = fid
        for sid, spos, w in shares:
            add(row, sid, deff, "def", "fielding", spos, conv * w, oae * w)
        fid, fpos, _ = max(shares, key=lambda t: t[2])
    elif fid is None:
        add(row, row.pitcher, deff, "def", "pitching", "pitcher", conv)
    else:
        add(row, fid, deff, "def", "fielding", fpos, conv, oae)
    adv_def = -R
    if abs(adv_def) > 1e-12:
        if adv_def > 0:
            # runner cut down (not a force) or batter thrown out stretching: fielders on those outs
            def cut_down(m):
                return m["is_out"] and ((not m["is_batter"] and m["reason"] != "r_force_out")
                                        or (m["is_batter"] and et in HITS))
            cut = credits_of(g, {"f_putout", "f_assist", "f_assist_of"}, cut_down)
            if cut:
                for c in cut:
                    add(row, c["id"], deff, "def", "fielding", c["pos"], adv_def / len(cut))
            elif fid is not None and not of_air_no_cp:
                add(row, fid, deff, "def", "fielding", fpos, adv_def)
            else:
                add(row, row.pitcher, deff, "def", "pitching", "pitcher", adv_def)
        else:
            terr = credits_of(g, {"f_throwing_error"})
            if terr:
                add(row, terr[0]["id"], deff, "def", "fielding", terr[0]["pos"], adv_def)
            elif fid is not None and not of_air_no_cp:
                add(row, fid, deff, "def", "fielding", fpos, adv_def)
            else:
                add(row, row.pitcher, deff, "def", "pitching", "pitcher", adv_def)

# ---------------------------------------------------------------- mid-PA events
MID_DEF = {
    "pickoff_caught_stealing": [("pitcher", 1.0)],
    "pickoff": [("pitcher", 1.0)],
    "wild_pitch": [("pitcher", 1.0)], "balk": [("pitcher", 1.0)], "forced_balk": [("pitcher", 1.0)],
    "passed_ball": [("C", 1.0)],
}

# ---- stolen-base attempts: staged split from season skill (Savant)
# baseline league caught-stealing rate for the target base -> + pitcher's effect -> + catcher's
# effect; the rest (attempt at league-average defense, and actual vs expected) splits 50/50
REF = Path("reference")
SHRINK = 5  # attempts of league-average added to each player's season effect
PIT_FX, CAT_FX = {}, {}
if (REF / f"pitcher_running_{season}.csv").exists() and (REF / f"catcher_throwing_{season}.csv").exists():
    pr = pd.read_csv(REF / f"pitcher_running_{season}.csv")
    pr = pr[pr.key_target_base.eq("All")]
    PIT_FX = (pr.n_pitcher_cs_aa / (pr.n_sb + pr.n_cs + SHRINK)).groupby(pr.player_id).sum().to_dict()
    ct = pd.read_csv(REF / f"catcher_throwing_{season}.csv")
    CAT_FX = (ct.caught_stealing_above_average / (ct.sb_attempts + SHRINK)).groupby(ct.player_id).sum().to_dict()
else:
    stats["steal split: no Savant reference, 50/50"] += 1
_att = ev[ev.kind.eq("mid") & ev.event_type.str.match(r"^(stolen_base|caught_stealing)_(2b|3b|home)$", na=False)]
_base = _att.event_type.str.extract(r"_(2b|3b|home)$")[0]
CS_RATE = _att.event_type.str.startswith("caught").groupby(_base).mean().to_dict()
TARGET = {"2b": 2, "3b": 3, "home": 4}


def steal_split(row, g, D):
    """Defense credits for a single-runner steal attempt; None if it can't be staged."""
    if not (PIT_FX or CAT_FX):
        return None
    runners = {m["runner"] for m in g}
    if len(runners) != 1:
        return None
    m0 = g[0]
    base = row.event_type.rsplit("_", 1)[1]
    start, tgt = m0["start"], TARGET[base]
    if start != tgt - 1:
        return None
    bases = {1: row.on_1b, 2: row.on_2b, 3: row.on_3b}
    bases = {b: (None if v != v else v) for b, v in bases.items()}

    def value(safe):
        bs = dict(bases)
        bs[start] = None
        h, a, outs = row.home_before, row.away_before, row.outs_before
        if safe and tgt == 4:
            h, a = (h + 1, a) if row.half == "bottom" else (h, a + 1)
        elif safe:
            bs[tgt] = m0["runner"]
        else:
            outs += 1
        mask = sum(1 << (b - 1) for b, v in bs.items() if v is not None)
        return bat(WP.state(row.inning, row.half, outs, mask, h, a, row.balls, row.strikes), row.half)

    v_sb, v_cs = value(True), value(False)
    before = bat(row.we_before, row.half)
    act = bat(row.we_after, row.half)

    def E(p):
        return p * v_cs + (1 - p) * v_sb

    p0 = CS_RATE.get(base, 0.2)
    p1 = min(max(p0 + PIT_FX.get(row.pitcher, 0.0), 0.01), 0.99)
    cat = None if row.f2 != row.f2 else int(row.f2)
    p2 = min(max(p1 + CAT_FX.get(cat, 0.0), 0.01), 0.99)
    shared = -(E(p0) - before) - (act - E(p2))
    return [(row.pitcher, "pitching", "pitcher", shared / 2 - (E(p1) - E(p0))),
            (cat, "fielding", "C", shared / 2 - (E(p2) - E(p1)))]


for row in ev[ev.kind.eq("mid")].itertuples(index=False):
    off, deff, D = row.batting_team, row.fielding_team, row.d_we_bat
    g = groups.get((row.game_pk, row.at_bat_index, row.play_index), [])
    runners = list(dict.fromkeys(m["runner"] for m in g))
    if runners:
        for rid in runners:
            add(row, rid, off, "off", "baserunning", "runner", D / len(runners))
    else:
        add(row, row.batter, off, "off", "batting", "batter", D)
    et = row.event_type or ""
    key = next((k for k in ("pickoff_caught_stealing", "pickoff_error", "stolen_base", "caught_stealing",
                            "pickoff", "wild_pitch", "passed_ball", "forced_balk", "balk",
                            "defensive_indiff", "error") if et.startswith(k)), "other")
    if key in ("stolen_base", "caught_stealing"):
        split = steal_split(row, g, D)
        if split is None:
            stats["steal attempt split 50/50 (double steal etc.)"] += 1
            split = [(row.pitcher, "pitching", "pitcher", -D / 2),
                     (None if row.f2 != row.f2 else int(row.f2), "fielding", "C", -D / 2)]
        else:
            stats["steal attempt staged"] += 1
        for pid, bucket, role, c in split:
            add(row, pid, deff, "def", bucket, role, c)
    elif key in ("pickoff_error", "error"):
        err = credits_of(g, {"f_fielding_error", "f_throwing_error", "f_error_dropped_ball"})
        if err:
            add(row, err[0]["id"], deff, "def", "fielding", err[0]["pos"], -D)
        else:
            add(row, row.pitcher, deff, "def", "pitching", "pitcher", -D)
    elif key == "defensive_indiff":
        add(row, None, deff, "def", "coaching", "defensive indifference", -D)
    elif key in MID_DEF:
        for who, share in MID_DEF[key]:
            if who == "pitcher":
                add(row, row.pitcher, deff, "def", "pitching", "pitcher", -D * share)
            else:
                add(row, row.f2, deff, "def", "fielding", "C", -D * share)
    else:
        cut = credits_of(g, {"f_putout", "f_assist"})
        if cut:
            for c in cut:
                add(row, c["id"], deff, "def", "fielding", c["pos"], -D / len(cut))
        else:
            add(row, row.pitcher, deff, "def", "pitching", "pitcher", -D)

cr = pd.DataFrame(rows, columns=["game_pk", "at_bat_index", "play_index", "kind", "event_type", "player_id",
                                 "team", "side", "bucket", "role", "credit", "oae"])
cr["player_id"] = cr["player_id"].astype("Int64")
cr.to_parquet(OUT / f"credits_{season}.parquet", index=False)
print(f"credit rows: {len(cr):,}; notes: {dict(stats)}; win-prob fallbacks: {dict(WP.fallbacks)}")
