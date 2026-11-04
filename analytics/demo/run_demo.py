"""Live demo: run the forensic methods on real public data and write the
results the site's /demo/ page shows.

Always runs on data committed to the repo:

* docs/universe/data/usaspending_toptier_fy2026.csv: outlays, budget
  authority and obligations of every federal agency (USAspending, FY2026).
  Digit test, concentration, and a reconciliation of obligations and
  outlays against budget authority.
* analytics/roi/programs.csv through the ROI model (analytics/roi/model.py).

Also scores any award files that fetch_usaspending.py has written to
docs/demo/data/awards_*.csv: digit test, round-number share, bunching below
the simplified acquisition threshold, and recipient concentration.

Every number here is a test statistic on public data, not a finding. The
page says so, and no recipient is named.

    python3 analytics/demo/run_demo.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analytics"))

from forensic import digits, outliers  # noqa: E402
from roi import model as roi  # noqa: E402

OUT = ROOT / "docs/demo/data/demo.json"
# FAR 2.101 simplified acquisition threshold. The October 2025 inflation
# adjustment raised it from $250,000 to $350,000; check before relying on it.
SAT = 350_000.0


def digit_block(values: list[float]) -> dict:
    r = digits.digit_test(values, "first")
    return {
        "n": r.n,
        "observed": {str(k): v for k, v in r.observed.items()},
        "expected": {str(k): v for k, v in r.expected.items()},
        "chi2": r.chi2,
        "p_value": r.p_value,
        "mad": r.mad,
        "conformity": r.conformity,
        "spikes": r.spikes(),
    }


def toptier() -> dict:
    path = ROOT / "docs/universe/data/usaspending_toptier_fy2026.csv"
    rows = list(csv.DictReader(open(path, newline="")))
    cols = ["outlay_amount", "budget_authority_amount", "obligated_amount"]
    vals = [float(r[c]) for r in rows for c in cols if float(r[c]) > 0]
    outlays = sorted((float(r["outlay_amount"]) for r in rows if float(r["outlay_amount"]) > 0), reverse=True)
    total = sum(outlays)
    recon = []
    for r in rows:
        ba, ob, ou = (float(r[c]) for c in ("budget_authority_amount", "obligated_amount", "outlay_amount"))
        if ba > 1e8 and (ob > 1.05 * ba or ou > 1.05 * ba):
            recon.append({"agency": r["agency_name"], "abbreviation": r["abbreviation"], "budget_authority": ba,
                          "obligated": ob, "outlays": ou, "outlay_to_ba": ou / ba})
    recon.sort(key=lambda d: d["outlay_to_ba"], reverse=True)
    return {
        "source": "USAspending.gov agency profiles, FY2026 (docs/universe/data/usaspending_toptier_fy2026.csv)",
        "agencies": len(rows),
        "agencies_with_outlays": len(outlays),
        "digits": digit_block(vals),
        "digits_outlays_only": digit_block(outlays),
        "gini_outlays": outliers.gini(outlays),
        "top5_share": sum(outlays[:5]) / total,
        "top10_share": sum(outlays[:10]) / total,
        "reconciliation": recon,
    }


def awards(path: Path) -> dict:
    rows = list(csv.DictReader(open(path, newline="")))
    amts = [float(r["amount"]) for r in rows if r["amount"] not in ("", "None") and float(r["amount"]) > 0]
    by_recipient: dict[str, float] = {}
    for r in rows:
        if r["amount"] not in ("", "None"):
            by_recipient[r["recipient"]] = by_recipient.get(r["recipient"], 0.0) + max(float(r["amount"]), 0.0)
    shares = sorted(by_recipient.values(), reverse=True)
    tot = sum(shares) or 1.0
    out = {
        "file": str(path.relative_to(ROOT)),
        "awards": len(rows),
        "digits": digit_block(amts) if len(amts) >= 100 else None,
        "round_thousand_share": digits.round_number_share(amts, 1000.0),
        "recipients": len(by_recipient),
        "hhi_recipients": sum((v / tot) ** 2 for v in shares),
        "top10_recipient_share": sum(shares[:10]) / tot,
    }
    near = [a for a in amts if SAT * 0.5 <= a <= SAT * 1.5]
    if len(near) >= 200:
        b = outliers.bunching(near, SAT, bin_width=SAT / 40, span=20, degree=3)
        out["bunching_below_sat"] = {"threshold": SAT, "excess": b.excess_count, "ratio": b.ratio, "n_window": len(near)}
    return out


def main() -> dict:
    rows = roi.main()
    result = {
        "note": "Test statistics on public data. A result is a reason to look, not a finding. Savings: Pending.",
        "toptier": toptier(),
        "roi": [{k: r[k] for k in ("agency", "program", "status", "improper_usd", "reach", "net", "roi", "p_positive",
                                    "breakeven_new_detection", "first_pilot")} for r in rows],
        "awards": [awards(p) for p in sorted((ROOT / "docs/demo/data").glob("awards_*.csv"))],
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=1) + "\n")
    return result


if __name__ == "__main__":
    r = main()
    t = r["toptier"]
    print(f"toptier: n={t['digits']['n']} MAD={t['digits']['mad']:.4f} ({t['digits']['conformity']}), "
          f"gini={t['gini_outlays']:.3f}, top10 share={t['top10_share']:.1%}, recon flags={len(t['reconciliation'])}")
    print(f"award files scored: {len(r['awards'])}; wrote {OUT.relative_to(ROOT)}")
