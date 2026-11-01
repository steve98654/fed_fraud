# DOD-1: Set-aside contractor integrity screen

**For:** DCIS, DoD OIG, DoD Office of Small Business Programs.
**Weeks:** 3-7 (results by 2026-12-18). **Brief:** [DoD](../agencies/dod.md).

## The problem

Small business set-asides are meant for eligible firms. Fronts win them
and pass the work, and most of the money, to an ineligible firm. These
schemes are recurring DCIS and DOJ cases, and payment sampling does not
catch them because the invoices are real. The signs are in public award
and registration data.

## Data

- FPDS and USAspending DoD contract actions FY2021-FY2026: set-aside type,
  offers received, competition, modifications, place of performance.
- Subaward reports; SAM.gov entities and exclusions.
- SBA certification lists (8(a), HUBZone, WOSB, VetCert) and SBA
  decertifications (FOIA).

## Detection method

1. **New firm, large award:** entities registered recently that win large
   set-aside awards.
2. **Shared identity:** address, phone or point of contact shared with a
   large or ineligible business.
3. **Pass-through:** a high share of subaward dollars going to one
   non-eligible firm.
4. **Excluded links:** vendors sharing identifiers with excluded parties.

Each vendor gets a score and reason codes; a vendor becomes a lead only
with two or more independent signals.

## Validation

Back-test on DCIS and DOJ set-aside fraud cases 2018-2026 from the case
library and on SBA decertifications. Release bar: known cases five times
more common in the top 5%, and half of 25 hand-reviewed vendors judged
worth review.

## Exposure (public figures, not savings)

- DoD's reported improper payments are mostly travel and commercial pay
  ($1.4B in one commercial pay system, GAO FY2025). Set-aside fraud is
  largely outside that sample.
- Set-aside dollars at risk will be measured from FPDS in week 3 and added
  here.
- Savings from this work: **Pending.**

## What we ask for

- **Now:** a DCIS or OSBP contact; recent closed set-aside cases to use as
  labels; guidance on how leads should be packaged.
- **Phase 2:** invoice data (WAWF/PIEE) and subcontract payments through
  DCIS or DoD OIG, to measure real pass-through shares.

## What you get, and when

By week 7: a ranked vendor list with reasons, a review memo and lead
packages for the top vendors. The same code then runs on VA, DHS and other
agencies' awards (shared contractor screen C1).

## Limits

Public data show awards and declared subawards, not who did the work.
Many shared addresses are legitimate (incubators, registered agents) and
are checked before a lead goes out.

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [DOJ whistleblower program scope](https://www.justice.gov/fraud/whistleblower)
