#!/usr/bin/env python3
"""Records the classification-stage eligibility decisions in the database.

Classification decided eligibility for every screened-in paper - the full-text
criteria I1-I4 and E1-E7, applied with the pages in hand - but those decisions
lived only in the classifier JSON. Without this step the PRISMA flow reports
'reports assessed: 0', which is not what happened.

PRISMA 2020 item 16a asks for the number of reports ASSESSED for eligibility, not
just the number excluded, precisely so a flow cannot show papers arriving at the
included set without passing through the gate that admitted them.
"""
import json, os, pathlib, subprocess, collections

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

corpus = {r["id"] for r in json.loads((DATA / "screening-includes.json").read_text())}
over = {}
for f in (DATA / "batches").glob("recode-decisions-*.json"):
    for r in json.loads(f.read_text())["results"]:
        over[r["paper_id"]] = r
results = {}
for f in sorted((DATA / "batches").glob("facets-*.json")):
    doc = json.loads(f.read_text())
    for r in (doc.get("results") or ([doc] if "paper_id" in doc else [])):
        results[r["paper_id"]] = over.get(r["paper_id"], r)

tally, already, failed = collections.Counter(), 0, []
for pid, r in sorted(results.items()):
    if pid not in corpus:
        continue
    dec = "include" if r.get("eligible") else "exclude"
    reason = (r.get("eligibility_reason") or "").strip() or \
             ("Meets I1-I4 on the full text." if dec == "include" else "Excluded on the full text.")
    p = subprocess.run(["phd", "eligibility", "-topic-id", TOPIC, "-paper-id", str(pid),
                        "-decision", dec, "-reason", reason,
                        "-decided-by", "agent:classifier"],
                       capture_output=True, text=True)
    if p.returncode == 0:
        tally[dec] += 1
    elif "already recorded" in p.stderr:
        already += 1
    else:
        failed.append(f"{pid}: {p.stderr.strip()[:110]}")

# PRISMA item 16a wants the number of reports ASSESSED, which is the number
# that reached the full-text stage - not the size of the screening-include set
# it was drawn from. Labelling the corpus size "assessed" overstates the
# denominator by the whole sampled-out remainder.
# Counted from the coders' own files, not from how many rows this run wrote.
# The write is idempotent, so on a second run every row is "already recorded" and
# a tally of writes reports zero eligible papers for a corpus that has 66.
assessed = [r for pid, r in results.items() if pid in corpus]
out = {"assessed": len(assessed), "screening_includes": len(corpus),
       "eligible": sum(1 for r in assessed if r.get("eligible")),
       "excluded": sum(1 for r in assessed if not r.get("eligible")),
       "rows_written_this_run": dict(tally),
       "already_recorded": already, "failures": failed}
(DATA / "eligibility-summary.json").write_text(json.dumps(out, indent=1))
print(json.dumps({k: v for k, v in out.items() if k != "failures"}, indent=1))
if failed:
    print("FAILURES:", *failed[:5], sep="\n  ")
