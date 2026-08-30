#!/usr/bin/env python3
"""apply-pretest-b7.py — 写入第 7 批（高中地理）课前诊断题（人工撰写，非模板生成）

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
    "geo-h-earth-rotation": (
        "北半球沿水平方向运动的物体，在地转偏向力作用下会？",
        [("向右偏转", True), ("向左偏转", False), ("不发生偏转", False)],
        "受地转偏向力影响，北半球向右偏、南半球向左偏、赤道上不偏转。判断时"
        "要沿物体的运动方向看左右，南半球情况与北半球正好相反。",
    ),
    "geo-h-earth-structure": (
        "地球内部圈层划分的主要依据是？",
        [("各层的颜色差异", False), ("地震波传播速度的变化", True),
         ("各层温度的高低", False)],
        "地震波在不同物质中传播速度不同，科学家正是依据横波、纵波速度的突变"
        "界面（莫霍面、古登堡面）划分出地壳、地幔和地核。人类无法直接观察"
        "地球内部，地震波是最主要的探测手段。",
    ),
    "geo-h-environmental-issues": (
        "下列做法最符合可持续发展原则的是？",
        [("先发展经济，等有钱了再治理污染", False),
         ("为保护环境停止一切开发活动", False),
         ("在发展中保护，实现经济与环境的协调", True)],
        "可持续发展强调经济、社会、生态三者协调：既不能走「先污染后治理」的"
        "老路，也不是停止发展，而是转变发展方式，在保护中发展。",
    ),
    "geo-h-global-circulation": (
        "形成三圈环流的根本原因是？",
        [("高低纬受热不均，加上地转偏向力", True), ("海陆热力性质差异", False),
         ("地形起伏的影响", False)],
        "太阳辐射在纬度上分布不均造成高低纬受热差异，这是大气运动的根本原因；"
        "地转偏向力使气流方向发生改变，两者共同形成三圈环流。海陆热力差异"
        "形成的是季风，地形只起局部影响。",
    ),
    "geo-h-hydrosphere": (
        "水循环中，把海洋上空的水汽输送到陆地上空的主要环节是？",
        [("地表径流", False), ("水汽输送", True), ("下渗", False)],
        "水汽输送（主要由大气环流完成）把海洋上空的水汽带到陆地上空，为陆地"
        "降水提供水源；地表径流是水返回海洋的过程，下渗则是降水进入地下。",
    ),
    "geo-h-industry-cluster": (
        "工业集聚最主要的目的是？",
        [("增加企业数量", False), ("减少城市人口", False),
         ("降低运输成本、共用基础设施，获得规模效益", True)],
        "工业集聚可以共用基础设施、加强生产协作与信息交流、降低运输成本，从而"
        "获得规模效益。它不是为了单纯增加企业数量，与城市人口多少也无直接关系。",
    ),
    "geo-h-industry-location": (
        "钢铁工业布局在铁矿产地附近，主要考虑的区位因素是？",
        [("原料", True), ("市场", False), ("技术", False)],
        "钢铁工业原料消耗量大、产品重量相对减轻，靠近原料产地可节省运输成本，"
        "属于原料指向型。集成电路等属于技术指向型，啤酒等易变质产品属于市场"
        "指向型。",
    ),
    "geo-h-industry-services": (
        "与工业相比，服务业的显著特点是？",
        [("需要大量原料投入", False),
         ("产品多为无形服务，生产与消费常同时进行", True),
         ("必须靠近原料产地布局", False)],
        "服务业提供的是无形的服务，生产与消费往往在同一时间、同一地点完成，"
        "对原料依赖小，布局更看重市场、信息和劳动力素质，而不是原料产地。",
    ),
    "geo-h-landforms": (
        "三角洲地貌主要形成于什么地方？",
        [("山前出山口地带", False), ("冰川消融区", False),
         ("河流入海或入湖的河口处", True)],
        "河流在入海（湖）口处流速减慢，搬运能力下降，泥沙大量沉积形成三角洲，"
        "属于流水沉积地貌。山前出山口多形成冲积扇，冰川消融区形成冰碛地貌。",
    ),
    "geo-h-monsoon-system": (
        "东亚季风形成的主要原因是？",
        [("海陆热力性质差异", True), ("地形阻挡", False), ("洋流影响", False)],
        "东亚位于世界最大的大陆与最大的大洋之间，海陆热力性质差异最显著，形成"
        "典型的季风。南亚的西南季风除海陆差异外，还与气压带风带的季节移动有关。",
    ),
    "geo-h-natural-disaster": (
        "减轻洪涝灾害最有效的措施是？",
        [("灾害发生后全力救援", False),
         ("加强监测预警，同时保护湿地、退耕还湖", True),
         ("把河流全部改道", False)],
        "防灾减灾要「防救结合」：一方面加强监测预警，另一方面恢复湖泊、湿地的"
        "调蓄功能。灾后救援属于被动应对，河流全部改道既不现实也会破坏生态。",
    ),
    "geo-h-natural-integrity": (
        "「牵一发而动全身」体现了自然地理环境的什么特征？",
        [("差异性", False), ("开放性", False), ("整体性", True)],
        "整体性指各要素相互联系、相互制约，一个要素发生变化会引起其他要素甚至"
        "整体的改变。差异性讲的是不同区域之间的区别，两者是不同概念，"
        "分析时要分清。",
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
