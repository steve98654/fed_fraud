"""Statistical sampling and estimation of improper payments.

Covers what an agency's improper payment estimate (OMB Circular A-123,
Appendix C) and an OIG overpayment extrapolation rest on, so the team can
check published estimates and design its own samples in Phase 2. See
docs/playbook/forensic_methods.md section 10.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import mean, variance

from .stats import chi2_sf, norm_ppf


@dataclass
class Stratum:
    N: int  # payments in the population stratum
    sample_improper: list[float]  # improper dollars found in each sampled payment
    sample_paid: list[float] | None = None  # dollars paid on each sampled payment
    X: float | None = None  # total dollars paid in the stratum (known from the ledger)


@dataclass
class Estimate:
    total: float
    se: float
    lower: float
    upper: float
    rate: float | None = None
    rate_se: float | None = None
    rate_lower: float | None = None
    rate_upper: float | None = None


def stratified_total(strata: list[Stratum], confidence: float = 0.90) -> Estimate:
    """Expansion (mean-per-unit) estimator of total improper dollars.

        Y_hat = sum_h N_h * ybar_h
        Var   = sum_h N_h^2 * (1 - n_h/N_h) * s_h^2 / n_h

    If every stratum supplies X (dollars paid), also returns the improper
    payment rate Y_hat / X with its standard error. Confidence limits are
    two-sided normal limits at `confidence` (HHS-OIG overpayment
    extrapolations use the lower limit of a two-sided 90% interval)."""
    z = norm_ppf(0.5 + confidence / 2)
    tot = 0.0
    var = 0.0
    for s in strata:
        n = len(s.sample_improper)
        ybar = mean(s.sample_improper)
        s2 = variance(s.sample_improper) if n > 1 else 0.0
        tot += s.N * ybar
        var += s.N**2 * (1 - n / s.N) * s2 / n
    se = math.sqrt(var)
    est = Estimate(tot, se, tot - z * se, tot + z * se)
    if all(s.X is not None for s in strata):
        X = sum(s.X for s in strata)
        est.rate = tot / X
        est.rate_se = se / X
        est.rate_lower = est.rate - z * est.rate_se
        est.rate_upper = est.rate + z * est.rate_se
    return est


def combined_ratio(strata: list[Stratum], confidence: float = 0.90) -> Estimate:
    """Combined ratio estimator of the improper payment rate,
    R_hat = sum N_h ybar_h / sum N_h xbar_h, with the Taylor-linearized
    variance computed on residuals d = y - R_hat * x. More precise than the
    expansion estimator when improper dollars scale with payment size.
    Requires sample_paid in every stratum; if X is known the total is
    R_hat * X."""
    z = norm_ppf(0.5 + confidence / 2)
    num = sum(s.N * mean(s.sample_improper) for s in strata)
    den = sum(s.N * mean(s.sample_paid) for s in strata)
    r = num / den
    var = 0.0
    for s in strata:
        n = len(s.sample_improper)
        d = [y - r * x for y, x in zip(s.sample_improper, s.sample_paid)]
        s2 = variance(d) if n > 1 else 0.0
        var += s.N**2 * (1 - n / s.N) * s2 / n
    r_se = math.sqrt(var) / den
    X = sum(s.X for s in strata) if all(s.X is not None for s in strata) else den
    total = r * X
    return Estimate(total, r_se * X, (r - z * r_se) * X, (r + z * r_se) * X, r, r_se, r - z * r_se, r + z * r_se)


def neyman_allocation(N: list[int], S: list[float], n: int) -> list[int]:
    """Neyman allocation n_h proportional to N_h * S_h (S_h = expected standard
    deviation of improper dollars in stratum h), at least 2 per stratum."""
    w = [a * b for a, b in zip(N, S)]
    tw = sum(w)
    alloc = [max(2, round(n * x / tw)) for x in w]
    return [min(a, Nh) for a, Nh in zip(alloc, N)]


def sample_size_proportion(p: float, margin: float, confidence: float = 0.95, N: int | None = None) -> int:
    """Simple random sample size to estimate an error rate p within +/- margin,
    with finite population correction when N is given."""
    z = norm_ppf(0.5 + confidence / 2)
    n0 = z * z * p * (1 - p) / margin**2
    if N:
        n0 = n0 / (1 + (n0 - 1) / N)
    return math.ceil(n0)


def poisson_upper(k: int, confidence: float) -> float:
    """Upper confidence limit for a Poisson mean after observing k events
    (the 'upper error limit factor' used in monetary unit sampling):
    chi2_{confidence}(2k + 2) / 2."""
    df = 2 * k + 2
    lo, hi = 0.0, 10.0 * (k + 5)
    for _ in range(200):
        mid = (lo + hi) / 2
        if chi2_sf(mid, df) > 1 - confidence:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 4


def mus_upper_error_limit(book_value: float, n: int, taintings: list[float], confidence: float = 0.95) -> float:
    """Stringer bound for monetary unit (dollar unit) sampling.

    book_value: total dollars in the population; n: sampled dollar units;
    taintings: misstatement / book value for each sampled item found in
    error (0 < t <= 1). UEL = (BV/n) * [UF(0) + sum_i (UF(i) - UF(i-1)) * t_(i)],
    taintings in descending order. Use when errors are rare, where the
    normal-theory intervals above are unreliable."""
    interval = book_value / n
    t = sorted(taintings, reverse=True)
    bound = poisson_upper(0, confidence)
    for i, ti in enumerate(t, start=1):
        bound += (poisson_upper(i, confidence) - poisson_upper(i - 1, confidence)) * ti
    return interval * bound


def mus_sample_size(book_value: float, tolerable: float, confidence: float = 0.95, expected_errors: int = 0) -> int:
    """Sample size so that, if no more than `expected_errors` full-taint errors
    are found, the upper error limit stays below `tolerable` dollars."""
    return math.ceil(book_value * poisson_upper(expected_errors, confidence) / tolerable)
