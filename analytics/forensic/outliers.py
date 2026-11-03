"""Peer-outlier, growth and threshold-bunching tests.

See docs/playbook/forensic_methods.md section 5.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import median

import numpy as np


def robust_z(values: list[float]) -> list[float]:
    """Robust z-score: (x - median) / (1.4826 * MAD). The 1.4826 factor makes
    the MAD a consistent estimate of the standard deviation for normal data,
    and a few extreme entities cannot inflate it the way they inflate the
    ordinary standard deviation."""
    med = median(values)
    mad = median(abs(v - med) for v in values)
    scale = 1.4826 * mad
    if scale == 0:
        return [0.0 if v == med else math.copysign(math.inf, v - med) for v in values]
    return [(v - med) / scale for v in values]


@dataclass
class PoissonGammaFit:
    alpha: float
    beta: float  # prior on the rate ratio theta ~ Gamma(alpha, rate=beta)


def fit_gamma_prior(observed: list[float], expected: list[float]) -> PoissonGammaFit:
    """Method-of-moments fit of a Gamma prior for rate ratios
    theta_i = (true rate of entity i) / (peer rate), given counts
    y_i ~ Poisson(theta_i * E_i).

    With r_i = y_i / E_i: E[r] = alpha/beta = m and
    Var(r_i) = alpha/beta^2 + m/E_i (between-entity plus Poisson noise).
    So the between-entity variance is var(r) - m * mean(1/E_i), and
    alpha = m^2 / v_between, beta = m / v_between (exposure-weighted)."""
    y = np.asarray(observed, float)
    e = np.asarray(expected, float)
    r = y / e
    w = e / e.sum()
    m = float((w * r).sum())
    v_total = float((w * (r - m) ** 2).sum())
    v_between = max(v_total - m * float((w / e).sum()), 1e-9)
    alpha = m * m / v_between
    beta = m / v_between
    return PoissonGammaFit(alpha, beta)


def shrunk_rate_ratio(observed: float, expected: float, prior: PoissonGammaFit) -> tuple[float, float]:
    """Posterior mean of the rate ratio, and the posterior probability that it
    exceeds 1.5 x peers (normal approximation to the Gamma posterior).

    Shrinkage stops a provider with 3 claims against 0.5 expected from
    outranking one with 3,000 against 1,500: small denominators are pulled
    toward the peer rate."""
    a = prior.alpha + observed
    b = prior.beta + expected
    mean = a / b
    sd = math.sqrt(a) / b
    from .stats import norm_sf

    return mean, norm_sf((1.5 - mean) / sd)


def cusum(series: list[float], target: float, k: float, h: float) -> list[int]:
    """One-sided upper CUSUM: S_t = max(0, S_{t-1} + x_t - target - k).
    Returns the indexes where S_t first crosses h after each reset.
    k is usually half the shift worth detecting (in the series' units) and h
    sets the false-alarm rate (h = 4 to 5 standard deviations is typical)."""
    s = 0.0
    alarms = []
    for t, x in enumerate(series):
        s = max(0.0, s + x - target - k)
        if s > h:
            alarms.append(t)
            s = 0.0
    return alarms


@dataclass
class BunchingResult:
    excess_count: float
    counterfactual: float
    ratio: float  # excess / counterfactual in the bunching window
    missing_above: float


def bunching(values: list[float], threshold: float, bin_width: float, window_below: int = 2, window_above: int = 2, span: int = 20, degree: int = 5) -> BunchingResult:
    """Estimate excess mass just below a threshold (for example a
    micro-purchase limit or an approval level).

    Bin the amounts, fit a polynomial to bin counts over +/- `span` bins
    excluding the window around the threshold, and compare actual with
    fitted counts inside the window (Chetty et al. 2011 style). A ratio well
    above zero means amounts are being steered under the threshold."""
    v = np.asarray(values, float)
    lo = threshold - span * bin_width
    edges = lo + bin_width * np.arange(2 * span + 1)
    counts, _ = np.histogram(v, bins=edges)
    centers = (edges[:-1] + edges[1:]) / 2
    idx = np.arange(len(counts))
    t_bin = span  # first bin at or above the threshold
    in_win = (idx >= t_bin - window_below) & (idx < t_bin + window_above)
    x = (centers - threshold) / bin_width
    coef = np.polyfit(x[~in_win], counts[~in_win], degree)
    fitted = np.polyval(coef, x)
    below = in_win & (idx < t_bin)
    above = in_win & (idx >= t_bin)
    excess = float((counts[below] - fitted[below]).sum())
    cf = float(fitted[below].sum())
    missing = float((fitted[above] - counts[above]).sum())
    return BunchingResult(excess, cf, excess / cf if cf > 0 else math.inf, missing)


def gini(values: list[float]) -> float:
    """Gini coefficient of non-negative values (0 = equal, 1 = all in one)."""
    x = np.sort(np.asarray(values, float))
    n = len(x)
    if n == 0 or x.sum() == 0:
        return 0.0
    cum = np.cumsum(x)
    return float((n + 1 - 2 * (cum / cum[-1]).sum()) / n)
