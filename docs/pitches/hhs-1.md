# HHS-1: Hospice and home health risk map

**For:** CMS Center for Program Integrity, HHS-OIG Office of
Investigations, DOJ Health Care Fraud Unit. **Weeks:** 3-7 (results by
2026-12-18). **Brief:** [HHS](../agencies/hhs.md).

## The problem

Sham and captive hospices and home health agencies enroll in clusters,
bill heavily within months, enroll patients who are not terminally ill and
change owners when caught. CMS put a six-month nationwide moratorium on new
hospice and home health enrollments on 2026-05-13, and about 800 Los
Angeles providers had payments suspended. The pattern is visible in public
CMS files before it reaches a payment suspension.

## Data

- data.cms.gov: Hospice and HHA enrollments and All Owners files; Medicare
  Post-Acute Care and Hospice by Provider; Revoked providers list.
- NPPES full file and monthly deactivations; HHS-OIG LEIE exclusions.
- Care Compare hospice measures; DOJ Health Care Fraud Unit case releases.

## Detection method

1. **Clusters:** providers per address, shared owners and managing
   employees, frequent ownership changes, in Los Angeles County and
   Minnesota first.
2. **Billing ramp:** Medicare payments in the first 24 months after
   enrollment against peers enrolled the same year.
3. **Peer outliers:** length of stay, dementia-only diagnoses,
   live-discharge rate and payments per beneficiary, by county.
4. **Owner networks:** links to LEIE, revoked providers and DOJ defendants.
5. **National extension:** the same signals on durable medical equipment,
   labs and telehealth (HHS-3).

A provider becomes a lead only with two or more independent signals.

## Validation

Back-test on providers named in the moratorium materials, the Los Angeles
suspensions and DOJ Health Care Fraud Unit cases 2020-2026. The screen is
released only if known cases are at least five times more common in its
top 5% than in the population.

## Exposure (public figures, not savings)

- Medicare fee-for-service: $28.8B improper in FY2025 (6.6%); Medicaid:
  $37.4B (6.1%) (GAO).
- About 800 Los Angeles hospices and home health agencies under payment
  suspension.
- Savings from this work: **Pending.**

## What we ask for

- **Now:** a named CPI or HHS-OIG contact; the list of providers already
  suspended or under review, so our leads add to it rather than repeat it;
  the preferred referral format.
- **Phase 2:** Medicare hospice and home health claims through HHS-OIG or
  the CMS research data center, to score claims instead of providers.

## What you get, and when

By week 7: a risk map and ranked provider list for the two hot spots, an
owner network view, a national outlier table and lead packages for the top
networks, each with its reasons and source records.

## Limits

Public CMS files lag one to two years and show providers, not claims. A
high score is a reason to look, not proof of fraud.

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [WilmerHale: CMS hospice and home health moratorium (May 2026)](https://www.wilmerhale.com/en/insights/client-alerts/20260521-cms-announces-moratorium-on-new-medicare-enrollment-for-hospices-and-home-health-agencies)
