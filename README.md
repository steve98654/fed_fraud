# fed_fraud

Extends the SBA fraud work across the federal government, starting with the
agencies in the federal fraud initiative (america.gov/fraud).

- [Working plan](docs/plan.md)
- [Partner agencies: briefs and ranking (the original eight)](docs/agencies/landscape.md)
- [Top 33 agencies by budget: briefs and ranking](docs/agencies/top33.md)

## PDF versions

Every Markdown file under `docs/` has a LaTeX source (`.tex`) and a compiled
PDF next to it, for example [docs/plan.pdf](docs/plan.pdf). They use the
Classic report template (`detailed_1_classic`) from
`proposal_gen/templates/detailed_proposal_template`, set in Latin Modern.
The plan, `landscape` and `top33` get the full title page and contents; the
agency briefs get a compact one-page header in the same style.

The Markdown stays the source. After editing it, rebuild with
`latex/build.sh` (all files) or `latex/build.sh docs/agencies/hhs.md` (one).
It needs pandoc and pdflatex (TeX Live with `texlive-latex-extra` and
`lmodern`). The Geodesic brand kit it uses is copied into
`latex/geodesic_brand/`.
