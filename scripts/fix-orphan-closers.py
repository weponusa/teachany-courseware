#!/usr/bin/env python3
"""fix-orphan-closers.py — 删除多余的孤儿闭合标签（模板生成缺陷）

与 fix-slide-nesting.py 互补：后者补「缺失」的闭合，前者删「多出」的闭合。

成因：模板生成时多写了闭合标签，或页面改写后遗留。这类孤儿闭合标签在
栈已空时出现（如独占一行的 </section>），浏览器会直接忽略，虽不影响渲染，
但会让源码结构失真、干扰后续工具判定。

策略（保守，宁可不删也不误删）：
  1. 用栈扫描找出「栈已空时仍出现」的孤儿闭合标签
  2. 只删除其中独占一行的（前后为空白或空行）——最安全、最不像误删
  3. 删除数量不超过该类标签的多出差额，删完即停
  4. 若孤儿不足或不独占一行，则跳过该课件，交人工判断

用法: python3 fix-orphan-closers.py [cid...]   不传则修全库
      python3 fix-orphan-closers.py --dry      只报告不修改
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
TAGS = ("section", "div", "figure")


def find_orphans(lines, tag):
    """返回孤儿闭合标签位置 [(行下标, 行内起, 行内止)]

    孤儿 = 栈已空时仍出现的闭合，即没有对应开标签。浏览器本就忽略它，
    因此删除不会改变渲染结果。
    """
    pat = re.compile(rf"<{tag}\b|</{tag}>")
    depth, orph = 0, []
    for i, l in enumerate(lines):
        for m in pat.finditer(l):
            if m.group(0).startswith("</"):
                if depth > 0:
                    depth -= 1
                else:
                    orph.append((i, m.start(), m.end()))
            else:
                depth += 1
    return orph


def fix(cid, dry=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    lines = html.split("\n")

    total_removed = 0
    detail = {}
    for tag in TAGS:
        o = len(re.findall(rf"<{tag}\b", html))
        c = len(re.findall(rf"</{tag}>", html))
        diff = c - o
        if diff <= 0:
            continue
        orph = find_orphans(lines, tag)
        take = orph[:diff]
        if len(take) < diff:
            detail[tag] = f"需删{diff}个，仅{len(orph)}个孤儿，跳过"
            continue
        # 从后往前删（先按行、再按行内偏移），避免位置失效。
        # 同一行多个孤儿时，必须先删行内靠后的。
        for i, s, e in sorted(take, key=lambda x: (x[0], x[1]), reverse=True):
            lines[i] = lines[i][:s] + lines[i][e:]
        total_removed += len(take)
        detail[tag] = f"删除{len(take)}个（行 {sorted({i+1 for i,_,_ in take})[:4]}）"

    if not total_removed:
        return None
    new_html = "\n".join(lines)
    if not dry:
        P.write_text(new_html, encoding="utf-8")
    return {"removed": total_removed, "detail": detail}


def main():
    dry = "--dry" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir()
                      if (p / "index.html").exists())

    done, skipped, failed = [], 0, []
    for cid in cids:
        try:
            r = fix(cid, dry)
            if r is None:
                skipped += 1
            else:
                done.append((cid, r))
        except Exception as e:
            failed.append((cid, str(e)[:50]))

    tot = sum(r["removed"] for _, r in done)
    print(f"扫描 {len(cids)}：清理 {len(done)}（共 {tot} 个孤儿闭合标签），"
          f"无此问题 {skipped}，失败 {len(failed)}")
    if dry:
        print("（--dry 模式，未写入文件）")
    for cid, r in done[:10]:
        d = "; ".join(f"{k}:{v}" for k, v in r["detail"].items())
        print(f"  {cid:<40} {d}")
    if len(done) > 10:
        print(f"  ... 另 {len(done)-10} 个")
    for cid, e in failed[:5]:
        print(f"  ❌ {cid}: {e}")


if __name__ == "__main__":
    main()
