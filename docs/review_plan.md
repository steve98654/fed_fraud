# Fraud review plan: top 33 agencies

**Status:** Draft v0.1 (2026-10-27), for Steve's review.
**Builds on:** [the top 33 ranking](agencies/top33.md), the 33 agency briefs
in [docs/agencies/](agencies/top33.md) and the [working plan](plan.md).

## Bottom line

This plan turns the 33 agency briefs into a dated program of work in two
phases.

- **Phase 1 (public data, 2026-11-02 to 2027-03-05, 16 working weeks).**
  Build one shared data spine and case library, then run a defined review of
  every agency using only public data. Seven agencies get full prototypes
  (HHS, DoD, SBA, USDA, DHS, DOT, GSA). Five get contained pilots (FCC, OPM,
  VA, Commerce, PBGC). The rest are covered by three shared screens
  (contractors, research awards, grantees) or, where payee data is closed,
  by an aggregate screen plus a data-access proposal. Every agency ends
  Phase 1 with a written finding and a ranked lead list or a reasoned
  "nothing actionable from public data".
- **Phase 2 (internal data, from 2027-03 through 2028).** Use the Phase 1
  results to win data agreements, starting with Inspectors General, who
  already hold the data and the authority to act on it. Internal data moves
  the work from risky *entities* to specific false *claims and payments*,
  which is what prosecutors need, and makes pre-payment prevention possible.
  The first internal-data pilots can realistically start around 2027-07;
  agreements are the long pole, not the analytics.

The plan rests on three choices worth checking:

1. **Leads, not accusations.** Public-data findings are risk indicators.
   Nothing is published or named outside a referral to the responsible
   Inspector General or DOJ component.
2. **Build once, apply 33 times.** About 70% of the Phase 1 effort goes into
   shared assets (entity spine, case library, scoring, lead package). Each
   added agency then costs days, not months.
3. **Start Phase 2 paperwork in Phase 1.** Data agreements take 3 to 12
   months, so access requests go out in week 8, not after Phase 1 ends.

## Scope and ground rules

### What "a thorough review" means here

For each of the 33 agencies, the review answers five questions:

1. **Where is the money?** Which programs and payment streams carry the
   agency's outlays, and which are fraud-prone.
2. **What fraud is known?** Improper payment estimates, OIG and GAO
   findings, and charged cases, by scheme.
3. **What can public data see?** Which payees, awards and relationships are
   visible, and which are not.
4. **What does the data show?** Ranked leads from the screens in this plan,
   each with stated reasons and a validation result.
5. **What would internal data add?** The Phase 2 data request, access route
   and expected payoff.

The output for each agency is a **review memo** (one to three pages,
`docs/reviews/<agency>.md`) plus, where there are findings, a **lead
package** (see "Lead packages" below).

### Ground rules

- **Public and lawfully obtained data only in Phase 1.** That includes
  federal open data, state public records, court records, FOIA releases and
  licensed commercial data. No scraping behind logins, no personal data
  beyond what the source publishes.
- **Findings are leads.** A lead needs at least two independent risk signals
  and a written reason before it leaves the analysis team. No lead names a
  person in any public document.
- **Referral, not publicity.** Leads go to the agency OIG or the DOJ
  component named in each brief. Counsel reviews the referral route before
  the first package goes out, including False Claims Act public-disclosure
  and original-source questions and the DOJ whistleblower program at
  america.gov/fraud.
- **Reproducible.** Every number in a memo traces to a script and a dated
  data pull in the repo, so results can be rerun and defended.
- **Scored honestly.** Each screen is tested against known cases (see
  "Validation") and the hit rate is reported, including when it is poor.

### Team assumptions (to confirm)

The timeline assumes a core team of five, plus the SBA team (Rosemary) as
method owner:

| Role | Short name | Main job |
| --- | --- | --- |
| Program lead | Lead | Plan, agency contacts, reviews, briefings (Steve or delegate) |
| Data engineer | DE | Ingest, entity resolution, pipelines |
| Analyst (x2) | AN | Screens, scoring, validation, review memos |
| Fraud investigator | INV | Case library, lead review, referral packages |
| SBA team | SBA | Playbook, method review, reuse of SBA code |

With fewer people, keep the order and stretch the dates; the shared
foundation (weeks 1 to 4) must not be cut.

## Phase 1: public-data review

### Timeline at a glance

Week 1 starts Monday 2026-11-02. Weeks skip the holiday break
(2026-12-21 to 2027-01-01), so week 8 starts 2027-01-04 and week 16 ends
2027-03-05. Thanksgiving week (week 4) counts as a short week.

| Weeks | Dates | Focus | Main outputs |
| --- | --- | --- | --- |
| 1-2 | Nov 2 - Nov 13 | Foundation: playbook, data spine, case library v0, FOIA requests filed | `docs/playbook/sba-baseline.md`, spine v0, FOIA log |
| 3-4 | Nov 16 - Nov 27 | Foundation finished; Wave 1 screens start (HHS, DoD, SBA) | Spine v1, scoring framework, lead package template |
| 5-7 | Nov 30 - Dec 18 | Wave 1 screens validated; Wave 2 starts (DHS, USDA, DOT, GSA) | Wave 1 lead lists and memos (HHS, DoD, SBA) |
| 8-10 | Jan 4 - Jan 22 | Wave 2 finished; pilots (FCC, OPM, VA, Commerce, PBGC); Phase 2 access requests sent | Wave 2 lead lists, pilot results, 6 access proposals |
| 11-13 | Jan 25 - Feb 12 | Shared screens across remaining agencies; aggregate screens | Contractor, research and grantee screen results; aggregate memos |
| 14-15 | Feb 15 - Feb 26 | Review memos for all 33; lead package QA; counsel review | 33 review memos, referral packages |
| 16 | Mar 1 - Mar 5 | Briefings and Phase 1 report | Phase 1 report, leadership deck, Phase 2 go/no-go |

### Workstreams by week

| Workstream | Agencies | Weeks | First result |
| --- | --- | --- | --- |
| F. Shared foundation | All | 1-4, upkeep after | Week 4 |
| A1. Wave 1 deep dives | HHS, DoD, SBA | 3-7 | Week 7 |
| A2. Wave 2 deep dives | DHS, USDA, DOT, GSA | 5-10 | Week 10 |
| B. Contained pilots | FCC, OPM, VA, Commerce, PBGC | 7-11 | Week 11 |
| C1. Contractor screen | USACE, NASA, DOE, State, NRC, DHS and VA contracts | 9-13 | Week 13 |
| C2. Research award screen | NSF, DOE, NASA, PCORTF, DoD, HHS (NIH) | 9-12 | Week 12 |
| C3. Grantee screen | EPA, DOJ, AmeriCorps, HUD, USAID, State, EOP, DFC | 10-13 | Week 13 |
| D. Aggregate screens and access cases | Treasury, SSA, DOL, ED, HUD tenants, FDIC, DOI | 10-14 | Week 14 |
| E. Data partners | GSA, DOJ, SEC, SSA | 2-10, in parallel | Week 6 (DOJ case library) |
| R. Memos, referrals, briefings | All | 14-16 | Week 16 |

### Shared foundation (weeks 1 to 4)

These items serve every agency and come first. Each has an owner, a due
week and a test for "done".

| ID | Action | Owner | Due | Done when |
| --- | --- | --- | --- | --- |
| F1 | Write the SBA baseline playbook: data sources, typologies, features, scoring, measured results; mark what is SBA-only | SBA, Lead | Wk 2 | `docs/playbook/sba-baseline.md` reviewed by Rosemary |
| F2 | Stand up the repo layout (`pipelines/`, `prototypes/<agency>/`, `docs/reviews/`, `data/` manifest) and a dated-pull convention | DE | Wk 1 | Every pull logged with source, URL, date, row count, hash |
| F3 | Ingest the entity spine: SAM.gov public entity extract and exclusions, USAspending prime and subaward bulk files FY2020-FY2026, FPDS contract actions | DE | Wk 3 | One table keyed by UEI with awards, addresses, POCs, exclusions |
| F4 | Ingest watch lists: SAM exclusions, HHS-OIG LEIE, OPM OIG debarments, OFAC SDN and consolidated lists, World Bank debarred firms, HUD Limited Denial of Participation, USAC E-Rate suspensions | DE | Wk 2 | One watch-list table with source and date per row |
| F5 | Build the case library v0: DOJ press releases (justice.gov news API, all U.S. Attorneys' offices) 2020-2026, tagged by agency, program, scheme, dollars, defendants and entities | INV, AN | Wk 4 (v0), Wk 6 (v1) | At least 2,000 fraud releases tagged; entities linked to UEI or NPI where possible |
| F6 | Add OIG reports from Oversight.gov and GAO fraud reports to the case library | INV | Wk 6 | Report index with agency, program, finding type |
| F7 | Entity resolution: reuse the SBA matcher for names, addresses (USPS-standardized), phones, officers; add NPI and EDGAR CIK keys | DE, SBA | Wk 4 | Precision checked on 500 hand-labeled pairs (target 95%+) |
| F8 | Scoring framework: common signal library (shared address, shared officer, new entity large award, excluded link, peer outlier, rapid growth), reason codes, score calibration | AN | Wk 4 | Each signal documented with formula, threshold and false-positive notes |
| F9 | Lead package template and review checklist (see below) | INV, Lead | Wk 4 | Template approved by Lead |
| F10 | File FOIA and public-records requests with long lead times (list below) | Lead | Wk 1 | Requests filed and tracked in `docs/reviews/foia_log.md` |
| F11 | Counsel review of ground rules, referral route, FCA and whistleblower questions, data licensing | Lead | Wk 6 | Written guidance in `docs/playbook/legal.md` |
| F12 | Commercial data decision: vessel manifests (DHS), corporate registries and beneficial ownership (OpenCorporates or similar) | Lead | Wk 3 | Bought, or written reason not to |

**FOIA and records requests to file in week 1** (responses take 1 to 6
months, so file before they are needed):

- SBA: latest 7(a) and 504 loan-level releases if not already held; 8(a)
  and HUBZone decertification lists.
- USDA FNS: SNAP retailer disqualifications and civil money penalties by
  store, 2018-2026.
- CBP: published Enforce and Protect Act (EAPA) determinations list and
  penalty case summaries.
- Three to five state DOTs: DBE commercially-useful-function reviews and
  decertifications; prime-to-DBE payment reports.
- Two states (Minnesota plus one other): CACFP sponsor and site lists with
  meal counts by site.
- OPM: FEHB carrier provider debarment and suspension notices (if not on
  OPM OIG's public list).
- FSA (Education): school-level fraud referrals and Heightened Cash
  Monitoring reasons.

### Validation

Every screen is tested the same way before its leads are used:

1. **Back-test against known cases.** Take entities charged or settled in
   the case library (F5) for that program. Score the population as it looked
   *before* the case became public. Report how many known cases land in the
   top 1%, 5% and 10% of scores.
2. **Hand review a sample.** The investigator reviews 25 top-scored
   entities that are not known cases and records whether a reasonable
   reviewer would want to look further.
3. **Bar for release.** A screen is released when known cases are at least
   five times more common in its top 5% than in the population, and at least
   half of the hand-reviewed sample is judged worth review. Screens that miss
   the bar are reported as such and reworked or dropped.

### Lead packages

A lead package is what goes to an OIG or DOJ. One package per entity or
network, in a fixed format:

- Summary: who, which program, how much money, which scheme it resembles.
- Signals: each risk signal with its source record and date.
- Network: related entities, shared addresses, officers, exclusions.
- Comparison: how the entity compares with its peers.
- Known-case match: the charged cases it most resembles.
- Limits: what public data cannot show, and innocent explanations checked.
- Provenance: data pulls and script versions used.

Packages are reviewed by the investigator and the program lead, then by
counsel for the first ten, before referral.

### Agency review plans

Agencies are listed in the order of the recommended sequence in
[top33.md](agencies/top33.md). Each plan lists the review questions, the
data to pull, the analyses to run, how to validate, what is delivered and
when, and who receives it. Shared building blocks (F1 to F12) are assumed.

#### Wave 1 deep dives (weeks 3 to 7)

##### 1. HHS: Medicare and Medicaid providers

[Brief](agencies/hhs.md). Rank 1, score 4.8. Owner: AN 1 with INV.

- **Review questions.** Which hospices and home health agencies (HHAs) in
  Los Angeles County and Minnesota look like sham or captive providers? Which
  owners link to excluded or suspended providers? Which other provider types
  show the same ramp-and-cluster pattern nationally?
- **Pull (weeks 2-3).** data.cms.gov: Hospice and HHA enrollments, Hospice
  and HHA All Owners files, Medicare Post-Acute Care and Hospice by Provider,
  Physicians and Other Practitioners by Provider and Service, Part D
  Prescribers, Public Provider Enrollment, Revoked providers list; NPPES full
  file and monthly deactivations; LEIE; Open Payments; Care Compare hospice
  measures; Head Start and child care grants from USAspending.
- **Run (weeks 3-6).**
  1. Address and owner clustering for hospices and HHAs: providers per
     address, shared owners and managing employees, ownership change
     frequency.
  2. Billing ramp: Medicare payments in the first 24 months after
     enrollment versus peers enrolled the same year.
  3. Peer outliers: average length of stay, share of patients with
     dementia-only diagnoses, live-discharge rate, payments per beneficiary,
     by county.
  4. Owner network links to LEIE, revoked providers and DOJ case defendants.
  5. National extension: run the same signals for durable medical
     equipment, laboratories and telehealth billing outliers.
- **Validate.** Back-test against providers in the May 2026 moratorium
  materials, payment suspensions announced for Los Angeles, and DOJ Health
  Care Fraud Unit cases 2020-2026.
- **Deliver (week 7).** Risk map and ranked list for the two hot spots;
  owner network view; national outlier table; review memo; lead packages for
  the top networks.
- **Take to.** CMS Center for Program Integrity, HHS-OIG Office of
  Investigations, DOJ Health Care Fraud Unit.

##### 2. DoD: set-aside contractors

[Brief](agencies/dod.md). Rank 2, score 4.3. Owner: AN 2 with SBA.

- **Review questions.** Which set-aside winners look like fronts or
  pass-throughs for ineligible firms? Which groups of "competitors" share
  control? Which awards show threshold gaming or runaway modifications?
- **Pull (weeks 2-3).** FPDS / USAspending DoD contract actions FY2021-FY2026
  (set-aside type, offers received, competition, modifications, place of
  performance); subaward reports; SAM.gov entities and exclusions; SBA
  Dynamic Small Business Search and certification lists (8(a), HUBZone, WOSB,
  VetCert); DOJ and DCIS case releases.
- **Run (weeks 3-6).**
  1. Front-company signals: new entity with large set-aside awards, shared
     address or POC with a large business, high share of subaward dollars to
     one non-eligible firm.
  2. Collusion signals: shared officers, addresses or phones among bidders
     in the same market; win rotation by contracting office and NAICS code.
  3. Threshold gaming: sole-source awards clustered just under the 8(a),
     simplified acquisition and other dollar thresholds.
  4. Modification growth: value growth beyond award versus peers in the
     same product or service code.
  5. Excluded links: vendors sharing identifiers with excluded parties.
- **Validate.** DCIS and DOJ set-aside fraud cases 2018-2026 (case library);
  SBA decertifications from the FOIA request.
- **Deliver (week 7).** Contractor integrity screen with ranked vendors and
  reasons; collusion network view by market; review memo; lead packages.
- **Take to.** DoD Office of Small Business Programs, DCIS and DoD OIG,
  DOJ Procurement Collusion Strike Force.

##### 3. SBA: extend the baseline

[Brief](agencies/sba.md). Rank 3, score 4.2. Owner: SBA team with DE.

- **Review questions.** Which current (non-pandemic) loans, lenders, agents
  and certified firms carry the same signals as the pandemic fraud already
  found?
- **Pull (weeks 1-3).** 7(a) and 504 loan-level FOIA data FY2010-FY2026;
  PPP and EIDL data already held; 8(a), HUBZone, WOSB and VetCert lists;
  SBA OIG reports.
- **Run (weeks 3-6).**
  1. Apply the existing SBA identifier and address screens to 7(a) and 504.
  2. Lender and agent concentration: share of each lender's loans with
     pandemic fraud signals, charge-off rates versus peers.
  3. Cross-program reuse: borrowers and owners in pandemic fraud findings
     who now hold 7(a), 504 or contracting certifications.
- **Validate.** Existing SBA results and SBA OIG cases; PPP and EIDL cases
  inside the 10-year limitation period (extended by 2022 law), which keeps
  them prosecutable to 2030-2032.
- **Deliver (week 6).** Updated SBA results across all loan programs; lender
  risk table (shared with FDIC); playbook v1.
- **Take to.** SBA Office of Credit Risk Management, SBA OIG.

#### Wave 2 deep dives (weeks 5 to 10)

##### 4. DHS: customs evasion and FEMA

[Brief](agencies/dhs.md). Rank 4, score 3.9. Owner: AN 1.

- **Review questions.** In which high-duty product lines do U.S. imports from
  a country exceed that country's reported exports to the U.S.? Which
  importers of record drive the gap? Which FEMA contractors and public
  assistance recipients look like shells?
- **Pull (weeks 4-6).** Census USA Trade Online imports by HTS-10 and
  country; UN Comtrade partner exports for mirror checks; ITA list of active
  antidumping and countervailing duty orders and Section 301 / 232 tariff
  lists; CBP EAPA determinations; vessel manifest data from a licensed
  vendor (decision F12); OpenFEMA Public Assistance Funded Projects Details
  and Hazard Mitigation projects; DHS contracts from FPDS.
- **Run (weeks 6-9).**
  1. Mirror gap: product-country pairs with the largest unexplained gaps
     after tariff changes, for two product groups first (for example
     aluminum extrusions and plastic resin).
  2. Shell importers: new importers of record after a tariff change,
     sharing addresses or officers with penalized firms, using residential or
     registered-agent addresses.
  3. Country-of-origin shifts: shippers whose declared origin moves to a
     third country right after a duty change.
  4. FEMA contractor screen: shared foundation signals on disaster awards,
     plus out-of-area firms winning large awards within 30 days of a
     declaration.
- **Validate.** Trade Fraud Task Force resolutions and customs False Claims
  Act settlements 2020-2026; EAPA determinations.
- **Deliver (week 10).** Importer lead list with reasons for two product
  groups; FEMA contractor table; review memo.
- **Take to.** CBP Office of Trade, HSI, DOJ-DHS Trade Fraud Task Force,
  FEMA Fraud Investigations and Inspections Division, DHS OIG.

##### 5. USDA: SNAP retailers and child meal sponsors

[Brief](agencies/usda.md). Rank 4, score 3.9. Owner: AN 2.

- **Review questions.** Which SNAP retailers look like trafficking fronts?
  Which CACFP and summer meal sponsors claim more than their area can
  support? Which farm disaster payments go to linked or outlier entities?
- **Pull (weeks 4-6).** FNS historical SNAP retailer locator data
  (authorization and end dates, store type, location) 2005-2026; FNS
  disqualifications (FOIA); federal court retailer appeal cases (CourtListener
  / PACER); SNAP participation by county; ACS child population by tract;
  state CACFP sponsor and site lists (FOIA, two states); USAspending USDA
  grants and direct payments; EWG farm subsidy data or FSA payment FOIA
  files.
- **Run (weeks 6-9).**
  1. Retailer clusters: small stores authorized near disqualified stores,
     owner and address reuse after disqualification, store density versus
     SNAP households.
  2. Sponsor capacity: meals claimed per site versus children living
     nearby, site growth rates, sponsors serving many sites with shared
     addresses or officers (the Feeding Our Future pattern).
  3. Farm disaster outliers: Emergency Conservation Program and NAP
     payments far above county peers; linked entities across payees.
- **Validate.** Feeding Our Future defendants and sites; disqualified
  retailers (the FOIA list) as labels for the retailer screen.
- **Deliver (week 10).** SNAP retailer risk map for two states; sponsor
  screen for one state; farm payment outlier table; review memo.
- **Take to.** FNS Retailer Operations Division, USDA OIG, state SNAP and
  child nutrition agencies.

##### 6. DOT: DBE fronts and bid rigging

[Brief](agencies/dot.md). Rank 6, score 3.7. Owner: AN 1 with SBA.

- **Review questions.** Which certified DBEs look like fronts for their
  primes? Where do bidders rotate wins or share control? Where is DBE
  participation promised but never paid?
- **Pull (weeks 5-7).** Unified Certification Program DBE directories for
  three states (for example Pennsylvania, Illinois, California); state DOT
  bid tabulations for the same states, 2019-2026; USAspending FHWA, FTA and
  FAA grants and subawards; state FOIA responses on DBE reviews; DOT OIG and
  DOJ DBE cases.
- **Run (weeks 7-9).**
  1. Front signals: DBEs sharing addresses, phones or officers with a prime;
     DBEs that work for one prime; DBEs with work codes they lack equipment
     or staff for (from state contractor prequalification data).
  2. Bid rotation: complementary bids, stable bid ranks, bidders who never
     beat each other, using all bids per letting.
  3. Participation gap: DBE commitments at award versus subaward reports.
- **Validate.** Charged DBE cases (case library) and state decertifications.
- **Deliver (week 10).** DBE integrity screen and bid rotation report for
  three states; review memo; method note for other states.
- **Take to.** DOT OIG, FHWA Office of Civil Rights, state DOT DBE offices,
  DOJ Procurement Collusion Strike Force.

##### 7. GSA: SAM.gov integrity and schedules

[Brief](agencies/gsa.md). Rank 6, score 3.7. Owner: DE with AN 2.

- **Review questions.** How many active SAM.gov registrations share
  addresses, POCs or officers in ways that suggest shells? Which firms
  re-register after exclusion? Which schedule prices and leases are outliers?
- **Pull (weeks 5-7).** SAM.gov entity extract (already in spine) with
  history; CALC+ labor rate data; GSA Advantage product prices for a sample
  of high-volume items; GSA lease inventory (IOLP); GSA OIG and DOJ schedule
  pricing settlements.
- **Run (weeks 7-9).**
  1. Registration clusters government-wide, ranked by award dollars (the SBA
     entity screen at full scale).
  2. Re-registration: new UEIs that share officers, addresses or phone
     numbers with excluded entities.
  3. Labor rate and product price outliers by category.
  4. Lease outliers: rent per square foot versus local comparables; lessor
     entity links.
- **Validate.** Excluded entities that re-registered (known from the
  exclusion record history); schedule FCA settlements.
- **Deliver (week 10).** SAM.gov registration integrity report (also offered
  to GSA as a data-quality product); price and lease outlier tables.
- **Take to.** GSA Integrated Award Environment (SAM.gov), Federal
  Acquisition Service, GSA OIG.

#### Contained pilots (weeks 7 to 11)

##### 8. FCC: Universal Service Fund

[Brief](agencies/fcc.md). Rank 8, score 3.5. Owner: AN 2.

- **Pull (week 7).** USAC Open Data: E-Rate FCC Forms 470 and 471,
  commitments and disbursements by applicant and provider, funding years
  2016-2026; Lifeline disbursements by provider and state; Rural Health Care
  commitments; Affordable Connectivity Program enrollment by ZIP (ended
  2024); FCC Form 499 filer database; USAC suspensions and FCC enforcement
  actions.
- **Run (weeks 8-10).** E-Rate single-bid share by consultant and provider;
  price per unit versus peers for the same service; provider-consultant
  links through shared addresses or officers; Lifeline and ACP enrollment per
  eligible household by area and provider.
- **Validate.** E-Rate kickback and bid rigging cases; FCC Lifeline
  enforcement actions.
- **Deliver (week 11).** E-Rate network map and ranked relationships;
  Lifeline and ACP provider outlier table; review memo.
- **Take to.** FCC Enforcement Bureau and OIG, USAC Internal Audit.

##### 9. OPM: FEHB exclusions

[Brief](agencies/opm.md). Rank 11, score 3.3. Owner: AN 1.

- **Pull (week 7).** OPM OIG debarment list, LEIE, SAM exclusions (all in
  F4); NPPES with deactivations; state medical board actions for five large
  states.
- **Run (weeks 8-9).** Reconcile the three exclusion lists on name, NPI,
  address and license; count providers excluded by HHS or SAM but missing
  from OPM's list; flag deactivated or deceased-provider NPIs still listed as
  active in public carrier directories (sample of carriers).
- **Validate.** GAO-26-108139 counts (at least 1,200 LEIE entries missing
  from OPM's list) as the benchmark.
- **Deliver (week 10).** Reconciliation report with matched identifiers;
  review memo.
- **Take to.** OPM Healthcare and Insurance, OPM OIG.

##### 10. VA: SDVOSB contracts and GI Bill schools

[Brief](agencies/va.md). Rank 8, score 3.5. Owner: AN 2.

- **Pull (week 7).** VA contracts from the spine; VetCert lists; GI Bill
  Comparison Tool data with caution flags; VBA annual benefits report by
  state and county.
- **Run (weeks 8-10).** DoD contractor screen on VA awards; SDVOSBs whose
  subaward dollars go mostly to non-veteran firms; schools with fast GI Bill
  growth, caution flags or owners tied to closed schools; county compensation
  rates far above veteran population and age norms.
- **Validate.** VA OIG and DOJ SDVOSB cases; schools already sanctioned.
- **Deliver (week 11).** VA contractor results, school watch list,
  county outlier table, review memo.
- **Take to.** VA OSDBU, VBA Education Service, VA OIG.

##### 11. Commerce: BEAD and CHIPS

[Brief](agencies/doc.md). Rank 11, score 3.3. Owner: AN 1.

- **Pull (week 8).** State BEAD final proposals and subgrantee selections
  for three states with published awards; FCC National Broadband Map
  availability data; USF history per provider (from the FCC pilot); CHIPS
  and EDA awards from USAspending.
- **Run (weeks 9-10).** Funded locations already shown as served; provider
  history (USF enforcement, new entities, shared owners across bidders); cost
  per location versus peers in similar terrain.
- **Deliver (week 11).** BEAD subgrantee screen and review memo. Framed as
  pre-spending prevention.
- **Take to.** NTIA Office of Internet Connectivity and Growth, Commerce OIG,
  state broadband offices.

##### 12. PBGC: Special Financial Assistance

[Brief](agencies/pbgc.md). Rank 24, score 2.5. Owner: AN 2.

- **Pull (week 8).** PBGC's posted SFA applications and approvals (plan,
  amount, census and actuarial exhibits); Form 5500 and Schedule MB filings
  from DOL EFAST2 for every SFA plan, 2015 onward.
- **Run (weeks 9-10).** Participant counts and deaths in each SFA
  application versus the plan's Form 5500 trend and standard mortality;
  rank plans by likely overcount of living participants.
- **Validate.** Central States ($127M, 3,479 deceased participants) as the
  known case.
- **Deliver (week 11).** Plan-level table and memo; the death-data case for
  SSA and Treasury (shared with SSA below).
- **Take to.** PBGC Multiemployer Program, PBGC OIG, DOL EBSA.

#### Shared screens (weeks 9 to 13)

The three shared screens reuse the foundation and the Wave 1 code. Each
agency still gets its own section of results and its own review memo.

**C1. Contractor screen** (DoD code on other agencies' awards). Signals:
front companies, collusion networks, threshold gaming, modification growth,
excluded links, plus Davis-Bacon and wage violations from DOL Wage and Hour
enforcement data.

**C2. Research award screen.** Pull SBIR.gov awards (all agencies,
2010-2026), NSF Award Search, NIH RePORTER, NASA TechPort and PCORI's funded
projects. Run text similarity on abstracts and aims to find near-duplicate
awards across agencies; flag award mills (many Phase I, no Phase II or
commercialization), shared PIs across firms, and excluded links. Benchmark
against GAO-24-105470 (842 high-risk awardees, about $445M possibly
duplicative).

**C3. Grantee screen.** Join USAspending grants and subawards to SAM.gov,
IRS Form 990 bulk data and the watch lists. Signals: nonprofit formed
shortly before a large award, revenue far below award size, subgrant chains
with shared officers, prior OIG findings, cost per participant far above
peers.

##### 13. Army Corps of Engineers

[Brief](agencies/usace.md). Rank 14, score 3.2. C1, weeks 9-11.
Run the contractor screen by Corps district; add a bid rotation view using
the Corps' dredging contract history where bids are published, and offers
received from FPDS elsewhere; compare change-order growth with peer
projects. Deliver district-level results and memo in week 11. Take to USACE
Directorate of Contracting, Army CID Major Procurement Fraud Unit, DOJ
Procurement Collusion Strike Force.

##### 14. Energy

[Brief](agencies/doe.md). Rank 11, score 3.3. C1 and C2, weeks 9-12.
C2 duplicate-award screen on DOE SBIR/STTR; C3-style check of new
infrastructure and IRA grant recipients (thin history, large awards, shared
addresses); excluded links for Loan Programs Office borrowers and sponsors.
Deliver in week 12. Take to DOE OIG and the DOE SBIR/STTR office.

##### 15. Environmental Protection Agency

[Brief](agencies/epa.md). Rank 15, score 3.1. C3, weeks 10-13.
Grantee profile for the Greenhouse Gas Reduction Fund, Solar for All and
state revolving fund projects: entity age, Form 990 history, subgrant chains
and contractor screen on SRF construction. Facts only, no fraud labels, given
the litigation. Deliver in week 13. Take to EPA Office of Grants and
Debarment and EPA OIG.

##### 16. HUD: owners and disaster grants

[Brief](agencies/hud.md). Rank 16, score 3.0. C3 plus own owner view,
weeks 10-13. Join the Multifamily Assistance and Section 8 Contracts data to
inspection scores (NSPIRE/REAC), owners and management agents, the HUD
Limited Denial of Participation list and SAM exclusions; rank owner networks
with poor inspections and continuing payments. Run C3 on CDBG-DR
subrecipients and contractors using DRGR public reports. Use Picture of
Subsidized Households for area cost-per-unit outliers. Deliver in week 13.
Take to HUD Office of Multifamily Housing and HUD OIG.

##### 17. State (foreign assistance)

[Brief](agencies/state.md). Rank 16, score 3.0. C1 and C3, weeks 10-13.
Implementing-partner profile for the ten largest recipient countries from
ForeignAssistance.gov, USAspending and IATI; partner concentration and
competition; links to OFAC, UN and World Bank debarment lists; overhead and
unit cost outliers. Contractor screen on embassy construction and logistics.
Deliver in week 13. Take to State Office of Foreign Assistance and State OIG.

##### 18. NASA

[Brief](agencies/nasa.md). Rank 16, score 3.0. C1 and C2, weeks 9-12.
NASA SBIR/STTR in the duplicate-award screen; award mill check; supplier
screen on subawards under the largest primes. Deliver in week 12. Take to
NASA OIG.

##### 19. National Science Foundation

[Brief](agencies/nsf.md). Rank 16, score 3.0. C2 test bed, weeks 9-12.
Use NSF data to tune the text-similarity method first (week 9), then run
across all agencies. Deliver in week 12. Take to NSF OIG.

##### 20. Justice

[Brief](agencies/doj.md). Rank 20, score 2.9. Data partner (E) and C3.
The case library (F5) is the main DOJ product, finished in week 6 and kept
current weekly. In weeks 11-13 run C3 on Office of Justice Programs, OVW and
COPS subgrantees and price outliers on Bureau of Prisons commissary, medical
and telecom contracts. Take to Criminal Division Fraud Section, Civil
Division (False Claims Act) and DOJ OIG.

##### 21. Securities and Exchange Commission

[Brief](agencies/sec.md). Rank 21, score 2.8. Data partner (E), weeks 5-8.
Add EDGAR officers, Form D issuers and related persons to the entity spine;
flag federal award recipients whose officers appear in SEC litigation or
administrative releases, or in FINRA BrokerCheck disciplinary records.
Delivered as a spine feature in week 8 and a short memo. Take to SEC
Division of Enforcement as a data partner.

##### 22. USAID close-out

[Brief](agencies/usaid.md). Rank 24, score 2.5. C3, weeks 11-12.
Table of terminated awards with obligations far above outlays (possible
unreturned advances) and partners with prior OIG findings now receiving
State awards. Deliver in week 12. Take to State Office of Foreign
Assistance and USAID/State OIG.

##### 23. Development Finance Corporation

[Brief](agencies/dfc.md). Rank 29, score 2.1. C3, week 12.
Sanctions and exclusions check of every borrower and sponsor in DFC's
active projects list, plus ICIJ Offshore Leaks and OpenSanctions matches for
shell structures. Take to DFC Office of Accountability and DFC OIG.

##### 24. AmeriCorps

[Brief](agencies/cncs.md). Rank 30, score 2.0. C3, week 12.
Grantee risk list for the Foster Grandparent and AmeriCorps State and
National programs: prior OIG findings, cost per member versus peers, Form
990 revenue checks. Take to AmeriCorps Office of Grant Administration and
AmeriCorps OIG.

##### 25. PCOR Trust Fund

[Brief](agencies/pcortf.md). Rank 31, score 1.8. C2, week 12.
Add PCORI funded projects to the duplicate-award screen against NIH and
NSF; check awardees against LEIE and SAM. Take to PCORI and HHS OIG.

##### 26. Nuclear Regulatory Commission

[Brief](agencies/nrc.md). Rank 31, score 1.8. C1, week 13.
NRC contracts in the contractor screen; match suppliers named in public
10 CFR Part 21 defect reports and NRC enforcement actions against federal
contractor records. Take to NRC Office of Investigations and NRC OIG.

##### 27. Executive Office of the President

[Brief](agencies/eop.md). Rank 33, score 1.3. C3, week 13.
Grantee screen on ONDCP's HIDTA grants. EOP's main role is as audience: the
Phase 1 report is written for OMB's Office of Federal Financial Management.

#### Aggregate screens and access cases (weeks 10 to 14)

These agencies pay individuals whose data is confidential, so public data
can point only to places, intermediaries and programs. Each gets an
aggregate screen and a ready-to-send Phase 2 access proposal.

##### 28. Treasury (IRS)

[Brief](agencies/treasury.md). Rank 8, score 3.5. Weeks 10-13.
EITC and Additional Child Tax Credit hot-spot model from IRS SOI ZIP data
(tax years 2015-2023) against ACS income and household predictors; overlay
DOJ Tax Division preparer injunctions and IRS-CI cases; link ERC promoter
cases to PPP borrowers to size likely double dipping. Deliver the hot-spot
map and an IRS data-access proposal in week 13. Take to IRS Return Preparer
Office, IRS-CI, TIGTA and Treasury Office of Payment Integrity.

##### 29. Social Security Administration

[Brief](agencies/ssa.md). Rank 22, score 2.7. Weeks 10-13.
County SSI and disability outlier map from SSA state and county statistics,
adjusted with ACS age and disability and CDC PLACES health data; facilitator
network from charged disability cases (attorneys, doctors, representative
payees recurring across cases). With PBGC and OPM results, write the
cross-agency case for death data sharing. Take to SSA Office of Anti-Fraud
Programs, SSA OIG and Treasury Do Not Pay.

##### 30. Labor

[Brief](agencies/dol.md). Rank 26, score 2.4. Weeks 11-14.
State unemployment insurance dashboard from ETA 539 weekly claims, ETA 227
overpayment reports and Benefit Accuracy Measurement data: claims versus
local job loss, overpayment and fraud rates versus peers. Extract schemes
from charged UI cases into rules states can run (shared bank accounts,
addresses, IP addresses). Also review OLMS union financial filings for
embezzlement signals and EBSA plan data (with PBGC). Take to DOL ETA, DOL OIG
and state workforce agencies.

##### 31. Education

[Brief](agencies/ed.md). Rank 22, score 2.7. Weeks 11-13.
School-level ghost student risk ranking from FSA Title IV volume, Heightened
Cash Monitoring list, College Scorecard and IPEDS (online share, aid growth
versus completion and retention); owner links to closed or sanctioned
schools. Validate against colleges named in OIG and news reports. Take to
FSA Enforcement and Education OIG.

##### 32. FDIC

[Brief](agencies/fdic.md). Rank 27, score 2.3. Weeks 10-11.
PPP lender risk table joining SBA work results to FDIC BankFind and Call
Reports (share of each lender's PPP loans with fraud signals, fintech
partner channels). Pre-failure signal review for banks that failed
2019-2026. Take to FDIC OIG and FDIC Division of Risk Management
Supervision.

##### 33. Interior

[Brief](agencies/doi.md). Rank 27, score 2.3. Weeks 12-14.
Royalty-rate outlier table from ONRR Natural Resources Revenue Data
(royalty per unit of production by company, commodity, basin and year);
contractor screen on wildfire and land management contracts (C1). Take to
ONRR and DOI OIG.

### Phase 1 action items by week

The full list of dated action items. Owners use the short names from the
team table.

| Wk | Ending | Action items | Owner |
| --- | --- | --- | --- |
| 1 | Nov 6 | F2 repo layout; F10 FOIA requests filed; F4 watch lists started; agree team and roles; confirm agency order with Steve | Lead, DE |
| 2 | Nov 13 | F1 SBA playbook; F4 done; F3 spine ingest started; HHS and DoD pulls started; SBA 7(a)/504 pull | SBA, DE, AN |
| 3 | Nov 20 | F3 spine v1; F12 commercial data decision; HHS and DoD screens started | DE, Lead, AN |
| 4 | Nov 27 | F5 case library v0; F7 entity resolution tested; F8 scoring framework; F9 lead package template | INV, DE, AN |
| 5 | Dec 4 | HHS and DoD first scores; SBA extension results; DHS and USDA pulls; SEC enrichment starts | AN, DE |
| 6 | Dec 11 | F5 case library v1 and F6 OIG index; F11 counsel guidance; Wave 1 back-tests; SBA memo | INV, Lead, AN |
| 7 | Dec 18 | HHS and DoD lead lists and memos; first ten lead packages to counsel; DOT and GSA pulls | AN, INV |
| 8 | Jan 8 | Phase 2 access proposals sent (HHS-OIG, DoD OIG, SBA OIG, USDA OIG, DHS/CBP, GSA); FCC and OPM pilots start; SEC feature done | Lead, AN |
| 9 | Jan 15 | DHS, USDA, DOT, GSA screens scored; C1 and C2 start; NSF text-similarity tuning | AN, DE |
| 10 | Jan 22 | Wave 2 lead lists and memos; OPM reconciliation; C3 and aggregate screens start | AN |
| 11 | Jan 29 | FCC, VA, Commerce, PBGC pilot results; USACE results | AN |
| 12 | Feb 5 | C2 results (DOE, NSF, NASA, PCORTF); USAID, DFC, AmeriCorps; FDIC table | AN |
| 13 | Feb 12 | C1 and C3 results (EPA, HUD, State, DOJ, NRC, EOP); Treasury and SSA access proposals | AN, Lead |
| 14 | Feb 19 | DOL, ED, DOI results; all 33 review memos drafted; lead package QA | AN, INV |
| 15 | Feb 26 | Counsel review of referral set; memos final; Phase 1 report drafted | Lead, INV |
| 16 | Mar 5 | Referrals made; leadership briefings; Phase 2 go/no-go with Steve | Lead |

### Phase 1 success measures

- **Coverage.** A review memo for all 33 agencies by week 15.
- **Screen quality.** At least 10 screens pass the validation bar; hit rates
  reported for every screen, passing or not.
- **Leads.** At least 50 reviewed lead packages across at least 10 agencies,
  with the dollars they cover.
- **Access.** At least six Phase 2 access proposals sent by week 13 and at
  least two agencies or OIGs in active discussion by week 16.
- **Reuse.** Time to add a new agency to a shared screen under one week by
  week 12.

### Phase 1 risks

| Risk | Effect | Response |
| --- | --- | --- |
| FOIA responses late | USDA, DOT, CACFP labels missing | File in week 1; fall back to court records and press releases |
| Manifest data cost | DHS screen weaker | Start with mirror gaps and Census data; buy one product group only |
| Entity matching errors | False leads | 95% precision gate (F7); two-signal rule; human review |
| Too many leads to review | Backlog, quality drop | Cap at the top 25 per screen; investigator sets the order |
| Political sensitivity (EPA, USAID, State) | Findings misused | Facts-only profiles; no public release; referral only |
| Small team | Dates slip | Keep foundation and Wave 1 fixed; shift shared screens later |

## Phase 2: internal data to identify and prosecute fraud

### Why internal data matters

Public data can say *which entities look risky*. It cannot see the claim,
invoice, application or payment where the fraud happens. Internal data
changes three things:

1. **From entity to transaction.** Score each claim, invoice, loan or
   benefit payment, not just the payee.
2. **From lead to evidence.** Show the specific false statements, the
   dollars paid on them and who received the money. That is what a grand
   jury, a False Claims Act complaint or an administrative action needs.
3. **From recovery to prevention.** Run the same checks before money goes
   out: at enrollment, application, award and payment.

### Ideas: what internal data would enable

#### Cross-agency ideas (highest value)

These need data from more than one agency, which no single agency can do
alone. They are the strongest argument for a government-wide program.

| Idea | Internal data | What it finds | Lead agencies |
| --- | --- | --- | --- |
| Shared bank account screen | Payment file bank routing and account numbers across programs | One account receiving payments for many unrelated identities or entities | Treasury Fiscal Service, all payers |
| Full death data everywhere | SSA full death file | Payments to dead people in FEHB, PBGC, Medicare, VA, SNAP | SSA, Treasury Do Not Pay |
| Identity reuse across programs | SSN, address, phone, email, device and IP at application | One identity or device behind UI, SNAP, Medicaid, SBA and student aid claims | DOL, USDA, HHS, SBA, ED (via states) |
| Unified payee graph | Payee TINs, owners, bank accounts across grants, contracts, loans and benefits | Hidden common control across "separate" recipients | Treasury, GSA, OMB |
| Excluded-party enforcement | Internal claims and payments matched to all exclusion lists | Payments to excluded parties in any program | HHS, OPM, VA, GSA |
| Incarceration check | Bureau of Prisons and state prison data | Benefits paid to prisoners | DOJ, SSA, DOL, USDA |

#### Agency ideas

| Agency | Internal data | What it enables | Access route |
| --- | --- | --- | --- |
| HHS | Medicare claims, Medicaid T-MSIS claims, enrollment applications, PECOS, MA encounter data | Claim-level scoring; impossible-day and phantom-patient tests; MA risk-adjustment upcoding; patient recruitment rings | HHS-OIG; CMS Center for Program Integrity; CMS research data (VRDC) for analysis |
| DoD | Invoices (WAWF / PIEE), DCAA audits, subcontract payment data, CAGE and bid data | Invoice fraud, cost mischarging, losing bids for collusion tests, real pass-through shares | DCIS, DoD OIG, DPCAP |
| SBA | Loan applications, lender files, bank account and device data | Application-level identity fraud, lender and agent rings | SBA OIG (existing work) |
| USDA | SNAP EBT transactions (via states), retailer redemption data, CACFP claims | Trafficking from transaction patterns; sponsor claim tests | FNS; USDA OIG; state agencies |
| DHS | CBP entry data (ACE: declared value, origin, duty), FEMA applicant and payment data | Importer-level underpayment; duplicate disaster claims | CBP Office of Trade; HSI; FEMA FIID |
| DOT | Prime-to-DBE payments, state DBE review files | Proof of pass-through: money in versus work done | State DOTs; DOT OIG |
| GSA | SAM.gov sensitive fields (TINs, bank data), SmartPay transactions | Shell detection by shared TIN and bank account; purchase card misuse | GSA IAE; GSA OIG |
| Treasury | Returns, preparer PTINs on returns, ERC claims, payment files | Preparer-level EITC scoring; ERC claim screening; bank account reuse | IRS (6103 limits, see below); TIGTA |
| SSA | Payee and representative payee data, disability claims, full death file | Facilitator rings; payee abuse; death data for other agencies | SSA OIG; CDI units |
| VA | Compensation claims, community care claims, GI Bill enrollment certifications | Claim-level scoring; provider screens; school enrollment checks | VA OIG |
| OPM | FEHB carrier claims, retirement payee data | Provider claims after death or exclusion; dead annuitants | OPM OIG |
| DOL | State UI claims (identity, bank, IP data) | Cross-state duplicate claims, ring detection | States; DOL OIG; NASWA Integrity Data Hub |
| ED | FAFSA and enrollment data | Ghost student detection at application | FSA; Education OIG |
| HUD | Tenant income (EIV), payment and inspection files | Unreported income; landlord billing for empty units | HUD OIG; HUD CFO |
| FCC | USAC Lifeline subscriber data (National Verifier), E-Rate bid documents | Duplicate and phantom subscribers; full bid analysis | USAC; FCC OIG |
| Commerce | BEAD build-out verification, CHIPS milestone reports | Claimed coverage versus delivered | NTIA; Commerce OIG |
| PBGC | Participant data for SFA plans | Participant-level death checks | PBGC OIG |
| DOE, NSF, NASA, PCORTF | Full proposals and budgets, PI current-and-pending support | Duplicate funding at the proposal level | Each OIG |
| EPA, DOJ grants, AmeriCorps | Subrecipient financial reports, timesheets | Unsupported costs, stipend fraud | Each OIG |
| State, USAID, DFC | Partner financial reports, beneficiary lists, borrower KYC | Diversion and ghost beneficiaries; borrower ownership | Each OIG |
| Interior | Lease-level sales and valuation data | Royalty underpayment at the lease level | ONRR; DOI OIG |
| FDIC | Examination findings, loan-level data | Insider and borrower fraud before failure | FDIC OIG |
| NRC, EOP | Contract invoices; HIDTA grant reports | Ordinary contract and grant checks | Each OIG |

#### Prosecution support

Finding fraud is not enough; cases must hold up. Phase 2 adds:

- **Evidence-grade pipeline.** Locked data snapshots, logged queries,
  versioned code and reproducible outputs, so an analyst can testify to how
  a result was produced.
- **Case packages for prosecutors.** For each referral: the scheme, the
  claims or payments involved, total loss, the people who received the
  money, and a list of records to subpoena.
- **Limitations triage.** Rank cases by time left: five years for most
  federal fraud statutes, ten years for bank fraud and for PPP and EIDL
  fraud, and up to ten years under the False Claims Act.
- **Recovery focus.** Trace payments to accounts and assets to support
  seizure and forfeiture.
- **Feedback loop.** Outcomes of referred cases feed back into scoring.

### Access routes

Internal data comes through a small number of legal routes. They differ a
lot in speed.

| Route | How it works | Typical time to data | Best for |
| --- | --- | --- | --- |
| OIG partnership | Work under or alongside an Inspector General, who already has access under the IG Act and can act on findings | 2-4 months | HHS, DoD, SBA, USDA, VA, OPM |
| Agency pilot and data use agreement | Program integrity office shares data for a defined pilot | 3-6 months, plus security approval | CMS, FNS, GSA, FCC/USAC |
| Research data access | CMS Virtual Research Data Center and similar enclaves | 3-6 months | HHS claims analytics without a partnership |
| Computer matching agreement | Required under the Privacy Act for many cross-agency matches; approved by Data Integrity Boards | 6-12 months | Death data, identity reuse, cross-program matches |
| Treasury Do Not Pay | Treasury's central screening service, which already matches payments against death and exclusion data | 3-6 months to join for a use case | Cross-agency payment screens |
| State agreements | Data from states that run the program (SNAP EBT, UI, Medicaid) | 3-9 months per state | USDA, DOL, HHS Medicaid |
| Existing hubs | NASWA Integrity Data Hub (UI), CMS Healthcare Fraud Prevention Partnership (public-private health data sharing) | 2-6 months | DOL, HHS |

Two legal limits shape the plan:

- **Tax data (26 U.S.C. 6103)** can be shared only in narrow cases. IRS work
  should be done inside IRS or TIGTA, with us supplying methods and
  non-tax data, not by moving returns out.
- **Privacy Act and matching rules** mean cross-agency matching needs a
  matching agreement or an OIG exception. Starting with OIGs avoids the
  longest delays.

Recent policy may speed this up: the March 2025 executive order on
eliminating information silos directs agencies to give designated officials
access to unclassified records, and the 2026 anti-fraud task force makes
cross-agency fraud work a stated priority. The precedent to point to is
the Pandemic Response Accountability Committee's Pandemic Analytics Center
of Excellence, which matched data across agencies for pandemic programs
(check its current status: the committee's authority was set to end in
September 2025).

### Security and governance requirements

Agencies will ask for these before sharing data, so they are budgeted from
the start of Phase 2:

- A government-authorized environment (FedRAMP Moderate or High, or
  working inside the agency's or OIG's own enclave).
- An authority to operate for any system that holds agency data.
- Personnel suitability or background checks for analysts.
- Privacy impact assessment, data retention and destruction rules.
- Model documentation: what each score uses, how it was tested, and
  checks for bias against protected groups or places.
- A governance board with the OIG, program office and counsel that
  approves new uses of data.
- A contract vehicle or interagency agreement to pay for the work.

### Phase 2 timeline

Dates are estimates and depend mostly on how fast agreements are signed.

| Period | Dates | Goal | Main actions |
| --- | --- | --- | --- |
| 2a. Prepare | Jan - Mar 2027 (Phase 1 weeks 8-16) | Access proposals out | Six proposals in week 8 (HHS-OIG, DoD OIG, SBA OIG, USDA OIG, DHS/CBP, GSA); Treasury, SSA, DOL proposals in week 13; security plan and environment options; Phase 2 cost estimate |
| 2b. Agree | Mar - Jun 2027 | First two agreements signed | Pick two first pilots from the agencies that respond (likely HHS-OIG and one of DoD OIG or SBA OIG); data use agreements; environment authorized; analyst checks |
| 2c. First pilots | Jul - Dec 2027 | Claim- and invoice-level screens running | HHS: hospice and home health claim scoring. DoD or SBA: invoice and application screens. Weekly lead flow to the OIG; first case packages to prosecutors by Oct 2027 |
| 2d. Cross-agency | Oct 2027 - Jun 2028 | First cross-agency match | Death data case with SSA and Do Not Pay; matching agreement for one cross-program identity screen (for example UI with SNAP through two states); add USDA, DHS and GSA pilots |
| 2e. Scale | Jul - Dec 2028 | Program model proven | Pre-payment checks in at least one program; results report for OMB and the task force; proposal for a government-wide shared service |

### Phase 2 action items (first six months)

| ID | Action | Owner | Due |
| --- | --- | --- | --- |
| P1 | Write the access proposal template: problem, Phase 1 findings, data asked for, route, security, timeline, success measures | Lead | 2026-12-18 (Phase 1 week 7) |
| P2 | Send six access proposals (HHS-OIG, DoD OIG, SBA OIG, USDA OIG, DHS/CBP, GSA) | Lead | 2027-01-08 |
| P3 | Choose the secure environment approach (agency enclave, OIG enclave or our own authorized cloud) and estimate cost | DE | 2027-01-29 |
| P4 | Send Treasury, SSA and DOL proposals, including the death data case | Lead | 2027-02-12 |
| P5 | Request CMS research data access as a backup route for HHS analytics | AN | 2027-02-12 |
| P6 | Phase 2 go/no-go with Steve: budget, first two pilots | Lead | 2027-03-05 |
| P7 | Sign first data use agreement or OIG memorandum of understanding | Lead | 2027-05-28 |
| P8 | Environment authorized and analysts cleared | DE | 2027-06-25 |
| P9 | First pilot live on internal data | AN | 2027-07-30 |

### Phase 2 success measures

- Agreements signed with at least two agencies or OIGs by 2027-06.
- First internal-data pilot producing leads by 2027-08.
- First prosecutor-ready case package by 2027-10.
- Dollars identified, recovered or prevented, reported each quarter with
  the method used to count them.
- One cross-agency match running by mid-2028.

## Decisions for Steve

1. **Start date and team.** Is 2026-11-02 the right start, and who fills
   the five roles?
2. **Order.** Keep the [top33.md](agencies/top33.md) order, or move a target
   agency forward because of a meeting or contact?
3. **Commercial data.** Budget for vessel manifests and a corporate
   registry service (decision F12)?
4. **Referral route.** Refer leads only to OIGs and DOJ, or also consider
   False Claims Act filings with counsel?
5. **First Phase 2 partners.** Lead with OIGs (fastest) or with program
   offices (closer to prevention)?

## Sources

- [Top 33 ranking and shared screens](agencies/top33.md) and the agency
  briefs it links, which list the program-level sources used here.
- [Working plan](plan.md)
- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [GAO-24-105833: federal fraud losses estimated at $233B to $521B a year](https://www.gao.gov/products/GAO-24-105833)
- [GAO-24-105470: SBIR/STTR fraud vulnerabilities](https://www.gao.gov/products/GAO-24-105470)
- [GAO-26-108139: FEHB provider eligibility risks](https://files.gao.gov/reports/GAO-26-108139/index.html)
- [Oversight.gov: all Inspector General reports](https://www.oversight.gov/)
- [Treasury Do Not Pay](https://fiscal.treasury.gov/dnp/)
- [CMS Healthcare Fraud Prevention Partnership](https://www.cms.gov/medicare/medicaid-coordination/healthcare-fraud-prevention-partnership)
- [NASWA Integrity Data Hub](https://www.naswa.org/integrity-center/integrity-data-hub)
- [Privacy Act computer matching provisions (5 U.S.C. 552a(o))](https://www.law.cornell.edu/uscode/text/5/552a)
- [26 U.S.C. 6103: confidentiality of tax returns](https://www.law.cornell.edu/uscode/text/26/6103)
- [DOJ whistleblower program terms](https://www.justice.gov/fraud/whistleblower)
