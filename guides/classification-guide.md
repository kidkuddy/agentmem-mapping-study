# Classification guide — memory design patterns in LLM agents

You are classifying **one record** for a systematic mapping study on memory
mechanisms in LLM-based agent systems. You do two things in one pass:

1. decide whether the record is **eligible**, now that you have its text;
2. assign every **facet**.

Everything you need is in the file you were given: the record's metadata and the
extracted pages. **Do not fetch anything.** Do not download a PDF, do not call
`paper page`, do not touch the database. You read one file and write one file.

## What you were given, and what you were not

The extraction script pulled the **front matter** (title page, abstract,
introduction, contribution list) and the **tail** (evaluation, discussion,
conclusion), plus any page whose text matched an architecture cue. Those carry
the contribution claim, the mechanism and the evidence type — which is every
axis below.

You were not given the whole paper. If an axis genuinely is not decidable from
what you have, the answer is `null` with a justification saying what was
missing. `null` is a legitimate, counted, reported answer. A guessed value is
not, and it is worse than a null because nothing downstream can tell them apart.

## Step 1 — eligibility

Apply the criteria with the text in front of you. The screener saw only a title
and an abstract and was told to err toward admitting; you are the stage that
settles it.

**Include only if all hold:** the record's contribution includes a mechanism by
which an LLM-based agent writes state at run time and later retrieves it across
turns or sessions to condition its own future behaviour (**I1**); 2023 or later
(**I2**); English (**I3**); text retrievable (**I4**, already true or you would
not have the pages).

**Exclude if any hold:**

| | |
|---|---|
| **E1** | Hardware, GPU or DRAM memory, or inference-time cache optimisation, with no cross-turn agent state semantics. |
| **E2** | Memory is exclusively parametric, with no externalised store read or written at run time. |
| **E3** | Retrieval over a fixed corpus the agent never writes to. |
| **E4** | Secondary study — survey, review, systematic review, mapping study. |
| **E5** | Memory mentioned only incidentally; not part of the claimed contribution. |
| **E6** | Not an LLM-based agent. |
| **E7** | Fewer than four pages, or abstract-only. |

The three boundaries that decide most of the hard cases:

- **The agent must write the store.** A fixed index is E3 however good the
  retrieval. A pipeline that adds run-time writes to an otherwise classical RAG
  system is *in*: that boundary is what this map exists to trace.
- **An externalised store must exist.** Weights-only is E2. Weights *plus* a
  store is in, coded on the store.
- **A policy over what persists, not more room.** Extending context length is an
  architecture contribution (E1). Deciding what survives into the next turn —
  compaction, eviction, a maintained summary — is a memory mechanism.

If you exclude, write the code and the reason and **assign no facets**. Stop
there.

## Step 2 — the unit you are coding

Code the **one primary memory mechanism** the record's own contribution claim
centres on. Many records describe several stores. Pick the one the paper argues
for — the thing named in the title or the contributions list — and code that.

Additional stores go in `secondary_substrates` as a list. They are recorded, they
do not become rows in the map, and they are not a place to hedge: if you cannot
decide which store is primary, say so in the justification and pick the one the
evaluation section actually measures.

## The axes

### `substrate` — where the memory physically lives

| value | means |
|---|---|
| `prompt_resident` | The memory is the context itself: a running summary, a maintained scratchpad block, a system-prompt memory section, compacted history. Nothing is queried out of an external store. |
| `vector_store` | Embeddings with similarity search, over items the agent wrote. |
| `graph_store` | Nodes and edges the agent writes — knowledge graphs, temporal graphs, entity graphs. |
| `relational_db` | A schema'd tabular store, queried with SQL or an equivalent structured language. |
| `filesystem` | Files and directories the agent reads and writes: notes, markdown, documents, code files used as memory. |
| `kv_cache` | Persisted attention key-value state, reused across turns or sessions. |
| `multi_store` | Two or more of the above, deliberately combined, where **the combination is the contribution** — tiering, routing between stores, a hierarchy. |
| `other` | Anything else. Name it in the justification. |

`multi_store` is not "the system happens to have two stores". Almost every
system does. Use it only when the paper's contribution is how the stores relate.
Otherwise code the store the mechanism is about and list the rest as secondary.

### `write_policy` — what causes a memory to exist, and in what form

| value | means |
|---|---|
| `append_only` | Items are added; nothing already stored is rewritten. |
| `summarize_compress` | Content is condensed on write or on overflow — a running summary, a compaction pass. |
| `reflect_synthesize` | The model **generates new higher-level content** from stored memories: reflections, insights, lessons, abstractions. Content that was not in any single source item. |
| `edit_in_place` | Existing entries are updated, merged, corrected or deleted as new information arrives. |
| `agent_tool_invoked` | The agent decides when to write, through an explicit action, and the paper does not specify a transformation. |
| `none_declared` | The paper does not say. |

**Precedence, because these are not disjoint.** Code the *transformation*, not
the trigger. An agent that calls a `save_memory` tool to append is
`append_only`; a framework that automatically synthesises reflections is
`reflect_synthesize`. Reserve `agent_tool_invoked` for the case where agent
control **is** the contribution and the transformation is left unspecified.
If two transformations are both present, code the one the paper evaluates.

### `retrieval_policy` — what causes a memory to re-enter context

| value | means |
|---|---|
| `similarity_topk` | Embedding similarity, top-k. |
| `recency_window` | The last *n* items, or a time decay. |
| `structured_query` | SQL, graph traversal, keyword or metadata filter — an exact query, not a ranking. |
| `agent_directed` | The agent issues its own read as an action, choosing what to look for. |
| `always_in_context` | Never retrieved, because it is always present. Pairs with `prompt_resident`. |
| `hybrid` | Two or more combined with a **declared** fusion or re-ranking rule. |
| `none_declared` | The paper does not say. |

`hybrid` requires a stated combination rule. A system with two retrieval paths
used for different purposes is not hybrid; code the one the contribution is
about.

### `research_type` — Wieringa, via Petersen

| value | means |
|---|---|
| `validation` | A novel technique investigated in the lab. Benchmarks, controlled comparisons, ablations. **Not yet used in practice.** |
| `evaluation` | Implemented in a real setting, and the consequences of that are studied. Real users, deployment, a fielded system. |
| `solution` | A solution is proposed and argued, with a small example or a demonstration, but not systematically evaluated. |
| `philosophical` | A new conceptual framework, taxonomy or way of structuring the field. |
| `opinion` | The authors' position, with no evidence offered. |
| `experience` | A report of what actually happened when the authors used it, personal and retrospective rather than measured. |

**Assign from what the paper did, not from what it calls itself.** Mendes found
73% of papers self-designate their research type incorrectly, and this is the
axis where that shows. A paper that says "we evaluate in a real-world setting"
and reports benchmark scores on a public dataset is `validation`. `evaluation`
requires a setting with actual stakes outside the authors' own experiment.

The `validation`/`evaluation` boundary is the single most consequential judgement
you make, because RQ3 asks which substrates have never reached a deployed
setting. When it is genuinely ambiguous, code `validation` and say why in the
justification — the conservative direction, so an empty cell is not created by
generosity.

### `research_method` — how the evidence was produced

`controlled_experiment` · `benchmark_evaluation` · `case_study` · `simulation` ·
`proof_of_concept` · `none`

`controlled_experiment` manipulates a condition and compares against a control.
`benchmark_evaluation` runs systems over a fixed task suite and reports scores.
`proof_of_concept` demonstrates that the thing runs, without a comparison.
`none` for records that offer no empirical component at all.

### `contribution` — what the record gives the reader

`method` · `tool` · `model` · `metric` · `framework` · `dataset`

`method` is a technique or algorithm. `tool` is a usable implementation offered
as the contribution. `framework` is an architecture or a way of organising a
system. `dataset` covers memory benchmarks and corpora. Where a paper offers a
method and releases code, the contribution is `method` unless the artefact
itself is what the paper argues for.

### Assigned by script — do not assign these

`venue_type` and `stratum` come from metadata. They are listed so you know they
are handled, not so you can fill them in.

## Grey-stratum records

If your record is a practitioner system rather than a paper, its file says so.
Code `substrate`, `write_policy`, `retrieval_policy` and `contribution` from the
documentation exactly as above.

Code `research_type` and `research_method` as **`null`**, always, with the
justification "grey stratum: no research design". Documentation is not a study
and inventing a research type for it would put a fabricated cell in the map's
most-borrowed axis.

## Output

Write one JSON file to the `output_path` you were given. Nothing else.

```json
{
  "paper_id": 1234,
  "eligible": true,
  "eligibility_rule": "I1",
  "eligibility_criteria": [],
  "eligibility_reason": "Section 3 defines a per-episode reflection pass that writes synthesised lessons to a store the agent queries on later tasks; the agent authors the content at run time (p. 4).",
  "secondary_substrates": ["filesystem"],
  "facets": [
    {"axis": "substrate", "value": "vector_store",
     "justification": "Section 3.1: reflections are embedded and stored in FAISS; retrieval is over those embeddings (p. 4)."},
    {"axis": "write_policy", "value": "reflect_synthesize",
     "justification": "Section 3.2: at episode end the model is prompted to produce lessons that appear in no single trajectory step (p. 5)."},
    {"axis": "retrieval_policy", "value": "similarity_topk",
     "justification": "Section 3.3: top-5 nearest reflections by cosine similarity are prepended (p. 5)."},
    {"axis": "research_type", "value": "validation",
     "justification": "Evaluated on ALFWorld and WebShop against baselines; no deployment or real users reported (Section 5, p. 7)."},
    {"axis": "research_method", "value": "benchmark_evaluation",
     "justification": "Three benchmarks, four baselines, success rate reported (Table 2, p. 8)."},
    {"axis": "contribution", "value": "method",
     "justification": "The contribution list on p. 2 names the reflection mechanism; code is released but is not what the paper argues for."}
  ]
}
```

For an ineligible record, write `"eligible": false`, the rule and criteria, the
reason, and **`"facets": []`**.

Justifications cite what you actually read — a section number, a page number, a
table. You have the pages, so a justification with no anchor in them is a
justification you did not verify. Do not cite a page you were not given.
