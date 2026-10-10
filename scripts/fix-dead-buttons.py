#!/usr/bin/env python3
"""fix-dead-buttons.py — 修复「onclick 引用未定义函数」的死按钮（通用层）。

盘点（2026-10-10）：277 门课件 4325 个死按钮引用点。其中 76% 是跨课件通用的
判分/导航/选择题行为（checkAnswer / answerQ / answerPre / answerPost /
answerQuiz / goTo / showTab / selectOpt / 各学科 *DepthCheck），由共享库
assets/scripts/ta-interactions.js 统一实现——本脚本按每门课的实际缺失清单
注入引用与别名。剩余 ~1000 个课程特化交互（动画/画图/拖拽/流程）不在本层，
清单写到 /tmp/onclick-special.json 留待逐课实现。

用法：
  python3 scripts/fix-dead-buttons.py --ids a,b --apply
  python3 scripts/fix-dead-buttons.py --from-file f.txt --apply
  python3 scripts/fix-dead-buttons.py --all --apply
  python3 scripts/fix-dead-buttons.py --all --revert
幂等：已引用 ta-interactions.js 的课件跳过；--revert 按标记移除注入。
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
INVENTORY = Path("/tmp/onclick-missing.json")

SCRIPT_TAG = '<script src="../../assets/scripts/ta-interactions.js"></script>'
MARK = "ta-interactions.js"

GENERIC = {"checkAnswer", "answerTF", "answerQ", "answerPre", "answerPost",
           "answerQuiz", "goTo", "showTab", "selectOpt"}


def is_generic(fn: str) -> bool:
    return fn in GENERIC or fn.endswith("DepthCheck")


def load_targets(a):
    if a.ids:
        ids = [x.strip() for x in a.ids.split(",") if x.strip()]
    elif a.from_file:
        ids = [l.strip() for l in Path(a.from_file).read_text().splitlines()
               if l.strip() and not l.startswith("#")]
    else:
        ids = None
    inv = {r["id"]: r for r in json.loads(INVENTORY.read_text(encoding="utf-8"))}
    if ids is not None:
        dirs = [(COMMUNITY / i, inv.get(i)) for i in ids]
    else:
        dirs = [(COMMUNITY / i, inv.get(i)) for i in sorted(inv)]
    return [(p, r) for p, r in dirs if p.is_dir() and r]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ids")
    ap.add_argument("--from-file")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    a = ap.parse_args()
    if not any([a.ids, a.from_file, a.all]):
        ap.error("需指定 --ids / --from-file / --all 之一")

    targets = load_targets(a)
    mode = "回滚" if a.revert else ("写入" if a.apply else "预览")
    print(f"目标 {len(targets)} 门 · {mode}", flush=True)

    fixed_btns = special = {}
    special = {}
    ok_cnt = 0
    for p, rec in targets:
        f = p / "index.html"
        h = f.read_text(encoding="utf-8", errors="ignore")

        if a.revert:
            if MARK not in h:
                continue
            new = h.replace('\n<script src="../../assets/scripts/ta-interactions.js"></script>', "")
            new = re.sub(r'\n?<script>/\* ta-depth-alias \*/[\s\S]*?</script>', "", new)
            if new != h and a.apply:
                f.write_text(new, encoding="utf-8")
                ok_cnt += 1
            continue

        if MARK in h:
            continue                      # 幂等

        depth_names = [x["fn"] for x in rec["missing"] if x["fn"].endswith("DepthCheck")]
        gen_names = [x["fn"] for x in rec["missing"] if x["fn"] in GENERIC]
        if not depth_names and not gen_names:
            special[p.name] = [x["fn"] for x in rec["missing"]]
            continue

        block = "\n" + SCRIPT_TAG
        if depth_names:
            names = json.dumps(depth_names, ensure_ascii=False)
            block += (
                "\n<script>/* ta-depth-alias: 由 fix-dead-buttons.py 注入，"
                "把本课缺失的学科检查函数挂到共享实现 */\n"
                "window.__taRegisterDepthCheck(" + names + ");\n</script>"
            )
        if a.apply:
            i = h.rfind("</body>")
            h = h[:i] + block + h[i:] if i >= 0 else h + block
            f.write_text(h, encoding="utf-8")
            ok_cnt += 1
        fixed_btns[p.name] = len(gen_names) + len(depth_names)

    if a.revert:
        print(f"\n完成：回滚 {ok_cnt} 门")
        return
    print(f"\n完成：注入 {ok_cnt} 门，覆盖函数引用 {sum(fixed_btns.values())} 处")
    if special:
        n_pts = sum(len(v) for v in special.values())
        Path("/tmp/onclick-special.json").write_text(
            json.dumps(special, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"课程特化（本层不处理）{len(special)} 门 {n_pts} 个函数 -> /tmp/onclick-special.json")


if __name__ == "__main__":
    main()
