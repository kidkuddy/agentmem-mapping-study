# Screening guide — memory design patterns in LLM agents

You are screening records for a systematic mapping study on **memory mechanisms
in LLM-based agent systems**. You decide on **title and abstract only**. You are
not reading the paper. You are not classifying it.

Everything you need is in the batch file you were given. Do not fetch anything.

## What the study is about

**Agent memory** in one sentence: a mechanism by which an LLM-based agent
**writes state at run time** and **later retrieves it across turns or sessions**
in order to condition its own future behaviour.

Three clauses, all load-bearing:

- **writes at run time** — the agent authors the content. A corpus somebody
  indexed before deployment is not memory, however good the retrieval over it.
- **across turns or sessions** — the state outlives the immediate completion.
- **conditions future behaviour** — it is read back into the agent's own loop,
  not just logged for humans.

The word "memory" is a homonym and the adjacent literatures are much larger than
this one. Most of what you reject will be GPU and inference memory, classical
retrieval-augmented generation, and parametric knowledge editing. Rejecting them
correctly is the main thing this stage is for.

## Criteria

**Include only if all of these hold.**

| | |
|---|---|
| **I1** | The record's claimed contribution includes a mechanism by which an LLM-based agent writes state at run time and later retrieves it across turns or sessions to condition its own future behaviour. |
| **I2** | Published, released or first preprinted on or after 2023-01-01. |
| **I3** | Written in English. |
| **I4** | Full text appears to be retrievable. |

**Exclude if any of these hold.**

| | |
|---|---|
| **E1** | "Memory" denotes hardware, GPU or DRAM memory, or inference-time cache optimisation, with no cross-turn agent state semantics. |
| **E2** | Memory is exclusively parametric — fine-tuning, model editing, continual learning — with no externalised store the agent reads or writes at run time. |
| **E3** | Retrieval over a fixed corpus the agent never writes to (classical RAG). |
| **E4** | Secondary study — survey, review, systematic review or mapping study. |
| **E5** | Memory is mentioned only incidentally and is not part of the claimed contribution. |
| **E6** | Not an LLM-based agent — reinforcement-learning agent memory, or a symbolic cognitive architecture with no language model in the loop. |
| **E7** | Fewer than four pages, or abstract-only. |

## Decision rules

These exist so two coders reach the same answer on the hard records.

**Two passes, in this order.** Study design first, topic second. The design
question wins: a survey about agent memory is still a survey, and no topic rule
below pulls it back in.

### Pass 1 — study design. Any of these decides, whatever the topic.

- **D1.** The contribution is aggregating other papers' findings → **E4**,
  whether or not the record calls itself a survey, review or taxonomy. Labels
  are not the test. A record proposing a new framework, architecture or position
  **is primary** — keep it; it codes as research type `philosophical`. A primary
  study with a related-work section is obviously primary.
- **D2.** No LLM is in the loop — the agent is an RL policy, a robot controller,
  a symbolic cognitive architecture, or a human — → **E6**. Human memory
  research and neuroscience are **E6**, not E5.

  **D2 fires on positive evidence, not on silence.** An abstract that never
  mentions a language model has not told you there is no language model in the
  loop; embodied-planning and agent papers routinely omit it as understood.
  Silence → **include**, and say in the reason that the population could not be
  confirmed from the abstract. E6 requires the abstract to describe something
  that is positively not an LLM agent.
- **D3.** Not a full paper: abstract-only, poster, editorial, commentary,
  keynote description, or a duplicate of another record → **E7**.

### Pass 2 — topic. Only reached by records that survive pass 1.

Apply in order; the first that matches decides.

- **T1. Which sense of "memory"?** If every mention is bandwidth, footprint,
  allocation, peak usage, swapping, quantisation or throughput → **E1**.
  A record may talk about caches throughout and still be in scope: the question
  is whether *agent state persists across turns or sessions*, not whether the
  word "cache" appears. "Persistent KV cache so an agent resumes a session"
  is **include**; "KV-cache compression that raises tokens per second" is **E1**.

- **T2. Does the agent write the store?** If the retrievable content is authored
  offline and fixed at deployment — a document collection, a wiki dump, a code
  index, a product catalogue — → **E3**, no matter how sophisticated the
  retrieval. If the agent appends, edits, summarises, reflects into or deletes
  from the store while running → **include**. A record that adds run-time writes
  to an otherwise classical RAG pipeline is **include**; that is precisely the
  boundary this study maps.

- **T3. Is there an externalised store at all?** If the only thing that persists
  is model weights — fine-tuning on session history, model editing, continual
  learning — → **E2**. If weights are updated *and* an external store is
  maintained, → **include**, and note the hybrid.

- **T4. Context window versus memory.** Extending how much the model can attend
  to is an architecture contribution, not a memory mechanism → **E1**. Deciding
  *what survives* into the next turn — compaction, summarisation, eviction,
  a rolling scratchpad the agent maintains — is a memory mechanism → **include**.
  The test is whether the record contributes a *policy over what persists*, or
  merely more room.

- **T5. Incidental use.** An agent paper whose contribution is planning, tool
  use, or a domain application, which happens to keep a conversation buffer and
  says nothing more about it → **E5**. If the memory design is named, motivated,
  varied or ablated, it is part of the contribution → **include**.

- **T6. Work about memory rather than in it.** Benchmarks and datasets for agent
  memory, evaluation methodologies, and attacks or defences on agent memory
  (poisoning, extraction, membership inference, isolation) are **include**. They
  characterise a memory mechanism, and the map has facet values for them.

  **T6 against T5, when memory is one attack surface among several.** A security
  paper covering prompt injection, backdoors *and* memory poisoning is **T6** if
  the memory attack is **named and separately evaluated** — its own condition,
  its own result. If memory appears only in a list of surfaces with no separate
  treatment, it is incidental → **T5**. The test is a separate result, not the
  share of the paper spent on it.

- **T7. Multi-agent.** Shared memory, blackboards, memory passed between agents
  and memory-as-a-service are **include**.

### Uncertainty

If two rules genuinely conflict, or the abstract does not say enough to apply
**D2, T2 or T4**, **include** and say so in the reason. Screening errs toward admitting;
the full-text stage has the paper in front of it and will settle it. Do not
guess a mechanism the abstract does not state.

## Output

Write one JSON file to the `output_path` given in your batch file. Nothing else.

```json
{
  "batch": "<the batch id from your input file>",
  "decisions": [
    {
      "paper_id": 1234,
      "decision": "include",
      "rule": "T2",
      "criteria": [],
      "reason": "Agent appends per-episode summaries to a vector store it queries on later tasks; the store is authored at run time, so T2 keeps it."
    },
    {
      "paper_id": 1235,
      "decision": "exclude",
      "rule": "T1",
      "criteria": ["E1"],
      "reason": "Every mention of memory is peak GPU usage during training; no state crosses a turn."
    }
  ]
}
```

- `decision` — `include` or `exclude`, nothing else.
- `rule` — the decision rule that settled it (`D1`–`D3`, `T1`–`T7`).
- `criteria` — the exclusion codes that apply, empty for an include.
- `reason` — one or two sentences citing what the abstract actually says. Do not
  write "meets criteria" or "off-topic". A reason that would not let a second
  coder reconstruct the decision is not a reason.

One entry per record in your batch, in the order given. Do not omit records you
find hard — include them and say why they were hard.
