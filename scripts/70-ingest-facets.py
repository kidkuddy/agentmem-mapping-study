#!/usr/bin/env python3
"""Writes facet assignments from the classifier JSON into the database.

Agents write files; this writes rows, for the same reason screening does — every
`phd facet assign` an agent made would be a turn, and a turn re-sends its whole
accumulated context.

It also enforces what an agent cannot enforce on itself:
  - every included paper has exactly one result, and no invented paper ids
  - every value is on the axis whitelist (the CLI refuses others anyway, but a
    refusal here names the batch it came from)
  - every justification is specific rather than boilerplate
  - nulls are counted per axis and reported, because the per-axis null count is
    a result of this study, not a processing detail

`venue_type` is assigned here from record metadata, never by an agent: it is
deterministic and an agent turn spent on it would be wasted.
"""
import json, os, pathlib, re, subprocess, sys, collections

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

PREPRINT = re.compile(r"arxiv|preprint|ssrn|biorxiv|osf|researchsquare|techrxiv", re.I)
JOURNAL = re.compile(r"journal|transactions|letters|review of|nature|science|plos|"
                     r"frontiers|ieee access|acm computing surveys|quarterly", re.I)
WORKSHOP = re.compile(r"workshop|\bws\b|colocated|co-located", re.I)


def db_meta(paper_id):
    """venue and source from the database.

    scope-kept.json carries a venue only for records the dry-run capture pass
    matched, which is 5 of 331 — the rest were backfilled for their abstracts
    but not their venue, so deriving venue_type from that file produced 186
    nulls on an axis that is supposed to be free. The database has it."""
    try:
        raw = subprocess.run(["phd", "paper", "get", "-id", str(paper_id)],
                             capture_output=True, text=True, timeout=30).stdout
        d = json.loads(raw)
        return {"venue": d.get("venue"), "source": d.get("source")}
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return {}


def venue_type(rec):
    """Script-derived, from the venue string and the source. Preprint is decided
    first: this literature lives on arXiv and coding that makes it visible rather
    than hiding it behind an exclusion."""
    v = rec.get("venue") or ""
    if rec.get("source") == "arxiv" or PREPRINT.search(v):
        return "preprint"
    if WORKSHOP.search(v):
        return "workshop"
    if JOURNAL.search(v):
        return "journal"
    if v.strip():
        return "conference"
    return None


def allowed_values():
    raw = subprocess.run(["phd", "facet", "scheme", "list", "-topic-id", TOPIC],
                         capture_output=True, text=True, check=True).stdout
    return {a["axis"]: set(a["allowed"]) for a in json.loads(raw)["axes"]}


def main():
    scope = {r["id"]: r for r in json.loads((DATA / "screening-includes.json").read_text())}
    allow = allowed_values()

    # The re-code pass supersedes the original result for the records it covers.
    # It was made against the amended scheme — contribution gained
    # empirical_finding, and empty-abstract handling was reduced to one rule —
    # so where the two disagree it wins.
    overrides = {}
    for f in sorted((DATA / "batches").glob("recode-decisions-*.json")):
        for r in json.loads(f.read_text()).get("results", []):
            overrides[r["paper_id"]] = r

    results, problems = {}, []
    for f in sorted((DATA / "batches").glob("facets-*.json")):
        # Classification here is one agent per paper reading full text, so a
        # result file holds a single object. Batched files with a "results" array
        # are still accepted, because the second-coder pass writes them.
        doc = json.loads(f.read_text())
        for r in (doc.get("results") or ([doc] if "paper_id" in doc else [])):
            pid = r["paper_id"]
            if pid not in scope:
                problems.append(f"{f.name}: paper {pid} is not in the included set")
                continue
            if pid in results:
                problems.append(f"{f.name}: paper {pid} classified twice")
                continue
            results[pid] = (overrides.get(pid, r), f.name)

    for pid in sorted(set(scope) - set(results)):
        problems.append(f"included paper {pid} has no classification result")

    superseded = sum(1 for pid in results if pid in overrides)
    # Axes an eligible paper carries no entry for at all. This is not the same as
    # a null: a null is counted and reported, a missing entry silently shrinks the
    # denominator of whichever axis it belongs to. Six papers - the empty-abstract
    # records - had coders omit the entries rather than write explicit nulls. They
    # are counted as nulls here, which is what they mean.
    AXES = {"substrate", "write_policy", "retrieval_policy",
            "research_type", "research_method", "contribution"}
    nulls = collections.Counter()
    missing_entries = collections.Counter()
    values = collections.defaultdict(collections.Counter)
    written = ineligible = 0

    for pid, (r, src) in sorted(results.items()):
        if not r.get("eligible"):
            ineligible += 1
            continue
        for fa in r.get("facets", []):
            axis, val = fa["axis"], fa.get("value")
            if axis == "venue_type":
                continue                      # script-derived below
            if axis not in allow:
                problems.append(f"{src}: paper {pid} names unknown axis {axis!r}")
                continue
            if val is None:
                nulls[axis] += 1
                continue
            if val not in allow[axis]:
                problems.append(f"{src}: paper {pid} value {val!r} not on axis {axis}")
                continue
            just = (fa.get("justification") or "").strip()
            if len(just) < 25:
                problems.append(f"{src}: paper {pid} {axis}={val} justification too thin")
                continue
            values[axis][val] += 1
            proc = subprocess.run(
                ["phd", "facet", "assign", "-topic-id", TOPIC, "-paper-id", str(pid),
                 "-axis", axis, "-value", val, "-justification", just,
                 "-assigned-by", "agent:classifier"],
                capture_output=True, text=True)
            if proc.returncode != 0:
                problems.append(f"{src}: paper {pid} {axis}={val} write failed: {proc.stderr.strip()[:100]}")
            else:
                written += 1

        for axis in AXES - {fa["axis"] for fa in r.get("facets", [])}:
            nulls[axis] += 1
            missing_entries[axis] += 1

        # Secondary stores are recorded, not mapped. A record whose contribution
        # combines several stores is coded on its primary one; the rest are kept
        # so the map's "one mechanism per record" rule is auditable rather than
        # lossy.
        for sec in (r.get("secondary_substrates") or []):
            if sec in allow.get("substrate", ()):
                subprocess.run(
                    ["phd", "extract", "add", "-topic-id", TOPIC, "-paper-id", str(pid),
                     "-category", "secondary_substrate", "-content", sec,
                     "-page", "0", "-quote", f"secondary store reported alongside the primary mechanism: {sec}"],
                    capture_output=True, text=True)

        st = scope[pid].get("stratum") or "peer_reviewed"
        values["stratum"][st] += 1
        subprocess.run(
            ["phd", "facet", "assign", "-topic-id", TOPIC, "-paper-id", str(pid),
             "-axis", "stratum", "-value", st,
             "-justification", f"Derived by script: the record entered the corpus through the "
                               f"{'declared practitioner enumeration' if st == 'grey' else 'database search'}.",
             "-assigned-by", "script"],
            capture_output=True, text=True)

        vt = "grey" if st == "grey" else venue_type(db_meta(pid) or scope[pid])
        if vt:
            values["venue_type"][vt] += 1
            subprocess.run(
                ["phd", "facet", "assign", "-topic-id", TOPIC, "-paper-id", str(pid),
                 "-axis", "venue_type", "-value", vt,
                 "-justification", f"Derived by script from the record's venue and source "
                                   f"in the database (paper {pid}).",
                 "-assigned-by", "script"],
                capture_output=True, text=True)
        else:
            nulls["venue_type"] += 1

    summary = {
        "included": len(scope), "with_a_result": len(results),
        "ineligible_at_classification": ineligible,
        "superseded_by_recode": superseded,
        "assignments_written": written,
        "nulls_by_axis": dict(nulls.most_common()),
        "of_which_no_entry_written": dict(missing_entries.most_common()),
        "value_counts": {a: dict(c.most_common()) for a, c in values.items()},
        "problems": problems,
    }
    (DATA / "facet-summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "problems"}, indent=1))
    if problems:
        print(f"\n{len(problems)} PROBLEMS:")
        for p in problems[:20]:
            print("  -", p)


if __name__ == "__main__":
    main()
