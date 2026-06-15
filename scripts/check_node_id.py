#!/usr/bin/env python3
"""
check_node_id.py · v6.6 (courseware 仓内副本)

校验课件 manifest.json 的 node_id 是否存在于知识树。
ext-* PBL 课标外节点无需预注册，publish 后 rebuild-index 写入「其他知识」树。

用法：
  python3 scripts/check_node_id.py community/<course-id>
  python3 scripts/check_node_id.py --node-id ext-7be00e85
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

EXT_NODE_RE = re.compile(r"^ext-[a-f0-9]{6,12}$", re.I)
SCRIPT_DIR = Path(__file__).resolve().parent
LOCAL_REPO = SCRIPT_DIR.parent


def find_repo() -> Path | None:
    env = os.environ.get("TEACHANY_COURSEWARE_REPO", "").strip()
    candidates = [
        LOCAL_REPO,
        Path(env).expanduser() if env else None,
        Path.home() / "CodeBuddy" / "一次函数" / "teachany-courseware",
    ]
    for c in candidates:
        if c and (c / "data" / "trees").is_dir():
            return c.resolve()
    return None


def load_all_nodes(repo: Path) -> dict:
    result = {}
    for f in (repo / "data" / "trees").rglob("*.json"):
        try:
            t = json.load(open(f, encoding="utf-8"))
            if not isinstance(t, dict) or "domains" not in t:
                continue
            sub = t.get("subject", "") or f.stem
            stg = t.get("stage", "")
            if not stg:
                for p in f.parts:
                    if p in ("elementary", "middle", "high"):
                        stg = p
                        break
            for d in t.get("domains", []):
                for n in d.get("nodes", []):
                    nid = n.get("id")
                    if nid:
                        result[nid] = (sub, stg, n.get("name", ""), f)
        except Exception:
            pass
    return result


def suggest_similar(target, all_ids, limit=5):
    import difflib
    return difflib.get_close_matches(target, all_ids, n=limit, cutoff=0.3)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("course_dir", nargs="?", help="课件目录")
    ap.add_argument("--node-id", help="直接校验某 node id")
    ap.add_argument("--list-subject", help="列某学科所有节点")
    ap.add_argument("--stage", help="限定学段")
    args = ap.parse_args()

    repo = find_repo()
    if not repo:
        print("❌ 未找到含 data/trees 的 courseware 仓库", file=sys.stderr)
        sys.exit(2)
    all_nodes = load_all_nodes(repo)

    if args.list_subject:
        hits = [
            (nid, info)
            for nid, info in all_nodes.items()
            if info[0] == args.list_subject and (not args.stage or info[1] == args.stage)
        ]
        print(f"📚 {args.list_subject} ({args.stage or 'all stages'}) · {len(hits)} 节点")
        for nid, (_s, _g, name, _f) in sorted(hits):
            print(f"  {nid:40s} {name}")
        return

    if args.node_id:
        nid = args.node_id
    elif args.course_dir:
        m_path = Path(args.course_dir) / "manifest.json"
        if not m_path.exists():
            h_path = Path(args.course_dir) / "index.html"
            if not h_path.exists():
                print("❌ 既无 manifest.json 也无 index.html", file=sys.stderr)
                sys.exit(2)
            html = h_path.read_text(encoding="utf-8")
            m = re.search(r'<meta[^>]*name="teachany-node"[^>]*content="([^"]+)"', html)
            if not m:
                print("❌ index.html 里没 teachany-node meta 标签", file=sys.stderr)
                sys.exit(2)
            nid = m.group(1)
        else:
            m = json.load(open(m_path, encoding="utf-8"))
            nid = m.get("node_id", "")
            if not nid:
                print("❌ manifest.json 里 node_id 为空", file=sys.stderr)
                sys.exit(2)
    else:
        ap.print_help()
        sys.exit(2)

    if EXT_NODE_RE.match(nid):
        print(f"✅ node_id '{nid}' 为 PBL 外部知识点（ext-*）")
        print("   → 发布后将挂入 data/trees/other/user-generated.json（Gallery「其他知识」）")
        print("   → 勿 hang_tree register 到课标树；manifest 与 teachany-node 须一致")
        sys.exit(0)

    if nid in all_nodes:
        sub, stg, name, tree_file = all_nodes[nid]
        print(f"✅ node_id '{nid}' 已存在")
        print(f"   学科: {sub} · 学段: {stg}")
        print(f"   节点名: {name}")
        print(f"   所在树: {tree_file.relative_to(repo)}")
        print("   → 课件可直接提交，rebuild-index 会自动挂树")
        sys.exit(0)

    print(f"❌ node_id '{nid}' 不在任何知识树里")
    suggestions = suggest_similar(nid, list(all_nodes.keys()))
    if suggestions:
        print("\n🔍 相似的已有节点：")
        for s in suggestions:
            info = all_nodes[s]
            print(f"   {s:40s} [{info[0]}/{info[1]}] {info[2]}")
    print("\n🆕 课标内新节点：python3 hang_tree.py register --node-id ...")
    print("   PBL 课标外：保持 ext-{hash}，直接 publish（勿 register 课标树）")
    sys.exit(1)


if __name__ == "__main__":
    main()
