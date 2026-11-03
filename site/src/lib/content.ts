// Reads the planning documents in ../docs at build time, so the site always
// shows what is committed in the repo. Markdown stays the source of truth.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { Marked } from 'marked';
import katex from 'katex';

const DOCS = path.resolve(process.cwd(), '..', 'docs');
export const REPO = 'https://github.com/steve98654/fed_fraud';
const BLOB = `${REPO}/blob/main/docs`;

const BASE = import.meta.env.BASE_URL.replace(/\/?$/, '/');
/** Prefix a site path with the configured base. */
export const url = (p = '') => BASE + p.replace(/^\//, '');

const read = (rel: string) => fs.readFileSync(path.join(DOCS, rel), 'utf8');

/**
 * Date (YYYY-MM-DD) the newest of the given docs/ files last changed, from git
 * history. Falls back to file modification time when git history is missing,
 * e.g. in a shallow clone. Deploy builds should fetch full history.
 */
export function lastUpdated(...rels: string[]): string {
  const dates = rels.map((rel) => {
    const file = path.join(DOCS, rel);
    try {
      const out = execFileSync('git', ['log', '-1', '--format=%cs', '--', file], {
        cwd: DOCS,
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'ignore'],
      }).trim();
      if (out) return out;
    } catch {
      /* not a git checkout */
    }
    return fs.statSync(file).mtime.toISOString().slice(0, 10);
  });
  return dates.sort().at(-1)!;
}

// ---------------------------------------------------------------------------
// Markdown rendering with repo links rewritten to site routes.
// ---------------------------------------------------------------------------
const marked = new Marked({ gfm: true });

export const slugify = (s: string) =>
  s.toLowerCase().replace(/&[a-z]+;/g, '').replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

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
  if (rel === 'pitches/README.md' || rel === 'pitches') return url('pitches/') + anchor;
  const pitch = rel.match(/^pitches\/([a-z]+-\d+)\.md$/);
  if (pitch) return url(`pitches/${pitch[1]}/`) + anchor;
  if (rel === 'playbook/methodology.md') return url('library/methodology/') + anchor;
  if (rel === 'playbook/sba-case-study.md') return url('case-study/sba/') + anchor;
  if (rel === 'playbook/forensic_methods.md') return url('library/forensic-methods/') + anchor;
  if (rel === 'universe/all_agencies.md' || rel === 'universe') return url('universe/') + anchor;
  return `${BLOB}/${rel}${anchor}`;
}

// TeX math ($...$ inline, $$...$$ display) for docs that opt in. The inline
// rule mirrors pandoc's, so the site and the PDF agree on what is math: the
// opening $ is followed by a non-space, the closing $ follows a non-space and
// is not followed by a digit (so "$5,000 to $9,000" stays plain text).
const MATH_DISPLAY = /\$\$([\s\S]+?)\$\$/g;
const MATH_INLINE = /\$(?=\S)([^$\n]+?)(?<=\S)\$(?!\d)/g;

function protectMath(src: string): { text: string; restore: (html: string) => string } {
  const blocks: string[] = [];
  const keep = (tex: string, display: boolean) => {
    blocks.push(katex.renderToString(tex.trim(), { displayMode: display, throwOnError: false }));
    return `MATHPH${blocks.length - 1}X`;
  };
  const text = src
    .replace(MATH_DISPLAY, (_, tex) => `\n\n${keep(tex, true)}\n\n`)
    .replace(MATH_INLINE, (_, tex) => keep(tex, false));
  const restore = (html: string) =>
    html
      .replace(/<p>MATHPH(\d+)X<\/p>/g, (_, i) => `<div class="math-display">${blocks[+i]}</div>`)
      .replace(/MATHPH(\d+)X/g, (_, i) => blocks[+i]);
  return { text, restore };
}

export function md(src: string, fromDir = '', opts: { math?: boolean } = {}): string {
  const seen = new Set<string>();
  const m = opts.math ? protectMath(src) : undefined;
  const parsed = marked.parse(m ? m.text : src, { async: false }) as string;
  const html = m ? m.restore(parsed) : parsed;
  return html
    .replace(/href="([^"]+)"/g, (_, h) => {
      const out = rewriteHref(h, fromDir);
      const ext = /^https?:/.test(out) ? ' target="_blank" rel="noopener"' : '';
      return `href="${out}"${ext}`;
    })
    .replace(/>([a-z]+)\.md<\/a>/g, (all, slug) => (SHORT[slug] ? `>${SHORT[slug]}</a>` : all))
    .replace(/<table>/g, '<div class="table-wrap"><table>')
    .replace(/<\/table>/g, '</table></div>')
    .replace(/<h([23])>([\s\S]*?)<\/h\1>/g, (_, lvl, inner) => {
      const base = slugify(inner.replace(/<[^>]+>/g, '')) || 'section';
      let id = base;
      for (let n = 2; seen.has(id); n++) id = `${base}-${n}`;
      seen.add(id);
      return `<h${lvl} id="${id}">${inner}</h${lvl}>`;
    });
}

/** Level-2 headings (with ids) in rendered HTML, for an "On this page" list. */
export function toc(html: string): { id: string; label: string }[] {
  return [...html.matchAll(/<h2 id="([^"]+)">([\s\S]*?)<\/h2>/g)].map((m) => ({
    id: m[1],
    label: m[2].replace(/<[^>]+>/g, '').replace(/&amp;/g, '&').replace(/^\d+\.\s*/, ''),
  }));
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

// ---------------------------------------------------------------------------
// Long-form documents: one-page pitches (docs/pitches/) and the playbook
// (docs/playbook/). Each is split into its level-2 sections.
// ---------------------------------------------------------------------------
export interface Doc {
  title: string;
  /** Rendered paragraph(s) between the title and the first section. */
  meta: string;
  /** Plain-text status line, if the intro has one. */
  status: string;
  sections: { heading: string; id: string; html: string; src: string }[];
}

export function doc(rel: string): Doc {
  const src = read(rel);
  const dir = path.posix.dirname(rel);
  const title = src.match(/^# (.+)$/m)?.[1].trim() ?? rel;
  const body = src.replace(/^# .+\n/, '');
  const first = body.search(/^## /m);
  const intro = (first < 0 ? body : body.slice(0, first)).trim();
  const rest = first < 0 ? '' : body.slice(first);
  const math = src.includes('$$');
  const sections = rest
    .split(/^## /m)
    .filter(Boolean)
    .map((chunk) => {
      const nl = chunk.indexOf('\n');
      const heading = chunk.slice(0, nl).trim();
      const s = chunk.slice(nl + 1).trim();
      return { heading, id: slugify(heading), html: md(s, dir, { math }), src: s };
    });
  return {
    title,
    meta: md(intro, dir),
    status: intro.match(/\*\*Status:\*\* ([^\n]+(?:\n(?!\n)[^\n]+)*)/)?.[1].replace(/\n/g, ' ') ?? '',
    sections,
  };
}

export const docExists = (rel: string) => fs.existsSync(path.join(DOCS, rel));

/** The one-page pitch for a roadmap idea, e.g. "HHS-1". */
export const pitchPath = (id: string) => `pitches/${id.toLowerCase()}.md`;
export const hasPitch = (id: string) => docExists(pitchPath(id));

// ---------------------------------------------------------------------------
// Review plan pieces used by the agency leave-behinds: what each agency's
// Phase 1 review delivers, and what we ask the agency for in Phase 2.
// ---------------------------------------------------------------------------
export interface Ask {
  /** Agencies the row covers, as written in the review plan. */
  label: string;
  data: string;
  enables: string;
  route: string;
}

/** Phase 2 table labels to brief slugs (rows can cover several agencies). */
const ASK_LABEL: Record<string, string> = {
  ...ROADMAP_LABEL,
  DOE: 'doe', DOL: 'dol', ED: 'ed', 'DOJ grants': 'doj',
};

let askCache: Map<string, Ask> | undefined;

/** The Phase 2 internal data request for an agency ("Agency ideas" table). */
export function phase2Ask(slug: string): Ask | undefined {
  if (!askCache) {
    askCache = new Map();
    const src = read('review_plan.md');
    const start = src.indexOf('#### Agency ideas');
    const block = src.slice(start, src.indexOf('\n#### ', start + 1));
    for (const [label, data, enables, route] of tableRows(block)) {
      for (const part of label.split(',').map((s) => s.trim())) {
        const s = ASK_LABEL[part];
        if (s) askCache.set(s, { label, data, enables, route });
      }
    }
  }
  return askCache.get(slug);
}

/**
 * What an agency's Phase 1 review delivers: the "Deliver" bullet for the deep
 * dives, or the short review plan paragraph (without its "Take to" line) for
 * the pilots and shared screens.
 */
export function deliverable(slug: string): { when: string; text: string } | undefined {
  const src = read('review_plan.md');
  const at = src.indexOf(`[Brief](agencies/${slug}.md)`);
  if (at < 0) return undefined;
  const end = src.slice(at).search(/\n#{2,5} /);
  const part = src.slice(at, end < 0 ? undefined : at + end).trim();
  const bold = part.replace(/\n(?!- )/g, ' ').match(/\*\*Deliver \(([^)]+)\)\.\*\*\s*(.+)/);
  if (bold) return { when: bold[1], text: bold[2].replace(/\s+/g, ' ').trim() };
  const body = part
    .replace(/\s+/g, ' ')
    .replace(/^\[Brief\]\([^)]+\)\.\s*Rank \d+, score [\d.]+\.\s*(?:[^.]*?weeks? [\d-]+\.\s*)?/, '')
    .replace(/^Weeks? [\d-]+\.\s*/, '')
    .replace(/\s*Take to [^.]+\.\s*$/, '')
    .trim();
  if (!body || body.startsWith('-')) return undefined;
  const when = body.match(/\b(?:Deliver(?:ed)?|delivered)\b[^.]*?\b(weeks? \d+(?:-\d+)?)/)?.[1] ?? '';
  return { when, text: body.replace(/\s*Deliver in weeks? \d+(?:-\d+)?\.$/, '') };
}

/** Brief sections by heading, for layouts that pick sections individually. */
export function briefSections(slug: string): Map<string, string> {
  return sections(read(`agencies/${slug}.md`).replace(/^# .+\n/, ''));
}

/** Absolute path of a file in ../docs, for endpoints that serve it. */
export const docPath = (rel: string) => path.join(DOCS, rel);

// ---------------------------------------------------------------------------
// Change log for the "What's new" page, from git history of docs/ and site/.
// Empty when git history is missing (e.g. a shallow clone without history).
// ---------------------------------------------------------------------------
export interface Change {
  hash: string;
  date: string;
  title: string;
  pr?: number;
  /** Agency slugs whose brief changed. */
  agencies: string[];
  docs: string[];
  site: boolean;
}

export function changes(limit = 60): Change[] {
  let out = '';
  try {
    out = execFileSync('git', ['log', `-${limit}`, '--format=@@%h|%cs|%s', '--name-only', '--', 'docs', 'site'], {
      cwd: path.resolve(DOCS, '..'),
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'ignore'],
    });
  } catch {
    return [];
  }
  return out
    .split('@@')
    .filter(Boolean)
    .map((chunk) => {
      const [head, ...files] = chunk.trim().split('\n').filter(Boolean);
      const [hash, date, ...rest] = head.split('|');
      const subject = rest.join('|');
      const pr = subject.match(/\(#(\d+)\)\s*$/)?.[1];
      const agencySet = new Set<string>();
      const docSet = new Set<string>();
      for (const f of files) {
        const ag = f.match(/^docs\/agencies\/([a-z]+)\.md$/);
        if (ag && SHORT[ag[1]]) agencySet.add(ag[1]);
        else if (/^docs\/.+\.md$/.test(f) && !f.startsWith('docs/agencies/')) docSet.add(f.replace(/^docs\//, ''));
      }
      return {
        hash,
        date,
        title: subject.replace(/\s*\(#\d+\)\s*$/, ''),
        pr: pr ? Number(pr) : undefined,
        agencies: [...agencySet],
        docs: [...docSet],
        site: files.some((f) => f.startsWith('site/')),
      };
    });
}

// ---------------------------------------------------------------------------
// All federal bodies (docs/universe/data/all_agencies.csv), built by
// analytics/universe/build_universe.py.
// ---------------------------------------------------------------------------
export interface Body {
  abbreviation: string;
  name: string;
  kind: string;
  inUsaspending: string;
  outlaysUsd: number | null;
  tier: 'A' | 'B' | 'C' | 'D' | 'X';
  coverage: string;
  ideaIds: string;
  brief: string;
  notes: string;
}

function parseCsv(text: string): string[][] {
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') {
        cell += '"';
        i++;
      } else if (c === '"') quoted = false;
      else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === ',') {
      row.push(cell);
      cell = '';
    } else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(cell);
      rows.push(row);
      row = [];
      cell = '';
    } else cell += c;
  }
  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }
  return rows;
}

export function federalBodies(): Body[] {
  const [head, ...rows] = parseCsv(read('universe/data/all_agencies.csv'));
  return rows
    .filter((r) => r.length === head.length)
    .map((r) => {
      const o = Object.fromEntries(head.map((h, i) => [h, r[i]]));
      return {
        abbreviation: o.abbreviation,
        name: o.name,
        kind: o.kind,
        inUsaspending: o.in_usaspending,
        outlaysUsd: o.outlays_usd ? Number(o.outlays_usd) : null,
        tier: o.tier as Body['tier'],
        coverage: o.coverage,
        ideaIds: o.idea_ids,
        brief: o.brief,
        notes: o.notes,
      };
    });
}
