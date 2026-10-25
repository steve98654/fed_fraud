# Labor: one-page brief

**Priority:** 7 of 7 (score 2.4). **As of:** 2026-10-25. Public data only.

## Bottom line

Unemployment insurance fraud was enormous during the pandemic and is still
the highest-rate program here (14.9%), but claimant data are held by states
and are not public. With public data we can only point to states and periods
that look wrong. Labor is a strong candidate once a state or DOL grants data.

## Exposure

- Federal-State Unemployment Insurance: $5.6B improper (14.9%) in FY2025.
  (GAO)
- GAO estimated pandemic UI fraud at $100B to $135B.

## Public data we can use

- **DOL ETA state UI reports:** weekly claims, overpayments, and fraud
  recoveries by state.
- **DOL grants** on USAspending (state UI integrity grants).
- **DOL OIG reports** and DOJ releases.

## Detection plays

1. **State anomalies:** claims that diverge from local job loss, or high
   overpayment rates relative to peers.
2. **Case mining:** extract the schemes from charged cases (shared bank
   accounts, addresses, IP addresses) to build rules states can run.

## First prototype

A state-by-state UI integrity dashboard from public aggregates, plus a
playbook of rules drawn from charged cases.

## Limits

Detection at the claim level needs state data. This is a proposal-first,
data-later agency.

## Who to take it to

DOL Employment and Training Administration, DOL OIG, and state workforce
agencies.

## Sources

- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [GAO-23-106696: pandemic UI fraud of $100B to $135B](https://www.gao.gov/products/gao-23-106696)
