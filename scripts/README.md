# Scripts

Two kinds of script live here, and the difference matters.

## Runnable against this repository

These read `../data` and regenerate the study's outputs. Start with `verify.sh`.

| Script | Does |
|---|---|
| `verify.sh` | Regenerates every number, then re-checks each one independently. Fails on a mismatch **and** on any number it cannot check. |
| `100-facts.py` | Generates `data/facts.json` and `data/facts.tex` from the database and the decision files. |
| `101-verify.py` | Recomputes each fact by a separate route and compares. Deliberately does not import from `100-facts.py`. |
| `80-make-map.py` | Rebuilds `data/map.json`, the cross-tabulations behind the figures. |
| `92-facet-kappa.py` | Recomputes per-axis inter-coder agreement from the coding and re-coding files. |
| `44-test-retest.py` | Recomputes the screening test–retest agreement. |
| `102-prisma.py` | Regenerates the PRISMA flow into `../figures`. |
| `105-figures.py` | Regenerates the map figures into `../figures`. |
| `35-text-integrity.py` | Re-runs the title-against-extracted-text check. Needs the extracted text, which is not redistributed, so it will report nothing here. |

## As-executed, kept for provenance

These are the scripts that produced the study. They ran against a working tree
that held the fetched PDFs and their extracted text, neither of which is
redistributed, so they will not run unchanged here. They are published because
the method is the claim: `00-protocol.sh` shows exactly what was declared before
the first search, and `10-search.sh` shows exactly what was queried.

`00-protocol.sh` · `10-search.sh` · `11-capture-text.sh` · `20-scope-filter.py` ·
`30-fetch-text.py` · `40-build-screening-batches.py` · `45-ingest-screening.py` ·
`46-collect-includes.py` · `50-build-classification-batches.py` ·
`60-grey-frame.py` · `70-ingest-facets.py` · `71-ingest-eligibility.py`

`20-scope-filter.py --selftest` runs standalone: it exercises the scope filter
against its borderline test cases without touching any data.
