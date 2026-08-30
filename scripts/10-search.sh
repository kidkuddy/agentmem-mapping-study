#!/usr/bin/env bash
# Identification. Runs the declared query set against the digital libraries and
# stores every hit against the topic.
#
# Structure and the throttling logic are taken from scripts/cogbias/10-search.sh;
# the queries, the year floor and the provider set are this study's.
#
# One provider per invocation, not all at once: Semantic Scholar rate-limits above
# ~50 results and a combined call lets it stall arxiv and openalex behind it.
# Splitting also makes the cap-bound count per (query, provider) exact, which is
# the only coverage evidence a database search has.
#
# Two providers, not four, and both omissions are deliberate.
#
# PubMed indexes biomedical literature and this population is LLM agent systems;
# querying it to raise the library count would be padding the DARE QC2 criterion
# rather than searching.
#
# Semantic Scholar was queried and removed. It answered every anonymous request
# with HTTP 429 across two environments and forty minutes - an API-key
# requirement, not a throttle a backoff can outwait. Retrying it as written cost
# three minutes per query and returned nothing. The result is a two-engine
# search, which scores zero on DARE QC2, and that is reported as a coverage
# limitation rather than argued away.
#
# Resumable: a run with a non-empty output file is skipped.
set -uo pipefail
cd "$(dirname "$0")"
set -a; . ./local.env; set +a
. ./ids.env
mkdir -p runs

cap_for() { case "$1" in arxiv|openalex) echo 200 ;; esac; }

# Eighteen queries across four concept groups: what the memory IS (1-6), what
# MOVES it (7-8, 13), where it LIVES (9-12), and how it is NAMED or MEASURED
# (14-18). Written as natural-language strands rather than boolean expressions:
# the scoping dry runs showed OpenAlex matching boolean strands so loosely that a
# single strand reported 13,743 hits, which is a property of its parser and not
# of the field.
QUERIES=(
  "LLM agent memory mechanism"
  "long-term memory large language model agent"
  "episodic memory language agent"
  "agent memory architecture persistent state"
  "memory augmented LLM agent long-horizon task"
  "conversational agent long-term memory personalization"
  "memory management context window large language model agent"
  "reflection self-generated memory language agent"
  "vector store memory retrieval augmented agent"
  "knowledge graph memory LLM agent"
  "database symbolic memory large language model agent"
  "file system external memory language model agent"
  "memory consolidation forgetting eviction LLM agent"
  "MemGPT Letta memory operating system agent"
  "long-term conversational memory benchmark evaluation"
  "cross-session memory personalization assistant LLM"
  "procedural memory skill library agent"
  "experience memory reuse LLM agent learning"
)
PROVIDERS=(arxiv openalex)

i=0
for q in "${QUERIES[@]}"; do
  i=$((i+1))
  slug=$(printf '%s' "$q" | tr -cs 'a-zA-Z0-9' '-' | tr 'A-Z' 'a-z' | cut -c1-44)
  for prov in "${PROVIDERS[@]}"; do
    max=$(cap_for "$prov")
    out="runs/$(printf '%02d' $i)-${prov}-${slug}.json"
    [ -s "$out" ] && { echo "skip  [$prov] $q"; continue; }
    printf 'run   [%-9s] %s ... ' "$prov" "$q"
    # Semantic Scholar and OpenAlex both answer a throttled request with an empty
    # result set rather than an error, so a rate-limited run is indistinguishable
    # from a genuine zero. Space the calls out and retry a zero: reporting "the
    # library found nothing" when it was throttled is a false statement about
    # coverage, and coverage is the only thing a database search defends.
    case "$prov" in semantic) sleep 8 ;; openalex) sleep 3 ;; esac
    attempt=0
    while :; do
      if timeout 300 phd search -query "$q" -topic-id "$TOPIC_ID" -providers "$prov" \
           -max-results "$max" -start-year 2023 > "$out" 2>"$out.err"; then
        n=$(python3 -c "import json;print(json.load(open('$out'))['providers'][0]['found'])" 2>/dev/null || echo -1)
        case "$prov" in
          semantic|openalex)
            if [ "$n" = "0" ] && [ "$attempt" -lt 4 ]; then
              attempt=$((attempt+1)); printf 'zero, retry %d ... ' "$attempt"; sleep 45; continue
            fi
            # A zero that survives every retry is still ambiguous: a genuine miss,
            # or a throttle window longer than the backoff. Recording it as a zero
            # would put a possible artefact into the coverage evidence, so it is
            # recorded as a failure instead - the file is removed and a later run
            # retries it. A missing run is visibly missing; a false zero is not.
            if [ "$n" = "0" ]; then
              echo "UNRESOLVED ZERO after $attempt retries - left for a later run"
              rm -f "$out" "$out.err"
              break
            fi ;;
        esac
        python3 -c "
import json
d=json.load(open('$out')); p=d['providers'][0]
print('found=%-4d stored=%-4d cap_bound=%s' % (p['found'], d['stored'], p['found']>=$max))
" || echo "unparseable"
      else
        echo "FAILED/TIMEOUT"; rm -f "$out"
      fi
      break
    done
  done
done
echo "identification complete"
