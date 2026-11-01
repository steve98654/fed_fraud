// Plain definitions of the terms used across the site, drawn from the
// methodology (docs/playbook/methodology.md), the review plan and the top 33
// ranking. Keep each definition consistent with those documents.

export interface Term {
  term: string;
  id: string;
  group: string;
  def: string;
  /** Site path (without base) for more detail. */
  see?: { label: string; href: string };
}

const t = (group: string, term: string, def: string, see?: Term['see']): Term => ({
  term,
  group,
  def,
  see,
  id: term.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, ''),
});

const LADDER = { label: 'Methodology, section 7', href: 'library/methodology/#7-how-a-figure-moves-from-pending-to-confirmed-savings' };
const VALID = { label: 'Methodology, section 5', href: 'library/methodology/#5-validation' };

export const GLOSSARY_GROUPS = ['Savings ladder', 'Finding fraud', 'Planning and priority', 'Data and access'];

export const glossary: Term[] = [
  t('Savings ladder', 'Pending', 'The default for every figure on the scorecard: no validated screen or delivered lead yet. The site shows "Pending" instead of an estimate.', LADDER),
  t('Savings ladder', 'Identified', 'Dollars paid to entities in a delivered lead package, taken from public award or payment records. It is an upper bound on money under review, not a finding of fraud.', LADDER),
  t('Savings ladder', 'Referred', 'A lead package has been accepted for review by an Office of Inspector General or a DOJ component.', LADDER),
  t('Savings ladder', 'Confirmed', 'Dollars the receiving office confirms as recovered, prevented or subject to a judgment, settlement or payment stop. Only confirmed dollars count as savings.', LADDER),
  t('Savings ladder', 'Improper payment', 'A payment that should not have been made or was made in the wrong amount. It includes fraud but also errors and missing paperwork; agency improper payment rates appear on the site as context, never as savings.'),
  t('Finding fraud', 'Screen', 'A repeatable test run over a program\'s records that scores each entity on fraud signals, such as shell-company traits or shared identifiers.', { label: 'Tool previews', href: 'tools/' }),
  t('Finding fraud', 'Signal', 'One measurable sign of risk, scaled against peers in the same program, place and period. An entity becomes a lead only when at least two independent signals fire (the two-signal rule).', { label: 'Methodology, section 3', href: 'library/methodology/#3-signal-library' }),
  t('Finding fraud', 'Reason codes', 'The signals that drove a score, each with its source record and date. A score without reasons is never shown.', { label: 'Methodology, section 4', href: 'library/methodology/#4-scoring-and-reason-codes' }),
  t('Finding fraud', 'Entity resolution', 'Matching the same business or person across spellings, addresses, phone numbers and identifiers, reusing the SBA matcher.', { label: 'Methodology, section 2', href: 'library/methodology/#2-entity-resolution' }),
  t('Finding fraud', 'Case library', 'Entities charged or settled in past fraud cases, used to back-test screens and to show which known cases a lead resembles.'),
  t('Finding fraud', 'Validation', 'The test every screen passes before its leads are used: a back-test against the case library, a hand review of 25 top-scored entities, and a release bar (known cases at least five times more common in the top 5%, and at least half of the sample worth review).', VALID),
  t('Finding fraud', 'Lead package', 'What goes to an Inspector General or DOJ for one entity or network: a summary, the signals with source records, a known-case match, the limits of public data and the provenance of every pull.', { label: 'Methodology, section 6', href: 'library/methodology/#6-from-lead-to-referral' }),
  t('Finding fraud', 'Counsel review', 'Legal review of lead packages before release; the first ten packages go through counsel. No lead names a person in any public document.'),
  t('Finding fraud', 'Inspector General (OIG)', 'The independent Office of Inspector General inside each agency, which investigates fraud in that agency\'s programs and can act on our leads.'),
  t('Planning and priority', 'Phase 1', 'Sixteen working weeks from November 2, 2026, using public data only, to build shared screens, validate them and deliver the first lead packages.', { label: 'Phase 1 schedule', href: 'schedule/' }),
  t('Planning and priority', 'Phase 2', 'The follow-on stage that uses agency internal data (claims, invoices, applications) obtained through OIG partnerships and data agreements, opened by Phase 1 leads.', { label: 'Investigations: cross-agency', href: 'investigations/' }),
  t('Planning and priority', 'Investigation ID', 'A label such as HHS-1 (agency code and number) that ties an investigation idea to its prototype, pitch, memo and results. X-1 to X-6 are cross-agency Phase 2 ideas.', { label: 'All investigations', href: 'investigations/' }),
  t('Planning and priority', 'Start first', 'The ten investigations where the most fraud-prone money meets record-level public data; they begin in Phase 1 Waves 1 and 2.', { label: 'Roadmap page 1', href: 'plan/' }),
  t('Planning and priority', 'Deep dive', 'A full agency review in Wave 1 (HHS, DoD, SBA, weeks 3 to 7) or Wave 2 (DHS, USDA, DOT, GSA, weeks 5 to 10).', { label: 'Roadmap page 2', href: 'plan/deep-dives/' }),
  t('Planning and priority', 'Contained pilot', 'A narrower review of one well-defined program, for FCC, OPM, VA, Commerce and PBGC in weeks 7 to 11.', { label: 'Roadmap page 3', href: 'plan/pilots-and-shared-screens/' }),
  t('Planning and priority', 'Shared screen', 'One screen run across several agencies at once: the contractor screen, the research award screen and the grantee screen.', { label: 'Roadmap page 3', href: 'plan/pilots-and-shared-screens/' }),
  t('Planning and priority', 'Access case', 'For agencies whose risky payments are not visible in public data (Treasury, SSA, Labor, Education and others), an aggregate screen plus the case for getting internal data in Phase 2.', { label: 'Roadmap page 4', href: 'plan/access-cases/' }),
  t('Planning and priority', 'Priority score', 'How the 33 agencies are ranked: 0.3 × Exposure + 0.3 × Public data + 0.2 × SBA method fit + 0.2 × Actionability, each scored 1 to 5.', { label: 'Priority matrix', href: 'agencies/matrix/' }),
  t('Data and access', 'USAspending', 'The federal government\'s public record of contracts, grants, loans and outlays; the source of the FY2026 outlay figures on the scorecard.'),
  t('Data and access', 'SAM.gov', 'The System for Award Management, where federal contractors and grantees register and where exclusions (debarred parties) are listed.'),
  t('Data and access', 'LEIE', 'The HHS-OIG List of Excluded Individuals and Entities, barred from federal health care programs.'),
  t('Data and access', 'Do Not Pay', 'Treasury\'s central screening service, which matches payments against death and exclusion data. A Phase 2 route for cross-agency payment screens.'),
  t('Data and access', 'Computer matching agreement', 'The Privacy Act agreement, approved by Data Integrity Boards, required for many cross-agency data matches. It typically takes six to twelve months, so Phase 2 starts with OIG partnerships.'),
];
