"""Small statistical helpers with no dependency beyond the standard library.

Kept here so the forensic tests run anywhere (no SciPy needed). Each
function is checked against published values in tests/test_stats.py.
"""
from __future__ import annotations

import math
from statistics import NormalDist

_N = NormalDist()


def norm_sf(z: float) -> float:
    """Upper-tail probability P(Z > z) for a standard normal Z."""
    return 1.0 - _N.cdf(z)


def norm_ppf(p: float) -> float:
    """Inverse of the standard normal CDF."""
    return _N.inv_cdf(p)


def _gammainc_lower_reg(s: float, x: float) -> float:
    """Regularized lower incomplete gamma P(s, x) by series (x < s + 1)."""
    term = 1.0 / s
    total = term
    n = 0
    while abs(term) > abs(total) * 1e-15 and n < 10_000:
        n += 1
        term *= x / (s + n)
        total += term
    return total * math.exp(-x + s * math.log(x) - math.lgamma(s))


def _gammainc_upper_reg(s: float, x: float) -> float:
    """Regularized upper incomplete gamma Q(s, x) by continued fraction (x >= s + 1)."""
    tiny = 1e-300
    b = x + 1.0 - s
    c = 1.0 / tiny
    d = 1.0 / b
    h = d
    for i in range(1, 10_000):
        an = -i * (i - s)
        b += 2.0
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < 1e-15:
            break
    return h * math.exp(-x + s * math.log(x) - math.lgamma(s))


def chi2_sf(x: float, df: int) -> float:
    """Upper-tail probability of a chi-square variable with df degrees of freedom."""
    if x <= 0:
        return 1.0
    s = df / 2.0
    half = x / 2.0
    if half < s + 1.0:
        return 1.0 - _gammainc_lower_reg(s, half)
    return _gammainc_upper_reg(s, half)


def t_ppf_approx(p: float, df: int) -> float:
    """Student t quantile (Cornish-Fisher expansion; accurate to ~1e-3 for df >= 5)."""
    z = norm_ppf(p)
    g1 = (z**3 + z) / 4
    g2 = (5 * z**5 + 16 * z**3 + 3 * z) / 96
    g3 = (3 * z**7 + 19 * z**5 + 17 * z**3 - 15 * z) / 384
    return z + g1 / df + g2 / df**2 + g3 / df**3


def benjamini_hochberg(pvalues: list[float], q: float = 0.05) -> list[bool]:
    """Benjamini-Hochberg step-up procedure. Returns a reject flag per p-value.

    Controls the expected share of false discoveries among the flagged tests
    at level q, which is what we need when one test is run per vendor or per
    provider across thousands of entities.
    """
    m = len(pvalues)
    order = sorted(range(m), key=lambda i: pvalues[i])
    k_max = 0
    for rank, i in enumerate(order, start=1):
        if pvalues[i] <= rank * q / m:
            k_max = rank
    reject = [False] * m
    for rank, i in enumerate(order, start=1):
        if rank <= k_max:
            reject[i] = True
    return reject
