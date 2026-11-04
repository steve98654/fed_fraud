# Recovery and ROI model: the business case by program

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 3 of 10
(see the [extensions overview](../extensions.md)). Model:
`analytics/roi/model.py`; inputs: `analytics/roi/programs.csv`; results:
`docs/proposals/data/roi_results.csv`. Interactive version on the site at
`/tools/roi/`. **These are estimates for a business case, not savings.
Savings stay Pending until an Inspector General or DOJ confirms them.**

## Bottom line

Leaders fund what pays back. Starting from each program's reported
improper payments (GAO, FY2025) and a stated chain of assumptions, the
model estimates the five-year present value of what detection tooling would
prevent or recover, against what it costs to build, run and review.

- **The large health and benefit programs pay back many times over even on
  cautious assumptions.** Medicare fee-for-service: median net benefit about
  $880M over five years, roughly 10 times cost; Medicaid about $450M
  (8 times), even with only a fifth of Medicaid reachable through state data.
- **The break-even bar is low.** For Medicare, the tooling pays for itself if
  it catches 0.2% of the improper dollars it can see that current controls
  miss. For SNAP it is 0.8%. A pilot only has to beat that number.
- **Small programs do not pay back on their own.** OPM retirement, FEMA
  Public Assistance and the closed Shuttered Venue grant program have a 50%
  or lower chance of positive net benefit as stand-alone builds. They should
  ride on shared screens (cross-agency matching, exclusion checks), not get
  their own tooling.

## Results by program

| Program | Improper | Benefit / cost | Net, P10 to P50 | ROI | Break-even |
| --- | --- | --- | --- | --- | --- |
| Medicare FFS | $28.8B | $993M / $100M | $499M to $884M | 9.7x | 0.17% |
| Medicaid | $37.4B | $516M / $62M | $249M to $449M | 8.0x | 0.32% |
| EITC | $21.1B | $291M / $45M | $131M to $244M | 6.4x | 0.57% |
| SSI | $7.3B | $252M / $42M | $111M to $208M | 5.9x | 0.66% |
| SNAP | $10.2B | $211M / $38M | $89M to $171M | 5.4x | 0.79% |
| VA (7 programs) | $3.9B | $135M / $32M | $49M to $102M | 4.2x | 1.2% |
| HUD rental aid | $4.3B | $119M / $31M | $41M to $87M | 3.8x | 1.4% |
| UI | $5.6B | $116M / $31M | $39M to $85M | 3.8x | 1.4% |
| SSDI | $2.3B | $79M / $28M | $20M to $51M | 2.9x | 2.1% |
| SVOG (closed) | $10.1B | $32M / $31M | -$14M to $1M | 1.0x | 6.9% |
| OPM retirement | $0.4B | $20M / $23M | -$13M to -$3M | 0.9x | 8.3% |
| FEMA PA | $0.3B | $12M / $22M | -$18M to -$9M | 0.6x | 13% |

Improper payments are FY2025. Benefit, cost and ROI are five-year medians;
break-even is the catch rate at which net benefit is zero. Figures are
present values at a 2% real discount rate, from 20,000 Monte Carlo draws. Run `python3 analytics/roi/model.py` to reproduce them.

## 1. The chain

For each program and year:

- **caught** = improper payments x reach x detectable x new detection x ramp
- **flagged** = caught / precision (what reviewers have to look at)
- **benefit** = caught x [prevent + (1 - prevent) x recovery] x (1 + deterrence)
- **cost** = build (year 1) + run (every year) + review cost x flagged

Closed programs get no prevention and no deterrence: only recovery on the
stock of improper payments, spread over three years.

## 2. Assumptions and why

Each share is drawn from a triangular distribution (low, likely, high).
These are the numbers to argue about with an agency, and the pilot is
designed to measure the three that matter most (new detection, precision,
prevent).

| Assumption | Low | Likely | High | Basis |
| --- | --- | --- | --- | --- |
| Reach | per program (0.2 to 1.0) | | | Share of program dollars our data access covers within five years. Medicaid and EITC 0.2 (state data, tax-data limits); Medicare 0.5; OPM 0.8 |
| Detectable | 25% | 40% | 55% | Share of improper dollars with a data trace (identity, eligibility, billing pattern) rather than a missing document. Agencies report most improper payments as documentation errors; the detectable share is what the screens can reach |
| New detection | 3% | 8% | 15% | Share of detectable dollars our screens catch that current controls miss. The single most uncertain number; the pilot measures it |
| Precision | 30% | 50% | 70% | Share of flagged dollars confirmed on review. Sets reviewer workload |
| Prevent | 20% | 45% | 70% | Share caught before payment. Needs pre-payment integration (Do Not Pay, claims edits) |
| Recovery | 5% | 15% | 30% | Share recovered when caught after payment. Pay-and-chase recovers little; GAO and OIG reports show low recovery rates |
| Deterrence | 0% | 5% | 15% | Extra benefit from fewer attempts once controls are known |
| Build | $2M | $4M | $8M | One-time, per program, on the shared platform |
| Run | $1.5M | $3M | $6M | Per year, per program: data, compute, analysts |
| Review cost | 1% | 2% | 4% | Review and investigation cost per flagged dollar |
| Ramp | 25%, 60%, 100%, 100%, 100% | | | Capacity reached in years 1 to 5 |
| Discount rate | 2% real | | | OMB Circular A-94 (2023 revision) default; check the current value |

## 3. What the model does not count

- Criminal fines, False Claims Act damages and penalties (often larger than
  the recovered overpayment; treble damages under 31 U.S.C. 3729).
- Fraud outside improper payment estimates. GAO estimated total fraud
  losses at $233B to $521B a year (GAO-24-105833), well above reported
  improper payments, so starting from improper payments is conservative.
- Shared-platform savings: the second and later programs reuse the entity
  spine and screens, so build cost per program falls.
- Benefits to states (the state share of Medicaid, UI administration).

## 4. Sensitivity

The ranking is driven by improper dollars x reach. Within a program, net
benefit moves almost one for one with new detection and prevent. Precision
matters through review cost only; at 30% precision review cost roughly
doubles, but no large program turns negative. The break-even column is the
best single number for a leader: if the pilot shows a catch rate above it,
scale; if not, stop.

## 5. How to use it in a proposal

1. Quote the program's row, the break-even rate and the P10 (pessimistic)
   net, not the median.
2. Replace our assumptions with the agency's own where it has them
   (recovery rates, review cost).
3. State that savings stay Pending until confirmed, and that the pilot
   exists to measure the uncertain assumptions.
