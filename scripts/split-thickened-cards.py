#!/usr/bin/env python3
"""split-thickened-cards.py — 把加厚后的 lesson-focus 单卡拆成多卡（符合 #09 单卡≤200字）
原：card(span+h2+引入p+四段p)
新：card(span+h2+引入p) + card(概念本质) + card(结构过程) + card(实例证据) + card(易错提醒)
幂等：<!-- cards-split --> 标记
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARK = "<!-- cards-split -->"
SEG_KEYS = ["概念本质", "结构与过程", "实例与证据", "易错提醒"]


def split_card(sec):
    # 提取四段
    segs = []
    for key in SEG_KEYS:
        m = re.search(r"<p><strong>" + key + r"：</strong>[\s\S]*?</p>", sec)
        if not m:
            return None, 0
        segs.append(m.group(0))
    # 删除四段后，在原 card 闭合 </div> 处插入新卡
    new_sec = sec
    for s in segs:
        new_sec = new_sec.replace(s, "", 1)
    cards = "".join(f'<div class="card focus-detail">{s}</div>\n' for s in segs)
    # 插到 lesson-focus 的 card </div> 后（</section> 前）
    m = re.search(r"(</div>\s*)(</section>\s*<!-- focus-thickened -->|</section>)", new_sec)
    if not m:
        return None, 0
    new_sec = new_sec[:m.start(1)] + m.group(1) + cards + new_sec[m.start(2):]
    return new_sec, len(segs)


def main():
    src = (ROOT / "scripts/replace-fake-canvas.py").read_text(encoding="utf-8")
    ids = sorted(set(re.findall(r'^\s*"((?:bio|it)-h-[a-z0-9-]+)": dict\(', src, re.M)))
    ok, skip = 0, []
    for cid in ids:
        p = ROOT / "community" / cid / "index.html"
        html = p.read_text(encoding="utf-8")
        if MARK in html:
            continue
        m = re.search(r'<section class="section [^"]*" id="lesson-focus"[\s\S]*?</section>(?:\s*<!-- focus-thickened -->)?', html)
        if not m:
            skip.append((cid, "无lesson-focus"))
            continue
        sec = m.group(0)
        new_sec, n = split_card(sec)
        if not new_sec:
            skip.append((cid, "四段不全"))
            continue
        html = html.replace(sec, new_sec, 1)
        html = html.replace("</body>", MARK + "\n</body>", 1)
        p.write_text(html, encoding="utf-8")
        ok += 1
    print(f"拆卡 {ok} 个课件；跳过 {len(skip)}: {skip[:5]}")


if __name__ == "__main__":
    main()
