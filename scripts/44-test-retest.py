#!/usr/bin/env python3
"""Test-retest agreement on the pilot batch.

The pilot's 50 records were screened twice by independent coders working from the
guide alone: once before the pilot's feedback amended it, once after. This
compares the two runs.

It measures two different things at once, and they should not be confused:

  - **Reliability.** Two coders, same instrument-ish, same records. Percentage
    agreement and Cohen's kappa. This is the test-retest action in Petersen's
    rubric line 3, on which no mapping study he examined scored full marks.
  - **The amendment's effect.** Every disagreement is listed with both reasons,
    so a reader can see whether the amended rules moved decisions or whether the
    two coders simply differ. The amendment codified what the first run had
    already done under the uncertainty rule, so a large shift would be evidence
    the amendment did something other than what it claimed.

The post-amendment run is the one that stands. This file does not overwrite it;
it reports on it.
"""
import json, pathlib, collections

HERE = pathlib.Path(__file__).parent
# In the replication package the study data sits in ../data while the
# scripts stay in ../scripts. DATA is the only path that differs from
# the layout these scripts were executed in.
DATA = (HERE / ".." / "data").resolve()
PRE = DATA / "batches" / "retest-00-preamendment.json"
POST = DATA / "batches" / "decisions-00.json"


def load(p):
    return {d["paper_id"]: d for d in json.loads(p.read_text())["decisions"]}


def kappa(a, b):
    """Cohen's kappa on two binary labellings of the same items."""
    ids = sorted(set(a) & set(b))
    n = len(ids)
    obs = sum(1 for i in ids if a[i] == b[i]) / n
    pe = 0.0
    for label in ("include", "exclude"):
        pa = sum(1 for i in ids if a[i] == label) / n
        pb = sum(1 for i in ids if b[i] == label) / n
        pe += pa * pb
    return obs, (obs - pe) / (1 - pe) if pe < 1 else 1.0, n


def main():
    if not (PRE.exists() and POST.exists()):
        raise SystemExit("need both retest-00-preamendment.json and decisions-00.json")
    pre, post = load(PRE), load(POST)
    a = {k: v["decision"] for k, v in pre.items()}
    b = {k: v["decision"] for k, v in post.items()}
    obs, k, n = kappa(a, b)

    disagreements = []
    for i in sorted(set(a) & set(b)):
        if a[i] != b[i]:
            disagreements.append({
                "paper_id": i,
                "pre": {"decision": a[i], "rule": pre[i].get("rule"),
                        "criteria": pre[i].get("criteria"), "reason": pre[i].get("reason")},
                "post": {"decision": b[i], "rule": post[i].get("rule"),
                         "criteria": post[i].get("criteria"), "reason": post[i].get("reason")},
            })

    out = {
        "n_scored": n,
        "raw_agreement": round(obs, 4),
        "cohens_kappa": round(k, 4),
        "pre_amendment_includes": sum(1 for v in a.values() if v == "include"),
        "post_amendment_includes": sum(1 for v in b.values() if v == "include"),
        "rule_shifts": dict(collections.Counter(
            f"{pre[i].get('rule')}->{post[i].get('rule')}"
            for i in sorted(set(a) & set(b))
            if pre[i].get("rule") != post[i].get("rule"))),
        "disagreements": disagreements,
    }
    (DATA / "test-retest.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k2: v for k2, v in out.items() if k2 != "disagreements"}, indent=1))
    print(f"{len(disagreements)} disagreements")


if __name__ == "__main__":
    main()
