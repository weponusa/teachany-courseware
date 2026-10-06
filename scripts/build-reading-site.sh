#!/usr/bin/env bash
# 构建 read.teachany.cn 发布目录（reading-academy 内容作为站点根）
# 约束：Cloudflare Pages 免费版 ≤ 20,000 文件；默认门禁 19,000 留余量。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/_reading_site}"
MAX_FILES="${READING_MAX_FILES:-19000}"

echo "📖 Building reading academy site → $OUT"
rm -rf "$OUT"
mkdir -p "$OUT"

rsync -a "$ROOT/reading-academy/" "$OUT/"
touch "$OUT/.nojekyll"

FILE_COUNT="$(find "$OUT" -type f | wc -l | tr -d ' ')"
SIZE="$(du -sh "$OUT" | cut -f1)"

echo "✅ reading site built: ${FILE_COUNT} files, ${SIZE} (limit ${MAX_FILES})"

if [ "$FILE_COUNT" -gt "$MAX_FILES" ]; then
  echo ""
  echo "❌ 阅读学院发布文件数 ${FILE_COUNT} 超过门禁 ${MAX_FILES}（Cloudflare Pages 上限 20000）"
  exit 1
fi
