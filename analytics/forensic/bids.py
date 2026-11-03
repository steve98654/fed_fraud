"""Collusion (bid-rigging) screens on sealed-bid tender data.

Built for state DOT bid tabulations (DOT-1) and any agency that publishes
all bids, not only winners. Screens follow Imhof, Karagok and Rutz,
"Screening for Bid Rigging: Does It Work?" (Journal of Competition Law &
Economics, 2018) and Huber and Imhof (2019). See
docs/playbook/forensic_methods.md section 6.
"""
from __future__ import annotations

import random
from dataclasses import dataclass
from statistics import mean, pstdev


@dataclass
class TenderScreens:
    n_bids: int
    cv: float  # coefficient of variation of all bids
    spread: float  # (max - min) / min
    rd: float  # relative distance: (second - first) / sd of losing bids
    skew: float
    kurtosis: float  # excess kurtosis
    cover_ratio: float  # mean losing bid / winning bid


def tender_screens(bids: list[float]) -> TenderScreens:
    """Distribution screens for one tender. Collusive tenders tend to show a
    LOW coefficient of variation and spread (cover bids clustered near the
    agreed price) and a HIGH relative distance (a gap between the designated
    winner and tightly grouped cover bids)."""
    b = sorted(bids)
    n = len(b)
    if n < 3:
        raise ValueError("need at least three bids")
    m = mean(b)
    sd = pstdev(b)
    losing = b[1:]
    sd_l = pstdev(losing)
    rd = (b[1] - b[0]) / sd_l if sd_l > 0 else float("inf")
    if sd > 0:
        skew = sum((x - m) ** 3 for x in b) / n / sd**3
        kurt = sum((x - m) ** 4 for x in b) / n / sd**4 - 3
    else:
        skew = kurt = 0.0
    return TenderScreens(n, sd / m, (b[-1] - b[0]) / b[0], rd, skew, kurt, mean(losing) / b[0])


def rotation_test(winners: list[str], n_perm: int = 5000, seed: int = 7) -> tuple[float, float]:
    """Test whether a sequence of winners among a stable group of firms takes
    turns more evenly than chance. Statistic: number of times the same firm
    wins two consecutive tenders. Bid rotation produces FEWER repeats than a
    random ordering of the same wins. Returns (observed repeats, one-sided
    permutation p-value for 'too few repeats')."""
    def repeats(seq):
        return sum(1 for a, b in zip(seq, seq[1:]) if a == b)

    obs = repeats(winners)
    rng = random.Random(seed)
    seq = list(winners)
    le = 0
    for _ in range(n_perm):
        rng.shuffle(seq)
        if repeats(seq) <= obs:
            le += 1
    return obs, (le + 1) / (n_perm + 1)


def win_share_matrix(tenders: list[dict[str, float]]) -> dict[str, dict[str, int]]:
    """For each pair of firms that bid together, how often each one won.
    Pairs that meet often but where each firm only ever wins in its 'own'
    territory or turn are a market-allocation signal for review."""
    out: dict[str, dict[str, int]] = {}
    for t in tenders:
        winner = min(t, key=t.get)
        for a in t:
            for b in t:
                if a != b:
                    out.setdefault(a, {}).setdefault(b, 0)
                    if winner == a:
                        out[a][b] += 1
    return out
