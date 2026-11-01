// One row per agency with everything the scorecard shows, so the scorecard
// page, the compare page and the CSV/JSON downloads agree. Savings come only
// from src/data/scorecard.ts and read "Pending" until a finding is recorded.
import { agencies, groupLabel, phase2Ask, weekStart, weekEnd } from './content';
import { findings, stageOverride, asOf } from '../data/scorecard';

export { asOf };

export const stageOf = (slug: string) =>
  stageOverride[slug] ??
  (findings.some((f) => f.agency === slug && f.referredTo)
    ? 'Referred'
    : findings.some((f) => f.agency === slug)
      ? 'Leads delivered'
      : 'Planned');

const sum = (slug: string, k: 'identifiedUsd' | 'confirmedUsd') =>
  findings.filter((f) => f.agency === slug).reduce((n, f) => n + (f[k] ?? 0), 0);

const iso = (d: Date) => d.toISOString().slice(0, 10);

export interface Row {
  rank: number;
  slug: string;
  agency: string;
  short: string;
  fy2026_outlays_usd: number;
  budget_rank: number;
  priority_score: number;
  exposure: number;
  public_data: number;
  sba_fit: number;
  actionability: number;
  workstream: string;
  start_first: boolean;
  first_investigation: string;
  first_prototype: string;
  investigations: string[];
  phase1_start_week: number;
  phase1_end_week: number;
  phase1_start: string;
  phase1_end: string;
  take_leads_to: string;
  phase2_data_ask: string;
  stage: string;
  lead_packages: number;
  /** Dollars in delivered leads, or "Pending" while there are none. */
  savings_identified_usd: number | 'Pending';
  /** Dollars confirmed by the receiving office, or "Pending". */
  savings_confirmed_usd: number | 'Pending';
}

export function rows(): Row[] {
  return agencies().map((a) => {
    const mine = findings.filter((f) => f.agency === a.slug);
    return {
      rank: a.rank,
      slug: a.slug,
      agency: a.name,
      short: a.short,
      fy2026_outlays_usd: a.outlaysUsd,
      budget_rank: a.budgetRank,
      priority_score: a.score,
      exposure: a.factors.exposure,
      public_data: a.factors.data,
      sba_fit: a.factors.fit,
      actionability: a.factors.action,
      workstream: groupLabel(a.group),
      start_first: a.startFirst,
      first_investigation: a.ideas[0]?.id ?? '',
      first_prototype: a.firstPrototype,
      investigations: a.ideas.map((i) => i.id),
      phase1_start_week: a.startWeek,
      phase1_end_week: a.endWeek,
      phase1_start: a.startWeek ? iso(weekStart(a.startWeek)) : '',
      phase1_end: a.endWeek ? iso(weekEnd(a.endWeek)) : '',
      take_leads_to: a.takeTo,
      phase2_data_ask: phase2Ask(a.slug)?.data.replace(/\*\*/g, '') ?? '',
      stage: stageOf(a.slug),
      lead_packages: mine.reduce((n, f) => n + f.leads, 0),
      savings_identified_usd: mine.length ? sum(a.slug, 'identifiedUsd') : 'Pending',
      savings_confirmed_usd: mine.some((f) => f.confirmedUsd) ? sum(a.slug, 'confirmedUsd') : 'Pending',
    };
  });
}
