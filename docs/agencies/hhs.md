# HHS (Medicare and Medicaid): one-page brief

**Priority:** 1 of 33 (score 4.8). **FY2026 outlays:** $2,687B (USAspending).
**As of:** 2026-10-27 (first written 2026-10-25). Public data only.

## Bottom line

HHS is where the money and the data meet. Medicare and Medicaid had about
$90B in FY2025 improper payments, and CMS publishes provider-level billing,
enrollment and ownership data that let us score individual providers. Start
with hospice and home health, which CMS froze to new Medicare enrollment in
May 2026 and DOJ named as whistleblower priorities.

## Exposure

- Medicaid: $37.4B improper (6.1%). Medicare fee-for-service: $28.8B (6.6%).
  Medicare Advantage: $23.7B (6.1%). Head Start: 10.3% rate. (GAO, FY2025)
- CMS imposed a six-month nationwide moratorium on new hospice and home
  health enrollments on 2026-05-13, citing sham hospices and patients who
  were not terminally ill.
- Payment suspensions hit about 800 Los Angeles hospices and home health
  agencies; HHS froze federal child care payments to Minnesota in Dec 2025.

## Public data we can use

- **Medicare Provider Utilization and Payment** (by provider and service),
  Part D prescribers, and the hospice and home health provider files.
- **Provider ownership data** for hospices, home health agencies and nursing
  homes (owners, ownership changes, shared owners).
- **NPPES** (NPI registry: addresses, taxonomies, enumeration dates).
- **HHS-OIG LEIE** exclusion list and **Open Payments**.
- **DOJ and HHS-OIG enforcement releases** as labeled examples.
- Head Start and child care grants on **USAspending**.

## Detection plays

1. **Hospice and home health clusters:** many new providers at shared
   addresses or with shared owners, fast billing ramp after enrollment,
   unusually long stays or live-discharge rates versus peers.
2. **Ownership networks:** owners or managers linked to LEIE-excluded parties
   or to providers already suspended; serial ownership changes.
3. **Outlier billing:** providers far above peers in services per patient,
   new high-cost codes, or patterns matching past DOJ cases (for example
   COVID and respiratory test billing).

## First prototype

A hospice and home health risk map for two hot spots (Los Angeles County and
Minnesota). Each provider gets a score with the reasons behind it, and the
view shows the owner network. Validate against providers already suspended or
charged.

## Limits

Public files lag 1 to 2 years and are aggregated (small counts suppressed).
Medicaid claims are state-run and not public, so Medicaid work starts from
provider enrollment and ownership, not claims.

## Who to take it to

CMS Center for Program Integrity, HHS-OIG, and the DOJ Health Care Fraud Unit.

## Related briefs

[opm.md](opm.md) (FEHB uses the same provider screen), [ssa.md](ssa.md) (death data), [pcortf.md](pcortf.md).

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [WilmerHale: CMS hospice and home health moratorium (May 2026)](https://www.wilmerhale.com/en/insights/client-alerts/20260521-cms-announces-moratorium-on-new-medicare-enrollment-for-hospices-and-home-health-agencies)
- [NBC: Minnesota child care findings and HHS payment freeze](https://www.nbcwashington.com/news/national-international/minnesota-department-finds-child-care-centers-targeted-viral-video-open/4036664/)
- [DOJ whistleblower program priority areas](https://www.justice.gov/fraud/whistleblower)
