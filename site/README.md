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
npm run build    # static output in site/dist/
```

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
5. **Research library** (`/library/`): placeholder pages for methodology,
   research, detailed plans and per-agency results, to be filled in later.
6. **Downloads** (`/downloads/`): a PDF brief per agency plus the roadmap,
   review plan, ranking and working plan PDFs (served from `../docs`).

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
