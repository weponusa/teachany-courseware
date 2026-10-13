#!/usr/bin/env python3
"""apply-pretest-b9.py — 写入第 9 批（小学数学）课前诊断题（人工撰写，非模板生成）

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
    "math-elem-area-units": (
        "1 平方米等于多少平方分米？",
        [("100", True), ("10", False), ("1000", False)],
        "1 米＝10 分米，所以 1 平方米＝10×10＝100 平方分米。面积单位的进率是"
        "长度单位进率的平方，这里很容易误记成 10。",
    ),
    "math-elem-average-median": (
        "一组数据：2、3、100。要表示这组数据的「一般水平」，更合适的是？",
        [("平均数", False), ("中位数", True), ("最大的数", False)],
        "这组数据含有极端值 100，平均数被拉高到 35，反而不能代表多数数据的水平；"
        "中位数是 3，更贴近一般情况。数据中有极端值时通常优先选用中位数。",
    ),
    "math-elem-circle-area": (
        "圆的半径扩大到原来的 2 倍，面积会扩大到原来的几倍？",
        [("2 倍", False), ("3 倍", False), ("4 倍", True)],
        "圆面积 S＝πr²，半径变为 2 倍时，面积变为 2²＝4 倍。面积与半径的平方"
        "成正比，不是与半径本身成正比，这一点最容易记错。",
    ),
    "math-elem-complex-word-problems": (
        "解决复合应用题时，最关键的第一步是？",
        [("弄清数量关系，确定先算什么再算什么", True),
         ("把题目里的数字全部用上", False),
         ("先随便猜一个答案", False)],
        "复合应用题要先分析数量关系、想清楚解题步骤，再列式计算。想把题目里的"
        "数字都用上是常见误区，有些条件其实用不上；猜答案则没有依据。",
    ),
    "math-elem-cylinder-cone": (
        "等底等高的圆柱和圆锥，体积关系是？",
        [("圆锥是圆柱的 1/2", False), ("圆锥是圆柱的 1/3", True), ("两者相等", False)],
        "等底等高时，圆锥体积是圆柱体积的三分之一，这可以通过倒水或倒沙实验"
        "验证：装满圆锥三次才能倒满等底等高的圆柱。",
    ),
    "math-elem-decimal-operations": (
        "计算 0.25 × 0.4 时，积的小数位数是几位？",
        [("一位", False), ("两位", False), ("三位", True)],
        "0.25 有两位小数，0.4 有一位，积的小数位数是 2＋1＝3 位。0.25×0.4＝"
        "0.100，末尾的 0 化简后写成 0.1，但确定位数时仍应按三位来算。",
    ),
    "math-elem-decimals-intro": (
        "比较 0.5 和 0.12，结果是？",
        [("0.5 大", True), ("0.12 大", False), ("一样大", False)],
        "比较小数要先比整数部分，再依次比十分位、百分位。0.5 的十分位是 5，"
        "0.12 的十分位是 1，所以 0.5 更大。不能只看小数位数多少或数字表面大小。",
    ),
    "math-elem-decimals-meaning": (
        "在小数的末尾添上 0 或去掉 0，小数的大小？",
        [("变大", False), ("不变", True), ("变小", False)],
        "根据小数的性质，小数末尾添上 0 或去掉 0，大小不变（如 3.5＝3.50）。"
        "但要注意必须是「末尾」，小数中间的 0 是不能去掉的。",
    ),
    "math-elem-division-intro": (
        "在有余数的除法中，余数与除数相比？",
        [("余数大", False), ("一样大", False), ("余数一定比除数小", True)],
        "余数必须比除数小；如果余数大于或等于除数，说明还能再分一份，也就是"
        "商小了。这是检验有余数除法是否正确的重要依据。",
    ),
    "math-elem-equation-intro": (
        "下列写法中，符合「用字母表示数」规范的是？",
        [("a×3 写作 3a", True), ("a×3 写作 a3", False), ("1×a 写作 1a", False)],
        "数字与字母相乘时，数字写在字母前面并省略乘号，如 3a；1 与字母相乘时，"
        "1 要省略不写，直接写成 a。",
    ),
    "math-elem-four-operations-laws": (
        "计算 25×37×4 时，运用什么运算律最简便？",
        [("乘法分配律", False), ("乘法交换律和结合律", True), ("加法结合律", False)],
        "利用乘法交换律和结合律先算 25×4＝100，再乘 37 得 3700，最为简便。"
        "乘法分配律适用于 (a＋b)×c 这样的形式，这里用不上。",
    ),
    "math-elem-fraction-decimal-percent": (
        "把 0.25 化成百分数，结果是？",
        [("2.5%", False), ("250%", False), ("25%", True)],
        "小数化百分数，把小数点向右移动两位，再添上百分号：0.25＝25%。注意要"
        "移动两位，只移一位就错成 2.5% 了。",
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
