# Justice: one-page brief

**Priority:** 20 of 33 (score 2.9). **FY2026 outlays:** $52B (USAspending).
**As of:** 2026-10-27. Public data only.

## Bottom line

DOJ matters more as our customer than as a target: it runs the whistleblower
program behind america.gov/fraud, the Health Care Fraud Unit, the Trade Fraud
Task Force and the Procurement Collusion Strike Force. Its own fraud risk is
in grants (Office of Justice Programs, the Crime Victims Fund passed through
states) and in prison contracts. The best DOJ product is a case-mining
pipeline that turns its press releases into labeled training data for every
other brief.

## Exposure

- $52B in outlays, mostly salaries, prisons and grants to states and
  nonprofits.
- Grant risk: subgrantees of victim and public safety grants are many and
  small, and DOJ OIG regularly finds unsupported costs.
- No DOJ program is listed as high-risk for improper payments.

## Public data we can use

- **DOJ press releases** (all U.S. Attorneys' offices), searchable and
  structured enough to extract defendants, schemes, programs and dollars.
- **USAspending grants and subawards** for OJP, OVW and COPS.
- **DOJ OIG audit reports** of grantees.
- **FPDS** for Bureau of Prisons and other contracts.

## Detection plays

1. **Case mining (for all agencies):** extract defendant names, entities,
   addresses, schemes and agency from press releases; join to SAM.gov and
   USAspending to make labeled examples.
2. **Grant subrecipient risk:** subgrantees with prior OIG findings, shared
   officers across grantees, or award growth without performance data.
3. **Prison contract outliers:** commissary, medical and telecom vendors with
   prices far above peers.

## First prototype

A press-release case database: every fraud case since 2020 tagged by agency
and scheme and linked to award records. It becomes the label set for every
other prototype.

## Limits

Press releases cover charged cases only, which biases labels toward schemes
DOJ already finds. Grant subaward reporting is incomplete.

## Who to take it to

DOJ Criminal Division Fraud Section, Civil Division Commercial Litigation
(False Claims Act), Office of Justice Programs, and DOJ OIG.

## Sources

- [DOJ Whistleblower Rewards Program terms](https://www.justice.gov/fraud/whistleblower)
- [DOJ news releases](https://www.justice.gov/news)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
