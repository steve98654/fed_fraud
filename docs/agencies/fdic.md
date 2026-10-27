# FDIC: one-page brief

**Priority:** 27 of 33 (score 2.3). **FY2026 outlays:** $4.6B (USAspending).
**As of:** 2026-10-27. Public data only.

## Bottom line

FDIC's spending is mostly the Deposit Insurance Fund resolving failed banks.
Its fraud exposure is insider and borrower fraud that causes or follows bank
failures, and the PPP lending that ran through banks. FDIC's public bank data
is rich; the fit with the SBA work is mainly through PPP lender behavior.

## Exposure

- $4.6B in outlays but $148B in budgetary resources in FY2026 (the fund's
  balances).
- Bank fraud and PPP-related lender misconduct are FDIC OIG case types.

## Public data we can use

- **FDIC BankFind and Call Reports:** bank financials, failures, history.
- **FDIC enforcement decisions** and OIG reports.
- **SBA PPP loan data** by lender.

## Detection plays

1. **PPP lender outliers:** banks and fintech partners with unusually high
   shares of PPP loans later flagged in the SBA work.
2. **Pre-failure signals:** banks with rapid growth in risky loan types and
   insider loans before failure.

## First prototype

A PPP lender risk table joining SBA work results with FDIC bank data.

## Limits

Loan-level bank data and examination findings are confidential.

## Who to take it to

FDIC OIG, FDIC Division of Risk Management Supervision.

## Sources

- [FDIC BankFind Suite](https://banks.data.fdic.gov/)
- [USAspending agency profiles (FY2026 outlays)](https://www.usaspending.gov/agency)
