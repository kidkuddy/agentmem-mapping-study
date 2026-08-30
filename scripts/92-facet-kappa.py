#!/usr/bin/env python3
"""Inter-coder agreement on facet assignment, per axis.

A 20% sample of the eligible corpus was coded a second time by an independent
agent working from the same guide and the same extracted pages, with no access to
the first coder's output. This compares the two.

PER AXIS, NOT POOLED. Screening reliability and coding reliability are different
claims, and so are the axes: `research_type` is a borrowed instrument on which
misassignment is a known problem (Mendes: 73% of papers self-designate wrongly),
while `substrate` is derived from this corpus and should be easier. A single
pooled kappa hides which axis a reader should distrust.

NULLS ARE A CATEGORY, NOT A GAP. If one coder writes null and the other writes a
value, they disagree, and that disagreement is exactly what a null is supposed to
surface. Dropping null pairs would compute agreement over the easy cases only.

Cohen's kappa is unstable on small samples with skewed marginals - an axis where
both coders answer the same value 12 times out of 13 can post a low kappa off one
disagreement. So raw agreement is reported beside it, and both travel with n.
"""
import json, pathlib, collections

HERE = pathlib.Path(__file__).parent
# In the replication package the study data sits in ../data while the
# scripts stay in ../scripts. DATA is the only path that differs from
# the layout these scripts were executed in.
DATA = (HERE / ".." / "data").resolve()
AXES = ["substrate", "write_policy", "retrieval_policy",
        "research_type", "research_method", "contribution"]


def facets(doc):
    out = {a: None for a in AXES}
    for f in doc.get("facets", []):
        if f["axis"] in out:
            out[f["axis"]] = f.get("value")
    return out


def kappa(pairs):
    n = len(pairs)
    if n == 0:
        return None, None
    obs = sum(1 for a, b in pairs if a == b) / n
    la = collections.Counter(a for a, _ in pairs)
    lb = collections.Counter(b for _, b in pairs)
    pe = sum((la[k] / n) * (lb[k] / n) for k in set(la) | set(lb))
    k = 1.0 if pe >= 1 else (obs - pe) / (1 - pe)
    return round(obs, 4), round(k, 4)


def main():
    sample = json.loads((DATA / "second-coder-sample.json").read_text())
    b = DATA / "batches"
    rows, disagreements = {a: [] for a in AXES}, []
    elig_pairs, missing = [], []

    for pid in sample["paper_ids"]:
        f1, f2 = b / f"facets-{pid}.json", b / f"recode-{pid}.json"
        if not (f1.exists() and f2.exists()):
            missing.append(pid)
            continue
        d1, d2 = json.loads(f1.read_text()), json.loads(f2.read_text())
        elig_pairs.append((bool(d1.get("eligible")), bool(d2.get("eligible"))))
        a1, a2 = facets(d1), facets(d2)
        for ax in AXES:
            rows[ax].append((a1[ax], a2[ax]))
            if a1[ax] != a2[ax]:
                disagreements.append({"paper_id": pid, "axis": ax,
                                      "coder1": a1[ax], "coder2": a2[ax]})

    out = {
        "n_scored": len(elig_pairs),
        "sample_drawn": len(sample["paper_ids"]),
        "missing_recodes": missing,
        "eligibility": dict(zip(("raw_agreement", "cohens_kappa"), kappa(elig_pairs))),
        "by_axis": {},
        "disagreements": disagreements,
    }
    for ax in AXES:
        obs, k = kappa(rows[ax])
        out["by_axis"][ax] = {"raw_agreement": obs, "cohens_kappa": k,
                              "n": len(rows[ax]),
                              "disagreements": sum(1 for a, bb in rows[ax] if a != bb)}
    (DATA / "facet-kappa.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "disagreements"}, indent=1))
    print(f"\n{len(disagreements)} facet disagreements across {len(AXES)} axes")
    for d in disagreements:
        print(f"  {d['paper_id']}  {d['axis']:<18} {str(d['coder1']):<20} vs {d['coder2']}")


if __name__ == "__main__":
    main()
