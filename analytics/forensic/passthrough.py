"""Grants to states: screens for federal money that states administer
(Medicaid, unemployment insurance, SNAP, TANF, child care, education).

The federal government sees these programs as a state-level total; fraud
happens one claimant, provider or subrecipient further down. These screens
work on what is public or obtainable without new law: state-level program
statistics, Single Audit findings (Federal Audit Clearinghouse) and
subaward reports (FFATA / USAspending). See docs/research/grants_to_states.md.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

from .outliers import fit_gamma_prior, robust_z, shrunk_rate_ratio


@dataclass
class StateMetric:
    state: str
    observed: float  # e.g. improper or fraud-flagged dollars, overpayment count
    exposure: float  # matching denominator: benefits paid, claims, caseload


def state_outliers(rows: list[StateMetric], z_cut: float = 2.5) -> list[tuple[str, float, float, float]]:
    """States whose rate is unusual against the other states, two ways:
    a robust z on the raw rate and an empirical-Bayes rate ratio that pulls
    small states toward the national rate. Returns (state, raw rate,
    robust z, shrunk ratio) for states flagged by either, largest z first.
    A high rate can mean more fraud or better detection: states that look
    hardest find the most, so read a flag as "ask how this state measures"
    before "this state has a problem". The shrinkage treats `observed` as a
    count; for dollars, pass counts (claims, cases) or dollars in units of
    the typical claim."""
    rows = [r for r in rows if r.exposure > 0]
    rates = [r.observed / r.exposure for r in rows]
    zs = robust_z(rates)
    total_obs = sum(r.observed for r in rows)
    total_exp = sum(r.exposure for r in rows)
    national = total_obs / total_exp if total_exp else 0.0
    expected = [r.exposure * national for r in rows]
    prior = fit_gamma_prior([r.observed for r in rows], expected)
    out = []
    for r, rate, z, e in zip(rows, rates, zs, expected):
        ratio, _ = shrunk_rate_ratio(r.observed, e, prior)
        if abs(z) >= z_cut or ratio >= 1.5:
            out.append((r.state, rate, z, ratio))
    return sorted(out, key=lambda t: abs(t[2]), reverse=True)


@dataclass
class AuditFinding:
    auditee_uei: str
    year: int
    program: str  # Assistance Listing number, e.g. 93.778 (Medicaid)
    material_weakness: bool
    questioned_costs: float
    repeat: bool


def repeat_finding_entities(findings: list[AuditFinding], min_years: int = 3) -> dict[str, dict]:
    """Auditees with material weaknesses or questioned costs in at least
    `min_years` distinct years: the subrecipients a state keeps funding
    despite its own auditors' findings."""
    by: dict[str, list[AuditFinding]] = defaultdict(list)
    for f in findings:
        if f.material_weakness or f.questioned_costs > 0:
            by[f.auditee_uei].append(f)
    out = {}
    for uei, fs in by.items():
        years = {f.year for f in fs}
        if len(years) >= min_years:
            out[uei] = {
                "years": sorted(years),
                "questioned_costs": sum(f.questioned_costs for f in fs),
                "programs": sorted({f.program for f in fs}),
                "marked_repeat": sum(f.repeat for f in fs),
            }
    return out


def subaward_concentration(subawards: list[tuple[str, str, float]]) -> dict[str, tuple[float, str, float]]:
    """For each prime (state agency) the Herfindahl index of its subaward
    dollars and its largest subrecipient's share. `subawards` is a list of
    (prime_uei, subrecipient_uei, amount). One subrecipient taking most of
    a pass-through program, especially a new one, is the shape of the
    Feeding Our Future case in the Child Nutrition programs."""
    by: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for prime, sub, amt in subawards:
        by[prime][sub] += amt
    out = {}
    for prime, shares in by.items():
        tot = sum(shares.values())
        if tot <= 0:
            continue
        top, top_amt = max(shares.items(), key=lambda kv: kv[1])
        out[prime] = (sum((v / tot) ** 2 for v in shares.values()), top, top_amt / tot)
    return out


def growth_without_caseload(spend: dict[int, float], caseload: dict[int, float], ratio: float = 1.5) -> list[int]:
    """Years where program spending grew at least `ratio` times faster than
    caseload (spend growth / caseload growth). Spending that outruns the
    people served is the aggregate trace of billing for services not
    delivered, as in several state Medicaid housing and autism programs."""
    years = sorted(set(spend) & set(caseload))
    out = []
    for a, b in zip(years, years[1:]):
        if spend[a] > 0 and caseload[a] > 0 and caseload[b] > 0:
            g_s = spend[b] / spend[a]
            g_c = caseload[b] / caseload[a]
            if g_s > 1 and g_s / g_c >= ratio:
                out.append(b)
    return out
