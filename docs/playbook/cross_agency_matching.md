# Cross-agency data matching: one identity across many programs

**Status:** Draft v0.1 (2026-11-04), for Steve's review. Extension 1 of 10
(see the [extensions overview](../extensions.md)). Reference code:
`analytics/forensic/crossmatch.py`, tested on synthetic data only.

## Bottom line

Most large frauds are invisible inside one program and obvious across
several: the same person drawing unemployment insurance in two states and
a PPP loan that claims them as a full-time employee; a hospice owner who
was debarred by GSA and is still billing Medicare; a dead veteran's
identity cashing SNAP benefits. No agency can see this alone, because each
holds one slice of the identity. This extension builds the shared method:
link people and businesses across program files with privacy-preserving
keys, then run four checks that only a linked view allows.

1. **Stacking and exclusive programs:** one identity in more programs than
   its profile explains, or in two programs that the law says cannot both
   pay for the same thing at the same time.
2. **Paid after death:** a death recorded in any one program reaches every
   program the identity is paid by.
3. **Paid while excluded:** SAM exclusions, the HHS-OIG LEIE and OPM
   debarments applied to every payment stream, not only the one that issued
   the exclusion.
4. **One identifier, many identities:** one bank account, phone, email or
   device used by people or firms that otherwise do not link (roadmap idea
   X-2).

Phase 1 runs the business side on public data (SAM.gov, USAspending, SBA
loan-level files, CMS enrollment files, exclusion lists). Phase 2 adds
person-level data through Do Not Pay and computer matching agreements (see
the [policy and legal track](../policy/legal_track.md)).

## 1. Why cross-agency matching is the highest-value extension

- The roadmap's six cross-agency ideas (X-1 to X-6) all depend on it.
- GAO and the Pandemic Response Accountability Committee found the same
  identities across PPP, EIDL and unemployment insurance; the pandemic
  analytics center that matched them closed when its authority lapsed.
- Treasury's Do Not Pay already matches payments against death and
  exclusion lists, but only for agencies that send it files, and only on
  the identifiers they send. Matching on linked identities catches the
  variants that exact matching misses.

## 2. Data sources

| Source | Entities | Keys | Phase |
| --- | --- | --- | --- |
| SAM.gov entity registrations and exclusions | Businesses, individuals excluded | UEI, CAGE, name, address | 1 (public) |
| USAspending and FPDS | Contract, grant and loan recipients | UEI, name, address | 1 |
| SBA PPP and EIDL loan-level files | Borrowers | Name, address, lender, NAICS | 1 |
| CMS PECOS, NPPES, provider enrollment files | Providers and owners | NPI, name, address, owners | 1 |
| HHS-OIG LEIE, OPM debarments, state Medicaid exclusions | Excluded people and firms | NPI, name, DOB (LEIE), address | 1 |
| Treasury payment files (through Do Not Pay) | Payees | TIN, bank routing and account | 2 |
| SSA death data (full file through Do Not Pay) | People | SSN, name, DOB | 2 |
| State UI, SNAP and Medicaid eligibility files | Claimants | SSN, name, DOB, address, bank, device | 2 (state agreements) |
| NASWA Integrity Data Hub results | UI claims | Cross-state flags | 2 |

## 3. Method

**Normalize** every name and address the same way: legal suffixes and
punctuation removed, USPS standardization (CASS-certified in production),
phones to E.164, emails lowercased with plus-tags removed.

**Hash identifiers inside each owner's boundary.** TINs, SSNs and bank
accounts never leave the agency that holds them. Each data owner computes
a keyed hash (HMAC-SHA256) of the normalized value with a key held by the
matching authority, and only hashes are exchanged. Two equal hashes mean
two records share an identifier without revealing it. Keys rotate per
matching agreement.

**Block, then compare.** Candidate pairs are records that share a hashed
TIN, bank account, phone or email, or a first name token and ZIP. Blocks
larger than 200 records (registered agents, call centers) are dropped, as
hubs are in the network method. Each pair is scored with the
Fellegi-Sunter weights already in the [forensic methods
handbook](forensic_methods.md) section 7.

**Link and review.** Pairs above the upper threshold link automatically;
pairs between the thresholds go to clerical review. Thresholds are set on
500 hand-labeled pairs to reach 95% precision, as the methodology requires.

**Run the checks** in section 4 on every linked identity.

## 4. The four checks

| Check | Rule | Grace and exceptions | Typical cause |
| --- | --- | --- | --- |
| Stacking | Identity in more than three programs, or in a pair listed as exclusive | Written per pair from program law (for example UI and full-time payroll in the same weeks; two state SNAP cases in the same month) | Identity theft, eligibility fraud |
| Paid after death | Any payment dated more than the grace period after the earliest death date on any linked record | Month-of-death payments; claims for services before death | Identity theft, family members keeping benefits |
| Paid while excluded | Payment dated after an exclusion start in any list | Services before exclusion; reinstatements | Excluded providers working through new entities |
| Shared identifier | One bank account, phone, email or device used by three or more identities that did not link | Payroll processors, tax preparers, shelters, care homes (benign-hub list) | Mule accounts, synthetic identities, ghost employees |

A flag is a reason to look, never a finding. Each one carries the linked
records and the reason, and goes to the owning program or OIG under the
lead package format in the review plan.

## 5. Privacy and safeguards

- **Legal basis first.** Person-level matching across agencies is a
  computer matching program under the Privacy Act unless an exception
  applies (OIG investigations, Do Not Pay under the Payment Integrity
  Information Act). See the [policy and legal track](../policy/legal_track.md).
- **Minimum necessary.** Only the fields in section 3 cross a boundary, and
  only as hashes where they are identifiers.
- **Due process.** No payment is stopped on a match alone; the Privacy Act
  requires independent verification and notice before adverse action.
- **Error budget.** Each check reports its false-positive rate from the
  clerical review sample, and checks above 20% false positives are not
  released.
- **Bias review.** Match rates by state and by name origin are compared,
  since name-based matching is less accurate for some naming conventions.

## 6. Phase 1 deliverable (public data, weeks 5 to 9)

A business-side linked file across SAM.gov, USAspending, SBA loan files and
CMS enrollment, with three outputs:

1. Excluded parties (SAM, LEIE) linked to entities still receiving awards or
   loans after the exclusion date.
2. Entities in four or more programs with growth and address signals.
3. Bank-free "shared identifier" clusters using phone, email and address
   from public registrations.

## 7. Phase 2 deliverable

A Do Not Pay use case for one cross-program check (paid after death across
FEHB, VA and SNAP, roadmap X-1), and one state pair for UI and SNAP
identity reuse (roadmap X-3), under the [pilot kit](../proposals/pilot_kit.md).

## 8. Questions for Steve

1. Does the SBA work with Rosemary already hold linked identities we can
   reuse as the seed and labeled set?
2. Lead the Phase 2 ask with Treasury Do Not Pay (faster, narrower) or with
   one OIG (broader, slower)?
