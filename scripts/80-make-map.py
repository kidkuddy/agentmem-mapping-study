#!/usr/bin/env python3
"""Generates the systematic map: the cross-tabulations behind the bubble plot.

Petersen's output is two x-y scatterplots sharing a y-axis — the topical facet on
y, contribution on one x and research type on the other, bubble area proportional
to count. The empty cells are the finding.

Every number here is computed from the database, never typed. One RQ per axis:

  RQ1  substrate x year                 which substrates are used, and when
  RQ2  substrate x write_policy           what causes a memory to exist, per substrate
       substrate x retrieval_policy       what brings it back, per substrate
  RQ3  substrate x research_type          which substrates reach a deployed setting
       substrate x research_method        how the evidence was produced
  RQ4  substrate x stratum                what practice occupies that research does not

Reports the per-axis null counts alongside, because a zero cell in a column with
many nulls means something different from a zero cell in a column with none, and
a reader cannot tell the two apart from the plot.
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


def facet_map(x, y):
    raw = subprocess.run(["phd", "facet", "map", "-topic-ids", TOPIC, "-x", x, "-y", y],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(raw)


def main():
    out = {"topic": TOPIC, "maps": {}}
    for x in ("write_policy", "retrieval_policy", "research_type",
              "research_method", "contribution", "venue_type", "stratum"):
        out["maps"][f"substrate_x_{x}"] = facet_map(x, "substrate")
    # The two policy axes crossed with each other: RQ2 asks which substrate-by-
    # policy combinations occur, and a combination can be absent on the policy
    # pair while both policies are populated against substrate.
    out["maps"]["write_x_retrieval"] = facet_map("retrieval_policy", "write_policy")

    summary = json.loads((DATA / "facet-summary.json").read_text())
    out["nulls_by_axis"] = summary.get("nulls_by_axis", {})
    out["value_counts"] = summary.get("value_counts", {})

    # Empty cells, stated as a list rather than left for a reader to spot in a
    # plot. A zero in a row with three papers is not the same claim as a zero in
    # a row with seventy-nine, so the row total travels with it.
    empties = []
    for name, m in out["maps"].items():
        cells = m.get("cells", {})          # {y_value: {x_value: count}}
        for y, row in cells.items():
            row_total = sum(row.values())
            for x, n in row.items():
                if n == 0:
                    empties.append({"map": name, "row": y, "value": x,
                                    "row_total": row_total})
    out["empty_cells"] = empties
    (DATA / "map.json").write_text(json.dumps(out, indent=1))

    print(f"maps generated: {list(out['maps'])}")
    print(f"empty cells: {len(empties)}")
    print("nulls by axis:", json.dumps(out["nulls_by_axis"]))


if __name__ == "__main__":
    main()
