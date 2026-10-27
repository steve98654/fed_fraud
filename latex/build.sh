#!/bin/bash
# Convert the Markdown in docs/ to LaTeX and compile each to PDF.
# The .tex and .pdf land next to their .md source.
# Usage: latex/build.sh [docs/path.md ...]   (default: every .md under docs/)
# Needs pandoc and pdflatex (TeX Live with latex-extra and lmodern).
set -e
root="$(cd "$(dirname "$0")/.." && pwd)"
cd "$root"
export TEXINPUTS="$root/latex/geodesic_brand//:"
# Documents with a full title page and contents; everything else is a brief.
reports="docs/plan.md docs/review_plan.md docs/agencies/landscape.md docs/agencies/top33.md"
files=${@:-$(find docs -name '*.md' | sort)}
fail=0
for md in $files; do
  dir=$(dirname "$md"); base=$(basename "$md" .md)
  opts=""; case " $reports " in *" $md "*) ;; *) opts="-V brief";; esac
  pandoc "$md" -f markdown-implicit_figures -t latex --shift-heading-level-by=-1 \
    --template=latex/fed_report.latex --lua-filter=latex/filters.lua $opts \
    -o "$dir/$base.tex"
  if (cd "$dir" &&
      pdflatex -interaction=nonstopmode -halt-on-error "$base.tex" > /dev/null &&
      pdflatex -interaction=nonstopmode -halt-on-error "$base.tex" > /dev/null); then
    echo "ok    $dir/$base.pdf"
    rm -f "$dir/$base".{aux,log,out,toc}
  else
    echo "FAIL  $dir/$base.tex (see $dir/$base.log)"; fail=1
  fi
done
exit $fail
