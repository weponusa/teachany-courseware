#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."
mapfile -t CIDS < reports/hero-notext-remaining.txt
ARGS=(--limit 0)
for c in "${CIDS[@]}"; do
  [[ -n "$c" ]] || continue
  ARGS+=(--cid "$c")
done
export HERO_BACKEND=agnes HERO_GEN_TIMEOUT=90 HERO_NTV_SLOTS=ntv9,ntva,ntvb
echo "retrying ${#CIDS[@]} courses"
PYTHONUNBUFFERED=1 python3 scripts/batch_replace_hero_notext.py --sleep 5 "${ARGS[@]}"
