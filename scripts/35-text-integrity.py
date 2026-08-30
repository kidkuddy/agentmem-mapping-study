#!/usr/bin/env python3
"""Checks that the text fetched for each record is that record's own paper.

A classifier reading paper 19017 reported that its extracted pages were the text
of a different paper entirely. That is not a coding error, it is a corpus error,
and the only responsible reaction to finding one is to measure how many there are.

THE CHECK
  Take the record's title from the database, take the first two extracted pages,
  and compute what share of the title's content words appear in that text. A
  paper's own front matter contains its own title, so a correct pairing scores
  near 1.0. A mismatched pairing scores low, because two unrelated papers share
  only stopwords and a few domain terms.

  The threshold is 0.5, and it is deliberately loose. pdftotext mangles ligatures
  and hyphenation, titles get line-broken mid-word, and some publishers put the
  title only in a graphic. A loose threshold means the flagged set contains a few
  correct pairings, which is the right direction to err: every flag is looked at,
  so a false flag costs a glance while a missed mismatch costs a fabricated row
  in the map.

WHAT HAPPENS TO A MISMATCH
  It is dropped from the corpus, not re-fetched. Its facets, if any were written,
  were assigned from another paper's text and cannot be repaired by re-reading.
  Dropping is reported as its own line in the flow diagram.
"""
import json, os, pathlib, re, subprocess, sys

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

STOP = set("the a an of and for or in on to with by from is are as at we our this that "
           "via using use toward towards through into over under can be it its their "
           "not no more less than when where which who what how do does".split())
THRESHOLD = 0.5


def words(s):
    return [w for w in re.findall(r"[a-z0-9]+", (s or "").lower())
            if w not in STOP and len(w) > 2]


def flatten(s):
    """Collapse whitespace and hyphenation so a line-broken title still matches."""
    return re.sub(r"[^a-z0-9]+", "", (s or "").lower())


def main():
    src = DATA / "gate-kept.json"
    records = json.loads(src.read_text())
    rows, flagged = [], []
    for r in records:
        pid = r["id"]
        f = DATA / "txt" / f"{pid}.txt"
        if not f.exists():
            continue
        head = f.read_text(errors="replace")[:6000]
        flat_head = flatten(head)
        title_words = words(r.get("title"))
        if not title_words:
            continue
        # Two ways to match, and either one is enough: the title appears
        # contiguously (robust to line breaks), or most of its content words are
        # present somewhere in the front matter (robust to subtitle drift).
        contiguous = flatten(r["title"])[:60] in flat_head
        hits = sum(1 for w in set(title_words) if w in flat_head)
        share = hits / len(set(title_words))
        ok = contiguous or share >= THRESHOLD
        row = {"id": pid, "title": r.get("title"), "share": round(share, 3),
               "contiguous": contiguous, "ok": ok}
        rows.append(row)
        if not ok:
            flagged.append(row)

    out = {
        "checked": len(rows),
        "passed": len(rows) - len(flagged),
        "flagged": len(flagged),
        "threshold": THRESHOLD,
        "flagged_records": sorted(flagged, key=lambda x: x["share"]),
    }
    (DATA / "text-integrity.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "flagged_records"}, indent=1))
    for row in out["flagged_records"][:30]:
        print(f"  {row['share']:.2f}  {row['id']}  {row['title'][:70]}")


if __name__ == "__main__":
    main()
