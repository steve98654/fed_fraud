# Methodology: from public records to a scored lead

**Status:** Draft v0.1 (2026-11-01). Written before Phase 1 starts; it
states the method we will hold ourselves to. Thresholds marked *set in
week 4* are fixed when the scoring framework (item F8) is calibrated.

## Bottom line

One shared pipeline serves all 33 agencies. It joins public award,
provider and entity records into a single table of entities, runs a small
library of risk signals over it, and ranks entities by a score that always
comes with its reasons. No screen is used until it has been tested against
known fraud cases, and no lead leaves the team without two independent
signals, an investigator's review and, for the first ten, counsel review.
A dollar figure moves from *Pending* to *Confirmed* only when the office
that received the lead confirms it.

## 1. Data sources

Phase 1 uses only public and lawfully obtained data: federal open data,
state public records, court records, FOIA releases and licensed commercial
data. Nothing behind a login is scraped.

| Layer | Sources | Used for |
| --- | --- | --- |
| Entity and award spine | SAM.gov entity extract and exclusions; USAspending prime and subaward files FY2020-FY2026; FPDS contract actions | Who is paid, how much, for what, and their registered addresses, contacts and officers |
| Program data | CMS provider and owner files; FNS SNAP retailer data; USAC E-Rate data; state DBE directories and bid tabs; Census trade data; SBA loan-level releases | Agency-specific screens |
| Cross-keys | NPPES (NPI); SEC EDGAR (CIK); Form 990 (EIN, officers) | Linking the same entity across sources |
| Watch lists | SAM exclusions, HHS-OIG LEIE, OPM OIG debarments, OFAC lists, World Bank debarments, HUD LDP, USAC suspensions | Links to excluded or sanctioned parties |
| Case library | DOJ press releases 2020-2026 (2,000+ fraud releases tagged by agency, program, scheme and entity); OIG and GAO reports | Labels for validation, and scheme patterns |

Every pull is logged with its source, URL, date, row count and file hash,
so any figure can be traced to the data it came from.

## 2. Entity resolution

The same business or person appears under many spellings and addresses.
Entity resolution reuses the SBA matcher:

1. Standardize names (case, punctuation, legal suffixes) and addresses
   (USPS standard form, suite numbers kept).
2. Normalize phone numbers and contact emails to their domain.
3. Match records on combinations of these keys, plus UEI, NPI, CIK and EIN
   where present.
4. Group matched records into one entity, and link entities that share an
   address, phone or officer into networks.

**Quality check:** precision is measured on 500 hand-labeled pairs before
the spine is used; the target is 95% or better. Known benign hubs
(registered agents, incubators, large office buildings, hospitals) are
listed and down-weighted so they do not create false networks.

## 3. Signal library

Each signal has a written formula, a threshold and notes on false
positives. The shared signals are:

| Signal | What it measures | Typical innocent explanation |
| --- | --- | --- |
| Shared address | Unrelated entities at one address, beyond what the address type explains | Shared office buildings, registered agents |
| Shared officer or contact | One person or phone behind entities that present as independent | Legitimate affiliates that disclose the link |
| New entity, large award | Award size in the first 24 months after registration or enrollment, against peers | Spin-offs of established firms |
| Excluded link | Shared identifiers with an excluded, revoked or sanctioned party | Common names; old addresses |
| Peer outlier | Billing, price, length of stay or claims far outside peers in the same place and service | Specialty or case mix |
| Rapid growth | Payments or claims rising much faster than peers | Real expansion, mergers |
| Rotation and concentration | Winners taking turns; one consultant, lender or agent behind many outliers | Small markets with few providers |

Agency screens add program signals (for example mirror trade gaps for DHS
or meals per nearby child for USDA) built the same way.

## 4. Scoring and reason codes

- Each signal produces a value scaled against peers (the same program,
  place and period), so a hospice is compared with hospices in its county,
  not with every provider.
- The risk score combines the signals with weights fitted against the case
  library, so signals that actually separate known fraud count for more.
  *Weights set in week 4.*
- Every score carries **reason codes**: the signals that drove it, each with
  the source record and date. A score without reasons is never shown.
- **Two-signal rule:** an entity becomes a lead only when at least two
  independent signals fire. One strong signal alone is a question for
  review, not a lead.

## 5. Validation

Every screen is tested the same way before its leads are used.

1. **Back-test.** Take entities charged or settled in the case library for
   that program. Score the population as it looked *before* each case
   became public. Report how many known cases land in the top 1%, 5% and
   10% of scores.
2. **Hand review.** The investigator reviews 25 top-scored entities that
   are not known cases and records whether a reasonable reviewer would want
   to look further.
3. **Release bar.** A screen is released when known cases are at least
   **five times** more common in its top 5% than in the whole population,
   and at least **half** of the hand-reviewed sample is judged worth
   review.
4. **Report misses.** Screens that miss the bar are reported as such in the
   validation reports, then reworked or dropped.

Fairness check: scores are reviewed for patterns that track neighborhood
demographics rather than conduct, and signals that do so are removed.

## 6. From lead to referral

A **lead package** is what goes to an Inspector General or DOJ component,
one per entity or network:

- Summary: who, which program, how much money, which scheme it resembles.
- Signals with source records and dates; network view; peer comparison.
- Known-case match: the charged cases it most resembles.
- Limits: what public data cannot show, and innocent explanations checked.
- Provenance: data pulls and script versions.

Packages are reviewed by the investigator and the program lead, and the
first ten by counsel. Nothing is published, and no lead names a person in
any public document.

## 7. How a figure moves from Pending to confirmed savings

The scorecard shows *Pending* for every agency until a figure has passed
through these stages. Each stage has an owner and evidence.

| Stage | What it means | Who decides | Evidence kept |
| --- | --- | --- | --- |
| Pending | No validated screen or delivered lead yet | (default) | None |
| Identified | Dollars paid to entities in a delivered lead package, from public award or payment records | Program lead, after validation and package review | Package, data pulls, script version |
| Referred | The package has been accepted for review by an OIG or DOJ component | Receiving office | Referral record and date |
| Confirmed | Dollars the receiving office confirms as recovered, prevented or subject to a judgment, settlement or payment stop | Receiving office | Written confirmation, case or docket reference |

Rules that keep the numbers honest:

- **Identified is not fraud.** It is the money paid to entities under
  review, reported as an upper bound.
- **Only Confirmed counts as savings.** The headline savings figure is the
  confirmed total; identified and referred amounts are shown separately.
- **No double counting.** A dollar is counted once, under the idea that
  produced the lead, even if several offices act on it.
- **No estimates.** Program exposure figures (such as GAO improper payment
  rates) appear as context, never as savings.

## 8. Limits

- Public data lag one to two years and show entities and awards, not the
  claim or invoice where fraud happens. Phase 1 finds risky entities, not
  proven fraud.
- Some programs (tax credits, individual benefits) publish no payee data,
  so their review uses aggregate screens and a Phase 2 data request.
- The case library over-represents schemes that have been prosecuted, so
  new schemes may score low until they appear in cases.

Phase 2 addresses these limits with internal data reached through
Inspectors General: claims, invoices, applications and payment files.

## Sources

- [Review plan](../review_plan.md): items F3-F9, "Validation" and "Lead
  packages".
- [Roadmap](../roadmap.md) and the [SBA case study](sba-case-study.md).
- [GAO-24-105833: federal fraud losses estimated at $233B to $521B a year](https://www.gao.gov/products/GAO-24-105833)
