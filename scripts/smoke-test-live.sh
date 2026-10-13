#!/usr/bin/env bash
# 线上冒烟测试：导航页、数据、API
set -euo pipefail
BASE="${1:-https://www.teachany.cn}"
fail=0

check() {
  local name="$1" url="$2" pattern="$3"
  local body
  body=$(curl -s --max-time 25 "$url" | head -c 5000 || true)
  if echo "$body" | grep -q "location.replace('../../"; then
    echo "❌ $name — 跳转桩页"
    fail=1
    return
  fi
  if ! echo "$body" | grep -qE "$pattern"; then
    echo "❌ $name — 未匹配 /$pattern/"
    fail=1
    return
  fi
  echo "✅ $name"
}

check "tree" "$BASE/tree" "<html"
check "knowledge-map" "$BASE/knowledge-map" "全科"
check "path" "$BASE/path" "学习路径"
check "pbl" "$BASE/pbl" "PBL"
check "registry" "$BASE/registry.json" '"courses"'
check "ai-tutor" "$BASE/assets/scripts/ai-tutor.js" "v8\\.1"

code=$(curl -s -o /tmp/handoff.json -w "%{http_code}" --max-time 20 \
  "$BASE/api/pbl/handoff?id=00000000-0000-0000-0000-000000000000")
if grep -q NOT_FOUND /tmp/handoff.json 2>/dev/null; then
  echo "✅ pbl-handoff API"
else
  echo "❌ pbl-handoff API (HTTP $code)"
  fail=1
fi

exit "$fail"
