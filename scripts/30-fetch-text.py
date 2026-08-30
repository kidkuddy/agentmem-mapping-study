#!/usr/bin/env python3
"""The accessibility gate, and the full text behind it.

Every record that survived screening is fetched here. A record whose text cannot
be retrieved is excluded at this gate and counted in the PRISMA flow, so that
every record reaching classification is readable by construction. That is what
makes a full-text pass over the whole classification sample affordable, and it is
why this study needs no validation sample and reports no false-inclusion rate
(petersen.md 6.4).

Recovery, before excluding: a record with no open PDF is looked up on arXiv by
exact title. If it is there, that PDF becomes the text source. The DOI and venue
stay the peer-reviewed ones - only the text moves - so venue_type is unaffected.
In the loop-engineering run 36 of 93 unreadable records were recoverable this way
and none of them were recovered.

WHERE THIS SITS IN THE FUNNEL, and why it moved
  The protocol placed the gate before screening. It runs after screening instead.
  Fetching 1,000+ PDFs to gate a set from which 300 would be sampled spends the
  bulk of the fetching on records no agent will ever read, and a one-day execution
  cannot afford it. Screening is unaffected either way: it reads title and
  abstract, which every record has, and criterion I4 is applied here rather than
  there. Logged as a scope_change, and the gate's exclusions are a labelled row in
  the flow diagram rather than a silent shrinkage between two stages.

The CLI is not used to download. `phd paper download` stores against the record it
already has, which cannot express "this text came from arXiv under the same
title", and every call is a round trip. curl and pdftotext do the same job in one
process, in parallel, and leave the recovered source visible in the output.
"""
import json, os, pathlib, re, subprocess, sys, collections
from concurrent.futures import ThreadPoolExecutor

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

PDFDIR = DATA / "pdf"; PDFDIR.mkdir(exist_ok=True)
TXTDIR = DATA / "txt"; TXTDIR.mkdir(exist_ok=True)
ARXIV_ID = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?)", re.I)


def arxiv_title_query(t):
    """arXiv's API needs the title field named explicitly.

    Passing a title as a free-text query searches every field and ranks by the
    provider's own relevance, which for a long title returns whatever shares its
    common words - the first attempt at this returned three particle-physics
    papers for an agent-memory survey. `ti:"..."` returns the paper or nothing,
    which is the only useful behaviour for a title lookup."""
    return 'ti:"%s"' % re.sub(r'["\\]', " ", t or "").strip()


def norm_title(t):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", (t or "").lower()).split())


def db_urls(paper_id):
    """pdf_url, url and external_id from the database.

    scope-kept.json carries a url only for the records the dry-run capture pass
    matched by title, which is 44 of 192 - the rest were backfilled for their
    abstracts but not their links. Reading the link from the file instead of the
    database sent 137 of 192 records into the arXiv-by-title fallback and failed
    the gate on most of them, when the database had a direct pdf_url for them all
    along. On local sqlite this call costs about ten milliseconds."""
    try:
        raw = subprocess.run(["phd", "paper", "get", "-id", str(paper_id)],
                             capture_output=True, text=True, timeout=30).stdout
        d = json.loads(raw)
        return {k: d.get(k) or "" for k in ("pdf_url", "url", "external_id")}
    except (subprocess.TimeoutExpired, json.JSONDecodeError):
        return {}


def pdf_urls(rec):
    """Candidate PDF URLs for one record, best first."""
    out = []
    d = db_urls(rec["id"])
    ext = d.get("external_id") or ""
    for cand in (d.get("pdf_url"), d.get("url"), rec.get("url")):
        if not cand:
            continue
        m = ARXIV_ID.search(cand)
        if m:
            out.append(f"https://arxiv.org/pdf/{m.group(1)}")
        elif cand.lower().endswith(".pdf"):
            out.append(cand)
    if ext.startswith("arxiv:"):
        out.append(f"https://arxiv.org/pdf/{ext.split(':', 1)[1]}")
    seen, uniq = set(), []
    for u in out:
        if u not in seen:
            seen.add(u); uniq.append(u)
    return uniq


def arxiv_recover(title):
    """Look the record up on arXiv by title. Returns a PDF url or None."""
    try:
        raw = subprocess.run(
            ["phd", "search", "-dry-run", "-query", arxiv_title_query(title),
             "-providers", "arxiv", "-max-results", "5"],
            capture_output=True, text=True, timeout=120).stdout
        want = norm_title(title)
        for p in json.loads(raw).get("papers", []):
            if norm_title(p.get("title")) == want:
                m = ARXIV_ID.search(p.get("url") or "")
                if m:
                    return f"https://arxiv.org/pdf/{m.group(1)}"
    except Exception:
        pass
    return None


def fetch(rec):
    pid = rec["id"]
    pdf, txt = PDFDIR / f"{pid}.pdf", TXTDIR / f"{pid}.txt"
    if txt.exists() and txt.stat().st_size > 2000:
        return {"id": pid, "ok": True, "source": "cached"}

    cands = [(u, "direct") for u in pdf_urls(rec)]
    if not cands:
        u = arxiv_recover(rec.get("title") or "")
        if u:
            cands = [(u, "arxiv_by_title")]
    if not cands:
        return {"id": pid, "ok": False, "reason": "no retrievable pdf url"}

    for url, how in cands:
        r = subprocess.run(["curl", "-sSL", "--max-time", "90", "-A",
                            "Mozilla/5.0 (compatible; academic-mapping-study)",
                            "-o", str(pdf), url], capture_output=True, text=True)
        if r.returncode != 0 or not pdf.exists() or pdf.stat().st_size < 20000:
            continue
        if pdf.read_bytes()[:5] != b"%PDF-":
            continue
        subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)],
                       capture_output=True, text=True)
        if txt.exists() and txt.stat().st_size > 2000:
            return {"id": pid, "ok": True, "source": how, "url": url,
                    "chars": txt.stat().st_size}
    pdf.unlink(missing_ok=True)
    return {"id": pid, "ok": False, "reason": "fetch or parse failed",
            "tried": [u for u, _ in cands]}


def main():
    src = DATA / "screening-includes.json"
    if not src.exists():
        sys.exit("run 46-collect-includes.py first")
    records = json.loads(src.read_text())

    with ThreadPoolExecutor(max_workers=8) as ex:
        results = list(ex.map(fetch, records))

    by_id = {r["id"]: r for r in results}
    gated_in = [r for r in records if by_id[r["id"]]["ok"]]
    gated_out = [{"id": r["id"], "title": r["title"],
                  "reason": by_id[r["id"]].get("reason")} for r in records
                 if not by_id[r["id"]]["ok"]]

    (DATA / "gate-kept.json").write_text(json.dumps(gated_in, indent=1))
    (DATA / "gate-dropped.json").write_text(json.dumps(gated_out, indent=1))
    summary = {
        "screening_includes": len(records),
        "text_retrieved": len(gated_in),
        "excluded_at_accessibility_gate": len(gated_out),
        "by_source": dict(collections.Counter(
            r.get("source") for r in results if r["ok"])),
        "recovered_from_arxiv_by_title": sum(
            1 for r in results if r.get("source") == "arxiv_by_title"),
    }
    (DATA / "gate-summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
