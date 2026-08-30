# PRISMA Methodology Log — Design Patterns for LLM Agent Memory

**Research question:** What memory design patterns exist in LLM-based agent systems, how are they realised and evaluated, and which substrate/policy combinations does peer-reviewed research leave to practice?

## Research scope

### Topic 'LLM agent memory design patterns' declared a mapping study
_2026-08-30T18:26:08Z · methodology_choice · proposed by user_

review_type=mapping

**Rationale:** No outcome variable is comparable across studies. Papers report task success on incomparable benchmarks (LoCoMo, MemGPT's own task suite, bespoke agent environments) under incomparable memory budgets and context lengths, so nothing can be aggregated. The answerable question is what memory designs exist and which combinations nobody has studied, which is Petersen's what-exists/what-is-missing test rather than Kitchenham's what-does-the-evidence-say. Aggregating memory effectiveness was considered and rejected: it would require an SLR with quality assessment over effect measures that are not commensurable.

### Research question RQ1
_2026-08-30T18:26:08Z · methodology_choice · proposed by user_

Which storage substrates do LLM-agent memory mechanisms use, and how has their distribution changed over 2023-2026?

**Rationale:** answered by: facet:substrate

### Research question RQ2
_2026-08-30T18:26:08Z · methodology_choice · proposed by user_

Which write and retrieval policies govern agent memory, and which substrate-by-policy combinations occur in practice?

**Rationale:** answered by: facet:write_policy

### Research question RQ3
_2026-08-30T18:26:08Z · methodology_choice · proposed by user_

With which research types and research methods is agent memory investigated, and which substrates have never been evaluated in a deployed setting?

**Rationale:** answered by: facet:research_type

### Research question RQ4
_2026-08-30T18:26:08Z · methodology_choice · proposed by user_

Which substrate and policy combinations do practitioner systems occupy that the peer-reviewed literature does not?

**Rationale:** answered by: facet:stratum

### Facet axis 'research_type' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

validation,evaluation,solution,philosophical,opinion,experience

**Rationale:** Wieringa et al. 2006 as adopted wholesale by Petersen et al. 2008. Borrowed, not derived, so this map is comparable with every other Petersen map. Assigned to the peer-reviewed stratum only; practitioner records carry no research type by construction.

### Facet axis 'research_method' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

controlled_experiment,benchmark_evaluation,case_study,simulation,proof_of_concept,none

**Rationale:** Petersen 2015 lists research method alongside research type and venue type as the classification-scheme actions its rubric scores. Coding it is what lifts rubric line 4 above minimal.

### Facet axis 'contribution' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

method,tool,model,metric,framework,dataset

**Rationale:** Petersen 2008 contribution facet, with dataset added because memory benchmarks (LoCoMo and its successors) are a recurring contribution type this facet would otherwise force into 'metric'.

### Facet axis 'venue_type' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

journal,conference,workshop,preprint,grey

**Rationale:** Third scheme action in Petersen 2015. Also carries the stratum boundary: 'grey' is the practitioner enumeration.

### Facet axis 'substrate' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

prompt_resident,vector_store,graph_store,relational_db,filesystem,kv_cache,multi_store,other

**Rationale:** Derived topical axis, provisional. Values were seeded from the mechanisms named in the six secondary studies identified during scoping, and are reconciled against a keywording pass over the classification sample before any paper is coded.

### Facet axis 'write_policy' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

append_only,summarize_compress,reflect_synthesize,edit_in_place,agent_tool_invoked,none_declared

**Rationale:** Derived, provisional. What causes a memory to exist. Distinguishes a transcript log from a reflective store, which is the distinction the existing narrative surveys draw informally and inconsistently.

### Facet axis 'retrieval_policy' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

similarity_topk,recency_window,structured_query,agent_directed,always_in_context,hybrid,none_declared

**Rationale:** Derived, provisional. What causes a memory to re-enter context. agent_directed covers the case where the agent issues its own read - a tool call or a query - rather than being served a ranked slice it did not ask for.

### Facet axis 'stratum' declared
_2026-08-30T18:26:09Z · methodology_choice · proposed by user_

peer_reviewed,grey

**Rationale:** Garousi et al. 2019 multivocal review convention. The two strata are reported as separate panels because research_type is undefined for practitioner records; the comparison between panels answers RQ4.

### Unit of classification: one primary memory mechanism per record
_2026-08-30T18:26:09Z · methodology_choice · proposed by agent_

Each included record is assigned exactly one value on each mechanism axis, describing the memory design its own contribution claim centres on. Records presenting several mechanisms have the secondary ones recorded as extractions rather than as additional map rows.

**Rationale:** Two reasons. The map's denominator then equals the PRISMA flow's denominator, so every count in the paper reconciles against the flow diagram. And a record whose contribution is a single named design is the unit its authors themselves argue for; splitting records into mechanisms would let a paper with an elaborate architecture outvote a paper with a focused one.

### Sampling caps and seed, declared before the draw
_2026-08-30T18:26:09Z · methodology_choice · proposed by agent_

Screening cap 300 records, drawn by seeded random sample from everything surviving the automated scope filter and the accessibility gate. Classification cap 80 records, drawn by seeded random sample from the screening includes. Seed 20260830 for both draws.

**Rationale:** Petersen imposes no cap, but an uncapped corpus at this scale cannot be read in full within the available time, and a corpus judged from abstracts cannot support claims about mechanism structure. A declared seeded sample is an ordinary sampling design; a top-k slice of a provider's relevance ranking is not. Both caps sit below the 120-200 primary studies an eight-page map would ideally carry, and that shortfall is reported as a limitation rather than concealed.

### Grey stratum is a declared enumeration, not an open search
_2026-08-30T18:26:09Z · methodology_choice · proposed by agent_

The practitioner stratum is the union of (a) every distinct agent-memory system named in two or more of the identified secondary studies on agent memory, and (b) the memory components documented in the official documentation of named LLM agent frameworks, with the frame fixed on 2026-08-30. No open web search contributes records.

**Rationale:** An open grey search is unbounded human time and is not reproducible by a third party. A declared enumeration with a stated rule and a fixed date is a purposive sample, and is reported as one. Clause (b) exists so the grey stratum can contain designs the secondary literature has not noticed, which is exactly what RQ4 asks about.

### No target-audience consultation was performed
_2026-08-30T18:26:09Z · methodology_choice · proposed by agent_

Petersen rubric line 1 awards its top mark only when the research questions are defined together with a named target audience. No consultation was conducted.

**Rationale:** The study was executed inside a single day and a documented consultation with practising agent developers could not be arranged in that window. Scored honestly as partial, which is where 100 percent of the mapping studies Petersen examined also sit. Declared here so it is a known limitation rather than an omission a reader has to detect.

### Parametric memory excluded from scope
_2026-08-30T18:26:09Z · methodology_choice · proposed by agent_

Fine-tuning, model editing and continual learning are out of scope unless combined with an externalised store the agent reads or writes at run time (criterion E2).

**Rationale:** Decided by the principal investigator. The boundary is reported so that readers who consider parametric memory part of agent memory can see exactly what was left out.

### Screening and classification performed by LLM agents
_2026-08-30T18:26:09Z · methodology_choice · proposed by agent_

Title-and-abstract screening, full-text eligibility and all facet assignments were produced by Claude-based agents working from a written coding guide, each decision carrying its decided_by field and a written justification. A second independent coder re-coded a 20 percent sample; agreement is reported per axis.

**Rationale:** These are scientific judgements, not clerical ones, and both the IEEE policy and the PRISMA 2020 AI-disclosure expectations require them to be declared in the manuscript rather than only in the repository.

### RQ4 and the grey stratum withdrawn
_2026-08-30T18:41:33Z · scope_change · proposed by agent_

The practitioner stratum is not collected and RQ4 - which substrate and policy combinations do practitioner systems occupy that the peer-reviewed literature does not - is withdrawn. The study is executed as a single-stratum map of the peer-reviewed literature. The stratum axis remains declared and every record is coded peer_reviewed, so the axis is reported as unused rather than deleted.

**Rationale:** Two defects, one in the rule and one in the schedule. The rule's clause (a) - systems named in two or more identified secondary studies - was implemented and returns research prototypes such as MemGPT, HippoRAG, MemoryBank and ChatDB, which are already primary records in this corpus. Coding them again as practitioner records would double-count them and would contrast the literature with itself, which is not what RQ4 asks. Clause (b) - the memory components of named agent frameworks - does not have that defect, but it is a hand-enumerated frame whose documentation would have to be fetched and coded inside the remaining execution window, and a purposive frame assembled in a hurry is precisely the unreproducible selection this study criticises in others. Withdrawing the question is the honest option: the alternative is to answer it from a frame that cannot carry it, which would move a number on the data axis to save a number on the paper axis. Reported in the manuscript as a withdrawn research question with this reason, not omitted.

### Accessibility gate moved from before screening to after it
_2026-08-30T18:41:33Z · scope_change · proposed by agent_

The protocol placed the accessibility gate before screening. It is executed after screening instead: records are screened on title and abstract, and full text is fetched only for the screening includes, from which the classification sample is drawn.

**Rationale:** Fetching PDFs for all 1285 scope-filter survivors in order to gate a set from which 300 would be sampled spends the bulk of the fetching on records no coder will ever read. Screening is unaffected either way - it reads title and abstract, which every record has. Criterion I4 is applied at the later point, and the gate's exclusions appear as their own labelled row in the flow diagram rather than as a silent shrinkage between two stages.

### Screening guide amended after the 50-record pilot
_2026-08-30T18:42:59Z · scope_change · proposed by agent_

Two decision rules were under-specified and are now explicit. D2 (no LLM in the loop) fires on positive evidence that the agent is not LLM-based, never on an abstract that simply does not mention a language model; silence defaults to include, and the uncertainty rule now names D2 alongside T2 and T4. T6 versus T5 for security work: a memory attack that is named and separately evaluated counts as T6 even when it is one of several attack surfaces; memory listed among surfaces with no separate result is incidental and falls to T5.

**Rationale:** Both gaps were found by the pilot screener on 50 records and reported before the remaining 250 were screened, which is what the pilot exists for. The pilot had resolved both cases the same way the amendment now prescribes, using the uncertainty rule, so the amendment codifies the pilot's own behaviour rather than reversing it. The pilot is nonetheless re-screened under the amended guide, and the two runs are compared as a test-retest reliability measure - one of the search and selection reliability actions in Petersen's rubric line 3, on which no mapping study he examined scored full marks.

### Only one of the three planned search strategies was executed
_2026-08-30T19:51:00Z · scope_change · proposed by agent_

The protocol committed to database search, backward and forward snowballing, and manual inspection of the enumerated practitioner frame. Only the database search was executed. Snowballing was not performed; the manual strand fell away with the withdrawn grey stratum.

**Rationale:** Snowballing would have changed the corpus and required re-running screening, the accessibility gate, classification and the second-coder pass, which the one-day execution window could not absorb. Recorded as an unfulfilled commitment rather than left implicit: the study therefore scores zero on Petersen's search-strategy rubric line, where the plan would have scored two, and the manuscript now says so in the theoretical-validity paragraph rather than letting a reader infer it from the absence of a snowballing subsection.

## Search strategy

### Three search strategies will be used
_2026-08-30T18:26:09Z · search_strategy · proposed by agent_

Database search across the available providers; backward and forward snowballing from the most-cited included records; and manual inspection of the enumerated practitioner frame.

**Rationale:** Petersen rubric line 2 scores the count of search types, and roughly 58 percent of published maps use only one. Three is the maximum the rubric recognises.

### Search 258 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:27:03Z · search_strategy · proposed by user_

providers=arxiv; query=LLM agent memory mechanism; years=2023-0; max_results=200; hits=200; new=154

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 259 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:27:08Z · search_strategy · proposed by user_

providers=openalex; query=LLM agent memory mechanism; years=2023-0; max_results=200; hits=200; new=107

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 260 on 'LLM agent memory design patterns' (semantic)
_2026-08-30T18:27:53Z · search_strategy · proposed by user_

providers=semantic; query=LLM agent memory mechanism; years=2023-0; max_results=100; hits=0; new=0

**Rationale:** Search strategy recorded at run time for reproducibility.

### Search 261 on 'LLM agent memory design patterns' (semantic)
_2026-08-30T18:29:14Z · search_strategy · proposed by user_

providers=semantic; query=LLM agent memory mechanism; years=2023-0; max_results=100; hits=0; new=0

**Rationale:** Search strategy recorded at run time for reproducibility.

### Search 262 on 'LLM agent memory design patterns' (semantic)
_2026-08-30T18:30:35Z · search_strategy · proposed by user_

providers=semantic; query=LLM agent memory mechanism; years=2023-0; max_results=100; hits=0; new=0

**Rationale:** Search strategy recorded at run time for reproducibility.

### Search 263 on 'LLM agent memory design patterns' (semantic)
_2026-08-30T18:31:23Z · search_strategy · proposed by user_

providers=semantic; query=LLM agent memory mechanism; years=2023-0; max_results=100; hits=100; new=84

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 100, so this is top-100-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 264 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:31:41Z · search_strategy · proposed by user_

providers=arxiv; query=long-term memory large language model agent; years=2023-0; max_results=200; hits=200; new=80

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 265 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:31:47Z · search_strategy · proposed by user_

providers=openalex; query=long-term memory large language model agent; years=2023-0; max_results=200; hits=200; new=69

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 266 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:31:54Z · search_strategy · proposed by user_

providers=arxiv; query=episodic memory language agent; years=2023-0; max_results=200; hits=200; new=92

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 267 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:31:59Z · search_strategy · proposed by user_

providers=openalex; query=episodic memory language agent; years=2023-0; max_results=200; hits=200; new=143

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 268 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:32:06Z · search_strategy · proposed by user_

providers=arxiv; query=agent memory architecture persistent state; years=2023-0; max_results=200; hits=200; new=130

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 269 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:32:11Z · search_strategy · proposed by user_

providers=openalex; query=agent memory architecture persistent state; years=2023-0; max_results=200; hits=200; new=137

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 270 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:32:18Z · search_strategy · proposed by user_

providers=arxiv; query=memory augmented LLM agent long-horizon task; years=2023-0; max_results=200; hits=200; new=117

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 271 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:32:23Z · search_strategy · proposed by user_

providers=openalex; query=memory augmented LLM agent long-horizon task; years=2023-0; max_results=200; hits=200; new=98

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 272 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:32:29Z · search_strategy · proposed by user_

providers=arxiv; query=conversational agent long-term memory personalization; years=2023-0; max_results=200; hits=200; new=111

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 273 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:32:34Z · search_strategy · proposed by user_

providers=openalex; query=conversational agent long-term memory personalization; years=2023-0; max_results=200; hits=200; new=115

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 274 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:32:41Z · search_strategy · proposed by user_

providers=arxiv; query=memory management context window large language model agent; years=2023-0; max_results=200; hits=200; new=61

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 275 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:32:47Z · search_strategy · proposed by user_

providers=openalex; query=memory management context window large language model agent; years=2023-0; max_results=200; hits=200; new=93

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 276 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:33:10Z · search_strategy · proposed by user_

providers=arxiv; query=reflection self-generated memory language agent; years=2023-0; max_results=200; hits=200; new=55

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 277 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:33:15Z · search_strategy · proposed by user_

providers=openalex; query=reflection self-generated memory language agent; years=2023-0; max_results=200; hits=200; new=64

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 278 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:33:21Z · search_strategy · proposed by user_

providers=arxiv; query=vector store memory retrieval augmented agent; years=2023-0; max_results=200; hits=200; new=144

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 279 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:33:27Z · search_strategy · proposed by user_

providers=openalex; query=vector store memory retrieval augmented agent; years=2023-0; max_results=200; hits=200; new=104

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 280 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:33:34Z · search_strategy · proposed by user_

providers=arxiv; query=knowledge graph memory LLM agent; years=2023-0; max_results=200; hits=200; new=71

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 281 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:33:39Z · search_strategy · proposed by user_

providers=openalex; query=knowledge graph memory LLM agent; years=2023-0; max_results=200; hits=200; new=47

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 282 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:33:45Z · search_strategy · proposed by user_

providers=arxiv; query=database symbolic memory large language model agent; years=2023-0; max_results=200; hits=200; new=36

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 283 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:33:50Z · search_strategy · proposed by user_

providers=openalex; query=database symbolic memory large language model agent; years=2023-0; max_results=200; hits=200; new=64

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 284 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:33:57Z · search_strategy · proposed by user_

providers=arxiv; query=file system external memory language model agent; years=2023-0; max_results=200; hits=200; new=31

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 285 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:34:03Z · search_strategy · proposed by user_

providers=openalex; query=file system external memory language model agent; years=2023-0; max_results=200; hits=200; new=45

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 286 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:34:09Z · search_strategy · proposed by user_

providers=arxiv; query=memory consolidation forgetting eviction LLM agent; years=2023-0; max_results=200; hits=200; new=53

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 287 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:34:13Z · search_strategy · proposed by user_

providers=openalex; query=memory consolidation forgetting eviction LLM agent; years=2023-0; max_results=200; hits=118; new=80

**Rationale:** Search strategy recorded at run time for reproducibility.

### Search 288 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:34:19Z · search_strategy · proposed by user_

providers=arxiv; query=MemGPT Letta memory operating system agent; years=2023-0; max_results=200; hits=200; new=65

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 289 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:34:24Z · search_strategy · proposed by user_

providers=openalex; query=MemGPT Letta memory operating system agent; years=2023-0; max_results=200; hits=114; new=72

**Rationale:** Search strategy recorded at run time for reproducibility.

### Search 290 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:34:30Z · search_strategy · proposed by user_

providers=arxiv; query=long-term conversational memory benchmark evaluation; years=2023-0; max_results=200; hits=200; new=72

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 291 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:34:36Z · search_strategy · proposed by user_

providers=openalex; query=long-term conversational memory benchmark evaluation; years=2023-0; max_results=200; hits=200; new=75

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 292 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:34:43Z · search_strategy · proposed by user_

providers=arxiv; query=cross-session memory personalization assistant LLM; years=2023-0; max_results=200; hits=200; new=100

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 293 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:34:48Z · search_strategy · proposed by user_

providers=openalex; query=cross-session memory personalization assistant LLM; years=2023-0; max_results=200; hits=200; new=119

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 294 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:34:54Z · search_strategy · proposed by user_

providers=arxiv; query=procedural memory skill library agent; years=2023-0; max_results=200; hits=200; new=156

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 295 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:34:59Z · search_strategy · proposed by user_

providers=openalex; query=procedural memory skill library agent; years=2023-0; max_results=200; hits=200; new=151

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 296 on 'LLM agent memory design patterns' (arxiv)
_2026-08-30T18:35:06Z · search_strategy · proposed by user_

providers=arxiv; query=experience memory reuse LLM agent learning; years=2023-0; max_results=200; hits=200; new=53

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

### Search 297 on 'LLM agent memory design patterns' (openalex)
_2026-08-30T18:35:11Z · search_strategy · proposed by user_

providers=openalex; query=experience memory reuse LLM agent learning; years=2023-0; max_results=200; hits=200; new=88

**Rationale:** Search strategy recorded at run time. NOTE: the harvest hit the max_results cap of 200, so this is top-200-by-relevance per provider, not an exhaustive result set — a coverage limitation that must be declared.

## Screening criteria (title/abstract)

### inclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

I1 The record's claimed contribution includes a mechanism by which an LLM-based agent writes state at run time and later retrieves it across turns or sessions in order to condition its own future behaviour.

**Rationale:** This is the operational definition of agent memory used throughout. The run-time write is the discriminating clause: it is what separates memory from retrieval over a corpus the agent cannot change.

### inclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

I2 Published, released or first preprinted on or after 2023-01-01.

**Rationale:** MemGPT, Generative Agents and Reflexion all appear in 2023 and are the point at which externalised agent memory becomes a named design concern. Earlier memory-augmented language-model work belongs to a different research programme.

### inclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

I3 Written in English.

**Rationale:** The reviewers read English. A language criterion applied silently is a validity threat; applied openly it is a stated limitation.

### inclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

I4 Full text is retrievable, directly or via an arXiv record under the same title.

**Rationale:** Accessibility gate. Every included record must be readable by construction, so the whole corpus can be classified from full text and no false-inclusion rate has to be estimated from a validation sample.

### exclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

E1 'Memory' denotes hardware, GPU or DRAM memory, or inference-time cache optimisation, with no cross-turn agent state semantics.

**Rationale:** The dominant source of false positives: processing-in-memory, memory-bound kernels and KV-cache throughput work share the vocabulary and share nothing else. A KV-cache paper is in scope only if the cache persists agent state across sessions.

### exclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

E2 Memory is exclusively parametric - fine-tuning, model editing or continual learning - with no externalised store the agent reads or writes at run time.

**Rationale:** Scope decision by the principal investigator. Weight-resident knowledge is a large, mature and separate research programme; including it would roughly double the corpus without changing what the map is about.

### exclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

E3 Retrieval over a fixed corpus the agent never writes to (classical retrieval-augmented generation).

**Rationale:** Retrieval is not memory unless the agent authors what it later retrieves. Without this criterion the corpus becomes the RAG literature.

### exclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

E4 Secondary study - survey, review, systematic review or mapping study.

**Rationale:** Secondary studies are the comparison this map is motivated against, so they are recorded as related work rather than as primary records.

### exclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

E5 Memory is mentioned only incidentally and is not part of the claimed contribution.

**Rationale:** An agent paper that happens to keep a scratchpad is not a memory paper. Petersen's keywording works on the contribution claim.

### exclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

E6 The system is not an LLM-based agent - reinforcement-learning agent memory, or a symbolic cognitive architecture with no language model in the loop.

**Rationale:** Population boundary. Prior cognitive-architecture memory work informs the discussion but is not the population being mapped.

### exclusion criterion proposed
_2026-08-30T18:26:09Z · criterion_screening · proposed by agent_

E7 Fewer than four pages, or abstract-only.

**Rationale:** A record too short to state a mechanism cannot be classified on the mechanism axes.

## Exclusions during screening

### Paper 18739 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=18739 criteria=24

**Rationale:** The mechanism prices flash program/erase-cycle wear ('every persisted write spends one of a few thousand program/erase cycles and never refills') and routes storage across RAM/NVM/cloud by cost; this is hardware endurance/cost optimisation with no cross-turn agent state semantics, and no LLM is described in the loop.

### Paper 13868 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=13868 criteria=27

**Rationale:** Abstract says the paper 'explores multi-agent systems and identify challenges that remain inadequately addressed' and 'discuss[es]' task allocation, debate and memory management as open problems -- this aggregates known issues rather than presenting a primary mechanism or novel architecture.

### Paper 14808 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=14808 criteria=29

**Rationale:** Abstract is a 'review' of 'episodic-like memory' in 'animal minds' and 'comparative cognitive psychology', about food caching in non-human animals, with AI models mentioned only as a hoped-for 'fruitful avenue for future behavioural research' -- positively not an LLM agent.

### Paper 16968 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=16968 criteria=26

**Rationale:** ARM 'replaces a static vector index with a dynamic memory substrate governed by selective remembrance and decay' of already-indexed items based on retrieval frequency; no agent authors new content into the store, and no LLM agent loop is described -- a RAG index-management improvement.

### Paper 20089 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=20089 criteria=28

**Rationale:** Abstract concerns 'routing accuracy,' 'skill library' scaling and 'execution law' across '1,141 real-world skills'; memory is never mentioned, so no memory mechanism is part of the claimed contribution.

### Paper 17064 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=17064 criteria=26

**Rationale:** LRAT trains a retriever from logged 'agent trajectories' ('browsing actions, unbrowsed rejections, and post-browse reasoning traces') to improve ranking; the retriever is trained offline and no persistent cross-session agent-authored store is described.

### Paper 17228 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=17228 criteria=26

**Rationale:** The method retrieves 'relevant passages from external memory' built from a fixed corpus of 'scientific papers,' organized via a 'document tree' representing existing paper structure; the agent never writes to this corpus.

### Paper 14959 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=14959 criteria=24

**Rationale:** OISMA is an 'in-memory computing (IMC) architecture' converting 'memory read operations into in situ stochastic multiplication operations,' reporting 'TOPS/W' and 'GOPS/mm2' -- hardware/RRAM compute memory with no agent or cross-turn state semantics.

### Paper 14099 excluded at screening
_2026-08-30T18:52:08Z · exclusion_screening · proposed by agent:screener_

paper_id=14099 criteria=28

**Rationale:** A 'dynamic memory mechanism enables InternGeometry to conduct more than two hundred interactions with the symbolic engine' is mentioned once with no further description, motivation, or ablation; the claimed contributions are heuristic auxiliary constructions and Complexity-Boosting RL.

### Paper 17824 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=17824 criteria=28

**Rationale:** 'Memory-augmented tool use' and 'hyperdimensional memory layers' are mentioned only among a list of phenomena/proposed biases a VSA lens is applied to; the paper's contribution is a vector-symbolic interpretation of attention, not a memory mechanism.

### Paper 15219 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=15219 criteria=27

**Rationale:** Self-described 'review article' providing 'a comprehensive analysis of the A2A protocol' and examining 'a broad range of industrial and research use cases' from prior work -- aggregates existing material rather than proposing a primary mechanism (and is not about agent memory at all).

### Paper 20087 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=20087 criteria=29

**Rationale:** COMAD is explicitly reinforcement learning: it builds a 'skill-augmented policy learning objective,' evaluates on 'diverse MARL benchmarks,' and discusses 'catastrophic forgetting and plasticity loss' with no language model anywhere in the pipeline -- positively an RL agent, not LLM-based.

### Paper 18746 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=18746 criteria=28

**Rationale:** 'Long-term memory' is listed once among many exposed capabilities ('context, events, state rendering, long-term memory, and validated LLM loops') of a general agent-as-Python-object framework; memory is not named, motivated or evaluated as its own contribution.

### Paper 16014 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=16014 criteria=29

**Rationale:** DT4IER is a 'decision transformer-based recommendation model' trained with 'reinforcement learning' for a Recommender System; 'long-term retention' refers to user engagement metrics, not an agent memory mechanism, and no LLM is in the loop.

### Paper 18742 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=18742 criteria=24

**Rationale:** Leyline is 'a serving-side primitive' for 'KV cache' editing during inference, addressing 'exact-prefix caches,' 'position-independent caching,' and 're-prefill' cost; this is inference-time cache-serving optimisation, matching the guide's own E1 example of 'KV-cache compression that raises tokens per second.'

### Paper 14654 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=14654 criteria=29

**Rationale:** Agents are explicitly 'Sequential Episodic Control (SEC) agents,' framed as 'neurocomputational models' of 'cultural evolution' and collective foraging, with no language model anywhere in the description -- positively not an LLM agent.

### Paper 17192 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=17192 criteria=26

**Rationale:** SafetyRAG retrieves from 'an external knowledge base of safety facts' that is fixed and provided to 'enhance the decision-making' of the LLM; the agent never writes to this safety-fact store.

### Paper 17207 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=17207 criteria=26

**Rationale:** The system retrieves from 'ChromaDB vector storage' built over a fixed 'Global Tuberculosis Report 2024' document; the agent performs multi-hop retrieval/reasoning over this static corpus but never writes to it.

### Paper 19260 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=19260 criteria=29

**Rationale:** 'Speaker Information Enhanced Long-Short Term Memory (SI-LSTM) for the ERC task' is a recurrent neural architecture for emotion recognition, not an LLM in the loop -- positive evidence of a non-LLM population fires D2.

### Paper 17053 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=17053 criteria=26

**Rationale:** EICL 'aids in generating sentences...by memorizing semantic and attribute information from unlabelled corpora,' i.e. content fixed/derived offline from a corpus rather than authored by the agent at run time, so T2 routes this to classical RAG (E3).

### Paper 17432 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=17432 criteria=24

**Rationale:** The 'working memory constraints' addressed are within-query buffering of graph text for a single reasoning pass ('Buffer Module integrates and indexes graph data across multiple formats'), not state that persists across turns or sessions, closer to attention/context capacity than agent memory.

### Paper 20349 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=20349 criteria=24

**Rationale:** The only 'memory' mentioned is storage cost of policy populations ('incurring quadratic computation and linear memory costs'; GEMS has '1.3x less memory usage than PSRO') -- resource/footprint sense only, no cross-turn agent state.

### Paper 19982 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=19982 criteria=28

**Rationale:** The abstract describes a structured representation for 'agent skill artifacts' (scheduling/structural/logical signals) with no mention of a memory store the agent writes to and retrieves across turns/sessions; there is nothing to apply I1 to.

### Paper 19947 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=19947 criteria=28

**Rationale:** 'memory-aware failure recovery' is named once with no elaboration; the claimed contribution is the skill base (parameterized execution/composition graphs) and skill retrieval, so memory is incidental (E5).

### Paper 18211 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=18211 criteria=28

**Rationale:** The abstract concerns repository exploration strategies (linear vs. domain-scoped parallel agent traversal) for file localization; no memory store or cross-turn/session state is described anywhere.

### Paper 19975 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=19975 criteria=28

**Rationale:** CODESKILL is explicitly contrasted with 'the strongest prompt-based or memory baseline,' positioning its skill-bank mechanism as distinct from a memory system; the abstract never frames its own skill bank as memory.

### Paper 17360 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=17360 criteria=27

**Rationale:** 'This survey presents a comprehensive review of agent memory from the graph-based perspective' and offers 'a taxonomy of agent memory'; aggregating other papers' findings fires D1/E4 regardless of the memory topic.

### Paper 14103 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=14103 criteria=27

**Rationale:** 'we systematically evaluate 18 representative healthcare agent papers under strict mechanism-level criteria' is aggregation of other papers' findings via a taxonomy, D1/E4 regardless of the memory-evolution topic it covers.

### Paper 15873 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=15873 criteria=27

**Rationale:** The paper's stated method is '1) reviewing the technological underpinnings of LTM..., 2) surveying current personal AI companions and assistants, and 3) analyzing critical considerations' -- an explicit review/survey design, D1/E4.

### Paper 18950 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=18950 criteria=28

**Rationale:** The contribution is a diagnostic method for locating faithfulness/citation errors across a multi-agent report pipeline; the abstract contains no description of a memory store the agents write to or read from.

### Paper 14371 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=14371 criteria=27

**Rationale:** 'This survey aims to provide a comprehensive overview of LSTM architectures' -- a secondary aggregation of RNN literature with no LLM agents at all, D1/E4 (also fails E6 on population).

### Paper 18749 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=18749 criteria=29

**Rationale:** This is 'Experience Replay' for 'artificial neural networks' on split-CIFAR100/TinyImageNet image classification, with no language model in the loop -- D2 fires on positive evidence of a non-LLM population.

### Paper 14898 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=14898 criteria=25

**Rationale:** The mechanism is 'sharpness-aware minimization' applied 'during fine-tuning' to flatten the loss landscape; only model weights are affected, no externalised store the agent reads or writes at run time (E2).

### Paper 19086 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=19086 criteria=28

**Rationale:** The contribution is a model-harness 'interface contract' hierarchy for goal/tool/action validity; 'persistent state' is invoked generally but no concrete write/retrieve memory mechanism is described, so it is incidental to the actual contribution.

### Paper 20043 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=20043 criteria=28

**Rationale:** EffiSkill builds 'a portable optimization toolbox' of 'reusable agent skills' (Operator and Meta Skills) mined from program pairs; the abstract never uses the word memory or describes cross-turn/session agent state.

### Paper 19976 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=19976 criteria=28

**Rationale:** The note is about skill artefacts as software artefacts, mentioning 'project memory files' only as one contrasted mechanism among slash commands, subagents, and hooks; memory is not the claimed contribution.

### Paper 18689 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=18689 criteria=27

**Rationale:** 'this survey provides the first comprehensive and systematic review of Vibe Coding...Drawing from systematic analysis of over 1000 research papers' is explicit secondary aggregation, D1/E4.

### Paper 20129 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=20129 criteria=29

**Rationale:** The study is 'a longitudinal study with 78 teams' of human contributors' self-beliefs and transactive memory; this is human memory/socio-cognitive research, D2's explicit E6 case, not an LLM agent.

### Paper 17013 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=17013 criteria=24

**Rationale:** KGERMAR 'constructs dynamic, context-specific knowledge graphs from input text during inference' and is evaluated on perplexity over SlimPajama/WikiText-103/PG-19 -- long-context language modeling, not an agent whose state persists across turns or sessions.

### Paper 14402 excluded at screening
_2026-08-30T18:52:09Z · exclusion_screening · proposed by agent:screener_

paper_id=14402 criteria=28

**Rationale:** DroidAgent 'is based on Large Language Models and support mechanisms such as long- and short-term memory' -- named once with no further design detail; the claimed contribution is intent-driven goal-setting and GUI test generation, memory is incidental.

### Paper 14042 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=14042 criteria=24

**Rationale:** 'memory, and energy constraints' here means device resource budgets for small LLMs on IoT edge hardware ('51.2% CPU usage reduction and 50.4% energy savings'); no cross-turn agent state semantics are described.

### Paper 17082 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=17082 criteria=29

**Rationale:** RowNet is a 'retrieval-based neural architecture for real estate price-per-square-meter prediction' comparing MLPs and gradient-boosted trees; there is no LLM in the loop, only a similarity-based 'memory bank of labeled properties' for tabular regression.

### Paper 20237 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=20237 criteria=29

**Rationale:** This is 'a modified version of Performance Factor Analysis' using attention mechanisms over student item-response data; large language models are mentioned only as background context lacking 'a complete approach for tracking knowledge,' not as the studied population -- no LLM agent in the loop.

### Paper 16754 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=16754 criteria=29

**Rationale:** The paper studies effects of AI tool use on human students' 'critical thinking,' 'creativity,' and 'storage of memories' via surveys and prior studies of students -- human cognition research, D2's explicit E6 case.

### Paper 17244 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=17244 criteria=27

**Rationale:** 'this tutorial provides a systematic and comprehensive introduction to the principles, design, and applications of Large Artificial Intelligence Models (LAMs) and Agentic AI technologies' -- explicit secondary aggregation/tutorial, D1/E4.

### Paper 16068 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=16068 criteria=30

**Rationale:** The abstract field contains only a bibliographic citation ('Kai Tzu-iunn Ong...Proceedings of the 2025 Conference...') with no descriptive content to evaluate against I1-I4; treated as unretrievable/insufficient content, E7.

### Paper 15965 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=15965 criteria=27

**Rationale:** 'This tutorial introduces the evolution from traditional RAG to advanced Long-Term Memory (LTM) mechanisms' and reviews 'cutting-edge systems (like Mem0)' -- explicit tutorial/secondary aggregation, D1/E4.

### Paper 15734 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=15734 criteria=27

**Rationale:** 'This study reviews multi-turn conversational AI across text-only dialogue, AudioLLMs...and tool-augmented agents,' organizing 'the literature around datasets and benchmarks' -- explicit review, D1/E4.

### Paper 19639 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=19639 criteria=27

**Rationale:** 'This paper presents a retrospective overview of a decade of research...We summarize past experiments and results' -- explicit retrospective aggregation of the group's own prior work, D1/E4.

### Paper 18780 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=18780 criteria=30

**Rationale:** This is a 'Reproduction package...judged outputs, flag manifests, and analysis scripts,' i.e. a software/data artifact description (npm install/run instructions, CI details), not a research paper abstract -- D3/E7.

### Paper 14977 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=14977 criteria=28

**Rationale:** A 'convergent memory model' is named once amid many hardware-layer components (routing policy, habit-compilation, safety constraints); the measured contribution is latency/energy reduction from cognitive decomposition across compute substrates, not the memory design itself.

### Paper 6721 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=6721 criteria=28

**Rationale:** The tool explicitly targets 'memoryless sequential decision-making tasks' -- the studied LLM policies have no persistent state to write or retrieve, the opposite of I1's mechanism.

### Paper 14045 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=14045 criteria=25

**Rationale:** PEAM 'transforms agent memory from inference-time retrieval into parameter-resident skills internalized through experience' via LoRA adapters ('parameter-level continual learning') with no externalised store described -- exclusively parametric memory, E2.

### Paper 18501 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=18501 criteria=24

**Rationale:** IndexMem addresses 'standard softmax attention incur[ring] a KV cache that grows linearly with sequence length' during a single long-context inference pass, evaluated on RULER/Needle-in-a-Haystack/LongBench -- inference-time cache/eviction optimisation, not cross-turn/session agent state.

### Paper 14090 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=14090 criteria=28

**Rationale:** 'reasoning trajectories are treated as reliable internal beliefs for guiding actions and updating memory' is background framing; the claimed contribution is adversarial self-auditing/verification of belief states (SAVeR), not a memory design, so memory is incidental.

### Paper 13873 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=13873 criteria=27

**Rationale:** 'This review examines recent developments in employing LLMs as autonomous agents and tool users and comprises seven research questions,' explicitly a structured review across 2023-2025 papers -- D1/E4.

### Paper 14745 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=14745 criteria=29

**Rationale:** SMEMO is 'a neural network based on an end-to-end trainable working memory' for pedestrian trajectory forecasting; there is no language model in the loop, only a purpose-built memory-augmented RNN/attention network.

### Paper 13756 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=13756 criteria=26

**Rationale:** MemoryForge “synthesize[s] such lifelong memory from brief target personas” as a framework step, and the “frozen LLMs... dynamically retrieve situation-relevant memory” — the store is authored offline by MemoryForge, not written by the agent itself at run time, so T2 routes it to E3.

### Paper 16672 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=16672 criteria=26

**Rationale:** The method “post-processes model outputs and corrects factual inconsistencies via external semantic memory” built from RDF triples; there is no description of an agent writing to this store across turns, only single-shot retrieval-based correction, so T2 routes it to E3.

### Paper 18276 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=18276 criteria=28

**Rationale:** The only memory mention is “enhancing their context-awareness and long-term memory” in a passing sentence; CMAT's actual contribution is adaptive weight-update tuning between agents, with memory neither named as a mechanism nor evaluated, so T5 applies.

### Paper 16125 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=16125 criteria=24

**Rationale:** The method “continually compresses the accumulating attention key/value pairs into a compact memory space, facilitating language model inference in a limited memory space” — KV-cache compression for throughput/context handling, not cross-turn agent state (T1/E1).

### Paper 15866 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=15866 criteria=27

**Rationale:** “This survey provides a capability-oriented review of personalized LLM-powered agents”, synthesizing existing methods into a taxonomy — an explicit secondary/aggregating study (D1/E4).

### Paper 18991 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=18991 criteria=28

**Rationale:** “external memory” appears only once, inside a list of mutable modules (“foundational models, system prompts, tool-access policies, external memory”) supporting an identity/reputation argument; no memory mechanism is described or evaluated (T5).

### Paper 13975 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=13975 criteria=28

**Rationale:** “leveraging LLM capabilities, cognitive mechanisms, and contextual memory retrieval” is a passing description of the virtual-patient chatbot; the paper's actual contribution is the training tool and its usability score, memory is not named or evaluated (T5).

### Paper 20669 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=20669 criteria=29

**Rationale:** The paper is about “Long Short-Term Memory (LSTM) networks for energy consumption forecasting” and hardware-accelerated ML for building management systems, with no LLM or agent described — positively not an LLM agent (D2/E6).

### Paper 13691 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=13691 criteria=28

**Rationale:** “acquire memory” is one item in a list of agent runtime capabilities (“Skills, synthesize tools, fork child processes... commit checkpoints”); the paper's actual focus is capability-controlled security admission, and memory is never elaborated as a contribution (T5).

### Paper 18203 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=18203 criteria=24

**Rationale:** The study is about context formatting/schema structure for SQL-generation tasks (“4 formats (YAML, Markdown, JSON, TOON)”); no memory or cross-turn/session state is described, only how much/what shape of context the model attends to (T4/E1).

### Paper 18205 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=18205 criteria=29

**Rationale:** ComMem performs “test-time adaptation (TTA) of vision-language models” for classification via a visual cache and refined text prototypes across test samples; no agent, tool use, or task-taking behavior is described — positively not an LLM agent (D2/E6).

### Paper 14594 excluded at screening
_2026-08-30T18:52:10Z · exclusion_screening · proposed by agent:screener_

paper_id=14594 criteria=29

**Rationale:** The study examines “the relationship between interacting attention heads and human episodic memory”, directly comparing induction heads to “the contextual maintenance and retrieval (CMR) model of human episodic memory” — human memory/neuroscience research is E6 per D2, not E5.

### Paper 14030 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14030 criteria=28

**Rationale:** “maintaining memory” is one item in a list of runtime responsibilities (“scheduling jobs, calling tools, maintaining memory, and pushing results to humans”, “a knowledge-base memory plane”); the paper's contribution is a failure taxonomy, not the memory mechanism (T5).

### Paper 18531 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=18531 criteria=29

**Rationale:** The paper proposes a theory of “memory consolidation” in “high-capacity neocortical networks” with “biologically plausible predictive coding circuits” — human/brain memory research, explicitly E6 per D2's neuroscience note.

### Paper 13999 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=13999 criteria=27

**Rationale:** “Using a PRISMA-inspired framework, we systematically reviewed nearly 250 scholarly sources” — an explicit secondary/survey study of evaluation methods (D1/E4).

### Paper 18678 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=18678 criteria=27

**Rationale:** “we propose a comprehensive survey on the memory of LLM-driven AI systems”, organizing prior work into a taxonomy — an explicit survey (D1/E4).

### Paper 13953 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=13953 criteria=24

**Rationale:** H2-LLM is a “Hybrid-bonding-based Heterogeneous accelerator” using “near-memory processing (NMP)” embedded in “DRAM dies” for low-batch LLM inference — hardware/DRAM memory optimization with no cross-turn agent state (T1/E1).

### Paper 13993 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=13993 criteria=28

**Rationale:** “the memory recollection mechanism for the dynamic execution agent” is a single unelaborated clause; the paper's actual contribution is a proactive-clarification planning framework (CEP), not the memory design (T5).

### Paper 17241 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=17241 criteria=27

**Rationale:** “we discuss work showing that these systems implement some key features of episodic memory” and “this article is part of the theme issue’Elements of episodic memory’” — a synthesizing review of existing AI systems to inform biological memory theory (D1/E4).

### Paper 19064 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=19064 criteria=27

**Rationale:** “This survey presents a comprehensive and structured synthesis of memory in LLMs and MLLMs, organizing the literature into a cohesive taxonomy” — an explicit survey (D1/E4).

### Paper 19218 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=19218 criteria=25

**Rationale:** “Memory Decoder introduces a parametric long-term memory module” and studies “allocating more parameters to memory” — purely parametric memory with no externalized run-time store the agent itself writes to (T3/E2).

### Paper 15463 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=15463 criteria=28

**Rationale:** “the memoryless agents repeat wrong calls for days at a time” — the evaluated trading agents are explicitly memoryless; memory is only mentioned as motivating “a memory-aware, LLM-based successor”, i.e. future work, not the paper's contribution (T5).

### Paper 14417 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14417 criteria=29

**Rationale:** The paper tunes “Long Short-Term Memory (LSTM) neural networks... for wind power generation forecasting” — a neural time-series model, no LLM or agent in the loop (D2/E6).

### Paper 15046 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=15046 criteria=24

**Rationale:** DGAP targets “Emerging persistent memory technologies, such as Optane DCPMM” for dynamic graph analysis — a hardware persistent-memory systems paper with no agent state semantics (T1/E1).

### Paper 14077 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14077 criteria=24

**Rationale:** Warp Cortex “reduce[s] memory complexity from O(N * L) to O(1) for weights and O(N * k) for context” by treating “the KV-cache as a point cloud” — a GPU/VRAM memory-efficiency optimization for scaling agent count, not cross-session agent state (T1/E1).

### Paper 14061 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14061 criteria=27

**Rationale:** “This survey makes three contributions. First, we introduce a four-dimensional taxonomy, covering... memory architecture” applied to 12 systems — an explicit survey (D1/E4).

### Paper 18508 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=18508 criteria=24

**Rationale:** SleepGate “augments transformer-based LLMs with a learned sleep cycle over the key-value (KV) cache”, including “a forgetting gate trained to selectively evict or compress stale cache entries” — within-context KV-cache management with no agent or cross-session persistence described (T1/E1).

### Paper 17765 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=17765 criteria=26

**Rationale:** The framework augments LLMs with “relational databases as external memory”, data that is “typically stored in relational databases” beforehand — classical retrieval over a fixed corpus, not content the agent writes at run time (T2/E3).

### Paper 17050 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=17050 criteria=26

**Rationale:** The paper proposes a general “graph-augmented vector retrieval” technique for ANN search, applicable to “memory-augmented agents” among other uses, but describes no agent writing state — a static retrieval/embedding-selection method (T2/E3).

### Paper 14641 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14641 criteria=26

**Rationale:** BitMar's decoder is “used to query a fixed-size key-value episodic memory” for image-text generation — retrieval over a bounded/fixed memory store, with no description of the model writing new entries during interaction (T2/E3).

### Paper 14831 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14831 criteria=29

**Rationale:** This is a clinical drug trial: “Women with IIH... were treated with exenatide... or placebo”, measuring “episodic memory” as a human cognitive outcome — human medical research, no LLM or agent (D2/E6).

### Paper 18770 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=18770 criteria=28

**Rationale:** “discussions centered on the agents' own architecture, especially memory, learning, and self-reflection, are prevalent in the corpus” — memory is a topic-modeling finding about agent discourse content, not the study's own memory mechanism (T5).

### Paper 19075 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=19075 criteria=27

**Rationale:** “This review connects ten historical cognitive architectures, eight language-agent runtime families, and forty-two mechanism-focused modern systems”, coding “evidence relation” across them — an explicit mechanism-level review (D1/E4).

### Paper 18610 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=18610 criteria=24

**Rationale:** The method “gradually distills episodic retrievals into parametric semantic memory” specifically to reduce “attention operations”/compute on GPT-2, an inference-efficiency technique, not cross-session agent state (T1/E1).

### Paper 14671 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14671 criteria=24

**Rationale:** EpMAN's “output of episodic attention is then used to reweigh the decoder's self-attention to the stored KV cache of the context” specifically “for generalizing to longer contexts” (16k-256k tokens) — a context-window extension architecture, not cross-session persistence (T4/E1).

### Paper 15120 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=15120 criteria=28

**Rationale:** The document explicitly states “No memory architecture... or integration recipe is disclosed” — a doctrinal/legal-style specification about memory “admissibility” with no memory mechanism proposed or evaluated (T5).

### Paper 13829 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=13829 criteria=27

**Rationale:** “we provide a review of the current efforts to develop LLM agents... we examine the memory management approaches used in these agents” — an explicit review (D1/E4).

### Paper 19981 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=19981 criteria=26

**Rationale:** SkillComposer “predict[s] an executable skill plan” by selecting/ordering from “a real, human-curated skill library” — composition over a pre-existing curated library, with no description of the agent authoring new memory entries at run time (T2/E3).

### Paper 14726 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14726 criteria=29

**Rationale:** NaQ is “a data augmentation strategy that transforms standard video-text narrations into training data for a video query localization model” on Ego4D — a supervised video-language grounding method with no LLM-based agent described (D2/E6).

### Paper 19468 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=19468 criteria=27

**Rationale:** “The present survey examines the role of big data analytics in advancing remote sensing and geospatial analysis”, with LSTM as one of several ML techniques — an explicit survey unrelated to agent memory (D1/E4).

### Paper 16237 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=16237 criteria=24

**Rationale:** H2M2 proposes “an asymmetric memory architecture consisting of capacity-centric and bandwidth-centric memory” for GPU LLM inference — a hardware memory management paper, not cross-turn agent state (T1/E1).

### Paper 14036 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14036 criteria=28

**Rationale:** “LLM-powered agents, equipped with profile and memory modules, simulate the forgery creation process” — memory is named only as one equipped module, never elaborated or evaluated; the contribution is the forgery-data generation/detection pipeline (T5).

### Paper 14386 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14386 criteria=28

**Rationale:** The study measures human “long-term retention of productive vocabulary” after using an LLM chatbot for language learning — human learner memory, with no agent-authored memory mechanism described (T5).

### Paper 17047 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=17047 criteria=26

**Rationale:** MAIN-RAG has “multiple LLM agents collaboratively filter and score retrieved documents” pulled from external retrieval each query, with no persistent store the agents write to across turns — a classical RAG filtering improvement (T2/E3).

### Paper 15753 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=15753 criteria=30

**Rationale:** Same “PerLTQA” dataset/authors as record 15994 (“Memory Classification, Retrieval, and Synthesis” vs. “...and Fusion”) — a duplicate of another record in this batch (D3/E7).

### Paper 14003 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14003 criteria=27

**Rationale:** “This survey carefully analyzes 72 studies on LLM-based medical agents... and systematically introduces a structured taxonomy” — an explicit survey (D1/E4).

### Paper 14122 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14122 criteria=24,29

**Rationale:** The contribution is enlarging attendable past context ('LongMem can thus memorize long past context... typically enlarge the long-form memory to 65k tokens... to benefit various downstream tasks' via in-context learning), which T4 treats as more room rather than a policy over what persists; the abstract never frames this as an interactive agent, only a language-modeling backbone, so no cross-turn agent state is described (E6).

### Paper 19071 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=19071 criteria=25,26

**Rationale:** Compares only two static substrates -- 'per-user gamma-LoRA (a small LoRA adapter trained on each user's history)', a parametric mechanism with no run-time externalised store (E2), against 'BGE-large dense top-K retrieval', a fixed-corpus classical RAG comparator (E3). No mechanism where an agent itself writes memory at run time is described.

### Paper 18641 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=18641 criteria=24,29

**Rationale:** Mela integrates the Hierarchical Memory Module into a Transformer decoder to 'perform online memory consolidation at test time' so that it 'maintains performance on significantly longer contexts, whereas Transformer baselines degrade rapidly' -- an architecture-level context-extension contribution (T4->E1), evaluated purely as a language model with no agent, turns or sessions described (E6).

### Paper 14969 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14969 criteria=25

**Rationale:** The only memory-adjacent content is verifying 'the model retains its general capabilities without significant catastrophic forgetting after training' following knowledge distillation and fine-tuning -- a parametric, weights-only effect with no externalised store an agent reads or writes, and no agent or cross-turn behaviour is described at all.

### Paper 14517 excluded at screening
_2026-08-30T18:52:11Z · exclusion_screening · proposed by agent:screener_

paper_id=14517 criteria=25

**Rationale:** Echo's episodic-memory capability is instilled by training: 'Temporal information is innovatively incorporated into the LLM training process, and Echo is trained using the EM-Train' -- this is a parametric fine-tuning approach baking episodic recall into weights, with no externalised store the deployed agent writes to or reads from at run time.

## Exclusions during eligibility

### Paper 13796 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=13796 criteria=

**Rationale:** The paper's own contribution list (p. 2) names four things: (1) identifying Memory Control Flow Attacks (MCFA) as a security threat, (2) a taxonomy of control-flow deviation types, (3) the MEMFLOW automated evaluation/attack framework, and (4) a large-scale evaluation of MCFA against GPT-5 mini, Claude Sonnet 4.5 and Gemini 2.5 Flash. None of these is a memory write/retrieve mechanism. The agent memory that is read and written (Definition 1's Φret/Φupd, and the 'Naive vs. RBMS' Persistent Memory architectures described as the 'Victim System' in Appendix A.1, p. 13) is treated only as the pre-existing, generic attack surface MEMFLOW configures and probes ('Agent Runner ... defines execution settings for agent models, memory mechanisms, and tool frameworks', p. 2) — it is not proposed, designed, or argued for by this paper. Memory is central to the threat model but is not part of the claimed contribution itself, which is the attack/evaluation methodology, so this falls under E5.

### Paper 13810 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=13810 criteria=

**Rationale:** The evaluated pipelines (SH-CONFLICT and CAR) only read from a fixed, pre-built corpus C = {(s_i, t_i)} of numbered facts via BM25 retrieval and then execute a policy (select the candidate with the largest version serial) over the retrieved evidence (Section 3, p. 4, including the sh_conflict and car pseudocode). The corpus itself is the MemoryAgentBench FactConsolidation benchmark's pre-constructed memory of counterfactual-versioned facts, built by the benchmark rather than written by the agent under test at run time ('FactConsolidation ... builds a memory of numbered facts in which a counterfactual version carries a higher serial than the original', p. 1). Across the sampled pages (1-4, 9-12), no write, update, or persistence operation performed by the agent onto this or any other store is described; the entire contribution is about post-retrieval assembly (evidence extraction plus policy execution) on the read side (Contributions list, p. 3). This fails I1 (no agent-authored write to an externalised store as part of the contribution) and matches E3 (retrieval over a fixed corpus the agent never writes to).

### Paper 14072 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=14072 criteria=

**Rationale:** LSTM-MAS is a multi-agent pipeline for processing one long document/query in a single pass, not a mechanism that gives an agent state persisting across turns or sessions. Section III.A defines the task as a single (x, y, q) triple: the long context x is split into blocks and fed sequentially through the agent chain 'to simulate the sequence expansion of LSTM time steps' (p. 3). Algorithm 1 (p. 5) shows the 'long-term memory' bank C0 is initialised empty at the start of each such run and is consumed entirely within that one forward pass, ending in 'return LLM_M(...)' as the final answer to that query -- nothing is written for a later, separate turn or session to retrieve. This is the architecture-level long-context category the paper itself sets out to compete in: the abstract and related work (p. 1-2) frame it against methods that 'reduce the context window' or 'extend the context window' (RAG, positional-encoding tricks, fine-tuning), i.e. it is offered as an alternative way to fit more input into one query, not a policy over what an agent carries forward between separate interactions. No cross-turn or cross-session agent state semantics are described anywhere in the extracted pages.

### Paper 14210 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=14210 criteria=

**Rationale:** The record's own contribution is an independent reproducible testbed and cost/accuracy benchmarking methodology for comparing existing LTM frameworks (mem0, Graphiti, cognee) against RAG and full-context baselines in a simulated cloud-edge DMAS — not a mechanism by which an agent writes and retrieves its own memory. The contributions list on p. 2 names three items: 'a testbed for evaluating LTM frameworks in a DMAS', 'independent benchmarks of three LTM frameworks funded by venture capital ... including full-context and RAG baselines, using LoCoMo as the source', and 'evaluations under unconstrained and constrained network scenarios'. None of these is a memory-write/retrieve mechanism the paper argues for; the mem0/Graphiti/cognee mechanisms belong to the systems under test, described only in related work (p. 2), and this paper does not modify or propose one. p. 8-9 report only comparative accuracy/cost/latency results across those third-party systems. No axis can be coded to a mechanism this record itself contributes.

### Paper 14538 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=14538 criteria=

**Rationale:** The paper is a position/risk-analysis piece, not a contribution of a run-time write/retrieve mechanism. The abstract (p. 1) states the contribution as outlining risks and benefits and proposing 'four principles to guide the development of episodic memory capabilities' — not a mechanism the authors built. Section II (Related Work, p. 2) discusses other systems (MemGPT, Voyager, RAG-based approaches) only as background citations, not as this paper's own contribution. Section IV (Risks of Episodic Memory, p. 5) analyzes hypothetical deception, privacy, and unpredictability risks of future systems having episodic memory, again without proposing or evaluating an agent-authored store. No externalised store is written to or read from by an agent as part of this record's own claimed contribution, so I1 is not satisfied.

### Paper 14586 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=14586 criteria=

**Rationale:** MemVLN's 'episodic memory' is a pyramidal-resolution rescaling function applied deterministically to the entire raw observation history Ht={v0,...,vt-1} by temporal distance (Eq. 1, Sec. 3.2, p. 5): recent frames keep full resolution, older frames are spatially downsampled, but nothing is ever selectively written or queried out of an addressable store — the whole history is always processed, just at reduced fidelity. Section 3.1 (p. 4) confirms the architecture simply 'selects a subset St ⊂ Ht' via this fixed function before every LVLM forward pass, and Section 5/'Preliminary: Why not Token Merging?' (p. 5) explicitly positions pyramidal resolution as a substitute for token-merging 'sequence compression and memory control' techniques (Uni-Navid, StreamVLN) used purely to fit long visual context into a fixed budget for real-time inference (14 FPS, p. 1 abstract; p. 2 intro). This is an inference-time context/cache compression technique with no genuine agent-authored write or query semantics beyond ordinary causal history. The 'procedural memory' (Sec. 3.1, p. 4; augmented action vocabulary, Appendix E and Table 8, p. 14-15) is likewise not a store: it is a fixed, pre-defined atomic-action vocabulary substituted for auto-regressive decoding to cut latency (~70ms vs >300ms, Fig. 2, p. 4), with no run-time write step and no cross-turn retrieval of agent-authored content. Both mechanisms are architecture/latency contributions dressed in a biological-memory metaphor (Fig. 1, p. 1) rather than an externalized store the agent writes to and later retrieves from to condition future behaviour, matching E1.

### Paper 15338 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=15338 criteria=

**Rationale:** The paper's primary contribution, Causal Memory Intervention (CMI), is a selection rule over a memory bank that is fixed per example and never written to by the method being coded: Section 5.1 (p. 6) states 'each method receives the same current task and candidate memory bank, but differs in which memories it selects or exposes to the response model,' and the CMI selection rule in Section 3.4 (p. 5) only computes Utility/Stability over existing candidate memories mi to decide inclusion (Utility(mi) > 0, Stability(mi) >= 0) — there is no step where the agent authors or updates memory content. The memory bank itself (useful, irrelevant, and synthetic harmful memories) is constructed offline by an LLM-assisted pipeline before evaluation (Section 4, p. 6: '100 candidate CAUSAL-LOCOMO examples from LoCoMo using GPT-5 as the dataset construction model' followed by deterministic filtering), not written at run time by the agent whose behaviour is being conditioned. This matches E3: retrieval/selection over a fixed corpus the agent never writes to, so I1 (an agent-authored, run-time-written, later-retrieved store) is not met by the coded contribution. Baselines named alongside CMI (vector, graph, reflection, summary, full-history, no-memory; Section 5.1, pp. 6-7) are alternative selection/retrieval strategies over the same fixed bank, not writing mechanisms that change this judgement for the primary contribution.

### Paper 15702 excluded at eligibility
_2026-08-30T19:21:11Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=15702 criteria=

**Rationale:** The contribution is a benchmark (ES-MemEval) and an accompanying static multi-session dataset (EvoEmo) for evaluating memory capabilities of existing LLM systems on QA, summarization and dialogue-generation tasks over a fixed pre-recorded conversation transcript (p. 1, abstract: 'we introduce ES-MemEval, a comprehensive benchmark...To support the benchmark, we also propose EvoEmo, a multi-session dataset'). The evaluated systems are off-the-shelf long-context models fed the full given history, and RAG variants where 'a dense retriever (bge-m3) retrieves the top-4 most relevant full-session contexts from a FAISS index to supply user information' (p. 6, Section 5). In both cases the store being read is the fixed, pre-existing dialogue transcript supplied as benchmark input, not a store the agent itself writes to at run time during the interaction; no page given describes an agent deciding what to write into a memory store or a write-then-later-retrieve loop that conditions the agent's own future behaviour (I1 not met). This matches E3: retrieval over a fixed corpus the agent never writes to.

### Paper 19070 excluded at eligibility
_2026-08-30T19:21:12Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=19070 criteria=

**Rationale:** The record's own contribution is TriggerBench, a 1,265-task benchmark for measuring prospective memory (PM) in LLMs/agents (p. 1 abstract: 'We introduce TriggerBench, a comprehensive PM benchmark'; p. 2: 'we introduce TriggerBench, a comprehensive benchmark of 1,265 PM tasks spanning five dimensions'). The memory-writing/retrieving mechanisms present in the record are the evaluated baselines, not the paper's contribution: p. 16 (§B.2) lists 'Memory Systems' — A-MEM, Mem0, and a simplified Letta-Sim — as third-party methods being benchmarked ('We evaluate three families of approaches on TriggerBench... Memory Systems include three frameworks that utilize semantic search over LLM-curated memory items'), and p. 29's case study shows Letta-Sim's write-time curation to core memory succeeding where RAG/A-MEM/Mem0 fail, again as an evaluated external system rather than an authored mechanism. Long-context models and RAG are likewise evaluated baselines (p. 16). No page given shows TriggerBench itself specifying a store the agent writes to and later reads from as part of its own contribution — the contribution is the benchmark/dataset and its evaluation protocol (p. 1-2, p. 32-33 blueprint examples). Memory-write/retrieve semantics are therefore present in the record but not part of the claimed contribution (E5).

### Paper 19291 excluded at eligibility
_2026-08-30T19:21:12Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=19291 criteria=

**Rationale:** AgentIR's contribution is entirely on the retrieval side of the pipeline: a workload-adaptive fusion/cascade router and a time-partitioned index over records that are ingested from the agent's own conversation trace (p. 3: 'Modern LLM agents ... produce memory traces comprising user messages, assistant responses, tool calls ... Each record is annotated with timestamps, session identifiers, agent identifiers, and tool types'). Nothing in the given pages describes an agentic write decision -- what gets stored, synthesised, or evicted -- as part of the contribution; the record stream is logged wholesale, not authored by the agent choosing what to persist. The paper explicitly disclaims the write side as someone else's layer: 'AgentIR's contribution is orthogonal and complementary ... the retrieval substrate itself should be agent-aware ... not just the memory-management layer above it. A production deployment can combine, e.g., Mem0's write-batching policy with AgentIR's retrieval substrate' (p. 17). The evaluation throughout (Tables/figures on pp. 2-3, 17-18) reports nDCG@10, Recall@k, Hit@k and latency over BEIR/LongMemEval/LoCoMo as fixed IR benchmarks, i.e. retrieval quality/speed over a growing but agent-independent log, not evidence of a memory mechanism that conditions the agent's own future behaviour. This matches E3: retrieval infrastructure over a corpus the agent itself never decides to write to; the paper's own framing (p. 17) confirms the write/memory-management layer is out of scope for its contribution.

### Paper 19507 excluded at eligibility
_2026-08-30T19:21:12Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=19507 criteria=

**Rationale:** The paper's contribution is the CAPA benchmark and an inference-time 'same-user history gating' method that reads a user's previously resolved coding sessions to resolve recurring ambiguity (p. 1 abstract; p. 2 contributions list). Those prior-session histories are synthetically constructed by the paper's own three-stage generation pipeline (p. 2, 'A data generation pipeline' contribution), not written by the coding-assistant agent under test at run time. The evaluated mechanism (p. 7, 'A lightweight same-user history gating method') is a gate LLM that reviews this already-fixed resolved history and highlights evidence to add to context -- a retrieval/filter over a fixed corpus the agent never writes to, matching E3. The mem0 and A-mem systems the paper compares against (p. 7, Table 4) do write agent-authored stores, but they are baselines the paper argues against, not the record's own contribution -- the paper's own gating approach explicitly works by 'reviewing the resolved history' directly rather than writing a store, and outperforms both memory baselines on FT-ES/TTC (p. 7).

### Paper 20081 excluded at eligibility
_2026-08-30T19:21:12Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=20081 criteria=

**Rationale:** The system's 'experience memory' stores records e = (scene features, score vector, best strategy, best margin) that the Strategy Router 'consults' to pick a retrieval strategy (p. 2, Section 2.2), and Section 2.3 describes it as 'reusable experience records' that are looked up (p. 3). No page describes the agent writing new entries to this store at run time: the strongest reported setting is a static 'rule-based routing' table mapping task types to fixed strategies ('maps direct tasks to dense, and both multi hop and scientific tasks to hybrid rrf', p. 2), and the learned-routing variants that were tried are reported as underperforming and not adopted (p. 2, and Appendix A.2 on p. 5). The evaluation in Section 3 (pp. 3) measures only retrieval quality (Recall@10/MRR@10/nDCG@10) against a fixed candidate pool, with no measurement of any write, update, or persistence-across-sessions process for the experience memory. This is retrieval over a store the agent is never shown writing to (E3); the pages given do not evidence the run-time write-and-later-retrieve-across-turns mechanism required by I1.

### Paper 20436 excluded at eligibility
_2026-08-30T19:21:12Z · exclusion_eligibility · proposed by agent:classifier_

paper_id=20436 criteria=

**Rationale:** MemChain's own contribution is explicitly scoped to post-retrieval processing of an already-retrieved candidate set, not to writing the memory store. Section 2.1 states 'MemChain instead leaves M unchanged and learns the temporary mapping (q, Cq) -> E' (p. 3), and the introduction states 'MemChain leaves retrieval and memory writing fixed; it learns the post-retrieval transformation from Cq to E' (p. 2). The memory pool M is treated as a fixed store the mediator reads from but never writes to; its output E ('active memory') is 'exposed only to the frozen answer model' for the current query (p. 3), with no mechanism shown for E or any agent-authored content to persist into later turns or sessions. The Conclusion/Limitations even flag this as future work: 'Future work will... extend MemChain to richer, continually updated memory stores' (p. 9), confirming the present contribution does not update the store. This is retrieval/post-retrieval transformation over a fixed candidate pool (E3); it does not meet I1, since the claimed contribution contains no mechanism by which the agent itself writes state at run time for later cross-turn or cross-session retrieval.

## Notes

### Execution environment: local sqlite, not the shared remote database
_2026-08-30T18:26:09Z · note · proposed by agent_

The study is executed against a local sqlite workspace. An initial attempt against the shared remote database was abandoned after the first search strand: storing 410 records took roughly fifteen minutes, because identification writes one row per record over the network.

**Rationale:** Recorded so that the absence of this project from the shared database is a documented choice rather than an inconsistency. The protocol is identical in both; this script is the authoritative statement of it, and its git commit predates the first search.

### Semantic Scholar removed from the provider set
_2026-08-30T18:32:03Z · note · proposed by agent_

Semantic Scholar answered every anonymous request with HTTP 429, across two execution environments and roughly forty minutes of attempts. It was removed. The database search ran on arXiv and OpenAlex only. PubMed was never queried: it indexes biomedical literature and this population is LLM agent systems.

**Rationale:** The 429 is an API-key requirement, not a throttle a backoff can outwait; the retry logic inherited from the previous study cost three minutes per query and returned nothing. Two search engines scores zero on DARE criterion QC2, which asks for four or more reputable digital libraries. OpenAlex aggregates IEEE, ACM, Springer and Elsevier records so venue coverage is wider than the engine count suggests, but that is a mitigation and not a defence, and it is reported as a coverage limitation.

### Identification is cap-bound in 34 of 36 provider runs
_2026-08-30T18:35:46Z · note · proposed by agent_

Eighteen queries were run against two providers at a fetch cap of 200 records per provider run. 7032 gross hits yielded 3862 unique records. Thirty-four of the thirty-six runs returned exactly 200 and are therefore truncated: the true match set is larger than what was fetched, by an unknown amount.

**Rationale:** arXiv hard-caps at 200 and does not paginate, so raising the cap is not available. The corpus is consequently a relevance-ranked slice of each query's match set, and every count derived from it is a property of two rankers before it is a property of the field. Two things carry the study instead of a completeness claim: eighteen queries rather than one, so the slices overlap and no single ranking decides membership; and a seeded random draw for screening, so the sampling is defensible even where the retrieval is not. Stated as the coverage limitation it is.

### One record dropped at a text-integrity check
_2026-08-30T19:18:58Z · note · proposed by agent_

A classifier reported that the pages extracted for record 19017 were the text of a different paper. A title-match check was then run over all 171 records with retrieved text: 170 passed, 1 failed, and the one failure was that record. It is excluded from the classification sample and reported as its own line in the flow diagram; the classification sample is therefore 79, not the 80 drawn.

**Rationale:** The mismatch was found by a coder, not by the pipeline, which means the pipeline had no such check. Adding one and running it over the whole corpus turns an anecdote into a measured rate: 1 in 171. The record is dropped rather than re-fetched because any facet assigned to it was assigned from another paper's text, and re-reading cannot repair a row whose provenance is already wrong. The check is scripts/agentmem/35-text-integrity.py and its output is in the replication package.


