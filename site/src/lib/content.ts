// Reads the planning documents in ../docs at build time, so the site always
// shows what is committed in the repo. Markdown stays the source of truth.
import fs from 'node:fs';
import path from 'node:path';
import { Marked } from 'marked';

const DOCS = path.resolve(process.cwd(), '..', 'docs');
export const REPO = 'https://github.com/steve98654/fed_fraud';
const BLOB = `${REPO}/blob/main/docs`;

const BASE = import.meta.env.BASE_URL.replace(/\/?$/, '/');
/** Prefix a site path with the configured base. */
export const url = (p = '') => BASE + p.replace(/^\//, '');

const read = (rel: string) => fs.readFileSync(path.join(DOCS, rel), 'utf8');

// ---------------------------------------------------------------------------
// Markdown rendering with repo links rewritten to site routes.
// ---------------------------------------------------------------------------
const marked = new Marked({ gfm: true });

/** Map a relative .md link found in `fromDir` (relative to docs/) to a URL. */
function rewriteHref(href: string, fromDir: string): string {
  if (/^(https?:|mailto:|#)/.test(href)) return href;
  const [file, hash = ''] = href.split('#');
  const rel = path.posix.normalize(path.posix.join(fromDir, file));
  const anchor = hash ? `#${hash}` : '';
  if (rel === 'agencies/top33.md' || rel === 'agencies') return url('agencies/') + anchor;
  const agency = rel.match(/^agencies\/([a-z]+)\.md$/);
  if (agency && agency[1] !== 'landscape') return url(`agencies/${agency[1]}/`) + anchor;
  if (rel === 'roadmap.md') return url('plan/') + anchor;
  return `${BLOB}/${rel}${anchor}`;
}

export function md(src: string, fromDir = ''): string {
  const html = marked.parse(src, { async: false }) as string;
  return html
    .replace(/href="([^"]+)"/g, (_, h) => {
      const out = rewriteHref(h, fromDir);
      const ext = /^https?:/.test(out) ? ' target="_blank" rel="noopener"' : '';
      return `href="${out}"${ext}`;
    })
    .replace(/>([a-z]+)\.md<\/a>/g, (all, slug) => (SHORT[slug] ? `>${SHORT[slug]}</a>` : all))
    .replace(/<table>/g, '<div class="table-wrap"><table>')
    .replace(/<\/table>/g, '</table></div>');
}

export const mdInline = (src: string, fromDir = '') =>
  md(src, fromDir).replace(/^<p>|<\/p>\s*$/g, '');

/** Split markdown into sections keyed by heading text (levels 2 and 3). */
export function sections(src: string): Map<string, string> {
  const out = new Map<string, string>();
  let key = '_intro';
  let buf: string[] = [];
  for (const line of src.split('\n')) {
    const h = line.match(/^#{2,3} (.+)$/);
    if (h) {
      out.set(key, buf.join('\n').trim());
      key = h[1].trim();
      buf = [];
    } else buf.push(line);
  }
  out.set(key, buf.join('\n').trim());
  return out;
}

function tableRows(block: string): string[][] {
  return block
    .split('\n')
    .filter((l) => l.startsWith('|') && !/^\|\s*-/.test(l))
    .slice(1)
    .map((l) =>
      l
        .replace(/^\|/, '')
        .replace(/\|\s*$/, '')
        .split(' | ')
        .map((c) => c.trim()),
    );
}

// ---------------------------------------------------------------------------
// Phase 1 calendar: week 1 starts Monday 2026-11-02 and the holiday break
// (2026-12-21 to 2027-01-01) is skipped.
// ---------------------------------------------------------------------------
export function weekStart(n: number): Date {
  const d = new Date(Date.UTC(2026, 10, 2 + 7 * (n - 1)));
  if (d >= new Date(Date.UTC(2026, 11, 21))) d.setUTCDate(d.getUTCDate() + 14);
  return d;
}
export function weekEnd(n: number): Date {
  const d = weekStart(n);
  d.setUTCDate(d.getUTCDate() + 4);
  return d;
}
export const fmtDate = (d: Date | string) =>
  new Date(typeof d === 'string' ? `${d}T12:00:00Z` : d).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    timeZone: 'UTC',
  });

// ---------------------------------------------------------------------------
// Agencies: ranking (top33.md), budget (CSV), ideas (roadmap.md), briefs.
// ---------------------------------------------------------------------------
export interface Idea {
  id: string;
  text: string;
}
export interface Agency {
  slug: string;
  name: string;
  short: string;
  rank: number;
  budgetRank: number;
  outlaysB: number;
  outlaysUsd: number;
  factors: { exposure: number; data: number; fit: number; action: number };
  score: number;
  firstPrototype: string;
  group: string;
  ideas: Idea[];
  when: string;
  takeTo: string;
  startWeek: number;
  endWeek: number;
  startFirst: boolean;
}

/** Roadmap row labels to brief slugs. */
const ROADMAP_LABEL: Record<string, string> = {
  HHS: 'hhs', DoD: 'dod', SBA: 'sba', DHS: 'dhs', USDA: 'usda', DOT: 'dot', GSA: 'gsa',
  FCC: 'fcc', VA: 'va', OPM: 'opm', Commerce: 'doc', PBGC: 'pbgc', Energy: 'doe',
  USACE: 'usace', EPA: 'epa', HUD: 'hud', State: 'state', NASA: 'nasa', NSF: 'nsf',
  Justice: 'doj', SEC: 'sec', USAID: 'usaid', DFC: 'dfc', AmeriCorps: 'cncs',
  PCORTF: 'pcortf', NRC: 'nrc', EOP: 'eop', Treasury: 'treasury', SSA: 'ssa',
  Education: 'ed', Labor: 'dol', FDIC: 'fdic', Interior: 'doi',
};
export const SHORT: Record<string, string> = Object.fromEntries(
  Object.entries(ROADMAP_LABEL).map(([k, v]) => [v, k]),
);

export const GROUPS = [
  'Wave 1 and Wave 2 deep dives (weeks 3 to 10)',
  'Contained pilots (weeks 7 to 11)',
  'Shared screens (weeks 9 to 13)',
  'Aggregate screens and access cases (weeks 10 to 14)',
];
export const groupLabel = (g: string) => g.replace(/ \(.*\)$/, '');

let cache: Agency[] | undefined;

export function agencies(): Agency[] {
  if (cache) return cache;
  const top = sections(read('agencies/top33.md'));
  const csv = read('agencies/data/top33_fy2026.csv').trim().split('\n').slice(1);
  const outlays = new Map(
    csv.map((l) => {
      const c = l.split(',');
      return [c[c.length - 1].replace('.md', ''), Number(c[c.length - 3])];
    }),
  );

  const road = sections(read('roadmap.md'));
  const ideaRows = new Map<string, { group: string; cell: string }>();
  for (const g of GROUPS) {
    for (const [label, cell] of tableRows(road.get(g) ?? '')) {
      const slug = ROADMAP_LABEL[label];
      if (slug) ideaRows.set(slug, { group: g, cell });
    }
  }
  const startFirst = new Set(
    tableRows(road.get('The ten investigations to start first') ?? '').map((r) => r[1]),
  );

  cache = tableRows(top.get('Ranking') ?? '').map((r) => {
    const link = r[1].match(/\[(.+)\]\(([a-z]+)\.md\)/)!;
    const slug = link[2];
    const row = ideaRows.get(slug);
    const cell = row?.cell ?? '';
    const ideas = [...cell.matchAll(/\*\*([A-Z]+-\d+)\*\*\s*(.+?)(?=\s*\*\*[A-Z]+-\d+\*\*|\s*\*Rank|$)/g)].map(
      (m) => ({ id: m[1], text: m[2].trim().replace(/^[a-z]/, (c) => c.toUpperCase()) }),
    );
    const meta = cell.match(/\*Rank \d+; (.+?); take to (.+?)\.?\*\s*$/);
    const weeks = (meta?.[1] ?? '').match(/weeks? (\d+)(?:-(\d+))?/);
    return {
      slug,
      name: link[1],
      short: SHORT[slug] ?? slug.toUpperCase(),
      rank: Number(r[0]),
      budgetRank: Number(r[2]),
      outlaysB: Number(r[3].replace(/,/g, '')),
      outlaysUsd: outlays.get(slug) ?? 0,
      factors: { exposure: +r[4], data: +r[5], fit: +r[6], action: +r[7] },
      score: Number(r[8].replace(/\*/g, '')),
      firstPrototype: r[9],
      group: row?.group ?? '',
      ideas,
      when: meta?.[1] ?? '',
      takeTo: meta?.[2] ?? '',
      startWeek: weeks ? Number(weeks[1]) : 0,
      endWeek: weeks ? Number(weeks[2] ?? weeks[1]) : 0,
      startFirst: ideas.some((i) => startFirst.has(i.id)),
    };
  });
  return cache;
}

export interface Brief {
  html: string;
  bottomLine: string;
  meta: string;
}

export function brief(slug: string): Brief {
  const src = read(`agencies/${slug}.md`).replace(/^# .+\n/, '');
  const metaEnd = src.indexOf('\n## ');
  const meta = src.slice(0, metaEnd).trim();
  const body = src.slice(metaEnd).trim();
  const s = sections(body);
  return {
    html: md(body.replace(/^## Bottom line\n[\s\S]*?(?=\n## )/, '').trim(), 'agencies'),
    bottomLine: (s.get('Bottom line') ?? '').split('\n\n')[0].replace(/\n/g, ' '),
    meta: md(meta, 'agencies'),
  };
}

// ---------------------------------------------------------------------------
// Roadmap pieces used by the five plan pages and the scorecard.
// ---------------------------------------------------------------------------
export function roadmap() {
  const s = sections(read('roadmap.md'));
  const intro = s.get('_intro') ?? '';
  const status = intro.match(/\*\*Status:\*\* (.+)/)?.[1] ?? '';
  return {
    status,
    get: (k: string) => s.get(k) ?? '',
    startFirst: tableRows(s.get('The ten investigations to start first') ?? '').map((r) => ({
      n: r[0], id: r[1], title: r[2], scheme: r[3], weeks: r[4], takeTo: r[5],
    })),
    crossAgency: tableRows(s.get('Phase 2: what internal data adds') ?? '').map((r) => ({
      id: r[0], title: r[1], data: r[2], lead: r[3], target: r[4],
    })),
    milestones: tableRows(s.get('Milestones') ?? '').map((r) => ({ date: r[0], text: r[1] })),
  };
}

/** Prose before the first table in a markdown block. */
export const proseOnly = (block: string) => block.split('\n|')[0].trim();
