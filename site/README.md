# Federal Fraud Scorecard site

Astro site that presents the fraud work: a GAO-style report layout with
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
4. **Research library** (`/library/`): placeholder pages for methodology,
   research, detailed plans and per-agency results, to be filled in later.

## Where the content comes from

The site reads the Markdown in `../docs` at build time, so editing a brief,
`docs/agencies/top33.md` or `docs/roadmap.md` and rebuilding updates the
site. Only two files are edited by hand:

- `src/data/scorecard.ts`: delivered findings and savings. **It is empty on
  purpose.** No savings have been found yet, so every savings figure shows
  "Pending". Add a finding only after its screen passes validation and its
  lead package clears counsel review.
- `src/data/library.ts`: the section 4 placeholder documents and outlines.
