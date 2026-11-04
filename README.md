# fed_fraud

Extends the SBA fraud work across the federal government, starting with the
agencies in the federal fraud initiative (america.gov/fraud).

- [Working plan](docs/plan.md)
- [Partner agencies: briefs and ranking (the original eight)](docs/agencies/landscape.md)
- [Top 33 agencies by budget: briefs and ranking](docs/agencies/top33.md)
- [Every federal agency: coverage plan beyond the top 33](docs/universe/all_agencies.md)
  (137 bodies, universal screens U1-U8, shared screens C4-C7, new idea IDs)
- [Forensic methods handbook](docs/playbook/forensic_methods.md): the mathematics
  behind each fraud test, with a tested reference implementation in
  [`analytics/`](analytics/README.md)
- [Ten extensions](docs/extensions.md): cross-agency matching, network
  scoring, the ROI model, a 90-day pilot kit, the policy and legal track,
  procurement fraud, grants to states, a live demo on public data, tip
  triage and a red-team playbook
- [The Geodesic Accountability Office website (Astro)](site/README.md): scorecard, agency plans,
  five-page roadmap and research library, built from `docs/`

## PDF versions

Every Markdown file under `docs/` has a LaTeX source (`.tex`) and a compiled
PDF next to it, for example [docs/plan.pdf](docs/plan.pdf). They use the
Classic report template (`detailed_1_classic`) from
`proposal_gen/templates/detailed_proposal_template`, set in Latin Modern.
The plan, review plan, roadmap, `landscape`, `top33`, the all-agency plan
and the forensic methods handbook get the full title page and contents; the
agency briefs get a compact one-page header in the same style.

The Markdown stays the source. After editing it, rebuild with
`latex/build.sh` (all files) or `latex/build.sh docs/agencies/hhs.md` (one).
It needs pandoc and pdflatex (TeX Live with `texlive-latex-extra` and
`lmodern`). The Geodesic brand kit it uses is copied into
`latex/geodesic_brand/`.
