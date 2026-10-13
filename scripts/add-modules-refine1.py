#!/usr/bin/env python3
"""add-modules-refine1.py — 为试点的 2 个课件补写缺失模块（人工撰写）

补的是 worked-example（范例）与 lesson-method（方法）——这两个模块
6 个试点课件全部缺失，是内容短板里最突出的。

内容由我逐条撰写：先读课件正文弄清它教什么、学生卡在哪，再下笔。
脚本只负责套进标准 HTML 结构并插入正确位置。
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# cid → [(模块id, 标题, [(小标题, 正文)] )]
DATA = {
    "bio-asexual-repro": [
        ("lesson-method", "方法：抓住「有无两性生殖细胞结合」这条判断标准", [
            ("判断标准",
             "判断一种繁殖方式是否属于无性生殖，只看一件事：有没有经过两性生殖细胞"
             "（精子与卵细胞）的结合形成受精卵。有 → 有性生殖；没有 → 无性生殖。"),
            ("再看繁殖器官",
             "确认为无性生殖后，再看由什么结构完成：用营养器官（根、茎、叶）繁殖的叫"
             "营养繁殖，如扦插（茎）、嫁接（茎）、压条（茎）、分株（根或茎）；"
             "依靠孢子繁殖的（如蕨类、蘑菇）不经结合，同样属于无性生殖。"),
            ("范例",
             "马铃薯用块茎繁殖、酵母菌出芽生殖，都没有两性细胞结合，属于无性生殖；"
             "而小麦用种子繁殖，要经过开花、传粉、受精，属于有性生殖。"),
            ("常见误区",
             "「出芽」和「发芽」不是一回事：酵母菌出芽是母体上长出芽体、脱落后成为"
             "新个体；土豆发芽是块茎上的芽萌发长成植株——两者都不经过结合，"
             "都属无性生殖；而种子萌发长成的植株是有性生殖的后代。"),
        ]),
        ("worked-example", "范例：扦插月季为什么能保持品种特性", [
            ("情境",
             "把月季的一段枝条插入湿润土壤，枝条基部会形成不定根，逐渐发育成一株"
             "完整的新月季，且花色、花型与母株几乎一致。"),
            ("分析",
             "关键在于新个体由母株的体细胞直接发育而来，没有经过两性生殖细胞的结合，"
             "遗传物质与母株相同，因此优良性状能稳定保持。"),
            ("对比",
             "若用种子繁殖，经过减数分裂和受精作用会发生基因重组，后代出现变异，"
             "母本的花色、花型未必能保持——这正是苹果、梨等果树普遍采用嫁接的原因。"),
        ]),
    ],
    "bio-cell-life": [
        ("lesson-method", "方法：判断物质跨膜运输方式的三步法", [
            ("第一步：看浓度方向",
             "顺浓度梯度（高浓度→低浓度）一般是被动运输；逆浓度梯度（低浓度→高浓度）"
             "一定是主动运输。"),
            ("第二步：看是否需要载体",
             "自由扩散不需要载体蛋白；协助扩散和主动运输都需要膜上的载体蛋白协助。"),
            ("第三步：看是否消耗 ATP",
             "只有主动运输需要消耗能量（ATP）；自由扩散和协助扩散都不消耗。"),
            ("范例",
             "O₂、CO₂ 等小分子直接穿过磷脂双分子层，属自由扩散；葡萄糖进入红细胞"
             "需要载体但不耗能，属协助扩散；小肠上皮细胞吸收葡萄糖、细胞积累无机盐"
             "离子常逆浓度进行，属主动运输。"),
            ("常见误区",
             "以为「细胞需要的物质都是主动运输」。实际上多数气体和小分子顺浓度进入"
             "细胞属于被动运输；主动运输只用于逆浓度运输或需要快速积累的情形。"),
        ]),
        ("worked-example", "范例：红细胞吸收葡萄糖为什么是协助扩散", [
            ("情境",
             "血液中的葡萄糖浓度通常高于红细胞内，葡萄糖不断进入红细胞供其利用。"),
            ("分析",
             "葡萄糖顺浓度梯度进入细胞，需要细胞膜上的载体蛋白协助，但整个过程"
             "不消耗 ATP——符合协助扩散的两个特征：需载体、不耗能。"),
            ("对比",
             "换成小肠绒毛上皮细胞吸收葡萄糖，肠腔中葡萄糖浓度往往低于细胞内，"
             "需要逆浓度运输并消耗 ATP，此时属于主动运输。可见判断依据不是"
             "「是不是葡萄糖」，而是浓度方向与是否耗能。"),
        ]),
    ],
}


def build(sid, title, blocks):
    parts = [f'\n<section class="section" id="{sid}" data-scaffold="full">',
             '<div class="card">',
             f'<h2 class="section-title">{escape(title)}</h2>']
    for head, body in blocks:
        if head == "范例":
            parts.append(f'<div class="worked-example"><strong>范例：</strong>{escape(body)}</div>')
        elif head == "常见误区":
            parts.append(f'<p class="bioh-pitfall"><strong>常见误区：</strong>{escape(body)}</p>')
        else:
            parts.append(f'<p><strong>{escape(head)}：</strong>{escape(body)}</p>')
    parts += ["</div></section>\n"]
    return "".join(parts)


def insert(html, sid, frag):
    """插到合适的锚点之后"""
    after = {"lesson-method": ["lesson-focus", "core-concept", "learn"],
             "worked-example": ["lesson-method", "lesson-focus", "deep-understanding"]}
    for a in after.get(sid, []):
        m = re.search(rf'<section\b[^>]*\bid="{a}"[^>]*>', html)
        if m:
            end = html.find("</section>", m.end())
            if end > 0:
                return html[:end + 10] + frag + html[end + 10:]
    m = re.search(r"\s*</body>", html)
    if m:
        return html[:m.start()] + frag + html[m.start():]
    return None


def main():
    dry = "--dry" in sys.argv
    n = 0
    for cid, mods in DATA.items():
        P = COMMUNITY / cid / "index.html"
        html = P.read_text(encoding="utf-8", errors="replace")
        for sid, title, blocks in mods:
            if re.search(rf'<section\b[^>]*\bid="{sid}"', html):
                print(f"  跳过（已有）{cid}/{sid}")
                continue
            new = insert(html, sid, build(sid, title, blocks))
            if new is None:
                print(f"  ⚠ 无插入点 {cid}/{sid}")
                continue
            html = new
            n += 1
        if not dry:
            P.write_text(html, encoding="utf-8")
    print(f"补写 {n} 个模块" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
