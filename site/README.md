# The Geodesic Accountability Office (site)

Astro site for The Geodesic Accountability Office, which presents the
federal fraud work: a GAO-style report layout with
Geodesic Solutions branding (palette and house footer from
`latex/geodesic_brand/geodesicbrand.sty`, logo and wordmark from the
Geodesic website).

## Develop

```sh
cd site
npm install
npm run dev      # http://localhost:4321
npm run build    # static output in site/dist/, plus the search index
npx astro preview   # serve dist/ to try search and print
npm run test:a11y   # axe-core WCAG 2.1 AA check of every built page
```

Search is built by [Pagefind](https://pagefind.app) after the Astro build, so
it works on built and deployed sites but not under `npm run dev`. The
accessibility check needs a Playwright Chromium (`npx playwright install
chromium`, once). Pull requests run both through `.github/workflows/site-check.yml`.

Hosting on Cloudflare Pages behind a password (`functions/_middleware.js`)
is set out step by step in [HOSTING.md](HOSTING.md).

## Polish

- **Search** (`/search/`, plus the box in the header) indexes page content,
  not the header or footer.
- **Print**: every page prints as a clean brief; agency pages have a "Print
  this plan" button. External links print with their URL.
- **Last updated** on each agency page is the newest git commit date of its
  brief, `docs/roadmap.md` and `docs/agencies/top33.md`.
- **Accessibility**: skip link, visible keyboard focus, reduced-motion
  support, and AA color contrast (`--gold-ink` is the gold for text).

- **Scorecard table**: click a column header to sort, type to filter, and
  the workstream filter is kept in the link (`/?group=contained-pilots`).
- **Keyboard**: press `/` to jump to search. Long pages get a back-to-top
  link, and headings in long-form pages get a copy-link `#` anchor.
- **On this page** contents on agency plans and the SBA case study.

To host under a subpath (for example GitHub Pages at `/fed_fraud/`), build
with `SITE_BASE=/fed_fraud/ npm run build`.

## Sections

1. **Scorecard** (`/`): one-page aggregate view of savings, Phase 1 progress
   and a 33-agency table.
2. **Agency plans** (`/agencies/<slug>/`): one page per agency, rendered from
   the briefs in `docs/agencies/` plus that agency's roadmap ideas.
3. **Roadmap** (`/plan/`): the five-page roadmap from `docs/roadmap.md`.
4. **Tool previews** (`/tools/`): wireframes of the detection screens for
   three of the first ten investigations (HHS-1 hospice, DOD-1 set-asides,
   USDA-1 SNAP retailers). Sample records only; defined in `src/data/tools.ts`
   and `src/components/tools/`.
5. **Explore** (header "More" menu): `/investigations/` (all 86 ideas plus
   the six cross-agency ideas, filterable), `/schedule/` (Gantt view of
   Phase 1 by agency), `/agencies/matrix/` (agencies by any two priority
   factors), `/agencies/compare/?a=hhs,dod,usda` (side-by-side comparison),
   `/glossary/` (terms, in `src/data/glossary.ts`) and `/updates/` (what's
   new, from git history; needs a full clone to show anything).
6. **Research library** (`/library/`): placeholder pages for methodology,
   research, detailed plans and per-agency results, to be filled in later.
7. **Every federal agency** (`/universe/`): all 137 federal bodies with
   tier, FY2026 outlays and screens, filterable by tier (`?tier=B`), plus
   the coverage plan from `docs/universe/all_agencies.md`. The register is
   `docs/universe/data/all_agencies.csv`, built by
   `analytics/universe/build_universe.py`.
8. **Forensic methods** (`/library/forensic-methods/`): the handbook from
   `docs/playbook/forensic_methods.md`. TeX math (`$...$`, `$$...$$`) is
   rendered with KaTeX at build time for docs that contain display math;
   the inline rule matches pandoc's, so the site and the PDF agree.
9. **Benford checker** (`/tools/benford/`): a working client-side prototype
   of universal screen U1. Pasted data never leave the browser.
10. **Downloads** (`/downloads/`): a PDF brief per agency, the roadmap,
   review plan, ranking, all-agency plan, forensic methods and working plan
   PDFs (served from `../docs`), the all-agency register as
   `/downloads/all_agencies.csv`, and the scorecard as `/downloads/scorecard.csv` and `.json`, built from
   `src/lib/scorecard.ts`. Savings columns read `Pending` until findings
   are recorded.

## Agency brief PDFs

Each agency has a printable leave-behind at `/briefs/<slug>/`, built from its
brief, roadmap ideas and review plan (including the Phase 2 data request).
The PDFs in `public/downloads/briefs/` are generated from those pages with
the Chromium that Playwright provides:

```sh
npm run build      # without SITE_BASE
npm run briefs     # all agencies, or: npm run briefs hhs dod
```

Rerun both after editing a brief, `docs/roadmap.md` or `docs/review_plan.md`,
and commit the updated PDFs.

## Where the content comes from

The site reads the Markdown in `../docs` at build time, so editing a brief,
`docs/agencies/top33.md` or `docs/roadmap.md` and rebuilding updates the
site. Only two files are edited by hand:

- `src/data/scorecard.ts`: delivered findings and savings. **It is empty on
  purpose.** No savings have been found yet, so every savings figure shows
  "Pending". Add a finding only after its screen passes validation and its
  lead package clears counsel review.
- `src/data/library.ts`: the section 4 placeholder documents and outlines.
