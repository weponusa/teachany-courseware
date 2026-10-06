#!/usr/bin/env python3
"""scan-onclick-undefined.py — 扫描 onclick 引用但未定义的函数
判定：HTML 中 onclick="fn(...)" 引用的 fn，在内联 script 和加载的本地 js 中均无定义
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# 标准库已知的全局函数（抽查 assets/scripts 里定义的）
STDLIB = ROOT / "assets" / "scripts"
stdlib_src = ""
for js in STDLIB.glob("*.js"):
    stdlib_src += js.read_text(encoding="utf-8", errors="replace")


def defined_functions(src):
    names = set()
    for m in re.finditer(r"function\s+([A-Za-z_$][\w$]*)\s*\(", src):
        names.add(m.group(1))
    for m in re.finditer(r"(?:window\.|var\s+|let\s+|const\s+)([A-Za-z_$][\w$]*)\s*=\s*(?:function|\()", src):
        names.add(m.group(1))
    return names


STDLIB_FUNCS = defined_functions(stdlib_src)


def main():
    results = []
    fn_counter = Counter()
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        html = f.read_text(encoding="utf-8", errors="replace")
        onclick_fns = set(re.findall(r'onclick="([A-Za-z_$][\w$]*)\s*\(', html))
        if not onclick_fns:
            continue
        scripts = "\n".join(re.findall(r"<script\b[^>]*>([\s\S]*?)</script>", html))
        local_funcs = defined_functions(scripts) | STDLIB_FUNCS
        missing = sorted(onclick_fns - local_funcs)
        if missing:
            results.append({"id": cid, "missing": missing})
            for fn in missing:
                fn_counter[fn] += 1
    print(f"{len(results)} 个课件存在 onclick 未定义函数")
    for fn, n in fn_counter.most_common(20):
        print(f"  {fn}: {n} 个课件")
    out = ROOT / "scripts" / "onclick-undefined-scan.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"明细 → {out}")


if __name__ == "__main__":
    main()
