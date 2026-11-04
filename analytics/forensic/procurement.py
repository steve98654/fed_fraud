"""Procurement and contract fraud screens on FPDS / USAspending award data.

Covers the three schemes in docs/playbook/procurement_fraud.md:

* bid rigging and weak competition (single-offer awards, incumbent lock-in;
  sealed-bid screens are in bids.py);
* change-order and modification inflation (value growth after award, many
  small modifications, modifications just under approval thresholds);
* false small-business set-aside claims (size over the standard, pass-through
  above the limitations on subcontracting, set-aside winners that share
  owners or addresses with large firms).

Inputs are plain dicts or dataclasses mirroring FPDS fields; field names in
comments are the USAspending contract download column names.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass, field
from statistics import median

from .outliers import robust_z

# FAR 52.219-14 limitations on subcontracting: the most a set-aside prime
# may pay to firms that are not similarly situated, as a share of the
# amount paid to it (supplies exclude cost of materials).
SUBCONTRACT_LIMIT = {"services": 0.50, "supplies": 0.50, "general_construction": 0.85, "specialty_construction": 0.75}


@dataclass
class Award:
    award_id: str  # award_id_piid
    vendor: str  # recipient_uei
    office: str  # awarding_office_code
    naics: str  # naics_code
    base_value: float  # base_and_all_options_value at the first action
    current_value: float  # current_total_value_of_award
    offers: int | None = None  # number_of_offers_received
    competed: bool = True  # extent_competed not in (B, C, G, NDO)
    set_aside: str = ""  # type_of_set_aside (SBA, 8A, HZC, SDVOSBC, WOSB, ...)
    mods: list[float] = field(default_factory=list)  # federal_action_obligation of each modification


# ---------------------------------------------------------------------------
# Competition
# ---------------------------------------------------------------------------
def single_offer_rates(awards: list[Award], min_awards: int = 10) -> dict[str, tuple[float, int]]:
    """Share of competed awards that drew exactly one offer, by contracting
    office. Offices with fewer than `min_awards` competed awards are skipped.
    Persistently high rates point to tailored specifications or a steered
    market; compare within NAICS because some markets are thin by nature."""
    tot: dict[str, int] = defaultdict(int)
    one: dict[str, int] = defaultdict(int)
    for a in awards:
        if a.competed and a.offers is not None:
            tot[a.office] += 1
            one[a.office] += a.offers == 1
    return {o: (one[o] / n, n) for o, n in tot.items() if n >= min_awards}


def incumbent_lock(awards: list[Award], min_awards: int = 5) -> dict[tuple[str, str], float]:
    """Herfindahl index of vendor dollar shares for each (office, NAICS)
    market. 1.0 means one vendor takes everything. High HHI with mostly
    single-offer competitions is the pattern to review."""
    by: dict[tuple[str, str], dict[str, float]] = defaultdict(lambda: defaultdict(float))
    n: dict[tuple[str, str], int] = defaultdict(int)
    for a in awards:
        by[(a.office, a.naics)][a.vendor] += a.current_value
        n[(a.office, a.naics)] += 1
    out = {}
    for k, shares in by.items():
        if n[k] < min_awards:
            continue
        tot = sum(shares.values())
        out[k] = sum((v / tot) ** 2 for v in shares.values()) if tot > 0 else 0.0
    return out


# ---------------------------------------------------------------------------
# Change-order inflation
# ---------------------------------------------------------------------------
def growth_ratio(a: Award) -> float:
    """current_value / base_value. Values above 1 mean the award grew after
    it was competed; the competition no longer priced what is being bought."""
    return a.current_value / a.base_value if a.base_value > 0 else math.inf


def modification_outliers(awards: list[Award], z_cut: float = 3.5, min_peers: int = 8) -> list[tuple[str, float, float]]:
    """Awards whose log growth ratio is a robust-z outlier among awards with
    the same NAICS code. Returns (award_id, growth_ratio, z), largest z
    first. Log scale because growth is multiplicative."""
    by: dict[str, list[Award]] = defaultdict(list)
    for a in awards:
        if a.base_value > 0 and a.current_value > 0:
            by[a.naics].append(a)
    out = []
    for group in by.values():
        if len(group) < min_peers:
            continue
        zs = robust_z([math.log(growth_ratio(a)) for a in group])
        out.extend((a.award_id, growth_ratio(a), z) for a, z in zip(group, zs) if z >= z_cut)
    return sorted(out, key=lambda t: t[2], reverse=True)


def mods_below_threshold(a: Award, threshold: float, band: float = 0.10) -> int:
    """Count of modifications priced within `band` below an approval
    threshold (for example a contracting officer's warrant limit or the
    level that triggers legal or cost-price review). Several of them on one
    award is the modification version of a split purchase."""
    lo = threshold * (1 - band)
    return sum(1 for m in a.mods if lo <= m < threshold)


# ---------------------------------------------------------------------------
# Set-aside eligibility
# ---------------------------------------------------------------------------
@dataclass
class SetAsideCheck:
    vendor: str
    reasons: list[str]


def set_aside_checks(vendor: str, avg_annual_receipts: float | None, employees: int | None,
                     size_standard_receipts: float | None, size_standard_employees: int | None,
                     paid_to_prime: float, paid_to_non_similarly_situated: float, work_type: str,
                     linked_large_firms: int = 0) -> SetAsideCheck:
    """Rule checks for one set-aside prime on one award. Size standards come
    from 13 CFR 121.201 for the award's NAICS code; receipts and employees
    from SAM.gov representations, public filings or the firm's own website.
    `linked_large_firms` is the number of other-than-small firms that share
    an owner, officer, address or bank account with the vendor (network.py),
    the affiliation question under 13 CFR 121.103 and the ostensible
    subcontractor rule. A reason is a question for the contracting officer
    or SBA, not a finding: size is measured at offer, and affiliation needs
    the facts behind the link."""
    reasons = []
    if size_standard_receipts and avg_annual_receipts and avg_annual_receipts > size_standard_receipts:
        reasons.append(f"receipts {avg_annual_receipts:,.0f} above size standard {size_standard_receipts:,.0f}")
    if size_standard_employees and employees and employees > size_standard_employees:
        reasons.append(f"{employees} employees above size standard {size_standard_employees}")
    limit = SUBCONTRACT_LIMIT.get(work_type)
    if limit is not None and paid_to_prime > 0:
        share = paid_to_non_similarly_situated / paid_to_prime
        if share > limit:
            reasons.append(f"passes {share:.0%} to non-similarly-situated firms (limit {limit:.0%})")
    if linked_large_firms:
        reasons.append(f"linked to {linked_large_firms} other-than-small firm(s)")
    return SetAsideCheck(vendor, reasons)


def set_aside_share_jump(values_by_year: dict[int, tuple[float, float]]) -> list[int]:
    """Years in which a vendor's set-aside share of revenue from federal
    awards jumps by more than 40 points while total awards at least double:
    the profile of a front company created to win set-asides for a larger
    partner. `values_by_year` maps year -> (set_aside_dollars, total_dollars)."""
    years = sorted(values_by_year)
    out = []
    for prev, cur in zip(years, years[1:]):
        sa0, t0 = values_by_year[prev]
        sa1, t1 = values_by_year[cur]
        if t0 > 0 and t1 >= 2 * t0 and (sa1 / t1 if t1 else 0) - (sa0 / t0) > 0.40:
            out.append(cur)
    return out


def typical_growth(awards: list[Award]) -> float:
    """Median growth ratio, for reporting next to outliers."""
    vals = [growth_ratio(a) for a in awards if a.base_value > 0]
    return median(vals) if vals else float("nan")
