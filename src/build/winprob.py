"""MLB win probability as a lookup by game state.

MLB's model (Savant `home_win_exp`) is a fixed function of
(inning, half, outs, bases, balls, strikes, home score - away score). We rebuild it
from a season's pitches so any state, including states between pitches, has a value.
"""
from collections import Counter

import pandas as pd

KEY = ["inning", "half", "outs_when_up", "bases", "balls", "strikes", "diff"]


class WinProb:
    def __init__(self, table: pd.DataFrame):
        self.exact = {tuple(r[:-1]): r[-1] for r in table[KEY + ["home_win_exp"]].itertuples(index=False)}
        z = table[(table.balls == 0) & (table.strikes == 0)]
        self.at00 = z.set_index(["inning", "half", "outs_when_up", "bases", "diff"])["home_win_exp"].to_dict()
        self.max_inning = int(table["inning"].max())
        self.fallbacks = Counter()

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
        self.fallbacks["unresolved (decided game)"] += 1
        return 1.0 if diff > 0 else 0.0 if diff < 0 else 0.5

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
