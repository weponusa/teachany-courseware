#!/usr/bin/env python3
"""enhance-math-visuals.py — 数学课件视觉与互动增强（可泛化模板）
1. 补 iframe 容器样式（PhET/GeoGebra 可见）
2. 注入内嵌 SVG 几何图示（直角三边正方形面积图 / 3-4-5 特例 / 梯子应用 / 赵爽弦图）
3. 嵌入 GeoGebra 互动（拖动顶点验证 a²+b²=c²）
4. 删除空白 section
幂等：<!-- math-visuals-v1 -->
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CID = sys.argv[1] if len(sys.argv) > 1 else "math-m-pythagorean-theorem"
P = ROOT / "community" / CID / "index.html"
MARK = "<!-- math-visuals-v1 -->"

IFRAME_CSS = """.iframe-wrap{position:relative;width:100%;aspect-ratio:16/10;min-height:520px;border-radius:12px;overflow:hidden;border:1px solid rgba(148,163,184,.25);background:rgba(10,21,32,.6)}
.iframe-wrap iframe{position:absolute;inset:0;width:100%;height:100%;border:0;display:block}
.math-fig{display:block;margin:16px auto;max-width:100%;background:rgba(15,29,43,.6);border:1px solid rgba(148,163,184,.2);border-radius:12px}
.external-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:14px}"""

# ---- SVG 图示 ----
FIG_SQUARES = '''<figure class="ta-standard-figure"><figcaption>图1 三边正方形面积关系：两个小正方形面积之和等于大正方形（a²+b²=c²）</figcaption>
<svg class="math-fig" viewBox="0 0 480 460" role="img" aria-label="直角三角形与三边正方形">
  <defs>
    <style>
      .sq-a{fill:rgba(59,130,246,.28);stroke:#60a5fa;stroke-width:2}
      .sq-b{fill:rgba(52,211,153,.28);stroke:#34d399;stroke-width:2}
      .sq-c{fill:rgba(245,158,11,.22);stroke:#fbbf24;stroke-width:2}
      .tri{fill:rgba(239,68,68,.25);stroke:#f87171;stroke-width:2.5}
      .lbl{font:600 16px "PingFang SC",sans-serif;fill:#e2e8f0}
      .lbl-s{font:600 13px "PingFang SC",sans-serif;fill:#cbd5e1}
    </style>
  </defs>
  <!-- 直角三角形：直角顶点(200,260)，垂直边a=120，水平边b=160，斜边c=200 -->
  <polygon class="tri" points="200,260 200,140 360,260"/>
  <!-- a 边正方形（左侧） -->
  <polygon class="sq-a" points="200,140 200,260 80,260 80,140"/>
  <text class="lbl" x="126" y="206" text-anchor="middle">a²</text>
  <!-- b 边正方形（下方） -->
  <polygon class="sq-b" points="200,260 360,260 360,420 200,420"/>
  <text class="lbl" x="280" y="348" text-anchor="middle">b²</text>
  <!-- c 边正方形（斜边外侧） -->
  <polygon class="sq-c" points="200,140 360,260 240,420 80,300"/>
  <text class="lbl" x="220" y="290" text-anchor="middle">c²</text>
  <!-- 直角标记 -->
  <path d="M200,240 L220,240 L220,260" fill="none" stroke="#f87171" stroke-width="2"/>
  <!-- 边长标注 -->
  <text class="lbl-s" x="188" y="206" text-anchor="end">a</text>
  <text class="lbl-s" x="284" y="278" text-anchor="middle">b</text>
  <text class="lbl-s" x="292" y="192" text-anchor="middle">c</text>
</svg></figure>'''

FIG_345 = '''<figure class="ta-standard-figure"><figcaption>图2 最经典的整数边直角三角形：3-4-5（3²+4²=9+16=25=5²）</figcaption>
<svg class="math-fig" viewBox="0 0 420 320" role="img" aria-label="3-4-5 直角三角形">
  <polygon fill="rgba(239,68,68,.22)" stroke="#f87171" stroke-width="2.5" points="80,240 80,120 260,240"/>
  <path d="M80,220 L100,220 L100,240" fill="none" stroke="#f87171" stroke-width="2"/>
  <g font="600 17px 'PingFang SC',sans-serif" fill="#e2e8f0">
    <text x="62" y="188" text-anchor="end">3</text>
    <text x="176" y="264" text-anchor="middle">4</text>
    <text x="184" y="168" text-anchor="middle">5</text>
  </g>
  <g font="600 15px 'PingFang SC',sans-serif" fill="#7dd3fc">
    <text x="80" y="288">3² + 4² = 9 + 16 = 25</text>
    <text x="80" y="312">5² = 25 ✓</text>
  </g>
</svg></figure>'''

FIG_LADDER = '''<figure class="ta-standard-figure"><figcaption>图3 生活应用：梯子靠墙——已知梯长与墙高，求地面距离</figcaption>
<svg class="math-fig" viewBox="0 0 420 320" role="img" aria-label="梯子靠墙的勾股定理应用">
  <line x1="80" y1="40" x2="80" y2="270" stroke="#64748b" stroke-width="3"/>
  <line x1="80" y1="270" x2="360" y2="270" stroke="#64748b" stroke-width="3"/>
  <line x1="80" y1="90" x2="300" y2="270" stroke="#f59e0b" stroke-width="4"/>
  <g stroke="#fbbf24" stroke-width="1.5" opacity=".8">
    <line x1="120" y1="132" x2="140" y2="152"/><line x1="160" y1="176" x2="180" y2="196"/>
    <line x1="200" y1="220" x2="220" y2="240"/><line x1="240" y1="264" x2="260" y2="270"/>
  </g>
  <path d="M80,250 L100,250 L100,270" fill="none" stroke="#f87171" stroke-width="2"/>
  <g font="600 15px 'PingFang SC',sans-serif" fill="#e2e8f0">
    <text x="72" y="186" text-anchor="end">墙高 4 m</text>
    <text x="200" y="292" text-anchor="middle">地面距离 ？m</text>
    <text x="216" y="176">梯长 5 m</text>
  </g>
</svg></figure>'''

GEOGEBRA = '''<section class="section" id="geogebra-lab" data-interactive="sim" data-bloom-level="apply" data-tts="geogebra-lab" data-tsh="互动实验 - 拖动验证勾股定理">
<div class="lesson-panel"><span class="phase-tag">Interactive Lab</span>
<h2>🔺 拖动三角形顶点，实时验证 a² + b² = c²</h2>
<div class="iframe-wrap"><iframe src="https://www.geogebra.org/classic?lang=zh_CN" title="GeoGebra 勾股定理互动实验" allowfullscreen loading="lazy" sandbox="allow-scripts allow-same-origin allow-forms allow-popups"></iframe></div>
<p class="feedback" style="margin-top:12px">💡 在 GeoGebra 中画一个直角三角形，测量三边长度并计算 a²+b² 与 c²，拖动顶点观察两者是否始终相等。</p>
<p style="font-size:12px;color:#64748b">外链：<a href="https://www.geogebra.org/classic?lang=zh_CN" target="_blank" rel="noopener">GeoGebra 经典版</a> · <a href="https://phet.colorado.edu/zh_CN/sims/html/trig-tour/latest/trig-tour_zh_CN.html" target="_blank" rel="noopener">PhET 三角函数游览</a></p>
</div></section>'''

EXTERNAL_LINKS = '''<div class="card" style="border-left:4px solid #a78bfa;">
<h3 style="margin:0 0 10px;">🔗 拓展资源</h3>
<div class="external-links">
  <a class="mini-card" href="https://www.geogebra.org/classic?lang=zh_CN" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><strong>GeoGebra 经典版</strong><br><span style="font-size:13px;opacity:.85">拖动验证勾股定理</span></a>
  <a class="mini-card" href="https://phet.colorado.edu/zh_CN/sims/html/trig-tour/latest/trig-tour_zh_CN.html" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><strong>PhET 三角函数</strong><br><span style="font-size:13px;opacity:.85">单位圆与三角关系</span></a>
  <a class="mini-card" href="https://basic.smartedu.cn/" target="_blank" rel="noopener" style="text-decoration:none;color:inherit"><strong>国家中小学智慧教育平台</strong><br><span style="font-size:13px;opacity:.85">同步课程资源</span></a>
</div>
</div>'''


def main():
    html = P.read_text(encoding="utf-8")
    if MARK in html:
        print("已增强")
        return
    actions = []

    # 1) iframe 样式
    if ".iframe-wrap" not in html:
        html = html.replace("</style>", IFRAME_CSS + "\n</style>", 1)
        actions.append("iframe样式")

    # 2) SVG 图示：插到精讲四卡之后（lesson-focus 后）
    m = re.search(r'(<div class="card focus-detail"><p><strong>易错提醒：</strong>[\s\S]*?</div>)', html)
    if m:
        html = html[:m.end()] + "\n" + FIG_SQUARES + "\n" + FIG_345 + "\n" + FIG_LADDER + html[m.end():]
        actions.append("SVG图示×3")

    # 3) GeoGebra 互动（插到 PhET 块前）
    if "geogebra-lab" not in html:
        mp = re.search(r'<section\b[^>]*id="phet-lab"', html)
        if mp:
            html = html[:mp.start()] + GEOGEBRA + "\n" + html[mp.start():]
        else:
            html = html.replace("</body>", GEOGEBRA + "\n</body>", 1)
        actions.append("GeoGebra")

    # 4) 拓展资源卡（posttest 前）
    if "拓展资源" not in html:
        mp2 = re.search(r'<section\b[^>]*id="posttest"', html)
        if mp2:
            html = html[:mp2.start()] + EXTERNAL_LINKS + "\n" + html[mp2.start():]
        actions.append("拓展资源")

    # 5) 删空白 section
    def remove_empty(h):
        out, changed = [], False
        for m2 in re.finditer(r'<section\b[^>]*>[\s\S]*?</section>', h):
            body = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", m2.group(0)))
            if len(body) < 5 and "<img" not in m2.group(0) and "<canvas" not in m2.group(0) and "<svg" not in m2.group(0) and "<iframe" not in m2.group(0):
                changed = True
                continue
            out.append(m2.group(0))
        return h, changed
    # 逐段扫描删除空 section（保留段落间文本）
    def remove_empty_inplace(h):
        result, changed = [], False
        parts = re.split(r'(<section\b[^>]*>[\s\S]*?</section>)', h)
        for seg in parts:
            if re.match(r'^<section\b', seg or ""):
                body = re.sub(r"\s+", "", re.sub(r"<[^>]+>", "", seg))
                if len(body) < 5 and not any(k in seg for k in ("<img", "<canvas", "<svg", "<iframe")):
                    changed = True
                    continue
            result.append(seg)
        return "".join(result), changed
    html, ch = remove_empty_inplace(html)
    if ch:
        actions.append("删空白模块")

    if not actions:
        print("无可增强项")
        return
    html = html.replace("</body>", MARK + "\n</body>", 1)
    P.write_text(html, encoding="utf-8")
    print(f"增强完成: {'、'.join(actions)}")


if __name__ == "__main__":
    main()
