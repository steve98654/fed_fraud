# Partner agencies: landscape and prioritization

**As of:** 2026-10-25. Public data only. Scores are our judgment from the
sources listed at the end; they are a starting point for discussion, not a
measured result.

## Bottom line

Start with **HHS (Medicare and Medicaid providers)**, then **DoD contracting**
and **USDA nutrition programs**. Keep **SBA** running as the baseline that
proves the method. HHS has the most money at risk (about $90B in FY2025
improper payments across Medicare and Medicaid) and the richest public
provider-level data, and its hospice and home health fraud is the stated
priority of the new whistleblower program. DoD contracting is the closest
match to the SBA work: the same SAM.gov, FPDS and set-aside data, applied to
the largest contract budget in government. USDA's SNAP retailer and child
meal programs bring the day care and food fraud patterns the program also
names.

## Which agencies are in scope

america.gov/fraud is the intake form for DOJ's Whistleblower Incentive
Program (WHIP), launched 2026-10-20 with $25M from Treasury and awards of
$10K to $30K when charges are filed. DOJ's terms page says tips must concern
federal health care offenses or fraud on programs run by these **eight
agencies**:

| Agency | Example program named by DOJ | Brief |
| --- | --- | --- |
| Health and Human Services (incl. CMS) | Health care benefit programs | [hhs.md](hhs.md) |
| War (Defense) | — | [dod.md](dod.md) |
| Small Business Administration | — | [sba.md](sba.md) |
| Agriculture | SNAP | [usda.md](usda.md) |
| Veterans Affairs | — | [va.md](va.md) |
| Housing and Urban Development | — | [hud.md](hud.md) |
| Education | Student aid fraud | [ed.md](ed.md) |
| Labor | Unemployment fraud | [dol.md](dol.md) |

DOJ (which pays the awards) and Treasury (which funds them) run the program
rather than being program agencies, so they are partners for referrals, not
targets. The site itself blocks automated reading, so this list comes from
DOJ's terms page, which the site links to. It should still be checked against
the live site. The wider task force and DOJ's National Fraud Detection Center
also name Treasury (EITC), SSA, DHS, Interior and OMB; see "Wave 2" below.

## How we scored

Each agency gets 1 to 5 on four factors, weighted toward what we can do with
public data alone.

| Factor | Weight | What 5 means |
| --- | --- | --- |
| Exposure | 30% | Tens of billions a year in improper payments or fraud-prone spend |
| Public data | 30% | Record-level data that names payees (providers, contractors, retailers) |
| SBA method fit | 20% | The SBA patterns (shell entities, shared identifiers, stacked awards, ineligible recipients) apply directly |
| Actionability | 20% | A WHIP priority area, active enforcement, and a clear owner to take findings to |

## Ranking

| Rank | Agency | Exposure | Public data | SBA fit | Action | Score | First prototype |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | HHS (CMS) | 5 | 5 | 4 | 5 | **4.8** | Hospice and home health provider risk map |
| 2 | DoD | 4 | 5 | 5 | 3 | **4.3** | Small business set-aside contractor integrity screen |
| — | SBA (baseline) | 3 | 5 | 5 | 4 | **4.2** | Extend current work to 7(a), 504 and 8(a) |
| 3 | USDA | 4 | 3 | 4 | 5 | **3.9** | SNAP retailer and child meal sponsor anomalies |
| 4 | VA | 3 | 4 | 4 | 3 | **3.5** | SDVOSB contract and GI Bill school screen |
| 5 | HUD | 3 | 3 | 3 | 3 | **3.0** | Multifamily owner network and disaster grant screen |
| 6 | Education | 2 | 3 | 3 | 3 | **2.7** | Ghost student risk by college |
| 7 | Labor | 3 | 1 | 2 | 4 | **2.4** | State UI anomaly dashboard from aggregates |

Score = 0.3 × Exposure + 0.3 × Public data + 0.2 × SBA fit + 0.2 × Action.

## Recommended sequence

1. **Now: HHS and DoD.** HHS gives the biggest dollar story; DoD gives the
   fastest technical win because it reuses the SBA contractor pipeline as is.
2. **Next: USDA and VA.** USDA adds retailer and sponsor fraud; VA shares the
   contractor pipeline with DoD and adds veteran-owned set-asides.
3. **Later: HUD, Education, Labor.** Their public data is aggregate or thin.
   They are better approached once an agency pilot grants non-public data.

## Shared building blocks

Every brief reuses the same core, which is what makes a government-wide
program realistic:

- **Entity spine:** SAM.gov entity records (UEI, address, owners, exclusions)
  joined to USAspending awards and FPDS contracts.
- **Exclusion and enforcement lists:** SAM.gov exclusions, HHS-OIG LEIE, DOJ
  press releases and OIG reports, used both as labels to train on and as
  watch lists.
- **Common patterns:** many payees at one address, new entities winning large
  awards fast, shared officers across "competing" firms, payees tied to
  excluded parties, and spending far above peers.

## Wave 2 candidates (outside the eight)

| Agency | Why it matters | Public data |
| --- | --- | --- |
| Treasury / IRS | EITC improper payments $21.1B (32.7%) in FY2025 | Aggregate only; preparer-level data not public |
| SSA | SSI improper payments $7.3B (11.6%) in FY2025 | Aggregate only |
| DHS / FEMA | Disaster assistance fraud | OpenFEMA has program-level and some recipient data |

## Sources

- [DOJ Whistleblower Rewards Program terms (lists the eight agencies)](https://www.justice.gov/fraud/whistleblower)
- [Latin Times: inside DOJ's WHIP program (launch date, award range, $25M)](https://www.latintimes.com/how-turn-fraudster-get-paid-immediately-inside-dojs-groundbreaking-whip-program-600382)
- [Runtime Wire: America.gov AI-assisted tip form](https://runtimewire.com/article/america-gov-fraud-whistleblower-ai-intake)
- [GAO-26-108694: improper payments rose to $186B in FY2025](https://www.gao.gov/products/gao-26-108694)
- [CRFB: FY2025 improper payments by program](https://www.crfb.org/blogs/federal-improper-payments-total-186-billion-fy-2025)
- [GAO-24-105833: federal fraud losses estimated at $233B to $521B a year](https://www.gao.gov/products/GAO-24-105833)
- [Working plan for this project](../plan.md)
