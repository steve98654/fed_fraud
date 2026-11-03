"""Digit and number tests (Benford's law and related tests).

Formulas follow Nigrini, *Benford's Law: Applications for Forensic
Accounting, Auditing, and Fraud Detection* (Wiley, 2012). See
docs/playbook/forensic_methods.md section 3 for when each test applies.
"""
from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field

from .stats import chi2_sf, norm_sf

# Nigrini (2012) conformity ranges for the mean absolute deviation (MAD).
MAD_THRESHOLDS = {
    "first": [(0.006, "close"), (0.012, "acceptable"), (0.015, "marginal")],
    "second": [(0.008, "close"), (0.010, "acceptable"), (0.012, "marginal")],
    "first_two": [(0.0012, "close"), (0.0018, "acceptable"), (0.0022, "marginal")],
}


def benford_expected(test: str) -> dict[int, float]:
    """Expected digit proportions under Benford's law."""
    if test == "first":
        return {d: math.log10(1 + 1 / d) for d in range(1, 10)}
    if test == "first_two":
        return {d: math.log10(1 + 1 / d) for d in range(10, 100)}
    if test == "second":
        return {
            d: sum(math.log10(1 + 1 / (10 * k + d)) for k in range(1, 10)) for d in range(10)
        }
    if test == "last_two":
        return {d: 0.01 for d in range(100)}
    raise ValueError(test)


def _digits_of(x: float) -> str:
    """Significant digits of |x| as a string, without leading zeros."""
    s = f"{abs(x):.10e}"  # d.dddddddddde+XX
    mantissa = s.split("e")[0].replace(".", "")
    return mantissa


def leading_digits(values, test: str) -> list[int]:
    """Extract the digit(s) each test looks at. Values below 10 are dropped
    for first-two and second-digit tests, as Nigrini recommends."""
    out = []
    for v in values:
        if v is None or v == 0 or (isinstance(v, float) and math.isnan(v)):
            continue
        a = abs(v)
        if test == "first":
            out.append(int(_digits_of(a)[0]))
        elif test in ("first_two", "second"):
            if a < 10:
                continue
            dd = int(_digits_of(a)[:2])
            out.append(dd if test == "first_two" else dd % 10)
        elif test == "last_two":
            cents = round(a * 100)
            if cents % 100 == 0:  # whole dollars: use the last two dollar digits
                whole = int(round(a))
                if whole < 100:
                    continue
                out.append(whole % 100)
            else:
                out.append(cents % 100)
        else:
            raise ValueError(test)
    return out


@dataclass
class DigitTestResult:
    test: str
    n: int
    observed: dict[int, float]
    expected: dict[int, float]
    chi2: float
    df: int
    p_value: float
    mad: float
    conformity: str
    z: dict[int, float] = field(default_factory=dict)

    def spikes(self, z_crit: float = 1.96) -> list[int]:
        """Digits whose observed share is significantly above expectation."""
        return [d for d, zz in self.z.items() if zz > z_crit and self.observed[d] > self.expected[d]]


def digit_test(values, test: str = "first") -> DigitTestResult:
    """Run a digit test: chi-square, MAD with Nigrini's conformity band and a
    z-statistic per digit (with continuity correction)."""
    digits = leading_digits(values, test)
    n = len(digits)
    if n == 0:
        raise ValueError("no usable values")
    exp = benford_expected(test)
    counts = Counter(digits)
    obs = {d: counts.get(d, 0) / n for d in exp}
    chi2 = sum(n * (obs[d] - p) ** 2 / p for d, p in exp.items())
    df = len(exp) - 1
    mad = sum(abs(obs[d] - p) for d, p in exp.items()) / len(exp)
    conformity = "nonconformity"
    for limit, label in MAD_THRESHOLDS.get(test, []):
        if mad <= limit:
            conformity = label
            break
    if test == "last_two":
        conformity = "n/a (use chi-square)"
    z = {}
    for d, p in exp.items():
        se = math.sqrt(p * (1 - p) / n)
        num = abs(obs[d] - p) - 1 / (2 * n)
        z[d] = max(num, 0.0) / se
    return DigitTestResult(test, n, obs, exp, chi2, df, chi2_sf(chi2, df), mad, conformity, z)


def summation_test(values) -> dict[int, float]:
    """Nigrini's summation test: share of the total dollar amount by first-two
    digits. Under Benford each of the 90 groups holds ~1/90 of the total;
    a large share in one group points to a few very large (possibly duplicated
    or inflated) amounts."""
    sums: dict[int, float] = {d: 0.0 for d in range(10, 100)}
    total = 0.0
    for v in values:
        if v is None or abs(v) < 10:
            continue
        d = int(_digits_of(abs(v))[:2])
        sums[d] += abs(v)
        total += abs(v)
    return {d: s / total for d, s in sums.items()} if total else sums


def round_number_share(values, unit: float = 1000.0) -> float:
    """Share of non-zero amounts that are exact multiples of `unit`."""
    vals = [abs(v) for v in values if v]
    if not vals:
        return 0.0
    hits = sum(1 for v in vals if abs(v / unit - round(v / unit)) < 1e-9)
    return hits / len(vals)


def round_number_test(values, unit: float, expected_share: float) -> tuple[float, float]:
    """One-sided binomial (normal approximation) test that round amounts occur
    more often than `expected_share`, the share in a clean reference
    population. Returns (observed share, p-value)."""
    vals = [v for v in values if v]
    n = len(vals)
    share = round_number_share(vals, unit)
    se = math.sqrt(expected_share * (1 - expected_share) / n)
    z = (share - expected_share) / se if se else 0.0
    return share, norm_sf(z)


def number_duplication(values, top: int = 20) -> list[tuple[float, int]]:
    """Nigrini's number duplication test: the most frequently repeated exact
    amounts. Repeated odd amounts (not prices on a schedule) are what to read."""
    return Counter(round(v, 2) for v in values if v).most_common(top)


def relative_size_factor(amounts_by_group: dict[str, list[float]]) -> dict[str, float]:
    """Largest amount divided by the second largest, per group (vendor,
    cardholder). Ratios far above peers suggest an error or an inflated
    one-off payment."""
    out = {}
    for g, vals in amounts_by_group.items():
        s = sorted((abs(v) for v in vals if v), reverse=True)
        if len(s) >= 2 and s[1] > 0:
            out[g] = s[0] / s[1]
    return out
