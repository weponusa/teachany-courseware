#!/bin/bash
# final-verify-ith.sh — it-h 5 课件最终验证 + 全库复扫
cd "$(dirname "$0")/.."
for c in it-h-sorting-searching it-h-programming-basics it-h-data-structures it-h-control-structures it-h-functions-modules; do
  r=$(node scripts/validate-courseware.cjs community/$c 2>&1 | grep -o "总评：[0-9/]*")
  echo "$c $r"
done
echo "=== 全库复扫 v2 ==="
python3 scripts/scan-fake-modules-v2.py 2>&1 | head -14
