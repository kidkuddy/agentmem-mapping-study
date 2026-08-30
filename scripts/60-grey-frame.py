#!/usr/bin/env python3
"""Derives the grey stratum's sampling frame, mechanically.

The protocol's rule: the practitioner stratum is every distinct agent-memory
system named in TWO OR MORE of the secondary studies identified by this study's
own search, plus the memory components of named agent frameworks, with the frame
fixed on 2026-08-30.

Clause (a) is implemented here and nowhere else, as a script rather than a
judgement, because a frame chosen by a person is a frame that cannot be
reproduced. The candidate extraction is deliberately dumb - it takes tokens with
the shape of a system name (CamelCase, Name-with-digit, an internal capital, a
hyphenated Mem-prefix) out of the surveys' own text and counts how many distinct
surveys each appears in. Nothing about a token's meaning is consulted.

Judgement enters at exactly one point, and it is recorded: a candidate that is not
an agent-memory system - a benchmark, a base model, an institution, a metric - is
rejected by hand, with its reason, into grey-frame-rejected.json. That file is
part of the replication package, so the one subjective step in the frame is
auditable rather than invisible.

Threshold two, not one: a system named in a single survey is that survey's
example. A system three separate research groups independently chose to describe
is a system the field recognises, and that is what a purposive frame should hold.
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

SURVEYDIR = DATA / "surveys"; SURVEYDIR.mkdir(exist_ok=True)
ARXIV_ID = re.compile(r"arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]{4,5}(?:v[0-9]+)?)", re.I)

# Off-topic homonyms: "Long Short-Term Memory Networks: A Comprehensive Survey"
# is about LSTMs. The title filter that found the secondary studies cannot tell
# those apart from agent-memory surveys, so they are named and excluded here.
OFF_TOPIC = re.compile(r"long short-term memory|LSTM|polymeric|language learning", re.I)

NAMEY = re.compile(r"""
    \b(
        (?:[A-Z][a-z]+){2,}                  # CamelCase: MemoryBank, HippoRAG
      | [A-Z][a-zA-Z]*-?[A-Z]{2,}[a-zA-Z]*   # MemGPT, ExpeL, A-MEM
      | [A-Z][a-zA-Z]{2,}[0-9]               # Mem0, Zep2
      | Mem[A-Z][a-zA-Z]+                    # MemInsight, MemoRAG
    )\b
""", re.X)


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


def fetch(rec):
    pid = rec["id"]
    txt = SURVEYDIR / f"{pid}.txt"
    if txt.exists() and txt.stat().st_size > 2000:
        return pid
    url = rec.get("url") or ""
    m = ARXIV_ID.search(url)
    if not m:
        try:
            raw = subprocess.run(
                ["phd", "search", "-dry-run", "-query", arxiv_title_query(rec["title"]),
                 "-providers", "arxiv", "-max-results", "5"],
                capture_output=True, text=True, timeout=120).stdout
            want = norm_title(rec["title"])
            for p in json.loads(raw).get("papers", []):
                if norm_title(p.get("title")) == want:
                    m = ARXIV_ID.search(p.get("url") or "")
                    break
        except Exception:
            pass
    if not m:
        return None
    pdf = SURVEYDIR / f"{pid}.pdf"
    subprocess.run(["curl", "-sSL", "--max-time", "120", "-o", str(pdf),
                    f"https://arxiv.org/pdf/{m.group(1)}"], capture_output=True)
    if not pdf.exists() or pdf.read_bytes()[:5] != b"%PDF-":
        return None
    subprocess.run(["pdftotext", "-layout", str(pdf), str(txt)], capture_output=True)
    return pid if txt.exists() and txt.stat().st_size > 2000 else None


def main():
    src = DATA / "secondary-studies.json"
    if not src.exists():
        sys.exit("secondary-studies.json missing")
    surveys = [r for r in json.loads(src.read_text())
               if not OFF_TOPIC.search(r["title"] or "")]
    print(f"{len(surveys)} on-topic secondary studies "
          f"({len(json.loads(src.read_text())) - len(surveys)} dropped as homonyms)")

    with ThreadPoolExecutor(max_workers=6) as ex:
        got = [p for p in ex.map(fetch, surveys) if p]
    print(f"{len(got)} of {len(surveys)} retrieved as full text")

    doc_count = collections.Counter()
    where = collections.defaultdict(set)
    for pid in got:
        toks = set(NAMEY.findall((SURVEYDIR / f"{pid}.txt").read_text(errors="replace")))
        for t in toks:
            doc_count[t] += 1
            where[t].add(pid)

    candidates = [{"name": t, "surveys": n, "survey_ids": sorted(where[t])}
                  for t, n in doc_count.most_common() if n >= 2]
    out = {
        "frame_fixed": "2026-08-30",
        "rule": "named in two or more on-topic secondary studies identified by this study's search",
        "surveys_used": [{"id": r["id"], "title": r["title"], "year": r.get("year")}
                         for r in surveys if r["id"] in got],
        "surveys_unretrievable": [r["id"] for r in surveys if r["id"] not in got],
        "candidates": candidates,
    }
    (DATA / "grey-candidates.json").write_text(json.dumps(out, indent=1))
    print(f"{len(candidates)} candidate names appear in >= 2 surveys")
    print("top 60:", ", ".join(c["name"] for c in candidates[:60]))


if __name__ == "__main__":
    main()
