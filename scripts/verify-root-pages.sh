#!/usr/bin/env bash
# 校验站点根 HTML 不是 pbl-map/engine 跳转桩（发布前可单独运行）
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PAGES=(tree.html knowledge-map.html path.html my.html pbl.html index.html commercial-license.html)
fail=0
for f in "${PAGES[@]}"; do
  p="$ROOT/$f"
  if [ ! -f "$p" ]; then
    echo "❌ 缺少 $f"
    fail=1
    continue
  fi
  if grep -q "location.replace('../../" "$p" 2>/dev/null; then
    echo "❌ $f 是跳转桩，请从 _site_deploy 或 git 历史恢复完整页面"
    fail=1
    continue
  fi
  size=$(wc -c < "$p" | tr -d ' ')
  if [ "$size" -lt 1000 ]; then
    echo "❌ $f 过小 (${size}B)，可能已损坏"
    fail=1
    continue
  fi
  echo "✅ $f (${size}B)"
done
exit "$fail"
