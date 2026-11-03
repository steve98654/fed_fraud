"""Build docs/universe/data/all_agencies.csv: every federal body we know of,
with its tier and the screens that cover it.

Inputs (committed):
  docs/universe/data/usaspending_toptier_fy2026.csv  USAspending toptier list (111 rows)
  docs/agencies/data/top33_fy2026.csv                top 33 and their brief files
Everything else (kind, tier, coverage, ideas, bodies outside USAspending's
list) is set below by hand and explained in docs/universe/all_agencies.md.

Run from the repo root:  python3 analytics/universe/build_universe.py
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "docs/universe/data/usaspending_toptier_fy2026.csv"
TOP = ROOT / "docs/agencies/data/top33_fy2026.csv"
OUT = ROOT / "docs/universe/data/all_agencies.csv"

UNIVERSAL_P1 = "U1-U6"
UNIVERSAL_P2 = "U7-U8"

CABINET = {"USDA", "DOC", "DOD", "ED", "DOE", "HHS", "DHS", "HUD", "DOJ", "DOL", "DOS", "DOT", "VA", "DOI", "TREAS"}
CORPORATION = {"CNCS", "EXIM", "DFC", "MCC", "PBGC", "FDIC", "FCSIC", "OPIC", "PRESIDIO"}
FOUNDATION = {"USADF", "IAF", "GOLDWATER", "TRUMAN", "MADISON", "UDALL", "JUSFC", "VEF", "PCORTF", "NSF", "NEA", "NEH", "IMLS", "KENNEDY CENTER"}
REGIONAL = {"ARC", "DRA", "DENALI", "NBRC", "SCRC", "SBRC", "GCERC"}
JUDICIAL = {"DC COURTS", "CAVC", "CSOSA"}
LEGISLATIVE = {"GAO"}
COMMISSION_WORDS = ("Commission", "Board", "Council", "Committee", "Authority")

# Shared screens beyond the universal ones. C1-C3 are in review_plan.md;
# C4-C7 are new in docs/universe/all_agencies.md.
SHARED = {
    "C4": {"EXIM", "DFC", "FCSIC", "NCUA", "SBA", "USDA", "HUD", "ED", "TREAS", "OPIC"},
    "C5": {"RRB", "OPM", "SSA", "VA", "DOL", "AFRH", "PBGC"},
    "C6": {"CFPB", "FTC", "CFTC", "SEC", "DOJ"},
    "C7": {"DC COURTS", "JUD", "DOL", "HHS", "USPS", "VA"},
    "C3": {"USADF", "IAF", "JUSFC", "ARC", "DRA", "DENALI", "NBRC", "SCRC", "GCERC", "NEA", "NEH", "IMLS",
           "MCC", "USAGM", "EAC", "USTDA", "TRUMAN", "GOLDWATER", "MADISON", "UDALL", "LSC", "CPB", "AMTRAK", "FPISC"},
    "C1": {"CSOSA", "NARA", "AFRH", "PRESIDIO", "PC", "ABMC", "USAGM", "NTSB", "CPSC", "EEOC", "NLRB", "CFPB",
           "CFTC", "FTC", "GAO", "TVA", "USPS", "AMTRAK", "SI", "LOC", "GPO", "AOC", "USITC", "DC COURTS", "JUD"},
}

# Tier B: bodies outside the top 33 with a payment stream worth its own idea.
TIER_B = {
    "RRB": ("RRB-1, RRB-2", "Disability and sickness benefit outliers by employer and physician; annuities after death (Phase 2)"),
    "USPS": ("USPS-1, USPS-2", "Supplier and highway contract route screen (not in FPDS; FOIA/OIG); workers' compensation provider outliers"),
    "TVA": ("TVA-1", "Supplier integrity screen (data access to confirm)"),
    "AMTRAK": ("AMTRAK-1", "Contractor and grant subcontractor screen on federal grants to Amtrak"),
    "JUD": ("JUD-1", "Criminal Justice Act attorney and expert vouchers: impossible days and peer outliers (Phase 2)"),
    "DC COURTS": ("DCC-1", "Court-appointed counsel vouchers: impossible days and peer outliers (Phase 2)"),
    "EXIM": ("EXIM-1", "Exporter, buyer and lender shell checks on authorizations"),
    "MCC": ("MCC-1", "Compact implementers and contractors against development-bank debarment lists"),
    "CFPB": ("CFPB-1", "Civil Penalty Fund and redress payments: duplicate and synthetic claimant tests"),
    "FTC": ("FTC-1", "Consumer refund programs: duplicate and synthetic claimant tests"),
    "NEA": ("ARTS-1", "Duplicate funding across NEA, NEH and IMLS (text similarity) plus Single Audit findings"),
    "NEH": ("ARTS-1", "See NEA"),
    "IMLS": ("ARTS-1", "See NEA"),
    "ARC": ("REG-1", "Regional commission grant overlap with EDA, USDA Rural Development and each other"),
    "DRA": ("REG-1", "See ARC"),
    "DENALI": ("REG-1", "See ARC"),
    "NBRC": ("REG-1", "See ARC"),
    "SCRC": ("REG-1", "See ARC"),
    "GCERC": ("RESTORE-1", "RESTORE Act grants: subrecipient reconciliation and grantee screen"),
    "LSC": ("LSC-1", "Legal aid grantee screen with Single Audit findings"),
    "CPB": ("CPB-1", "Station grant screen against station financial reports"),
    "USAGM": ("USAGM-1", "Grantee network and contractor screen"),
}

# Bodies not on USAspending's toptier list. No dollar figures are given for
# them because we have not pulled a comparable source; see the doc.
EXTRA = [
    ("USPS", "United States Postal Service", "Independent establishment (off-budget)", ""),
    ("TVA", "Tennessee Valley Authority", "Government corporation", "Wholly owned corporation under 31 U.S.C. 9101."),
    ("AMTRAK", "National Railroad Passenger Corporation (Amtrak)", "Government corporation", "Federally chartered; federal grants flow through DOT."),
    ("JUD", "Federal Judiciary (Administrative Office of the U.S. Courts)", "Judicial branch", "Not on the USAspending toptier list."),
    ("LOC", "Library of Congress", "Legislative branch", ""),
    ("GPO", "Government Publishing Office", "Legislative branch", ""),
    ("AOC", "Architect of the Capitol", "Legislative branch", ""),
    ("CBO", "Congressional Budget Office", "Legislative branch", "Salaries only; universal screens only."),
    ("CONGRESS", "House of Representatives and Senate", "Legislative branch", "Office spending is published in the Statements of Disbursements."),
    ("SI", "Smithsonian Institution", "Trust instrumentality", ""),
    ("LSC", "Legal Services Corporation", "Federally funded nonprofit corporation", ""),
    ("CPB", "Corporation for Public Broadcasting", "Federally funded nonprofit corporation", ""),
    ("USIP", "United States Institute of Peace", "Federally funded nonprofit corporation", ""),
    ("FHFA", "Federal Housing Finance Agency", "Independent regulator (assessment-funded)", ""),
    ("FCA", "Farm Credit Administration", "Independent regulator (assessment-funded)", ""),
    ("PRC", "Postal Regulatory Commission", "Regulatory commission or board", ""),
    ("FRS", "Federal Reserve System", "Out of scope", "Not funded by appropriations; has its own OIG."),
    ("GSE", "Fannie Mae, Freddie Mac and the Federal Home Loan Banks", "Out of scope", "Shareholder- or member-owned; FHFA and FHFA OIG oversee them."),
    ("FCS", "Farm Credit System banks", "Out of scope", "Privately owned successors to the Farm Credit banks named in 31 U.S.C. 9101(2); FCA supervises them."),
]

# Government corporations inside departments: covered through the parent.
COMPONENT_CORPS = [
    ("CCC", "Commodity Credit Corporation", "USDA"),
    ("FCIC", "Federal Crop Insurance Corporation", "USDA"),
    ("GNMA", "Government National Mortgage Association (Ginnie Mae)", "HUD"),
    ("FHA", "Federal Housing Administration Fund", "HUD"),
    ("FPI", "Federal Prison Industries", "DOJ"),
    ("CDFI", "Community Development Financial Institutions Fund", "TREAS"),
    ("GLS", "Great Lakes St. Lawrence Seaway Development Corporation", "DOT"),
]


INDEPENDENT = {"RRB", "CIGIE", "ABILITYONE", "USAB"}


def kind_of(abbr: str, name: str) -> str:
    if abbr in INDEPENDENT:
        return "Independent agency"
    if abbr in CABINET:
        return "Cabinet department"
    if abbr in CORPORATION:
        return "Government corporation"
    if abbr in REGIONAL:
        return "Regional commission"
    if abbr in FOUNDATION:
        return "Foundation, endowment or trust fund"
    if abbr in JUDICIAL:
        return "Judicial branch or court-related"
    if abbr in LEGISLATIVE:
        return "Legislative branch"
    if abbr in ("EOP",):
        return "Executive Office of the President"
    if any(w in name for w in COMMISSION_WORDS):
        return "Regulatory commission or board"
    return "Independent agency"


def shared_for(abbr: str) -> list[str]:
    return [c for c, members in SHARED.items() if abbr in members]


def main() -> None:
    top = {r["abbreviation"]: r for r in csv.DictReader(TOP.open())}
    rows = []
    for r in csv.DictReader(SRC.open()):
        abbr, name = r["abbreviation"], r["agency_name"]
        out = float(r["outlay_amount"])
        shared = shared_for(abbr)
        if abbr in top:
            tier = "A"
            brief = top[abbr]["brief"].removesuffix(".md")
            ideas = f"{abbr if abbr != 'DOS' else 'STATE'}-n (roadmap)"
            note = "Own plan in the roadmap and review plan."
        elif abbr in TIER_B:
            tier, brief = "B", ""
            ideas, note = TIER_B[abbr]
        elif abbr == "RRB":
            tier, brief = "B", ""
            ideas, note = TIER_B[abbr]
        elif out > 0:
            tier, brief, ideas, note = "C", "", "", "Universal screens and any shared screen listed."
        else:
            tier, brief, ideas, note = "D", "", "", "No outlays reported to USAspending for FY2026; check whether spending is reported elsewhere."
        if abbr == "RRB":
            tier = "B"
            note = TIER_B["RRB"][1] + ". USAspending shows no FY2026 outlays for RRB; its benefit spending is not reported there under RRB."
        coverage = []
        if tier == "A":
            coverage.append("Own plan")
        coverage += shared
        if out > 0:
            coverage += [UNIVERSAL_P1, UNIVERSAL_P2]
        elif tier == "B":
            coverage += [UNIVERSAL_P2]
        rows.append({
            "abbreviation": abbr,
            "name": name,
            "kind": kind_of(abbr, name),
            "in_usaspending": "yes",
            "outlays_usd": f"{out:.2f}",
            "tier": tier,
            "coverage": " ".join(coverage),
            "idea_ids": ideas,
            "brief": brief,
            "notes": note,
        })
    for abbr, name, kind, note in EXTRA:
        if kind == "Out of scope":
            tier, coverage, ideas = "X", "", ""
        elif abbr in TIER_B:
            tier = "B"
            ideas, n2 = TIER_B[abbr]
            note = (note + " " + n2).strip()
            coverage = " ".join(shared_for(abbr) + [UNIVERSAL_P1, UNIVERSAL_P2])
        else:
            tier, ideas = "C", ""
            coverage = " ".join(shared_for(abbr) + [UNIVERSAL_P1, UNIVERSAL_P2])
        rows.append({"abbreviation": abbr, "name": name, "kind": kind, "in_usaspending": "no", "outlays_usd": "",
                     "tier": tier, "coverage": coverage, "idea_ids": ideas, "brief": "", "notes": note})
    for abbr, name, parent in COMPONENT_CORPS:
        rows.append({"abbreviation": abbr, "name": name, "kind": "Government corporation (component)",
                     "in_usaspending": f"within {parent}", "outlays_usd": "", "tier": "A" if parent in top else "C",
                     "coverage": f"Through {parent}", "idea_ids": "", "brief": "",
                     "notes": f"Wholly owned corporation under 31 U.S.C. 9101; spending reported under {parent}."})
    order = {"A": 0, "B": 1, "C": 2, "D": 3, "X": 4}
    rows.sort(key=lambda r: (order[r["tier"]], -(float(r["outlays_usd"]) if r["outlays_usd"] else 0), r["name"]))
    with OUT.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    counts = {t: sum(1 for r in rows if r["tier"] == t) for t in order}
    print(f"wrote {OUT.relative_to(ROOT)}: {len(rows)} rows; tiers {counts}")


if __name__ == "__main__":
    main()
