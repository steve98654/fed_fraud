# Securities and Exchange Commission: one-page brief

**Priority:** 21 of 33 (score 2.8). **FY2026 outlays:** $1.8B (USAspending).
**As of:** 2026-10-27. Public data only.

## Bottom line

The SEC spends little, so it is not a fraud target in the usual sense. Its
value here is as a data source and partner: EDGAR filings reveal ownership,
officers and related parties for public companies and many private
offerings, which strengthens the entity spine for every other brief. The SEC
also distributes Fair Fund money to harmed investors, which can attract
fraudulent claims.

## Exposure

- $1.8B in outlays in FY2026, mostly salaries.
- Fair Fund and disgorgement distributions to investors.

## Public data we can use

- **EDGAR:** company filings, Form D private offerings (issuers, officers,
  addresses), insider ownership.
- **SEC litigation and administrative releases** naming individuals.

## Detection plays

1. **Entity enrichment:** link federal contractors and grantees to EDGAR
   officers and Form D issuers to find hidden common control.
2. **Bad-actor overlap:** people barred or charged by the SEC who also run
   federal award recipients.

## First prototype

An EDGAR enrichment step added to the shared entity pipeline, reporting
award recipients whose officers appear in SEC enforcement actions.

## Limits

Most small federal contractors are private and absent from EDGAR except
through Form D.

## Who to take it to

SEC Division of Enforcement (as a data partner), SEC OIG.

## Sources

- [SEC EDGAR search](https://www.sec.gov/edgar/search/)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
