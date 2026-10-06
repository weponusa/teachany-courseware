#!/usr/bin/env python3
"""normalize-module-ids.py — 模块 id 归一（语义等价者才改）

背景：不同批次课件生成时用了不同 id 命名，导致工具链（插图落位、模块体检）
无法统一识别。但**并非所有「替代 id」都等价于标准模块**：

  可归一（语义确实相同）：
    learn / core-concept / concept  → lesson-focus   （都是「核心知识讲解」）
    pre-test / warmup               → pretest        （都是「课前诊断/热身」）
    knowledge                       → knowledge-graph（就是知识图谱）

  不可归一（语义不同，强改会造成错误）：
    module-1/2/3  是「并列知识点块」（PBL 三段式），不是 精讲/方法/理解；
                  例：module-1=细胞膜的结构 / module-2=被动运输 / module-3=主动运输
    intro         是「背景导入」环节，不等于知识精讲

策略：
  1. 课件已有标准 id 时不改动（避免重复）
  2. 缺标准 id 时，把语义等价的替代 id 重命名过去
  3. 同步更新该 id 的全部引用：锚点 #id、getElementById("id")、querySelector("#id")
  4. 只在能安全同步引用时才改，否则跳过

用法: python3 normalize-module-ids.py [--dry]
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# 标准 id ← 语义等价的替代 id（按优先级）
MAP = {
    "lesson-focus": ["core-concept", "learn", "concept"],
    "pretest": ["pre-test", "warmup"],
    "knowledge-graph": ["knowledge"],
}
# 明确不动（语义不同，仅作记录，防止后人误加进 MAP）
KEEP = ["module-1", "module-2", "module-3", "intro", "method", "deep"]


def ref_pattern(old):
    """匹配 id 的各种引用形式"""
    o = re.escape(old)
    return re.compile(
        rf'(id\s*=\s*["\']){o}(["\'])'          # id="old"
        rf'|(#){o}\b'                            # #old（锚点 / querySelector）
        rf'|(getElementById\(\s*["\']){o}(["\']\s*\))'
        rf'|(getElementById\(\s*["\'])#{o}(["\']\s*\))'
    )


def replace_refs(html, old, new):
    """把所有对 old 的引用换成 new，返回 (新html, 替换数)"""
    pat = ref_pattern(old)
    n = 0

    def sub(m):
        nonlocal n
        n += 1
        g = m.groups()
        if g[0]:                       # id="old"
            return f'{g[0]}{new}{g[1]}'
        if g[2]:                       # #old
            return f'#{new}'
        if g[3]:                       # getElementById("old")
            return f'{g[3]}{new}{g[4]}'
        if g[5]:                       # getElementById("#old")
            return f'{g[5]}#{new}{g[6]}'
        return m.group(0)

    return pat.sub(sub, html), n


def process(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    ids = re.findall(r'<section\b[^>]*\bid="([^"]+)"', html)
    idset = set(ids)

    changed, detail = 0, []
    for std, alts in MAP.items():
        if std in idset:
            continue                                   # 已有标准模块
        old = next((a for a in alts if a in idset), None)
        if not old:
            continue
        new_html, n = replace_refs(html, old, std)
        if n == 0:
            continue
        # 校验：替换后 old 不应再作为 id 或锚点出现
        leftover = len(re.findall(rf'\bid\s*=\s*"{re.escape(old)}"', new_html))
        if leftover:
            detail.append(f"{old}→{std} 仍有{leftover}处残留，跳过")
            continue
        html = new_html
        idset = set(re.findall(r'<section\b[^>]*\bid="([^"]+)"', html))
        changed += 1
        detail.append(f"{old} → {std}（同步 {n} 处引用）")

    if changed and not dry:
        P.write_text(html, encoding="utf-8")
    return changed, detail


def main():
    dry = "--dry" in sys.argv
    cids = sorted(p.name for p in COMMUNITY.iterdir() if (p / "index.html").exists())
    tot, files = 0, []
    for c in cids:
        try:
            n, d = process(c, dry)
            if n:
                tot += n
                files.append((c, d))
        except Exception as e:
            print(f"  ❌ {c}: {str(e)[:50]}")
    print(f"归一 {len(files)} 个课件，共 {tot} 个模块 id" + ("（--dry 未写入）" if dry else ""))
    for c, d in files[:10]:
        print(f"  {c:<34} {'; '.join(d)}")
    if len(files) > 10:
        print(f"  ... 另 {len(files)-10} 个")


if __name__ == "__main__":
    main()
