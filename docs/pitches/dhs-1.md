# DHS-1: Tariff-evasion importer lead list

**For:** CBP Office of Trade, HSI, DOJ-DHS Trade Fraud Task Force.
**Weeks:** 6-10 (results by 2027-01-22). **Brief:** [DHS](../agencies/dhs.md).

## The problem

When duties rise, some importers ship through a third country, declare a
false origin or undervalue goods, often through shell importers of record
that disappear when penalized. DOJ now treats this as a priority: the Trade
Fraud Task Force announced three resolutions totaling over $100M on
2025-12-18. Trade statistics show where the gaps are; entity data shows who
is behind them.

## Data

- Census USA Trade Online imports by HTS-10 code and country.
- UN Comtrade partner exports, for mirror checks.
- ITA antidumping and countervailing duty orders; Section 301 and 232
  tariff lists; CBP EAPA determinations.
- Vessel manifests from a licensed vendor (if bought under decision F12).

## Detection method

1. **Mirror gap:** product and country pairs where U.S. imports exceed the
   partner's reported exports, after a tariff change. Two product groups
   first (for example aluminum extrusions and plastic resin).
2. **Origin shift:** shippers whose declared origin moves to a third
   country right after a duty change.
3. **Shell importers:** new importers of record after a tariff change, at
   residential or registered-agent addresses, or sharing officers with
   penalized firms.

## Validation

Back-test on Trade Fraud Task Force resolutions, customs False Claims Act
settlements 2020-2026 and EAPA determinations.

## Exposure (public figures, not savings)

- Over $100M in three Task Force resolutions (2025-12-18), including
  Ceratizit at $54.4M for Chinese goods declared as Taiwanese.
- CBP reports 1,200 investigations from revenue allegations.
- Savings from this work: **Pending.**

## What we ask for

- **Now:** a contact in CBP Office of Trade or HSI; the product groups CBP
  most wants covered; EAPA case outcomes for validation.
- **Phase 2:** entry-level ACE data (declared value, origin, duty paid) to
  measure underpayment importer by importer.

## What you get, and when

By week 10: an importer lead list with reasons for two product groups, a
mirror-gap table that can be rerun for any product, and a review memo.

## Limits

Mirror gaps have innocent causes (timing, classification, re-exports).
Without manifests, importer names come from case records and public
filings, so coverage is partial.

## Sources

- [Akin Gump: DOJ year-end customs fraud enforcement (Jan 2026)](https://www.akingump.com/en/insights/alerts/dojs-yearend-customs-fraud-enforcement-signals-whats-ahead-in-2026)
- [Morgan Lewis: DOJ establishes Trade Fraud Task Force (Sept 2025)](https://morganlewis.com/pubs/2025/09/us-department-of-justice-establishes-trade-fraud-task-force-to-counter-tariff-evasion)
- [19 CFR 103.31: public vessel manifest information](https://www.law.cornell.edu/cfr/text/19/103.31)
