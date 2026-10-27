# Pension Benefit Guaranty Corporation: one-page brief

**Priority:** 24 of 33 (score 2.5). **FY2026 outlays:** $10.6B
(USAspending). **As of:** 2026-10-27. Public data only.

## Bottom line

PBGC pays pensions for failed plans and, since 2021, has paid Special
Financial Assistance (SFA) grants to rescue multiemployer plans. The SFA
program showed a concrete, public failure: Central States got about $127M
too much because 3,479 dead participants were counted as alive, since PBGC
was not checking SSA's death file until November 2023. Other SFA plans may
carry the same error.

## Exposure

- $10.6B in outlays and $91B in budgetary resources in FY2026.
- Central States alone received a $35.8B SFA grant; the $127M overpayment
  was about 0.35% of it. PBGC says it will recover funds tied to deceased
  participants from other plans.

## Public data we can use

- **PBGC SFA application and approval listings** (plan, amount, date).
- **Form 5500 filings (DOL EFAST):** participant counts, deaths reported,
  and actuarial data for every plan.
- **PBGC OIG reports** and congressional oversight letters.

## Detection plays

1. **SFA census checks:** plans whose participant counts or death rates in
   the SFA application differ from their own Form 5500 history and actuarial
   norms.
2. **Benefit payee checks** (with SSA data): payees with no sign of life.

## First prototype

A plan-level table comparing SFA application data with Form 5500 trends,
ranking plans by likely overcounted participants.

## Limits

Participant-level data is not public; the screen finds plans to audit,
not individual dead payees.

## Who to take it to

PBGC Multiemployer Program, PBGC OIG, and DOL's Employee Benefits Security
Administration.

## Sources

- [PlanSponsor: Central States to repay $127M SFA overpayment](https://www.plansponsor.com/pbgc-says-central-states-will-reimburse-sfa-overpayment/)
- [PBGC OIG semiannual report (SR-2026-01)](https://oig.pbgc.gov/pdfs/SR-2026-01.pdf)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
