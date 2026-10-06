#!/usr/bin/env python3
"""apply-pretest-b11.py — 写入第 10 批（收尾）课前诊断题（人工撰写，非模板生成）

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
    "math-elem-fractions-intro": (
        "把一个蛋糕平均分成 4 份，取其中 3 份，用分数表示是？",
        [("1/4", False), ("3/4", True), ("4/3", False)],
        "分母表示把整体平均分成多少份（4 份），分子表示取了几份（3 份），所以"
        "是 3/4。也可以想成取了 3 个 1/4。",
    ),
    "math-elem-fractions-meaning": (
        "分数 3/4 的分子和分母同时乘 2，分数的大小？",
        [("变大", False), ("变小", False), ("不变", True)],
        "根据分数的基本性质：分子和分母同时乘或除以相同的数（0 除外），分数"
        "大小不变，即 3/4＝6/8。这正是约分和通分的依据。",
    ),
    "math-elem-large-numbers": (
        "10 个一万是？",
        [("十万", True), ("一百万", False), ("一千", False)],
        "相邻计数单位之间的进率都是 10：10 个一万是十万，10 个十万是一百万，"
        "10 个一百万是一千万，按十进制顺序推即可。",
    ),
    "math-elem-length-units": (
        "1 千米等于多少米？",
        [("100 米", False), ("1000 米", True), ("10 米", False)],
        "1 千米＝1000 米；1 米＝10 分米＝100 厘米＝1000 毫米。注意千米与米之间"
        "的进率是 1000，其余相邻长度单位之间的进率是 10。",
    ),
    "math-elem-line-graph": (
        "折线统计图最主要的优点是？",
        [("能看出数量的多少", False), ("能看出各部分占总数的比例", False),
         ("能清楚反映数量的增减变化趋势", True)],
        "折线统计图通过线段的升降直观反映数量随时间的变化趋势，这是它区别于"
        "条形统计图的最大特点。要看各部分占总数的比例，应当用扇形统计图。",
    ),
    "math-elem-mass-units": (
        "1 吨等于多少千克？",
        [("1000 千克", True), ("100 千克", False), ("10 千克", False)],
        "1 吨＝1000 千克，1 千克＝1000 克。质量单位中相邻单位间的进率都是 1000，"
        "与多数长度单位进率为 10 的情况不同，容易记混。",
    ),
    "math-elem-multi-digit-divide": (
        "计算除数是两位数的除法时，一般怎样试商？",
        [("把除数看作整百数", False),
         ("用四舍五入法看作与它接近的整十数", True),
         ("直接当作一位数来算", False)],
        "除数是两位数时，常用四舍五入法把它看成接近的整十数来试商，再根据余数"
        "调整商的大小（商大了调小、商小了调大），这是提高试商速度的基本方法。",
    ),
    "math-high-power-function": (
        "下列函数中，属于幂函数的是？",
        [("y＝2^x", False), ("y＝x＋1", False), ("y＝x²", True)],
        "幂函数的形式是 y＝x^α（α 为常数），自变量在底数位置，如 y＝x²、y＝x³。"
        "y＝2^x 的自变量在指数上，属于指数函数，与幂函数不同。",
    ),
    "science-genetics-variation-intro": (
        "「种瓜得瓜，种豆得豆」描述的是生物的什么现象？",
        [("遗传", True), ("变异", False), ("进化", False)],
        "子代与亲代相似的现象叫遗传；子代与亲代之间以及子代个体之间的差异叫"
        "变异。「种瓜得瓜」强调的是前后代相似，因此属于遗传。",
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
