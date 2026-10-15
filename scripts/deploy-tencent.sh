#!/usr/bin/env bash
# deploy-tencent.sh — 把发布产物 _site/ 增量镜像到腾讯云服务器（主站/备用源）
#
# 用法:
#   bash scripts/deploy-tencent.sh /tmp/teachany-site-build
#   环境变量（或写入 scripts/.tencent-deploy.env，600 权限，勿提交）:
#     TENCENT_HOST   服务器 IP 或域名（必填）
#     TENCENT_USER   SSH 用户（默认 root）
#     TENCENT_PORT   SSH 端口（默认 22）
#     TENCENT_WEBROOT 服务器上站点根目录（默认 /var/www/teachany）
#     TENCENT_DRYRUN 1=只演练不同步
#
# 安全设计:
#   - rsync --delete 只作用于 $TENCENT_WEBROOT 内部，且先做 --dry-run 统计变动
#   - 变动超过 3000 个文件时中止（防止误删整站，人工确认后加 --force-sync 重跑）
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENV_FILE="$SCRIPT_DIR/.tencent-deploy.env"
[ -f "$ENV_FILE" ] && set -a && source "$ENV_FILE" && set +a

HOST="${TENCENT_HOST:?未设置 TENCENT_HOST}"
USER_="${TENCENT_USER:-root}"
PORT="${TENCENT_PORT:-22}"
WEBROOT="${TENCENT_WEBROOT:-/var/www/teachany}"
DRYRUN="${TENCENT_DRYRUN:-0}"
FORCE="${2:-$1}"
SRC="${1:-}"
case "$FORCE" in --force-sync) SRC="${1:-}";; esac
[ -z "$SRC" ] && SRC="${TEACHANY_SITE_DIR:-$SCRIPT_DIR/../_site}"
[ -d "$SRC" ] || { echo "❌ 发布目录不存在: $SRC（先跑 scripts/build-publish-site.sh）"; exit 1; }

SSH_OPTS="-p $PORT -o StrictHostKeyChecking=accept-new -o ConnectTimeout=15"
RSYNC_SSH="ssh $SSH_OPTS"

echo "== 目标: $USER_@$HOST:$PORT → $WEBROOT"
echo "== 来源: $SRC ($(find "$SRC" -type f | wc -l | tr -d ' ') 文件, $(du -sh "$SRC" | cut -f1))"

# 远端就位:目录 + nginx 配置一次性初始化
ssh $SSH_OPTS "$USER_@$HOST" "mkdir -p $WEBROOT"

DRY=""
[ "$DRYRUN" = "1" ] && DRY="--dry-run"
STATS=$(rsync -az $DRY $RSYNC_SSH \
  --delete --delete-excluded \
  --stats \
  "$SRC/" "$USER_@$HOST:$WEBROOT/" || { echo "❌ rsync 失败"; exit 1; })

echo "$STATS" | grep -E 'files transferred|deleted|total size' || true
CHANGED=$(echo "$STATS" | sed -n 's/.*files transferred: \([0-9]*\).*/\1/p')
DELETED=$(echo "$STATS" | sed -n 's/.*deleted files: \([0-9]*\).*/\1/p')
CHANGED=${CHANGED:-0}; DELETED=${DELETED:-0}

if [ "$DRYRUN" != "1" ] && [ $((CHANGED + DELETED)) -gt 3000 ] && [ "${FORCE}" != "--force-sync" ]; then
  echo "⛔ 变动量 $((CHANGED + DELETED)) 超过安全阈值 3000，疑似误操作。确认无误后加 --force-sync 重跑。"
  exit 1
fi

# 首次部署时放 nginx 配置（幂等）
ssh $RSYNC_SSH "$USER_@$HOST" "command -v nginx >/dev/null || { echo '⚠ 服务器未装 nginx，请参考 docs/TENCENT-MIRROR.md 安装'; }"
echo "✅ 同步完成（changed=$CHANGED deleted=$DELETED）"
