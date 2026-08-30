#!/usr/bin/env python3
"""Builds self-contained screening batches.

Each batch file holds the inlined coding guide and every record's title, year,
venue and abstract. A screening agent therefore makes two tool calls: read this
file, write its decisions. It never searches, never fetches a page, never
touches the database.

That is the whole cost model. An agent's token cost is the sum of its context
across every turn, so an agent that makes ten calls while building to 85k of
context costs closer to half a million tokens than to 85k. Batching at 120 also
amortises the ~4k-token guide over 120 records instead of 45 (petersen.md 6.0,
6.5).

Batch 00 is the pilot: 50 records, drawn with a committed seed, screened first
so an under-specified criterion is found at 50 records rather than at 300.
"""
import json, os, pathlib, random, sys

HERE = pathlib.Path(__file__).parent
# In the replication package the study data sits in ../data while the
# scripts stay in ../scripts. DATA is the only path that differs from
# the layout these scripts were executed in.
DATA = (HERE / ".." / "data").resolve()

# Same local-sqlite switch the shell scripts use: every `phd` call below would
# otherwise be a network round trip to Turso.
# Point the phd CLI at the database shipped beside these scripts. The original
# study read this from a local.env; that file used shell command substitution to
# find itself, which os.path.expandvars does not evaluate, so the path is
# resolved here directly instead.
os.environ["PHD_ENV"] = str((HERE / ".." / ".no-remote.env").resolve())
os.environ["EPT_DATA"] = str(DATA)
GUIDE = (DATA / ".." / ".." / "docs" / "agentmem-screening-guide.md").resolve()
SEED = 20260830          # committed here before the draw
PILOT = 50
BATCH = 120
SCREEN_CAP = 300         # declared in the protocol before the draw. A one-day
                         # execution cannot screen an uncapped survivor set and
                         # still read 80 papers in full; the shortfall against the
                         # 120-200 primary studies an eight-page map wants is
                         # reported as a limitation, not concealed.


def main():
    src = DATA / "scope-kept.json"
    if not src.exists():
        sys.exit("run 20-scope-filter.py first")
    screenable = json.loads(src.read_text())

    # Seeded random draw, applied to papers *entering* the stage rather than to
    # what the providers returned. A declared sample is an ordinary design; a
    # top-k slice of a relevance ranking is not (petersen.md 6.2). Below the cap
    # nothing is sampled and the whole surviving set is screened.
    rng = random.Random(SEED)
    order = sorted(screenable, key=lambda r: r["id"])
    rng.shuffle(order)
    sampled_out = []
    if SCREEN_CAP and len(order) > SCREEN_CAP:
        sampled_out = order[SCREEN_CAP:]
        order = order[:SCREEN_CAP]

    guide = GUIDE.read_text()
    outdir = DATA / "batches"
    outdir.mkdir(exist_ok=True)
    for f in outdir.glob("screen-*.json"):
        f.unlink()

    def fields(r):
        return {"paper_id": r["id"], "title": r["title"], "year": r.get("year"),
                "venue": r.get("venue"), "authors": r.get("authors"),
                "abstract": r.get("abstract") or ""}

    rest = order[PILOT:]
    chunks = [("00", order[:PILOT])] + [
        (f"{i // BATCH + 1:02d}", rest[i:i + BATCH]) for i in range(0, len(rest), BATCH)
    ]
    chunks = [(n, c) for n, c in chunks if c]

    manifest = []
    for name, chunk in chunks:
        path = outdir / f"screen-{name}.json"
        path.write_text(json.dumps({
            "batch": name,
            "is_pilot": name == "00",
            "seed": SEED,
            "output_path": str(outdir / f"decisions-{name}.json"),
            "guide": guide,
            "records": [fields(r) for r in chunk],
        }, indent=1))
        manifest.append({"batch": name, "n": len(chunk), "path": str(path)})

    summary = {
        "seed": SEED,
        "screenable": len(screenable),
        "screen_cap": SCREEN_CAP,
        "sampled_into_screening": len(order),
        "not_drawn_by_sampling": len(sampled_out),
        "pilot_size": PILOT,
        "batch_size": BATCH,
        "batches": manifest,
        "not_drawn_ids": [r["id"] for r in sampled_out],
    }
    (DATA / "batch-summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "not_drawn_ids"}, indent=1))


if __name__ == "__main__":
    main()
