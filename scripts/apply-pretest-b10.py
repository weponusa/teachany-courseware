#!/usr/bin/env python3
"""apply-pretest-b10.py — 写入第 10 批（收尾）课前诊断题（人工撰写，非模板生成）

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
    "geo-h-urban-problems": (
        "大城市出现「热岛效应」的主要原因是？",
        [("人为热排放多、下垫面性质改变", True), ("城市纬度较低", False),
         ("城市海拔较高", False)],
        "热岛效应由城市大量人为热排放、建筑材料吸热强、植被和水面减少等共同"
        "造成，与纬度、海拔无关。增加绿地和水面、减少人为热排放是缓解措施。",
    ),
    "geo-h-urban-structure": (
        "城市中最广泛的土地利用方式一般是？",
        [("工业用地", False), ("住宅用地", True), ("商业用地", False)],
        "住宅用地通常占城市用地的很大比重，是最广泛的土地利用方式。商业用地"
        "集中在市中心，占地不大但地价最高，两者不要混淆。",
    ),
    "geo-h-urbanization": (
        "发展中国家城市化进程中的突出问题是？",
        [("城市人口比重过低", False), ("城市数量太少", False),
         ("城市化速度与经济发展水平不协调", True)],
        "部分发展中国家城市化快于工业化和经济发展，出现就业不足、住房紧张、"
        "贫民窟等问题，属于「过度城市化」。发达国家面临的则多是逆城市化。",
    ),
    "geo-h-vegetation-soil": (
        "热带雨林植被的典型特征是？",
        [("终年常绿，层次多，有板根和茎花现象", True), ("叶片细小、根系发达", False),
         ("冬季落叶", False)],
        "热带雨林全年高温多雨，植被终年常绿、层次复杂，常见板根、茎花、绞杀"
        "等现象。叶片细小是荒漠植被的适应特征，冬季落叶属温带落叶阔叶林。",
    ),
    "geo-h-water-cycle": (
        "人类活动对水循环影响最显著的环节是？",
        [("水汽输送", False), ("地表径流", True), ("降水", False)],
        "人类通过修建水库、跨流域调水、城市化改变下垫面等方式，主要改变的是"
        "地表径流。对水汽输送和大范围降水的人为影响目前还很有限。",
    ),
    "geo-h-weather-system": (
        "冷锋过境后，当地天气一般表现为？",
        [("气温升高、气压降低", False), ("持续阴雨", False),
         ("气温下降、气压升高、天气转晴", True)],
        "冷锋过境后当地受冷气团控制，气温下降、气压升高、天气转晴；大风降温"
        "雨雪出现在过境时。暖锋过境后才是气温升高、气压降低。",
    ),
    "hist-m-may-fourth-movement": (
        "五四运动爆发的直接导火索是？",
        [("巴黎和会上中国外交的失败", True), ("辛亥革命的爆发", False),
         ("甲午中日战争中国战败", False)],
        "1919 年巴黎和会拒绝中国收回山东权益的正当要求，消息传回国内，直接引发"
        "五四运动。甲午战败在 1895 年，辛亥革命在 1911 年，时间都对不上。",
    ),
    "hist-m-sui-tang-ruling": (
        "隋朝创立、唐朝进一步完善的选官制度是？",
        [("察举制", False), ("科举制", True), ("九品中正制", False)],
        "科举制由隋朝创立、唐朝完善，以考试成绩选拔官员，扩大了统治基础。"
        "察举制是汉代做法，九品中正制行于魏晋南北朝、重门第，时代不同。",
    ),
    "info-u-signals-pbl": (
        "关于模拟信号与数字信号，下列说法正确的是？",
        [("模拟信号抗干扰能力更强", False),
         ("数字信号在时间和幅值上都是连续的", False),
         ("数字信号抗干扰能力强，便于存储和远距离传输", True)],
        "数字信号在时间和幅值上都是离散的，抗干扰能力强，便于存储、压缩和远距离"
        "传输，所以现代通信广泛采用数字方式。模拟信号连续但容易受干扰。",
    ),
    "math-elem-fraction-operations": (
        "计算 1/2 ＋ 1/3，正确结果是？",
        [("5/6", True), ("2/5", False), ("1/6", False)],
        "异分母分数相加要先通分：1/2＝3/6，1/3＝2/6，相加得 5/6。把分子、分母"
        "分别相加得到 2/5 是典型错法，那样做没有统一的分数单位。",
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
