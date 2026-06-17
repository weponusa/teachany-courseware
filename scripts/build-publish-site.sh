#!/usr/bin/env bash
# 构建 teachany.cn / gh-pages 发布目录 _site/
# 约束：Cloudflare Pages 免费版 ≤ 20,000 文件；默认门禁 19,000 留余量。
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${1:-$ROOT/_site}"
MAX_FILES="${PUBLISH_MAX_FILES:-19000}"

COMMUNITY_EXCLUDES=(
  --exclude='remotion/'
  --exclude='*/assets/scripts/'
  --exclude='drafts/'
  --exclude='pending/'
  --exclude='archive/'
  --exclude='reading-academy/'
  --exclude='*.teachany'
)

echo "📦 Building publish site → $OUT"
rm -rf "$OUT"
mkdir -p "$OUT"

# 1. 社区课件（排除草稿/待审/归档/重复 reading-academy/打包文件）
rsync -a "${COMMUNITY_EXCLUDES[@]}" "$ROOT/community/" "$OUT/community/"

# 2. 站点公共资源
rsync -a --exclude='maps/physical/' "$ROOT/assets/" "$OUT/assets/"

# 3. 数据（排除 venv、断链、构建期资料；kp 卫星文件仅用于离线管线，站点读 trees/*.json）
rsync -a \
  --exclude='.venv/' \
  --exclude='history' \
  --exclude='geography' \
  --exclude='kp/' \
  --exclude='curriculum-sources/' \
  --exclude='kp/_backups/' \
  "$ROOT/data/" "$OUT/data/"

# 4. 根级页面与索引
touch "$OUT/.nojekyll"
for f in \
  404.html index.html courseware-registry.json registry.json registry-v2.json \
  commercial-license.html pbl.html tree.html knowledge-map.html path.html \
  my.html license.html imported-course.html reading.html
do
  if [ -f "$ROOT/$f" ]; then
    cp "$ROOT/$f" "$OUT/"
  fi
done

# 5. Cloudflare 重定向（阅读学院已迁至 read.teachany.cn）
if [ -f "$ROOT/_redirects" ]; then
  cp "$ROOT/_redirects" "$OUT/"
fi

FILE_COUNT="$(find "$OUT" -type f | wc -l | tr -d ' ')"
SIZE="$(du -sh "$OUT" | cut -f1)"

echo "✅ _site built: ${FILE_COUNT} files, ${SIZE} (limit ${MAX_FILES})"
echo "Top-level:"
ls "$OUT"

if [ "$FILE_COUNT" -gt "$MAX_FILES" ]; then
  echo ""
  echo "❌ 发布文件数 ${FILE_COUNT} 超过门禁 ${MAX_FILES}（Cloudflare Pages 上限 20000）"
  echo "   请排除更多非运行时目录，或迁移大资源到 R2/CDN。"
  echo ""
  echo "文件数 TOP 目录："
  for d in community assets data; do
    if [ -d "$OUT/$d" ]; then
      c="$(find "$OUT/$d" -type f | wc -l | tr -d ' ')"
      echo "   $d: $c"
    fi
  done
  exit 1
fi
