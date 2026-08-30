# PRISMA 2020 Reporting Checklist — completed (re-audit)

Manuscript audited: `docs/manuscript-agentmem/main.tex` + `sections/{intro,method,results,discussion}.tex`
Flow data: `docs/manuscript-agentmem/prisma.md`, `prisma.dot`, `prisma.pdf`; numbers: `scripts/agentmem/facts.json` vs `docs/manuscript-agentmem/facts.tex`.

This is a systematic mapping study (Petersen 2008/2015), reported against PRISMA 2020 by the authors' own declaration (method.tex L3–4). Items with no mapping-study analog (RoB tool, effect measures, meta-analysis, GRADE certainty) are N/A with the paper's own justification cited. Every "Reported"/"Partial" row cites file + line. `facts.tex` was diffed key-by-key against `scripts/agentmem/facts.json` — no numeric mismatches, and the two facts previously computed-but-unused (`\factClassified`, `\factIneligible`) are now both used in prose (method.tex L149–150, main.tex L33). **The flow-diagram figure itself, however, has a count bug — see item 16a.**

## What changed since the last audit (verified against the diff, not taken on trust)

- Table I (screening criteria, I1–I4/E1–E7) — **added, confirmed** (method.tex L32–61). Fixes item 5.
- PRISMA flow figure — **added, confirmed**, but its "Drawn for classification" node is mislabeled (see item 16a). Partial fix.
- Eligibility subsection (79 assessed / 13 excluded / 66 eligible, with full-text exclusion reasons) — **added, confirmed**, but the reason counts don't sum to the stated total (see item 16b). Partial fix.
- Search date and query provenance — **added, confirmed** (`\factSearchDate` now used, method.tex L18). Fixes item 6.
- Synthesis subsection stating method in advance — **added, confirmed** (method.tex §Synthesis, L167–175). Fixes item 13d.
- "Screening was single-coder" statement — **added, confirmed**, explicit and unambiguous (method.tex L91–96). Fixes item 8.
- Data availability / Registration and protocol / Acknowledgements and disclosure — **added, confirmed** (main.tex L77–113). Fixes items 24, 25, 26, 27.
- Abstract eligibility chain — **added, confirmed** (main.tex L30–34), but this is a chain of *counts*, not a statement of *criteria*; item 3 (abstract) is **not** fixed by it.
- Abstract limitations clause — **added, confirmed** (main.tex L47–48). Fixes abstract item 9.

## Main checklist (27 items)

| # | Section / Topic | Status | Location |
|---|---|---|---|
| 1 | Title identifies systematic review | Reported | main.tex L17 |
| 2 | Abstract (structured summary) | Reported | see Abstract checklist below |
| 3 | Rationale in context of existing knowledge | Reported | intro.tex L11–20 |
| 4 | Explicit objectives/questions | Reported | intro.tex L22–32 (RQ1–RQ3), L34–37 (RQ4 withdrawal, dated and explained) |
| 5 | Eligibility criteria + synthesis grouping | Reported | Table I, method.tex L32–61 (I1–I4 include, E1–E7 exclude); grouping by six facets, intro.tex L41, method.tex L138–145 |
| 6 | Information sources + search date | Reported | method.tex L16–19: arXiv + OpenAlex named, `\factSearchDate` ("30 August 2026") now appears in prose |
| 7 | Full search strategy, all databases, filters/limits | Partial | method.tex L17–23 states 18 queries span four concept groups and are "reproduced verbatim in the replication package (Section~\ref{sec:availability})"; `replication/search-strings.json` exists on disk and the package is described as accompanying the submission as supplementary material (main.tex L79–81). Not verbatim inside the compiled manuscript itself — a reviewer without the supplementary bundle cannot see a single query string. |
| 8 | Selection process: reviewer count, independence, automation | Reported | method.tex L91–96: explicit — "Each record was screened once; there was no parallel double-screening of the full set," reliability instead rests on test–retest (L96–105) and second-coder pass at classification; the paper states plainly "That is weaker than dual review with adjudication, and we say so rather than implying otherwise" |
| 9 | Data collection process: reviewer count, independence, automation | Reported | method.tex L128–136 ("Each paper was read by one agent..."); Reliability subsection L160–165 (20% second-coded, independent, no access to first coding) |
| 10a | Data items — outcomes sought | Partial | Six facets named (intro.tex L41, method.tex L138–145), but category values within each facet are defined only in `replication/agentmem-classification-guide.md`, never reproduced or even summarized in the manuscript |
| 10b | Data items — other variables (characteristics) | Partial | Venue type is coded and reported (results.tex L111–116) but never pre-specified as a sought data item in Methods; no other paper-level characteristics (year, affiliation) are listed as sought variables anywhere |
| 11 | Study risk-of-bias assessment methods | N/A (disclosed) | method.tex L177–182: "quality assessment of primary studies is deliberately not performed... it costs a point on the DARE instrument and we accept that trade" — explicit, matches Petersen 2015's guidance for mapping studies |
| 12 | Effect measures | N/A | method.tex L5–7: "no outcome variable is comparable across the corpus... nothing can be aggregated" |
| 13 | Synthesis methods (eligibility for synthesis, data prep, tabulation, method+rationale stated in advance, heterogeneity, sensitivity) | Reported | Eligibility-for-synthesis: results.tex Fig. 1 caption L9–10 ($n=61$ of 66, 5 null-substrate excluded from both panels). Data prep: method.tex L134–136 (null-coding rule). Tabulation: results.tex Fig. 1/2, Table I. Method-stated-in-advance (**new**): method.tex §Synthesis L167–175 — descriptive counts/cross-tabs, empty cells reported not omitted, rule-of-three bound for zero cells, stated prospectively rather than surfacing only in Results. Heterogeneity/sensitivity: N/A, no pooled estimate exists (consistent with item 12). |
| 14 | Reporting-bias assessment methods | N/A | No meta-analytic synthesis exists for missing-result bias to attach to. The nearest analog — search-coverage limitation from cap-bound runs and a 2-library search — is disclosed as a *theoretical validity* threat (discussion.tex L72–81), which is the correct category, not item 14 |
| 15 | Certainty-of-evidence assessment methods | N/A | No GRADE-style certainty grading exists in a Petersen mapping method; correctly not addressed |
| 16a | Flow diagram, all counts | Partial — figure exists but a node count is wrong | Fig. 2 (results.tex L14–21, `fig:prisma`, `prisma.pdf`) is now included and referenced (results.tex L24). Cross-checked against `prisma.dot`/`facts.json` node by node: **the "Drawn for classification" box is labeled n = 79; `facts.json`/`facts.tex` gives `Drawn` = 80.** The true value 80 (the seeded draw) is never shown anywhere in the diagram — the box silently substitutes `Classified` (79, i.e. post-integrity-drop) for `Drawn`, and the −1 integrity-check drop is buried as a second line of text inside the adjacent "Not drawn (seeded sample)" exclusion box rather than shown as its own step. The prose gets this right (method.tex L147–150: 80 drawn, 1 dropped, 79 assessed) — only the figure disagrees with the database. All other diagram counts (7032/3862/2549/28/1285/300/985/192/108/171/21/91/13/66) match `facts.json` exactly. |
| 16b | Near-misses excluded, with reasons | Partial — reasons present, arithmetic doesn't reconcile | Screening stage: 108 exclusions broken down E5=27, E4=22, E6=20, E1=19, E3=14, E2=6, E7=3 (method.tex L106–111), with an explicit caveat "a decision may cite more than one criterion" — sums correctly account for double-counting. Full-text stage (**new**): method.tex L150–154 gives E3=7, I1=4, E5=2, E1=2 — **these sum to 15, but the stated total excluded at this stage is 13** (`\factIneligible`), and unlike the screening-stage sentence, **no caveat about multiple criteria per decision is given here.** Either two of these reason counts are wrong, the total is wrong, or the missing-multi-citation caveat needs to be added and explained — as written, the numbers do not reconcile and a careful reviewer will catch it. |
| 17 | Study characteristics cited | Not reported | `main.bbl` has 31 `\bibitem`s against 66 corpus papers in `corpus.bib`; no `\nocite{*}` for the corpus and only ~6–8 papers are named as illustrative examples (results.tex L41–51). The gap is now explicitly disclosed rather than silent — main.tex L92–95 states only named papers are cited "listing all 66 in the reference section would consume roughly two pages... without making any of them easier to find than the package already does" and redirects to `classification.json` + a BibTeX file in the replication package — but PRISMA item 17 asks for each included study to be cited in the report itself, and this manuscript explicitly declines to. Disclosure of a gap is not the same as closing it. No characteristics table (year, venue, facet values per paper) appears anywhere in the compiled document either. |
| 18 | Risk-of-bias per included study | N/A | Consistent with item 11 |
| 19 | Individual study results (summary stats, effect, precision) | N/A | No comparable per-study quantitative outcome exists (method.tex L5–7) |
| 20a | Synthesis — characteristics + RoB summarized | Partial | Characteristics via Fig. 1/2 counts/captions (results.tex L9–10, L23–33); RoB component N/A per item 11/18 |
| 20b | Synthesis — statistical results presented | Reported | results.tex L96–100: rule-of-three 95% upper bound (4.4%) on evaluation-research share; L75–85 cross-tab occupied/empty cell counts |
| 20c | Synthesis — heterogeneity results | N/A | Consistent with item 13's heterogeneity N/A |
| 20d | Synthesis — sensitivity analysis results | Partial | No formal sensitivity re-run; discussion.tex L82–87 gives an informal directional argument (residual research-type misclassification "would make the headline finding stronger, not weaker") — qualitative, not a rerun under alternative assumptions |
| 21 | Reporting bias per synthesis | N/A | Consistent with item 14 |
| 22 | Certainty per outcome | N/A | Consistent with item 15 |
| 23a | Interpretation in context of other evidence | Reported | discussion.tex L1–22 |
| 23b | Limitations of the evidence included | Partial | results.tex L111–116 notes 62/66 papers are preprints, framed as a reason to read the research-type finding as "a statement about a young literature" — evidence-quality-relevant, but it lives in Results, not gathered under a Discussion "limitations of evidence" heading, and there is still no discussion of what skipping quality assessment (item 11) means for trusting individual papers' claims. Unchanged since the last audit; not among the items the author reported fixing. |
| 23c | Limitations of the review process | Reported | discussion.tex L102–138 (corpus size, RQ4 withdrawal, no target-audience consultation, LLM-based screening/classification with kappa figures) and L60–100 (threats to validity: descriptive/theoretical/interpretive/repeatability) |
| 23d | Implications for practice/research | Reported | discussion.tex L47–58 |
| 24a | Registration — name/number or explicit "not registered" | Reported | main.tex L97–104, "Registration and protocol": explicit — "This review is *not* registered in a public register: PROSPERO does not accept reviews outside health research, and software engineering has no equivalent" — with the commit hash (`e21f9f3`) that fixes the protocol given as a verifiable substitute |
| 24b | Protocol access, or "none prepared" | Reported | main.tex L79–88 (Data availability, describing the decision log/protocol contents) + L100–104 (Registration and protocol, "committed to the study's version-controlled repository," commit hash given). Points to the replication package described as accompanying the submission as supplementary material; `replication/protocol.md` exists on disk and matches this description. Minor: the protocol is described as folded into a "decision log" rather than named as a standalone document, but the location and access route are stated. |
| 24c | Amendments described | Reported | method.tex L9–14 ("there were three" dated amendments); two are pilot-driven screening-rule clarifications (method.tex L96–101) and the third is the RQ4 withdrawal (intro.tex L34–37, discussion.tex L113–123, with reasons given) |
| 25 | Funding/support, funders' role | Reported | main.tex L106–107, "Acknowledgements and disclosure": "Funding: none." |
| 26 | Competing interests | Reported | main.tex L107, same section: "Competing interests: none declared." |
| 27 | Data/code/materials availability | Reported | main.tex L77–95, "Data availability": states the replication package "accompanies this submission as supplementary material," lists its contents (decision log, all 18 search strings with providers/caps, every screened record and reason, every classified paper's pages and facet justification, second coding, both reliability computations, and the regenerating scripts), and states what is *not* redistributed (full-text PDFs) and why |

**Main checklist tally: 13 Reported, 5 Partial, 1 Not reported, 8 N/A (27 total).**

## Abstract checklist (12 items)

| # | Item | Status | Location |
|---|---|---|---|
| 1 | Title identifies systematic review | Reported | main.tex L17 |
| 2 | Objectives/questions | Partial | main.tex L26–27, "This paper maps it instead," states a general aim; none of RQ1–RQ3 (intro.tex L22–32) is restated or paraphrased in the abstract |
| 3 | Eligibility criteria | Not reported | main.tex L26: "screened against pre-registered criteria" asserts criteria exist but states none of their content. **The new eligibility-chain numbers (main.tex L30–34: gate-in/classified/corpus) are a count of how many papers passed each stage, not a description of what the criteria are — that distinction matters, and it does not fix this item.** Same gap as before. |
| 4 | Information sources + search date | Partial | main.tex L30–31 gives the provider count ("2 digital libraries") but not names (arXiv/OpenAlex appear only in method.tex) or a search date |
| 5 | Risk of bias — methods to assess | N/A | Consistent with main item 11 — a deliberate design choice, not restated in the abstract, acceptable |
| 6 | Synthesis methods | Not reported | Abstract reports findings (bound, empty-cell counts) but never states how they were derived (rule of three, cross-tabulation) |
| 7 | Included studies — number + characteristics | Reported | main.tex L27–29: `\factCorpus{}` papers read in full, coded on six named facets |
| 8 | Results for main outcomes | Reported | main.tex L29–37: evaluation-research bound (4.4%), write-by-retrieval empty cells, substrate comparison |
| 9 | Limitations (brief) | Reported | main.tex L47–48 (**new**): "The corpus is a declared random sample of a cap-bound search, and [62] of its papers are preprints; both bound how far these findings generalise." Fixes the prior gap. |
| 10 | Interpretation/implications | Partial | The "not one paper... implemented in practice and studied there" framing (main.tex L29–31) carries interpretive weight, but there is no explicit "so what" sentence as there is in Discussion |
| 11 | Funding | Not reported | Not stated in the abstract itself. (Main body now has "Funding: none," main.tex L106, but PRISMA-A item 11 is about the abstract; a one-clause funding line is cheap to add here.) |
| 12 | Registration | Not reported | Abstract states "pre-registered criteria" (main.tex L26) with no register name/number and no "not registered" statement in the abstract. **This is now a real inconsistency, not just an omission**: the body (main.tex L97–99) explicitly states the review is *not* registered in a public register — the abstract's "pre-registered" wording will read to a careful reviewer as contradicting that, since "pre-registered" ordinarily implies formal registration in a register, not "criteria fixed and committed to a repo before the search." Worth a wording fix in the abstract regardless of checklist status. |

**Abstract checklist tally: 4 Reported, 3 Partial, 4 Not reported, 1 N/A (12 total).**

## Flow-diagram counts vs. database

`prisma.dot`/`prisma.pdf` node-by-node against `scripts/agentmem/facts.json`:

| Stage | Diagram | facts.json | Match? |
|---|---|---|---|
| Records returned | 7032 | GrossHits=7032 | yes |
| Distinct records | 3862 | Identified=3862 | yes |
| Duplicate provider hits removed | 3170 | (GrossHits−Identified) | yes |
| Excluded by scope filter | 2549 | ScopeDropped=2549 | yes |
| Title-identical duplicates | 28 | DuplicatesRemoved=28 | yes |
| Screening pool | 1285 | ScopeKept=1285 | yes |
| Screened | 300 | Screened=300 | yes |
| Not drawn (screening) | 985 | NotDrawnScreening=985 | yes |
| Included at screening | 192 | Included=192 | yes |
| Excluded at screening | 108 | Excluded=108 | yes |
| Full text retrieved | 171 | GateIn=171 | yes |
| No retrievable text | 21 | GateOut=21 | yes |
| **Drawn for classification** | **79** | **Drawn=80** | **NO — figure undercounts by 1** |
| Not drawn (classification) | 91 | NotDrawnClassification=91 | yes |
| Text-integrity drop | 1 | IntegrityFlagged=1 | yes |
| Papers in the map | 66 | Corpus=66 | yes |
| Excluded at eligibility | 13 | Ineligible=13 | yes |

15 of 16 node values match exactly. The one mismatch is not cosmetic: it conflates two different pipeline stages (the seeded draw of 80, and the post-integrity-check count of 79 that actually got assessed) into a single mislabeled box, so the diagram's own internal count of "drawn" disagrees with the prose two subsections later (method.tex L147–150 correctly says 80 drawn, 1 dropped, 79 assessed).

## MUST FIX before submission, ordered by cost at review

1. **Item 16a — flow diagram mislabels "Drawn for classification" as n=79; database says 80.** Regenerate `prisma.dot`/`prisma.pdf` from `facts.json` so the drawn-count box reads 80, with the integrity-check drop shown as its own step feeding into 79 classified. A flow diagram that disagrees with the manuscript's own prose two paragraphs later is the single most reviewer-visible defect in this draft.
2. **Item 16b — full-text exclusion reasons (E3=7, I1=4, E5=2, E1=2) sum to 15, not the stated total of 13 excluded.** Either add the same "a decision may cite more than one criterion" caveat used for the screening-stage breakdown (method.tex L108–109) and explain the overlap, or fix the reason counts/total so they reconcile. As written this is an unexplained arithmetic error in a section added specifically to close a prior gap.
3. **Item 17 — no characteristics table or citation of all 66 included studies in the manuscript.** 31 of 66 corpus papers are cited; the rest exist only in the replication package. The paper now explicitly defends this choice (main.tex L92–95) rather than leaving it silent, but PRISMA item 17 is not satisfied by a disclosed decision to skip it — add at minimum a compact characteristics table (year, venue type, facet values) even if full bibliographic citation of all 66 is traded off for space.
4. **Abstract item 12 vs. main item 24a — wording contradiction.** Abstract says "screened against pre-registered criteria" (main.tex L26); Registration section says "not registered in a public register" (main.tex L97–98). Reword the abstract to something like "criteria fixed and committed to a repository before screening" so it doesn't read as claiming formal registration the body then disclaims.

## PARTIAL (lower cost, worth fixing if space allows)

- Item 7 — full search strategy is signposted to the replication package (method.tex L23, `search-strings.json` confirmed to exist) but not reproduced verbatim anywhere in the compiled manuscript.
- Item 10a/10b — facet category definitions and the characteristic-variable list live only in `replication/agentmem-classification-guide.md`, never summarized in Methods.
- Item 20d — sensitivity argument is qualitative (discussion.tex L82–87), not a rerun under alternative assumptions.
- Item 23b — preprint-dominance caveat (results.tex L111–116) is evidence-quality-relevant but sits in Results, not gathered into a Discussion "limitations of the evidence" statement; the consequence of skipping quality assessment for trusting individual papers' claims is still never discussed.
- Abstract items 2, 4, 10, 11 — objectives, source names/date, an explicit implications sentence, and a funding clause are all absent from the abstract text itself (present or partially present in the body).

## Cross-check: numbers vs. data

`facts.tex` and `scripts/agentmem/facts.json` match exactly key-by-key for every key used in prose (programmatic diff, zero mismatches). `\factClassified` and `\factIneligible` — flagged in the previous audit as computed but never surfaced — are now both used (method.tex L149–150, main.tex L33). The only numeric disagreement found in this audit is the flow-diagram figure's own "Drawn for classification" node (79 vs. the correct 80), which is a defect in `prisma.dot`/`prisma.pdf`, not in `facts.tex` or the prose.
