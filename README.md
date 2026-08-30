# Replication package — Memory Design in LLM Agents: A Systematic Mapping Study

Everything behind the paper: the protocol that predates the search, every
screening and classification decision with its written justification, the two
reliability computations, the database, and the scripts that regenerate every
number and figure from it.

The study maps **66** primary studies on memory mechanisms in LLM-based agents,
drawn from 7,032 records returned by arXiv and OpenAlex on 30 August 2026.

## The short version

```bash
scripts/verify.sh
```

This regenerates every number in the paper from `data/phd.sqlite` and then checks
each one **independently** — the verifier expresses its queries separately from
the generator, because one expression checked against itself only proves it is
self-consistent. It exits non-zero on a mismatch, and also on any number used in
the paper that it could not check. An unchecked number is a failure, not a skip.

It needs `python3` and the `phd` CLI (a small Go tool; source at
`cli/phd` in the project's tooling repository).

## Layout

| Path | What it is |
|---|---|
| `protocol.md` | The complete decision log: study design, research questions, all 11 screening criteria, the facet scheme, and every amendment with its timestamp and reason. |
| `data/phd.sqlite` | The study database — 3,862 identified records, 379 screening decisions, 507 facet assignments, 201 logged decisions. This project only. |
| `data/screening.csv` | Every screened record with the abstract it was judged from, the decision, the decision rule, and the written reason. |
| `data/classification.json` | Every classified paper: which pages its coder was given, the eligibility call, and each facet assignment with its justification. |
| `data/second-coding.json` | The independent second coder's output for the reliability sample. |
| `data/facet-kappa.json`, `data/test-retest.json` | The two reliability computations, with every disagreement listed in full. |
| `data/text-integrity.json` | The title-against-extracted-text check run over the whole gated corpus. |
| `data/search-strings.json` | All 18 queries, the providers, the year floor and the per-run fetch cap. |
| `data/runs/` | The raw provider responses for each (query, provider) run. |
| `data/facts.json` | Every number that appears in the paper. |
| `data/map.json` | The cross-tabulations behind the figures, including the empty cells. |
| `data/grey-candidates.json` | Output of the **withdrawn** grey-stratum frame rule, released so the withdrawal can be checked rather than taken on trust. |
| `guides/` | The screening and classification guides the coders worked from, verbatim. |
| `scripts/` | The pipeline, in execution order. `verify.sh` is the entry point. |
| `figures/` | The map figures and the PRISMA flow, as published. |
| `prisma.md`, `prisma-checklist.md` | The generated PRISMA 2020 flow and the completed 27-item + 12-item checklists. |

## What is deliberately not here

**No full text.** The study fetched PDFs and extracted page text to code from;
neither is redistributed. `classification.json` records which pages were supplied
to each coder, so the same pages can be re-extracted from the sources.

Nine records arrived from OpenAlex with full body text in their abstract field.
Those nine are truncated to 5,000 characters in the shipped database, with a
marker. No other record is altered.

**No practitioner stratum.** RQ4 was declared in the protocol and withdrawn
during execution; `grey-candidates.json` and the amendment in `protocol.md` show
why.

## Reading the study honestly

Two things a reader should weigh before using these numbers.

**Coverage.** 34 of 36 search runs returned exactly their fetch cap, so the
corpus is a relevance-ranked slice of a larger match set rather than a census.
Eighteen overlapping queries mitigate this and two seeded random draws make the
sampling defensible, but the map does not claim completeness. The protocol
committed to three search strategies and only the database search was executed.

**Who coded.** Screening, full-text eligibility and every facet assignment were
produced by LLM agents working from the guides in `guides/`. Each decision
records its author and its rationale, and agreement was measured rather than
assumed: test–retest on the screening pilot at κ = 0.9561, and an independent
second coder on 20% of the classified corpus at κ = 0.81–1.00 per axis. Those
figures are in `test-retest.json` and `facet-kappa.json` with every disagreement
listed.

## Licence

Code under `scripts/` is MIT. The study's own products — protocol, guides,
decisions, justifications, derived counts — are CC BY 4.0. Bibliographic metadata
and abstracts of the reviewed papers remain their sources' and are reproduced
under the terms of arXiv and OpenAlex. See `LICENSE`.
