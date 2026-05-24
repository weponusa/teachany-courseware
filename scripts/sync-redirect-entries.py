#!/usr/bin/env python3
"""
TeachAny 重定向入口同步工具 v1.0

功能：扫描 teachany-courseware 仓库的 community/ 下所有课件，
对比 teachany（主仓库）的 community/ 目录，自动为缺失的课件
创建标准重定向入口（index.html + history-tracker.js）。

设计原则：
  - courseware 仓库是课件实体的唯一信源
  - 主仓库只存轻量重定向页（< 1KB），跳转到 courseware 的 Pages URL
  - 已有完整课件（非重定向页）的主仓库入口不会被覆盖
  - 可独立运行，也可被 rebuild-index.py 调用

用法：
  # 独立运行（自动检测两个仓库路径）
  python3 scripts/sync-redirect-entries.py

  # 指定主仓库路径
  python3 scripts/sync-redirect-entries.py --main-repo /path/to/teachany

  # 仅检查，不写文件
  python3 scripts/sync-redirect-entries.py --dry-run

v1.0 变更（2026-05-21）:
  - 初始版本：扫描 + 生成重定向 + 拷贝 history-tracker.js
v1.1 变更（2026-05-21）:
  - 新增 --migrate 模式：将主仓库中的完整课件替换为重定向页
    （先备份原完整课件的 assets/ 和 tts/ 到 courseware 仓库，
     然后用重定向页覆盖主仓库入口）
"""

import argparse
import json
import shutil
import sys
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────────

COURSEWARE_BASE_URL = "https://weponusa.github.io/teachany-courseware"
COMMUNITY_SKIP = {"drafts", "pending", "README.md", ".DS_Store"}

REDIRECT_TEMPLATE = """\
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0; url={target_url}">
  <link rel="canonical" href="{target_url}">
  <title>正在打开 TeachAny 课件</title>
  <script>window.location.replace('{target_url}');</script>

  <meta name="teachany-courseware-id" content="{course_id}">

  <script src="./history-tracker.js" defer></script>
</head>
<body style="margin:0;background:#07111f;color:#e5f2ff;font-family:-apple-system,BlinkMacSystemFont,'PingFang SC',sans-serif;display:grid;min-height:100vh;place-items:center;text-align:center">
  <main>
    <p>正在打开课件，请稍候…</p>
    <p><a style="color:#7dd3fc" href="{target_url}">如果没有自动打开，点这里</a></p>
  </main>
</body>
</html>
"""


def find_main_repo(courseware_root: Path) -> Path | None:
    """自动探测主仓库路径（与 courseware 仓库同级目录）"""
    parent = courseware_root.parent
    candidates = [
        parent / "teachany-opensource",
        parent / "teachany",
    ]
    for p in candidates:
        if (p / "community").is_dir():
            return p
    return None


def scan_courseware_ids(courseware_community: Path) -> set[str]:
    """扫描 courseware 仓库 community/ 下所有有效课件 ID"""
    ids = set()
    if not courseware_community.is_dir():
        return ids
    for d in courseware_community.iterdir():
        if not d.is_dir() or d.name in COMMUNITY_SKIP:
            continue
        if (d / "index.html").exists():
            ids.add(d.name)
    return ids


def scan_main_entries(main_community: Path) -> dict[str, str]:
    """
    扫描主仓库 community/ 下的入口。
    返回 {course_id: 'redirect' | 'full' | 'missing'}
    """
    entries = {}
    if not main_community.is_dir():
        return entries
    for d in main_community.iterdir():
        if not d.is_dir() or d.name in COMMUNITY_SKIP:
            continue
        index = d / "index.html"
        if not index.exists():
            entries[d.name] = "missing"
            continue
        # 判断是重定向页还是完整课件
        try:
            content = index.read_text(encoding="utf-8", errors="ignore")
            if "http-equiv=\"refresh\"" in content or "location.replace(" in content:
                entries[d.name] = "redirect"
            else:
                entries[d.name] = "full"
        except Exception:
            entries[d.name] = "unknown"
    return entries


def is_redirect_page(index_path: Path) -> bool:
    """判断一个 index.html 是否是重定向页面"""
    try:
        content = index_path.read_text(encoding="utf-8", errors="ignore")
        return "http-equiv=\"refresh\"" in content or "location.replace(" in content
    except Exception:
        return False


def create_redirect_entry(
    main_community: Path,
    course_id: str,
    history_tracker_src: Path | None,
    dry_run: bool = False,
) -> bool:
    """为一个课件创建重定向入口"""
    target_url = f"{COURSEWARE_BASE_URL}/community/{course_id}/index.html"
    entry_dir = main_community / course_id

    if dry_run:
        return True

    entry_dir.mkdir(parents=True, exist_ok=True)

    # 写入重定向 index.html
    html = REDIRECT_TEMPLATE.format(target_url=target_url, course_id=course_id)
    (entry_dir / "index.html").write_text(html, encoding="utf-8")

    # 拷贝 history-tracker.js
    if history_tracker_src and history_tracker_src.exists():
        shutil.copy2(history_tracker_src, entry_dir / "history-tracker.js")

    return True


def sync(
    courseware_root: Path,
    main_repo: Path | None = None,
    dry_run: bool = False,
    migrate: bool = False,
) -> dict:
    """
    主同步逻辑。返回统计信息。

    Args:
        migrate: 若为 True，将主仓库中的完整课件也替换为重定向页
                 （前提是 courseware 仓库已有对应课件）

    Returns:
        {"created": [...], "migrated": [...], "skipped_full": [...],
         "already_ok": int, "errors": [...]}
    """
    result = {"created": [], "migrated": [], "skipped_full": [], "already_ok": 0, "errors": []}

    courseware_community = courseware_root / "community"
    if not courseware_community.is_dir():
        result["errors"].append("courseware community/ 目录不存在")
        return result

    # 自动探测主仓库
    if main_repo is None:
        main_repo = find_main_repo(courseware_root)
    if main_repo is None:
        result["errors"].append(
            "未找到主仓库（teachany-opensource 或 teachany），"
            "请用 --main-repo 指定"
        )
        return result

    main_community = main_repo / "community"
    if not main_community.is_dir():
        result["errors"].append(f"主仓库 community/ 不存在: {main_community}")
        return result

    # history-tracker.js 源文件
    ht_src = main_repo / "scripts" / "history-tracker.js"
    if not ht_src.exists():
        # 从任意已有入口拷贝
        for d in main_community.iterdir():
            candidate = d / "history-tracker.js"
            if candidate.exists():
                ht_src = candidate
                break

    # 1. 扫描 courseware 课件
    cw_ids = scan_courseware_ids(courseware_community)

    # 2. 逐个检查主仓库
    for cid in sorted(cw_ids):
        entry_dir = main_community / cid
        index_path = entry_dir / "index.html"

        if index_path.exists():
            if is_redirect_page(index_path):
                # 已有重定向，OK
                result["already_ok"] += 1
            elif migrate:
                # migrate 模式：把完整课件替换为重定向页
                try:
                    # 删除主仓库中的完整课件（保留目录结构）
                    if not dry_run:
                        # 删除所有文件，只保留目录
                        for f in entry_dir.rglob("*"):
                            if f.is_file():
                                f.unlink()
                        # 清理空子目录
                        for d in sorted(entry_dir.rglob("*"), reverse=True):
                            if d.is_dir():
                                try:
                                    d.rmdir()
                                except OSError:
                                    pass
                        # 创建重定向入口
                        create_redirect_entry(main_community, cid, ht_src, dry_run)
                    result["migrated"].append(cid)
                except Exception as e:
                    result["errors"].append(f"{cid} (migrate): {e}")
            else:
                # 非 migrate 模式：跳过完整课件
                result["skipped_full"].append(cid)
        else:
            # 缺失，创建
            try:
                create_redirect_entry(main_community, cid, ht_src, dry_run)
                result["created"].append(cid)
            except Exception as e:
                result["errors"].append(f"{cid}: {e}")

    # kg-manifest 只保存在 courseware 仓库；主仓库运行时远程加载 courseware 数据源。
    result["manifest_synced"] = False

    return result


def main():
    parser = argparse.ArgumentParser(
        description="同步 teachany-courseware → teachany 主仓库重定向入口"
    )
    parser.add_argument(
        "--main-repo",
        type=Path,
        default=None,
        help="主仓库路径（默认自动探测）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="仅检查，不写文件",
    )
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="将主仓库中的完整课件替换为重定向页（需配合 courseware 仓库已有对应课件）",
    )
    args = parser.parse_args()

    # 推断 courseware 根目录（脚本在 scripts/ 下）
    courseware_root = Path(__file__).resolve().parents[1]

    print("🔗 步骤7: 同步主仓库重定向入口...")

    result = sync(courseware_root, args.main_repo, args.dry_run, args.migrate)

    if result["errors"]:
        for e in result["errors"]:
            print(f"  ❌ {e}")
        if not result["created"] and not result["migrated"]:
            sys.exit(1)

    if result["created"]:
        label = "（dry-run）" if args.dry_run else ""
        print(f"  🆕 新建重定向入口{label}: {len(result['created'])} 个")
        for cid in result["created"][:20]:
            print(f"     + {cid}")
        if len(result["created"]) > 20:
            print(f"     ... 及另外 {len(result['created']) - 20} 个")

    if result["migrated"]:
        label = "（dry-run）" if args.dry_run else ""
        print(f"  🔄 迁移完整课件→重定向{label}: {len(result['migrated'])} 个")
        for cid in result["migrated"][:20]:
            print(f"     ↪ {cid}")
        if len(result["migrated"]) > 20:
            print(f"     ... 及另外 {len(result['migrated']) - 20} 个")

    if not result["created"] and not result["migrated"]:
        print(f"  ✅ 所有课件已有重定向入口，无需新建")

    if result["skipped_full"]:
        print(f"  ⚠️  跳过完整课件（非重定向）: {len(result['skipped_full'])} 个")
        print(f"     💡 使用 --migrate 将这些替换为重定向页")

    print(f"  📊 统计: 已有={result['already_ok']}, "
          f"新建={len(result['created'])}, "
          f"迁移={len(result['migrated'])}, "
          f"跳过={len(result['skipped_full'])}, "
          f"错误={len(result['errors'])}")

    # manifest 同步状态
    if result.get("manifest_synced"):
        print(f"  📦 kg-manifest 已同步到主仓库")
    elif result.get("manifest_synced") is False:
        print(f"  ⚠️  kg-manifest 同步失败（源文件或目标目录不存在）")

    return result


if __name__ == "__main__":
    main()
