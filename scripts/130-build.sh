#!/usr/bin/env bash
# One command from data to PDF. Every stage refuses to proceed on a defect the
# next stage would hide.
set -euo pipefail
cd "$(dirname "$0")"

echo "== regenerate facts from the database"
python3 100-facts.py

echo "== verify every fact independently (fails on a mismatch OR an unchecked fact)"
python3 101-verify.py > verify.log || { tail -30 verify.log; exit 1; }
tail -1 verify.log

echo "== regenerate the PRISMA flow from the same facts"
python3 102-prisma.py

echo "== regenerate the map figures from the same data"
python3 105-figures.py

echo "== sync facts into the manuscript"
cp facts.tex ../../docs/manuscript-agentmem/facts.tex

echo "== build"
cd ../../docs/manuscript-agentmem
dot -Tpdf prisma.dot -o prisma.pdf
pdflatex -interaction=nonstopmode main.tex >/dev/null
bibtex main >/dev/null 2>&1 || true
pdflatex -interaction=nonstopmode main.tex >/dev/null
pdflatex -interaction=nonstopmode main.tex > build.log 2>&1

und=$(grep -ci "undefined" build.log || true)
if [ "$und" != "0" ]; then
  echo "FAIL: $und undefined references or citations"
  grep -i "undefined" build.log | head -20
  exit 1
fi
pages=$(pdfinfo main.pdf | awk '/^Pages/{print $2}')
echo "built main.pdf, $pages pages, no undefined references"
