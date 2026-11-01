# FCC-1: E-Rate provider and consultant network map

**For:** FCC Enforcement Bureau and OIG, USAC Internal Audit.
**Weeks:** 8-11 (results by 2027-01-29). **Brief:** [FCC](../agencies/fcc.md).

## The problem

E-Rate pays for school and library internet. Some providers, consultants
and school officials rig the bidding: one bid, a friendly consultant and a
high price, sometimes with a kickback. These are long-running DOJ cases.
USAC publishes the bids, commitments and disbursements, so steering is
visible in the data.

## Data

- USAC Open Data: E-Rate FCC Forms 470 and 471, commitments and
  disbursements by applicant and provider, funding years 2016-2026.
- FCC Form 499 filer database; USAC suspensions and FCC enforcement
  actions.

## Detection method

1. **Single-bid share** by consultant and provider.
2. **Price outliers:** price per unit against peers for the same service.
3. **Links:** providers and consultants sharing addresses or officers.

## Validation

Back-test on E-Rate kickback and bid-rigging cases and USAC suspensions.

## Exposure (public figures, not savings)

- FCC outlays: $10.1B in FY2026. Lifeline: about 9% improper in FY2025
  (about $76M).
- E-Rate dollars in flagged relationships will be measured from USAC data
  in week 8.
- Savings from this work: **Pending.**

## What we ask for

- **Now:** an FCC OIG or USAC Internal Audit contact; current open matters
  to avoid duplication.
- **Phase 2:** full E-Rate bid documents, to see losing bids and
  evaluation scores.

## What you get, and when

By week 11: an E-Rate network map with ranked provider-consultant
relationships and reasons, and a review memo.

## Limits

Rural areas often have only one provider, so single bids are normal there;
the screen compares like with like.

## Sources

- [PaymentAccuracy.gov: USF Lifeline](https://paymentaccuracy.gov/program/fcc-universal-service-fund-lifeline)
- [USAC investigation documents](https://www.usac.org/about/contact-usac/submit-a-whistleblower-alert/investigation-documents/)
- [DOJ: Illinois technology company owner pleads guilty to E-Rate fraud](https://www.justice.gov/opa/pr/owner-illinois-technology-company-pleads-guilty-scheme-defraud-federal-e-rate-program)
