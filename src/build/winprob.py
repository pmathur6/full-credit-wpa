"""MLB win probability as a lookup by game state.

MLB's model (Savant `home_win_exp`) is a fixed function of
(inning, half, outs, bases, balls, strikes, home score - away score). We rebuild it
from a season's pitches so any state, including states between pitches, has a value.
"""
from collections import Counter, defaultdict
from math import exp, log

import pandas as pd

KEY = ["inning", "half", "outs_when_up", "bases", "balls", "strikes", "diff"]


class WinProb:
    def __init__(self, table: pd.DataFrame):
        self.exact = {tuple(r[:-1]): r[-1] for r in table[KEY + ["home_win_exp"]].itertuples(index=False)}
        z = table[(table.balls == 0) & (table.strikes == 0)]
        self.at00 = z.set_index(["inning", "half", "outs_when_up", "bases", "diff"])["home_win_exp"].to_dict()
        self.max_inning = int(table["inning"].max())
        self.fallbacks = Counter()
        # score margin -> value, per state without the margin (for interpolation)
        self.by_diff = defaultdict(dict)
        for k, v in self.exact.items():
            self.by_diff[k[:-1]][k[-1]] = v

    @staticmethod
    def build(pitches: pd.DataFrame) -> pd.DataFrame:
        p = pitches.assign(
            half=lambda d: d["inning_topbot"].map({"Top": "top", "Bot": "bottom"}),
            bases=lambda d: d["on_1b"].notna().astype(int) + 2 * d["on_2b"].notna() + 4 * d["on_3b"].notna(),
            diff=lambda d: d["home_score"] - d["away_score"])
        return p.groupby(KEY, as_index=False)["home_win_exp"].first()

    def lookup(self, inning, half, outs, bases, balls, strikes, diff):
        balls, strikes = min(balls, 3), min(strikes, 2)
        k = (inning, half, outs, bases, balls, strikes, diff)
        if k in self.exact:
            return self.exact[k]
        for inn in dict.fromkeys((inning, min(inning, self.max_inning), 10 if inning > 10 else inning)):
            for dd in dict.fromkeys((diff, max(min(diff, 10), -10))):
                if (inn, half, outs, bases, balls, strikes, dd) in self.exact:
                    self.fallbacks["clamped inning/score"] += 1
                    return self.exact[(inn, half, outs, bases, balls, strikes, dd)]
                if (inn, half, outs, bases, dd) in self.at00:
                    self.fallbacks["count 0-0"] += 1
                    return self.at00[(inn, half, outs, bases, dd)]
        # Rare lopsided states (e.g. down 5 in the 12th): interpolate across score
        # margins for the same inning/outs/bases/count, in log-odds space.
        for inn in dict.fromkeys((inning, min(inning, self.max_inning), 10 if inning > 10 else inning, 9)):
            for b, s in ((balls, strikes), (0, 0)):
                v = self._interp(self.by_diff.get((inn, half, outs, bases, b, s)), diff)
                if v is not None:
                    self.fallbacks["interpolated score margin"] += 1
                    return v
        self.fallbacks["unresolved (decided game)"] += 1
        return 1.0 if diff > 0 else 0.0 if diff < 0 else 0.5

    @staticmethod
    def _interp(pts, diff):
        if not pts or len(pts) < 2:
            return None
        lo = lambda p: log(min(max(p, 0.0005), 0.9995) / (1 - min(max(p, 0.0005), 0.9995)))
        ds = sorted(pts)
        below = [d for d in ds if d < diff]
        above = [d for d in ds if d > diff]
        if below and above:
            a, b = below[-1], above[0]
        elif below:
            a, b = ds[-2], ds[-1]
        else:
            a, b = ds[0], ds[1]
        la, lb = lo(pts[a]), lo(pts[b])
        x = la + (lb - la) * (diff - a) / (b - a)
        return round(1 / (1 + exp(-x)), 4)

    def state(self, inning, half, outs, bases, home, away, balls=0, strikes=0):
        """Home win probability; `bases` is a 3-bit mask; 3 outs = start of the next half-inning."""
        diff = home - away
        if outs >= 3:
            inn, h = (inning, "bottom") if half == "top" else (inning + 1, "top")
            if h == "bottom" and inn >= 9 and diff > 0:
                return 1.0
            if h == "top" and inn >= 10 and diff != 0:
                return 1.0 if diff > 0 else 0.0
            return self.lookup(inn, h, 0, 2 if inn >= 10 else 0, 0, 0, diff)
        if half == "bottom" and inning >= 9 and diff > 0:
            return 1.0  # walk-off: game over
        return self.lookup(inning, half, outs, bases, balls, strikes, diff)
