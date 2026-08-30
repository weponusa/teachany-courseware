#!/usr/bin/env python3
"""apply-pretest-b6.py — 写入第 6 批（高中地理）课前诊断题（人工撰写，非模板生成）

本文件内容由我（模型）逐题撰写：先读课件正文弄清它真正教什么、学生
容易错在哪，再出题。脚本只负责搬运成 HTML。

与 add-missing-modules.py 的 pretest_block 区别：那个用「{知识点}与{主题}
完全无关」之类空壳拼选项，知识点一错整句就荒谬；这里每题的题干、三个
选项、错因诊断都是针对该课真实误区写的。

正确项在 A/B/C 间轮换，避免学生按位置猜答案。
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# cid → (题干, [(选项文本, 是否正确)], 错因诊断)
DATA = {
    "geo-h-agriculture": (
        "分析一个地区农业生产的特点，最合理的思路是？",
        [("只看当地的气候条件", False), ("主要看当地的种植历史", False),
         ("综合自然条件和社会经济条件一起分析", True)],
        "农业区位要同时考虑自然因素（气候、地形、土壤、水源）和社会经济因素"
        "（市场、交通、劳动力、技术、政策）。只看气候会漏掉市场、交通这些"
        "决定性因素，种植历史只是影响因素之一。",
    ),
    "geo-h-agriculture-location": (
        "下列因素中，属于农业区位的「社会经济因素」的是？",
        [("地形", False), ("土壤", False), ("市场", True)],
        "地形、土壤、气候、水源属于自然因素；市场、交通、劳动力、政策、技术"
        "属于社会经济因素。把两类因素分清，是区位分析的第一步。",
    ),
    "geo-h-agriculture-types": (
        "季风水田农业的典型特点是？",
        [("小农经营，单产高，商品率低", True),
         ("生产规模大，机械化水平高", False),
         ("以养牛为主，产品主要面向市场", False)],
        "季风水田农业以家庭为单位经营，精耕细作使单产较高，但人多地少、自给比"
        "重大，商品率低。规模大、机械化高是商品谷物农业的特点，以养牛为主是"
        "大牧场放牧业。",
    ),
    "geo-h-atmosphere": (
        "对流层大气主要的直接热源是？",
        [("地面辐射", True), ("太阳辐射", False), ("大气逆辐射", False)],
        "对流层大气对太阳短波辐射吸收很少，主要吸收地面长波辐射而增温，因此"
        "地面是它的直接热源。太阳辐射是根本能量来源，但要经过地面转换才能"
        "有效加热大气。",
    ),
    "geo-h-atmospheric-circulation": (
        "三圈环流中，副热带高气压带的成因主要是？",
        [("热力原因：受热膨胀上升", False), ("动力原因：高空空气堆积下沉", True),
         ("海陆热力性质差异", False)],
        "副热带高压是赤道上升的气流在高空向两极流动、受地转偏向力作用堆积下沉"
        "形成的，属于动力原因。赤道低压才是受热上升的热力原因形成；海陆热力"
        "差异形成的是季风。",
    ),
    "geo-h-atmospheric-heating": (
        "晴朗的夜晚更容易出现霜冻，主要原因是？",
        [("太阳辐射弱", False), ("地面辐射强", False),
         ("云少，大气逆辐射弱，保温作用差", True)],
        "晴朗少云的夜晚，大气逆辐射弱，地面热量散失快，气温下降明显，容易形成"
        "霜冻。多云的夜晚大气逆辐射强、保温好，反而不易出现霜冻。",
    ),
    "geo-h-climate-change": (
        "近百年来全球气温上升，一般认为的主要原因是？",
        [("人类活动大量排放温室气体", True), ("太阳辐射明显增强", False),
         ("地球自转速度发生变化", False)],
        "工业革命以来，化石燃料燃烧使二氧化碳等温室气体浓度上升，温室效应增强，"
        "被认为是近现代升温的主因。太阳辐射变化属自然因素，无法解释近百年这种"
        "快速升温。",
    ),
    "geo-h-climate-types": (
        "地中海气候的成因是？",
        [("终年受赤道低压控制", False), ("受海陆热力性质差异影响", False),
         ("受西风带和副热带高压交替控制", True)],
        "地中海气候夏季受副热带高压控制、炎热干燥，冬季受西风带控制、温和多雨，"
        "成因是气压带风带的季节移动。终年受赤道低压控制形成的是热带雨林气候，"
        "海陆热力差异形成的是季风气候。",
    ),
    "geo-h-crustal-movement": (
        "喜马拉雅山脉的形成主要是由于？",
        [("板块张裂", False), ("板块碰撞挤压隆起", True), ("火山喷发堆积", False)],
        "喜马拉雅山由印度洋板块与亚欧板块碰撞挤压隆起形成，位于消亡边界。板块"
        "张裂形成的是裂谷或海洋（如东非大裂谷），火山喷发堆积形成的是火山地貌。",
    ),
    "geo-h-earth-in-universe": (
        "地球上存在生命的重要条件之一是？",
        [("日地距离适中，地表温度适宜", True),
         ("地球是太阳系中体积最大的行星", False),
         ("地球拥有卫星月球", False)],
        "日地距离适中使地表温度适宜、液态水能够存在，是生命存在的关键条件。"
        "太阳系体积最大的行星是木星；有没有卫星并不是生命存在的必要条件。",
    ),
    "geo-h-earth-motion": (
        "下列现象由地球自转产生的是？",
        [("四季更替", False), ("五带的划分", False), ("昼夜更替", True)],
        "昼夜更替由地球自转产生。四季更替、正午太阳高度的季节变化以及五带的"
        "划分，都由地球公转（加上黄赤交角）引起。要分清自转与公转各自的地理"
        "意义。",
    ),
    "geo-h-earth-revolution": (
        "夏至日这一天，下列各地中正午太阳高度最大的是？",
        [("赤道", False), ("北回归线", True), ("南回归线", False)],
        "夏至日太阳直射北回归线，北回归线上正午太阳高度为 90°，达到最大；"
        "此时赤道和南半球各地离直射点都较远，正午太阳高度较小。",
    ),
}


def block(q, opts, diag):
    letters = "ABC"
    btns = ""
    for i, (text, ok) in enumerate(opts):
        L = letters[i]
        corr = ' data-correct="1"' if ok else ""
        d = f' data-diag="{escape(diag)}"' if ok else ""
        btns += (f'<button class="quiz-option" data-q="pre" data-a="{L}"'
                 f'{corr}{d}>{L}. {escape(text)}</button>')
    return (f'\n<section class="section text-module" id="pretest" '
            f'data-bloom-level="remember" data-scaffold="full" data-tts="pretest">'
            f'<div class="panel"><span class="phase-tag">Pretest</span>'
            f'<h2>📝 课前诊断：先暴露一个误区</h2><p>{escape(q)}</p>{btns}'
            f'<div class="feedback" id="fb-pre">选择后显示错因诊断。</div>'
            f'</div></section>\n')


def put(html, frag):
    """插到 objectives 之后，没有则放 hero 后，再没有则 body 前"""
    for sid in ("objectives", "hero-infographic"):
        m = re.search(rf'<section\b[^>]*\bid="{sid}"[^>]*>', html)
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
    for cid, (q, opts, diag) in DATA.items():
        P = COMMUNITY / cid / "index.html"
        if not P.exists():
            print(f"  ⚠ 不存在 {cid}")
            continue
        html = P.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<section\b[^>]*\bid="pretest"', html):
            print(f"  跳过（已有）{cid}")
            continue
        new = put(html, block(q, opts, diag))
        if new is None:
            print(f"  ⚠ 无插入点 {cid}")
            continue
        if not dry:
            P.write_text(new, encoding="utf-8")
        n += 1
    print(f"写入 {n} 个课前诊断题" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
