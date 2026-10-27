# Top 33 agencies by budget: landscape and prioritization

**As of:** 2026-10-27. Public data only. Scores are our judgment from the
sources in each brief; they are a starting point for discussion, not a
measured result. This extends [landscape.md](landscape.md), which covers the
eight agencies in DOJ's whistleblower program, to the 33 largest agencies.

## Bottom line

Budget size and fraud opportunity are not the same list. Treasury and SSA
are the 2nd and 3rd largest agencies but rank 8th and 22nd here, because
taxpayer and beneficiary data are not public. The top of the list is where
large fraud-prone spending meets record-level public data: **HHS, DoD and
SBA** as before, then **USDA and DHS**, then **DOT and GSA**.

Three new agencies stand out:

- **DHS (customs and FEMA)** is the biggest new opportunity. Tariff evasion
  through shell importers and false country of origin is a top DOJ priority
  (Trade Fraud Task Force, August 2025) and looks like SBA shell-entity
  fraud.
- **DOT** is the fastest technical win: Disadvantaged Business Enterprise
  fronts are the same pattern as SBA 8(a) fronts, and states publish DBE
  directories and bid tabs.
- **GSA** owns SAM.gov and FPDS, the data spine for every brief. A GSA
  partnership improves the data for all 33.

Below the top 15, most agencies are either small spenders or have little
public payee data. Their best use is to join shared screens (contractors,
research awards, grantees) rather than to get their own projects.

## Which agencies, and how we measured budget

- **Source:** USAspending.gov agency list
  (`/api/v2/references/toptier_agencies/`), pulled 2026-10-27.
- **Fiscal year:** FY2026, all four quarters (October 2025 to September
  2026), as reported by agencies to USAspending. Figures may be revised.
- **Measure:** we ranked by **outlays** (money actually paid out). We also
  record **total budgetary resources**, which USAspending labels
  `budget_authority_amount`; it includes balances carried over from prior
  years, so it overstates insurance funds (FDIC, PBGC) and multi-year
  programs. Ranking by budgetary resources would swap in the Farm Credit
  System Insurance Corporation, Millennium Challenge Corporation and CFTC for
  FCC, PCORTF and NRC; the top 25 are nearly the same either way.
- **What is counted as an agency:** USAspending's "toptier agency" list, as
  is. That list includes one trust fund (PCORTF) and omits off-budget or
  non-reporting bodies such as the Postal Service, Tennessee Valley
  Authority and Railroad Retirement Board (about $5.1B net in FY2026 per
  Treasury's Monthly Treasury Statement), and the legislative and judicial
  branches.
- **Cross-check:** Treasury's Monthly Treasury Statement (Table 5,
  2026-09-30) gives the same top tier. Totals differ (for example DoD $917B
  net in MTS versus $1,345B in USAspending, which also counts military trust
  funds), but the ranking is stable.
- Raw figures: [data/top33_fy2026.csv](data/top33_fy2026.csv).

## How we scored

Same method as [landscape.md](landscape.md): each agency gets 1 to 5 on four
factors, weighted toward what we can do with public data alone.

| Factor | Weight | What 5 means |
| --- | --- | --- |
| Exposure | 30% | Tens of billions a year in improper payments or fraud-prone spend |
| Public data | 30% | Record-level data that names payees (providers, contractors, retailers) |
| SBA method fit | 20% | The SBA patterns (shell entities, shared identifiers, stacked awards, ineligible recipients) apply directly |
| Actionability | 20% | Active enforcement priority and a clear owner to take findings to |

Score = 0.3 × Exposure + 0.3 × Public data + 0.2 × SBA fit + 0.2 × Action.
Scores for the original eight are unchanged from
[landscape.md](landscape.md).

## Ranking

"Budget rank" is the agency's place by FY2026 outlays; outlays are in
billions of dollars.

| Rank | Agency | Budget rank | Outlays ($B) | Exposure | Public data | SBA fit | Action | Score | First prototype |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | [Health and Human Services](hhs.md) | 1 | 2,687 | 5 | 5 | 4 | 5 | **4.8** | Hospice and home health provider risk map |
| 2 | [Defense (War)](dod.md) | 4 | 1,345 | 4 | 5 | 5 | 3 | **4.3** | Set-aside contractor integrity screen |
| 3 | [Small Business Administration (baseline)](sba.md) | 22 | 15 | 3 | 5 | 5 | 4 | **4.2** | Extend current work to 7(a), 504 and 8(a) |
| 4 | [Agriculture](usda.md) | 7 | 220 | 4 | 3 | 4 | 5 | **3.9** | SNAP retailer and child meal sponsor anomalies |
| 4 | [Homeland Security (CBP, FEMA)](dhs.md) | 6 | 259 | 4 | 3 | 4 | 5 | **3.9** | Tariff-evasion importer lead list |
| 6 | [Transportation](dot.md) | 10 | 125 | 3 | 4 | 5 | 3 | **3.7** | DBE front and bid rotation screen |
| 6 | [General Services Administration](gsa.md) | 16 | 38 | 2 | 5 | 5 | 3 | **3.7** | SAM.gov registration integrity report |
| 8 | [Treasury (IRS)](treasury.md) | 2 | 1,975 | 5 | 2 | 3 | 4 | **3.5** | EITC hot-spot map by ZIP |
| 8 | [Veterans Affairs](va.md) | 5 | 419 | 3 | 4 | 4 | 3 | **3.5** | SDVOSB contract and GI Bill school screen |
| 8 | [Federal Communications Commission (USF)](fcc.md) | 25 | 10 | 3 | 4 | 4 | 3 | **3.5** | E-Rate provider and consultant network map |
| 11 | [Office of Personnel Management](opm.md) | 8 | 201 | 4 | 3 | 3 | 3 | **3.3** | FEHB exclusion-list reconciliation |
| 11 | [Energy](doe.md) | 13 | 63 | 3 | 4 | 4 | 2 | **3.3** | Cross-agency SBIR duplicate-award screen |
| 11 | [Commerce](doc.md) | 20 | 20 | 3 | 4 | 4 | 2 | **3.3** | BEAD subgrantee screen |
| 14 | [Army Corps of Engineers](usace.md) | 18 | 28 | 2 | 4 | 4 | 3 | **3.2** | DoD contractor screen on Corps awards |
| 15 | [Environmental Protection Agency](epa.md) | 21 | 17 | 3 | 4 | 3 | 2 | **3.1** | Grantee profile for large IRA programs |
| 16 | [Housing and Urban Development](hud.md) | 11 | 85 | 3 | 3 | 3 | 3 | **3.0** | Multifamily owner network and disaster grant screen |
| 16 | [State (incl. foreign assistance)](state.md) | 15 | 39 | 3 | 3 | 3 | 3 | **3.0** | Implementing-partner risk profile |
| 16 | [NASA](nasa.md) | 19 | 23 | 2 | 4 | 4 | 2 | **3.0** | Join the SBIR duplicate-award screen |
| 16 | [National Science Foundation](nsf.md) | 26 | 8.1 | 2 | 4 | 4 | 2 | **3.0** | Test bed for the SBIR duplicate-award screen |
| 20 | [Justice](doj.md) | 14 | 52 | 2 | 3 | 3 | 4 | **2.9** | Press-release case database (labels for all) |
| 21 | [Securities and Exchange Commission](sec.md) | 28 | 1.8 | 1 | 5 | 3 | 2 | **2.8** | EDGAR enrichment for the entity spine |
| 22 | [Education](ed.md) | 9 | 135 | 2 | 3 | 3 | 3 | **2.7** | Ghost student risk by college |
| 22 | [Social Security Administration](ssa.md) | 3 | 1,664 | 4 | 1 | 2 | 4 | **2.7** | County SSI outlier map and death-data case |
| 24 | [USAID (winding down)](usaid.md) | 23 | 12 | 2 | 3 | 3 | 2 | **2.5** | Close-out balance and partner table |
| 24 | [Pension Benefit Guaranty Corporation](pbgc.md) | 24 | 11 | 3 | 2 | 2 | 3 | **2.5** | SFA application vs. Form 5500 check |
| 26 | [Labor](dol.md) | 12 | 63 | 3 | 1 | 2 | 4 | **2.4** | State UI anomaly dashboard |
| 27 | [Interior](doi.md) | 17 | 37 | 2 | 3 | 2 | 2 | **2.3** | Royalty-rate outlier table |
| 27 | [FDIC](fdic.md) | 27 | 4.6 | 2 | 3 | 2 | 2 | **2.3** | PPP lender risk table |
| 29 | [Development Finance Corporation](dfc.md) | 29 | 1.6 | 2 | 3 | 2 | 1 | **2.1** | Sponsor sanctions and exclusions check |
| 30 | [AmeriCorps](cncs.md) | 30 | 1.2 | 1 | 3 | 2 | 2 | **2.0** | Foster Grandparent grantee risk list |
| 31 | [PCOR Trust Fund](pcortf.md) | 31 | 1.1 | 1 | 3 | 2 | 1 | **1.8** | Join the research award screen |
| 31 | [Nuclear Regulatory Commission](nrc.md) | 32 | 0.9 | 1 | 3 | 2 | 1 | **1.8** | None; include in contractor screen |
| 33 | [Executive Office of the President](eop.md) | 33 | 0.9 | 1 | 2 | 1 | 1 | **1.3** | None; audience for the proposal |

## Recommended sequence

1. **Now (unchanged): HHS and DoD,** with SBA as the baseline.
2. **Next: DHS customs, USDA, DOT.** DHS and USDA have the strongest
   enforcement pull; DOT reuses the SBA front-company code with new state
   data.
3. **Data partners in parallel: GSA, DOJ, SEC, SSA.** Each makes the shared
   pipeline better: GSA for SAM.gov and FPDS, DOJ for labeled cases, SEC for
   ownership, SSA for death data.
4. **Contained pilots: FCC (E-Rate) and OPM (FEHB exclusions).** Small,
   data-rich, and quick to show results.
5. **Shared screens instead of separate projects** for the rest: one
   contractor screen (DoD, USACE, NASA, NRC, State), one research award
   screen (DOE, NSF, NASA, PCORTF), one grantee screen (EPA, DOJ, AmeriCorps,
   Commerce).
6. **Proposal first, data later: Treasury, SSA, Labor, PBGC.** Big money,
   but the payee data is confidential, so lead with a data-access proposal.

## Shared screens

Grouping agencies by the screen they need keeps the build to a handful of
reusable tools.

| Screen | Core data | Agencies |
| --- | --- | --- |
| Provider integrity | CMS files, NPPES, LEIE, ownership | HHS, OPM, VA |
| Contractor integrity | SAM.gov, FPDS, SBA certifications | DoD, VA, GSA, USACE, DHS, NASA, DOE, State, NRC, SBA |
| Small business fronts | SBA and state DBE directories, subawards | SBA, DoD, DOT, VA |
| Research awards | SBIR.gov, NSF, NIH RePORTER, PCORI | DOE, NSF, NASA, PCORTF, DoD |
| Grantees and nonprofits | USAspending subawards, Form 990 | EPA, DOJ, AmeriCorps, HUD, Commerce, State, USAID |
| Retailers and sponsors | SNAP retailer data, meal sponsors | USDA |
| Customs and trade | Manifests, Census trade data | DHS |
| Telecom subsidies | USAC open data, FCC broadband map | FCC, Commerce |
| Benefits (aggregate only) | SOI ZIP data, state and county stats | Treasury, SSA, Labor, PBGC |

## Sources

- [USAspending agency list API (FY2026 Q4)](https://api.usaspending.gov/api/v2/references/toptier_agencies/?sort=outlay_amount&order=desc)
- [Treasury Monthly Treasury Statement data (Table 5)](https://fiscaldata.treasury.gov/datasets/monthly-treasury-statement/)
- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [GAO-24-105470: SBIR/STTR fraud vulnerabilities](https://www.gao.gov/products/GAO-24-105470)
- [Partner agencies landscape (the original eight)](landscape.md)
- Each agency brief lists its own sources.
