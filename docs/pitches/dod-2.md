# DOD-2: Bidder collusion networks by market

**For:** DOJ Procurement Collusion Strike Force, DCIS. **Weeks:** 4-7
(results by 2026-12-18). **Brief:** [DoD](../agencies/dod.md).

## The problem

When "competitors" for a contract are secretly under common control, or
take turns winning, the government pays more and gets no real competition.
The Procurement Collusion Strike Force prosecutes these cases, but finding
them usually depends on a tip. Shared identifiers among bidders and
regular win patterns are visible in public award and registration data.

## Data

- FPDS and USAspending DoD contract actions FY2021-FY2026, with offers
  received, contracting office and NAICS code.
- SAM.gov entities (addresses, phones, points of contact) and exclusions.
- DOJ and Strike Force case releases for labels.

## Detection method

1. **Shared control:** firms in the same market sharing officers,
   addresses or phones.
2. **Win rotation:** winners that take turns by contracting office and
   NAICS code, with few offers per award.
3. **Network view:** each market drawn as a graph of firms and shared
   identifiers, ranked by award dollars.

## Validation

Back-test on Strike Force and DOJ bid-rigging cases 2018-2026.

## Exposure (public figures, not savings)

- Collusion inflates prices on competed contracts; the dollars in flagged
  markets will be measured from FPDS in week 4.
- Savings from this work: **Pending.**

## What we ask for

- **Now:** a Strike Force contact; the markets it considers most at risk.
- **Phase 2:** losing bid data from DoD contracting systems, which public
  data omit and which collusion tests need.

## What you get, and when

By week 7: a collusion network view by market with ranked firm groups,
reasons and a review memo.

## Limits

Public data show winners, not losing bids. Affiliated firms may compete
legally if they disclose the affiliation.

## Sources

- [DOJ whistleblower program scope](https://www.justice.gov/fraud/whistleblower)
