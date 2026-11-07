"""Build the agency budget and fraud ROM table.

Writes:
  docs/universe/data/agency_budget_fraud_rom.csv   one row per body (137)
  docs/universe/budget_fraud_rom.md                the same table, rendered

Every fraud figure here is a rough order of magnitude (ROM) allocation of
GAO's government-wide estimate, NOT a measurement and NOT a finding. The
method is set out in docs/universe/budget_fraud_rom.md and in the
constants below; change a constant, rerun, and both files update.

Inputs (committed):
  docs/universe/data/all_agencies.csv   the 137-body list (build_universe.py)
  OFF_LIST below                        budgets for bodies USAspending omits

Run from the repo root:  python3 analytics/universe/budget_fraud_rom.py
"""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "docs/universe/data/all_agencies.csv"
OUT_CSV = ROOT / "docs/universe/data/agency_budget_fraud_rom.csv"
OUT_MD = ROOT / "docs/universe/budget_fraud_rom.md"

# GAO-24-106608 (April 2024): the federal government loses an estimated
# $233B to $521B a year to fraud (FY2018-2022 data), 3% to 7% of average
# federal obligations.
GAO_LOW = 233e9
GAO_HIGH = 521e9

# Treasury's USAspending outlays include interest on the debt, which is not
# a fraud exposure. We remove CBO's FY2026 net interest on the public debt
# (Monthly Budget Review, Oct 2026: $1,143B). Using net rather than gross
# interest ($1.36T) leaves Treasury with more exposure, not less.
TREAS_INTEREST_EXCLUDED = 1_143e9

# Risk weight per class. The weight multiplies exposed outlays before GAO's
# total is shared out, so only the ratios between weights matter.
WEIGHTS = {"H": 2.0, "S": 1.0, "L": 0.5, "-": 0.0}
CLASS_LABEL = {
    "H": "High: benefit, loan or payment programs with large documented fraud or improper payments",
    "S": "Standard: contracts, grants and mixed programs",
    "L": "Low: payroll-heavy, regulatory, self-funded or low measured error",
    "-": "Not scored: counted in parent, no outlays, or out of scope",
}
HIGH = {"HHS", "USDA", "SBA", "DOL", "TREAS", "FCC"}
LOW_ABBR = {"SSA", "OPM", "PBGC", "FDIC", "USPS", "TVA", "EOP", "GAO", "SEC", "NRC"}
LOW_KINDS = {
    "Regulatory commission or board",
    "Independent regulator (assessment-funded)",
    "Legislative branch",
    "Judicial branch",
    "Judicial branch or court-related",
    "Executive Office of the President",
    "Trust instrumentality",
}

# Bodies not on USAspending's toptier list: (amount_usd, measure, fiscal
# year, source). "approx." marks figures from memory of the cited source
# that a reviewer should confirm before external use.
CRS_LEG = "CRS R48612, Legislative Branch: FY2026 Appropriations (Mar 2026)"
OFF_LIST = {
    "USPS": (89.8e9, "Total operating expenses (self-funded)", "FY2025", "USPS FY2025 results release, 14 Nov 2025"),
    "TVA": (13.672e9, "Operating revenues (self-funded; used as size proxy)", "FY2025", "TVA FY2025 results release"),
    "AMTRAK": (6.8e9, "Federal grants: annual appropriation plus IIJA advance appropriation (approx.)", "FY2025", "FRA Amtrak annual grants fact sheet; IIJA div. J (approx.)"),
    "JUD": (9.187e9, "Enacted discretionary appropriations", "FY2026", "CRS R49357, Judiciary Appropriations, FY2026 (P.L. 119-75)"),
    "CONGRESS": (3.550e9, "Enacted appropriations, House $2,083M + Senate $1,467M", "FY2026", CRS_LEG),
    "LOC": (852.2e6, "Enacted appropriations (incl. CRS)", "FY2026", CRS_LEG),
    "AOC": (811.9e6, "Enacted appropriations", "FY2026", CRS_LEG),
    "GPO": (132.0e6, "Enacted appropriations", "FY2026", CRS_LEG),
    "CBO": (74.8e6, "Enacted appropriations", "FY2026", CRS_LEG),
    "SI": (1.1e9, "Federal appropriations (approx.)", "FY2025", "Smithsonian congressional budget justification (approx.)"),
    "LSC": (560e6, "Appropriation (approx.)", "FY2025", "LSC budget request / FY2025 full-year CR (approx.)"),
    "CPB": (535e6, "Advance appropriation (approx.); FY2026-27 funds rescinded July 2025, CPB winding down", "FY2025", "P.L. 119-28 rescission; CPB announcements (approx.)"),
    "FHFA": (390e6, "Assessment-funded budget (approx.)", "FY2025", "FHFA performance and budget documents (approx.)"),
    "FCA": (100e6, "Assessment-funded budget (approx.)", "FY2025", "FCA budget documents (approx.)"),
    "USIP": (55e6, "Appropriation (approx.)", "FY2024", "Consolidated Appropriations Act, 2024 (approx.)"),
    "RRB": (17.5e9, "Benefit payments (approx.); USAspending reports $0 outlays for RRB", "FY2025", "RRB annual report / financial statements (approx.)"),
    "PRC": (22e6, "Budget, paid from the Postal Service Fund (approx.)", "FY2025", "PRC budget documents (approx.)"),
}
USASPENDING_SRC = "USAspending toptier agencies API, FY2026 Q4, pulled 2026-11-03"

# PaymentAccuracy.gov FY2025: susceptible outlays ($M) x improper payment
# rate, the same table as docs/universe/all_agencies.md. Context only:
# improper payments are not fraud, and fraud is not all improper payments.
IMPROPER_FY2025 = {
    "HHS": (1_670_124, 0.0583), "SSA": (1_494_212, 0.0076), "DOD": (241_689, 0.0072),
    "VA": (201_103, 0.0109), "ED": (185_708, 0.0071), "OPM": (176_584, 0.0025),
    "USDA": (148_306, 0.0905), "TREAS": (105_743, 0.2654), "DOT": (67_068, 0.0357),
    "SBA": (66_238, 0.1229), "HUD": (50_439, 0.0), "DOL": (41_634, 0.1216),
    "DHS": (21_631, 0.0015), "FCC": (2_741, 0.0503), "CNCS": (478, 0.0264),
}


def risk_class(row: dict) -> str:
    abbr, tier, kind = row["abbreviation"], row["tier"], row["kind"]
    if tier in {"D", "X"} or kind == "Government corporation (component)":
        return "-"
    if abbr in HIGH:
        return "H"
    if abbr in LOW_ABBR or kind in LOW_KINDS:
        return "L"
    return "S"


def magnitude(x: float) -> str:
    if x <= 0:
        return ""
    for lo, label in [(1e11, "$100B+"), (1e10, "$10B-$100B"), (1e9, "$1B-$10B"), (1e8, "$100M-$1B"),
                      (1e7, "$10M-$100M"), (1e6, "$1M-$10M")]:
        if x >= lo:
            return label
    return "under $1M"


def sig(x: float, n: int = 2) -> float:
    if x <= 0:
        return 0.0
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))


def build() -> list[dict]:
    rows = list(csv.DictReader(SRC.open()))
    out = []
    for r in rows:
        abbr = r["abbreviation"]
        cls = risk_class(r)
        if r["in_usaspending"] == "yes" and abbr not in OFF_LIST:
            budget, measure, fy, src = float(r["outlays_usd"] or 0), "Outlays", "FY2026", USASPENDING_SRC
        elif abbr in OFF_LIST:
            budget, measure, fy, src = OFF_LIST[abbr]
        elif r["kind"] == "Government corporation (component)":
            budget, measure, fy, src = None, f"Counted in parent ({r['in_usaspending'].replace('within ', '')})", "", ""
        else:
            budget, measure, fy, src = None, "Not appropriated; out of scope", "", ""
        exposed = max(budget or 0.0, 0.0)
        if abbr == "TREAS":
            exposed = max(exposed - TREAS_INTEREST_EXCLUDED, 0.0)
        ip = IMPROPER_FY2025.get(abbr)
        out.append({
            "abbreviation": abbr, "name": r["name"], "tier": r["tier"],
            "budget_usd": "" if budget is None else f"{budget:.0f}",
            "budget_measure": measure, "budget_fy": fy, "budget_source": src,
            "exposed_usd": exposed, "risk_class": cls, "weight": WEIGHTS[cls],
            "improper_fy2025_usd": "" if ip is None else f"{ip[0] * 1e6 * ip[1]:.0f}",
        })
    total_w = sum(o["exposed_usd"] * o["weight"] for o in out)
    for o in out:
        share = o["exposed_usd"] * o["weight"] / total_w
        o["share_of_gao"] = share
        o["fraud_rom_low_usd"] = GAO_LOW * share
        o["fraud_rom_high_usd"] = GAO_HIGH * share
        b = float(o["budget_usd"]) if o["budget_usd"] else 0.0
        o["implied_rate_low"] = o["fraud_rom_low_usd"] / b if b > 0 else 0.0
        o["implied_rate_high"] = o["fraud_rom_high_usd"] / b if b > 0 else 0.0
    out.sort(key=lambda o: (-o["fraud_rom_high_usd"], -(float(o["budget_usd"]) if o["budget_usd"] else -1), o["abbreviation"]))
    return out


FIELDS = ["rank", "abbreviation", "name", "tier", "budget_usd", "budget_measure", "budget_fy", "budget_source",
          "exposed_usd", "risk_class", "weight", "share_of_gao", "fraud_rom_low_usd", "fraud_rom_high_usd",
          "fraud_rom_magnitude", "implied_rate_low", "implied_rate_high", "improper_fy2025_usd"]


def write_csv(rows: list[dict]) -> None:
    with OUT_CSV.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        n = 0
        for r in rows:
            scored = r["weight"] > 0
            n += scored
            w.writerow({
                **{k: r[k] for k in ("abbreviation", "name", "tier", "budget_usd", "budget_measure", "budget_fy",
                                     "budget_source", "risk_class", "weight", "improper_fy2025_usd")},
                "rank": n if scored else "",
                "exposed_usd": f"{r['exposed_usd']:.0f}" if scored else "",
                "share_of_gao": f"{r['share_of_gao']:.6f}" if scored else "",
                "fraud_rom_low_usd": f"{sig(r['fraud_rom_low_usd']):.0f}" if scored else "",
                "fraud_rom_high_usd": f"{sig(r['fraud_rom_high_usd']):.0f}" if scored else "",
                "fraud_rom_magnitude": magnitude(r["fraud_rom_high_usd"]) if scored else "",
                "implied_rate_low": f"{r['implied_rate_low']:.4f}" if scored else "",
                "implied_rate_high": f"{r['implied_rate_high']:.4f}" if scored else "",
            })


def money(x: float | str) -> str:
    if x == "" or x is None:
        return "n/a"
    x = float(x)
    if x == 0:
        return "$0"
    if x >= 1e9:
        return f"${sig(x / 1e9, 2):,.3g}B" if x < 1e12 else f"${x / 1e12:,.2f}T"
    if x >= 1e6:
        return f"${sig(x / 1e6, 2):,.3g}M"
    return f"${sig(x / 1e3, 2):,.3g}K"


def write_md(rows: list[dict]) -> None:
    scored = [r for r in rows if r["weight"] > 0]
    total_budget = sum(float(r["budget_usd"]) for r in rows if r["budget_usd"] and float(r["budget_usd"]) > 0)
    top10 = sum(r["share_of_gao"] for r in scored[:10])
    lines = [
        "# Federal agency budgets and fraud estimates (rough order of magnitude)",
        "",
        "> **Every fraud figure below is a rough order of magnitude (ROM) allocation of GAO's",
        "> government-wide estimate. None is a measurement, a finding or a savings claim.**",
        "> Use them to size and rank work, never to cite an agency's fraud level.",
        "",
        "Generated by `analytics/universe/budget_fraud_rom.py` from the 137-body list in",
        "[all_agencies.md](all_agencies.md). Data: [agency_budget_fraud_rom.csv](data/agency_budget_fraud_rom.csv).",
        "",
        "## Bottom line",
        "",
        f"- GAO's government-wide range, **${GAO_LOW / 1e9:.0f}B to ${GAO_HIGH / 1e9:.0f}B a year**, is shared across "
        f"{len(scored)} scored bodies; the unrounded column totals equal GAO's range.",
        f"- The top 10 rows take {top10:.0%} of the total. HHS alone is "
        f"{money(scored[0]['fraud_rom_low_usd'])} to {money(scored[0]['fraud_rom_high_usd'])}.",
        f"- Budgets listed sum to {money(total_budget)}. This is above total federal outlays "
        "(CBO: $7.40T in FY2026) because USAspending agency totals include transfers between agencies "
        "and trust funds. It shifts shares between agencies; it does not change the government-wide total.",
        "",
        "## Method",
        "",
        "1. **Budget.** FY2026 Q4 outlays from USAspending for the bodies it lists. For the 16 it",
        "   omits, and for RRB (which it shows at $0), the latest enacted appropriation or, for self-funded bodies (USPS, TVA), operating",
        "   expenses or revenue, with fiscal year and source on each row. Figures marked *approx.* in the",
        "   CSV's measure or source column need confirming before external use. Component corporations",
        "   (CCC, FCIC, FHA, Ginnie Mae, CDFI Fund, FPI, Seaway) are counted inside their parent.",
        "2. **Exposure.** Budget, with negative outlays set to zero and Treasury's interest on the debt",
        f"   removed (${TREAS_INTEREST_EXCLUDED / 1e9:,.0f}B, CBO FY2026 net interest).",
        "3. **Risk weight.** " + "; ".join(f"{k} = {WEIGHTS[k]:g} ({CLASS_LABEL[k]})" for k in ("H", "S", "L")) + ".",
        f"   High: {', '.join(sorted(HIGH))}. Low: {', '.join(sorted(LOW_ABBR))}, plus every regulator,",
        "   legislative, judicial and EOP body. Everything else is Standard.",
        "4. **Allocation.** Each body's share = exposure x weight / sum over all bodies. ROM low and",
        "   high = share x GAO's $233B and $521B. Values are rounded to two significant figures.",
        "5. **Cross-check.** FY2025 improper payments (PaymentAccuracy.gov, susceptible outlays x rate)",
        "   are shown for the 15 agencies that report them. Improper payments are not fraud: they include",
        "   paperwork errors, and much fraud is never caught as an improper payment.",
        "",
        "## Caveats",
        "",
        "- GAO's range is built on FY2018-2022 data, which includes pandemic programs (UI, PPP, EIDL),",
        "  so it is likely high for a normal year. GAO's 3-7% applies to obligations, not outlays.",
        "- USAspending agency totals are not clean program budgets: DoD's $1.35T and HHS's $2.69T",
        "  include trust-fund and intragovernmental flows, which inflates their shares.",
        "- SBA's FY2025 improper payments ($8.1B) far exceed its ROM because they come from pandemic",
        "  loan and grant programs paid out in earlier years; the ROM sizes current-year outlays only.",
        "- The risk weights are judgment, set out in the script so anyone can change them and rerun.",
        "  Doubling or halving a class changes shares, not the government-wide total.",
        "- Small bodies get small numbers by construction. A $10M agency can still host a large scheme;",
        "  the screens in the [coverage plan](all_agencies.md) are how we find out.",
        "",
        "## The table",
        "",
        "Sorted by ROM high. Implied rate = ROM / budget.",
        "",
        "| # | Body | Tier | Budget | Basis | Risk | Fraud ROM (low-high) | Magnitude | Implied rate | FY2025 improper payments |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    n = 0
    for r in rows:
        s = r["weight"] > 0
        n += s
        basis = f"{r['budget_measure']}, {r['budget_fy']}".strip(", ")
        rom = f"{money(sig(r['fraud_rom_low_usd']))} - {money(sig(r['fraud_rom_high_usd']))}" if s else "n/a"
        rate = f"{r['implied_rate_low']:.1%} - {r['implied_rate_high']:.1%}" if s and r["budget_usd"] else ""
        lines.append(
            f"| {n if s else ''} | {r['name']} ({r['abbreviation']}) | {r['tier']} | {money(r['budget_usd'])} | {basis} | "
            f"{r['risk_class']} | {rom} | {magnitude(r['fraud_rom_high_usd']) if s else ''} | {rate} | "
            f"{money(r['improper_fy2025_usd']) if r['improper_fy2025_usd'] else ''} |"
        )
    lines += [
        "",
        "## Sources",
        "",
        "- [GAO-24-106608: Fraud Risk Management, $233B to $521B annual estimate](https://www.gao.gov/products/gao-24-106608)",
        "- [USAspending agency list API (FY2026 Q4)](https://api.usaspending.gov/api/v2/references/toptier_agencies/), pulled 2026-11-03",
        "- [PaymentAccuracy.gov agencies and programs (FY2025)](https://paymentaccuracy.gov/agencies-and-programs)",
        "- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)",
        "- [CBO Monthly Budget Review, October 2026](https://www.cbo.gov/system/files/2026-10/61985-MBR.pdf): FY2026 outlays and net interest",
        "- [CRS R49357: Judiciary Appropriations, FY2026](https://www.everycrsreport.com/reports/R49357.html)",
        "- [CRS R48612: Legislative Branch, FY2026 Appropriations](https://www.everycrsreport.com/reports/R48612.html)",
        "- [USPS FY2025 results](https://about.usps.com/newsroom/national-releases/2025/1114-usps-reports-fiscal-year-2025-results.pdf)",
        "- [TVA FY2025 results](https://s205.q4cdn.com/318912997/files/doc_financials/2025/q4/FY25-Investor-Webcast-Press-Release-Final.pdf)",
        "- [FRA Amtrak annual grants fact sheet](https://railroads.dot.gov/sites/fra.dot.gov/files/2025-01/Amtrak%20Annual%20Grants%20fact%20sheet_1.23.25_PDFa.pdf)",
        "",
    ]
    OUT_MD.write_text("\n".join(lines))


def main() -> None:
    rows = build()
    write_csv(rows)
    write_md(rows)
    print(f"wrote {OUT_CSV.relative_to(ROOT)} and {OUT_MD.relative_to(ROOT)} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
