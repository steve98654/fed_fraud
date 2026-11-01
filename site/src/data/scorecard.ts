// The scorecard's only hand-edited numbers. Everything else on the site is
// read from the Markdown in ../docs.
//
// RULE: record a finding here only after its screen has passed validation
// (review plan, "Validation") and the lead package has been through counsel
// review. Until then the scorecard shows "Pending", never an estimate.

export const asOf = '2026-11-01';

export type Stage = 'Planned' | 'In review' | 'Leads delivered' | 'Referred';

export interface Finding {
  /** Roadmap idea ID, e.g. "HHS-1". */
  idea: string;
  /** Brief slug, e.g. "hhs". */
  agency: string;
  title: string;
  /** Date the package was delivered, YYYY-MM-DD. */
  date: string;
  leads: number;
  referredTo?: string;
  /** Dollars of improper payments identified in delivered leads (not recovered). */
  identifiedUsd?: number;
  /** Dollars recovered or prevented, as confirmed by the receiving office. */
  confirmedUsd?: number;
  note?: string;
}

/** Confirmed, delivered findings. Empty until Phase 1 produces its first. */
export const findings: Finding[] = [];

/** Optional per-agency override of the stage shown in the scorecard. */
export const stageOverride: Record<string, Stage> = {};
