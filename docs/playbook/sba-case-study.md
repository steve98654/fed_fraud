# SBA case study: the method in practice

**Status:** Draft v0.1 (2026-11-01). The method sections describe the SBA
work as recorded in this repo. The results section waits on figures from
the SBA team (Rosemary) and stays *Pending* until they are supplied and
checked.

## Bottom line

The SBA work with Rosemary is the proof that this approach works on real
federal money. It took public loan-level data from SBA's pandemic programs,
joined it to entity records and found borrowers that share identifiers and
addresses in ways honest borrowers rarely do. Every other agency plan on
this site reuses that pipeline. The ask of a partner agency is to let us
run the same method on its programs, starting with public data and moving
to internal data through its Inspector General.

## Why SBA came first

- Pandemic lending moved hundreds of billions of dollars quickly, with
  light checks at application. GAO's FY2025 estimates still show the
  highest improper payment rates in government: Shuttered Venue Operators
  Grant $10.1B (68.9%), PPP loan forgiveness 19.2%, PPP guaranty purchases
  13.3%.
- SBA released loan-level PPP and EIDL data, so the fraud could be studied
  record by record without access agreements.
- PPP and EIDL fraud carries a ten-year limitation period (2022 law), so
  leads found now remain prosecutable to 2030-2032.

## What the work does

**Data.** PPP and EIDL loan-level releases, SAM.gov and FPDS records, SBA
certification lists (8(a), HUBZone, WOSB, VetCert), SBA OIG reports and DOJ
press releases.

**Schemes it targets.**

- Identity theft and synthetic borrowers.
- Shell entities created to borrow.
- Stacked awards: one person or address behind many loans.
- Ineligible recipients.

**How it finds them.**

1. **Entity resolution.** Names, addresses (USPS-standardized) and phone
   numbers are normalized and matched so that "different" borrowers that
   are really one person or one address are grouped together.
2. **Shared identifiers.** Groups with many loans at one address or behind
   one contact are scored, together with signals such as new businesses
   with large loans.
3. **Leads, not accusations.** Results are ranked leads with stated
   reasons, for the office that can act on them.

How the SBA results were validated, and what the receiving offices did
with them, will be written up with the SBA team in the playbook (item F1).

## Results

These measures will be filled in from the SBA team's records and checked
before they appear anywhere else on this site. No figure is estimated.

| Measure | Value |
| --- | --- |
| Loans and borrowers screened | Pending |
| Groups and borrowers flagged | Pending |
| Known cases in the top 5% of scores (back-test) | Pending |
| Leads referred, and to whom | Pending |
| Leads accepted, charged or recovered | Pending |
| Dollars identified, referred and confirmed | Pending |

## Why it carries over

Almost every fraud scheme in the 33 agency briefs is a version of what the
SBA screens already detect. The signals change their inputs, not their
logic.

| SBA signal | Same signal elsewhere | Roadmap ideas |
| --- | --- | --- |
| Many borrowers at one address | Many providers, stores or vendors at one address | HHS-1, USDA-1, GSA-1 |
| Shared contact or officer across borrowers | Shared control among bidders or DBEs and their primes | DOD-2, DOT-1 |
| New business, large loan | New contractor, large set-aside award; new importer after a tariff change | DOD-1, DHS-1 |
| Borrower tied to a charged case | Owner tied to an excluded or revoked provider | HHS-2, GSA-2 |
| Lender or agent behind many bad loans | Consultant behind many single-bid E-Rate awards; sponsor behind many outlier sites | FCC-1, USDA-2 |

What is SBA-only: the loan program rules, the lender relationships and the
pandemic-era data releases. Those parts are kept in the SBA prototype; the
rest moves into the shared pipeline described in the
[methodology](methodology.md).

## What comes next at SBA

- **SBA-1 (weeks 3-6):** run the same screens on 7(a) and 504 loans and on
  8(a), HUBZone, WOSB and VetCert firms.
- **SBA-2:** lender and agent concentration, shared with FDIC.
- **SBA-3:** pandemic fraud owners now holding new loans or certifications.
- **Playbook (week 2, item F1):** the full SBA baseline written down in
  `docs/playbook/sba-baseline.md` and reviewed by Rosemary.

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [CRFB: FY2025 improper payments by program](https://www.crfb.org/blogs/federal-improper-payments-total-186-billion-fy-2025)
- [SBA brief](../agencies/sba.md) and [review plan](../review_plan.md)
