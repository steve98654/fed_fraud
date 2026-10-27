# General Services Administration: one-page brief

**Priority:** 6 of 33 (score 3.7). **FY2026 outlays:** $38B (USAspending).
**As of:** 2026-10-27. Public data only.

## Bottom line

GSA is the best technical partner in government for this program because it
owns the data spine every brief uses: SAM.gov (entities and exclusions),
FPDS (contracts) and the Multiple Award Schedules that other agencies buy
through. Its own fraud risks are schedule pricing fraud, purchase card misuse
and lease fraud. A GSA pilot improves the shared data for every other agency
at once.

## Exposure

- $38B in outlays (leases, Federal Buildings Fund, IT and schedules), plus
  tens of billions a year in orders other agencies place on GSA schedules.
- Schedule contractors who misstate commercial pricing or sell non-compliant
  goods are a recurring False Claims Act case type.
- GSA SmartPay purchase and travel cards carry misuse risk across agencies.

## Public data we can use

- **SAM.gov:** entity registrations, owners, addresses, exclusions.
- **FPDS / USAspending:** every contract action, including schedule orders.
- **GSA Advantage and CALC** schedule price data.
- **GSA lease inventory** (lessor, location, rent).
- **GSA OIG** reports and DOJ settlements.

## Detection plays

1. **Price outliers:** schedule prices far above peers for the same item or
   labor category.
2. **Registration red flags:** many SAM.gov registrations at one address,
   recycled officers across UEIs, and firms that re-register after exclusion.
3. **Lease risk:** lessors linked to officials or shell entities, and rents
   far above local comparables.

## First prototype

A SAM.gov registration integrity report: clusters of entities sharing
addresses, officers or bank-like identifiers, ranked by award dollars. This
is the SBA entity screen run government-wide.

## Limits

Purchase card transactions and SAM.gov sensitive fields (bank data, TINs)
are not public.

## Who to take it to

GSA Federal Acquisition Service, the Integrated Award Environment (SAM.gov)
team, and GSA OIG.

## Sources

- [SAM.gov data services](https://sam.gov/data-services)
- [GSA SmartPay audit repository](https://smartpay.gsa.gov/guidance-and-audits/audits/)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
