#!/usr/bin/env python3
"""inject-quiz-binding.py — 给 quiz 交互缺失的课件注入 teachany-quiz-binding.js
名单 = quiz-binding-scan.json(无绑定) ∪ onclick-undefined-scan.json(未定义函数)
幂等：已含 teachany-quiz-binding.js 引用则跳过
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
TAG = '<script src="../../assets/scripts/teachany-quiz-binding.js" defer></script>'


def main():
    affected = set()
    for name in ("quiz-binding-scan.json", "onclick-undefined-scan.json"):
        for r in json.load(open(ROOT / "scripts" / name, encoding="utf-8")):
            affected.add(r["id"])
    done, skipped, missing = 0, 0, []
    for cid in sorted(affected):
        p = COMMUNITY / cid / "index.html"
        if not p.exists():
            missing.append(cid)
            continue
        html = p.read_text(encoding="utf-8", errors="replace")
        if "teachany-quiz-binding.js" in html:
            skipped += 1
            continue
        if "</body>" not in html:
            missing.append(cid + "(无</body>)")
            continue
        html = html.replace("</body>", TAG + "\n</body>", 1)
        p.write_text(html, encoding="utf-8")
        done += 1
    print(f"受影响课件 {len(affected)}：注入 {done}，已注入 {skipped}，异常 {len(missing)}")
    for m in missing:
        print("  ⚠️", m)


if __name__ == "__main__":
    main()
