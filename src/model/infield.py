"""Infield ground-ball conversion model.

For every ground ball, the probability an average infield records an out on the play
(batter or a forced runner), from:
  exit velocity, launch angle, spray angle, batter handedness, batter sprint speed,
  runners on base and outs (force plays), and - in the positioned version only - the
  infield alignment (Standard / Infield shade / Strategic).

Errors count as failed conversions, so an average fielder nets zero over a season.
Predictions are out-of-fold (5-fold, grouped by game) so a play never predicts itself.

Output: data/build/infield_prob_<season>.parquet
  game_pk, at_bat_index, p_out_x (no alignment), p_out_pos (with alignment), out
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import brier_score_loss, roc_auc_score
from sklearn.model_selection import GroupKFold

season = sys.argv[1]
BUILD = Path(sys.argv[2] if len(sys.argv) > 2 else "data/build")
RAW = Path(sys.argv[3] if len(sys.argv) > 3 else "data/raw")
REF = Path("reference")

ev = pd.read_parquet(BUILD / f"events_{season}.parquet")
gb = ev[ev.kind.eq("pa") & ev.bb_type.eq("ground_ball") & ev.hc_x.notna() & ev.launch_speed.notna()].copy()

sv = pd.read_parquet(RAW / f"savant_pitches_{season}.parquet", columns=["game_pk", "at_bat_number", "stand", "events"])
sv = sv[sv.events.notna()].drop_duplicates(["game_pk", "at_bat_number"])
gb = gb.merge(sv[["game_pk", "at_bat_number", "stand"]].assign(at_bat_index=lambda d: d.at_bat_number - 1),
              on=["game_pk", "at_bat_index"], how="left")

speed = pd.Series(dtype=float)
if (REF / f"sprint_speed_{season}.csv").exists():
    ss = pd.read_csv(REF / f"sprint_speed_{season}.csv")
    speed = ss.set_index("player_id")["sprint_speed"]

gb["spray"] = np.degrees(np.arctan2(gb.hc_x - 125.42, 198.27 - gb.hc_y))
gb["stand_r"] = gb.stand.eq("R").astype(float)
gb["pull_spray"] = np.where(gb.stand.eq("L"), -gb.spray, gb.spray)  # negative = pulled
gb["sprint"] = gb.batter.map(speed)
gb["on1"] = gb.r_on_1b.notna().astype(int)
gb["on2"] = gb.r_on_2b.notna().astype(int)
gb["on3"] = gb.r_on_3b.notna().astype(int)
gb["align"] = gb.if_fielding_alignment.map({"Standard": 0, "Infield shade": 1, "Strategic": 2})
gb["out"] = ((gb.outs_after.clip(upper=3) - gb.r_outs) > 0).astype(int)

BASE = ["launch_speed", "launch_angle", "spray", "pull_spray", "stand_r", "sprint", "on1", "on2", "on3", "r_outs"]
BASE = [f for f in BASE if gb[f].notna().any()]  # sprint speed is absent without the reference file
POS = BASE + ["align"]
folds = GroupKFold(n_splits=5)


def oof(features):
    pred = np.zeros(len(gb))
    X, y, groups = gb[features].to_numpy(float), gb["out"].to_numpy(), gb["game_pk"].to_numpy()
    for tr, te in folds.split(X, y, groups):
        m = HistGradientBoostingClassifier(max_iter=400, learning_rate=0.05, max_leaf_nodes=31,
                                           min_samples_leaf=80, l2_regularization=1.0, random_state=7)
        m.fit(X[tr], y[tr])
        pred[te] = m.predict_proba(X[te])[:, 1]
    return pred


gb["p_out_x"] = oof(BASE)
gb["p_out_pos"] = oof(POS)

out = gb[["game_pk", "at_bat_index", "p_out_x", "p_out_pos", "out"]]
out.to_parquet(BUILD / f"infield_prob_{season}.parquet", index=False)

# ---- model report
y = gb["out"]
xba_out = 1 - gb.estimated_ba_using_speedangle
lines = [f"# Infield model: {season}", "",
         f"- Ground balls: {len(gb):,}; converted to an out: {y.mean():.3f}; sprint speed coverage: {gb.sprint.notna().mean():.1%}",
         "", "| Predictor | AUC | Brier | Mean predicted |", "|---|---|---|---|"]
for name, p in (("1 - xBA (old stand-in)", xba_out), ("Model, no alignment", gb.p_out_x), ("Model, with alignment", gb.p_out_pos)):
    ok = p.notna()
    lines.append(f"| {name} | {roc_auc_score(y[ok], p[ok]):.3f} | {brier_score_loss(y[ok], p[ok]):.4f} | {p[ok].mean():.3f} |")
gb["bin"] = pd.cut(gb.p_out_pos, [0, .2, .4, .6, .8, .9, .95, 1.0])
cal = gb.groupby("bin", observed=True).agg(n=("out", "size"), predicted=("p_out_pos", "mean"), actual=("out", "mean"))
lines += ["", "Calibration (with alignment):", "", "| Predicted | n | Mean predicted | Actual |", "|---|---|---|---|"]
lines += [f"| {b} | {r.n:,} | {r.predicted:.3f} | {r.actual:.3f} |" for b, r in cal.iterrows()]
al = gb.groupby("if_fielding_alignment").agg(n=("out", "size"), actual=("out", "mean"),
                                              no_align=("p_out_x", "mean"), with_align=("p_out_pos", "mean"))
lines += ["", "By alignment (positioning effect = with - without):", "",
          "| Alignment | n | Actual | Without alignment | With alignment |", "|---|---|---|---|---|"]
lines += [f"| {a} | {r.n:,} | {r.actual:.3f} | {r.no_align:.3f} | {r.with_align:.3f} |" for a, r in al.iterrows()]
Path("reports").mkdir(exist_ok=True)
Path(f"reports/infield_model_{season}.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
