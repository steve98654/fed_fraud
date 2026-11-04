# Grants to states: following federal money through state programs

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 7 of 10
(see the [extensions overview](../extensions.md)). Reference code:
`analytics/forensic/passthrough.py`, tested on synthetic data only.

## Bottom line

Most of the pandemic-era losses happened in programs the federal
government pays for and states run: unemployment insurance (GAO estimated
fraud at $100 billion to $135 billion), Medicaid, SNAP, child nutrition and
emergency rental assistance. Federal agencies see these programs as a
state-level total; the fraud happens one claimant, provider or subrecipient
below that, in state systems. This extension sets out how to follow the
money anyway, in three layers:

1. **State-level screens on public statistics** (Phase 1): which states,
   programs and years look unusual against their peers, adjusted so small
   states are not over-flagged.
2. **Subrecipient screens on Single Audit and subaward data** (Phase 1):
   the organizations a state keeps funding despite repeated audit findings,
   and pass-through programs where one new subrecipient takes most of the
   money.
3. **Claim-level screens through states and existing hubs** (Phase 2):
   NASWA's Integrity Data Hub for UI, CMS's T-MSIS for Medicaid, USDA's
   National Accuracy Clearinghouse for duplicate SNAP participation.

## 1. Programs and exposure

Public figures; check each against the latest PaymentAccuracy.gov release.

| Program | Federal agency | FY2025 improper payments | Main fraud patterns |
| --- | --- | --- | --- |
| Medicaid | HHS (CMS) | $37.4B (6.1%) | Billing for services not provided (personal care, behavioral health, housing supports, autism therapy), provider identity theft, ineligible enrollees |
| Unemployment insurance | DOL | $5.6B (14.9%) | Identity theft, multi-state claims, fictitious employers, prisoners and deceased claimants |
| SNAP | USDA (FNS) | $10.2B (10.9%) | Retailer trafficking, duplicate participation across states, EBT skimming |
| Child Nutrition (CACFP, Summer Food) | USDA (FNS) | CACFP 10.5% | Sponsor fraud on meal counts (the Feeding Our Future case, about $250M) |
| TANF, child care (CCDF) | HHS (ACF) | Not all reported | Misuse of block grant funds, phantom attendance |
| Emergency Rental Assistance, Homeowner Assistance Fund | Treasury | Not reported as improper | Fictitious tenants and landlords |

## 2. Layer 1: state-level screens (public data)

| Screen | Data | Method |
| --- | --- | --- |
| UI overpayment and fraud rates by state | DOL ETA 902P (Benefit Accuracy Measurement), ETA 227 overpayment reports | Robust z and empirical-Bayes rate ratio across states (`state_outliers`) |
| UI claims versus local job loss | ETA 539 weekly claims, BLS LAUS and QCEW | Claims growth that outruns job loss (DOL-1) |
| Medicaid spending versus enrollment by service | CMS-64 expenditure reports, T-MSIS Analytic Files summaries, enrollment reports | Spending that grows faster than people served (`growth_without_caseload`), by service category |
| SNAP payment error rates by state | FNS Quality Control reports | Peer comparison with shrinkage |
| SNAP retailer redemptions | FNS retailer data (where public), store counts by area | Redemption per store outliers (USDA-1) |

A high state rate can mean more fraud or better detection. States that
look hardest find the most, so the first question to a flagged state is
how it measures, before whether it has a problem.

## 3. Layer 2: subrecipients (public data)

- **Single Audit findings** (Federal Audit Clearinghouse, fac.gov): every
  entity spending $1M or more in federal awards a year (2 CFR 200.501, as
  revised in 2024) files an audit with findings, questioned costs and
  repeat-finding flags. Screen: subrecipients with material weaknesses or
  questioned costs in three or more years that keep receiving funds
  (`repeat_finding_entities`).
- **Subaward concentration** (FFATA subaward reports in USAspending):
  Herfindahl index of each state agency's subawards and the largest
  subrecipient's share, by program and year (`subaward_concentration`).
  One new subrecipient taking most of a pass-through program is the shape
  of the Feeding Our Future case.
- **Missing audits:** subrecipients whose federal spending implies a
  Single Audit but none was filed.
- **Cross-agency matching** of subrecipients against exclusions, and
  network scoring of subrecipients that share officers and addresses (see
  [cross-agency matching](../playbook/cross_agency_matching.md) and
  [network analytics](../playbook/network_analytics.md)).

## 4. Layer 3: claim-level, with states (Phase 2)

| Hub or route | Program | What it allows | Who to ask |
| --- | --- | --- | --- |
| NASWA Integrity Data Hub | UI | Cross-state matching of claims, suspicious actor repository, bank account verification | NASWA, DOL ETA, participating states |
| T-MSIS | Medicaid | National claim-level data submitted by states | CMS, HHS-OIG (already uses it) |
| National Accuracy Clearinghouse | SNAP | Duplicate participation across states, required by the 2018 Farm Bill | FNS |
| State data sharing agreements | Any | Claim and eligibility files for a pilot | State program integrity units, state auditors, Medicaid Fraud Control Units |

Recommended Phase 2 entry: two states that already participate in the
Integrity Data Hub and have an active state auditor partnership, running
UI and SNAP identity reuse (roadmap X-3).

## 5. Partners beyond federal agencies

- **State auditors** (through NASACT) and **Medicaid Fraud Control Units**
  (federally funded, in every state).
- **Program integrity units** in state Medicaid, labor and human services
  agencies.
- **Federal OIGs** with state grant oversight: HHS-OIG, DOL-OIG, USDA-OIG.

## 6. Limits

- Public state data is aggregate and lags by a year or more.
- Single Audit quality varies, and findings are self-reported by the
  auditee's auditor.
- States own the claim data; each state agreement is separate.

## 7. Next steps

1. Build the state UI panel (ETA 902P, 227, 539 with BLS) for 2019-2026.
2. Load FAC findings for the six largest pass-through programs and run the
   repeat-finding screen.
3. Draft the two-state proposal using the [pilot kit](../proposals/pilot_kit.md).
