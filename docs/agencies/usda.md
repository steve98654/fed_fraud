# USDA: one-page brief

**Priority:** 4 of 33 (score 3.9). **FY2026 outlays:** $220B (USAspending).
**As of:** 2026-10-27 (first written 2026-10-25). Public data only.

## Bottom line

USDA brings two strong targets: SNAP retailer trafficking and child meal
sponsor fraud, the pattern behind Minnesota's $250M Feeding Our Future case.
Both are DOJ whistleblower priorities (SNAP and day care). Public data name
the retailers and the grantees, but not the transactions, so we score
entities, not purchases.

## Exposure

- SNAP: $10.2B improper (10.9%). Child and Adult Care Food Program: 10.5%.
  Emergency Conservation Program: 55.5%. Noninsured Crop Disaster
  Assistance: 10.6%. (GAO, FY2025)
- Feeding Our Future: $250M scheme, 78 people charged.

## Public data we can use

- **SNAP authorized retailer data** (store type, location, authorization
  dates) and published retailer disqualification actions.
- **USAspending** grants and payments, including farm program and nutrition
  grants to states and sponsors.
- **State CACFP sponsor and site lists**, where states publish them.
- **USDA OIG reports** and DOJ releases.

## Detection plays

1. **Retailer outliers:** small stores in dense clusters, new authorizations
   near already disqualified stores, and owners linked to past violators.
2. **Meal sponsor anomalies:** sites claiming more meals than local child
   population supports, sudden growth, and shared sponsors across many sites.
3. **Farm disaster payments:** recipients far above local peers, or payments
   tied to entities with shared officers.

## First prototype

A SNAP retailer risk map for two states, scoring each store against nearby
peers and known disqualified stores, plus a sponsor screen for one state that
publishes CACFP site lists.

## Limits

SNAP redemption data by store are not public, so trafficking is inferred
from location and ownership, not sales. CACFP data vary by state.

## Who to take it to

The Food and Nutrition Service (Retailer Operations), USDA OIG, and state
SNAP and child nutrition agencies.

## Related briefs

[treasury.md](treasury.md) and [ssa.md](ssa.md) (other means-tested benefits), [doe.md](doe.md) (SBIR screen).

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [NBC: Minnesota child care findings and Feeding Our Future](https://www.nbcwashington.com/news/national-international/minnesota-department-finds-child-care-centers-targeted-viral-video-open/4036664/)
- [DOJ whistleblower program scope](https://www.justice.gov/fraud/whistleblower)
