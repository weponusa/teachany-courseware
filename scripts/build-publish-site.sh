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
bash "$ROOT/scripts/verify-root-pages.sh"
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

# 4. 根级页面脚本（path/tree/index 等引用 ./scripts/，须随站发布）
mkdir -p "$OUT/scripts"
rsync -a \
  --include='*.js' \
  --include='*.css' \
  --exclude='*' \
  "$ROOT/scripts/" "$OUT/scripts/"

# 4b. learning-path.js 双份须一致（index 用 scripts/，path 用 assets/scripts/）
LP_A="$ROOT/scripts/learning-path.js"
LP_B="$ROOT/assets/scripts/learning-path.js"
if [ -f "$LP_A" ] && [ -f "$LP_B" ] && ! cmp -s "$LP_A" "$LP_B"; then
  echo "⚠️  learning-path.js 不一致，同步 scripts/ → assets/scripts/"
  cp "$LP_A" "$LP_B"
fi

# 5. 根级页面与索引
touch "$OUT/.nojekyll"
for f in \
  404.html index.html courseware-registry.json registry.json registry-v2.json \
  commercial-license.html pbl.html tree.html knowledge-map.html path.html \
  my.html license.html imported-course.html reading.html
do
  if [ -f "$ROOT/$f" ]; then
    if [[ "$f" == *.html ]] && grep -q "location.replace('../../" "$ROOT/$f" 2>/dev/null; then
      echo "❌ $f 是 pbl-map/engine 跳转桩，不能作为站点根页面发布"
      exit 1
    fi
    cp "$ROOT/$f" "$OUT/"
  fi
done

# 5b. 发布目录根页面不得含 pbl-map/engine 跳转桩
for f in tree.html knowledge-map.html path.html my.html pbl.html index.html commercial-license.html; do
  if [ -f "$OUT/$f" ] && grep -q "location.replace('../../" "$OUT/$f" 2>/dev/null; then
    echo "❌ 发布目录 $f 含跳转桩，构建中止"
    exit 1
  fi
done

# 6. Cloudflare Pages Functions（PBL API、LLM 中转等；须随 gh-pages 一并发布）
if [ -d "$ROOT/functions" ]; then
  rsync -a "$ROOT/functions/" "$OUT/functions/"
fi

# 7. Cloudflare 重定向（阅读学院已迁至 read.teachany.cn）
if [ -f "$ROOT/_redirects" ]; then
  cp "$ROOT/_redirects" "$OUT/"
fi

# 8. K12 PBL Map（pbl-map/ 目录或 ../finalpbl）
PBL_MAP_SRC="${PBL_MAP_SRC:-}"
if [ -z "$PBL_MAP_SRC" ]; then
  if [ -L "$ROOT/pbl-map" ]; then
    PBL_MAP_SRC="$(cd "$ROOT/pbl-map" && pwd -P 2>/dev/null || true)"
  elif [ -d "$ROOT/pbl-map" ]; then
    PBL_MAP_SRC="$ROOT/pbl-map"
  elif [ -d "$ROOT/../finalpbl" ]; then
    PBL_MAP_SRC="$(cd "$ROOT/../finalpbl" && pwd)"
  fi
fi
if [ -n "$PBL_MAP_SRC" ] && [ -d "$PBL_MAP_SRC" ]; then
  echo "📍 PBL Map ← $PBL_MAP_SRC"
  rsync -a \
    --exclude='engine' \
    --exclude='node_modules/' \
    --exclude='.git/' \
    "$PBL_MAP_SRC/" "$OUT/pbl-map/"
  # engine 在源目录可能是指向仓库根的 symlink，禁止 rm -rf（会误删站点根文件）
  if [ -L "$OUT/pbl-map/engine" ]; then
    rm -f "$OUT/pbl-map/engine"
  elif [ -d "$OUT/pbl-map/engine" ]; then
    rm -rf "$OUT/pbl-map/engine"
  fi
  mkdir -p "$OUT/pbl-map/engine"
  for page in index.html pbl.html tree.html knowledge-map.html path.html my.html; do
    printf '%s\n' \
      '<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">' \
      "<script>location.replace('../../${page}'+location.search+location.hash);</script>" \
      "<link rel=\"canonical\" href=\"../../${page}\"></head>" \
      "<body><p>跳转中… <a href=\"../../${page}\">TeachAny</a></p></body></html>" \
      > "$OUT/pbl-map/engine/$page"
  done
else
  echo "⚠️ PBL Map 源目录未找到，跳过 pbl-map/"
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
