# Transportation: one-page brief

**Priority:** 6 of 33 (score 3.7). **FY2026 outlays:** $125B (USAspending).
**As of:** 2026-10-27. Public data only.

## Bottom line

DOT's money flows mostly as highway, transit and airport grants to states,
which then hire contractors. Its signature fraud is the Disadvantaged
Business Enterprise (DBE) front: a certified small firm that passes work and
money through to a large contractor. That is the same pattern as SBA 8(a)
and set-aside fronts, so the SBA pipeline carries over directly. Bid rigging
on highway lettings is the second pattern.

## Exposure

- Over $125B a year in outlays, most of it federal-aid construction under
  the 2021 infrastructure law.
- DBE pass-through fraud is a recurring DOT OIG and DOJ case type, including
  criminal convictions and False Claims Act settlements.
- DOT does not report a high-risk improper payment program, so most exposure
  is procurement fraud that payment sampling does not see.

## Public data we can use

- **USAspending grants and subawards** for FHWA, FTA and FAA.
- **State Unified Certification Program DBE directories:** certified firms,
  owners, addresses, work codes.
- **State DOT bid tabulations** (many states publish every bid per letting).
- **SAM.gov, FPDS** for direct DOT contracts.
- **DOT OIG and DOJ press releases** as labeled cases.

## Detection plays

1. **DBE fronts:** certified firms that share addresses, phones or officers
   with their prime contractor, have no equipment or staff signals, or work
   almost only for one prime.
2. **Bid rotation:** bidders who take turns winning, submit complementary
   high bids, or share ownership across "competing" firms.
3. **Subaward anomalies:** DBE participation claimed on bids that never shows
   up in subaward reporting.

## First prototype

A DBE integrity screen for two or three states with good public directories
and bid tabs. Reuse the SBA entity-resolution code; rank firms with reasons;
validate against charged DBE cases.

## Limits

Prime-to-subcontractor payments are reported to states, not publicly, and
data quality varies by state. Results point to firms worth review, not proof.

## Who to take it to

DOT OIG, FHWA Office of Civil Rights, state DOT DBE offices, and DOJ's
Procurement Collusion Strike Force.

## Sources

- [DOJ: Pennsylvania man convicted of exploiting the DOT DBE program](https://www.justice.gov/usao-edpa/pr/downingtown-man-convicted-exploiting-usdot-disadvantaged-business-program)
- [DOJ: Ohio construction firm pays $500K over DBE False Claims Act allegations](https://www.justice.gov/opa/pr/ohio-construction-firm-agrees-pay-500000-resolve-false-claims-act-allegations)
- [Troutman: continued prosecution of DBE pass-through cases](https://www.troutman.com/insights/suppliers-beware-us-government-continues-prosecution-of-dbe-fraud-cases-involving-supplies-passed-through-dbes/)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
