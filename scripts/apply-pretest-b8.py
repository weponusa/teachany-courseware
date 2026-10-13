#!/usr/bin/env python3
"""apply-pretest-b8.py — 写入第 8 批（高中地理）课前诊断题（人工撰写，非模板生成）

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
    "geo-h-natural-zones": (
        "从赤道到两极的自然带更替，其主导因素是？",
        [("热量", True), ("水分", False), ("地形", False)],
        "由赤道到两极的地域分异以热量为基础（纬度地带性）；从沿海到内陆的"
        "分异以水分为基础（经度地带性）；山地垂直分异则是水热组合随海拔升高"
        "而变化。三者成因不同，要先判断分异方向。",
    ),
    "geo-h-ocean-current": (
        "北半球中低纬度的大洋环流，流向是？",
        [("逆时针", False), ("顺时针", True), ("没有固定规律", False)],
        "北半球中低纬大洋环流呈顺时针，南半球呈逆时针；而北半球中高纬环流"
        "是逆时针。记忆时要区分半球和纬度带，不能只记一个方向。",
    ),
    "geo-h-plate-tectonics": (
        "下列地区中，位于板块生长边界的是？",
        [("喜马拉雅山脉", False), ("马里亚纳海沟", False), ("大西洋中脊", True)],
        "生长边界是板块张裂处，形成海岭、裂谷（如大西洋中脊、东非大裂谷）；"
        "消亡边界是碰撞挤压处，形成高大山脉（喜马拉雅）或海沟（马里亚纳）。"
        "判断的关键是板块运动方向。",
    ),
    "geo-h-population-growth": (
        "一个地区的人口自然增长率取决于？",
        [("出生率与死亡率之差", True), ("迁入人口与迁出人口之差", False),
         ("人口总数与面积之比", False)],
        "自然增长率＝出生率－死亡率，只反映自然变动；迁入减迁出是机械增长；"
        "人口总数与面积之比是人口密度。三者是完全不同的概念，容易混淆。",
    ),
    "geo-h-population-migration": (
        "一般而言，影响人口迁移最主要、最经常起作用的因素是？",
        [("气候条件", False), ("经济因素", True), ("地形条件", False)],
        "就业机会、收入水平、发展前景等经济因素是人口迁移的主要动因，多数"
        "情况下起决定作用。气候、地形等自然因素在历史上影响较大，现代迁移"
        "更多由经济原因驱动。",
    ),
    "geo-h-population-urbanization": (
        "衡量一个国家或地区城市化水平的最主要指标是？",
        [("城市的数量", False), ("城市的面积", False),
         ("城市人口占总人口的比重", True)],
        "城市化水平的核心指标是城市人口比重。城市数量和建成区面积只反映城市"
        "规模大小，并不能说明城市化的程度。",
    ),
    "geo-h-resource-energy": (
        "下列属于非可再生资源的是？",
        [("煤炭", True), ("太阳能", False), ("风能", False)],
        "煤炭、石油、天然气等化石燃料形成周期极其漫长，短期内无法补充，属于"
        "非可再生资源；太阳能、风能、水能可以持续获得，属于可再生资源。",
    ),
    "geo-h-river-features": (
        "河流上游段最常见的开发利用方式是？",
        [("发展航运", False), ("开发水能", True), ("引水灌溉", False)],
        "上游落差大、水流急，水能资源丰富，适合建设水电站；中下游地势平缓、"
        "水量较大，才更适宜发展航运和灌溉。",
    ),
    "geo-h-service-location": (
        "大型商场选址时，最优先考虑的区位因素是？",
        [("原料供应", False), ("能源供应", False), ("市场和交通通达度", True)],
        "服务业直接面向消费者，布局最看重市场（人流量、消费能力）和交通通达度。"
        "原料、能源是传统工业选址时考虑较多的因素，对商业影响很小。",
    ),
    "geo-h-sustainable-development": (
        "可持续发展的三大基本原则是？",
        [("公平性、持续性、共同性", True), ("效率性、效益性、环保性", False),
         ("经济性、安全性、美观性", False)],
        "三大原则是公平性（代内与代际公平）、持续性（不超过资源环境承载力）、"
        "共同性（全球共同协作）。后两组都不是可持续发展理论的基本原则。",
    ),
    "geo-h-transportation": (
        "山区公路多呈「之」字形弯曲，主要是为了？",
        [("缩短两地距离", False), ("降低坡度，保证行车安全", True),
         ("减少占用耕地", False)],
        "山区地形起伏大，公路沿等高线迂回前进可以减小坡度、保障行车安全，"
        "代价是里程变长。这也是山区公路建设成本高、路网密度小的原因之一。",
    ),
    "geo-h-transportation-communication": (
        "交通条件改善对区域发展的主要作用是？",
        [("减少区域之间的联系", False), ("降低区域的对外开放程度", False),
         ("加强区际联系，促进资源开发和产业布局优化", True)],
        "交通改善缩短时空距离，加强区域之间的人员、物资、信息流动，带动资源"
        "开发、扩大市场范围，并促进产业布局优化，从而提高区域开放程度。",
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
