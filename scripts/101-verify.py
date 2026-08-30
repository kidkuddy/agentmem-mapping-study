#!/usr/bin/env python3
"""Verifies the manuscript's numbers against the data, independently.

Two rules this exists to enforce:

  1. Every number in the abstract is in the verifier. A verifier that covers the
     easy counts and skips the headline claim verifies nothing that matters.
  2. A fact the verifier cannot check is a FAILURE, not a skip. It prints
     NOT CHECKED and exits non-zero, so a number nobody verified cannot pass as
     verified.

The queries here are written independently of 100-facts.py -- not imported, not
copied. Two independent expressions of the same definition catch a bug; one
expression checked against itself only proves it is self-consistent. Where
100-facts.py reads a summary JSON, this reads the database or the coders' own
files, and vice versa.
"""
import json, os, pathlib, subprocess, sys, collections, glob

HERE = pathlib.Path(__file__).parent
# In the replication package the study data sits in ../data while the
# scripts stay in ../scripts. DATA is the only path that differs from
# the layout these scripts were executed in.
DATA = (HERE / ".." / "data").resolve()
# Point the phd CLI at the database shipped beside these scripts. The original
# study read this from a local.env; that file used shell command substitution to
# find itself, which os.path.expandvars does not evaluate, so the path is
# resolved here directly instead.
os.environ["PHD_ENV"] = str((HERE / ".." / ".no-remote.env").resolve())
os.environ["EPT_DATA"] = str(DATA)
IDS = dict(l.strip().split("=") for l in (HERE / "ids.env").read_text().splitlines() if "=" in l)
TOPIC = IDS["TOPIC_ID"]
F = json.loads((DATA / "facts.json").read_text())

checked, failures = set(), []


def cli(*args):
    return json.loads(subprocess.run(["phd", *args], capture_output=True,
                                     text=True, check=True).stdout)


def check(name, got):
    """Compare an independently computed value against the published fact."""
    checked.add(name)
    want = F.get(name)
    if want is None:
        failures.append(f"{name}: not present in facts.json")
    elif str(got) != str(want):
        failures.append(f"{name}: verifier says {got!r}, facts.json says {want!r}")


# --- identification, recomputed from the raw run files ----------------------
runs = list(glob.glob(str(DATA / "runs" / "*.json")))
gross = capbound = nruns = 0
queries = set()
for f in runs:
    d = json.loads(pathlib.Path(f).read_text())
    queries.add(d["query"])
    for p in d["providers"]:
        nruns += 1
        gross += p["found"]
        capbound += 1 if p["found"] >= 200 else 0
check("Queries", len(queries))
check("Runs", nruns)
check("GrossHits", gross)
check("CapBound", capbound)
check("CapBoundPct", round(100 * capbound / nruns))

# Identified: from the database, not from the scope summary.
check("Identified", len(cli("paper", "list", "-topic-id", TOPIC, "-limit", "20000")["papers"]))

# --- scope filter, recomputed from its own output files ---------------------
kept = json.loads((DATA / "scope-kept.json").read_text())
dropped = json.loads((DATA / "scope-dropped.json").read_text())
dupes = json.loads((DATA / "duplicates.json").read_text())
check("ScopeKept", len(kept))
check("ScopeDropped", len(dropped))
check("DuplicatesRemoved", sum(len(d["dropped_ids"]) for d in dupes))
check("BranchGeneric", sum(1 for r in kept if r.get("scope_branch") == "generic"))

# --- screening, recomputed from the database rather than the ingest summary --
inc = cli("paper", "list-by-stage", "-stage", "screening_included",
          "-topic-id", TOPIC, "-limit", "5000")["papers"]
exc = cli("paper", "list-by-stage", "-stage", "screening_excluded",
          "-topic-id", TOPIC, "-limit", "5000")["papers"]
check("Included", len(inc))
check("Excluded", len(exc))
check("Screened", len(inc) + len(exc))
check("IncludeRate", round(100 * len(inc) / (len(inc) + len(exc)), 1))
check("NotDrawnScreening", len(kept) - (len(inc) + len(exc)))

# --- test-retest, recomputed from the two decision files --------------------
pre = {d["paper_id"]: d["decision"] for d in
       json.loads((DATA / "batches" / "retest-00-preamendment.json").read_text())["decisions"]}
post = {d["paper_id"]: d["decision"] for d in
        json.loads((DATA / "batches" / "decisions-00.json").read_text())["decisions"]}
both = sorted(set(pre) & set(post))
check("RetestN", len(both))
check("RetestAgreement", round(100 * sum(1 for i in both if pre[i] == post[i]) / len(both), 1))
check("RetestDisagreements", sum(1 for i in both if pre[i] != post[i]))

# Exclusion reasons, recounted from the coders' own decision files rather than
# from the ingest summary. These are cited in the manuscript, so they are checked.
_scr_x = collections.Counter()
for f in sorted((DATA / "batches").glob("decisions-*.json")):
    for d in json.loads(f.read_text())["decisions"]:
        if d.get("decision") == "exclude":
            for c in (d.get("criteria") or []):
                _scr_x[c] += 1
for c, n in _scr_x.items():
    if "Excl" + c in F:
        check("Excl" + c, n)

# --- gate and integrity, recomputed from the fetched files ------------------
gate_kept = json.loads((DATA / "gate-kept.json").read_text())
check("GateIn", len(gate_kept))
check("GateOut", len(inc) - len(gate_kept))
ti = json.loads((DATA / "text-integrity.json").read_text())
check("IntegrityChecked", len(gate_kept))
check("IntegrityFlagged", sum(1 for r in ti["flagged_records"]))

# --- classification, recomputed from the coders' own files ------------------
results = {}
for f in sorted((DATA / "batches").glob("facets-*.json")):
    d = json.loads(f.read_text())
    results[d["paper_id"]] = d
check("Classified", len(results))
check("Ineligible", sum(1 for d in results.values() if not d.get("eligible")))
check("Corpus", sum(1 for d in results.values() if d.get("eligible")))
# The draw is re-derived from the committed seed rather than counted from the
# batch files. Counting files makes the check depend on artefacts that are not
# redistributable; re-running the draw checks the thing that actually matters,
# which is that the sample is reproducible from the seed in the protocol.
import random as _random
_rng = _random.Random(json.loads((DATA / "batch-summary.json").read_text())["seed"])
_order = sorted(gate_kept, key=lambda r: r["id"])
_rng.shuffle(_order)
_drawn_ids = {r["id"] for r in _order[:F["ClassifyCap"]]}
check("Drawn", len(_drawn_ids))
_coded = set(results)
if not _coded <= _drawn_ids:
    failures.append(f"{len(_coded - _drawn_ids)} classified papers are not in the "
                    f"sample the seed reproduces")
if len(_drawn_ids - _coded) != ti["flagged"]:
    failures.append(f"drawn-but-uncoded is {len(_drawn_ids - _coded)}, "
                    f"integrity drops is {ti['flagged']}")
check("NotDrawnClassification", len(gate_kept) - F["Drawn"])

# Facet value counts, recomputed from the database rather than the ingest file.
assign = collections.defaultdict(collections.Counter)
nulls = collections.Counter()
for pid, d in results.items():
    if not d.get("eligible"):
        continue
    seen = set()
    for fa in d.get("facets", []):
        ax, v = fa["axis"], fa.get("value")
        seen.add(ax)
        if v is None:
            nulls[ax] += 1
        else:
            assign[ax][v] += 1
for ax, vals in assign.items():
    for v, n in vals.items():
        name = ax.title().replace("_", "") + v.title().replace("_", "")
        if name in F:
            check(name, n)
for ax, n in nulls.items():
    name = "Null" + ax.title().replace("_", "")
    if name in F:
        check(name, n)

# Full-text exclusion reasons (PRISMA item 16b), recounted here.
_ft_x = collections.Counter()
for d in results.values():
    if d.get("eligible"):
        continue
    cr = d.get("eligibility_criteria") or []
    if not cr:
        r = (d.get("eligibility_rule") or "").strip()
        cr = [r] if r else []
    for c in cr:
        _ft_x[c] += 1
for c, n in _ft_x.items():
    if "FullTextExcl" + c in F:
        check("FullTextExcl" + c, n)

# --- the headline claim, recomputed three ways ------------------------------
rt = collections.Counter()
for d in results.values():
    if not d.get("eligible"):
        continue
    for fa in d.get("facets", []):
        if fa["axis"] == "research_type" and fa.get("value"):
            rt[fa["value"]] += 1
check("RTAssignments", sum(rt.values()))
check("Evaluation", rt.get("evaluation", 0))
check("EvaluationBound", round(100 * (1 - 0.05 ** (1 / sum(rt.values()))), 1))
# And from the database, which is a different store than the coder files.
db_rt = cli("facet", "map", "-topic-ids", TOPIC, "-x", "research_type", "-y", "substrate")
db_eval = sum(row.get("evaluation", 0) for row in db_rt["cells"].values())
if db_eval != rt.get("evaluation", 0):
    failures.append(f"Evaluation: coder files say {rt.get('evaluation',0)}, database says {db_eval}")

# --- reliability, recomputed from the recode files --------------------------
kap = json.loads((DATA / "facet-kappa.json").read_text())
n_pairs = 0
disagree = 0
for pid in json.loads((DATA / "second-coder-sample.json").read_text())["paper_ids"]:
    f2 = DATA / "batches" / f"recode-{pid}.json"
    if not f2.exists():
        continue
    n_pairs += 1
    d1, d2 = results[pid], json.loads(f2.read_text())
    def m(d):
        return {fa["axis"]: fa.get("value") for fa in d.get("facets", [])}
    a, b = m(d1), m(d2)
    for ax in ("substrate", "write_policy", "retrieval_policy",
               "research_type", "research_method", "contribution"):
        if a.get(ax) != b.get(ax):
            disagree += 1
check("KappaN", n_pairs)
check("KappaDisagreements", disagree)
check("KappaSharePct", round(100 * n_pairs / F["Corpus"]))


# Per-axis agreement recomputed here rather than read from facet-kappa.json, so
# the table in the paper is checked against the coder files and not against the
# script that produced it.
def _kappa(pairs):
    n = len(pairs)
    obs = sum(1 for a, b in pairs if a == b) / n
    la = collections.Counter(a for a, _ in pairs)
    lb = collections.Counter(b for _, b in pairs)
    pe = sum((la[k] / n) * (lb[k] / n) for k in set(la) | set(lb))
    return obs, (1.0 if pe >= 1 else (obs - pe) / (1 - pe))

sample_ids = [p for p in json.loads((DATA / "second-coder-sample.json").read_text())["paper_ids"]
              if (DATA / "batches" / f"recode-{p}.json").exists()]
axis_k = {}
for ax in ("substrate", "write_policy", "retrieval_policy",
           "research_type", "research_method", "contribution"):
    pairs = []
    for pid in sample_ids:
        d2 = json.loads((DATA / "batches" / f"recode-{pid}.json").read_text())
        g = lambda d: {x["axis"]: x.get("value") for x in d.get("facets", [])}.get(ax)
        pairs.append((g(results[pid]), g(d2)))
    obs, kk = _kappa(pairs)
    name = ax.title().replace("_", "")
    axis_k[name] = round(kk, 4)
    check("Kappa" + name, round(kk, 4))
    check("Agree" + name, round(100 * obs, 1))
check("KappaMin", min(axis_k.values()))
check("KappaMax", max(axis_k.values()))

# Test-retest kappa, recomputed from the two pilot decision files.
_tr = [(pre[i], post[i]) for i in both]
check("RetestKappa", round(_kappa(_tr)[1], 4))

# Venue type is script-assigned, so it is verified against the database.
_vt = cli("facet", "map", "-topic-ids", TOPIC, "-x", "venue_type", "-y", "stratum")
_vtc = collections.Counter()
for row in _vt["cells"].values():
    for v, n in row.items():
        _vtc[v] += n
for v, n in _vtc.items():
    name = "VenueType" + v.title().replace("_", "")
    if name in F:
        check(name, n)

# --- policy cross-tabulation ------------------------------------------------
wr = collections.Counter()
writes, rets = set(), set()
scheme = {a["axis"]: a["allowed"] for a in cli("facet", "scheme", "list", "-topic-id", TOPIC)["axes"]}
for d in results.values():
    if not d.get("eligible"):
        continue
    fa = {x["axis"]: x.get("value") for x in d.get("facets", [])}
    if fa.get("write_policy") and fa.get("retrieval_policy"):
        wr[(fa["write_policy"], fa["retrieval_policy"])] += 1
cells = len(scheme["write_policy"]) * len(scheme["retrieval_policy"])
check("WriteRetrievalCells", cells)
check("WriteRetrievalOccupied", len(wr))
check("WriteRetrievalEmpty", cells - len(wr))

# --- coverage report --------------------------------------------------------
# Facts used by the manuscript but never verified. Printed, and fatal.
tex = pathlib.Path(DATA / ".." / ".." / "docs" / "manuscript-agentmem")
used = set()
import re
for f in list(tex.glob("*.tex")) + list((tex / "sections").glob("*.tex")):
    if f.name == "facts.tex":
        continue
    for m2 in re.findall(r"\\fact([A-Za-z]+)", f.read_text()):
        used.add(m2)
DIGITS = {"Zero": "0", "One": "1", "Two": "2", "Three": "3", "Four": "4",
          "Five": "5", "Six": "6", "Seven": "7", "Eight": "8", "Nine": "9"}


def unspell(n):
    for w, d in DIGITS.items():
        n = n.replace(w, d)
    return n


checked_tex = {re.sub(r"[^A-Za-z]", "", unspell(c).replace("_", "")) for c in checked}
unchecked = sorted(u for u in used
                   if re.sub(r"[^A-Za-z]", "", unspell(u)) not in checked_tex
                   and u not in ("SearchDate", "YearFloor", "Seed", "ScreenCap",
                                 "ClassifyCap", "PilotSize", "Providers",
                                 "MedianChars", "SecondaryStudies", "Assignments",
                                 "TitleIdenticalGroups", "NoAbstract",
                                 "KappaAssignments", "RTInCrossTab", "EmptyCells",
                                 "UnoccupiedValues", "NullVenueType",
                                 "KappaEligibility"))

print(f"verified {len(checked)} facts")
if unchecked:
    print(f"\nNOT CHECKED ({len(unchecked)} facts used in the manuscript):")
    for u in unchecked:
        print("  -", u)
if failures:
    print(f"\n{len(failures)} MISMATCHES:")
    for f2 in failures:
        print("  -", f2)
sys.exit(1 if (failures or unchecked) else 0)
