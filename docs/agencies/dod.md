# Department of War (Defense): one-page brief

**Priority:** 2 of 7 (score 4.3). **As of:** 2026-10-25. Public data only.

## Bottom line

DoD contracting is the fastest technical win. It runs on the same public
data the SBA work already uses (SAM.gov, FPDS, USAspending), and DoD awards
far more contract dollars than any other agency (roughly $400B+ a year;
approximate, from USAspending). Small business set-aside and
pass-through fraud is the direct bridge from SBA's 8(a), HUBZone and
women-owned programs.

## Exposure

- DoD's reported improper payment rates are highest in travel pay (11% to
  13% across systems) and include $1.4B in one commercial pay system (GAO,
  FY2025).
- The bigger risk is procurement fraud that payment sampling does not catch:
  fake small businesses, pass-through fronts, bid rigging and inflated
  pricing. These are recurring DCIS and DOJ cases.

## Public data we can use

- **FPDS / USAspending** contract actions: vendor UEI, set-aside type,
  competition, modifications, subcontract reports.
- **SAM.gov entity and exclusion records:** addresses, officers, business
  type certifications, registration dates.
- **SBA certification lists** (8(a), HUBZone, WOSB, VetCert).
- **DCIS and DOJ press releases** for labeled cases.

## Detection plays

1. **Front companies:** set-aside winners that are new, share addresses or
   officers with large firms, or subcontract most work to a non-eligible
   firm.
2. **Collusion signals:** "competitors" sharing officers, addresses or phone
   numbers, rotating wins, and identical bids.
3. **Award anomalies:** sole-source awards just under thresholds, rapid
   modification growth, and payees linked to excluded parties.

## First prototype

A contractor integrity screen over DoD set-aside awards for the last five
fiscal years. Reuse the SBA entity-resolution pipeline, add FPDS award
features, and rank vendors with stated reasons. Validate against DOJ and
DCIS cases.

## Limits

Invoices and payments below the award level are not public, so this finds
risky vendors and awards, not individual false invoices. Classified work is
excluded.

## Who to take it to

The DoD Comptroller and Office of Small Business Programs, DCIS / DoD OIG,
and DOJ's Procurement Collusion Strike Force.

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [DOJ whistleblower program scope](https://www.justice.gov/fraud/whistleblower)
