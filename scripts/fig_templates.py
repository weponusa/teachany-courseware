#!/usr/bin/env python3
"""fig-templates.py — 教学示意图 SVG 模板库（纯本地生成，零外部依赖）

设计遵循「深色科技风信息图」规范：
  底色 #0a1520 + 圆角外框 + 五色功能体系 + 线性渐变 + 引线标注 + 图例
  动画用 SMIL（渐显入场 / 流动虚线 / 呼吸脉动），零 JS 依赖

五色语义：
  蓝 #3b82f6 结构体   橙 #f59e0b 运动变化   红 #ef4444 能量热源
  绿 #34d399 条件控制  紫 #a78bfa 连接传动

提供模板：
  cycle        循环/流程环形图（如四冲程、碳循环、解题闭环）
  hierarchy    层次结构图（知识体系、分类树）
  compare      双栏对比图（异同、正反、易错辨析）
  composition  组成结构图（部件 + 引线标注）
  steps        阶梯进程图（步骤推进、层级递进）
"""
from html import escape

W, H = 640, 420
BG = "#0a1520"
FRAME = "rgba(148,163,184,.07)"
FRAME_LINE = "#334155"
TEXT = "#e2e8f0"
KEY = "#fbbf24"      # 关键术语
DATA = "#7dd3fc"     # 数据
LEAD = "#64748b"     # 引线
DOT = "#7dd3fc"      # 引线端点

PALETTE = ["#3b82f6", "#f59e0b", "#ef4444", "#34d399", "#a78bfa"]
# 每种色配「亮描边」
STROKE = {"#3b82f6": "#60a5fa", "#f59e0b": "#fbbf24", "#ef4444": "#f87171",
          "#34d399": "#6ee7b7", "#a78bfa": "#c4b5fd"}


def esc(s):
    return escape(str(s), quote=True)


def wrap(text, per=8, max_lines=2):
    """中文按字数断行（教学图标注通常短，按字数比按宽度稳）"""
    t = str(text).strip()
    if len(t) <= per:
        return [t]
    lines, cur = [], ""
    for ch in t:
        cur += ch
        if len(cur) >= per:
            lines.append(cur)
            cur = ""
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1][:-1] + "…"
    return lines


def defs(colors):
    """渐变 + 箭头 marker 定义"""
    g = []
    for i, c in enumerate(colors):
        g.append(
            f'<linearGradient id="gf{i}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0%" stop-color="{c}" stop-opacity=".30"/>'
            f'<stop offset="100%" stop-color="{c}" stop-opacity=".10"/>'
            f'</linearGradient>')
    g.append('<marker id="ar" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">'
             '<path d="M0,0 L0,6 L9,3 z" fill="#fbbf24"/></marker>')
    g.append('<marker id="ar2" markerWidth="9" markerHeight="9" refX="8" refY="3" orient="auto">'
             '<path d="M0,0 L0,6 L9,3 z" fill="#7dd3fc"/></marker>')
    return "<defs>" + "".join(g) + "</defs>"


def bg(title=None, subtitle=None):
    """背景层 + 外框 + 可选标题"""
    s = [f'<rect x="0" y="0" width="{W}" height="{H}" fill="{BG}"/>']
    # 极淡网格
    for x in range(40, W, 40):
        s.append(f'<line x1="{x}" y1="20" x2="{x}" y2="{H-20}" stroke="#94a3b8" stroke-opacity=".05"/>')
    for y in range(40, H, 40):
        s.append(f'<line x1="20" y1="{y}" x2="{W-20}" y2="{y}" stroke="#94a3b8" stroke-opacity=".05"/>')
    s.append(f'<rect x="14" y="14" width="{W-28}" height="{H-28}" rx="10" fill="{FRAME}" '
             f'stroke="{FRAME_LINE}" stroke-width="1"/>')
    if title:
        s.append(f'<text x="{W//2}" y="46" font-size="16" font-weight="700" fill="{KEY}" '
                 f'text-anchor="middle">{esc(title)}</text>')
    if subtitle:
        s.append(f'<text x="{W//2}" y="66" font-size="12" fill="{TEXT}" opacity=".75" '
                 f'text-anchor="middle">{esc(subtitle)}</text>')
    return "".join(s)


def legend(items, x=None, y=None):
    """图例框：小色块 + 说明"""
    n = len(items)
    if n == 0:
        return ""
    bw, bh = 168, 26 + n * 19
    x = W - bw - 30 if x is None else x
    y = H - bh - 26 if y is None else y
    s = [f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" fill="rgba(15,23,42,.72)" '
         f'stroke="{FRAME_LINE}"/>']
    s.append(f'<text x="{x+12}" y="{y+18}" font-size="12" font-weight="700" fill="{TEXT}">图例</text>')
    for i, (color, label) in enumerate(items):
        yy = y + 36 + i * 19
        s.append(f'<rect x="{x+12}" y="{yy-9}" width="11" height="11" rx="2" fill="{color}"/>')
        s.append(f'<text x="{x+30}" y="{yy}" font-size="12" fill="{TEXT}">{esc(label)}</text>')
    return "".join(s)


def lead_line(x1, y1, x2, y2, label, anchor="start", delay=0.0):
    """引线 + 端点圆点 + 标注（带渐显动画）"""
    s = [f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{LEAD}" '
         f'stroke-width="1" opacity=".8"/>']
    s.append(f'<circle cx="{x1:.0f}" cy="{y1:.0f}" r="3" fill="{DOT}"/>')
    lines = wrap(label, 9, 2)
    for i, ln in enumerate(lines):
        s.append(f'<text x="{x2:.0f}" y="{y2 + i*15:.0f}" font-size="12" fill="{TEXT}" '
                 f'text-anchor="{anchor}">{esc(ln)}'
                 f'<animate attributeName="opacity" from="0" to="1" dur=".5s" '
                 f'begin="{delay:.2f}s" fill="freeze"/></text>')
    return "".join(s)


def shell(inner, title=None, subtitle=None, colors=None, legend_items=None):
    """组装完整 SVG"""
    colors = colors or PALETTE
    parts = [f'<svg class="math-fig" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
             defs(colors), bg(title, subtitle), inner]
    if legend_items:
        parts.append(legend(legend_items))
    parts.append("</svg>")
    return "".join(parts)


# ---------------------------------------------------------------- 模板 1：循环图
def cycle(items, title=None, subtitle=None, cx=None, cy=None, r=118):
    """环形流程：节点等分圆周，箭头串联，中心放主题

    items: [(标签, 说明), ...]  建议 3~6 个
    """
    n = len(items)
    cx = W // 2 - 40 if cx is None else cx
    cy = H // 2 + 6 if cy is None else cy
    colors = PALETTE[:max(3, min(5, n))]
    s = []

    # 中心圆
    s.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="url(#gf0)" stroke="{STROKE[colors[0]]}" '
             f'stroke-width="2"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="none" stroke="{colors[0]}" '
             f'stroke-opacity=".35"><animate attributeName="r" values="46;52;46" dur="3s" '
             f'repeatCount="indefinite"/></circle>')
    ct = wrap(title or "循环过程", 6, 2)
    for i, ln in enumerate(ct):
        s.append(f'<text x="{cx}" y="{cy - 4 + i*17 - (len(ct)-1)*8}" font-size="14" '
                 f'font-weight="700" fill="{KEY}" text-anchor="middle">{esc(ln)}</text>')

    # 节点坐标
    import math
    pts = []
    for i in range(n):
        a = -math.pi / 2 + (2 * math.pi * i) / n
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    # 连线（带流动动画）
    for i in range(n):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % n]
        # 缩短线段两端，避免压住节点
        dx, dy = x2 - x1, y2 - y1
        L = (dx * dx + dy * dy) ** .5 or 1
        ux, uy = dx / L, dy / L
        ax, ay = x1 + ux * 34, y1 + uy * 34
        bx, by = x2 - ux * 34, y2 - uy * 34
        s.append(f'<path d="M{ax:.0f} {ay:.0f} L{bx:.0f} {by:.0f}" stroke="{DATA}" '
                 f'stroke-width="2" fill="none" marker-end="url(#ar2)" '
                 f'stroke-dasharray="7 5">'
                 f'<animate attributeName="stroke-dashoffset" from="24" to="0" dur="1.2s" '
                 f'repeatCount="indefinite"/></path>')

    # 节点
    for i, (label, desc) in enumerate(items):
        x, y = pts[i]
        c = colors[i % len(colors)]
        delay = 0.15 + i * 0.18
        s.append(f'<g><circle cx="{x:.0f}" cy="{y:.0f}" r="30" fill="url(#gf{i%5})" '
                 f'stroke="{STROKE[c]}" stroke-width="2">'
                 f'<animate attributeName="opacity" from="0" to="1" dur=".5s" '
                 f'begin="{delay:.2f}s" fill="freeze"/></circle>')
        ls = wrap(label, 4, 2)
        for j, ln in enumerate(ls):
            s.append(f'<text x="{x:.0f}" y="{y - 2 + j*15 - (len(ls)-1)*7:.0f}" font-size="12" '
                     f'font-weight="700" fill="{KEY}" text-anchor="middle">{esc(ln)}'
                     f'<animate attributeName="opacity" from="0" to="1" dur=".5s" '
                     f'begin="{delay:.2f}s" fill="freeze"/></text>')
        s.append("</g>")
        # 说明引线：从节点指向外侧
        import math as _m
        a = -_m.pi / 2 + (2 * _m.pi * i) / n
        ox, oy = cx + (r + 46) * _m.cos(a), cy + (r + 46) * _m.sin(a)
        anc = "start" if _m.cos(a) >= 0 else "end"
        s.append(lead_line(x + 30 * _m.cos(a), y + 30 * _m.sin(a), ox, oy, desc,
                           anchor=anc, delay=delay + .1))

    return shell("".join(s), title=None, subtitle=subtitle, colors=colors,
                 legend_items=[(colors[i % len(colors)], items[i][0]) for i in range(min(n, 5))])


# ---------------------------------------------------------------- 模板 2：层次结构
def hierarchy(root, branches, title=None, subtitle=None):
    """层次树：根在左，分支向右展开；或根在上、分支在下。

    这里用「根在上、分支在下」的两层结构，适合知识体系/分类。
    branches: [(标题, [子项...]), ...]  建议 2~4 组
    """
    colors = PALETTE[:max(3, len(branches))]
    s = []
    rx, ry = W // 2 - 30, 92
    s.append(f'<rect x="{rx-92}" y="{ry-24}" width="184" height="48" rx="10" fill="url(#gf0)" '
             f'stroke="{STROKE[colors[0]]}" stroke-width="2"/>')
    rl = wrap(root, 12, 2)
    for i, ln in enumerate(rl):
        s.append(f'<text x="{rx}" y="{ry + i*17 - (len(rl)-1)*8 + 5}" font-size="14" '
                 f'font-weight="700" fill="{KEY}" text-anchor="middle">{esc(ln)}</text>')

    n = len(branches)
    top, gap = 160, (H - 200) / max(1, n)
    for i, (head, subs) in enumerate(branches):
        c = colors[i % len(colors)]
        y = top + gap * i + gap / 2 - 10
        bx = 150
        delay = 0.2 + i * 0.16
        # 连线：根 → 分支
        s.append(f'<path d="M{rx} {ry+24} C {rx} {y-40}, {bx+120} {y-40}, {bx+120} {y-26}" '
                 f'stroke="{DATA}" stroke-width="1.6" fill="none" stroke-dasharray="6 4">'
                 f'<animate attributeName="stroke-dashoffset" from="20" to="0" dur="1.4s" '
                 f'repeatCount="indefinite"/></path>')
        # 分支头
        s.append(f'<rect x="{bx}" y="{y-26}" width="150" height="34" rx="8" fill="url(#gf{i%5})" '
                 f'stroke="{STROKE[c]}" stroke-width="1.8">'
                 f'<animate attributeName="opacity" from="0" to="1" dur=".5s" '
                 f'begin="{delay:.2f}s" fill="freeze"/></rect>')
        s.append(f'<text x="{bx+75}" y="{y-4}" font-size="13" font-weight="700" fill="{KEY}" '
                 f'text-anchor="middle">{esc(wrap(head,9,1)[0])}</text>')
        # 子项
        for j, sub in enumerate(subs[:3]):
            sy = y - 26 + j * 30 + 12
            s.append(f'<rect x="{bx+196}" y="{sy-13}" width="196" height="26" rx="6" '
                     f'fill="rgba(148,163,184,.10)" stroke="{FRAME_LINE}">'
                     f'<animate attributeName="opacity" from="0" to="1" dur=".45s" '
                     f'begin="{delay + .12 + j*.1:.2f}s" fill="freeze"/></rect>')
            s.append(f'<line x1="{bx+150}" y1="{y-9}" x2="{bx+196}" y2="{sy}" stroke="{LEAD}" '
                     f'stroke-width="1" opacity=".7"/>')
            s.append(f'<text x="{bx+206}" y="{sy+5}" font-size="12" fill="{TEXT}">'
                     f'{esc(wrap(sub, 16, 1)[0])}</text>')

    return shell("".join(s), title=title, subtitle=subtitle, colors=colors,
                 legend_items=[(colors[i % len(colors)], branches[i][0]) for i in range(min(n, 5))])


# ---------------------------------------------------------------- 模板 3：双栏对比
def compare(left, right, left_title="", right_title="", title=None, subtitle=None):
    """左右双栏对比：适合异同、正反、易错辨析"""
    colors = ["#3b82f6", "#f59e0b"]
    s = []
    mid = W // 2 - 20
    top = 96
    colw = 232

    # 中轴
    s.append(f'<line x1="{mid}" y1="{top-16}" x2="{mid}" y2="{H-70}" stroke="{LEAD}" '
             f'stroke-width="1.4" stroke-dasharray="4 4" opacity=".7"/>')

    for side, (items, ct, cx0, c) in enumerate([
            (left, left_title, 60, colors[0]),
            (right, right_title, mid + 28, colors[1])]):
        s.append(f'<rect x="{cx0}" y="{top-30}" width="{colw}" height="30" rx="7" '
                 f'fill="url(#gf{side})" stroke="{STROKE[c]}" stroke-width="1.8"/>')
        s.append(f'<text x="{cx0+colw//2}" y="{top-9}" font-size="13" font-weight="700" '
                 f'fill="{KEY}" text-anchor="middle">{esc(wrap(ct,12,1)[0])}</text>')
        for j, it in enumerate(items[:5]):
            y = top + 12 + j * 44
            delay = 0.2 + side * 0.1 + j * 0.1
            s.append(f'<rect x="{cx0}" y="{y}" width="{colw}" height="36" rx="7" '
                     f'fill="rgba(148,163,184,.09)" stroke="{FRAME_LINE}">'
                     f'<animate attributeName="opacity" from="0" to="1" dur=".45s" '
                     f'begin="{delay:.2f}s" fill="freeze"/></rect>')
            s.append(f'<rect x="{cx0}" y="{y}" width="4" height="36" rx="2" fill="{c}"/>')
            ls = wrap(it, 15, 2)
            for k, ln in enumerate(ls):
                s.append(f'<text x="{cx0+14}" y="{y+15+k*15 - (len(ls)-1)*6}" font-size="12" '
                         f'fill="{TEXT}">{esc(ln)}</text>')

    return shell("".join(s), title=title, subtitle=subtitle, colors=colors,
                 legend_items=[(colors[0], left_title or "左"), (colors[1], right_title or "右")])


# ---------------------------------------------------------------- 模板 4：组成结构
def composition(center, parts, title=None, subtitle=None):
    """中心主体 + 四周部件引线标注"""
    colors = PALETTE[:max(3, len(parts))]
    s = []
    cx, cy = W // 2 - 30, H // 2 + 4
    s.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="url(#gf0)" stroke="{STROKE[colors[0]]}" '
             f'stroke-width="2.2"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="{colors[0]}" '
             f'stroke-opacity=".3"><animate attributeName="r" values="62;70;62" dur="3.2s" '
             f'repeatCount="indefinite"/></circle>')
    cl = wrap(center, 6, 2)
    for i, ln in enumerate(cl):
        s.append(f'<text x="{cx}" y="{cy + i*18 - (len(cl)-1)*9 + 5}" font-size="15" '
                 f'font-weight="700" fill="{KEY}" text-anchor="middle">{esc(ln)}</text>')

    import math
    n = len(parts)
    for i, (label, desc) in enumerate(parts[:6]):
        a = -math.pi / 2 + (2 * math.pi * i) / n
        rr = 128 if n <= 4 else 138
        px = cx + rr * math.cos(a)
        py = cy + rr * math.sin(a) * 0.78
        c = colors[i % len(colors)]
        delay = 0.2 + i * 0.15
        s.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="26" fill="url(#gf{i%5})" '
                 f'stroke="{STROKE[c]}" stroke-width="1.8">'
                 f'<animate attributeName="opacity" from="0" to="1" dur=".5s" '
                 f'begin="{delay:.2f}s" fill="freeze"/></circle>')
        ls = wrap(label, 4, 2)
        for j, ln in enumerate(ls):
            s.append(f'<text x="{px:.0f}" y="{py + j*15 - (len(ls)-1)*7 + 4:.0f}" font-size="12" '
                     f'font-weight="700" fill="{KEY}" text-anchor="middle">{esc(ln)}</text>')
        # 连线到中心
        s.append(f'<line x1="{cx + 62*math.cos(a):.0f}" y1="{cy + 62*math.sin(a)*0.78:.0f}" '
                 f'x2="{px - 26*math.cos(a):.0f}" y2="{py - 26*math.sin(a)*0.78:.0f}" '
                 f'stroke="{c}" stroke-width="1.6" opacity=".65" stroke-dasharray="5 4">'
                 f'<animate attributeName="stroke-dashoffset" from="18" to="0" dur="1.3s" '
                 f'repeatCount="indefinite"/></line>')
        if desc:
            s.append(f'<text x="{px:.0f}" y="{py + 40:.0f}" font-size="11" fill="{TEXT}" '
                     f'opacity=".8" text-anchor="middle">{esc(wrap(desc,10,1)[0])}</text>')

    return shell("".join(s), title=title, subtitle=subtitle, colors=colors,
                 legend_items=[(colors[i % len(colors)], parts[i][0]) for i in range(min(n, 5))])


# ---------------------------------------------------------------- 模板 5：阶梯进程
def steps(items, title=None, subtitle=None):
    """阶梯上升：步骤推进 / 层级递进，适合方法步骤、能力层级"""
    n = len(items)
    colors = PALETTE[:max(3, min(5, n))]
    s = []
    left, base = 76, H - 92
    stepw = (W - left - 150) / max(1, n)
    sth = 46
    for i, (label, desc) in enumerate(items[:5]):
        x = left + i * stepw
        y = base - i * sth
        c = colors[i % len(colors)]
        delay = 0.15 + i * 0.16
        s.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{stepw-16:.0f}" height="{sth-8}" rx="8" '
                 f'fill="url(#gf{i%5})" stroke="{STROKE[c]}" stroke-width="1.8">'
                 f'<animate attributeName="opacity" from="0" to="1" dur=".5s" '
                 f'begin="{delay:.2f}s" fill="freeze"/></rect>')
        s.append(f'<text x="{x+16:.0f}" y="{y+20:.0f}" font-size="13" font-weight="700" '
                 f'fill="{KEY}">{i+1}. {esc(wrap(label,9,1)[0])}</text>')
        if desc:
            s.append(f'<text x="{x+16:.0f}" y="{y+34:.0f}" font-size="11" fill="{TEXT}" '
                     f'opacity=".82">{esc(wrap(desc,13,1)[0])}</text>')
        if i > 0:
            s.append(f'<path d="M{x-10:.0f} {y+sth-14:.0f} q 8 -10 14 -18" stroke="{DATA}" '
                     f'stroke-width="1.6" fill="none" marker-end="url(#ar2)" opacity=".8"/>')

    return shell("".join(s), title=title, subtitle=subtitle, colors=colors,
                 legend_items=[(colors[i % len(colors)], f"第{i+1}步 {items[i][0]}")
                               for i in range(min(n, 4))])
