# Forensic methods handbook: the mathematics behind each fraud test

**Status:** Draft v0.1 (2026-11-03), for Steve's review. Companion to the
[methodology](methodology.md), which says how a lead is scored, validated
and referred; this handbook says exactly how each test is computed, when it
is valid and what it cannot show. Every formula here has a tested reference
implementation in `analytics/forensic/` (run on synthetic data only; no real
entity appears in the tests).

## Bottom line

Fraud leaves arithmetic traces: digits that people invent, amounts steered
just under a limit, invoices paid twice, bids that cluster too neatly,
providers who bill more hours than a day has, and "separate" companies that
share a phone line. This handbook turns each trace into a written test with
a formula, a threshold, a false-positive story and a validation plan. Ten
families of tests cover every fraud area in the roadmap and in the
[all-agency plan](../universe/all_agencies.md):

1. **Digit and number tests** (Benford's law, round numbers, duplication).
2. **Duplicate, split and impossible-billing tests.**
3. **Peer outliers, growth and threshold bunching**, with Bayesian
   shrinkage so small providers are not over-flagged.
4. **Collusion screens** for sealed bids.
5. **Entity resolution** (Fellegi-Sunter record linkage).
6. **Network analysis** with hub discounting and risk propagation.
7. **Eligibility and identity tests** (death, incarceration, impossible
   identities).
8. **Improper payment estimation** with confidence intervals, so we can
   check and extend agency estimates.
9. **Reconciliation and audit-trail tests** across USAspending, Treasury,
   PaymentAccuracy.gov and Single Audit data.
10. **Score combination and validation** (likelihood ratios, lift,
    false discovery control).

The rule that keeps this honest: **a test result is a reason to look, not
a finding.** Only an Inspector General or DOJ confirms fraud, and only a
confirmed dollar counts as savings.

## 1. Where each method sits

Tests work at five levels. Public data supports the first three in Phase 1;
the last two mostly need internal records reached through OIGs in Phase 2.

| Level | Unit tested | Example tests | Phase 1 public data | Phase 2 internal data |
| --- | --- | --- | --- | --- |
| Population | All awards or payments of an agency or program | Benford, round numbers, bunching, reconciliation | USAspending award and account files, PaymentAccuracy.gov, Treasury MTS | General ledger, payment files |
| Entity | One contractor, grantee, provider, retailer | Peer outliers, growth, new-entity-large-award, entity-level Benford | USAspending, SAM.gov, CMS files, SNAP retailer data | Claims, invoices |
| Network | Groups of entities | Shared attributes, components, risk propagation | SAM.gov addresses and contacts, NPPES, Form 990, state registries | Bank accounts, devices, IP addresses |
| Transaction | One payment, claim, invoice or voucher | Duplicates, splits, impossible days, after-death payments | Rarely public | Payment, claim, card and voucher files |
| Estimate | The program's improper payment rate | Stratified and ratio estimators, monetary unit sampling | Published agency estimates | Sample case files |

## 2. Ground rules for forensic testing

- **Hypothesis first.** Each test is written down with the scheme it
  targets before it is run. A test without a scheme is data dredging.
- **Pre-registration.** Thresholds, peer groups and exclusions are fixed
  in the screen's specification before results are seen, and changes are
  logged with reasons.
- **Multiple testing.** Running one test per entity across 100,000
  entities guarantees thousands of chance "hits". Entity-level p-values are
  controlled with the Benjamini-Hochberg procedure (section 12.4), not a
  fixed 0.05.
- **Practical significance.** With millions of records, a chi-square test
  rejects for trivially small deviations. Every test reports an effect size
  (MAD, ratio, excess dollars) alongside its p-value, and effect size
  decides whether anyone looks.
- **Innocent explanations first.** Each test lists its known benign causes
  and checks the main ones before a result enters a lead package.
- **Reproducibility.** Every result cites its data pull (source, date,
  hash) and the code version, so another analyst can rerun it exactly. This
  follows the GAO Yellow Book's evidence standard and the AICPA Statement on
  Standards for Forensic Services No. 1.
- **Known error rates.** Each screen's back-test (section 12.3) gives its
  measured hit rate and false-positive rate. That is what an expert needs
  to defend a method in court (the Daubert standard asks for a known or
  potential error rate).

## 3. Digit and number tests

### 3.1 Benford's law

Many naturally occurring sets of amounts (invoices, claims, award values)
follow Benford's law: the leading digit $d$ appears with probability

$$P(D_1 = d) = \log_{10}\left(1 + \frac{1}{d}\right), \quad d = 1, \dots, 9,$$

so about 30.1% of amounts start with 1 and only 4.6% start with 9. The
first-two-digits version, with $d = 10, \dots, 99$, uses the same formula
and is the sharper forensic test. The second digit has probability

$$P(D_2 = d) = \sum_{k=1}^{9} \log_{10}\left(1 + \frac{1}{10k + d}\right), \quad d = 0, \dots, 9.$$

**Why it detects fraud.** People inventing numbers spread leading digits
too evenly and favor middle digits; schemes that keep amounts under a limit
create spikes at specific first-two digits (for example 48 and 49 below a
$5,000 approval level).

**When it applies.** Benford's law holds for amounts that span several
orders of magnitude, arise from multiplying many factors, and have no
built-in floor or ceiling. It does **not** apply to assigned numbers
(invoice or account numbers), prices set on a schedule (fixed per-diem
rates, Medicare fee schedules), amounts with caps (a $10,000 grant
maximum), or small samples. A thousand or more records works best for
first-two-digit tests.

**Statistics.** With $n$ amounts, observed digit shares $\hat p_d$ and
expected shares $p_d$:

- Chi-square: $\chi^2 = n \sum_d (\hat p_d - p_d)^2 / p_d$ with 8 (first
  digit) or 89 (first two) degrees of freedom. Sensitive to $n$; use for
  small populations.
- Per-digit z with continuity correction:
  $z_d = \left(|\hat p_d - p_d| - \tfrac{1}{2n}\right) / \sqrt{p_d(1-p_d)/n}$.
  Identifies which digits spike.
- Mean absolute deviation: $\text{MAD} = \frac{1}{k}\sum_d |\hat p_d - p_d|$,
  which does not grow with $n$ and is the main conformity measure.

| Test | Close conformity | Acceptable | Marginal | Nonconformity |
| --- | --- | --- | --- | --- |
| First digit | MAD up to 0.006 | 0.006 to 0.012 | 0.012 to 0.015 | Above 0.015 |
| Second digit | Up to 0.008 | 0.008 to 0.010 | 0.010 to 0.012 | Above 0.012 |
| First two digits | Up to 0.0012 | 0.0012 to 0.0018 | 0.0018 to 0.0022 | Above 0.0022 |

Thresholds are Nigrini's (2012), derived from large real-world data sets.

**How we use it.** At the population level, nonconformity is a reason to
look at the program's controls, not at any one payee. At the entity level
(one vendor's 400 invoices, one provider's claims), each entity's MAD is
compared with its peers' distribution of MADs, and only the extreme tail
with enough records is reviewed. Benford is a **weak signal alone**; it
never counts as one of the two required signals unless combined with a
digit spike at a known threshold.

### 3.2 Companion number tests

| Test | Formula | What it catches | Benign causes |
| --- | --- | --- | --- |
| Last-two-digits | Chi-square of the last two digits against uniform (1% each) | Invented cents, or amounts all ending .00 or .99 | Whole-dollar pricing, fixed fees |
| Round numbers | Share of amounts that are exact multiples of $1,000 (or $100), tested against a clean reference share with a one-sided binomial test | Estimates billed as actuals; made-up invoices | Lump-sum milestone payments, fixed grants |
| Number duplication | Most frequent exact amounts, ranked | One odd amount (say $4,987.13) paid 60 times | Recurring contracts, subscriptions |
| Summation | Share of total dollars by first-two digits; each of the 90 groups should hold about 1/90 | A few very large amounts driving the total | One large legitimate contract |
| Relative size factor | Largest payment divided by second largest, per vendor or cardholder | One inflated or misplaced payment | Annual true-ups |

## 4. Duplicate, split and impossible-billing tests

These are transaction tests. They need payment, invoice, card or voucher
records, so most run in Phase 2, but the award-level versions run in
Phase 1 on USAspending contract actions.

### 4.1 Duplicate payments

Duplicate payments are the most common recoverable error and a common
fraud (resubmitting an invoice with a changed number). The test runs in
four tiers, strongest first:

1. **Exact:** same vendor, amount, invoice number and date.
2. **Same invoice, different date:** same vendor, amount and *normalized*
   invoice number. Normalization uppercases, strips prefixes (INV, #) and
   suffixes (-A, -R, DUP), maps look-alike characters (O to 0, I and l to 1,
   S to 5) and removes leading zeros.
3. **Near-identical invoice:** same vendor and amount, normalized invoice
   numbers within one edit (Damerau-Levenshtein distance 1, which counts a
   transposed pair of digits as one edit), paid within 90 days.
4. **Same invoice, different vendor:** same amount and invoice number paid
   to two vendor records, which points to duplicate vendor master entries
   or a diverted payment.

Expected false positives are recurring identical charges (monthly rent,
subscriptions); these are listed per vendor and excluded after review.

### 4.2 Split purchases and split awards

Rules that require more scrutiny above a dollar limit (the FAR
micro-purchase threshold for card purchases, the simplified acquisition
threshold for contracts, internal approval levels) invite splitting. The
test groups purchases by the same buyer from the same vendor within a short
window (three days for cards, 30 days for contract actions) and flags any
group where **every** item is under the limit but the **sum** is over it.

At the population level, the same idea becomes a **bunching test**
(section 5.4): an excess of amounts just under the limit.

The limits change with inflation adjustments (the October 2025 FAR
adjustment raised the micro-purchase threshold to $15,000 and the
simplified acquisition threshold to $350,000); each screen reads the limit
in force on the transaction date from FAR 2.101 rather than a fixed number.

### 4.3 Impossible days and impossible volumes

For any biller paid by time or by service (Criminal Justice Act panel
attorneys, workers' compensation providers, Medicaid personal care aides,
time-and-materials contractors), total billed hours per person per day
across all matters is

$$H_{b,t} = \sum_{m} h_{b,m,t}.$$

$H > 24$ is impossible; reviews also look at $H > 16$ on many days and at
service counts that exceed what one clinician can deliver (for example,
more 60-minute psychotherapy sessions in a day than hours in a working
day). The test is simple, explains itself to a jury, and has produced many
health care fraud prosecutions.

### 4.4 Services and payments after death

Any service or payment dated after the beneficiary's date of death, beyond
a short grace period for legitimate end-of-month payments, is flagged. Death
data come from SSA through Treasury's Do Not Pay service (which began
receiving SSA's full death file in 2023 under a three-year pilot) or from
state vital records; the Phase 1 public alternative is the obituary-backed
case library, which is too sparse to screen with.

## 5. Peer outliers, growth and threshold bunching

### 5.1 Peer groups

Every outlier test compares an entity with **peers in the same program,
service, place and period**: a hospice with hospices in its county and
year, a SNAP retailer with stores of the same type within a mile. A
national comparison mostly finds specialty, case mix and size.

### 5.2 Robust z-scores

For a peer group with values $x_i$,

$$z_i = \frac{x_i - \operatorname{median}(x)}{1.4826 \cdot \operatorname{MAD}(x)},$$

where $\operatorname{MAD}(x) = \operatorname{median}|x_i - \operatorname{median}(x)|$.
The constant makes the scale match a standard deviation for normal data, and
unlike the mean and standard deviation, a few extreme entities cannot mask
themselves by inflating the scale. Skewed measures (dollars, counts) are
log-transformed first. Review threshold: $z > 3.5$ (set per screen in the
calibration week).

### 5.3 Count data and empirical Bayes shrinkage

For counts (claims, services, meals) with exposure (beneficiaries, enrolled
children), let entity $i$ have observed count $y_i$ and expected count
$E_i$ from its peers' rate. The raw ratio $y_i / E_i$ is unstable when
$E_i$ is small: 3 claims against 0.5 expected looks like a 6x outlier but
is weak evidence. We model

$$y_i \sim \text{Poisson}(\theta_i E_i), \qquad \theta_i \sim \text{Gamma}(\alpha, \beta),$$

fit $\alpha, \beta$ across the peer population by the method of moments,
and rank on the posterior

$$\theta_i \mid y_i \sim \text{Gamma}(\alpha + y_i,\ \beta + E_i), \qquad
\mathbb{E}[\theta_i \mid y_i] = \frac{\alpha + y_i}{\beta + E_i}.$$

Leads are ranked by the posterior probability that $\theta_i$ exceeds a
material multiple of peers (1.5x by default), which balances size of
excess against strength of evidence. This is the same approach used in
disease mapping and in the hierarchical models behind CMS's hospital
readmission and mortality measures.

### 5.4 Bunching below thresholds

If a limit $T$ invites steering, amounts pile up just below it. Bin amounts
in width $w$, fit a polynomial of degree 5 to bin counts outside a window
around $T$, and predict counts inside the window. Excess mass is

$$B = \sum_{\text{bins below } T \text{ in window}} (c_j - \hat c_j), \qquad
b = B \Big/ \sum \hat c_j,$$

following Chetty et al. (2011). A ratio $b$ well above zero, with
matching missing mass just above $T$, is strong population-level evidence
of splitting or steering. Applied to card purchases (micro-purchase
limit), contract actions (simplified acquisition and certified cost data
thresholds) and grant draws (prior-approval thresholds). Standard errors
come from bootstrapping the residuals.

### 5.5 Rapid growth and change points

For an entity's monthly payments $x_t$ with a peer-based expected level
$\mu_0$, the one-sided CUSUM

$$S_t = \max(0,\ S_{t-1} + x_t - \mu_0 - k)$$

signals when $S_t > h$. Setting $k$ to half the shift worth detecting and
$h$ at four to five standard deviations gives a low false-alarm rate. CUSUM
catches sudden ramps (a new hospice billing at the cap within months, a
retailer whose redemptions triple) that annual totals hide.

### 5.6 Concentration

The Gini coefficient of an entity's billing across service codes, or of a
program's payments across entities, measures concentration. A provider
whose billing collapses onto one or two high-paying codes (Gini near 1
where peers sit near 0.5) is an upcoding signal; a program where a handful
of new entities take most of the money is a capture signal.

## 6. Collusion screens for sealed bids

Bid rigging leaves statistical traces in the full set of bids, which state
DOTs publish as bid tabulations (DOT-1) and some agencies release on
request. For each tender with bids $b_{(1)} \le b_{(2)} \le \dots \le b_{(n)}$:

| Screen | Formula | Collusive pattern |
| --- | --- | --- |
| Coefficient of variation | $\text{CV} = \sigma_b / \bar b$ | Low: cover bids cluster near an agreed price |
| Spread | $(b_{(n)} - b_{(1)}) / b_{(1)}$ | Low |
| Relative distance | $\text{RD} = (b_{(2)} - b_{(1)}) / \sigma_{\text{losing}}$ | High: a gap between the designated winner and tight cover bids |
| Skewness and kurtosis | Third and fourth standardized moments of the bids | Distorted by clustered cover bids |
| Cover ratio | Mean losing bid divided by winning bid | Stable across tenders for the same group |

Imhof, Karagök and Rutz (2018) found these distribution screens separate
known Swiss cartels from competitive markets, and Huber and Imhof (2019)
raised accuracy by combining them in a classifier. Our use: compute the
screens per tender, then compare each regular group of bidders with the
same work type and region.

**Rotation test.** Among a stable group of firms, cartels often take turns.
Count how often the same firm wins two consecutive tenders, and compare
with a permutation distribution formed by shuffling the order of the same
wins. Too *few* repeats (an orderly rotation) is the signal.

**Market allocation.** A win-share matrix shows, for each pair of firms that
often bid together, who wins. Firms that meet often but each win only in
"their" county or season are flagged for review.

**Benign causes.** Few bidders in rural markets, standard engineer's
estimates that anchor bids, capacity constraints. Screens are
leads for DOJ's Procurement Collusion Strike Force, not findings.

## 7. Entity resolution

The entity spine joins records that describe the same business or person
across SAM.gov, USAspending, NPPES, Form 990, state registries and the
watch lists. Errors here create false networks (merging strangers) or hide
real ones (splitting one entity).

**Blocking.** Compare only pairs that share a cheap key (ZIP plus name
token, phone, email domain, UEI, NPI), which reduces billions of pairs to
millions.

**Comparison.** For each candidate pair, compare fields to get an agreement
vector $\gamma$: name (Jaro-Winkler similarity at least 0.92 after removing
legal suffixes), street address (USPS-standardized, exact), phone (exact),
officer name, email domain.

**Fellegi-Sunter weights.** With $m_k = P(\gamma_k = 1 \mid \text{match})$
and $u_k = P(\gamma_k = 1 \mid \text{non-match})$, the match weight is

$$W = \sum_k \left[\gamma_k \log_2 \frac{m_k}{u_k} + (1 - \gamma_k)\log_2\frac{1 - m_k}{1 - u_k}\right].$$

A rare field agreement (same phone number) earns a large weight because
$u_k$ is tiny; a common one (same city) earns little. $m$ and $u$ are
estimated without labels by the EM algorithm and checked on the 500
hand-labeled pairs in the methodology.

**Decision.** Pairs above an upper threshold are matches; below a lower
threshold, non-matches; between them, clerical review. The upper threshold
is the lowest weight with labeled precision of 95% or better.

**Clustering.** Linking matched pairs transitively can chain unrelated
records (A matches B, B matches C, A and C are strangers). We cluster on the
weighted match graph and split clusters whose weakest internal link falls
below the upper threshold.

## 8. Network analysis

### 8.1 Shared-attribute graph

Entities connect through shared attributes: address, phone, email, officer,
registered agent and, in Phase 2, bank account and device. We build the
bipartite entity-attribute graph and project it onto entities with an
Adamic-Adar style weight:

$$w_{ij} = \sum_{a \in A_i \cap A_j} \frac{1}{\log(1 + \deg(a))}.$$

A phone shared by two firms counts far more than an address shared by
4,000 firms at a registered agent. Attributes on the benign-hub list, or
shared by more entities than a set cap, are dropped.

### 8.2 Co-location test

Is an address hosting more entities than its type explains? If addresses of
that type (single-family home, small office, mailbox store) average
$\lambda$ registered entities, the Poisson tail

$$P(X \ge k) = 1 - \sum_{i=0}^{k-1} \frac{e^{-\lambda}\lambda^i}{i!}$$

gives how surprising $k$ entities are. Twelve federal contractors at a
house where 1.5 are typical is a lead; twelve at a coworking space is not.

### 8.3 Components, brokers and communities

- **Connected components** above an edge-weight floor give candidate rings.
- **Betweenness centrality** finds brokers (one consultant, preparer or
  billing agent linking many outliers), a pattern in E-Rate, SBA lending and
  health care cases.
- **Community detection** (Louvain or Leiden) splits large components into
  tighter groups for review.
- **Temporal motifs** catch waves: many entities registered within weeks of
  each other at linked addresses, just before a program opens.

### 8.4 Risk propagation

Personalized PageRank spreads risk from known bad actors (excluded,
debarred, convicted entities) through weighted links. With restart
probability $\alpha$ and seed distribution $s$,

$$r = \alpha s + (1 - \alpha) P^{\top} r,$$

where $P$ is the row-normalized weighted adjacency matrix. An entity's
score measures how close it sits to known fraud through strong links. Used
as a signal, never as guilt by association: a high score must be paired
with an independent signal of its own.

## 9. Eligibility and identity tests

Mostly Phase 2, run on applicant and payee files under OIG data agreements.

| Test | Rule | Programs |
| --- | --- | --- |
| Death match | Payment or service date after date of death (SSA full death file, state records) | Medicare, Medicaid, FEHB, VA, PBGC, RRB, SNAP, OPM annuities |
| Incarceration match | Benefit paid during a period of incarceration (BOP and state prison data) | SSI, UI, SNAP, VA |
| Impossible identity | SSN issued after the person's stated birth year plus a plausible gap, or SSN issued after the claim; SSNs issued after June 2011 are randomized and need SSA verification instead of area-number rules | UI, SBA, student aid |
| Identity reuse | One SSN, bank account, phone, email or device behind claims in several states or programs | UI, SNAP, Medicaid, SBA, ED |
| Synthetic identity | Thin credit-file-style profile: new email, prepaid phone, no history, shared device | UI, SBA, tax credits |
| Concurrent eligibility | Benefits that cannot legally be received together (for example some disability and earnings combinations) | SSA, RRB, DOL, VA |

Bank-account reuse is the strongest single identity signal in pandemic
cases; it is the core of cross-agency idea X-2 in the roadmap.

## 10. Estimating improper payments

Agencies estimate improper payments by sampling payments and reviewing
them (Payment Integrity Information Act of 2019; OMB Circular A-123,
Appendix C). We need this math for three jobs: reading published estimates
critically, designing samples for Phase 2 pilots, and estimating the
dollars behind a screen's leads without overstating them.

### 10.1 Stratified expansion estimator

Payments are split into strata $h$ (by size, region or payment type). From
$N_h$ payments, $n_h$ are sampled and reviewed, giving improper dollars
$y_{hi}$. The estimated total and its variance are

$$\hat Y = \sum_h N_h \bar y_h, \qquad
\widehat{\operatorname{Var}}(\hat Y) = \sum_h N_h^2 \left(1 - \frac{n_h}{N_h}\right)\frac{s_h^2}{n_h}.$$

The improper payment rate is $\hat R = \hat Y / X$, where $X$ is total
outlays, with standard error $\operatorname{SE}(\hat Y)/X$. A two-sided
interval at confidence $1-a$ is $\hat Y \pm z_{1-a/2}\operatorname{SE}$.

### 10.2 Ratio estimator

When improper dollars scale with payment size, the combined ratio
estimator is more precise:

$$\hat R = \frac{\sum_h N_h \bar y_h}{\sum_h N_h \bar x_h}, \qquad
\widehat{\operatorname{Var}}(\hat R) = \frac{1}{\hat X^2} \sum_h N_h^2 \left(1 - \frac{n_h}{N_h}\right)\frac{s_{d,h}^2}{n_h},$$

where $x$ is dollars paid, $\hat X = \sum_h N_h \bar x_h$ and $d = y - \hat R x$ are the residuals
(Taylor linearization).

### 10.3 When the normal interval fails

Improper dollars are highly skewed: most sampled payments are fully
correct, a few are wholly wrong. Normal-theory intervals then cover the
truth less often than stated. In our simulation (8% of payments improper,
lognormal payment sizes; see `analytics/tests/test_forensic.py`), nominal
90% intervals covered the true rate about 77% of the time at $n = 100$,
84% at $n = 400$ and 88% at $n = 1{,}500$. Remedies, in order of
preference: larger samples in high-variance strata (Neyman allocation,
$n_h \propto N_h S_h$), bootstrap intervals, and for audits with few
errors, monetary unit sampling.

### 10.4 Monetary unit sampling

Monetary unit (dollar unit) sampling selects dollars, not payments, so
large payments are more likely to be sampled. With book value $BV$, $n$
sampled dollars and taintings $t_{(1)} \ge t_{(2)} \ge \dots$ (each error's
share of its payment's value), the Stringer upper error limit is

$$\text{UEL} = \frac{BV}{n}\left[U(0) + \sum_{i \ge 1} \big(U(i) - U(i-1)\big)\, t_{(i)}\right],$$

where $U(k) = \tfrac{1}{2}\chi^2_{c}(2k + 2)$ is the upper Poisson confidence
limit after $k$ errors ($U(0) = 3.00$ and $U(1) = 4.74$ at 95%). The sample
size that keeps the bound under a tolerable misstatement $TM$ when no
errors are expected is $n = BV \cdot U(0) / TM$.

### 10.5 Conventions to know

- HHS-OIG and Medicare contractors extrapolate overpayments using the
  lower limit of a confidence interval (HHS-OIG uses the lower limit of a
  two-sided 90% interval), which favors the provider. Our lead packages use
  the same convention when they size dollars.
- HHS-OIG's RAT-STATS is the standard tool for these samples; our code
  reproduces its core estimators for checking.
- **Unknown payments** (payments that cannot be shown proper for lack of
  documentation) are reported separately from improper payments under
  A-123 and are neither fraud nor savings.
- **Improper is not fraud.** GAO estimated federal fraud losses at $233
  billion to $521 billion a year (GAO-24-105833) using a different method;
  FY2025 improper payment estimates totaled about $186 billion across 64
  programs at 15 agencies (GAO-26-108694). Neither figure is ever used as
  a savings claim.

### 10.6 Checking a published estimate

From public reports we can test whether an estimate is internally
consistent: whether its stated interval matches its sample size and
strata, whether the rate moved more than its standard error would allow
from one year to the next without a stated cause, and whether programs that
"did not report" left large susceptible outlays unmeasured. These checks
become questions in a Phase 2 proposal, not findings.

## 11. Reconciliation and audit-trail tests

### 11.1 Public reconciliations (Phase 1)

| Check | Left side | Right side | What a gap means |
| --- | --- | --- | --- |
| Account to award | USAspending File A/B obligations and outlays by Treasury account | File C award-level obligations linked to D1/D2 awards | Unlinked or unreported awards; spending invisible to payee-level screens |
| Agency totals | USAspending agency outlays | Treasury Monthly Treasury Statement outlays | Reporting scope differences (trust funds, offsetting receipts); explains, rarely fraud |
| Program outlays | PaymentAccuracy.gov susceptible outlays by program | USAspending outlays by Assistance Listing | Programs measured on a different base than they pay out |
| Prime to subaward | Prime award obligation | Sum of FFATA subawards reported under it | Subawards exceeding the prime are impossible and point to reporting errors or double-counting; missing subawards hide pass-throughs |
| Grantee self-report | Grant drawdowns in USAspending | Federal expenditures reported in the grantee's Single Audit | Large unexplained gaps between what was drawn and what was audited |
| Single Audit findings | Federal Audit Clearinghouse findings and questioned costs | The grantee's continuing awards | Repeat material weaknesses or questioned costs with no change in funding |

The Single Audit data (fac.gov) are the broadest public internal-control
data in government: every non-federal entity spending $1 million or more
of federal awards a year (the threshold since the 2024 Uniform Guidance
revision) files one. Two cheap signals cover every grant-making agency:
repeat findings at the same grantee, and **auditor concentration** (one
small audit firm auditing many grantees that share officers, or whose
audits never report findings).

### 11.2 Audit-trail tests on internal ledgers (Phase 2)

These follow the journal-entry and fraud procedures in auditing standards
(AU-C 240 and PCAOB AS 2401) and are run on the general ledger, vendor
master, payment and card files that OIGs can obtain.

| Test | Rule | Scheme |
| --- | --- | --- |
| Sequence gaps and duplicates | Missing or repeated check, invoice and obligation numbers | Removed or fabricated documents |
| Three-way match | Payment without a matching order and receiving report, or with amounts that differ | Payment for goods not delivered |
| Vendor-employee match | Vendor address, phone or bank account equal to an employee's | Shell vendors owned by insiders |
| Bank account change | Vendor bank account changed shortly before a large payment, especially after an email request | Business email compromise, diversion |
| Segregation of duties | Same user created the vendor, entered the invoice and approved the payment | Insider fraud |
| Timing | Entries on weekends, holidays or after hours; entries just after period close | Concealment, manipulation |
| Just-below-approval | Entries clustered under a user's approval limit (bunching test, section 5.4) | Splitting to avoid review |
| Card tests | Split purchases (section 4.2), merchant category codes outside policy, purchases on leave days | Purchase and travel card misuse (Government Charge Card Abuse Prevention Act of 2012 requires OIG risk assessments of these programs) |
| Payroll | Employees with no leave ever, shared bank accounts, pay after separation | Ghost employees |

## 12. Combining signals, calibrating and validating

### 12.1 Likelihood ratios

For a binary signal $S$, the case library gives

$$\text{LR}^{+} = \frac{P(S \mid \text{known case})}{P(S \mid \text{population})},$$

estimated with additive smoothing so an unobserved combination never gets a
ratio of zero. Under conditional independence, posterior odds are prior
odds times the product of the signals' ratios:

$$\frac{P(F \mid S_1, \dots, S_k)}{1 - P(F \mid S_1, \dots, S_k)} = \frac{\pi}{1 - \pi}\prod_{j} \text{LR}_j.$$

Correlated signals (shared address and shared phone) are grouped and only
the strongest in each group enters the product.

### 12.2 The base-rate trap

Even a strong signal leaves most flagged entities innocent when fraud is
rare. A signal present in 40% of known cases and 0.5% of the population has
$\text{LR}^{+} = 80$; with a 1-in-1,000 prior, the posterior is only about
7%. This is why the methodology requires two independent signals and human
review, and why scores are presented as rankings for review, not as
probabilities of guilt. (The numbers in this paragraph are illustrative and
are reproduced in the scoring tests.)

### 12.3 Validation metrics

- **Lift at the top $q$:** share of known cases in the top $q$ of scores
  divided by their share overall. Release bar: lift of 5 or more at the
  top 5% (methodology section 5).
- **Precision at $k$:** share of known cases (or of hand-review "worth a
  look" judgments) among the top $k$ leads, matched to investigator
  capacity.
- **Average precision:** area under the precision-recall curve; preferred
  over ROC AUC when cases are rare.
- **Calibration:** when scores are shown as probabilities in Phase 2,
  isotonic regression on held-out cases maps scores to observed rates.
- **Temporal holdout:** score the population as it looked before each
  case became public, so a screen is not credited for finding cases it
  learned from.

### 12.4 Controlling false discoveries

When the same test runs on $m$ entities, rank their p-values
$p_{(1)} \le \dots \le p_{(m)}$ and flag the largest $k$ with

$$p_{(k)} \le \frac{k}{m}\, q.$$

The Benjamini-Hochberg procedure keeps the expected share of chance hits
among flagged entities at or below $q$ (we use $q = 0.05$ for entity-level
digit and outlier tests).

## 13. Methods by fraud area

Each fraud area in the roadmap maps to a small set of tests. "P1" means the
test runs on public data in Phase 1; "P2" needs internal data.

| Fraud area | Main schemes | Primary tests (section) | Data | Agencies (examples) |
| --- | --- | --- | --- | --- |
| Health care billing | Upcoding, phantom services, kickback-driven referrals, hospice and home health mills | Peer outliers with shrinkage (5.3), concentration (5.6), growth (5.5), impossible days (4.3, P2), after-death services (4.4, P2), networks (8) | CMS provider and utilization files (P1); claims (P2) | HHS, VA, OPM (FEHB), DOL (FECA), USPS (workers' comp) |
| Procurement fronts | Pass-through set-aside fronts, shell bidders | Entity resolution (7), shared attributes and co-location (8.1-8.2), new entity with large award, subaward reconciliation (11.1) | SAM.gov, FPDS, USAspending subawards | DoD, VA, DOT, GSA, SBA, USACE, all agencies (U4) |
| Bid rigging | Rotation, cover bids, market allocation | Collusion screens and rotation test (6) | State DOT bid tabs; agency bid data (P2) | DOT, USACE, DoD, GSA |
| Price and cost mischarging | Inflated prices, defective pricing, labor mischarging | Unit price outliers (5.2), modification growth (U3), bunching under cost-data thresholds (5.4), impossible hours (4.3, P2) | FPDS, USAspending; invoices and timesheets (P2) | DoD, NASA, DOE, GSA |
| Grant misuse | Duplicate funding, unallowable costs, ghost participants | Text-similarity duplicate awards, Single Audit findings and auditor concentration (11.1), cost per participant outliers (5.2), drawdown gaps (11.1) | USAspending, fac.gov, Form 990, SBIR.gov | NSF, NIH, DOE, EPA, NEA, NEH, IMLS, regional commissions, LSC, CPB |
| Loans and guarantees | Identity and income fraud, lender and agent rings, straw borrowers | Entity resolution (7), broker centrality (8.3), digit tests on loan amounts (3), bunching under program caps (5.4) | SBA and USDA loan-level releases, EXIM authorizations, HMDA | SBA, USDA, HUD (FHA), EXIM, DFC |
| Benefits | Ineligible, deceased or incarcerated recipients; identity reuse | Death, incarceration and identity tests (9), sampling estimates (10) | Aggregate public statistics (P1); payee files (P2) | SSA, RRB, DOL, VA, OPM, USDA |
| Tax credits | Preparer-driven false claims | Geographic outliers with shrinkage (5.3) on IRS statistics by ZIP; preparer networks (P2) | IRS SOI ZIP data (P1); returns (P2, section 6103 limits) | Treasury |
| Customs and trade | Undervaluation, false origin, transshipment | Mirror-trade gaps, importer entity resolution, co-location (8.2) | Census trade data, manifests | DHS |
| Subsidies (E-Rate, Lifeline, BEAD) | Consultant-steered bids, phantom subscribers | Collusion screens (6), broker centrality (8.3), duplicate subscribers (4.1, P2) | USAC open data | FCC, Commerce |
| Disaster and emergency aid | Duplicate claims, ineligible addresses | Duplicate tests (4.1), identity reuse (9), address validation | FEMA public data (P1); applicant files (P2) | DHS (FEMA), SBA, HUD (CDBG-DR) |
| Settlement and refund distributions | Synthetic claimants, duplicate claims | Duplicate and identity tests (4.1, 9) on claims files | Distribution reports (P1); claims (P2) | CFPB, FTC, SEC, CFTC, DOJ |
| Internal (every agency) | Card misuse, payroll ghosts, insider vendors, payment diversion | Split purchases (4.2), audit-trail tests (11.2), bunching (5.4) | OIG charge card risk assessments (P1); ledgers and card files (P2) | All bodies (U7) |

## 14. Reference implementation

`analytics/forensic/` holds a small, readable implementation of every test
in this handbook, with 30 unit tests that run on synthetic data:

| Module | Sections |
| --- | --- |
| `digits.py` | 3: Benford first, second, first-two and last-two digit tests; MAD conformity; per-digit z; summation; round numbers; duplication; relative size factor |
| `duplicates.py` | 4: invoice normalization, four-tier duplicate test, split purchases, impossible days, after-death services |
| `outliers.py` | 5: robust z, Poisson-Gamma shrinkage, CUSUM, bunching, Gini |
| `bids.py` | 6: tender screens, rotation test, win-share matrix |
| `linkage.py` | 7: Fellegi-Sunter EM, thresholds, Jaro-Winkler |
| `network.py` | 8: shared-attribute projection, components, personalized PageRank, co-location |
| `sampling.py` | 10: stratified and ratio estimators, Neyman allocation, sample sizes, monetary unit sampling |
| `scoring.py` | 12: likelihood ratios, posterior odds, lift, precision, average precision, two-signal rule |

Run `python3 -m unittest discover -s analytics/tests -t analytics` from the
repository root. Production pipelines may use faster libraries but must
reproduce these functions' results on the test fixtures.

## Sources

- Nigrini, M. (2012). *Benford's Law: Applications for Forensic Accounting,
  Auditing, and Fraud Detection.* Wiley.
- Fellegi, I. and Sunter, A. (1969). "A Theory for Record Linkage."
  *Journal of the American Statistical Association* 64(328).
- Winkler, W. (1988). "Using the EM Algorithm for Weight Computation in
  the Fellegi-Sunter Model of Record Linkage." Proceedings of the Section
  on Survey Research Methods, American Statistical Association.
- Imhof, D., Karagök, Y. and Rutz, S. (2018). "Screening for Bid
  Rigging: Does It Work?" *Journal of Competition Law & Economics* 14(2).
- Huber, M. and Imhof, D. (2019). "Machine Learning with Screens for
  Detecting Bid-Rigging Cartels." *International Journal of Industrial
  Organization* 65.
- Chetty, R., Friedman, J., Olsen, T. and Pistaferri, L. (2011).
  "Adjustment Costs, Firm Responses, and Micro vs. Macro Labor Supply
  Elasticities." *Quarterly Journal of Economics* 126(2).
- Benjamini, Y. and Hochberg, Y. (1995). "Controlling the False Discovery
  Rate." *Journal of the Royal Statistical Society B* 57(1).
- Cochran, W. (1977). *Sampling Techniques*, 3rd ed. Wiley.
- [GAO-15-593SP: A Framework for Managing Fraud Risks in Federal Programs](https://www.gao.gov/products/gao-15-593sp)
- [GAO-24-105833: federal fraud losses estimated at $233B to $521B a year](https://www.gao.gov/products/GAO-24-105833)
- [GAO-26-108694: FY2025 improper payments](https://www.gao.gov/products/gao-26-108694)
- [PaymentAccuracy.gov agencies and programs](https://paymentaccuracy.gov/agencies-and-programs)
- [OMB M-21-19: Appendix C to Circular A-123](https://www.whitehouse.gov/wp-content/uploads/2021/03/M-21-19.pdf)
- [Federal Audit Clearinghouse](https://www.fac.gov/)
- [USAspending DATA Act file definitions (DAIMS)](https://fiscal.treasury.gov/data-transparency/DAIMS-current.html)
- [HHS-OIG RAT-STATS](https://oig.hhs.gov/compliance/rat-stats/)
- [AICPA Statement on Standards for Forensic Services No. 1](https://www.aicpa-cima.com/resources/download/statement-on-standards-for-forensic-services)
- [DOJ Procurement Collusion Strike Force](https://www.justice.gov/procurement-collusion-strike-force)
