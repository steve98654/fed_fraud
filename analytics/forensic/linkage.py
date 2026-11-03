"""Probabilistic record linkage (Fellegi-Sunter) for the entity spine.

Each candidate pair of records (from blocking: same ZIP, same phone, same
name token, ...) is compared field by field to give a binary agreement
vector gamma. Fellegi and Sunter (1969) show the optimal decision rule ranks
pairs by the log-likelihood ratio

    W = sum_k [ gamma_k * log2(m_k / u_k) + (1 - gamma_k) * log2((1 - m_k) / (1 - u_k)) ]

where m_k = P(field k agrees | same entity) and u_k = P(agrees | different
entities). m and u are estimated without labels by EM (Winkler 1988) and
checked against the 500 hand-labeled pairs required by methodology section 2.
See docs/playbook/forensic_methods.md section 7.
"""
from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass
class FSModel:
    fields: list[str]
    m: list[float]
    u: list[float]
    p: float  # share of candidate pairs that are true matches

    def weight(self, gamma: list[int]) -> float:
        w = 0.0
        for g, m, u in zip(gamma, self.m, self.u):
            w += math.log2(m / u) if g else math.log2((1 - m) / (1 - u))
        return w

    def match_probability(self, gamma: list[int]) -> float:
        """Posterior probability the pair is a match (uses the fitted p)."""
        lr = 2 ** self.weight(gamma)
        odds = lr * self.p / (1 - self.p)
        return odds / (1 + odds)


def fit_em(fields: list[str], gammas: list[list[int]], iters: int = 200, tol: float = 1e-8) -> FSModel:
    """EM for the two-class latent model with conditional independence of
    fields given match status."""
    k = len(fields)
    m = [0.9] * k
    u = [0.1] * k
    p = 0.1
    eps = 1e-6
    for _ in range(iters):
        # E-step
        g_m = []
        for g in gammas:
            lm = p
            lu = 1 - p
            for j in range(k):
                lm *= m[j] if g[j] else 1 - m[j]
                lu *= u[j] if g[j] else 1 - u[j]
            g_m.append(lm / (lm + lu))
        # M-step
        sm = sum(g_m)
        su = len(gammas) - sm
        new_m = [min(max(sum(w for w, g in zip(g_m, gammas) if g[j]) / sm, eps), 1 - eps) for j in range(k)]
        new_u = [min(max(sum(1 - w for w, g in zip(g_m, gammas) if g[j]) / su, eps), 1 - eps) for j in range(k)]
        new_p = sm / len(gammas)
        delta = max(abs(a - b) for a, b in zip(new_m + new_u + [new_p], m + u + [p]))
        m, u, p = new_m, new_u, new_p
        if delta < tol:
            break
    return FSModel(fields, m, u, p)


def thresholds_for_precision(scored: list[tuple[float, bool]], target_precision: float = 0.95) -> float:
    """Lowest weight threshold whose labeled precision meets the target.
    `scored` is (weight, is_true_match) for hand-labeled pairs. Pairs between
    this threshold and a lower review threshold go to clerical review."""
    best = math.inf
    for t, _ in sorted(scored, reverse=True):
        above = [y for w, y in scored if w >= t]
        if above and sum(above) / len(above) >= target_precision:
            best = t
    return best


def jaro_winkler(s1: str, s2: str, p: float = 0.1) -> float:
    """Jaro-Winkler similarity, the usual name comparator (agree if >= 0.92)."""
    if s1 == s2:
        return 1.0
    l1, l2 = len(s1), len(s2)
    if not l1 or not l2:
        return 0.0
    dist = max(l1, l2) // 2 - 1
    f1 = [False] * l1
    f2 = [False] * l2
    matches = 0
    for i, c in enumerate(s1):
        lo, hi = max(0, i - dist), min(i + dist + 1, l2)
        for j in range(lo, hi):
            if not f2[j] and s2[j] == c:
                f1[i] = f2[j] = True
                matches += 1
                break
    if not matches:
        return 0.0
    t = 0
    j = 0
    for i in range(l1):
        if f1[i]:
            while not f2[j]:
                j += 1
            if s1[i] != s2[j]:
                t += 1
            j += 1
    t /= 2
    jaro = (matches / l1 + matches / l2 + (matches - t) / matches) / 3
    prefix = 0
    for a, b in zip(s1[:4], s2[:4]):
        if a != b:
            break
        prefix += 1
    return jaro + prefix * p * (1 - jaro)
