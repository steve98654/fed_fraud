# Every federal agency: coverage plan beyond the top 33

**Status:** Draft v0.1 (2026-11-03), for Steve's review. Public data only.
Extends the [top 33 ranking](../agencies/top33.md), the
[review plan](../review_plan.md) and the [roadmap](../roadmap.md) to every
federal body we could identify, and relies on the
[forensic methods handbook](../playbook/forensic_methods.md) for how each
test is computed.

## Bottom line

We identified **137 federal bodies**: the 111 agencies on USAspending's
list, 19 bodies that are not on it (the Postal Service, TVA, Amtrak, the
judiciary, the legislative branch and others) and 7 government corporations
that report through a parent department. Every one now has a tier and a
named set of screens.

- **The top 33 already cover 99.9% of the money USAspending reports.** In
  FY2026 they paid out $9,561 billion of $9,570 billion; the other 78
  listed agencies together paid about $8.2 billion. Going broader is not
  mainly about dollars in USAspending.
- **Going broader matters for three other reasons.** First, large money
  sits outside USAspending's list (the Postal Service, TVA, the federal
  judiciary). Second, small agencies bring schemes the top 33 do not
  (court-appointed counsel vouchers, settlement refund claims, arts and
  regional grants). Third, a government-wide proposal to OMB and the
  Inspectors General needs every agency covered, not just the large ones.
- **Only 15 agencies report improper payment estimates** (FY2025: about
  $186 billion across 64 programs, GAO-26-108694). The other 120-plus
  bodies have no measured error rate at all, which is itself a finding to
  put in front of OMB.
- **Eight universal screens (U1 to U8) cover every body cheaply.** Six run
  on public data already in the entity spine (award-level number tests,
  split awards, contract growth, recipient integrity, Single Audit findings
  and DATA Act reconciliation); two need internal data (charge cards and
  payroll, death and Do Not Pay matching).
- **Four new shared screens (C4 to C7)** join C1 to C3: credit and
  guarantees, benefit and annuity rolls, settlement and refund
  distributions, and time-and-voucher billing.
- **22 bodies get their own idea IDs** (Tier B), such as RRB-1 (railroad
  disability benefits), USPS-1 (postal contracts outside FPDS), JUD-1
  (Criminal Justice Act vouchers) and CFPB-1 (Civil Penalty Fund payments).
- **Timing:** universal screens are built on the top 33 in Phase 1 weeks
  11 to 14 and then run on every body in a **Phase 1b, weeks 17 to 26
  (2027-03-08 to 2027-05-14)**, so the Phase 1 plan does not slip.

## How we built the list

| Source | What it gave | Rows |
| --- | --- | --- |
| USAspending toptier agency list, FY2026 Q4, pulled 2026-11-03 | Every agency that reports to USAspending, with outlays, budgetary resources and obligations | 111 |
| 31 U.S.C. 9101 (Government Corporation Control Act) | Wholly owned and mixed-ownership government corporations | 26 named; 7 report through a parent department, 4 are on USAspending's list, the rest are closed, merged or privately owned |
| Our additions | Bodies that spend federal money but are not on USAspending's list: Postal Service, TVA, Amtrak, federal judiciary, Library of Congress, GPO, Architect of the Capitol, CBO, Congress, Smithsonian, Legal Services Corporation, Corporation for Public Broadcasting, U.S. Institute of Peace, FHFA, Farm Credit Administration, Postal Regulatory Commission | 16 |
| Out of scope, listed for completeness | Federal Reserve; Fannie Mae, Freddie Mac and the Federal Home Loan Banks; Farm Credit System banks. None is funded by appropriations, and each has its own regulator and OIG | 3 |

Notes on the figures:

- Outlays are USAspending's FY2026 figures as reported by agencies; they may
  be revised. The raw pull is in
  [data/usaspending_toptier_fy2026.csv](data/usaspending_toptier_fy2026.csv)
  and the classified list in [data/all_agencies.csv](data/all_agencies.csv),
  built by `analytics/universe/build_universe.py`.
- We give **no dollar figure** for bodies outside USAspending's list,
  because we have not yet pulled a comparable source. Their spending is to
  be sized from their own financial reports in week 17.
- Nine listed agencies report zero FY2026 outlays. One of them, the
  Railroad Retirement Board, pays billions in benefits that are not
  reported to USAspending under its name; it is treated as Tier B.
- Statutory names that no longer exist (the Resolution Trust Corporation,
  closed 1995; the Panama Canal Commission, ended 1999; the Pennsylvania
  Avenue Development Corporation, dissolved 1996) are not counted.

## Tiers

| Tier | Meaning | Count | Coverage |
| --- | --- | --- | --- |
| A | The top 33 by outlays, plus 7 government corporations inside them (CCC, FCIC, Ginnie Mae, FHA Fund, Federal Prison Industries, CDFI Fund, St. Lawrence Seaway) | 33 + 7 | Own plan in the roadmap, plus all universal and relevant shared screens |
| B | Outside the top 33, with a distinct payment stream worth its own investigation idea | 22 | Own idea ID, shared screens, universal screens |
| C | Smaller agencies, commissions, boards, foundations and legislative bodies | 63 | Universal screens, plus a shared screen where one fits |
| D | Listed by USAspending with no FY2026 outlays | 9 | Check where their spending is reported; no screens until it is found |
| X | Out of scope: not appropriated funds, own regulator and OIG | 3 | None; referenced only where they touch a federal program |

## Universal screens: one set of tests for every body

Every body that spends money awards contracts or grants, pays staff, holds
charge cards and reports to Treasury. These eight screens use the same code
for all of them. Section numbers refer to the
[forensic methods handbook](../playbook/forensic_methods.md).

| ID | Screen | Data | Method (handbook section) | Output per body | Phase |
| --- | --- | --- | --- | --- | --- |
| U1 | Award number tests | USAspending contract and grant actions FY2020-FY2026 | First-two-digit Benford with MAD, round-number and duplication tests, bunching under the micro-purchase and simplified acquisition thresholds (3, 5.4) | Conformity table and any threshold spikes | 1 |
| U2 | Split and duplicate awards | Same | Same recipient, same office, actions within 30 days each under a threshold but summing over it; repeated identical actions (4.1, 4.2) | List of action groups for review | 1 |
| U3 | Contract growth | FPDS modifications | Ratio of current to base value against peers in the same product code; sole-source modifications after competitive award; robust z (5.2) | Contracts above the peer tail | 1 |
| U4 | Recipient integrity | Entity spine and watch lists | Excluded links, new entity with large award, shared-attribute networks, co-location (7, 8) | Recipients with two or more independent signals | 1 |
| U5 | Single Audit check | Federal Audit Clearinghouse (fac.gov) | Repeat findings, questioned costs, auditor concentration, drawdown-to-audit gaps (11.1) | Grantees with repeat findings and continuing awards | 1 |
| U6 | DATA Act reconciliation | USAspending account (File A/B) and award (File C, D1/D2, F) data | Account-to-award gap, unlinked awards, subawards above the prime (11.1) | Share of spending not visible at payee level | 1 |
| U7 | Charge card, payroll and vendor master | OIG charge card risk assessments (public); card, payroll and vendor files (internal) | Split purchases, merchant category tests, vendor-employee matches, audit-trail tests (4.2, 11.2) | Card and payroll exceptions | 2 |
| U8 | Death and Do Not Pay match | Treasury Do Not Pay; payee files | Payments after death or to excluded payees (4.4, 9) | Payee exceptions | 2 |

**Why this is cheap.** U1 to U6 run on data the entity spine already
ingests for the top 33 (review plan items F3 and F4, plus fac.gov). Adding a
body means filtering by its agency code, not building a new pipeline. The
cost per added body is review time, roughly half a day of analyst time for
a Tier C body with nothing unusual.

## Shared screens, old and new

| ID | Screen | Status | Members outside the top 33 |
| --- | --- | --- | --- |
| C1 | Contractor screen | In review plan | USPS, TVA, Amtrak, judiciary, legislative agencies, Smithsonian, NARA, Peace Corps, CSOSA, regulatory commissions with large contracts |
| C2 | Research award screen | In review plan | NEA, NEH and IMLS (duplicate funding by text similarity) |
| C3 | Grantee screen | In review plan | Regional commissions, Gulf Coast council, foundations, LSC, CPB, MCC, USAGM, USTDA, EAC |
| C4 | Credit and guarantee screen | **New** | EXIM, FCSIC, NCUA, OPIC legacy portfolio; with SBA, USDA, HUD, ED, Treasury (CDFI), DFC |
| C5 | Benefit and annuity rolls | **New** (Phase 2) | RRB, Armed Forces Retirement Home; with SSA, OPM, VA, DOL, PBGC |
| C6 | Settlement and refund distributions | **New** | CFPB, FTC, CFTC; with SEC and DOJ |
| C7 | Time and voucher billing | **New** (mostly Phase 2) | Federal judiciary and DC Courts (court-appointed counsel), USPS (workers' compensation providers); with HHS, DOL, VA |

**C4. Credit and guarantee screen.** Reuses the SBA loan methods on every
federal credit program: straw and shell borrowers through entity
resolution, broker and lender centrality in the borrower network, bunching
just under program caps, and repeat defaults by linked borrowers. EXIM
publishes authorization-level data; other programs publish loan-level
files of varying depth.

**C5. Benefit and annuity rolls.** Death, incarceration and concurrent
eligibility tests on payee files, plus provider outliers in disability
determinations. Almost all of it needs internal data, so its Phase 1
product is a single data-access proposal covering several payers at once,
which is the cross-agency death data idea X-1 in the roadmap.

**C6. Settlement and refund distributions.** Agencies that return money to
harmed consumers or investors (CFPB's Civil Penalty Fund, FTC refunds, SEC
Fair Funds, CFTC restitution) pay through claims administrators. The risks
are synthetic and duplicate claimants and administrator overbilling. Phase
1 reviews published distribution reports for unexplained per-claimant
amounts; Phase 2 runs duplicate and identity tests on claims files.

**C7. Time and voucher billing.** Anyone paid by the hour or the service
can bill an impossible day. The impossible-day test (more than 24 hours, or
many days over 16) and peer outliers by matter type need voucher data,
which the courts and DOL hold.

## Tier B: new investigation ideas

IDs follow the roadmap's scheme. "Take to" is the body's own Inspector
General unless noted.

| ID | Body | Idea | Data | Phase | Take to |
| --- | --- | --- | --- | --- | --- |
| RRB-1 | Railroad Retirement Board | Disability and sickness benefit outliers by employer, occupation and examining physician; the Long Island Rail Road disability prosecutions (from 2011) are the reference case | RRB statistical tables (P1); claims files (P2) | 1b, 2 | RRB OIG |
| RRB-2 | Railroad Retirement Board | Annuities paid after death; joins C5 | Payee files and death data | 2 | RRB OIG |
| USPS-1 | Postal Service | Supplier and highway contract route screen. USPS buys outside the FAR and does not report to FPDS, so contract data come by FOIA or through the OIG | FOIA release (P1b); contract files (P2) | 1b | USPS OIG |
| USPS-2 | Postal Service | Workers' compensation provider outliers for postal claimants; joins C7 | DOL OWCP data | 2 | USPS OIG, DOL OIG |
| TVA-1 | Tennessee Valley Authority | Supplier integrity screen (C1); data access route to confirm | TVA procurement data | 1b | TVA OIG |
| AMTRAK-1 | Amtrak | Contractor and subcontractor screen on federal grants to Amtrak (C1, C3) | USAspending grants and subawards | 1b | Amtrak OIG |
| JUD-1 | Federal judiciary | Criminal Justice Act attorney and expert vouchers: impossible days, peer outliers by case type (C7) | Voucher data via the Administrative Office | 2 | Judiciary (no statutory OIG); proposal to the Administrative Office |
| DCC-1 | DC Courts | Court-appointed counsel vouchers, same tests as JUD-1 (C7) | Voucher data | 2 | DC Courts |
| EXIM-1 | Export-Import Bank | Exporter, buyer and lender shell checks on authorizations (C4) | EXIM authorization data, SAM.gov, sanctions lists | 1b | EXIM OIG |
| MCC-1 | Millennium Challenge Corporation | Compact implementers and contractors against World Bank and other development bank debarment lists (C3) | USAspending, debarment lists | 1b | MCC (via USAID OIG oversight arrangement, to confirm) |
| CFPB-1 | Consumer Financial Protection Bureau | Civil Penalty Fund and redress payments: duplicate and synthetic claimant tests (C6) | Fund reports (P1b); claims (P2) | 1b, 2 | Fed Board and CFPB OIG |
| FTC-1 | Federal Trade Commission | Consumer refund programs: duplicate and synthetic claimant tests (C6) | Refund reports (P1b); claims (P2) | 1b, 2 | FTC OIG |
| ARTS-1 | NEA, NEH, IMLS | Duplicate funding of the same project across the three (text similarity on award descriptions), plus Single Audit findings (C2, C3) | USAspending descriptions, fac.gov | 1b | Each OIG |
| REG-1 | ARC, Delta Regional Authority, Denali, NBRC, SCRC | Overlap of regional commission grants with EDA, USDA Rural Development and each other for the same project and recipient (C3) | USAspending, fac.gov | 1b | Each commission's OIG or designated OIG |
| RESTORE-1 | Gulf Coast Ecosystem Restoration Council | RESTORE Act grants: subrecipient reconciliation and grantee screen (C3, U6) | USAspending, fac.gov | 1b | Commerce OIG, which serves as the Council's OIG (to confirm) |
| LSC-1 | Legal Services Corporation | Legal aid grantee screen with Single Audit findings (C3, U5) | LSC grantee data, fac.gov | 1b | LSC OIG |
| CPB-1 | Corporation for Public Broadcasting | Station grants against station financial reports (C3, U5) | CPB station data, fac.gov | 1b | CPB OIG |
| USAGM-1 | U.S. Agency for Global Media | Grantee network and contractor screen (C1, C3) | USAspending, Form 990 | 1b | State OIG, which oversees USAGM |

## Tier C: how small bodies are covered

Most Tier C bodies spend mainly on salaries, rent and a modest number of
contracts. For them the universal screens are the review: U1 to U6 in Phase
1b, with a one-page memo each stating what was run and either a lead list or
"nothing actionable from public data". Groups:

- **Regulatory commissions and boards** (41, for example NLRB, EEOC, NTSB,
  CPSC, FEC): U1 to U6 and C1 for the few with large contracts.
- **Foundations and scholarship trusts** (Goldwater, Truman, Madison,
  Udall, African Development Foundation, Inter-American Foundation,
  Japan-U.S. Friendship Commission): C3 and U5 on their grantees.
- **Legislative branch** (Library of Congress, GPO, Architect of the
  Capitol, CBO, Congress, and GAO as an audience as much as a subject): C1
  where contracts are reported, and congressional office disbursement
  reports for U1-style number tests.
- **Assessment-funded regulators** (FHFA, Farm Credit Administration, NCUA,
  FCSIC): their own spending gets U1 to U6; the systems they supervise are
  out of scope except where federal guarantees are at stake (C4).

## Tier D: agencies with no reported outlays

Nine listed agencies show zero FY2026 outlays: the 400 Years of
African-American History Commission, the Commission for the Preservation
of America's Heritage Abroad, FFIEC, the Kennedy Center, the National
Council on Disability, the Office of Navajo and Hopi Indian Relocation, the
Southwest Border Regional Commission, the U.S. Interagency Council on
Homelessness and the Vietnam Education Foundation. Some are funded through
another agency's accounts, some are inactive. Week 17 task: find where each
one's spending is reported, then move it to Tier C or retire it from the
list.

## Schedule

| Weeks | Dates | Work |
| --- | --- | --- |
| 11-14 (Phase 1) | 2027-01-25 to 2027-02-19 | Build U1 to U6 on the top 33; validate U1 and U4 against the case library |
| 15-16 (Phase 1) | 2027-02-22 to 2027-03-05 | Add universal screen results to the 33 review memos |
| 17 | 2027-03-08 to 2027-03-12 | Size Tier B bodies outside USAspending from their own financial reports; trace Tier D spending; file FOIA for USPS and TVA contract data |
| 17-20 | 2027-03-08 to 2027-04-02 | Run U1 to U6 on all Tier B and C bodies; build C4 and C6 |
| 19-24 | 2027-03-22 to 2027-04-30 | Tier B ideas that run on public data (EXIM-1, MCC-1, ARTS-1, REG-1, RESTORE-1, LSC-1, CPB-1, USAGM-1, AMTRAK-1) |
| 23-26 | 2027-04-19 to 2027-05-14 | Memos for every Tier B and C body; C5 and C7 access proposals; government-wide summary for OMB and CIGIE |

Phase 1b assumes the Phase 1 team stays in place. It adds no new data
purchases; FOIA responses for USPS and TVA may arrive after week 26, in
which case those ideas move to Phase 2.

## What Phase 1b will and will not show

- It **will** show, for every federal body, which universal tests were run,
  what they found and what internal data would add.
- It **will not** produce savings. As everywhere on this project, a figure
  moves from Pending only through the stages in the methodology, and only
  confirmed dollars count.
- For most Tier C bodies the honest expected result is "nothing actionable
  from public data". That result still matters: it documents coverage for a
  government-wide proposal and shows where internal-control data (U7, U8)
  are needed.

## Improper payment reporting, FY2025

For every body's budget and a rough order-of-magnitude fraud estimate, see
[budget_fraud_rom.md](budget_fraud_rom.md).

Context only, never savings. Source: PaymentAccuracy.gov agencies and
programs page, FY2025 data; "susceptible outlays" are outlays in programs
the agency has found susceptible to significant improper payments, not
improper payments.

| Agency | Susceptible outlays ($M) | Susceptible programs | Improper payment rate |
| --- | --- | --- | --- |
| HHS | 1,670,124 | 10 | 5.83% |
| SSA | 1,494,212 | 3 | 0.76% |
| Defense (War) | 241,689 | 8 | 0.72% |
| VA | 201,103 | 7 | 1.09% |
| Education | 185,708 | 3 | 0.71% |
| OPM | 176,584 | 2 | 0.25% |
| USDA | 148,306 | 10 | 9.05% |
| Treasury | 105,743 | 7 | 26.54% |
| DOT | 67,068 | 2 | 3.57% |
| SBA | 66,238 | 8 | 12.29% |
| HUD | 50,439 | 2 | 0.0% |
| Labor | 41,634 | 2 | 12.16% |
| DHS | 21,631 | 3 | 0.15% |
| FCC | 2,741 | 2 | 5.03% |
| AmeriCorps | 478 | 2 | 2.64% |

Every other agency on the page shows no susceptible outlays. GAO reports 64
programs with estimates in FY2025; the page's susceptible-program counts sum
to 70, a difference we have not reconciled. Some programs show "did not
report", including TANF.

## Full list outside the top 33

Outlays are FY2026 USAspending outlays in millions of dollars; "not listed"
means the body is not on USAspending's agency list. Coverage codes: U1-U6
public universal screens, U7-U8 internal universal screens, C1 to C7 shared
screens. The top 33 are in the [ranking](../agencies/top33.md).

| Body | Kind | Outlays ($M) | Tier | Coverage |
| --- | --- | --- | --- | --- |
| Millennium Challenge Corporation (MCC) | Government corporation | 531 | B | C3 U1-U6 U7-U8 (MCC-1) |
| U.S. Agency for Global Media (USAGM) | Independent agency | 523 | B | C3 C1 U1-U6 U7-U8 (USAGM-1) |
| Consumer Financial Protection Bureau (CFPB) | Independent agency | 435 | B | C6 C1 U1-U6 U7-U8 (CFPB-1) |
| Export-Import Bank of the United States (EXIM) | Government corporation | 401 | B | C4 U1-U6 U7-U8 (EXIM-1) |
| Federal Trade Commission (FTC) | Regulatory commission or board | 356 | B | C6 C1 U1-U6 U7-U8 (FTC-1) |
| District of Columbia Courts (DC COURTS) | Judicial branch or court-related | 298 | B | C7 C1 U1-U6 U7-U8 (DCC-1) |
| Institute of Museum and Library Services (IMLS) | Foundation, endowment or trust fund | 217 | B | C3 U1-U6 U7-U8 (ARTS-1) |
| Gulf Coast Ecosystem Restoration Council (GCERC) | Regional commission | 179 | B | C3 U1-U6 U7-U8 (RESTORE-1) |
| National Endowment for the Arts (NEA) | Foundation, endowment or trust fund | 137 | B | C3 U1-U6 U7-U8 (ARTS-1) |
| Delta Regional Authority (DRA) | Regional commission | 75 | B | C3 U1-U6 U7-U8 (REG-1) |
| National Endowment for the Humanities (NEH) | Foundation, endowment or trust fund | 62 | B | C3 U1-U6 U7-U8 (ARTS-1) |
| Denali Commission (DENALI) | Regional commission | 49 | B | C3 U1-U6 U7-U8 (REG-1) |
| Northern Border Regional Commission (NBRC) | Regional commission | 44 | B | C3 U1-U6 U7-U8 (REG-1) |
| Appalachian Regional Commission (ARC) | Regional commission | 13 | B | C3 U1-U6 U7-U8 (REG-1) |
| Southeast Crescent Regional Commission (SCRC) | Regional commission | 11 | B | C3 U1-U6 U7-U8 (REG-1) |
| Corporation for Public Broadcasting (CPB) | Federally funded nonprofit corporation | not listed | B | C3 U1-U6 U7-U8 (CPB-1) |
| Federal Judiciary (Administrative Office of the U.S. Courts) (JUD) | Judicial branch | not listed | B | C7 C1 U1-U6 U7-U8 (JUD-1) |
| Legal Services Corporation (LSC) | Federally funded nonprofit corporation | not listed | B | C3 U1-U6 U7-U8 (LSC-1) |
| National Railroad Passenger Corporation (Amtrak) (AMTRAK) | Government corporation | not listed | B | C3 C1 U1-U6 U7-U8 (AMTRAK-1) |
| Railroad Retirement Board (RRB) | Independent agency | 0 | B | C5 U7-U8 (RRB-1, RRB-2) |
| Tennessee Valley Authority (TVA) | Government corporation | not listed | B | C1 U1-U6 U7-U8 (TVA-1) |
| United States Postal Service (USPS) | Independent establishment (off-budget) | not listed | B | C7 C1 U1-U6 U7-U8 (USPS-1, USPS-2) |
| Government Accountability Office (GAO) | Legislative branch | 817 | C | C1 U1-U6 U7-U8 |
| National Archives and Records Administration (NARA) | Independent agency | 647 | C | C1 U1-U6 U7-U8 |
| Equal Employment Opportunity Commission (EEOC) | Regulatory commission or board | 382 | C | C1 U1-U6 U7-U8 |
| Peace Corps (PC) | Independent agency | 377 | C | C1 U1-U6 U7-U8 |
| Commodity Futures Trading Commission (CFTC) | Regulatory commission or board | 324 | C | C6 C1 U1-U6 U7-U8 |
| Presidio Trust (PRESIDIO) | Government corporation | 306 | C | C1 U1-U6 U7-U8 |
| National Labor Relations Board (NLRB) | Regulatory commission or board | 255 | C | C1 U1-U6 U7-U8 |
| Court Services and Offender Supervision Agency (CSOSA) | Judicial branch or court-related | 243 | C | C1 U1-U6 U7-U8 |
| Farm Credit System Insurance Corporation (FCSIC) | Government corporation | 228 | C | C4 U1-U6 U7-U8 |
| National Transportation Safety Board (NTSB) | Regulatory commission or board | 130 | C | C1 U1-U6 U7-U8 |
| Consumer Product Safety Commission (CPSC) | Regulatory commission or board | 129 | C | C1 U1-U6 U7-U8 |
| Armed Forces Retirement Home (AFRH) | Independent agency | 117 | C | C5 C1 U1-U6 U7-U8 |
| International Trade Commission (USITC) | Regulatory commission or board | 111 | C | C1 U1-U6 U7-U8 |
| American Battle Monuments Commission (ABMC) | Regulatory commission or board | 101 | C | C1 U1-U6 U7-U8 |
| Federal Election Commission (FEC) | Regulatory commission or board | 71 | C | U1-U6 U7-U8 |
| United States Trade and Development Agency (USTDA) | Independent agency | 58 | C | C3 U1-U6 U7-U8 |
| Election Assistance Commission (EAC) | Regulatory commission or board | 57 | C | C3 U1-U6 U7-U8 |
| Merit Systems Protection Board (MSPB) | Regulatory commission or board | 45 | C | U1-U6 U7-U8 |
| United States Court of Appeals for Veterans Claims (CAVC) | Judicial branch or court-related | 41 | C | U1-U6 U7-U8 |
| Surface Transportation Board (STB) | Regulatory commission or board | 38 | C | U1-U6 U7-U8 |
| Defense Nuclear Facilities Safety Board (DNFSB) | Regulatory commission or board | 37 | C | U1-U6 U7-U8 |
| Federal Maritime Commission (FMC) | Regulatory commission or board | 36 | C | U1-U6 U7-U8 |
| Federal Permitting Improvement Steering Council (FPISC) | Regulatory commission or board | 30 | C | C3 U1-U6 U7-U8 |
| Council of the Inspectors General on Integrity and Efficiency (CIGIE) | Independent agency | 28 | C | U1-U6 U7-U8 |
| Selective Service System (SSS) | Independent agency | 28 | C | U1-U6 U7-U8 |
| Office of Special Counsel (OSC) | Independent agency | 27 | C | U1-U6 U7-U8 |
| Federal Mediation and Conciliation Service (FMCS) | Independent agency | 26 | C | U1-U6 U7-U8 |
| Federal Labor Relations Authority (FLRA) | Regulatory commission or board | 21 | C | U1-U6 U7-U8 |
| Office of Government Ethics (OGE) | Independent agency | 18 | C | U1-U6 U7-U8 |
| Inter-American Foundation (IAF) | Foundation, endowment or trust fund | 14 | C | C3 U1-U6 U7-U8 |
| Federal Mine Safety and Health Review Commission (FMSHRC) | Regulatory commission or board | 14 | C | U1-U6 U7-U8 |
| National Mediation Board (NMB) | Regulatory commission or board | 13 | C | U1-U6 U7-U8 |
| Occupational Safety and Health Review Commission (OSHRC) | Regulatory commission or board | 12 | C | U1-U6 U7-U8 |
| United States Chemical Safety Board (CSB) | Regulatory commission or board | 12 | C | U1-U6 U7-U8 |
| Commission on Civil Rights (USCCR) | Regulatory commission or board | 12 | C | U1-U6 U7-U8 |
| Privacy and Civil Liberties Oversight Board (PCLOB) | Regulatory commission or board | 11 | C | U1-U6 U7-U8 |
| Advisory Council on Historic Preservation (ACHP) | Regulatory commission or board | 10 | C | U1-U6 U7-U8 |
| National Capital Planning Commission (NCPC) | Regulatory commission or board | 10 | C | U1-U6 U7-U8 |
| Committee for Purchase from People Who Are Blind or Severely Disabled (ABILITYONE) | Independent agency | 10 | C | U1-U6 U7-U8 |
| Access Board (USAB) | Independent agency | 9.4 | C | U1-U6 U7-U8 |
| Morris K. Udall and Stewart L. Udall Foundation (UDALL) | Foundation, endowment or trust fund | 8.9 | C | C3 U1-U6 U7-U8 |
| African Development Foundation (USADF) | Foundation, endowment or trust fund | 8.6 | C | C3 U1-U6 U7-U8 |
| Commission of Fine Arts (CFA) | Regulatory commission or board | 8.1 | C | U1-U6 U7-U8 |
| Harry S Truman Scholarship Foundation (TRUMAN) | Foundation, endowment or trust fund | 5.3 | C | C3 U1-U6 U7-U8 |
| Nuclear Waste Technical Review Board (NWTRB) | Regulatory commission or board | 3.2 | C | U1-U6 U7-U8 |
| Marine Mammal Commission (MMC) | Regulatory commission or board | 3.1 | C | U1-U6 U7-U8 |
| Administrative Conference of the U.S. (ACUS) | Independent agency | 3.0 | C | U1-U6 U7-U8 |
| Public Buildings Reform Board (PBRB) | Regulatory commission or board | 2.9 | C | U1-U6 U7-U8 |
| Barry Goldwater Scholarship and Excellence In Education Foundation (GOLDWATER) | Foundation, endowment or trust fund | 2.1 | C | C3 U1-U6 U7-U8 |
| National Credit Union Administration (NCUA) | Independent agency | 2.1 | C | C4 U1-U6 U7-U8 |
| James Madison Memorial Fellowship Foundation (MADISON) | Foundation, endowment or trust fund | 2.0 | C | C3 U1-U6 U7-U8 |
| Japan-United States Friendship Commission (JUSFC) | Foundation, endowment or trust fund | 1.6 | C | C3 U1-U6 U7-U8 |
| Overseas Private Investment Corporation (OPIC) | Government corporation | 0.4 | C | C4 U1-U6 U7-U8 |
| Architect of the Capitol (AOC) | Legislative branch | not listed | C | C1 U1-U6 U7-U8 |
| Congressional Budget Office (CBO) | Legislative branch | not listed | C | U1-U6 U7-U8 |
| Farm Credit Administration (FCA) | Independent regulator (assessment-funded) | not listed | C | U1-U6 U7-U8 |
| Federal Housing Finance Agency (FHFA) | Independent regulator (assessment-funded) | not listed | C | U1-U6 U7-U8 |
| Government Publishing Office (GPO) | Legislative branch | not listed | C | C1 U1-U6 U7-U8 |
| House of Representatives and Senate (CONGRESS) | Legislative branch | not listed | C | U1-U6 U7-U8 |
| Library of Congress (LOC) | Legislative branch | not listed | C | C1 U1-U6 U7-U8 |
| Postal Regulatory Commission (PRC) | Regulatory commission or board | not listed | C | U1-U6 U7-U8 |
| Smithsonian Institution (SI) | Trust instrumentality | not listed | C | C1 U1-U6 U7-U8 |
| United States Institute of Peace (USIP) | Federally funded nonprofit corporation | not listed | C | U1-U6 U7-U8 |
| 400 Years of African-American History Commission (AAHC) | Regulatory commission or board | 0 | D | None |
| Commission for the Preservation of America's Heritage Abroad (HERITAGEABROAD) | Regulatory commission or board | 0 | D | None |
| Federal Financial Institutions Examination Council (FFIEC) | Regulatory commission or board | 0 | D | None |
| John F. Kennedy Center for the Performing Arts (KENNEDY CENTER) | Foundation, endowment or trust fund | 0 | D | None |
| National Council on Disability (NCD) | Regulatory commission or board | 0 | D | None |
| Office of Navajo and Hopi Indian Relocation (ONHIR) | Independent agency | 0 | D | None |
| Southwest Border Regional Commission (SBRC) | Regional commission | 0 | D | None |
| U.S. Interagency Council on Homelessness (USICH) | Regulatory commission or board | 0 | D | None |
| Vietnam Education Foundation (VEF) | Foundation, endowment or trust fund | 0 | D | None |
| Fannie Mae, Freddie Mac and the Federal Home Loan Banks (GSE) | Out of scope | not listed | X | None |
| Farm Credit System banks (FCS) | Out of scope | not listed | X | None |
| Federal Reserve System (FRS) | Out of scope | not listed | X | None |

## Sources

- [USAspending agency list API (FY2026 Q4)](https://api.usaspending.gov/api/v2/references/toptier_agencies/), pulled 2026-11-03
- [31 U.S.C. 9101: government corporation definitions](https://www.law.cornell.edu/uscode/text/31/9101)
- [USAGov A-Z index of federal agencies](https://www.usa.gov/agency-index)
- [PaymentAccuracy.gov agencies and programs (FY2025)](https://paymentaccuracy.gov/agencies-and-programs)
- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [Federal Audit Clearinghouse](https://www.fac.gov/)
- [Top 33 ranking](../agencies/top33.md), [review plan](../review_plan.md), [roadmap](../roadmap.md)
- [Forensic methods handbook](../playbook/forensic_methods.md)
