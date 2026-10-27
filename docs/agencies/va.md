# Veterans Affairs: one-page brief

**Priority:** 8 of 33 (score 3.5). **FY2026 outlays:** $419B (USAspending).
**As of:** 2026-10-27 (first written 2026-10-25). Public data only.

## Bottom line

VA pairs naturally with DoD. Its service-disabled veteran-owned (SDVOSB)
set-aside contracts use the same SAM.gov and FPDS pipeline, and its GI Bill
school data let us screen schools. Benefit payment fraud itself (compensation,
community care) is mostly hidden from public data.

## Exposure

- VA reported $3.92B in improper and unknown payments across 7 programs in
  FY2025: $1.49B monetary loss and $1.74B unknown. Compensation alone was
  about $2.3B. (PaymentAccuracy.gov, GAO)
- SDVOSB pass-through and fake-eligibility schemes are recurring VA OIG and
  DOJ cases.

## Public data we can use

- **FPDS / USAspending** VA contracts with set-aside type.
- **SAM.gov** and **SBA VetCert** certification lists.
- **GI Bill Comparison Tool** data (school, enrollment, caution flags).
- **VA OIG reports** and DOJ releases.

## Detection plays

1. **SDVOSB fronts:** certified firms that subcontract most work, share
   officers with non-veteran firms, or appear just before large awards.
2. **School risk:** GI Bill schools with fast enrollment growth, caution
   flags, or ownership links to schools that closed or were sanctioned.
3. **Community care providers:** cross-match VA community care vendors
   against HHS-OIG's exclusion list (via the HHS pipeline).

## First prototype

Add VA to the DoD contractor screen (same code, VA awards) and a GI Bill
school watch list.

## Limits

Claims and community care payment details are not public.

## Who to take it to

VA's Office of Small and Disadvantaged Business Utilization, Veterans
Benefits Administration (Education Service), and VA OIG.

## Related briefs

[dod.md](dod.md) (shared contractor pipeline), [opm.md](opm.md) (benefit payees and death data).

## Sources

- [PaymentAccuracy.gov: VA](https://paymentaccuracy.gov/agency/VA)
- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
