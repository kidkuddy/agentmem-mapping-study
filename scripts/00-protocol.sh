#!/usr/bin/env bash
# Protocol for the LLM agent-memory systematic mapping study.
#
# Everything here MUST run before the first search (petersen.md §6.12 step 1).
# It creates the project and topic, declares the study design, the four research
# questions, the eleven screening criteria, and every facet axis whose values are
# known a priori.
#
# The `substrate`, `write_policy` and `retrieval_policy` axes ARE declared here
# with provisional values, and that is a deviation from the cogbias run, where
# the derived axis was withheld until keywording. The reason is scope: those three
# axes are the ones the research questions are written against, and a one-day
# execution has no room to re-code the corpus if keywording reshapes them. They
# are declared provisional and reconciled against the keywording pass in
# 60-keyword-substrate-axis.py; any value the corpus does not occupy, and any
# value the corpus needs that is absent here, is logged as a scope_change.
#
# Writes the resulting ids to scripts/agentmem/ids.env.
set -euo pipefail
cd "$(dirname "$0")"
set -a; . ./local.env; set +a   # local sqlite, not the remote Turso database

j() { python3 -c 'import json,sys; print(json.load(sys.stdin)["'"$1"'"])'; }

if [ -f ids.env ]; then
  . ./ids.env
  echo "reusing project=$PROJECT_ID topic=$TOPIC_ID"
else
  PROJECT_ID=$(phd project create \
    -name "Design Patterns for LLM Agent Memory" \
    -owner "kidkuddy" \
    -description "Systematic mapping study (Petersen 2008/2015) with a multivocal grey-literature stratum (Garousi et al. 2019) of memory mechanisms in LLM-based agents, 2023-2026." \
    -research-question "What memory design patterns exist in LLM-based agent systems, how are they realised and evaluated, and which substrate/policy combinations does peer-reviewed research leave to practice?" \
    | j project_id)

  TOPIC_ID=$(phd topic create \
    -project-id "$PROJECT_ID" \
    -name "LLM agent memory design patterns" \
    -description "Primary and only topic. Two strata: peer-reviewed literature and a declared enumeration of practitioner systems. Unit of classification is the record's primary memory mechanism." \
    -research-question "What memory design patterns exist in LLM-based agent systems, how are they realised and evaluated, and which substrate/policy combinations does peer-reviewed research leave to practice?" \
    | j topic_id)

  printf 'PROJECT_ID=%s\nTOPIC_ID=%s\n' "$PROJECT_ID" "$TOPIC_ID" > ids.env
  echo "created project=$PROJECT_ID topic=$TOPIC_ID"
fi

# --- Design -----------------------------------------------------------------
# study-design Phase 2: name the outcome variable you would compare across
# studies. There isn't one, so this is a map, not an SLR.
phd topic set-type -id "$TOPIC_ID" -type mapping -rationale \
"No outcome variable is comparable across studies. Papers report task success on incomparable benchmarks (LoCoMo, MemGPT's own task suite, bespoke agent environments) under incomparable memory budgets and context lengths, so nothing can be aggregated. The answerable question is what memory designs exist and which combinations nobody has studied, which is Petersen's what-exists/what-is-missing test rather than Kitchenham's what-does-the-evidence-say. Aggregating memory effectiveness was considered and rejected: it would require an SLR with quality assessment over effect measures that are not commensurable." >/dev/null

# --- Research questions, one per facet axis ---------------------------------
phd rq add -topic-id "$TOPIC_ID" -label RQ1 -answered-by facet:substrate \
  -text "Which storage substrates do LLM-agent memory mechanisms use, and how has their distribution changed over 2023-2026?" >/dev/null
phd rq add -topic-id "$TOPIC_ID" -label RQ2 -answered-by facet:write_policy \
  -text "Which write and retrieval policies govern agent memory, and which substrate-by-policy combinations occur in practice?" >/dev/null
phd rq add -topic-id "$TOPIC_ID" -label RQ3 -answered-by facet:research_type \
  -text "With which research types and research methods is agent memory investigated, and which substrates have never been evaluated in a deployed setting?" >/dev/null
phd rq add -topic-id "$TOPIC_ID" -label RQ4 -answered-by facet:stratum \
  -text "Which substrate and policy combinations do practitioner systems occupy that the peer-reviewed literature does not?" >/dev/null

# --- Screening criteria (title/abstract) ------------------------------------
inc() { phd criterion add -topic-id "$TOPIC_ID" -stage screening -kind inclusion -accept -proposed-by agent -text "$1" -rationale "$2" >/dev/null; }
exc() { phd criterion add -topic-id "$TOPIC_ID" -stage screening -kind exclusion -accept -proposed-by agent -text "$1" -rationale "$2" >/dev/null; }

inc "I1 The record's claimed contribution includes a mechanism by which an LLM-based agent writes state at run time and later retrieves it across turns or sessions in order to condition its own future behaviour." \
"This is the operational definition of agent memory used throughout. The run-time write is the discriminating clause: it is what separates memory from retrieval over a corpus the agent cannot change."
inc "I2 Published, released or first preprinted on or after 2023-01-01." \
"MemGPT, Generative Agents and Reflexion all appear in 2023 and are the point at which externalised agent memory becomes a named design concern. Earlier memory-augmented language-model work belongs to a different research programme."
inc "I3 Written in English." \
"The reviewers read English. A language criterion applied silently is a validity threat; applied openly it is a stated limitation."
inc "I4 Full text is retrievable, directly or via an arXiv record under the same title." \
"Accessibility gate. Every included record must be readable by construction, so the whole corpus can be classified from full text and no false-inclusion rate has to be estimated from a validation sample."

exc "E1 'Memory' denotes hardware, GPU or DRAM memory, or inference-time cache optimisation, with no cross-turn agent state semantics." \
"The dominant source of false positives: processing-in-memory, memory-bound kernels and KV-cache throughput work share the vocabulary and share nothing else. A KV-cache paper is in scope only if the cache persists agent state across sessions."
exc "E2 Memory is exclusively parametric - fine-tuning, model editing or continual learning - with no externalised store the agent reads or writes at run time." \
"Scope decision by the principal investigator. Weight-resident knowledge is a large, mature and separate research programme; including it would roughly double the corpus without changing what the map is about."
exc "E3 Retrieval over a fixed corpus the agent never writes to (classical retrieval-augmented generation)." \
"Retrieval is not memory unless the agent authors what it later retrieves. Without this criterion the corpus becomes the RAG literature."
exc "E4 Secondary study - survey, review, systematic review or mapping study." \
"Secondary studies are the comparison this map is motivated against, so they are recorded as related work rather than as primary records."
exc "E5 Memory is mentioned only incidentally and is not part of the claimed contribution." \
"An agent paper that happens to keep a scratchpad is not a memory paper. Petersen's keywording works on the contribution claim."
exc "E6 The system is not an LLM-based agent - reinforcement-learning agent memory, or a symbolic cognitive architecture with no language model in the loop." \
"Population boundary. Prior cognitive-architecture memory work informs the discussion but is not the population being mapped."
exc "E7 Fewer than four pages, or abstract-only." \
"A record too short to state a mechanism cannot be classified on the mechanism axes."

# --- Facet axes -------------------------------------------------------------
fs() { phd facet scheme add -topic-id "$TOPIC_ID" -axis "$1" -values "$2" -rationale "$3" >/dev/null; }

fs research_type "validation,evaluation,solution,philosophical,opinion,experience" \
"Wieringa et al. 2006 as adopted wholesale by Petersen et al. 2008. Borrowed, not derived, so this map is comparable with every other Petersen map. Assigned to the peer-reviewed stratum only; practitioner records carry no research type by construction."
fs research_method "controlled_experiment,benchmark_evaluation,case_study,simulation,proof_of_concept,none" \
"Petersen 2015 lists research method alongside research type and venue type as the classification-scheme actions its rubric scores. Coding it is what lifts rubric line 4 above minimal."
fs contribution "method,tool,model,metric,framework,dataset" \
"Petersen 2008 contribution facet, with dataset added because memory benchmarks (LoCoMo and its successors) are a recurring contribution type this facet would otherwise force into 'metric'."
fs venue_type "journal,conference,workshop,preprint,grey" \
"Third scheme action in Petersen 2015. Also carries the stratum boundary: 'grey' is the practitioner enumeration."
fs substrate "prompt_resident,vector_store,graph_store,relational_db,filesystem,kv_cache,multi_store,other" \
"Derived topical axis, provisional. Values were seeded from the mechanisms named in the six secondary studies identified during scoping, and are reconciled against a keywording pass over the classification sample before any paper is coded."
fs write_policy "append_only,summarize_compress,reflect_synthesize,edit_in_place,agent_tool_invoked,none_declared" \
"Derived, provisional. What causes a memory to exist. Distinguishes a transcript log from a reflective store, which is the distinction the existing narrative surveys draw informally and inconsistently."
fs retrieval_policy "similarity_topk,recency_window,structured_query,agent_directed,always_in_context,hybrid,none_declared" \
"Derived, provisional. What causes a memory to re-enter context. agent_directed covers the case where the agent issues its own read - a tool call or a query - rather than being served a ranked slice it did not ask for."
fs stratum "peer_reviewed,grey" \
"Garousi et al. 2019 multivocal review convention. The two strata are reported as separate panels because research_type is undefined for practitioner records; the comparison between panels answers RQ4."

# --- Methodology decisions --------------------------------------------------
lg() { phd log add -project-id "$PROJECT_ID" -topic-id "$TOPIC_ID" -kind "$1" -title "$2" -content "$3" -rationale "$4" -proposed-by agent -accepted 1 >/dev/null; }

lg methodology_choice "Unit of classification: one primary memory mechanism per record" \
"Each included record is assigned exactly one value on each mechanism axis, describing the memory design its own contribution claim centres on. Records presenting several mechanisms have the secondary ones recorded as extractions rather than as additional map rows." \
"Two reasons. The map's denominator then equals the PRISMA flow's denominator, so every count in the paper reconciles against the flow diagram. And a record whose contribution is a single named design is the unit its authors themselves argue for; splitting records into mechanisms would let a paper with an elaborate architecture outvote a paper with a focused one."

lg methodology_choice "Sampling caps and seed, declared before the draw" \
"Screening cap 300 records, drawn by seeded random sample from everything surviving the automated scope filter and the accessibility gate. Classification cap 80 records, drawn by seeded random sample from the screening includes. Seed 20260830 for both draws." \
"Petersen imposes no cap, but an uncapped corpus at this scale cannot be read in full within the available time, and a corpus judged from abstracts cannot support claims about mechanism structure. A declared seeded sample is an ordinary sampling design; a top-k slice of a provider's relevance ranking is not. Both caps sit below the 120-200 primary studies an eight-page map would ideally carry, and that shortfall is reported as a limitation rather than concealed."

lg methodology_choice "Grey stratum is a declared enumeration, not an open search" \
"The practitioner stratum is the union of (a) every distinct agent-memory system named in two or more of the identified secondary studies on agent memory, and (b) the memory components documented in the official documentation of named LLM agent frameworks, with the frame fixed on 2026-08-30. No open web search contributes records." \
"An open grey search is unbounded human time and is not reproducible by a third party. A declared enumeration with a stated rule and a fixed date is a purposive sample, and is reported as one. Clause (b) exists so the grey stratum can contain designs the secondary literature has not noticed, which is exactly what RQ4 asks about."

lg methodology_choice "No target-audience consultation was performed" \
"Petersen rubric line 1 awards its top mark only when the research questions are defined together with a named target audience. No consultation was conducted." \
"The study was executed inside a single day and a documented consultation with practising agent developers could not be arranged in that window. Scored honestly as partial, which is where 100 percent of the mapping studies Petersen examined also sit. Declared here so it is a known limitation rather than an omission a reader has to detect."

lg methodology_choice "Parametric memory excluded from scope" \
"Fine-tuning, model editing and continual learning are out of scope unless combined with an externalised store the agent reads or writes at run time (criterion E2)." \
"Decided by the principal investigator. The boundary is reported so that readers who consider parametric memory part of agent memory can see exactly what was left out."

lg methodology_choice "Screening and classification performed by LLM agents" \
"Title-and-abstract screening, full-text eligibility and all facet assignments were produced by Claude-based agents working from a written coding guide, each decision carrying its decided_by field and a written justification. A second independent coder re-coded a 20 percent sample; agreement is reported per axis." \
"These are scientific judgements, not clerical ones, and both the IEEE policy and the PRISMA 2020 AI-disclosure expectations require them to be declared in the manuscript rather than only in the repository."

lg search_strategy "Three search strategies will be used" \
"Database search across the available providers; backward and forward snowballing from the most-cited included records; and manual inspection of the enumerated practitioner frame." \
"Petersen rubric line 2 scores the count of search types, and roughly 58 percent of published maps use only one. Three is the maximum the rubric recognises."

lg note "Execution environment: local sqlite, not the shared remote database" \
"The study is executed against a local sqlite workspace. An initial attempt against the shared remote database was abandoned after the first search strand: storing 410 records took roughly fifteen minutes, because identification writes one row per record over the network." \
"Recorded so that the absence of this project from the shared database is a documented choice rather than an inconsistency. The protocol is identical in both; this script is the authoritative statement of it, and its git commit predates the first search."

echo "protocol complete: project=$PROJECT_ID topic=$TOPIC_ID"
