"""Build the master play tables for a season from the raw pulls.

Outputs (data/build/):
  events_{season}.parquet       one row per win-probability-changing event:
                                - kind 'pa': every plate appearance (result + batted ball)
                                - kind 'mid': every event between pitches that moves a
                                  runner (SB, CS, WP, PB, pickoff, balk, error, ...)
  runner_moves_{season}.parquet one row per runner movement, with fielding credits
  we_lookup_{season}.parquet    MLB win probability by game state

Win probability: MLB's model (Savant `home_win_exp`) is a fixed function of
(inning, half, outs, bases, balls, strikes, home - away score). We rebuild it as a
lookup so every state, including states between pitches, has a value.

Telescoping: a 'mid' event's delta is measured at the count when it happened. A 'pa'
row's delta is (next PA start - this PA start - sum of this PA's mid deltas), so pitch
-by-pitch count changes stay with the batter and pitcher. Each game's deltas sum to the
final result (1/0) minus the opening value.
"""
import gzip
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from winprob import RunExp, WinProb  # noqa: E402

season = sys.argv[1]
RAW = Path(sys.argv[2] if len(sys.argv) > 2 else "data/raw")
OUT = Path(sys.argv[3] if len(sys.argv) > 3 else "data/build")
OUT.mkdir(parents=True, exist_ok=True)
BASES = {"1B": 1, "2B": 2, "3B": 3}

# ---------------------------------------------------------------- Savant pitches
p = pd.read_parquet(RAW / f"savant_pitches_{season}.parquet")
we = WinProb.build(p)
we.to_parquet(OUT / f"we_lookup_{season}.parquet", index=False)
WP = WinProb(we)
fallbacks = WP.fallbacks
re_tab = RunExp.build(p)
re_tab.to_parquet(OUT / f"re_lookup_{season}.parquet", index=False)
RE = RunExp(re_tab)


def mask(st):
    return sum(1 << (b - 1) for b, rid in st["bases"].items() if rid)


def state_we(st, balls=0, strikes=0):
    """Home win probability for a tracked state; 3 outs = start of the next half-inning."""
    return WP.state(st["inning"], st["half"], st["outs"], mask(st), st["home"], st["away"], balls, strikes)


def state_re(st, balls=0, strikes=0):
    """Context-neutral (run expectancy) value of a tracked state; 3 outs = half over."""
    return RE.state(st["inning"], st["half"], st["outs"], mask(st), st["home"], st["away"], balls, strikes)


def num(v):
    return None if v is None or (isinstance(v, float) and np.isnan(v)) or v is pd.NA else v


FLD = [f"fielder_{i}" for i in range(2, 10)]
BB = ["bb_type", "launch_speed", "launch_angle", "hc_x", "hc_y", "hit_location", "hit_distance_sc",
      "estimated_ba_using_speedangle", "estimated_woba_using_speedangle",
      "if_fielding_alignment", "of_fielding_alignment", "events", "des"]
fielders = p.set_index(["game_pk", "at_bat_number", "pitch_number"])[FLD].to_dict("index")
first = p.sort_values("pitch_number").groupby(["game_pk", "at_bat_number"]).first()
sv_state = first[["outs_when_up", "on_1b", "on_2b", "on_3b", "home_score", "away_score"]].to_dict("index")
bb = p[p["events"].notna()].set_index(["game_pk", "at_bat_number"])[BB].to_dict("index")
del p, first

cp = pd.read_parquet(RAW / f"of_catch_prob_{season}.parquet")
CP_COLS = {"player_id": "cp_player", "pos": "cp_pos", "catch_rate": "catch_prob", "out": "cp_out",
           "stars": "cp_stars", "distance": "cp_distance", "opportunity_time": "cp_time",
           "wall": "cp_wall", "back": "cp_back"}
cp = cp.set_index("play_id")[list(CP_COLS)].rename(columns=CP_COLS).to_dict("index")

# ---------------------------------------------------------------- walk the game feeds
events, moves, checks = [], [], Counter()


def fielders_at(gpk, abn, pitch_no):
    fl = fielders.get((gpk, abn, max(pitch_no, 1))) or fielders.get((gpk, abn, pitch_no + 1)) or {}
    return {f"f{i}": num(fl.get(f"fielder_{i}")) for i in range(2, 10)}


with gzip.open(RAW / f"feeds_{season}.jsonl.gz", "rt") as fh:
    for line in fh:
        g = json.loads(line)
        gpk, teams = g["game_pk"], g["teams"]
        plays = [pl for pl in g["plays"] if pl.get("about", {}).get("isComplete", True)]
        st = None
        for n_play, pl in enumerate(plays):
            ab = pl["about"]
            half, inning = ab["halfInning"], ab["inning"]
            if st is None or (st["inning"], st["half"]) != (inning, half):
                h, a = (st["home"], st["away"]) if st else (0, 0)
                st = {"inning": inning, "half": half, "outs": 0, "bases": {1: None, 2: None, 3: None},
                      "home": h, "away": a}
            abn = pl["atBatIndex"] + 1
            evs = {e["index"]: e for e in pl["playEvents"]}
            pitch_idx = [i for i, e in sorted(evs.items()) if e.get("isPitch")]
            final_pitch = pitch_idx[-1] if pitch_idx else None
            pitch_no = {}
            n = 0
            for i in sorted(evs):
                n += bool(evs[i].get("isPitch"))
                pitch_no[i] = n
            by_idx = defaultdict(list)
            for r in pl.get("runners", []):
                by_idx[r["details"].get("playIndex", final_pitch)].append(r)
            batter, pitcher = pl["matchup"]["batter"]["id"], pl["matchup"]["pitcher"]["id"]
            team = {"batting_team": teams["home" if half == "bottom" else "away"]["abbreviation"],
                    "fielding_team": teams["away" if half == "bottom" else "home"]["abbreviation"]}

            # automatic runner placed before the PA: set up state, no credit
            for idx, rs in list(by_idx.items()):
                if all(r["details"].get("eventType") == "runner_placed" for r in rs):
                    for r in rs:
                        st["bases"][BASES[r["movement"]["end"]]] = r["details"]["runner"]["id"]
                    del by_idx[idx]

            # the PA result is the event where the batter himself moves (reaches or is out);
            # covers automatic IBBs and pitch-clock strikeouts with no final pitch
            batter_idx = [i for i, rs in by_idx.items()
                          if any(r["details"]["runner"]["id"] == batter and r["movement"]["start"] is None for r in rs)]
            pa_idx = min(batter_idx) if batter_idx else None

            def substitute(e):
                """Pinch runner swaps, and the extra-innings automatic runner; no credit for either."""
                et = e.get("details", {}).get("eventType")
                if et == "runner_placed" and e.get("player"):
                    desc = e["details"].get("description", "")
                    base = 1 if "1st" in desc else 3 if "3rd" in desc else 2
                    st["bases"][base] = e["player"]["id"]
                    return
                if et == "offensive_substitution" and e.get("replacedPlayer"):
                    old, new = e["replacedPlayer"]["id"], e["player"]["id"]
                    for b in (1, 2, 3):
                        if st["bases"][b] == old:
                            st["bases"][b] = new

            first_pitch = pitch_idx[0] if pitch_idx else None
            # substitutions before anything else happens in this PA
            first_action = min([i for i in by_idx] + [first_pitch if first_pitch is not None else 10 ** 6])
            for i in sorted(evs):
                if i < first_action:
                    substitute(evs[i])

            def check_state():
                sv = sv_state.get((gpk, abn))
                if not sv:
                    return
                theirs = [None if pd.isna(sv[c]) else int(sv[c]) for c in ("on_1b", "on_2b", "on_3b")]
                if len([x for x in theirs if x]) != len({x for x in theirs if x}):
                    checks["savant_duplicate_runner"] += 1  # Savant lists one runner on two bases
                    return
                checks["pa_checked"] += 1
                checks["bases_match"] += [st["bases"][b] for b in (1, 2, 3)] == theirs
                checks["outs_match"] += st["outs"] == sv["outs_when_up"]
                checks["score_match"] += (st["home"], st["away"]) == (sv["home_score"], sv["away_score"])

            pa_start = state_we(st)
            pa_start_re = state_re(st)
            re_mid_sum = 0.0
            pa_state = {"outs_before": st["outs"], "on_1b": st["bases"][1], "on_2b": st["bases"][2],
                        "on_3b": st["bases"][3], "home_before": st["home"], "away_before": st["away"]}
            mid_sum = 0.0
            res_snap = None
            checked = False
            for idx in sorted(set(by_idx) | set(evs)):
                if first_pitch is not None and idx >= first_pitch and not checked:
                    check_state()  # state as the first pitch is thrown
                    checked = True
                if idx >= first_action:
                    substitute(evs.get(idx, {}))
                if idx not in by_idx:
                    continue
                rs = by_idx[idx]
                is_pa = idx == pa_idx
                ev = evs.get(idx, {})
                if is_pa:  # state the result is judged from (after any earlier mid-PA events)
                    res_snap = {"r_outs": st["outs"], "r_on_1b": st["bases"][1], "r_on_2b": st["bases"][2],
                                "r_on_3b": st["bases"][3], "r_home": st["home"], "r_away": st["away"],
                                "we_res": state_we(st), "re_res": state_re(st)}
                if not is_pa:
                    cnt = ev.get("count", {})
                    balls, strikes = cnt.get("balls", 0), cnt.get("strikes", 0)
                    if ev.get("isPitch"):  # count shown is after the pitch; use the count before it
                        prev = [i for i in pitch_idx if i < idx]
                        c0 = evs[prev[-1]].get("count", {}) if prev else {}
                        balls, strikes = c0.get("balls", 0), c0.get("strikes", 0)
                    before = state_we(st, balls, strikes)
                    before_re = state_re(st, balls, strikes)
                    snap = {"outs_before": st["outs"], "on_1b": st["bases"][1], "on_2b": st["bases"][2],
                            "on_3b": st["bases"][3], "home_before": st["home"], "away_before": st["away"]}
                # apply each runner's final outcome for this event at once, so the
                # order runners are listed in can't overwrite someone who already moved
                final = {}
                for r in rs:
                    rid, m = r["details"]["runner"]["id"], r["movement"]
                    out = final.get(rid, {}).get("out", False) or m["isOut"]
                    final[rid] = {"out": out, "end": m["end"]}
                for rid in final:
                    for bb_ in (1, 2, 3):
                        if st["bases"][bb_] == rid:
                            st["bases"][bb_] = None
                for rid, f_ in final.items():
                    if f_["out"]:
                        st["outs"] += 1
                    elif f_["end"] == "score":
                        st["home" if half == "bottom" else "away"] += 1
                    elif f_["end"] in BASES:
                        st["bases"][BASES[f_["end"]]] = rid
                for r in rs:
                    m, d = r["movement"], r["details"]
                    rid = d["runner"]["id"]
                    moves.append({
                        "game_pk": gpk, "at_bat_index": pl["atBatIndex"], "play_index": idx,
                        "is_pa_result": is_pa, "runner_id": rid, "is_batter": rid == batter,
                        "start": m["start"], "end": m["end"], "is_out": m["isOut"], "out_base": m["outBase"],
                        "event_type": d.get("eventType"), "movement_reason": d.get("movementReason"),
                        "is_scoring": d.get("isScoringEvent"), "earned": d.get("earned"),
                        "credits": json.dumps([{"id": c["player"]["id"], "pos": c["position"]["abbreviation"],
                                                "credit": c["credit"]} for c in r.get("credits", [])]),
                    })
                if not is_pa:
                    after = state_we(st, balls, strikes)
                    mid_sum += after - before
                    after_re = state_re(st, balls, strikes)
                    re_mid_sum += after_re - before_re
                    events.append({
                        "game_pk": gpk, "at_bat_index": pl["atBatIndex"], "play_index": idx, "kind": "mid",
                        "event_type": ev.get("details", {}).get("eventType") or rs[0]["details"].get("eventType"),
                        "description": ev.get("details", {}).get("description") or rs[0]["details"].get("event"),
                        "inning": inning, "half": half, **team, **snap,
                        "outs_after": st["outs"], "home_after": st["home"], "away_after": st["away"],
                        "balls": balls, "strikes": strikes, "batter": batter, "pitcher": pitcher,
                        **fielders_at(gpk, abn, pitch_no.get(idx, 0)),
                        "we_before": before, "we_after": after, "d_we_home": after - before,
                        "re_before": before_re, "re_after": after_re, "d_re_home": after_re - before_re,
                        "play_id": ev.get("playId") or ev.get("actionPlayId"),
                    })
                    if st["outs"] >= 3:
                        break  # inning ended between pitches (e.g. caught stealing for out 3)

            # PA row: we_after/d filled once the next PA's start is known
            review = pl.get("reviewDetails") or {}
            res_idx = pa_idx if pa_idx is not None else final_pitch
            fp_play = (evs.get(res_idx, {}).get("playId") or evs.get(final_pitch, {}).get("playId")
                       if res_idx is not None else None)
            b = bb.get((gpk, abn), {})
            truncated = pa_idx is None
            row = {
                "game_pk": gpk, "at_bat_index": pl["atBatIndex"], "play_index": res_idx, "kind": "pa",
                "event_type": "truncated_pa" if truncated else pl["result"].get("eventType"),
                "description": pl["result"].get("description"),
                "inning": inning, "half": half, **team, **pa_state,
                "outs_after": st["outs"], "home_after": st["home"], "away_after": st["away"],
                "balls": 0, "strikes": 0, "batter": batter, "pitcher": pitcher,
                **fielders_at(gpk, abn, pitch_no.get(final_pitch, 0) if final_pitch is not None else 1),
                "we_before": pa_start, "we_after": None, "mid_sum": mid_sum,
                "re_before": pa_start_re, "re_after": state_re(st), "re_mid_sum": re_mid_sum,
                **(res_snap or {"r_outs": st["outs"], "r_on_1b": st["bases"][1], "r_on_2b": st["bases"][2],
                                "r_on_3b": st["bases"][3], "r_home": st["home"], "r_away": st["away"],
                                "we_res": state_we(st), "re_res": state_re(st)}),
                "a_on_1b": st["bases"][1], "a_on_2b": st["bases"][2], "a_on_3b": st["bases"][3],
                "play_id": fp_play,
                "has_review": bool(review), "review_type": review.get("reviewType"),
                "review_overturned": review.get("isOverturned"),
                "review_challenge_team": review.get("challengeTeamId"),
                **{c: num(b.get(c)) for c in BB},
                **{v: None for v in CP_COLS.values()},
            }
            if not truncated and fp_play in cp:
                row.update(cp[fp_play])
            if n_play == len(plays) - 1:
                row["we_after"] = 1.0 if st["home"] > st["away"] else 0.0 if st["home"] < st["away"] else 0.5
            events.append(row)

ev = pd.DataFrame(events).sort_values(["game_pk", "at_bat_index", "kind", "play_index"],
                                      key=lambda s: s.map({"mid": 0, "pa": 1}) if s.name == "kind" else s)
ev = ev.reset_index(drop=True)
pa = ev["kind"].eq("pa")
nxt = ev[pa].groupby("game_pk")["we_before"].shift(-1)
ev.loc[pa, "we_after"] = ev.loc[pa, "we_after"].fillna(nxt)
ev.loc[pa, "d_we_home"] = ev.loc[pa, "we_after"] - ev.loc[pa, "we_before"] - ev.loc[pa, "mid_sum"]
ev["d_we_bat"] = np.where(ev["half"].eq("bottom"), ev["d_we_home"], -ev["d_we_home"])
ev.loc[pa, "d_re_home"] = ev.loc[pa, "re_after"] - ev.loc[pa, "re_before"] - ev.loc[pa, "re_mid_sum"]
ev["d_re_bat"] = np.where(ev["half"].eq("bottom"), ev["d_re_home"], -ev["d_re_home"])
mv = pd.DataFrame(moves)
ev.to_parquet(OUT / f"events_{season}.parquet", index=False)
mv.to_parquet(OUT / f"runner_moves_{season}.parquet", index=False)

# ---------------------------------------------------------------- report
g = ev.groupby("game_pk").agg(d=("d_we_home", "sum"), start=("we_before", "first"),
                               h=("home_after", "last"), a=("away_after", "last"))
g["gap"] = (g.d - (np.where(g.h > g.a, 1.0, np.where(g.h < g.a, 0.0, 0.5)) - g.start)).abs()
# runs version: within each half-inning, deltas telescope from its first state to its last
hh = ev.groupby(["game_pk", "inning", "half"], sort=False)
hp = ev[pa].groupby(["game_pk", "inning", "half"], sort=False)
re_gap = (hh["d_re_home"].sum() - (hp["re_after"].last() - hp["re_before"].first())).abs()
c = checks["pa_checked"]
lines = [
    f"# Play table build: {season}", "",
    f"- Events: {len(ev):,} ({pa.sum():,} plate appearances, {(~pa).sum():,} mid-PA events); runner moves: {len(mv):,}",
    f"- Tracked state vs Savant at the first pitch ({c:,} PAs; {checks['savant_duplicate_runner']:,} skipped where Savant lists one runner on two bases): bases {checks['bases_match'] / c:.2%}, "
    f"outs {checks['outs_match'] / c:.2%}, score {checks['score_match'] / c:.2%}",
    f"- Games whose deltas sum to the final result (within .001): {(g.gap < 1e-3).mean():.2%} of {len(g):,}; max gap {g.gap.max():.4f}",
    f"- Win-prob lookups needing a fallback: {dict(fallbacks)}",
    f"- Runs version: half-innings whose deltas telescope (within 1e-9): {(re_gap < 1e-9).mean():.2%} of {len(re_gap):,}; "
    f"run-expectancy fallbacks: {dict(RE.fallbacks)}",
    f"- PAs with a batted ball: {ev.loc[pa, 'bb_type'].notna().sum():,}; with outfield catch probability: {ev['catch_prob'].notna().sum():,}",
    f"- PAs with a Savant final pitch: {ev.loc[pa, 'events'].notna().mean():.2%}; truncated PAs: {(ev.event_type == 'truncated_pa').sum():,}",
    "", "Mid-PA event types:", "",
] + [f"- {k}: {v:,}" for k, v in ev.loc[~pa, "event_type"].value_counts().items()]
Path(OUT / f"build_report_{season}.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
