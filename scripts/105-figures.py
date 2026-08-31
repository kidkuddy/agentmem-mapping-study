#!/usr/bin/env python3
"""Generates the map figures from map.json — the same data the prose cites.

A figure produced on a separate path from the numbers is a figure that goes stale
silently, and it is the thing a reviewer notices first. These read map.json,
which reads the database.

Petersen's output is a bubble plot: two scatterplots sharing a y-axis, bubble area
proportional to count, and the EMPTY CELLS are the finding. So empty cells are
drawn, not omitted — a faint marker at every zero, because a blank region in a
scatterplot is ambiguous between "nothing here" and "nothing plotted here".
"""
import json, pathlib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = pathlib.Path(__file__).parent
# In the replication package the study data sits in ../data while the
# scripts stay in ../scripts. DATA is the only path that differs from
# the layout these scripts were executed in.
DATA = (HERE / ".." / "data").resolve()
OUT = (HERE / ".." / "figures").resolve()
M = json.loads((DATA / "map.json").read_text())
F = json.loads((DATA / "facts.json").read_text())

LABEL = {
    "prompt_resident": "prompt-resident", "vector_store": "vector store",
    "graph_store": "graph store", "relational_db": "relational DB",
    "filesystem": "filesystem", "kv_cache": "KV cache",
    "multi_store": "multi-store", "other": "other",
    "append_only": "append-only", "summarize_compress": "summarise / compress",
    "reflect_synthesize": "reflect / synthesise", "edit_in_place": "edit in place",
    "agent_tool_invoked": "agent tool-invoked", "none_declared": "none declared",
    "similarity_topk": "similarity top-$k$", "recency_window": "recency window",
    "structured_query": "structured query", "agent_directed": "agent-directed",
    "always_in_context": "always in context", "hybrid": "hybrid",
    "controlled_experiment": "controlled experiment",
    "benchmark_evaluation": "benchmark evaluation", "case_study": "case study",
    "proof_of_concept": "proof of concept", "simulation": "simulation",
    "none": "none", "validation": "validation", "evaluation": "evaluation",
    "solution": "solution proposal", "philosophical": "philosophical",
    "opinion": "opinion", "experience": "experience",
    "method": "method", "tool": "tool", "model": "model", "metric": "metric",
    "framework": "framework", "dataset": "dataset",
}


def lab(v):
    return LABEL.get(v, v.replace("_", " "))


def bubble(ax, cells, xorder, yorder, title):
    """One panel. x values across, y values down, area proportional to count."""
    xi = {v: i for i, v in enumerate(xorder)}
    yi = {v: i for i, v in enumerate(yorder)}
    xs, ys, ss, ns = [], [], [], []
    for y in yorder:
        row = cells.get(y, {})
        for x in xorder:
            n = row.get(x, 0)
            xs.append(xi[x]); ys.append(yi[y]); ns.append(n)
            # Area proportional to count, with a floor so a zero is a visible
            # dot rather than an absence. Petersen's finding lives in the zeros.
            ss.append(18 + 62 * n)
    filled = [(x, y, s, n) for x, y, s, n in zip(xs, ys, ss, ns) if n]
    empty = [(x, y) for x, y, n in zip(xs, ys, ns) if not n]
    if empty:
        ax.scatter([e[0] for e in empty], [e[1] for e in empty], s=14,
                   facecolors="none", edgecolors="#c9c9c9", linewidths=0.7, zorder=1)
    ax.scatter([f[0] for f in filled], [f[1] for f in filled],
               s=[f[2] for f in filled], color="#33506e", alpha=0.75, zorder=2)
    for x, y, _, n in filled:
        ax.annotate(str(n), (x, y), ha="center", va="center", color="white",
                    fontsize=6.5, zorder=3)
    ax.set_xticks(range(len(xorder)))
    ax.set_xticklabels([lab(v) for v in xorder], rotation=38, ha="right", fontsize=7.5)
    ax.set_yticks(range(len(yorder)))
    ax.set_yticklabels([lab(v) for v in yorder], fontsize=7.5)
    ax.set_xlim(-0.6, len(xorder) - 0.4)
    ax.set_ylim(-0.6, len(yorder) - 0.4)
    ax.invert_yaxis()
    ax.grid(True, which="major", color="#eeeeee", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.set_title(title, fontsize=8.5, pad=6)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)


def ordered(axis, cells, allowed):
    """Rows sorted by total, descending — but unoccupied values kept, at the end.

    Dropping a value the corpus does not occupy would delete exactly the row the
    map exists to show."""
    tot = {v: sum(cells.get(v, {}).values()) for v in allowed}
    return sorted(allowed, key=lambda v: (-tot[v], v))


def main():
    sub_rt = M["maps"]["substrate_x_research_type"]["cells"]
    sub_ct = M["maps"]["substrate_x_contribution"]["cells"]
    subs = ordered("substrate", sub_rt,
                   ["vector_store", "multi_store", "graph_store", "prompt_resident",
                    "other", "filesystem", "relational_db", "kv_cache"])
    rts = ["validation", "evaluation", "solution", "philosophical", "opinion", "experience"]
    cts = ["framework", "method", "dataset", "metric", "tool", "model"]

    fig, axes = plt.subplots(1, 2, figsize=(7.4, 3.3), sharey=True)
    bubble(axes[0], sub_ct, cts, subs, "(a) contribution type")
    bubble(axes[1], sub_rt, rts, subs, "(b) research type (Wieringa)")
    axes[0].set_ylabel("memory substrate", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "map-substrate.pdf", bbox_inches="tight")
    plt.close(fig)

    wr = M["maps"]["write_x_retrieval"]["cells"]
    writes = ordered("write_policy", wr,
                     ["edit_in_place", "reflect_synthesize", "append_only",
                      "summarize_compress", "agent_tool_invoked", "none_declared"])
    rets = ["hybrid", "similarity_topk", "always_in_context", "structured_query",
            "agent_directed", "recency_window", "none_declared"]
    fig, ax = plt.subplots(figsize=(4.4, 3.0))
    bubble(ax, wr, rets, writes, "")
    ax.set_ylabel("write policy", fontsize=8)
    ax.set_xlabel("retrieval policy", fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "map-policy.pdf", bbox_inches="tight")
    plt.close(fig)

    print(f"wrote {OUT/'map-substrate.pdf'} and map-policy.pdf")
    print(f"  substrates plotted: {len(subs)}, of which unoccupied: "
          f"{sum(1 for s in subs if not sum(sub_rt.get(s, {}).values()))}")


if __name__ == "__main__":
    main()
