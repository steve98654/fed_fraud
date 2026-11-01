# USDA-1: SNAP retailer risk map

**For:** FNS Retailer Operations Division, USDA OIG, state SNAP agencies.
**Weeks:** 6-10 (results by 2027-01-22). **Brief:** [USDA](../agencies/usda.md).

## The problem

SNAP trafficking runs through small stores that trade benefits for cash.
When a store is disqualified, the same owners often reopen nearby under a
new name. Store authorization history is public, so clusters and owner
reuse can be found before transaction data is in hand.

## Data

- FNS historical SNAP retailer data: authorization and end dates, store
  type and location, 2005-2026.
- FNS disqualifications and civil money penalties by store (FOIA).
- Federal court retailer appeal cases; SNAP participation by county.

## Detection method

1. **Clusters:** small stores authorized close to disqualified stores.
2. **Reuse:** owners, addresses and phone numbers that reappear after a
   disqualification.
3. **Density:** authorized stores per SNAP household against similar
   areas.

Two states first, chosen with FNS.

## Validation

Disqualified retailers from the FOIA list are the labels: the screen,
scored on data from before each disqualification, should rank them high.

## Exposure (public figures, not savings)

- SNAP: $10.2B improper in FY2025 (10.9%) (GAO). Improper payments include
  eligibility errors as well as trafficking.
- Savings from this work: **Pending.**

## What we ask for

- **Now:** an FNS Retailer Operations contact; the disqualification list
  (FOIA filed in week 1); the two states FNS most wants covered.
- **Phase 2:** retailer redemption data and EBT transactions through
  states, to detect trafficking from transaction patterns.

## What you get, and when

By week 10: a retailer risk map for two states with ranked stores and
reasons, and a review memo.

## Limits

Public retailer data do not include owner names for every store, and
stores cluster for innocent reasons (dense neighborhoods, food deserts).

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
