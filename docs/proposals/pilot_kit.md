# Pilot proposal kit: a 90-day pilot with one agency

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 4 of 10
(see the [extensions overview](../extensions.md)). Recommended first
partner: **HHS-OIG with CMS, on hospice and home health (HHS-1)**, with SBA
OIG as the alternate. Everything below is written so the agency name and
screen can be swapped.

## Bottom line

A leader can say yes to 90 days, a small team, no new system in their
boundary and a clear stop rule. This kit gives them exactly that: a
week-by-week plan, the data-sharing paperwork as fill-in templates, the
metrics that decide whether to scale, and the staffing on both sides.

- **Why HHS first:** the largest improper payment base ($28.8B Medicare
  fee-for-service, $37.4B Medicaid), the highest modeled return (see the
  [ROI model](roi_model.md)), a live public problem (the 2026 hospice and
  home health moratorium) and an OIG that already runs data analytics.
- **Why SBA as the alternate:** the SBA work with Rosemary is the proof of
  method, the OIG knows the pandemic cases, and the data is already
  understood. It is the faster yes, but the smaller prize.
- **Stop rule:** at day 75, if the screen's top 5% does not contain known
  cases at five times the base rate, or reviewers confirm fewer than one in
  five leads as worth opening, the pilot ends and the report says why.

## 1. Scope

| Item | HHS (recommended) | SBA (alternate) |
| --- | --- | --- |
| Partner | HHS-OIG Office of Investigations and Office of Audit Services; CMS Center for Program Integrity | SBA OIG; Office of Capital Access |
| Screen | HHS-1 hospice and home health risk map, plus cluster scoring and exclusion matching | SBA-1 pandemic signals on 7(a) and 504, plus cross-program matching |
| Data from the agency | Medicare hospice and home health claims for two states (California, Minnesota is the suggested pair), 2022-2026; provider enrollment with owners | 7(a) and 504 application and lender data, 2020-2026 |
| Where analysis runs | Inside the OIG's or CMS's authorized environment, or the CMS Virtual Research Data Center | SBA OIG's environment |
| Out of scope | Beneficiary-level contact, payment suspension decisions, any adverse action | Borrower contact, loan decisions |

## 2. 90-day plan

| Days | Work | Output | Agency time needed |
| --- | --- | --- | --- |
| 0-10 | Sign the memorandum of understanding and data use agreement; analysts complete suitability and access training; agree the known-case list for back-testing | Signed agreements; access granted | Counsel and privacy officer review (template below); 2 hours with the case lead |
| 11-25 | Load data; build the provider and owner spine; reproduce public-data HHS-1 results inside the environment | Data profile; reconciliation to published totals | Data steward, 2 hours a week |
| 26-45 | Run claim-level screens (billing ramp, length of stay, live discharge, shared owners, exclusion links); score clusters | First ranked list with reason codes | — |
| 46-60 | Back-test on known cases; hand review of the top 50 leads with OIG investigators | Lift and precision report | Two investigators, 1 day each |
| 61-75 | Tune; second review round of 50 new leads; decide on stop rule | Final metrics | Two investigators, 1 day each |
| 76-90 | Lead packages for the confirmed-worth-opening cases; results briefing; scale-up proposal or close-out report | Briefing, report, lead packages | Leadership briefing, 1 hour |

## 3. Success metrics

Agreed before data arrives, and reported whatever the result.

| Metric | Definition | Pass mark |
| --- | --- | --- |
| Lift at 5% | Known-case rate in the top 5% of scores / overall rate | At least 5x (the review plan's release bar) |
| Reviewer precision | Share of the 100 reviewed leads the OIG rates worth opening | At least 20% |
| New detection | Share of worth-opening leads not already known to the OIG or CMS | At least 50% |
| Dollars at issue | Medicare payments to providers in worth-opening leads | Reported, not targeted |
| Time to lead | Days from data load to first reviewed lead list | 45 or fewer |
| Catch rate vs break-even | Measured new detection against the ROI model's break-even rate | Above break-even |
| Burden | Agency staff hours used | 80 or fewer |

## 4. Staffing

| Role | Our side | Time | Agency side | Time |
| --- | --- | --- | --- | --- |
| Pilot lead | Lead (also the single point of contact) | 50% | OIG Special Agent in Charge or Assistant IG sponsor | 1 hour every 2 weeks |
| Data engineer | DE | 100% days 0-45, then 50% | Data steward | 2 hours a week |
| Analysts | AN x2 (one health-claims specialist) | 100% | Two investigators for review | 4 days total |
| Statistician | Part time, for validation and metrics | 25% | — | — |
| Counsel and privacy | Our counsel | As needed | Privacy officer, counsel | Days 0-10 |

## 5. Template: memorandum of understanding (outline)

Fill in bracketed text; counsel on both sides should edit freely.

1. **Parties.** [Agency or OIG] and [our organization].
2. **Purpose.** A 90-day pilot to test whether [screen] identifies
   [program] payments at elevated risk of fraud, for review by [OIG].
3. **Authority.** [IG Act of 1978 as amended, 5 U.S.C. 401-424 / agency
   program integrity authority / Payment Integrity Information Act].
4. **Roles.** The agency decides every investigative and administrative
   action. We supply methods, analysis and lead packages.
5. **Data.** As listed in the data use agreement (attachment A).
6. **Environment and security.** Analysis inside [agency environment]; no
   data leaves it; outputs reviewed before export (attachment B).
7. **Personnel.** Named analysts; suitability and training before access.
8. **Confidentiality.** Leads and results are agency records; we publish
   nothing about the pilot without written approval, and only in aggregate.
9. **Cost.** [No cost to the agency / interagency agreement / contract
   vehicle].
10. **Term and termination.** 90 days from data access; either party may end
    with 10 days' notice; data access ends at term.
11. **Deliverables.** Section 2 outputs; final report within 15 days of term.
12. **Points of contact.**

## 6. Template: data use agreement (attachment A)

| Field | Entry |
| --- | --- |
| Data owner and system of records | [System name and SORN number] |
| Routine use or authority for disclosure | [Routine use / OIG access / Privacy Act exception] |
| Files | [Claims, enrollment, owners], years [ ], states [ ] |
| Fields | Listed in an appendix; minimum necessary for the screens |
| Identifiers | Provider identifiers in clear; beneficiary identifiers [excluded / hashed] |
| Location | [Environment]; no copies outside it |
| Users | Named analysts only |
| Retention | Destroyed or returned within 30 days of term, with a certificate |
| Linkage | No linkage to other data except [public files listed] without written approval |
| Re-disclosure | None |
| Breach reporting | To the agency within one hour of discovery, per OMB M-17-12 |
| Publication | Aggregate statistics only, with cell suppression under 11, after agency review |

## 7. Template: security and output review (attachment B)

- Work only inside the environment, on agency-furnished or approved devices.
- Outputs leave the environment only after the agency's data steward reviews
  them; lead packages go straight to the OIG case system.
- Model documentation travels with every score: inputs, tests, known
  limits and bias checks.

## 8. Leave-behind for the first meeting

One page: the problem (pitch HHS-1), what the public-data screen already
shows, the 90-day plan, the three asks (data, two investigators for four
days, a sponsor), the stop rule, and the ROI row from the business case.
The site's agency brief PDFs supply the layout.

## 9. Questions for Steve

1. HHS-OIG first, or SBA OIG first because the relationship already exists?
2. Who on our side signs the memorandum?
3. Will we fund the pilot ourselves to remove the cost question?
