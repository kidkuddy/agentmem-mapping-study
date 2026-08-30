#!/usr/bin/env python3
"""Builds one self-contained classification file per paper, from full text.

One agent per paper, two tool calls: read this file, write its result. It never
fetches a page, never downloads a PDF, never touches the database. That is the
whole cost model - an agent's token cost is the sum of its context across every
turn, so ten small calls cost far more than the endpoint context suggests
(petersen.md 6.0).

WHICH PAGES, and why not all of them
  Front matter carries the contribution claim; the tail carries the evidence type.
  Between them they decide every axis except venue_type, which comes from
  metadata. The middle is method detail that rarely moves a facet - except when
  the mechanism itself is described there, which is exactly what this study codes.

  So the middle is not dropped, it is ranked: the three middle pages densest in
  memory-mechanism vocabulary are included. Selecting by ranking rather than by a
  fixed page range is what keeps `substrate`, `write_policy` and
  `retrieval_policy` decidable without shipping a 30-page paper into an agent's
  context.

  What the agent did not see is stated in its input file, so an axis it could not
  decide is a reported null rather than a guess (petersen.md 6.3).

The sample is drawn here with a seed committed before the draw (6.12 step 6).
"""
import json, os, pathlib, random, re, sys

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

GUIDE = (DATA / ".." / ".." / "docs" / "agentmem-classification-guide.md").resolve()
TXTDIR = DATA / "txt"
SEED = 20260830          # committed before the draw
CLASSIFY_CAP = 80        # declared in the protocol before the draw
FRONT = 2                # leading pages always included
TAIL = 3                 # trailing pages always included
MIDDLE = 3               # highest-scoring middle pages
MAX_CHARS = 46000        # per paper, after selection

# Vocabulary that indicates a page describes the memory mechanism rather than
# related work or experimental setup. Used only to rank middle pages.
CUE = re.compile(r"""
      memory\s+(module|component|store|bank|stream|graph|pool|layer|entry|item|record)
    | (write|store|append|insert|update|delete|evict|forget|consolidat|summari|reflect)\w*
      \s+(to|into|from|the)?\s*(the\s+)?memory
    | retriev\w+ | embedding | cosine | top-?k | similarity
    | \bschema\b | \bSQL\b | knowledge\s+graph | vector\s+(store|database|index)
    | file\s+system | scratchpad | \bJSON\b
    | our\s+(memory|architecture|design|mechanism|framework)
""", re.I | re.X)


def pages(pid):
    f = TXTDIR / f"{pid}.txt"
    if not f.exists():
        return []
    raw = f.read_text(errors="replace")
    return [p for p in raw.split("\f")]


def select(pid):
    """Return (selected_pages, note) where selected_pages is [(page_no, text)]."""
    ps = pages(pid)
    n = len(ps)
    if n == 0:
        return [], "no extracted text"
    front = list(range(0, min(FRONT, n)))
    tail = list(range(max(0, n - TAIL), n))
    chosen = set(front) | set(tail)
    middle = [i for i in range(n) if i not in chosen]
    ranked = sorted(middle, key=lambda i: -len(CUE.findall(ps[i])))
    extra = [i for i in ranked[:MIDDLE] if len(CUE.findall(ps[i])) > 0]
    chosen |= set(extra)
    sel = [(i + 1, ps[i]) for i in sorted(chosen)]

    total = sum(len(t) for _, t in sel)
    if total > MAX_CHARS:
        # Trim the longest pages first rather than dropping any page: a dropped
        # page is invisible to the coder, a trimmed one announces itself.
        budget = MAX_CHARS // len(sel)
        sel = [(p, t if len(t) <= budget else t[:budget] + "\n[... page truncated ...]")
               for p, t in sel]
    note = (f"pages {', '.join(str(p) for p, _ in sel)} of {n}; "
            f"front matter, tail, and the {len(extra)} middle page(s) densest in "
            f"memory-mechanism vocabulary. Other pages were not extracted.")
    return sel, note


def main():
    src = DATA / "gate-kept.json"
    if not src.exists():
        sys.exit("run 30-fetch-text.py first")
    gated = json.loads(src.read_text())

    rng = random.Random(SEED)
    order = sorted(gated, key=lambda r: r["id"])
    rng.shuffle(order)
    corpus = order[:CLASSIFY_CAP] if CLASSIFY_CAP else order
    not_drawn = order[CLASSIFY_CAP:] if CLASSIFY_CAP else []

    guide = GUIDE.read_text()
    outdir = DATA / "batches"
    outdir.mkdir(exist_ok=True)
    for f in outdir.glob("classify-*.json"):
        f.unlink()

    manifest, empty = [], []
    for r in corpus:
        pid = r["id"]
        sel, note = select(pid)
        if not sel:
            empty.append(pid)
            continue
        path = outdir / f"classify-{pid}.json"
        path.write_text(json.dumps({
            "paper_id": pid,
            "seed": SEED,
            "output_path": str(outdir / f"facets-{pid}.json"),
            "guide": guide,
            "record": {
                "paper_id": pid, "title": r.get("title"), "year": r.get("year"),
                "venue": r.get("venue"), "authors": r.get("authors"),
                "stratum": r.get("stratum") or "peer_reviewed",
                "abstract": r.get("abstract") or "",
            },
            "extraction_note": note,
            "pages": [{"page": p, "text": t} for p, t in sel],
        }, indent=1))
        manifest.append({"paper_id": pid, "path": str(path),
                         "chars": sum(len(t) for _, t in sel)})

    summary = {
        "seed": SEED,
        "gate_kept": len(gated),
        "classify_cap": CLASSIFY_CAP,
        "drawn": len(corpus),
        "batches_written": len(manifest),
        "drawn_but_no_text": empty,
        "not_drawn_by_sampling": len(not_drawn),
        "median_chars": sorted(m["chars"] for m in manifest)[len(manifest) // 2] if manifest else 0,
        "not_drawn_ids": [r["id"] for r in not_drawn],
    }
    (DATA / "classification-summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps({k: v for k, v in summary.items() if k != "not_drawn_ids"}, indent=1))


if __name__ == "__main__":
    main()
