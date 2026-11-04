"""Recovery and ROI model: what the detection tooling could return per
program, against what it costs, with the uncertainty stated.

The model starts from each program's reported improper payments (GAO,
PaymentAccuracy.gov) and walks down a chain of shares, each drawn from a
triangular distribution whose (low, likely, high) values are written in
ASSUMPTIONS below (and, for `reach`, per program in programs.csv) and argued in docs/proposals/roi_model.md:

    caught   = improper x reach x detectable x new_detection x ramp(year)
    flagged  = caught / precision                     (what reviewers see)
    benefit  = caught x [prevent + (1 - prevent) x recovery] x (1 + deterrence)
    cost     = build (year 1) + run (every year) + review_cost x flagged

Closed programs (pandemic programs that no longer pay) get no prevention or
deterrence: only recovery, on the stock of improper payments, spread over
the first three years.

Results are estimates for a business case, not savings. Under the site
rules savings stay "Pending" until an Inspector General or DOJ confirms
them; this model says what a pilot would need to show to justify scale-up.

Run from the repository root:

    python3 analytics/roi/model.py            # writes docs/proposals/data/
"""
from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]

# (low, likely, high) for triangular draws. Shares are fractions.
ASSUMPTIONS: dict[str, tuple[float, float, float]] = {
    "detectable": (0.25, 0.40, 0.55),      # share of improper dollars with a trace in data the screens see
    "new_detection": (0.03, 0.08, 0.15),   # share of that the agency's current controls miss and the screens catch
    "precision": (0.30, 0.50, 0.70),       # share of flagged dollars confirmed improper on review
    "prevent": (0.20, 0.45, 0.70),         # share caught before payment (needs pre-payment integration)
    "recovery": (0.05, 0.15, 0.30),        # share of post-payment dollars recovered
    "deterrence": (0.00, 0.05, 0.15),      # extra benefit from fewer attempts, as a share of direct benefit
    "build_usd": (2e6, 4e6, 8e6),          # one-time, per program
    "run_usd": (1.5e6, 3e6, 6e6),          # per year, per program
    "review_cost": (0.01, 0.02, 0.04),     # review and investigation cost per flagged dollar
}
RAMP = [0.25, 0.60, 1.0, 1.0, 1.0]  # share of steady-state capacity reached in years 1-5
DISCOUNT = 0.02  # real discount rate; OMB Circular A-94 (2023 revision) default, check the current value
YEARS = len(RAMP)


@dataclass
class Program:
    agency: str
    program: str
    improper_usd: float
    status: str  # "open" or "closed"
    first_pilot: str
    source: str
    reach: float  # share of program dollars the team's data access covers within five years


def load_programs(path: Path = ROOT / "analytics/roi/programs.csv") -> list[Program]:
    with open(path, newline="") as f:
        return [Program(r["agency"], r["program"], float(r["improper_usd"]), r["status"], r["first_pilot"], r["source"], float(r["reach"]))
                for r in csv.DictReader(f)]


def draw(n: int, rng: np.random.Generator, assumptions=ASSUMPTIONS) -> dict[str, np.ndarray]:
    return {k: rng.triangular(lo, mode, hi, n) if hi > lo else np.full(n, mode) for k, (lo, mode, hi) in assumptions.items()}


def likely(assumptions=ASSUMPTIONS) -> dict[str, np.ndarray]:
    """The single 'likely' scenario (every assumption at its mode)."""
    return {k: np.array([mode]) for k, (_, mode, _) in assumptions.items()}


def simulate(p: Program, a: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
    """Present-value benefit, cost, net and ROI over YEARS for each draw."""
    n = len(a["detectable"])
    pv_benefit = np.zeros(n)
    pv_cost = np.zeros(n)
    cum_net = np.zeros(n)
    payback = np.full(n, np.inf)
    open_ = p.status == "open"
    for t in range(YEARS):
        disc = (1 + DISCOUNT) ** -(t + 0.5)  # mid-year convention
        if open_:
            base = p.improper_usd
        else:
            base = p.improper_usd / 3 if t < 3 else 0.0
        caught = base * p.reach * a["detectable"] * a["new_detection"] * RAMP[t]
        flagged = caught / a["precision"]
        prevent = a["prevent"] if open_ else 0.0
        deter = a["deterrence"] if open_ else 0.0
        benefit = caught * (prevent + (1 - prevent) * a["recovery"]) * (1 + deter)
        cost = a["run_usd"] + a["review_cost"] * flagged + (a["build_usd"] if t == 0 else 0.0)
        pv_benefit += benefit * disc
        pv_cost += cost * disc
        cum_net += benefit - cost
        payback = np.where(np.isinf(payback) & (cum_net >= 0), t + 1, payback)
    return {"pv_benefit": pv_benefit, "pv_cost": pv_cost, "net": pv_benefit - pv_cost,
            "roi": pv_benefit / pv_cost, "payback_year": payback}


def summarize(p: Program, n: int = 20000, seed: int = 2026) -> dict:
    rng = np.random.default_rng(seed)
    mc = simulate(p, draw(n, rng))
    mode = simulate(p, likely())
    pct = lambda x: {q: float(np.percentile(x, q)) for q in (10, 50, 90)}
    pb = mc["payback_year"]
    return {
        "agency": p.agency,
        "program": p.program,
        "status": p.status,
        "first_pilot": p.first_pilot,
        "improper_usd": p.improper_usd,
        "source": p.source,
        "reach": p.reach,
        "pv_benefit": pct(mc["pv_benefit"]),
        "pv_cost": pct(mc["pv_cost"]),
        "net": pct(mc["net"]),
        "roi": pct(mc["roi"]),
        "likely": {k: float(v[0]) for k, v in mode.items() if k != "payback_year"},
        "p_positive": float((mc["net"] > 0).mean()),
        "median_payback_year": float(np.median(pb)) if np.isfinite(np.median(pb)) else None,
    }


def breakeven_new_detection(p: Program) -> float:
    """Lowest new_detection share (others at their likely values) at which
    the five-year net is zero: the single number a pilot must beat."""
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        a = likely()
        a["new_detection"] = np.array([mid])
        if simulate(p, a)["net"][0] > 0:
            hi = mid
        else:
            lo = mid
    return hi


def main(out_dir: Path = ROOT / "docs/proposals/data") -> list[dict]:
    progs = load_programs()
    rows = []
    for p in progs:
        s = summarize(p)
        s["breakeven_new_detection"] = breakeven_new_detection(p)
        rows.append(s)
    rows.sort(key=lambda r: r["net"][50], reverse=True)
    out_dir.mkdir(parents=True, exist_ok=True)
    meta = {"assumptions": {k: list(v) for k, v in ASSUMPTIONS.items()}, "ramp": RAMP, "discount": DISCOUNT,
            "years": YEARS, "note": "Estimates for a business case, not savings. Savings stay Pending until confirmed."}
    (out_dir / "roi_results.json").write_text(json.dumps({"meta": meta, "programs": rows}, indent=1) + "\n")
    with open(out_dir / "roi_results.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["agency", "program", "status", "improper_usd", "pv_benefit_p10", "pv_benefit_p50", "pv_benefit_p90",
                    "pv_cost_p50", "net_p10", "net_p50", "net_p90", "roi_p50", "p_positive", "breakeven_new_detection"])
        for r in rows:
            w.writerow([r["agency"], r["program"], r["status"], f"{r['improper_usd']:.0f}",
                        *(f"{r['pv_benefit'][q]:.0f}" for q in (10, 50, 90)), f"{r['pv_cost'][50]:.0f}",
                        *(f"{r['net'][q]:.0f}" for q in (10, 50, 90)), f"{r['roi'][50]:.2f}",
                        f"{r['p_positive']:.3f}", f"{r['breakeven_new_detection']:.4f}"])
    return rows


if __name__ == "__main__":
    rows = main()
    for r in rows:
        print(f"{r['agency']:6} {r['program'][:36]:36} net P50 ${r['net'][50] / 1e6:10,.0f}M  "
              f"ROI P50 {r['roi'][50]:6.1f}x  P(net>0) {r['p_positive']:.2f}  breakeven {r['breakeven_new_detection']:.2%}",
              file=sys.stdout)
