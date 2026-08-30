#!/usr/bin/env bash
# Regenerates every number in the paper from the shipped database, then checks
# each one independently. Exits non-zero on any mismatch, and also on any number
# the verifier could not check -- an unchecked number is a failure, not a skip.
#
# Needs: python3, and the `phd` CLI (github.com/kidkuddy/dr, cli/phd).
set -euo pipefail
cd "$(dirname "$0")"
set -a; . ./local.env; set +a
python3 100-facts.py
python3 101-verify.py
