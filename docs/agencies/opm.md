# Office of Personnel Management: one-page brief

**Priority:** 11 of 33 (score 3.3). **FY2026 outlays:** $201B (USAspending).
**As of:** 2026-10-27. Public data only.

## Bottom line

OPM runs two big payment streams: federal retirement ($109B in FY2025) and
the Federal Employees Health Benefits program (about $70B, 8.2 million
members). Retirement error rates are low, but GAO found in April 2026 that
FEHB paid deceased, incarcerated and excluded providers, and that OPM's own
debarment list is out of step with the HHS and SAM exclusion lists. That
cross-list gap is something we can measure with public data alone.

## Exposure

- Federal Retirement Services: $109.4B outlays, about $364M improper (0.33%)
  in FY2025.
- FEHB: about 400 deceased providers paid for services at least 50 days
  after death; over 2,000 claims from providers excluded elsewhere; over
  2,500 claims from providers OPM had already debarred. (GAO, CY2022 claims)
- Over 85% of OPM OIG's debarment records lack an NPI, and at least 1,200
  LEIE entries that meet OPM's debarment criteria are missing from its list.

## Public data we can use

- **HHS-OIG LEIE, SAM.gov exclusions, and OPM OIG's debarment list.**
- **NPPES** NPI registry (addresses, taxonomies, deactivation dates).
- **CMS provider data** to profile FEHB-overlapping providers.
- **OPM OIG investigative summaries** as labeled cases.

## Detection plays

1. **Exclusion list reconciliation:** match the three exclusion lists on name,
   NPI, address and license to find providers barred in one program and not
   another.
2. **Dead and deactivated providers:** NPIs deactivated or tied to deceased
   individuals that still look active in carrier networks.
3. **Cross-program spillover:** providers flagged in Medicare work (see
   [hhs.md](hhs.md)) who also serve FEHB members.

## First prototype

An exclusion-list reconciliation report: every provider excluded by HHS or
SAM but missing from OPM's list, with matched identifiers. This reuses the
HHS provider pipeline almost unchanged.

## Limits

FEHB claims are held by carriers and are not public, so we cannot see what
was paid to whom. Retirement payee data is not public.

## Who to take it to

OPM Healthcare and Insurance, OPM OIG, and FEHB carriers' special
investigation units.

## Sources

- [GAO-26-108139: FEHB provider eligibility risks (April 2026)](https://files.gao.gov/reports/GAO-26-108139/index.html)
- [PaymentAccuracy.gov: OPM Federal Retirement Services](https://paymentaccuracy.gov/program/opm-federal-retirement-services)
- [FedWeek: OPM OIG retirement and FEHB fraud cases](https://www.fedweek.com/issue-briefs/bogus-claims-cashing-checks-of-deceased-ig-cites-cases-of-fehbp-retirement-fraud/)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
