#!/usr/bin/env bash
# ============================================================
# TeachAny pre-push hook
# ------------------------------------------------------------
# 用户课件统一以当前 Git 用户身份上传到 community/<course-id>/。
# examples/ 只保留存量官方示例，不作为课件制作流程的上传目标。
#
# 本 hook 会：
#   1. 拦截 examples/<id>/ 下的新增或修改，避免用户课件误入官方示例目录
#   2. 对涉及的 community/<id>/ 课件运行 validate-courseware.py（质检闸门）
#
# 安装方式（一次性，从仓库根目录）：
#   ln -sf ../../scripts/pre-push.sh .git/hooks/pre-push
#   chmod +x scripts/pre-push.sh
#
# 跳过 validator（仅用于非课件改动，如 README/CI 脚本修复）：
#   TEACHANY_SKIP_VALIDATE=1 git push
# ============================================================

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

while read -r local_ref local_sha remote_ref remote_sha; do
    if [ "$local_sha" = "0000000000000000000000000000000000000000" ]; then
        continue
    fi

    if [ "$remote_sha" = "0000000000000000000000000000000000000000" ]; then
        if git rev-parse --verify origin/main >/dev/null 2>&1; then
            base="origin/main"
        else
            base="$(git rev-list --max-parents=0 "$local_sha" | head -1)"
        fi
    else
        base="$remote_sha"
    fi

    changed_examples=$(git diff --name-only "$base" "$local_sha" 2>/dev/null \
        | grep -E '^examples/[^/]+/' \
        | awk -F/ '{print $2}' \
        | sort -u \
        | grep -v '^_template$' \
        | grep -v '^$' || true)

    if [ -n "$changed_examples" ]; then
        echo ""
        echo "❌ 检测到 examples/ 目录下的课件变更，已拒绝 push："
        echo "$changed_examples" | sed 's/^/   - examples\//'
        echo ""
        echo "用户课件请上传到 community/<course-id>/，然后运行："
        echo "   python3 scripts/rebuild-index.py"
        echo "   git add -A && git commit -m \"feat: 新增课件 <course-id>\""
        echo "   git push origin main"
        echo ""
        exit 1
    fi

    changed_community=$(git diff --name-only "$base" "$local_sha" 2>/dev/null \
        | grep -E '^community/[^/]+/' \
        | grep -vE '^community/(drafts|pending|archive)/' \
        | awk -F/ '{print $2}' \
        | sort -u \
        | grep -v '^$' || true)

    if [ -z "$changed_community" ]; then
        continue
    fi

    if [ "$TEACHANY_SKIP_VALIDATE" = "1" ]; then
        echo "⚠️  TEACHANY_SKIP_VALIDATE=1 已启用，跳过 validator 检查"
        continue
    fi

    is_canonical_url_only_change() {
        local id="$1"
        local diff_text
        diff_text=$(git diff -U0 "$base" "$local_sha" -- "community/$id/" 2>/dev/null || true)
        if [ -z "$diff_text" ]; then
            return 1
        fi
        while IFS= read -r line; do
            case "$line" in
                "diff --git"*|"index "*|"--- "*|"+++ "*|"@@ "*)
                    continue
                    ;;
                +*|-*)
                    if echo "$line" | grep -Eq 'weponusa\.github\.io/teachany|www\.teachany\.cn'; then
                        continue
                    fi
                    return 1
                    ;;
                *)
                    continue
                    ;;
            esac
        done <<EOF
$diff_text
EOF
        return 0
    }

    # 仅新增/更新 knowledge-context.json（知识层 KCP），不改动 index.html → 跳过整课质检
    is_kcp_only_change() {
        local id="$1"
        local files
        files=$(git diff --name-only "$base" "$local_sha" -- "community/$id/" 2>/dev/null || true)
        if [ -z "$files" ]; then
            return 1
        fi
        while IFS= read -r f; do
            [ -z "$f" ] && continue
            case "$f" in
                community/$id/knowledge-context.json) continue ;;
                *) return 1 ;;
            esac
        done <<EOF
$files
EOF
        return 0
    }

    validate_ids=""
    for id in $changed_community; do
        index="community/$id/index.html"
        if [ -f "$index" ] \
            && grep -q "www.teachany.cn" "$index" \
            && grep -Eq "http-equiv=\"refresh\"|location\.replace" "$index"; then
            echo "  ↪️  community/$id 是轻量跳转入口，跳过课件质检"
            continue
        fi
        if is_canonical_url_only_change "$id"; then
            echo "  ↪️  community/$id 仅修改 canonical URL，跳过课件质检"
            continue
        fi
        if is_kcp_only_change "$id"; then
            echo "  ↪️  community/$id 仅 knowledge-context.json（KCP），跳过课件质检"
            continue
        fi
        validate_ids="$validate_ids $id"
    done

    if [ -z "$validate_ids" ]; then
        continue
    fi

    echo ""
    echo "🔍 检测到以下社区课件变更，开始质检："
    echo "$validate_ids" | tr ' ' '\n' | grep -v '^$' | sed 's/^/   - community\//'

    if ! python3 scripts/validate-courseware.py $validate_ids 2>&1; then
        echo ""
        echo "❌ validate-courseware.py 校验失败，push 被拒绝"
        echo ""
        echo "修复建议："
        echo "   1. 按上面报错列表修复课件（补 manifest / 补音频 / 补图 / 改 node_id）"
        echo "   2. 确认 python3 scripts/validate-courseware.py <id> 输出 0 错误"
        echo "   3. 重新运行 python3 scripts/rebuild-index.py 后再提交"
        echo ""
        exit 1
    fi

    echo "✅ 所有社区课件质检通过，允许 push"
done

exit 0
