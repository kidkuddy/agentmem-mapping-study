#!/usr/bin/env python3
"""Generates every number the manuscript uses, as LaTeX macros and as JSON.

The manuscript writes \\factCorpus{}, never 66. A number typed into prose drifts
the moment the corpus changes, and it drifts silently. Emits facts.tex (macros)
and facts.json (the same values, for the verifier).

101-verify.py expresses its queries independently rather than importing from here:
two independent statements of the same definition catch a bug, one statement
checked against itself only proves it is self-consistent.
"""
import json, os, pathlib, re, subprocess, collections

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


def jload(p):
    return json.loads((DATA / p).read_text())


F = {}

# --- identification ---------------------------------------------------------
runs = sorted((DATA / "runs").glob("*.json"))
gross = bound = total_runs = 0
providers = set()
for f in runs:
    d = json.loads(f.read_text())
    for p in d["providers"]:
        total_runs += 1
        gross += p["found"]
        providers.add(p.get("provider") or "")
        if p["found"] >= 200:
            bound += 1
F["Queries"] = len({json.loads(f.read_text())["query"] for f in runs})
F["Providers"] = 2                      # arxiv, openalex; see 10-search.sh
F["Runs"] = total_runs
F["GrossHits"] = gross
F["CapBound"] = bound
F["CapBoundPct"] = round(100 * bound / total_runs)

scope = jload("scope-summary.json")
F["Identified"] = scope["records_identified"]
F["ScopeKept"] = scope["kept"]
F["ScopeDropped"] = scope["dropped_by_scope_filter"]
F["DuplicatesRemoved"] = scope["duplicates_removed"]
F["TitleIdenticalGroups"] = scope["title_identical_groups_in_corpus"]
F["NoAbstract"] = scope["records_with_no_abstract_text"]
# Counted from scope-kept.json, not from scope-summary's kept_by_branch: that
# tally is taken before title-identical duplicates are collapsed, so it reports
# 280 generic-branch records where 275 actually reach a screener.
_kept = jload("scope-kept.json")
for br in ("generic", "named", "both"):
    F["Branch" + br.title()] = sum(1 for r in _kept if r.get("scope_branch") == br)

# --- sampling and screening -------------------------------------------------
bs = jload("batch-summary.json")
F["Seed"] = bs["seed"]
F["ScreenCap"] = bs["screen_cap"]
F["Screened"] = bs["sampled_into_screening"]
F["NotDrawnScreening"] = bs["not_drawn_by_sampling"]
F["PilotSize"] = bs["pilot_size"]

scr = jload("screening-summary.json")
F["Included"] = scr["include"]
F["Excluded"] = scr["exclude"]
F["IncludeRate"] = scr["include_rate"]
for crit, n in scr["exclusions_by_criterion"].items():
    F["Excl" + crit] = n

# --- test-retest on the pilot ----------------------------------------------
tr = jload("test-retest.json")
F["RetestN"] = tr["n_scored"]
F["RetestAgreement"] = round(100 * tr["raw_agreement"], 1)
F["RetestKappa"] = tr["cohens_kappa"]
F["RetestDisagreements"] = len(tr["disagreements"])

# --- accessibility gate and text integrity ---------------------------------
g = jload("gate-summary.json")
F["GateIn"] = g["text_retrieved"]
F["GateOut"] = g["excluded_at_accessibility_gate"]
ti = jload("text-integrity.json")
F["IntegrityChecked"] = ti["checked"]
F["IntegrityFlagged"] = ti["flagged"]

# --- classification ---------------------------------------------------------
cs = jload("classification-summary.json")
F["ClassifyCap"] = cs["classify_cap"]
F["Drawn"] = cs["drawn"]
F["NotDrawnClassification"] = cs["not_drawn_by_sampling"]
F["MedianChars"] = cs["median_chars"]

fs = jload("facet-summary.json")
# The integrity-flagged record was quarantined before this ingest ran, so it is
# already absent from with_a_result. Subtracting it here as well removed a paper
# that was never counted, and every downstream corpus figure was one too low.
F["Classified"] = fs["with_a_result"]
F["Ineligible"] = fs["ineligible_at_classification"]
F["Corpus"] = F["Classified"] - F["Ineligible"]
F["Assignments"] = fs["assignments_written"]
for axis, n in fs["nulls_by_axis"].items():
    F["Null" + axis.title().replace("_", "")] = n
for axis, vals in fs["value_counts"].items():
    ax = axis.title().replace("_", "")
    for v, n in vals.items():
        F[ax + v.title().replace("_", "")] = n

# Axis values the corpus does not occupy at all. Declared in the scheme, coded by
# nobody: these are the empty columns, and they are findings rather than gaps.
allowed = {a["axis"]: a["allowed"] for a in json.loads(subprocess.run(
    ["phd", "facet", "scheme", "list", "-topic-id", TOPIC],
    capture_output=True, text=True, check=True).stdout)["axes"]}
unoccupied = {}
for axis, vals in allowed.items():
    if axis in ("stratum", "venue_type"):
        continue
    seen = set(fs["value_counts"].get(axis, {}))
    missing = [v for v in vals if v not in seen]
    if missing:
        unoccupied[axis] = missing
F["UnoccupiedValues"] = sum(len(v) for v in unoccupied.values())


# --- full-text exclusion reasons (PRISMA item 16b) --------------------------
# From the coders' own files. A flow that reports 13 exclusions without saying
# why they were excluded fails item 16b, and the reasons exist.
_ftx = collections.Counter()
for _f in sorted((DATA / "batches").glob("facets-*.json")):
    _d = json.loads(_f.read_text())
    if _d.get("eligible"):
        continue
    _cr = _d.get("eligibility_criteria") or []
    if not _cr:
        _r = (_d.get("eligibility_rule") or "").strip()
        _cr = [_r] if _r else []
    for _x in _cr:
        _ftx[_x] += 1
for _k, _n in _ftx.items():
    F["FullTextExcl" + _k] = _n

# --- reliability ------------------------------------------------------------
k = jload("facet-kappa.json")
F["KappaN"] = k["n_scored"]
F["KappaSharePct"] = round(100 * k["n_scored"] / F["Corpus"])
F["KappaEligibility"] = k["eligibility"]["cohens_kappa"]
kappas = []
for axis, v in k["by_axis"].items():
    ax = axis.title().replace("_", "")
    F["Kappa" + ax] = v["cohens_kappa"]
    F["Agree" + ax] = round(100 * v["raw_agreement"], 1)
    kappas.append(v["cohens_kappa"])
F["KappaMin"] = min(kappas)
F["KappaMax"] = max(kappas)
F["KappaDisagreements"] = len(k["disagreements"])
F["KappaAssignments"] = sum(v["n"] for v in k["by_axis"].values())

# --- the map ----------------------------------------------------------------
m = jload("map.json")
rt = m["maps"]["substrate_x_research_type"]["cells"]
# From the axis tally, not from the cross-tabulation. The cross-tab drops the
# records whose substrate is null, so summing its cells counts 61 research-type
# assignments where 66 were made, and a zero-cell bound computed on 61 is a
# bound on the wrong denominator.
F["RTAssignments"] = sum(fs["value_counts"]["research_type"].values())
F["RTInCrossTab"] = sum(sum(r.values()) for r in rt.values())
F["Evaluation"] = fs["value_counts"]["research_type"].get("evaluation", 0)
# One-sided 95% upper bound on a true rate given zero observations in n trials:
# 1 - 0.05^(1/n), the rule-of-three generalisation. Stated so a zero cell is
# reported as "consistent with a rate below x%", not as "does not exist".
F["EvaluationBound"] = round(100 * (1 - 0.05 ** (1 / F["RTAssignments"])), 1)
wr = m["maps"]["write_x_retrieval"]["cells"]
occupied = sum(1 for row in wr.values() for n in row.values() if n)
F["WriteRetrievalCells"] = sum(len(row) for row in wr.values())
F["WriteRetrievalOccupied"] = occupied
F["WriteRetrievalEmpty"] = F["WriteRetrievalCells"] - occupied
F["EmptyCells"] = len(m["empty_cells"])

# --- secondary studies, the motivation --------------------------------------
sec = jload("secondary-studies.json")
OFF = re.compile(r"long short-term memory|LSTM|polymeric|language learning", re.I)
F["SecondaryStudies"] = sum(1 for r in sec if not OFF.search(r["title"] or ""))

F["SearchDate"] = "30 August 2026"
F["YearFloor"] = 2023

# --- write out --------------------------------------------------------------
DIGITS = {"0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four",
          "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"}


def texname(k):
    """LaTeX macro names cannot contain digits, so digits are spelled out.

    Stripping them instead silently collapses ExclE1 through ExclE7 into one
    macro with the last definition winning."""
    out = "".join(DIGITS.get(c, c) for c in k)
    return "fact" + re.sub(r"[^A-Za-z]", "", out)


names = {}
for k2 in F:
    names.setdefault(texname(k2), []).append(k2)
clash = {n: ks for n, ks in names.items() if len(ks) > 1}
if clash:
    raise SystemExit(f"macro name collision, would silently overwrite: {clash}")

tex = ["% Generated by scripts/agentmem/100-facts.py — do not edit.",
       "% Every number in the manuscript comes from here. Typing one into prose",
       "% is how a paper and its data quietly diverge.", ""]
for k2 in sorted(F):
    tex.append(f"\\newcommand{{\\{texname(k2)}}}{{{F[k2]}}}")
(DATA / "facts.tex").write_text("\n".join(tex) + "\n")
F["_unoccupied_values"] = unoccupied
(DATA / "facts.json").write_text(json.dumps(F, indent=1, sort_keys=True))
print(f"{len(F)} facts -> facts.tex, facts.json")
for k2 in ("Identified", "ScopeKept", "Screened", "Included", "GateIn", "Corpus",
           "Evaluation", "EvaluationBound", "KappaMin", "WriteRetrievalEmpty"):
    print(f"  {k2:<22} {F[k2]}")
print("  unoccupied axis values:", json.dumps(unoccupied))
