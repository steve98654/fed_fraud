"""Combining signals into a calibrated score and measuring screen quality.

See docs/playbook/forensic_methods.md section 12. Weights come from the
case library (known charged or settled entities); nothing here invents a
base rate.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


def likelihood_ratio(hits_in_cases: int, n_cases: int, hits_in_population: int, n_population: int, smoothing: float = 0.5) -> float:
    """LR+ of a binary signal: P(signal | known case) / P(signal | population),
    with additive smoothing so a signal never seen among cases does not get
    a ratio of zero."""
    p1 = (hits_in_cases + smoothing) / (n_cases + 2 * smoothing)
    p0 = (hits_in_population + smoothing) / (n_population + 2 * smoothing)
    return p1 / p0


def posterior_probability(prior: float, lrs: list[float]) -> float:
    """Posterior odds = prior odds x product of LRs (naive Bayes). Signals
    must be roughly independent given fraud status; correlated signals
    (shared address and shared phone) are grouped and only the strongest
    of each group is multiplied in."""
    log_odds = math.log(prior / (1 - prior)) + sum(math.log(x) for x in lrs)
    return 1 / (1 + math.exp(-log_odds))


def lift_at(scores: list[float], labels: list[bool], top_share: float) -> float:
    """Release-bar metric: share of known cases in the top `top_share` of
    scores divided by their share in the whole population."""
    n = len(scores)
    k = max(1, int(round(n * top_share)))
    order = sorted(range(n), key=lambda i: scores[i], reverse=True)[:k]
    base = sum(labels) / n
    top = sum(labels[i] for i in order) / k
    return top / base if base else math.nan


def precision_at_k(scores: list[float], labels: list[bool], k: int) -> float:
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return sum(labels[i] for i in order) / k


def average_precision(scores: list[float], labels: list[bool]) -> float:
    """Area under the precision-recall curve (step interpolation); a better
    summary than ROC AUC when known cases are rare."""
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    hits = 0
    total = 0.0
    for rank, i in enumerate(order, start=1):
        if labels[i]:
            hits += 1
            total += hits / rank
    return total / max(1, sum(labels))


@dataclass
class TwoSignalDecision:
    lead: bool
    reason: str


def two_signal_rule(fired: dict[str, bool], groups: dict[str, str]) -> TwoSignalDecision:
    """Methodology section 4: a lead needs at least two signals from
    DIFFERENT independence groups (e.g. 'network' and 'billing'). Two
    signals from one group count once."""
    gs = {groups[s] for s, on in fired.items() if on}
    if len(gs) >= 2:
        return TwoSignalDecision(True, "independent signals from groups: " + ", ".join(sorted(gs)))
    if gs:
        return TwoSignalDecision(False, "one signal group only; question for review")
    return TwoSignalDecision(False, "no signals")
