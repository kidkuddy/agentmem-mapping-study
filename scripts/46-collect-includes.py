#!/usr/bin/env python3
"""Collects the screening includes, with their abstracts, for the next stages."""
import json, os, pathlib, subprocess

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

raw = subprocess.run(["phd", "paper", "list-by-stage", "-stage", "screening_included",
                      "-topic-id", IDS["TOPIC_ID"], "-limit", "5000"],
                     capture_output=True, text=True, check=True).stdout
ids = {p["id"] for p in json.loads(raw).get("papers", [])}
scope = json.loads((DATA / "scope-kept.json").read_text())
out = [r for r in scope if r["id"] in ids]
(DATA / "screening-includes.json").write_text(json.dumps(out, indent=1))
print(json.dumps({"screening_includes": len(out), "with_abstract":
                  sum(1 for r in out if r.get("abstract"))}, indent=1))
