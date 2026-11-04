"""Cross-agency data matching: one identity seen across many programs.

Links person and business records from several program extracts (SBA loans,
CMS enrollments, USDA payments, Treasury disbursements, SAM.gov
registrations, state UI and SNAP files) into identity clusters, then runs
the cross-program checks that no single agency can run alone:

* the same identity drawing from more programs than its profile explains
  (stacking), or from mutually exclusive programs at the same time;
* payments dated after a death date (SSA death data, Do Not Pay);
* payments made during an exclusion or debarment window (SAM exclusions,
  HHS-OIG LEIE, OPM debarments);
* one identifier (TIN, bank account, phone, email, device) shared by
  identities that otherwise look unrelated.

Records are compared with the Fellegi-Sunter weights in `linkage.py`;
identifiers are expected to arrive already hashed (keyed HMAC over the
normalized value) so raw TINs and account numbers never leave the agency
that owns them. See docs/playbook/cross_agency_matching.md.
"""
from __future__ import annotations

import hashlib
import hmac
import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from itertools import combinations

from .linkage import FSModel, jaro_winkler
from .network import UnionFind

# ---------------------------------------------------------------------------
# Normalization and privacy-preserving keys
# ---------------------------------------------------------------------------
_SUFFIXES = r"\b(inc|incorporated|llc|l l c|ltd|corp|corporation|co|company|pllc|pc|lp|llp)\b"
_STREET = {"street": "st", "avenue": "ave", "road": "rd", "suite": "ste", "boulevard": "blvd",
           "drive": "dr", "lane": "ln", "north": "n", "south": "s", "east": "e", "west": "w"}


def normalize_name(name: str) -> str:
    """Upper-insensitive name key: punctuation, legal suffixes and extra
    spaces removed ("Acme Holdings, L.L.C." -> "acme holdings")."""
    s = re.sub(r"[^a-z0-9 ]+", " ", name.lower())
    s = re.sub(r"\b([a-z]) (?=[a-z]\b)", r"\1", s)  # "l l c" -> "llc"
    s = re.sub(_SUFFIXES, " ", s)
    return re.sub(r"\s+", " ", s).strip()


def normalize_address(addr: str) -> str:
    """Light USPS-style standardization. Production uses CASS-certified
    standardization; this keeps the tests honest about what is compared."""
    words = re.sub(r"[^a-z0-9# ]+", " ", addr.lower()).split()
    return " ".join(_STREET.get(w, w) for w in words)


def keyed_hash(value: str, key: bytes) -> str:
    """HMAC-SHA256 of a normalized identifier. Each data owner hashes with
    the shared key inside its own boundary; only hashes are exchanged, so a
    match reveals that two records share a TIN without revealing the TIN.
    The key is held by the matching authority (e.g. Do Not Pay) and rotated
    per agreement."""
    norm = re.sub(r"[^0-9a-z]", "", value.lower())
    return hmac.new(key, norm.encode(), hashlib.sha256).hexdigest()[:32]


# ---------------------------------------------------------------------------
# Records and linkage
# ---------------------------------------------------------------------------
@dataclass
class ProgramRecord:
    record_id: str
    program: str  # e.g. "SBA-PPP", "CMS-PECOS", "USDA-FSA", "STATE-UI"
    name: str
    address: str = ""
    dob_or_founded: str = ""  # ISO date or year
    tin_hash: str = ""
    bank_hash: str = ""
    phone: str = ""
    email: str = ""
    paid: list[tuple[date, float]] = field(default_factory=list)


FIELDS = ["name", "address", "dob_or_founded", "tin_hash", "bank_hash", "phone", "email"]


def compare(a: ProgramRecord, b: ProgramRecord) -> list[int]:
    """Binary agreement vector over FIELDS. Missing values count as
    disagreement, which is conservative (lowers the weight)."""
    na, nb = normalize_name(a.name), normalize_name(b.name)
    g = [1 if na and nb and jaro_winkler(na, nb) >= 0.92 else 0]
    aa, ab = normalize_address(a.address), normalize_address(b.address)
    g.append(1 if aa and aa == ab else 0)
    for f in FIELDS[2:]:
        va, vb = getattr(a, f), getattr(b, f)
        g.append(1 if va and va == vb else 0)
    return g


def blocking_pairs(records: list[ProgramRecord], max_block: int = 200) -> set[tuple[int, int]]:
    """Candidate pairs that share at least one blocking key: TIN hash, bank
    hash, phone, email, or first name token plus ZIP-like trailing number.
    Blocks larger than `max_block` (registered-agent addresses, shared
    call-center phones) are skipped, as hubs are in network.py."""
    blocks: dict[str, list[int]] = defaultdict(list)
    for i, r in enumerate(records):
        for f in ("tin_hash", "bank_hash", "phone", "email"):
            v = getattr(r, f)
            if v:
                blocks[f"{f}:{v}"].append(i)
        tok = normalize_name(r.name).split()
        zipm = re.findall(r"\b\d{5}\b", r.address)
        if tok:
            blocks[f"nz:{tok[0]}:{zipm[-1] if zipm else ''}"].append(i)
    pairs: set[tuple[int, int]] = set()
    for ids in blocks.values():
        if 2 <= len(ids) <= max_block:
            pairs.update(combinations(sorted(set(ids)), 2))
    return pairs


def link(records: list[ProgramRecord], model: FSModel, threshold: float) -> list[set[str]]:
    """Identity clusters: union of every candidate pair whose Fellegi-Sunter
    weight is at or above `threshold`. Returns sets of record ids, largest
    first. Transitive closure can chain weak links; the review step checks
    clusters whose internal minimum weight is low."""
    uf = UnionFind()
    for r in records:
        uf.find(r.record_id)
    for i, j in blocking_pairs(records):
        if model.weight(compare(records[i], records[j])) >= threshold:
            uf.union(records[i].record_id, records[j].record_id)
    groups: dict[str, set[str]] = defaultdict(set)
    for r in records:
        groups[uf.find(r.record_id)].add(r.record_id)
    return sorted(groups.values(), key=len, reverse=True)


# ---------------------------------------------------------------------------
# Cross-program checks on linked identities
# ---------------------------------------------------------------------------
@dataclass
class CrossFlag:
    identity: frozenset[str]
    check: str
    detail: str
    amount: float = 0.0


def program_stacking(clusters: list[set[str]], by_id: dict[str, ProgramRecord], max_programs: int = 3,
                     exclusive: list[set[str]] | None = None) -> list[CrossFlag]:
    """Identities that draw on more than `max_programs` distinct programs, or
    on two programs listed together in `exclusive` (e.g. state UI and a PPP
    loan claiming the same person as a full-time employee in the same
    weeks). Exclusivity rules come from program law and must be written down
    per pair; this function only applies them."""
    out = []
    exclusive = exclusive or []
    for c in clusters:
        progs = {by_id[i].program for i in c}
        total = sum(a for i in c for _, a in by_id[i].paid)
        if len(progs) > max_programs:
            out.append(CrossFlag(frozenset(c), "stacking", f"{len(progs)} programs: {', '.join(sorted(progs))}", total))
        for ex in exclusive:
            if ex <= progs:
                out.append(CrossFlag(frozenset(c), "exclusive", f"both of {', '.join(sorted(ex))}", total))
    return out


def paid_after_event(clusters: list[set[str]], by_id: dict[str, ProgramRecord], event_date: dict[str, date],
                     check: str, grace_days: int = 0) -> list[CrossFlag]:
    """Payments dated more than `grace_days` after an identity-level event:
    a death date (check="after-death") or an exclusion start date
    (check="while-excluded"). `event_date` is keyed by any record id in the
    cluster, so one death record in one program reaches every program the
    identity is paid by. Grace days cover legitimate lags (the month of
    death, claims for services before exclusion)."""
    out = []
    for c in clusters:
        dates = [event_date[i] for i in c if i in event_date]
        if not dates:
            continue
        ev = min(dates)
        late = [(d, a, by_id[i].program) for i in c for d, a in by_id[i].paid if (d - ev).days > grace_days]
        if late:
            progs = sorted({p for _, _, p in late})
            out.append(CrossFlag(frozenset(c), check,
                                 f"{len(late)} payments after {ev.isoformat()} in {', '.join(progs)}",
                                 sum(a for _, a, _ in late)))
    return out


def shared_identifier_conflicts(clusters: list[set[str]], by_id: dict[str, ProgramRecord],
                                attr: str = "bank_hash", min_identities: int = 3) -> list[CrossFlag]:
    """One identifier (bank account, phone, email) used by at least
    `min_identities` identity clusters that did NOT link to each other on
    name, address and TIN: the cross-program version of roadmap idea X-2."""
    owner = {i: k for k, c in enumerate(clusters) for i in c}
    users: dict[str, set[int]] = defaultdict(set)
    for rid, r in by_id.items():
        v = getattr(r, attr)
        if v:
            users[v].add(owner[rid])
    out = []
    for v, ks in users.items():
        if len(ks) >= min_identities:
            ids = frozenset(i for k in ks for i in clusters[k])
            total = sum(a for i in ids for _, a in by_id[i].paid)
            out.append(CrossFlag(ids, f"shared-{attr}", f"{len(ks)} unrelated identities share one {attr}", total))
    return out
