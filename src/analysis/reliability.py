"""Signal vs noise for each bucket.

1. Split-half: each player's season split into alternating games; correlation of the two
   halves' per-opportunity rates across players, averaged over seasons. Spearman-Brown
   turns it into a full-season reliability.
2. Year to year: correlation of per-opportunity rates for the same players in consecutive
   seasons.
3. Stabilization: the opportunities at which reliability reaches 0.5 (half signal, half
   noise), from the split-half correlation.

Opportunities: batting and baserunning per plate appearance, pitching per batter faced,
fielding per game in the field. Fielding is also shown leverage-free (outs above expected
per chance) to show how much the game situation adds noise.

Usage: python src/analysis/reliability.py <credit dir> [season ...]
Writes reports/reliability.md
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

CREDIT = Path(sys.argv[1] if len(sys.argv) > 1 else "data/credit")
seasons = sys.argv[2:] or sorted(f.stem.split("_")[1] for f in CREDIT.glob("credits_*.parquet"))

MIN_HALF = {"batting": 150, "baserunning": 150, "pitching": 150, "fielding": 30, "fielding (outs above expected)": 30}
MIN_SEASON = {k: 2 * v for k, v in MIN_HALF.items()}
UNIT = {"batting": "PA", "baserunning": "PA", "pitching": "batters faced",
        "fielding": "games in the field", "fielding (outs above expected)": "games in the field"}


def player_tables(season):
    cr = pd.read_parquet(CREDIT / f"credits_{season}.parquet")
    cr = cr[cr.player_id.notna()].copy()
    cr["player_id"] = cr.player_id.astype(int)
    # alternate each player's games: 1st, 3rd, 5th... vs 2nd, 4th, 6th...
    out = {}

    def halves(df, opp_df, value_col="credit"):
        games = opp_df[["player_id", "game_pk"]].drop_duplicates().sort_values(["player_id", "game_pk"])
        games["half"] = games.groupby("player_id").cumcount() % 2
        v = df.merge(games, on=["player_id", "game_pk"], how="inner").groupby(["player_id", "half"])[value_col].sum()
        o = opp_df.merge(games, on=["player_id", "game_pk"]).groupby(["player_id", "half"]).size()
        t = pd.concat([v.rename("value"), o.rename("opp")], axis=1).fillna({"value": 0}).dropna(subset=["opp"])
        return t

    pa = cr[(cr.kind == "pa") & (cr.role == "batter")][["player_id", "game_pk", "at_bat_index"]].drop_duplicates()
    bf = cr[(cr.kind == "pa") & (cr.role == "pitcher")][["player_id", "game_pk", "at_bat_index"]].drop_duplicates()
    fg = cr[cr.bucket == "fielding"][["player_id", "game_pk"]].drop_duplicates()
    out["batting"] = halves(cr[cr.bucket == "batting"], pa)
    out["baserunning"] = halves(cr[cr.bucket == "baserunning"], pa)
    out["pitching"] = halves(cr[cr.bucket == "pitching"], bf)
    out["fielding"] = halves(cr[cr.bucket == "fielding"], fg)
    out["fielding (outs above expected)"] = halves(cr[(cr.bucket == "fielding") & cr.oae.notna()], fg, "oae")
    for grp, roles in (("outfield", ("LF", "CF", "RF")), ("infield", ("1B", "2B", "3B", "SS"))):
        out[f"  {grp} (outs above expected)"] = halves(
            cr[(cr.bucket == "fielding") & cr.oae.notna() & cr.role.isin(roles)], fg, "oae")
    # team coaching: alternate each team's games
    co = cr.iloc[0:0]
    coach = pd.read_parquet(CREDIT / f"credits_{season}.parquet")
    coach = coach[coach.bucket == "coaching"]
    tg = coach[["team", "game_pk"]].drop_duplicates().sort_values(["team", "game_pk"])
    tg["half"] = tg.groupby("team").cumcount() % 2
    out["coaching (team)"] = coach.merge(tg, on=["team", "game_pk"]).groupby(["team", "half"])["credit"].sum() \
        .rename("value").to_frame().assign(opp=1)
    return out


tables = {s: player_tables(s) for s in seasons}
buckets = ["batting", "baserunning", "pitching", "fielding", "fielding (outs above expected)",
           "  outfield (outs above expected)", "  infield (outs above expected)", "coaching (team)"]
for k in ("  outfield (outs above expected)", "  infield (outs above expected)"):
    MIN_HALF[k], MIN_SEASON[k], UNIT[k] = 30, 60, "games in the field"
rows = []
for b in buckets:
    sh, n_sh, opp_half = [], [], []
    for s in seasons:
        t = tables[s][b].reset_index()
        idx = t.columns[0]
        w = t.pivot(index=idx, columns="half", values=["value", "opp"]).dropna()
        if b != "coaching (team)":
            w = w[(w[("opp", 0)] >= MIN_HALF[b]) & (w[("opp", 1)] >= MIN_HALF[b])]
            r0, r1 = w[("value", 0)] / w[("opp", 0)], w[("value", 1)] / w[("opp", 1)]
            opp_half.append(w[[("opp", 0), ("opp", 1)]].mean().mean())
        else:
            r0, r1 = w[("value", 0)], w[("value", 1)]
        if len(w) >= 10:
            sh.append(np.corrcoef(r0, r1)[0, 1])
            n_sh.append(len(w))
    r_half = float(np.mean(sh)) if sh else np.nan
    r_full = 2 * r_half / (1 + r_half) if r_half == r_half else np.nan
    # year to year
    yy, n_yy = [], []
    for a, c in zip(seasons, seasons[1:]):
        def season_rate(s):
            t = tables[s][b].reset_index()
            idx = t.columns[0]
            g = t.groupby(idx)[["value", "opp"]].sum()
            if b != "coaching (team)":
                g = g[g.opp >= MIN_SEASON[b]]
                return g.value / g.opp
            return g.value
        j = pd.concat([season_rate(a).rename("a"), season_rate(c).rename("c")], axis=1, join="inner").dropna()
        if len(j) >= 10:
            yy.append(np.corrcoef(j.a, j.c)[0, 1])
            n_yy.append(len(j))
    r_yy = float(np.mean(yy)) if yy else np.nan
    stab = (np.mean(opp_half) * (1 - r_half) / r_half) if (opp_half and r_half and r_half > 0) else np.nan
    rows.append({"bucket": b, "split_half": r_half, "full_season": r_full, "year_to_year": r_yy,
                 "players_split": int(np.mean(n_sh)) if n_sh else 0, "players_yy": int(np.mean(n_yy)) if n_yy else 0,
                 "stabilizes_at": stab, "unit": UNIT.get(b, "season (teams)"),
                 "by_season": ", ".join(f"{s} {r:.2f}" for s, r in zip(seasons, sh)) if len(sh) == len(seasons) else ""})

R = pd.DataFrame(rows)
L = ["# Signal vs noise by bucket", "",
     f"Seasons: {', '.join(seasons)}. Split-half = alternating games within a season, averaged over seasons. "
     "Full-season reliability = Spearman-Brown of the split-half. Year to year = same players, consecutive seasons. "
     "Stabilizes at = opportunities where reliability reaches 0.5.", "",
     "| Bucket | Split-half r | Full-season reliability | Year-to-year r | Stabilizes at | Players (split / y-to-y) |",
     "|---|---|---|---|---|---|"]
for r in R.itertuples():
    stab = "-" if r.bucket.startswith("coaching") or r.stabilizes_at != r.stabilizes_at else f"~{r.stabilizes_at:,.0f} {r.unit}"
    L.append(f"| {r.bucket} | {r.split_half:.2f} | {r.full_season:.2f} | {r.year_to_year:.2f} | {stab} | "
             f"{r.players_split} / {r.players_yy} |")
L += ["", "Split-half by season:", ""] + [f"- {r.bucket}: {r.by_season}" for r in R.itertuples() if r.by_season]
L += ["", "Notes:", "",
      "- Our buckets are wins, weighted by game situation. A big hit in a close late game counts far more "
      "than the same hit in a blowout, and those moments are scattered, so win-based numbers are much noisier "
      "than context-neutral stats. That's expected for any WPA-style measure: it records what happened and "
      "how much it mattered, not a player's true talent.",
      "- Fielding, leverage-free (outs above expected) vs win-weighted shows how much the game situation adds noise.",
      "- Outfield uses Savant's catch probability from each fielder's actual starting spot; infield uses our "
      "model, which can't see where the fielder stood. That gap is the main reason infield is less reliable.",
      "- Coaching's split-half is partly built in: infield positioning is calibrated to each player's season "
      "Savant OAA and spread evenly across his chances, so both halves carry the same share. Year to year is the "
      "fairer read on whether positioning persists.",
      "", f"Minimums: each half at least {MIN_HALF['batting']} PA / {MIN_HALF['pitching']} batters faced / "
      f"{MIN_HALF['fielding']} games in the field; year to year at least double that in both seasons. "
      "Coaching is team-level (30 teams)."]
Path("reports").mkdir(exist_ok=True)
Path("reports/reliability.md").write_text("\n".join(L) + "\n")
print("\n".join(L))
