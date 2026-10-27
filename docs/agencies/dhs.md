# Homeland Security (CBP and FEMA): one-page brief

**Priority:** 4 of 33 (score 3.9). **FY2026 outlays:** $259B (USAspending).
**As of:** 2026-10-27. Public data only.

## Bottom line

DHS is the biggest new opportunity outside the original eight, for two
reasons. First, customs duty evasion has become a top DOJ priority: a joint
DOJ and DHS Trade Fraud Task Force started in August 2025, and the largest
customs False Claims Act settlement to date ($54.4M) came in December 2025.
Evasion through shell importers and false country of origin is a close
cousin of SBA shell-entity fraud. Second, FEMA disaster aid has a long fraud
history and publishes recipient-level data through OpenFEMA.

## Exposure

- Customs: DOJ announced three Task Force resolutions totaling over $100M on
  2025-12-18, including Ceratizit ($54.4M, Chinese goods declared as
  Taiwanese). CBP reports 1,200 investigations from revenue allegations.
- FEMA: Public Assistance reported $0.3B improper in FY2025 (GAO); disaster
  grant and contractor fraud recur after every major storm.
- DHS's own contracts (CBP, ICE, FEMA) run through FPDS like DoD's.

## Public data we can use

- **Vessel manifest data:** public by regulation (19 CFR 103.31) and resold
  by commercial vendors; names importers, shippers and goods.
- **Census trade statistics:** imports by product and country, for mirror
  checks against partner-country exports.
- **CBP EAPA and penalty notices**, DOJ customs settlements.
- **OpenFEMA:** Public Assistance projects, Hazard Mitigation awards, and
  housing assistance aggregates.
- **FPDS / USAspending and SAM.gov** for DHS contractors.

## Detection plays

1. **Transshipment signals:** product lines where US imports from a country
   far exceed that country's recorded exports to the US, then the importers
   driving the gap.
2. **Shell importers:** new importers of record that share addresses or
   officers with firms under penalty, or that appear right after a new tariff.
3. **Disaster contractors:** new or out-of-area firms winning FEMA work fast,
   shared owners across bidders, and payees tied to excluded parties.

## First prototype

A tariff-evasion lead list for two high-duty product groups (for example
aluminum extrusions and plastic resin), built from mirror trade gaps and
manifest data, with importer risk scores and reasons. Validate against
settled cases.

## Limits

Entry-level customs data (declared value, duties paid) is not public, and
good manifest coverage needs a paid vendor. Customs fraud cuts revenue, not
spending, so it sits outside improper payment reporting.

## Who to take it to

CBP Office of Trade, HSI, the DOJ-DHS Trade Fraud Task Force, FEMA's Fraud
Investigations and Inspections Division, and DHS OIG.

## Sources

- [Akin Gump: DOJ year-end customs fraud enforcement (Jan 2026)](https://www.akingump.com/en/insights/alerts/dojs-yearend-customs-fraud-enforcement-signals-whats-ahead-in-2026)
- [Morgan Lewis: DOJ establishes Trade Fraud Task Force (Sept 2025)](https://morganlewis.com/pubs/2025/09/us-department-of-justice-establishes-trade-fraud-task-force-to-counter-tariff-evasion)
- [19 CFR 103.31: public vessel manifest information](https://www.law.cornell.edu/cfr/text/19/103.31)
- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [OpenFEMA data sets](https://www.fema.gov/about/openfema/data-sets)
