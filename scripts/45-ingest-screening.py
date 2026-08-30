#!/usr/bin/env python3
"""Writes screening decisions from the agents' JSON into the database.

Agents write files; this writes rows. Keeping the database out of the agents'
reach is the whole cost model — every `phd screen` call an agent made would be a
turn, and a turn re-sends its entire accumulated context. 520 records means 520
of those. Here they are 520 local subprocess calls at ~10ms.

It also does what an agent cannot be trusted to do: check that every record in
the batch got exactly one decision, that no id was invented, and that criteria
cited actually exist.
"""
import json, os, pathlib, subprocess, sys, collections

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


def criteria_map():
    raw = subprocess.run(["phd", "criterion", "list", "-topic-id", TOPIC],
                         capture_output=True, text=True, check=True).stdout
    out = {}
    for c in json.loads(raw).get("criteria", []):
        if c.get("status") != "accepted":
            continue
        # The code is the first whitespace-delimited token, with a trailing
        # colon tolerated. Splitting on ":" alone keyed the whole criterion
        # text for criteria written "E6 The system is not..." and every cited
        # code then looked unknown.
        out[c["text"].split()[0].strip(":.")] = c["id"]   # "I1", "E3", ...
    return out


def _db_screened(topic):
    """paper_id -> current screening decision already in the database.

    The database refuses to record a second decision for a paper without an
    explicit supersede, which is the right default: it means an ingest cannot
    quietly overwrite a decision. So this ingest is idempotent by construction —
    it writes what is absent, supersedes only what actually changed, and leaves
    an unchanged decision alone rather than manufacturing a reversal record for
    it."""
    out = {}
    for stage, decision in (("screening_included", "include"),
                            ("screening_excluded", "exclude")):
        raw = subprocess.run(["phd", "paper", "list-by-stage", "-stage", stage,
                              "-topic-id", topic, "-limit", "10000"],
                             capture_output=True, text=True).stdout
        try:
            for pap in json.loads(raw).get("papers", []):
                out[pap["id"]] = decision
        except json.JSONDecodeError:
            pass
    return out


def main():
    cmap = criteria_map()
    batches = sorted(f for f in (DATA / "batches").glob("decisions-*.json"))
    if not batches:
        sys.exit("no decisions-*.json in batches/ — run the screening agents first")

    # The corpus moved under the decisions: duplicate collapsing and the
    # borrowed-abstract repair both ran after screening. A decision about a
    # record that is no longer in the corpus is not written, and a record in the
    # corpus with no decision is reported rather than silently absent.
    corpus = {r["id"] for r in json.loads((DATA / "scope-kept.json").read_text())}

    # Re-review supersedes the original decision for the records it covers. It
    # was made against the corrected guide, so where the two disagree it wins.
    overrides = {}
    rr = DATA / "batches" / "rereview-decisions.json"
    if rr.exists():
        overrides = {d["paper_id"]: d for d in json.loads(rr.read_text())["decisions"]}

    already = _db_screened(TOPIC)
    tally = collections.Counter()
    reasons = collections.Counter()
    problems = []
    seen = set()
    superseded = 0
    dropped_not_in_corpus = 0
    unchanged = 0
    reversed_ = 0

    for f in batches:
        name = f.stem.replace("decisions-", "")
        if name == "rereview":
            continue                       # applied as overrides, not as a batch
        screen_file = DATA / "batches" / f"screen-{name}.json"
        if name == "inherited":
            # Same paper as an already-screened record, surfacing under another id
            # because adding records changed which member of a duplicate group is
            # retained. The decision is inherited, not re-judged, and it lives in
            # its own file so the audit trail says which.
            expected = {d["paper_id"] for d in json.loads(f.read_text())["decisions"]}
        elif screen_file.exists():
            expected = {r["paper_id"] for r in json.loads(screen_file.read_text())["records"]}
        else:
            continue
        decisions = json.loads(f.read_text())["decisions"]
        got = {d["paper_id"] for d in decisions}

        if got - expected:
            problems.append(f"{f.name}: ids not in the batch: {sorted(got - expected)}")
        if expected - got:
            problems.append(f"{f.name}: {len(expected - got)} records undecided: {sorted(expected - got)[:10]}")

        for d in decisions:
            pid = d["paper_id"]
            if pid in seen or pid not in expected:
                continue
            if pid not in corpus:
                dropped_not_in_corpus += 1
                continue
            if pid in overrides:
                if overrides[pid]["decision"] != d["decision"]:
                    superseded += 1
                d = overrides[pid]
            seen.add(pid)
            crits = [cmap[c] for c in d.get("criteria", []) if c in cmap]
            unknown = [c for c in d.get("criteria", []) if c not in cmap]
            if unknown:
                problems.append(f"{f.name}: paper {pid} cites unknown criteria {unknown}")
            reason = (d.get("reason") or "").strip()
            if len(reason) < 20:
                problems.append(f"{f.name}: paper {pid} reason too thin: {reason!r}")
                continue
            existing = already.get(pid)
            if existing == d["decision"]:
                tally[d["decision"]] += 1
                unchanged += 1
                if d["decision"] == "exclude":
                    for c in d.get("criteria", []):
                        reasons[c] += 1
                continue
            cmd = ["phd", "screen", "-topic-id", TOPIC, "-paper-id", str(pid),
                   "-decision", d["decision"], "-reason", reason,
                   "-decided-by", "agent:screener"]
            if existing is not None:
                cmd.append("-supersede")
            if crits:
                cmd += ["-criteria-ids", ",".join(str(c) for c in crits)]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode != 0:
                problems.append(f"{f.name}: paper {pid} write failed: {r.stderr.strip()[:120]}")
                continue
            if existing is not None:
                reversed_ += 1
            tally[d["decision"]] += 1
            if d["decision"] == "exclude":
                for c in d.get("criteria", []):
                    reasons[c] += 1

    # The earlier ingest wrote decisions against a larger corpus. Records since
    # removed as duplicates still carry a screening row, and an obsolete include
    # would inflate the corpus. They are superseded rather than deleted, so the
    # reversal is on the record.
    stale = 0
    for pid in sorted(set(already) - corpus):
        r = subprocess.run(["phd", "screen", "-topic-id", TOPIC, "-paper-id", str(pid),
                            "-decision", "exclude", "-supersede", "-decided-by", "agent:screener",
                            "-reason", "Superseded: this record was collapsed into a "
                                       "title-identical duplicate and is no longer in the corpus."],
                           capture_output=True, text=True)
        if r.returncode == 0:
            stale += 1
    summary_stale = stale

    undecided = sorted(corpus - seen)
    if undecided:
        problems.append(f"{len(undecided)} corpus records have no decision: {undecided[:10]}")

    inc = tally["include"]
    total = sum(tally.values())
    summary = {
        "written": total,
        "already_correct_left_alone": unchanged,
        "decisions_reversed_in_db": reversed_,
        "superseded_by_rereview": superseded,
        "decisions_dropped_record_no_longer_in_corpus": dropped_not_in_corpus,
        "corpus_records_without_a_decision": len(undecided),
        "stale_decisions_superseded": summary_stale,
        "include": inc,
        "exclude": tally["exclude"],
        "include_rate": round(100.0 * inc / max(1, total), 1),
        "exclusions_by_criterion": dict(reasons.most_common()),
        "problems": problems,
    }
    (DATA / "screening-summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "problems"}, indent=1))
    if problems:
        print(f"\n{len(problems)} PROBLEMS:")
        for p in problems[:20]:
            print("  -", p)


if __name__ == "__main__":
    main()
