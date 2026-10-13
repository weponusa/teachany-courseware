#!/usr/bin/env python3
"""add-modules-refine2.py — 为其余 4 个试点课件补写缺失模块（人工撰写）

沿用 add-modules-refine1.py 的写法与插入逻辑，内容同样逐条撰写。
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

DATA = {
    "chn-h-argumentative-essay": [
        ("worked-example", "范例：用「是什么—为什么—怎么办」搭建论证框架", [
            ("情境",
             "以“佛系青年”为题写一篇议论文，常见写法是罗列现象再发一通感慨，"
             "读起来像随笔而不像议论。"),
            ("分析",
             "换成三层推进：界定概念（佛系并非消极躺平，而是对结果低期待、"
             "对过程随意）→ 分析成因（竞争加剧、上升通道收窄，使部分青年以"
             "“无所谓”自我防御）→ 提出对策（个人重建目标感，社会提供更公平"
             "的机会与心理支持）。"),
            ("要点",
             "每一层都回扣中心论点，且层与层之间构成“是什么—为什么—怎么办”的"
             "递进；只罗列现象而缺少因果分析，论证就立不住。"),
        ]),
        ("summary", "小结：写议论文的三条底线", [
            ("一、论点要明确",
             "论点应是一个完整的陈述句，表明你的判断，不能只是话题或疑问。"),
            ("二、论据要能证明论点",
             "事例、数据、名言都要与论点一致，并能说清“为什么能证明”；"
             "只堆砌材料而不分析，等于没有论证。"),
            ("三、论证要有层次",
             "按“是什么—为什么—怎么办”或“现象—原因—对策”推进，"
             "避免平行罗列、原地打转。"),
        ]),
    ],
    "chn-h-advanced-composition": [
        ("worked-example", "范例：让议论落到“为什么”上", [
            ("情境",
             "写“限制未成年人网游”的议论文，若只写“网游有害、应当限制”，"
             "停留在表态，说服力很弱。"),
            ("分析",
             "补上因果链条：未成年人前额叶尚未发育成熟，自我控制能力弱"
             "（原因一）；游戏设计利用即时反馈与随机奖励，延长使用时长"
             "（原因二）；由此导致睡眠不足、学业受影响（结果）。"
             "把“为什么”说透，对策才站得住。"),
            ("要点",
             "议论的力量来自因果分析，而非态度强硬。每段都问自己一句"
             "“为什么会这样”，论证自然就深了。"),
        ]),
        ("summary", "小结：一篇好的议论文长什么样", [
            ("中心论点",
             "一句话说清你的判断，全文围绕它展开，不中途换话题。"),
            ("分论点",
             "两到三个，彼此不重叠，分别从“是什么/为什么/怎么办”的不同"
             "侧面支撑中心论点。"),
            ("论据与分析",
             "每个分论点配具体事例或数据，并说明它如何证明该分论点；"
             "忌只堆材料不分析。"),
            ("语言",
             "准确、简洁，避免空泛的抒情与口号式表达。"),
        ]),
    ],
    "bio-h-cell-metabolism": [
        ("deep-understanding", "深层理解：酶的高效、专一与需要温和条件", [
            ("高效性",
             "酶的催化效率约为无机催化剂的 10⁷ 倍，因此细胞内的化学反应才能"
             "在常温常压下快速进行。"),
            ("专一性",
             "一种酶通常只催化一种或一类反应，如淀粉酶只能水解淀粉，"
             "不能水解蛋白质——这保证了细胞代谢有条不紊。"),
            ("需要温和条件",
             "酶的作用需要适宜的温度和 pH。温度过高、过酸或过碱都会破坏酶的"
             "空间结构，使其变性失活，且往往不可逆。"),
            ("联系",
             "正因为酶需要温和条件，生物体才必须维持内环境稳态；一旦稳态被打破"
             "（如持续高烧），代谢就会紊乱。"),
        ]),
        ("worked-example", "范例：为什么发烧时会没胃口", [
            ("情境",
             "人发烧到 39 ℃ 时常感到食欲不振，退烧后胃口又逐渐恢复。"),
            ("分析",
             "人体消化酶的最适温度约为 37 ℃。体温升高超过最适温度后，"
             "酶的空间结构部分被破坏、活性下降，消化效率随之降低。"),
            ("结论",
             "体温回落后酶活性恢复，消化功能也跟着恢复。这说明酶的催化依赖"
             "温和条件，高温会导致酶变性失活。"),
        ]),
    ],
    "bio-biosphere-scope": [
        ("lesson-method", "方法：按「成分—作用—联系」分析生态系统", [
            ("第一步：分清成分",
             "先列出非生物成分（阳光、空气、水、土壤等）与生物成分"
             "（生产者、消费者、分解者），不遗漏、不重复。"),
            ("第二步：明确作用",
             "生产者制造有机物，是生态系统的基石；消费者促进物质循环与"
             "能量流动；分解者把有机物分解为无机物，归还无机环境。"),
            ("第三步：找联系",
             "沿着“生产者→消费者→分解者”梳理食物链和食物网，再看物质如何"
             "循环、能量如何单向流动。"),
            ("常见误区",
             "认为分解者可有可无。若没有分解者，动植物遗体就会堆积，"
             "物质无法循环，生态系统终将崩溃。"),
        ]),
        ("worked-example", "范例：一片森林里的生态系统组成", [
            ("情境",
             "以一片温带落叶阔叶林为例，看一个完整生态系统包含哪些部分。"),
            ("分析",
             "非生物成分：阳光、空气、水、土壤、温度；"
             "生产者：乔木、灌木、草本植物，通过光合作用把无机物合成有机物；"
             "消费者：昆虫、鸟、松鼠等；分解者：腐生细菌和真菌，"
             "把遗体分解为无机物归还环境。"),
            ("结论",
             "四类成分缺一不可：生产者提供能量与有机物基础，分解者完成"
             "物质循环，二者共同维系生态系统的稳定。"),
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
        elif head in ("常见误区", "要点", "结论"):
            cls = "bioh-pitfall" if head == "常见误区" else ""
            parts.append(f'<p class="{cls}"><strong>{escape(head)}：</strong>{escape(body)}</p>')
        else:
            parts.append(f'<p><strong>{escape(head)}：</strong>{escape(body)}</p>')
    parts += ["</div></section>\n"]
    return "".join(parts)


def insert(html, sid, frag):
    after = {
        "lesson-method": ["lesson-focus", "core-concept", "learn"],
        "worked-example": ["lesson-method", "lesson-focus", "deep-understanding"],
        "deep-understanding": ["lesson-method", "lesson-focus"],
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
