# Treasury (IRS and Fiscal Service): one-page brief

**Priority:** 8 of 33 (score 3.5). **FY2026 outlays:** $1,975B (USAspending;
mostly interest on the debt). **As of:** 2026-10-27. Public data only.

## Bottom line

Treasury holds the largest single fraud-prone payment outside health care:
refundable tax credits paid through the IRS. The Earned Income Tax Credit
alone had $21.1B in improper payments in FY2025, and the pandemic Employee
Retention Credit drew billions in fraudulent claims. Taxpayer data are
confidential, so public work has to start from geography, preparers and
promoters rather than individual returns. The payoff is large, but this is a
proposal-first agency.

## Exposure

- EITC: $21.1B improper (32.7%). Additional Child Tax Credit: 13.6% rate.
  American Opportunity Tax Credit: 30.7%. Premium Tax Credit: 31.6%. (GAO,
  FY2025)
- Employee Retention Credit: IRS Criminal Investigation had opened 545 ERC
  cases involving more than $5.6B by February 2025, out of 2,039 COVID fraud
  investigations totaling $10B.
- Fiscal Service disburses most federal payments and runs Do Not Pay, which
  makes it the natural home for any cross-agency screen.

## Public data we can use

- **IRS Statistics of Income (SOI) ZIP code data:** EITC and refundable
  credit counts and dollars by ZIP, by year.
- **IRS Return Preparer data and enforcement releases:** preparer injunctions
  and DOJ Tax Division cases name preparers and promoters.
- **PPP loan-level data (SBA):** employer names, addresses and jobs reported,
  which can be set against public ERC promoter cases.
- **IRS-CI and DOJ press releases** as labeled examples.

## Detection plays

1. **Credit hot spots:** ZIP codes where EITC or ACTC claim rates jump far
   above what income and household data predict, flagged for preparer review.
2. **Promoter networks:** link charged ERC and EITC promoters to the
   businesses, addresses and preparers that recur across cases.
3. **Pandemic overlap:** businesses with PPP loans that also appear in ERC
   cases, to estimate double dipping and find similar unreviewed firms.

## First prototype

An EITC hot-spot map from SOI ZIP data, with a ranked list of anomalous
areas and the known preparer cases inside them. Validate against DOJ preparer
injunctions.

## Limits

Returns, preparer identifiers on returns, and ERC claims are confidential
(26 U.S.C. 6103). Public data can only point to places and promoters; return
level scoring needs an IRS partnership.

## Who to take it to

IRS Return Preparer Office and Criminal Investigation, TIGTA, Treasury's
Office of Payment Integrity (Do Not Pay), and DOJ Tax Division.

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [IRS-CI: 2,039 COVID fraud investigations, 545 ERC cases (March 2025)](https://irs.gov/compliance/criminal-investigation/five-years-post-cares-act-irs-ci-has-launched-2039-covid-fraud-investigations-totaling-10b-in-attempted-fraud)
- [CRFB: FY2025 improper payments by program](https://www.crfb.org/blogs/federal-improper-payments-total-186-billion-fy-2025)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
