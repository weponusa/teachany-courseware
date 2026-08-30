#!/usr/bin/env python3
"""add-modules-bio2.py — 生物第 2 批：补写 worked-example 与 summary（人工撰写）

每课写两块：
  - worked-example 范例：用真实情境把核心知识讲透，含「情境—分析—结论」
  - summary 小结：按条目梳理本课要点，便于复习回顾

内容逐条撰写，脚本只负责套进标准 HTML 并插入正确位置。
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

DATA = {
    "bio-biosphere-largest": [
        ("worked-example", "范例：一条河里的污染物为什么会影响到海洋", [
            ("情境",
             "某河流上游工厂排放含重金属的废水，河水最终流入海洋，"
             "后来人们在海洋鱼类体内也检出了重金属。"),
            ("分析",
             "河流、湖泊、海洋等水域生态系统通过水流彼此连通，物质会随水循环和"
             "食物链迁移。污染物先被浮游生物吸收，再经小鱼、大鱼逐级富集，"
             "最终在海洋生物体内累积。"),
            ("结论",
             "各类生态系统并非彼此孤立，而是通过物质循环、能量流动和食物链"
             "相互联系。正是这种普遍联系，使地球上所有生态系统共同构成最大的"
             "生态系统——生物圈。"),
        ]),
        ("summary", "小结：生物圈的范围与地位", [
            ("范围",
             "大气圈的底部、水圈的大部、岩石圈的表面，"
             "大致是海平面上下各约 10 千米的薄层。"),
            ("组成",
             "包含地球上所有生态系统：森林、草原、海洋、淡水、"
             "湿地、农田、城市等。"),
            ("地位",
             "生物圈是地球上最大的生态系统，是全部生物与其生存环境"
             "构成的统一整体。"),
            ("保护",
             "生物圈是包括人类在内所有生物唯一的家园。污染、过度开发等"
             "人类活动会影响整个生物圈，需要全球协作加以保护。"),
        ]),
    ],
    "bio-cell-division": [
        ("worked-example", "范例：观察根尖细胞如何判断它处于哪个时期", [
            ("情境",
             "在显微镜下观察洋葱根尖分生区装片，不同细胞里的染色体"
             "呈现出不同状态。"),
            ("分析",
             "间期：细胞核完整，染色体呈细丝状的染色质，看不清个体；"
             "前期：染色体出现，核膜核仁消失，纺锤体形成；"
             "中期：染色体的着丝点排列在细胞中央的赤道板上，形态最清晰；"
             "后期：着丝点分裂，姐妹染色单体分开并移向两极；"
             "末期：染色体解螺旋，核膜核仁重现，缢裂成两个子细胞。"),
            ("结论",
             "判断分裂时期的关键是看染色体的位置和形态。其中中期染色体"
             "最清晰、数目最易数，是观察和计数的最佳时期。"),
        ]),
        ("summary", "小结：细胞分裂与细胞分化", [
            ("细胞分裂",
             "一个细胞分裂成两个，结果是细胞数目增多。有丝分裂是真核细胞"
             "分裂的主要方式，分前、中、后、末四个时期，保证亲子代细胞"
             "遗传物质一致。"),
            ("无丝分裂",
             "分裂过程中不出现纺锤丝和染色体的变化，过程较简单，"
             "如蛙的红细胞。"),
            ("细胞分化",
             "分裂产生的细胞在形态、结构和功能上发生稳定性差异，"
             "形成不同的组织。分化使细胞种类增多。"),
            ("意义",
             "分裂增加数目、分化增加种类，两者共同推动生物体的"
             "生长、发育和繁殖。"),
        ]),
    ],
    "bio-cell-structure": [
        ("worked-example", "范例：为什么植物能进行光合作用而动物不能", [
            ("情境",
             "绿色植物在光下能把二氧化碳和水合成有机物，"
             "动物却必须摄取现成的有机物。"),
            ("分析",
             "植物绿色部位的细胞里含有叶绿体，其中的叶绿素能吸收光能，"
             "把无机物合成有机物；动物细胞没有叶绿体，也就无法进行光合作用。"),
            ("补充",
             "植物细胞还有细胞壁（支持、保护，使植物挺立）和大的液泡"
             "（含细胞液，储存糖分、色素等），这是动物细胞没有的。"),
            ("结论",
             "结构与功能相适应：细胞具有什么结构，就决定它能完成什么功能。"
             "动植物细胞结构上的差异，正是二者营养方式不同的根本原因。"),
        ]),
        ("summary", "小结：动植物细胞的结构比较", [
            ("共同结构",
             "细胞膜（控制物质进出）、细胞质（生命活动的主要场所）、"
             "细胞核（含遗传物质，是控制中心）、线粒体（呼吸作用场所，供能）。"),
            ("植物特有",
             "细胞壁（支持、保护）、叶绿体（光合作用场所，只在绿色部分有）、"
             "大而明显的液泡（含细胞液，储存糖分、色素等）。"),
            ("动物特有",
             "中心体（与细胞分裂有关，低等植物细胞中也有）。"),
            ("观察要点",
             "制作临时装片时，植物材料滴清水、动物材料滴生理盐水以维持形态；"
             "用碘液染色可以看清细胞核。"),
        ]),
    ],
    "bio-characteristics": [
        ("worked-example", "范例：机器人和珊瑚，哪个是生物？", [
            ("情境",
             "机器人能行走、发声、回答提问；珊瑚礁会不断长大，还会分枝。"
             "它们算不算生物？"),
            ("分析",
             "机器人：不能进行新陈代谢（不需要营养、不呼吸、不排泄），"
             "不能繁殖后代，所谓的「反应」只是程序响应，不是应激性——不是生物。"
             "珊瑚：珊瑚虫本身是生物，能摄食、呼吸、繁殖；而我们看到的"
             "珊瑚「骨骼」是珊瑚虫分泌的石灰质堆积物，本身已无生命活动。"),
            ("结论",
             "判断生物不能只看「会不会动」或「会不会长大」，"
             "而要看是否同时具备生物的七大基本特征，"
             "其中新陈代谢是最根本的标志。"),
        ]),
        ("summary", "小结：判断生物的七条标准", [
            ("一",
             "生物的生活需要营养（自养如光合作用，异养如摄食）。"),
            ("二",
             "生物能进行呼吸（绝大多数吸入氧气、呼出二氧化碳）。"),
            ("三",
             "生物能排出体内产生的废物（排汗、排尿、呼气等）。"),
            ("四",
             "生物能对外界刺激作出反应，即应激性（如含羞草叶片合拢）。"),
            ("五",
             "生物能生长和繁殖，由小长大并产生后代。"),
            ("六",
             "生物都有遗传和变异的特性：种瓜得瓜，但后代又各不相同。"),
            ("七",
             "除病毒外，生物都由细胞构成——细胞是生命活动的基本单位。"),
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
        elif head in ("补充", "结论"):
            parts.append(f'<p><strong>{escape(head)}：</strong>{escape(body)}</p>')
        else:
            parts.append(f'<p><strong>{escape(head)}：</strong>{escape(body)}</p>')
    parts += ["</div></section>\n"]
    return "".join(parts)


def insert(html, sid, frag):
    after = {
        "worked-example": ["lesson-method", "lesson-focus", "deep-understanding"],
        "summary": ["posttest", "knowledge-graph"],
    }
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
