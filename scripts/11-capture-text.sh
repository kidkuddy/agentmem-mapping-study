#!/usr/bin/env bash
# Captures title + abstract + venue + url for every identified record.
#
# `phd search` without -dry-run returns paper_ids only; `phd paper list` has no
# abstract column and `phd export csv` does not emit one either. The remaining
# options are one `phd paper get` per record - roughly 1500 round trips to a
# remote database - or re-issuing the same 36 (query, provider) pairs as dry
# runs, which returns the same records with their text in 36 calls and stores
# nothing. Second option, for the same reason as everywhere else: the round trip
# is the cost, not the data.
#
# Run AFTER 10-search.sh, so the two are not competing for the same rate limits.
set -uo pipefail
cd "$(dirname "$0")"
set -a; . ./local.env; set +a   # local sqlite, not the remote
mkdir -p text

cap_for() { case "$1" in arxiv|openalex) echo 200 ;; esac; }

# Read the query set from 10-search.sh so there is exactly one declared list.
# `mapfile` is bash 4; macOS ships bash 3.2, so this reads the lines instead.
QUERIES=()
while IFS= read -r line; do
  QUERIES+=("$line")
done < <(sed -n '/^QUERIES=(/,/^)/p' 10-search.sh | sed '1d;$d' | sed 's/^ *"//; s/"$//')
PROVIDERS=(arxiv openalex)

i=0
for q in "${QUERIES[@]}"; do
  i=$((i+1))
  slug=$(printf '%s' "$q" | tr -cs 'a-zA-Z0-9' '-' | tr 'A-Z' 'a-z' | cut -c1-44)
  for prov in "${PROVIDERS[@]}"; do
    out="text/$(printf '%02d' $i)-${prov}-${slug}.json"
    [ -s "$out" ] && continue
    printf 'text  [%-9s] %s ... ' "$prov" "$q"
    if timeout 180 phd search -dry-run -query "$q" -providers "$prov" \
         -max-results "$(cap_for "$prov")" -start-year 2023 > "$out" 2>/dev/null; then
      python3 -c "import json;print(len(json.load(open('$out')).get('papers',[])),'records')" 2>/dev/null || echo "unparseable"
    else
      echo "FAILED"; rm -f "$out"
    fi
  done
done

python3 - <<'PY'
import json, glob, re
seen = {}
for f in glob.glob('text/*.json'):
    try: d = json.load(open(f))
    except Exception: continue
    for r in d.get('papers', []):
        k = re.sub(r'[^a-z0-9]+', ' ', (r.get('title') or '').lower()).strip()
        if k and len(r.get('abstract') or '') > len(seen.get(k, {}).get('abstract') or ''):
            seen[k] = r
json.dump(seen, open('text-index.json', 'w'), indent=1)
withtext = sum(1 for r in seen.values() if r.get('abstract'))
print(f"text-index.json: {len(seen)} unique titles, {withtext} with an abstract")
PY
