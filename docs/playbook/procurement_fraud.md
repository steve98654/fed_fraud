# Procurement and contract fraud: bid rigging, change orders and false set-asides

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 6 of 10
(see the [extensions overview](../extensions.md)). Reference code:
`analytics/forensic/procurement.py` and `analytics/forensic/bids.py`,
tested on synthetic data only.

## Bottom line

The government buys about $750 billion a year of goods and services
through contracts, and every award is published in FPDS and USAspending.
Three schemes leave traces in those records: **weak or rigged
competition**, **contracts that grow after they are won**, and **small
business set-asides won by firms that are not small or do not do the
work**. This extension turns each into a screen that runs on public data
across every agency, so DoD-1, VA-1, GSA-1 and DOT-1 share one engine.

## 1. Data

| Source | What it gives | Notes |
| --- | --- | --- |
| FPDS / USAspending contract transactions | Every action: base and current value, offers received, extent competed, set-aside type, NAICS, PSC, office, modifications with reason codes | Award-level and transaction-level downloads; fields named as in the USAspending data dictionary |
| SAM.gov entity data | Size representations by NAICS, socioeconomic certifications, parents, officers, addresses | Self-certified; size is measured at offer |
| SBA Dynamic Small Business Search, certification lists (8(a), HUBZone, WOSB, VetCert) | Certified status and dates | VA's SDVOSB verification moved to SBA in 2023 |
| FFATA subaward reports | First-tier subcontracts on larger awards | Underreported; absence is itself a signal |
| SBA size and status protest decisions, OHA decisions | Firms found other than small | Labeled cases for validation |
| DOJ Procurement Collusion Strike Force and contractor fraud releases | Charged cases | Labeled cases |
| State DOT bid tabulations | All bids, not only winners | For sealed-bid screens (DOT-1) |

## 2. Screens

### 2.1 Competition

- **Single-offer rate** by office and market: competed awards that drew
  one offer. Persistently high rates point to tailored requirements or a
  steered market. Compared within NAICS, since some markets are thin.
- **Incumbent lock-in:** Herfindahl index of vendor shares by office and
  NAICS; high concentration with mostly single-offer competitions.
- **Sealed-bid distribution screens and rotation tests** (handbook section
  6): low coefficient of variation, high relative distance, winners taking
  turns.

### 2.2 Change-order and modification inflation

- **Growth ratio:** current value / base and all options value at award.
  Robust z-score of its log within NAICS; awards above 3.5 are reviewed.
- **Many modifications just under an approval threshold** (warrant limits,
  cost or pricing data thresholds, legal review levels): the modification
  version of a split purchase.
- **Out-of-scope growth:** modifications coded as "additional work (new
  agreement)" or "supplemental agreement" on sole-source bridges.

### 2.3 Set-aside eligibility

| Check | Rule | Source |
| --- | --- | --- |
| Size | Average annual receipts or employees above the NAICS size standard | 13 CFR 121.201; SAM representations, public filings |
| Pass-through | Prime pays more than the limit to firms that are not similarly situated | FAR 52.219-14: 50% for services and supplies, 85% general construction, 75% specialty trade |
| Affiliation and ostensible subcontractor | Set-aside winner shares owners, officers, address or bank account with a large firm | 13 CFR 121.103; network method |
| Front-company profile | Set-aside share of revenue jumps by more than 40 points while awards at least double | Award history |
| Status after award | Firm acquired by or merged into a large business but keeps receiving set-aside orders without recertifying | SAM, FPDS recertification fields |

Each reason is a question for the contracting officer or SBA, not a
finding. Size is measured on the date of the offer, and affiliation needs
the facts behind a shared address.

## 3. Thresholds to know

Thresholds change with inflation adjustments (FAR 1.109). The October 2025
adjustment raised the micro-purchase threshold to $15,000 and the
simplified acquisition threshold to $350,000; check the current FAR 2.101
before relying on these. Bunching tests (handbook section 5.4) look for
excess awards just under each threshold.

## 4. Validation

- Positive set: SBA size protests sustained, OHA decisions, DOJ set-aside
  fraud cases, suspension and debarment records with procurement causes.
- Release bar as in the review plan: known cases at least five times more
  common in the top 5% than overall.
- False positives to expect: legitimate scope growth on research and
  development, emergency buys, sole-source awards under statute, joint
  ventures that are allowed to share resources.

## 5. Where it runs first

| Idea | Screens | Partner |
| --- | --- | --- |
| DOD-1 set-aside fronts | Size, pass-through, affiliation | DoD OIG, DCIS, SBA OIG |
| DOD-2 price and growth outliers | Growth ratio, threshold bunching | DoD OIG, DCAA |
| VA-1 SDVOSB fronts | Affiliation, front profile | VA OIG |
| GSA-1 schedule and MAS orders | Single-offer, lock-in, growth | GSA OIG |
| DOT-1 highway bid rigging | Sealed-bid screens, rotation | DOT OIG, DOJ Antitrust Division |

## 6. Next steps

1. Pull FY2021-FY2026 contract transactions for DoD, VA and GSA (public).
2. Build the growth and single-offer tables by office (week 6).
3. Back-test set-aside checks on sustained size protests (week 8).
