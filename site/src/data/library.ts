// Section 4: research, plans, results and methodology documents that are
// still to be written. Each entry renders as a placeholder page with its
// planned outline, due date and the plan item it comes from.

export interface LibraryDoc {
  slug: string;
  kind: 'Methodology' | 'Research' | 'Plan' | 'Results';
  title: string;
  summary: string;
  /** Review-plan IDs this document delivers (F#, P#, C#). */
  planIds: string[];
  /** Phase 1 week it is due. */
  dueWeek: number;
  /** Where the Markdown source will live in the repo. */
  source: string;
  outline: { heading: string; note: string }[];
}

export const library: LibraryDoc[] = [
  {
    slug: 'methodology',
    kind: 'Methodology',
    title: 'Methodology: from public records to a scored lead',
    summary:
      'How the shared pipeline turns award, provider and entity data into ranked risk scores with stated reasons, and how each screen is validated before its leads are used.',
    planIds: ['F3', 'F7', 'F8'],
    dueWeek: 4,
    source: 'docs/playbook/methodology.md',
    outline: [
      { heading: 'Entity spine', note: 'SAM.gov, USAspending, FPDS keyed by UEI; NPI and EDGAR CIK cross-keys.' },
      { heading: 'Entity resolution', note: 'Names, USPS-standardized addresses, phones and officers; precision on 500 labeled pairs.' },
      { heading: 'Signal library', note: 'Shared address, shared officer, new entity with large award, excluded link, peer outlier, rapid growth.' },
      { heading: 'Scoring and reason codes', note: 'Calibration, thresholds and false-positive notes for each signal.' },
      { heading: 'Validation', note: 'Back-test against known cases; hand review of 25; the 5x top-5% release bar.' },
      { heading: 'Limits', note: 'Data lags, suppression and what public data cannot show.' },
    ],
  },
  {
    slug: 'sba-baseline',
    kind: 'Methodology',
    title: 'SBA baseline playbook',
    summary:
      'What the SBA work with Rosemary does today, written down so it can be reused: data sources, fraud typologies, features, scoring and measured results, with SBA-only parts marked.',
    planIds: ['F1'],
    dueWeek: 2,
    source: 'docs/playbook/sba-baseline.md',
    outline: [
      { heading: 'Data sources', note: 'Loan-level PPP, EIDL, 7(a) and 504 releases and enrichment.' },
      { heading: 'Typologies', note: 'Identity theft, shell entities, stacked awards, ineligible recipients.' },
      { heading: 'Features and scoring', note: 'Which signals carry over to other agencies.' },
      { heading: 'Measured results', note: 'What the SBA work has found and how it was confirmed.' },
      { heading: 'Portability', note: 'What transfers to the other 32 agencies and what is SBA-only.' },
    ],
  },
  {
    slug: 'case-library',
    kind: 'Research',
    title: 'Fraud case library and typology research',
    summary:
      'DOJ press releases, OIG reports and GAO findings from 2020 to 2026, tagged by agency, program, scheme, dollars and entities. It is the label set every screen is tested against.',
    planIds: ['F5', 'F6'],
    dueWeek: 6,
    source: 'docs/research/case-library.md',
    outline: [
      { heading: 'Coverage', note: 'At least 2,000 tagged fraud releases across all U.S. Attorneys’ offices.' },
      { heading: 'Scheme taxonomy', note: 'Fronts, shells, kickbacks, false billing, identity reuse, ineligible payees.' },
      { heading: 'Typologies by agency', note: 'Which schemes recur in which programs, with dollar ranges.' },
      { heading: 'Entity links', note: 'Defendants and companies linked to UEI or NPI where possible.' },
    ],
  },
  {
    slug: 'data-sources',
    kind: 'Research',
    title: 'Data sources, watch lists and pull log',
    summary:
      'Every public dataset used, with source, URL, pull date, row count and hash, plus the watch lists and the FOIA requests filed in week 1.',
    planIds: ['F2', 'F4', 'F10'],
    dueWeek: 2,
    source: 'docs/research/data-sources.md',
    outline: [
      { heading: 'Award and entity data', note: 'USAspending, SAM.gov, FPDS, SBIR.gov, state DBE directories and bid tabs.' },
      { heading: 'Program data', note: 'CMS provider files, SNAP retailers, E-Rate, IRS SOI and others by agency.' },
      { heading: 'Watch lists', note: 'SAM exclusions, LEIE, OFAC, World Bank, HUD LDP, USAC suspensions.' },
      { heading: 'FOIA log', note: 'Requests filed, status and expected response dates.' },
    ],
  },
  {
    slug: 'agency-review-plans',
    kind: 'Plan',
    title: 'Detailed agency review plans',
    summary:
      'Expanded, step-by-step review plans for each of the 33 agencies: data pulls, screens, validation targets and owners, building on the one-page plans in this site.',
    planIds: ['A1', 'A2', 'B', 'C1', 'C2', 'C3', 'D'],
    dueWeek: 3,
    source: 'docs/review_plan.md',
    outline: [
      { heading: 'Wave 1 deep dives', note: 'HHS, DoD and SBA, weeks 3 to 7.' },
      { heading: 'Wave 2 deep dives', note: 'DHS, USDA, DOT and GSA, weeks 5 to 10.' },
      { heading: 'Contained pilots', note: 'FCC, OPM, VA, Commerce and PBGC, weeks 7 to 11.' },
      { heading: 'Shared screens', note: 'Contractor, research award and grantee screens, weeks 9 to 13.' },
      { heading: 'Aggregate screens', note: 'Treasury, SSA, Labor, Education, FDIC and Interior, weeks 10 to 14.' },
    ],
  },
  {
    slug: 'validation-reports',
    kind: 'Results',
    title: 'Screen validation reports',
    summary:
      'For each screen, how many known cases landed in its top 1%, 5% and 10%, the hand-review outcome, and whether it met the release bar. Misses are reported, not hidden.',
    planIds: ['F8'],
    dueWeek: 7,
    source: 'docs/reviews/validation.md',
    outline: [
      { heading: 'Back-test results', note: 'Known-case lift by screen.' },
      { heading: 'Hand review', note: 'Share of 25 top-scored entities judged worth review.' },
      { heading: 'Release decisions', note: 'Released, reworked or dropped, with reasons.' },
    ],
  },
  {
    slug: 'access-proposals',
    kind: 'Plan',
    title: 'Phase 2 data access proposals',
    summary:
      'The proposals that ask Inspectors General and agencies for internal claims, invoices and payment data, built on Phase 1 results. Six go out in week 8; Treasury, SSA and Labor follow.',
    planIds: ['P2', 'P4'],
    dueWeek: 8,
    source: 'docs/proposals/',
    outline: [
      { heading: 'Ask', note: 'Which data, which office and which legal route.' },
      { heading: 'Why it pays', note: 'The Phase 1 leads that internal data would turn into cases.' },
      { heading: 'Security and governance', note: 'Handling, retention and who sees what.' },
      { heading: 'Timeline', note: 'From signature to first pilot.' },
    ],
  },
  {
    slug: 'phase-1-report',
    kind: 'Results',
    title: 'Phase 1 report and leadership briefing',
    summary:
      'The consolidated results across all 33 agencies, written for OMB and agency leadership, with the Phase 2 go/no-go recommendation.',
    planIds: ['R', 'P6'],
    dueWeek: 16,
    source: 'docs/reports/phase-1.md',
    outline: [
      { heading: 'Findings', note: 'Validated screens, lead packages and referrals by agency.' },
      { heading: 'Savings', note: 'Identified, referred and confirmed amounts, each with its source.' },
      { heading: 'What did not work', note: 'Screens that missed the bar and why.' },
      { heading: 'Phase 2 recommendation', note: 'Partners, data and expected payoff.' },
    ],
  },
];

/** Outline used for every agency's detailed results placeholder. */
export const resultsOutline = [
  { heading: 'Summary', note: 'The finding in one paragraph, or a reasoned “nothing actionable from public data”.' },
  { heading: 'Where the money is', note: 'Programs and payment streams reviewed.' },
  { heading: 'Data pulled', note: 'Datasets, dates and row counts, linked to the pull log.' },
  { heading: 'Screens run', note: 'Each investigation idea, its signals and its validation result.' },
  { heading: 'Leads', note: 'Ranked lead list with reason codes (shared only with the receiving office).' },
  { heading: 'Referrals and outcomes', note: 'Packages sent, to whom, and what came back.' },
  { heading: 'Savings', note: 'Identified, referred and confirmed amounts, each with its source.' },
  { heading: 'Phase 2 request', note: 'What internal data would add, and the access route.' },
];
