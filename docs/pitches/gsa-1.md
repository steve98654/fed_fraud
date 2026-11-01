# GSA-1: SAM.gov registration integrity report

**For:** GSA Integrated Award Environment (SAM.gov), GSA OIG.
**Weeks:** 7-10 (results by 2027-01-22). **Brief:** [GSA](../agencies/gsa.md).

## The problem

Every federal contractor and grantee registers in SAM.gov. Shell networks
register many entities at one address or under one set of officers, and
excluded firms come back under a new Unique Entity ID. Because every agency
relies on SAM.gov, fixing it once protects all of them. This is the SBA
entity screen at government-wide scale.

## Data

- SAM.gov public entity extract with history, and exclusions (already in
  the shared entity spine).
- USAspending prime and subaward awards FY2020-FY2026, to rank clusters by
  dollars.

## Detection method

1. **Clusters:** registrations sharing addresses, points of contact or
   officers, ranked by award dollars.
2. **Re-registration:** new UEIs that share officers, addresses or phones
   with excluded entities (GSA-2).
3. **Thin entities:** recently registered entities with large awards and no
   other footprint.

## Validation

Excluded entities that later re-registered, found from the exclusion
history, are the labels.

## Exposure (public figures, not savings)

- SAM.gov sits in front of all federal awards; the dollars that flow to
  flagged clusters will be measured from USAspending in week 7.
- Savings from this work: **Pending.**

## What we ask for

- **Now:** a contact in GSA IAE; guidance on which data-quality issues are
  already known.
- **Phase 2:** SAM.gov sensitive fields (TINs and bank data) to detect
  shells by shared tax ID and account.

## What you get, and when

By week 10: a registration integrity report offered to GSA as a data
quality product, with ranked clusters and the re-registration list
referred to GSA OIG.

## Limits

Public SAM.gov data omit TINs and bank accounts. Many shared addresses
are registered agents or shared offices and are filtered before ranking.

## Sources

- [SAM.gov data services](https://sam.gov/data-services)
