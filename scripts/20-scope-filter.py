#!/usr/bin/env python3
"""Automated scope filter. One criterion, applied to title + abstract.

Petersen's screening is an agent judgement; this runs before it and only removes
records that cannot possibly be in scope, so that screening is not spent on the
processing-in-memory, KV-cache-throughput and memory-bandwidth literature that
dominates any query containing the word "memory".

THE ONE CRITERION
  A record is kept if its title or abstract carries a memory term in the
  AGENT-STATE sense - either (A) a loose mention of memory alongside a
  conversational or agentic context, or (B) a named memory construct, substrate
  or system - AND names an LLM or agent system.

Branch (A) exists so the filter does not bound the map's substrate axis. A paper
describing a store nobody thought to put in list (B) still survives on (A) and can
become a row in the derived scheme. A filter that was list (B) alone would make
the corpus a projection of the term list, and the map's "which substrates are
used" answer would be circular.

THE SENSE DISAMBIGUATION, and why it is not a second criterion
  "Memory" in this corpus is a homonym. It denotes agent state, and it denotes
  DRAM. Bare `memor\\w+` therefore admits "Swap-Based Memory Optimization for LLM
  Training" on exactly the same evidence as "Long-Term Memory for LLM Agents",
  and both halves of the gate pass for both records.

  So the gate does not ask whether the word appears; it asks which sense matched.
  A hardware phrase - memory bandwidth, memory footprint, GPU memory, DRAM,
  memory-bound - is not a memory-sense match on its own. It is not an exclusion:
  a record carrying BOTH a hardware phrase and an agent-state phrase is kept, and
  "Agent Memory Below the Prompt: Persistent KV Cache for Multi-Agent Inference"
  is kept for that reason. KV-cache work that persists agent state across sessions
  is in scope by design (the substrate axis has a kv_cache value); KV-cache work
  that is an inference optimisation is not, and criterion E1 is what rules on it.

Nothing is excluded here for being classical RAG, parametric-only, or a secondary
study. Precision is screening's job; this is a recall gate.

Run:  python3 20-scope-filter.py            # writes scope-kept.json, scope-dropped.json
      python3 20-scope-filter.py --selftest # borderline test set, no DB access
"""
import json, os, re, subprocess, sys, pathlib

HERE = pathlib.Path(__file__).parent
# In the replication package the study data sits in ../data while the
# scripts stay in ../scripts. DATA is the only path that differs from
# the layout these scripts were executed in.
DATA = (HERE / ".." / "data").resolve()

# Same local-sqlite switch the shell scripts use.
# Point the phd CLI at the database shipped beside these scripts. The original
# study read this from a local.env; that file used shell command substitution to
# find itself, which os.path.expandvars does not evaluate, so the path is
# resolved here directly instead.
os.environ["PHD_ENV"] = str((HERE / ".." / ".no-remote.env").resolve())
os.environ["EPT_DATA"] = str(DATA)
IDS = dict(l.strip().split("=") for l in (HERE / "ids.env").read_text().splitlines() if "=" in l)

# (B) named memory constructs, substrates, policies and systems. A recall device
# for retrieval, not the classification scheme - the substrate axis is reconciled
# against a keywording pass, not against this list.
NAMED = re.compile(r"""
      agent(ic)?\s+memory
    | memory\s+(mechanism|module|system|bank|store|stream|pool|graph|base|layer|substrate|architecture|management|hierarchy)
    | (long|short)[\s-]term\s+memory
    | (working|episodic|semantic|procedural|declarative|associative|external|persistent|lifelong|parametric|non[\s-]parametric)\s+memory
    | memory[\s-]augmented
    | memory\s+(retrieval|consolidation|compression|summari[sz]ation|update|write|read|eviction|forgetting|decay|injection)
    | (retrieval|reflection|experience|knowledge|conversation|dialogue|session|user|self)[\s-]memory
    | \bMemGPT\b | \bMem0\b | \bLetta\b | \bZep\b | \bA-?MEM\b | MemoryBank | \bChatDB\b
    | \bMemoryOS\b | \bMemoRAG\b | \bHippoRAG\b | \bMemInsight\b
    | memory\s+operating\s+system
    | scratchpad | note[\s-]taking
    | cross[\s-]session | inter[\s-]session
    | persistent\s+state | state\s+persistence | stateful\s+agent
    | skill\s+library | experience\s+(replay|reuse|pool|bank)
    | context\s+(engineering|management|compaction)
    | catastrophic\s+forgetting
""", re.I | re.X)

# (A) the loose branch. Bare memory vocabulary is only a memory-sense match when
# it sits next to something conversational or agentic, which is what separates
# "the agent remembers the user's preference" from "reduces peak memory by 40%".
LOOSE_MEM = re.compile(r"\b(memor(y|ies|is|iz)\w*|remember\w*|recall(ing|ed|s)?|forget\w*|retention)\b", re.I)
LOOSE_CTX = re.compile(r"""
      \bagents?\b | conversation\w* | dialogue\w* | \bsessions?\b | assistant\w*
    | \buser'?s?\b | interaction\w* | \bturns?\b | multi[\s-]turn | chat\w*
    | long[\s-]horizon | personali[sz]\w*
""", re.I | re.X)

# The hardware sense. Present in a record, these phrases do not by themselves make
# a memory-sense match. They never veto one: see the module docstring.
HARDWARE = re.compile(r"""
      memory\s+(bandwidth|footprint|usage|consumption|capacity|allocation|access|latency|wall|bound|tier\w*|overhead|efficien\w+|optimi[sz]\w+|saving|reduction)
    | (GPU|CPU|DRAM|HBM|SRAM|VRAM|device|host|peak|physical|virtual|cache)\s+memory
    | memory[\s-]bound | out[\s-]of[\s-]memory | in[\s-]memory\s+comput\w+
    | processing[\s-]in[\s-]memory | \bPIM\b
    | KV[\s-]cache | key[\s-]value\s+cache
""", re.I | re.X)

# The other half of the criterion: the record must concern an LLM or agent system.
# Deliberately broad - this is a recall gate, and a paper that says "GPT-4" without
# ever saying "LLM" must still pass.
SYSTEM = re.compile(r"""
      \bLLMs?\b | large\s+language\s+model | language\s+model | \bLMs?\b
    | \bGPT\b | GPT-[0-9] | ChatGPT | \bClaude\b | Gemini | \bLLaMA\b | Mistral | Qwen | DeepSeek
    | foundation\s+model | generative\s+AI | \bgenAI\b
    | \bagents?\b | \bagentic\b | multi[\s-]agent
    | chatbot | conversational\s+(agent|AI|system) | dialogue\s+system | assistant
    | \bRAG\b | retrieval[\s-]augmented
    | artificial\s+intelligence | \bAI\b
    | transformer | neural\s+(network|model) | model\s+weights
    | in[\s-]context\s+learning | instruction[\s-]tuned | \bRLHF\b
""", re.I | re.X)


def classify(title, abstract):
    """Return (keep, branch) for one record.

    Two halves, both required: the record must carry a memory term in the
    agent-state sense, AND name an LLM or agent system."""
    text = f"{title or ''}\n{abstract or ''}"
    if not SYSTEM.search(text):
        return False, None
    # NAMED is matched against untouched text: an agent-state phrase counts
    # whatever else the record also says, so a paper that persists agent state in
    # a KV cache is kept even though it talks about caches throughout.
    named = bool(NAMED.search(text))
    # The loose branch is evaluated with hardware phrases removed, so "reduces
    # peak memory by 40%" cannot supply the memory half by itself.
    stripped = HARDWARE.sub(" ", text)
    loose = bool(LOOSE_MEM.search(stripped)) and bool(LOOSE_CTX.search(text))
    if named and loose:
        return True, "both"
    if named:
        return True, "named"
    if loose:
        return True, "generic"
    return False, None


# Acronym pairs that split one paper into two records. "Split and Merge:
# Aligning Position Biases in LLM-based Evaluators" and "...in Large Language
# Model based Evaluators" are the same paper under two titles, and a literal
# title key admits both.
ACRONYM = [
    (r"multimodal large language models?", "mllm"),
    (r"large language models?", "llm"),
    (r"vision[\s-]language models?", "vlm"),
    (r"pre[\s-]?trained language models?", "plm"),
    (r"reinforcement learning from human feedback", "rlhf"),
    (r"chain[\s-]of[\s-]thought", "cot"),
    (r"retrieval[\s-]augmented generation", "rag"),
    (r"artificial intelligence", "ai"),
    (r"\bbased\b", ""),
]


def norm_title(t):
    """Normalisation key for joining and for duplicate detection.

    Title alone, not title + first-author + year: that key splits a 2023 preprint
    from its 2024 proceedings version into two fingerprints and admits both
    (petersen.md 6.8). Acronyms are folded first, because an expanded acronym
    produces exactly the same split for exactly the same reason."""
    t = (t or "").lower()
    for pat, rep in ACRONYM:
        t = re.sub(pat, rep, t)
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    # Crude singularisation. "...Alignment in LLM" and "...Alignment in LLMs" are
    # one paper listed twice, differing by a single truncated character, and a
    # literal key admits both. Words of three letters or fewer and -ss endings
    # are left alone so "bias" does not become "bia".
    return " ".join(w[:-1] if len(w) > 3 and w.endswith("s") and not w.endswith("ss") else w
                    for w in t.split())


def load_run_text():
    """Abstracts come from text-index.json, built by 11-capture-text.sh.

    They are not in the database's reach: `phd paper list` returns no abstract
    column, `phd export csv` does not emit one, and a stored `phd search`
    returns paper_ids only. Reading them per paper would be ~1500 round trips
    to a remote database to fetch text that one pass of dry-run searches
    already has."""
    idx = DATA / "text-index.json"
    if not idx.exists():
        sys.exit("run 11-capture-text.sh first (text-index.json missing)")
    return json.loads(idx.read_text())


def fetch_all(topic_id, page=200):
    out, off = [], 0
    while True:
        raw = subprocess.run(
            ["phd", "paper", "list", "-topic-id", str(topic_id),
             "-limit", str(page), "-offset", str(off)],
            capture_output=True, text=True, check=True).stdout
        batch = json.loads(raw).get("papers", [])
        if not batch:
            return out
        out += batch
        off += len(batch)
        if len(batch) < page:
            return out


def abstract_from_db(paper_id):
    """Fall back to the database for a record the dry-run capture missed.

    `phd paper list` and `phd export csv` have no abstract column, which is why
    the bulk of the text comes from the capture pass — but `phd paper get` does
    return one, and on local sqlite it costs about ten milliseconds. The capture
    pass and the storing pass are separate queries issued minutes apart, so
    provider ranking drift leaves a few hundred stored records unmatched. Judging
    those on their titles alone would drop any paper that names its bias in the
    abstract and not in the title."""
    try:
        raw = subprocess.run(["phd", "paper", "get", "-id", str(paper_id)],
                             capture_output=True, text=True, timeout=30).stdout
        return json.loads(raw).get("abstract") or ""
    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
        return ""


def resolve_shared_abstracts(rows):
    """Two records carrying the same abstract mean one of two different things.

    If their titles are the same paper, it is a duplicate the title key missed -
    a truncated subtitle, an OCR artefact ("Further -Frame" for "Further
    N-Frame"). Those fall to collapse_duplicates once flagged.

    If their titles are unrelated, one record's abstract belongs to the other
    paper. OpenAlex record 3055, titled "AI Supported Degradation of the Self
    Concept", carries the abstract of arXiv's "Towards Understanding Sycophancy
    in Language Models" verbatim. That record was screened on another paper's
    evidence.

    Ownership goes to the title sharing the most content words with the abstract;
    the loser's abstract is cleared, so it is screened on its title and counted as
    such rather than on text that is not its own.

    This is a far better detector than title/abstract word overlap, which flagged
    three records and was wrong about one of them."""
    STOP = set("the a an of and for in on to with by from is are we this that using "
               "use based study new towards toward its their our".split())

    def content(s):
        return {w for w in re.findall(r"[a-z]{4,}", (s or "").lower()) if w not in STOP}

    groups = {}
    for r in rows:
        a = (r.get("abstract") or "").strip()
        if len(a) > 200:
            groups.setdefault(a[:400], []).append(r)

    reassigned = []
    for members in groups.values():
        if len(members) < 2:
            continue
        abstract_words = content(members[0].get("abstract"))
        owner = max(members, key=lambda m: len(content(m["title"]) & abstract_words))
        owner_title = content(owner["title"])
        for m in members:
            if m is owner:
                continue
            other = content(m["title"])
            # Containment, not equality. The same paper reaches the corpus under
            # "Do LLMs Show Biases in Causal Learning?" and under that title plus
            # its subtitle, and under "Further N-Frame ..." and "Further -Frame
            # ..." where a provider dropped a character. Those are duplicates and
            # keeping the abstract is right. A title sharing almost nothing with
            # the abstract's owner is a different paper carrying borrowed text.
            overlap = len(other & owner_title) / max(1, min(len(other), len(owner_title)))
            if overlap >= 0.6:
                m["dedupe_key"] = norm_title(owner["title"])
                continue
            reassigned.append({"id": m["id"], "title": m.get("title"),
                               "source": m.get("source"),
                               "abstract_belongs_to": owner["id"],
                               "owner_title": owner.get("title"),
                               "title_overlap_with_owner": round(overlap, 2)})
            m["abstract"] = ""
    return reassigned


def collapse_duplicates(rows):
    """Title-identical records, merged to one, the rest recorded not deleted.

    The key is the normalised title alone. title+first-author+year splits a 2023
    preprint from its 2024 proceedings version into two fingerprints and lets
    both into the corpus (petersen.md 6.8). Every collision is written to
    duplicates.json for a human glance rather than silently resolved.

    The kept record is the one with the longest abstract, then the lowest id —
    a deterministic rule, so the same corpus always collapses the same way."""
    groups = {}
    for r in rows:
        groups.setdefault(r.get("dedupe_key") or norm_title(r["title"]), []).append(r)
    kept, dropped, collisions = [], [], []
    for key, members in groups.items():
        members.sort(key=lambda r: (-len(r.get("abstract") or ""), r["id"]))
        kept.append(members[0])
        if len(members) > 1:
            dropped += members[1:]
            collisions.append({
                "title": members[0]["title"],
                "kept_id": members[0]["id"],
                "dropped_ids": [m["id"] for m in members[1:]],
                "years": sorted({m.get("year") for m in members}),
                "sources": sorted({m.get("source") for m in members}),
            })
    return kept, dropped, collisions


def selftest():
    """Borderline cases only. A test set of obvious in-scope papers would be a
    test the filter cannot fail (petersen.md 6.7), so every case here is one a
    careless regex gets wrong. Titles marked (seen) are real records returned by
    the scoping dry runs; the rest are constructed boundary cases."""
    cases = [
        # (title, abstract, expected_keep, why)
        ("MemGPT: Towards LLMs as Operating Systems",
         "Virtual context management pages information between the context window and external storage.",
         True, "named system, the easy direction"),
        ("SmartSwap: Swap-Based Memory Optimization for LLM Training under Varying Operator Sequences",
         "Reduces peak GPU memory during training by swapping tensors to host memory.",
         False, "says memory five times and LLM once; hardware sense throughout - the dominant false positive"),
        ("Dalorex: A Data-Local Program Execution and Architecture for Memory-bound Applications",
         "Graph and sparse linear algebra workloads doing processing in memory.",
         False, "rank-one hit of the naive query 'LLM agent memory architecture'"),
        ("Agent Memory Below the Prompt: Persistent Q4 KV Cache for Multi-Agent LLM Inference on Edge Devices",
         "The cache is retained across sessions so an agent resumes where it stopped.",
         True, "hardware phrase AND agent-state phrase; kept, and criterion E1 is what rules on it"),
        ("Memory-Efficient Fine-Tuning of Large Language Models",
         "Low-rank adapters cut optimizer memory footprint.",
         False, "memory and LLM both present, hardware sense, no agent-state phrase"),
        ("Reconstructing Context: Evaluating Advanced Chunking Strategies for Retrieval-Augmented Generation",
         "We compare chunking strategies over a fixed document collection.",
         False, "classical RAG carries no memory term at all; dropped here rather than at E3"),
        ("Generative Agents: Interactive Simulacra of Human Behavior",
         "Agents store a complete record of experiences in a memory stream and synthesise them into reflections.",
         True, "memory stream and reflection, both named"),
        ("A Study of Long-Horizon Task Execution",
         "The assistant remembers what the user asked in earlier sessions and adapts to it.",
         True, "no named construct anywhere; survives only on branch A, which is why branch A exists"),
        ("Hippocampal replay during sleep in rodents",
         "Episodic memory consolidation depends on sharp-wave ripples.",
         False, "names two constructs, no system - the neuroscience case"),
        ("ChatDB: Augmenting LLMs with Databases as Their Symbolic Memory", "",
         True, "the relational substrate this map exists to find, and it never says 'agent'"),
        ("Evaluating Very Long-Term Conversational Memory of LLM Agents", "",
         True, "a benchmark contribution, in population"),
        ("Membership Inference Attacks on Memory in Chat Agents", "",
         True, "security angle on agent memory; in population, screening rules on I1"),
        ("Mass-Editing Memory in a Transformer",
         "We update factual associations stored in model weights at scale.",
         False, "parametric-only work with no agentic context; branch A needs one, so this "
                "never reaches screening and criterion E2 never has to fire"),
        ("Fine-Tuning as Memory: Distilling an Agent's Session History into Weights",
         "After each session the agent distils its own dialogue history into a LoRA adapter.",
         True, "the same parametric mechanism WITH an agentic context. The gate admits it and E2 "
               "decides whether an externalised store exists - a gate that pre-empted E2 here "
               "would silently narrow the scope decision the protocol reserved for screening"),
        ("Towards an Adaptable Systems Architecture for Memory Tiering at Warehouse-Scale",
         "Tiered DRAM and CXL memory for datacentre workloads.",
         False, "memory tiering is in the hardware list and no system term is present"),
        ("Cognitive Architectures for Language Agents",
         "A framework organising working memory and episodic memory for language agents.",
         True, "philosophical contribution, in population"),
    ]
    bad = 0
    for title, abstract, want, why in cases:
        got, branch = classify(title, abstract)
        if got != want:
            bad += 1
            print(f"FAIL want={want} got={got} ({branch}) :: {title[:62]} :: {why}")
    print(f"selftest: {len(cases) - bad}/{len(cases)} borderline cases pass")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)

    assert selftest() == 0, "scope filter self-test failed; not running it over the corpus"

    text_by_title = load_run_text()
    # Abstracts repaired by 22-recover-abstracts.py, applied here so that this
    # file has exactly one writer.
    patch_file = DATA / "recovered-abstracts.json"
    patch = {int(k): v for k, v in json.loads(patch_file.read_text()).items()} if patch_file.exists() else {}
    papers = fetch_all(int(IDS["TOPIC_ID"]))

    # Title-identical duplicates the database's own key did not merge. Reported,
    # never auto-deleted: a collision is a record for a human to glance at.
    groups = {}
    for p in papers:
        groups.setdefault(norm_title(p.get("title")), []).append(p["id"])
    dupes = {k: v for k, v in groups.items() if len(v) > 1}

    kept, dropped, no_text, backfilled = [], [], [], 0
    branches = {"generic": 0, "named": 0, "both": 0}
    for p in papers:
        rec = text_by_title.get(norm_title(p.get("title")), {})
        abstract = patch.get(p["id"]) or rec.get("abstract") or ""
        if not abstract:
            abstract = abstract_from_db(p["id"])
            if abstract:
                backfilled += 1
            else:
                no_text.append(p["id"])
        keep, branch = classify(p.get("title"), abstract)
        row = {
            "id": p["id"], "title": p.get("title"), "year": p.get("year"),
            "authors": p.get("authors"), "source": p.get("source"),
            "venue": rec.get("venue"), "url": rec.get("url"),
            "abstract": abstract, "scope_branch": branch,
        }
        if keep:
            kept.append(row)
            branches[branch] += 1
        else:
            dropped.append(row)

    reassigned = resolve_shared_abstracts(kept)
    kept, dup_rows, collisions = collapse_duplicates(kept)
    (DATA / "scope-kept.json").write_text(json.dumps(kept, indent=1))
    (DATA / "scope-dropped.json").write_text(json.dumps(dropped, indent=1))
    (DATA / "duplicates.json").write_text(json.dumps(collisions, indent=1))
    (DATA / "wrong-abstracts.json").write_text(json.dumps(reassigned, indent=1))
    summary = {
        "records_identified": len(papers),
        "title_identical_groups_in_corpus": len(dupes),
        "abstracts_backfilled_from_db": backfilled,
        "records_with_no_abstract_text": len(no_text),
        "passed_scope_filter": len(kept) + len(dup_rows),
        "duplicates_removed": len(dup_rows),
        "abstracts_cleared_as_another_papers": len(reassigned),
        "kept": len(kept),
        "dropped_by_scope_filter": len(dropped),
        "kept_by_branch": branches,
    }
    (DATA / "scope-summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))
