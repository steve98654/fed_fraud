"""Duplicate-payment, split-purchase and impossible-billing tests.

These are transaction tests: they need payment, invoice, card or voucher
records, so most run in Phase 2 on internal data. The award-level versions
(split awards, repeated award amounts) run on public USAspending data.
See docs/playbook/forensic_methods.md section 4.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta
from itertools import combinations

# Characters that OCR and keying commonly confuse.
_CONFUSABLE = str.maketrans({"O": "0", "o": "0", "I": "1", "l": "1", "S": "5", "B": "8", "Z": "2"})


def normalize_invoice(inv: str) -> str:
    """Canonical form of an invoice number: upper case, confusable letters
    mapped to digits, punctuation and leading zeros removed, common
    prefixes/suffixes (INV, -A, -R, -DUP) stripped."""
    s = inv.strip().upper()
    s = re.sub(r"^(INV(OICE)?|NO|#)[\s.#:-]*", "", s)
    s = re.sub(r"[-_ ]?(A|B|R|DUP|COPY|REV\d*)$", "", s)
    s = s.translate(_CONFUSABLE)
    s = re.sub(r"[^0-9A-Z]", "", s)
    return s.lstrip("0") or "0"


def damerau_levenshtein(a: str, b: str) -> int:
    """Optimal string alignment distance (insert, delete, substitute,
    transpose adjacent characters)."""
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + cost)
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[len(a)][len(b)]


@dataclass(frozen=True)
class Payment:
    id: str
    vendor: str
    amount: float
    paid: date
    invoice: str = ""
    payer: str = ""  # cardholder, approving official or office


@dataclass(frozen=True)
class DuplicatePair:
    a: str
    b: str
    rule: str


def duplicate_pairs(payments: list[Payment], window_days: int = 90, max_edit: int = 1) -> list[DuplicatePair]:
    """Find likely duplicate payments in four tiers, from strongest to weakest:

    1. SSSS: same vendor, amount, invoice and date (exact duplicate).
    2. SSS-D: same vendor, amount and normalized invoice, different date.
    3. SS-fuzzy: same vendor and amount, invoices within `max_edit` edits
       (transposed or mistyped digits) within `window_days`.
    4. SDS: same amount and invoice paid to two different vendors (vendor
       master duplicates, or a diverted payment).
    """
    out: list[DuplicatePair] = []
    by_va: dict[tuple[str, float], list[Payment]] = defaultdict(list)
    for p in payments:
        by_va[(p.vendor, round(p.amount, 2))].append(p)
    for group in by_va.values():
        for x, y in combinations(group, 2):
            nx, ny = normalize_invoice(x.invoice), normalize_invoice(y.invoice)
            if x.invoice == y.invoice and x.paid == y.paid:
                out.append(DuplicatePair(x.id, y.id, "same vendor, amount, invoice and date"))
            elif nx == ny:
                out.append(DuplicatePair(x.id, y.id, "same vendor, amount and invoice; different date"))
            elif (
                abs((x.paid - y.paid).days) <= window_days
                and nx
                and ny
                and damerau_levenshtein(nx, ny) <= max_edit
            ):
                out.append(DuplicatePair(x.id, y.id, "same vendor and amount; near-identical invoice"))
    by_ai: dict[tuple[float, str], list[Payment]] = defaultdict(list)
    for p in payments:
        if p.invoice:
            by_ai[(round(p.amount, 2), normalize_invoice(p.invoice))].append(p)
    for group in by_ai.values():
        for x, y in combinations(group, 2):
            if x.vendor != y.vendor:
                out.append(DuplicatePair(x.id, y.id, "same amount and invoice; different vendor"))
    return out


@dataclass(frozen=True)
class SplitFlag:
    payer: str
    vendor: str
    start: date
    ids: tuple[str, ...]
    total: float


def split_purchases(payments: list[Payment], threshold: float, window_days: int = 3) -> list[SplitFlag]:
    """Flag groups of purchases by one payer from one vendor within
    `window_days` where every purchase is under `threshold` but the group
    total is over it: the classic split to stay under a card or
    micro-purchase limit. Groups are maximal runs, reported once."""
    out = []
    groups: dict[tuple[str, str], list[Payment]] = defaultdict(list)
    for p in payments:
        if p.amount < threshold:
            groups[(p.payer, p.vendor)].append(p)
    for (payer, vendor), ps in groups.items():
        ps.sort(key=lambda p: p.paid)
        i = 0
        while i < len(ps):
            j = i
            while j + 1 < len(ps) and (ps[j + 1].paid - ps[i].paid).days <= window_days:
                j += 1
            run = ps[i : j + 1]
            total = sum(p.amount for p in run)
            if len(run) >= 2 and total > threshold:
                out.append(SplitFlag(payer, vendor, run[0].paid, tuple(p.id for p in run), round(total, 2)))
                i = j + 1
            else:
                i += 1
    return out


@dataclass(frozen=True)
class TimeEntry:
    biller: str  # attorney, provider, contractor employee
    day: date
    hours: float
    matter: str


def impossible_days(entries: list[TimeEntry], max_hours: float = 24.0) -> dict[tuple[str, date], float]:
    """Total billed hours per biller per day across all matters, returning
    the days above `max_hours`. A day over 24 hours cannot be true; review
    thresholds below 24 (for example 16) are set per program."""
    totals: dict[tuple[str, date], float] = defaultdict(float)
    for e in entries:
        totals[(e.biller, e.day)] += e.hours
    return {k: v for k, v in totals.items() if v > max_hours}


def services_after_death(service_dates: dict[str, list[date]], death_dates: dict[str, date], grace_days: int = 0) -> dict[str, list[date]]:
    """Services or payments dated after the person's date of death (plus an
    optional grace period for legitimate end-of-month payments)."""
    out = {}
    for pid, dates in service_dates.items():
        dod = death_dates.get(pid)
        if dod is None:
            continue
        late = [d for d in dates if d > dod + timedelta(days=grace_days)]
        if late:
            out[pid] = late
    return out
