#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""为「可视化单元不足」的课件生成一张真实、可读的矢量知识结构图并嵌入。

为什么这么做
------------
B-3a 要求「去重内容图 + 互动可视模块 ≥ 3 且至少 1 张嵌入内容图」。这批课件
（122 门）普遍是 1 张 hero + 1 个标准知识图谱 = 2，差 1 个单元。
它们 assets/ 里那些没用上的位图（concept-diagram.webp 等）经逐张查看，
中文基本是乱码（"开头见山""开举筒""重文的题写"），不能拿来充数。

所以改为：从课件**自身内容**（模块标题 + 要点句）生成一张矢量知识结构图
（`assets/knowledge-map.svg`），以 `<img src>` 嵌入。
- 文字全部取自课件原文 → 不会出现乱码，也不会凭空编造知识点；
- 矢量图可无损缩放、可打印，比位图更适合当结构图；
- 自带 unique id、无外部引用，独立文件可被浏览器正常缓存。

用法:
  python3 tools/gen-course-diagram.py --from-list /tmp/viz.txt --limit 2
  python3 tools/gen-course-diagram.py --from-list /tmp/viz.txt --apply
"""
from __future__ import annotations

import argparse
import html as htmlmod
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded  # noqa: E402

SKIP_ID = re.compile(
    r'(hero|cover|objectives|pretest|posttest|summary|knowledge-graph|kg-|ai-tutor|audio|anchor|'
    r'^s-pretest|^s-posttest|^s-abt|^s-error|^s-memory|error-clinic|error-prone|ai-interaction|'
    r'abt|tiered|feedback|reflection|nav|footer)', re.I)
SKIP_TITLE = re.compile(r'(学习目标|前测|后测|小结|知识图谱|AI 学伴|语音导学|记忆锚点|易错|真题练习|'
                        r'为什么要学|带着问题|知识结构|拓展|迁移挑战|概念检测|探究记录|学习路径|'
                        r'知识全景|综合|总结)')
SKIP_PT = re.compile(r'^(And|But|Therefore)\s*[·:：]')
CJK = re.compile(r'[\u4e00-\u9fff]')
URL_BIT = re.compile(r'https?://|www\.|\.edu\b|\.org\b|\.com\b|PhET|GeoGebra', re.I)
LABEL_ONLY = re.compile(r'^(即练|练习|小练|小结|提示|注意|思考|活动|任务|拓展|示例|例子|情境|导入|'
                        r'探究|讨论|总结|回顾|要点|重点|难点|目标|方法|步骤|定义|概念|例题|'
                        r'探究记录|概念检测|学习路径|巩固|检测|自测|作业)$')
META_PT = re.compile(r'（?ABT|^深层理解|^镜头[一二三四五六七八九十]|^用一个|^以一个|^反直觉|'
                     r'^黄金规则$|^核心讲解|^核心要点$|^重点提示$|^方法点拨$|^自主探究$|'
                     r'^你知道吗$|^想一想$|^小结一下$|^马上练|练一题|你已经知道|^[A-D]\s*[·•]|'
                     r'^Step\s*\d|^第[一二三四五六七八九十]步$')

FONT = "system-ui,-apple-system,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif"


def esc(s: str) -> str:
    return htmlmod.escape(s, quote=True)


def text_w(s: str, px: float) -> float:
    """粗略字宽：CJK/全角 ≈ 1em，其余 ≈ 0.55em。"""
    w = 0.0
    for ch in s:
        o = ord(ch)
        w += px if (o > 0x2E80) else px * 0.55
    return w


def wrap(s: str, max_px: float, px: float, max_lines: int = 2):
    lines, cur = [], ''
    for ch in s:
        if text_w(cur + ch, px) > max_px and cur:
            lines.append(cur)
            cur = ch
            if len(lines) == max_lines:
                break
        else:
            cur += ch
    if len(lines) < max_lines and cur:
        lines.append(cur)
    if len(lines) == max_lines:
        # 没放完 → 末行加省略号（回退 1 字给省略号）
        rest_at = sum(len(x) for x in lines)
        if rest_at < len(s):
            last = lines[-1]
            while last and text_w(last + '…', px) > max_px:
                last = last[:-1]
            lines[-1] = last.rstrip('，。、；：') + '…'
    return lines


def strip_tags(s: str) -> str:
    s = re.sub(r'<(script|style)\b.*?</\1>', ' ', s, flags=re.S | re.I)
    s = re.sub(r'<[^>]+>', ' ', s)
    s = htmlmod.unescape(s)
    return re.sub(r'\s+', ' ', s).strip()


def course_title(h: str) -> str:
    m = re.search(r'<title>(.*?)</title>', h, re.S)
    if not m:
        return '本课知识结构'
    t = strip_tags(m.group(1))
    return re.split(r'\s*[·|｜]\s*', t)[0].strip() or '本课知识结构'


def accent_of(h: str) -> str:
    for var in ('--accent', '--primary'):
        m = re.search(re.escape(var) + r'\s*:\s*([#a-zA-Z0-9(),.\s%]+)[;}]', h)
        if m:
            v = m.group(1).strip().split()[0]
            if re.fullmatch(r'#[0-9a-fA-F]{3,8}', v):
                return v
    return '#2563eb'


QUIZ_PRED = re.compile(r'data-answer\s*=|class="[^"]*(?:tu-fb|tu-opts|tu-opt|tu-fill|module-check|'
                       r'quiz-|exam-|question-|choice-)', re.I)


def drop_blocks(html: str, tag: str, pred) -> str:
    """按深度平衡删掉整块 <tag>…</tag>（只在开标签命中 pred 时）。

    注意：所有偏移量必须换算回原串（re.search 作用在 html[i:] 上）。
    """
    open_re = re.compile(r'<%s\b[^>]*>' % tag, re.I)
    any_re = re.compile(r'<(/?)%s\b[^>]*>' % tag, re.I)
    out, i = [], 0
    while True:
        m = open_re.search(html, i)
        if not m:
            out.append(html[i:])
            break
        if not pred(m.group(0)):
            out.append(html[i:m.end()])
            i = m.end()
            continue
        depth, j = 1, m.end()
        for t in any_re.finditer(html, j):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                j = t.end()
                break
        else:
            out.append(html[i:])
            break
        out.append(html[i:m.start()])
        i = j
    return ''.join(out)


def strip_quiz(body: str) -> str:
    """摘掉自测/选项块（带 data-answer 的 tu-q、选项容器、答案折叠），剩下的才是正文。"""
    body = drop_blocks(body, 'div', lambda t: bool(QUIZ_PRED.search(t)))
    body = drop_blocks(body, 'section', lambda t: bool(QUIZ_PRED.search(t)))
    body = drop_blocks(body, 'details', lambda t: True)
    return body


def clean_title(s: str) -> str:
    s = re.sub(r'^[^\w\u4e00-\u9fff]+', '', s).strip()
    return re.sub(r'\s+', ' ', s)


def clean_point(text: str, cap: int) -> str:
    """压成一句干净短要点：去掉 emoji/编号/标签前缀，优先取长度合适的分句。"""
    t = re.sub(r'\s+', ' ', text).strip()
    t = re.sub(r'^[^\w\u4e00-\u9fff]+', '', t)
    t = re.sub(r'^\d+[.、)）]\s*', '', t)
    for _ in range(2):
        t2 = re.sub(r'^[\u4e00-\u9fffA-Za-z]{2,8}\s*[:：]\s*', '', t)
        if t2 == t:
            break
        t = t2
    frags = [f.strip() for f in re.split(r'[。！？；]', t) if f.strip()]
    for f in frags:
        if 6 <= len(f) <= cap:
            return f
    s = frags[0] if frags else t
    for x in [y.strip() for y in re.split(r'[，：]', s) if y.strip()]:
        if 6 <= len(x) <= cap:
            return x
    return s[: cap - 1].rstrip('，。、；：') + ('…' if len(s) > cap else '')


def module_sections(h: str, limit: int = 5):
    """返回 [(标题, 正文)]。

    v2 幻灯片式课件里，同一模块常被拆成「外层包裹 + 内层模块 section」，
    导致同一标题出现两次（外层只剩几十字节）。所以：
      带标题的 section 开新条目；无标题的并入上一条目；同名条目合并正文。
    """
    order, bucket = [], {}
    for m in re.finditer(r'<section\b([^>]*)>(.*?)(?=<section\b|</body>)', h, re.S):
        attrs, body = m.group(1), m.group(2)
        if 'knowledge-map.svg' in body:      # 本工具自己插入的结构图块，不参与抽取
            continue
        sid_m = re.search(r'id="([^"]+)"', attrs)
        sid = sid_m.group(1) if sid_m else ''
        hd = re.search(r'<h[12][^>]*>(.*?)</h[12]>', body, re.S)
        if not hd:
            if order and order[-1]:
                bucket[order[-1]] += body
            continue
        title = clean_title(strip_tags(hd.group(1)))
        if not (4 <= len(title) <= 34) or SKIP_ID.search(sid or '') or SKIP_TITLE.search(title):
            order.append('')                # 占位：承接后续无标题 section，末尾丢弃
            continue
        if title not in bucket:
            bucket[title] = ''
            order.append(title)
        bucket[title] += body
    return [(t, strip_quiz(bucket[t])) for t in order if t][:limit]


def points_for(body: str, cap: int, want: int = 3):
    pts = []
    for x in re.findall(r'<h[34][^>]*>(.*?)</h[34]>', body, re.S):
        txt = clean_point(clean_title(strip_tags(x)), min(cap, 22))
        if (4 <= len(txt) <= min(cap, 22) and txt not in pts and CJK.search(txt)
                and not LABEL_ONLY.match(txt) and not META_PT.search(txt)
                and not txt.endswith(('？', '?'))):
            pts.append(txt)
        if len(pts) >= want:
            return pts
    for x in re.findall(r'<li\b[^>]*>(.*?)</li>', body, re.S) + \
             re.findall(r'<p\b[^>]*>(.*?)</p>', body, re.S):
        txt = strip_tags(x)
        if (SKIP_PT.match(txt) or not CJK.search(txt) or LABEL_ONLY.match(txt)
                or META_PT.search(txt) or URL_BIT.search(txt)):
            continue
        if txt.endswith(('？', '?')) or len(txt) < 10:
            continue
        c = clean_point(txt, cap)
        if len(c) >= 6 and c not in pts:
            pts.append(c)
        if len(pts) >= want:
            break
    return pts


def modules_of(h: str, limit: int = 5, cap: int = 24):
    out = []
    for t, body in module_sections(h, limit):
        pts = points_for(body, cap)
        if pts:
            out.append((t, pts))
    return out


def layout(secs, W=1360, pad=44, label_px=16.0, pt_px=13.5):
    n = len(secs)
    col_w = (W - pad * 2) / n
    box_w = col_w - 18
    inner = box_w - 34
    cap = max(10, int((inner - 14) / pt_px) * 2 - 1)
    return col_w, box_w, inner, cap


def build_svg(cid: str, h: str):
    """返回知识结构图 SVG；素材不足（<2 个可用模块）时返回空串由调用方跳过。"""
    title = course_title(h)
    accent = accent_of(h)
    secs = module_sections(h, 5)
    for _ in range(3):
        if len(secs) < 2:
            return ''
        cap = layout(secs)[3]
        keep = [(t, b, points_for(b, cap)) for t, b in secs]
        keep = [(t, b, p) for t, b, p in keep if p]
        if len(keep) == len(secs) or len(keep) < 2:
            secs = [(t, b) for t, b, _p in keep]
            break
        secs = [(t, b) for t, b, _p in keep]
    mods = [(t, points_for(b, layout(secs)[3])) for t, b in secs]
    mods = [(t, p[:3]) for t, p in mods if p]
    if len(mods) < 2:
        return ''

    n = len(mods)
    col_w, box_w, inner, cap = layout(mods)
    label_px, pt_px = 16.0, 13.5
    top, W, pad = 128, 1360, 44
    title_lines = [wrap(m[0], inner, label_px, 2) for m in mods]
    pt_lines = [[wrap(p, inner - 14, pt_px, 2) for p in m[1][:3]] for m in mods]
    max_pt_lines = max((sum(len(x) for x in pl) for pl in pt_lines), default=1)
    head_h = 22 + (0 if max(len(t) for t in title_lines) == 1 else 22)
    card_h = head_h + 18 + max_pt_lines * 22 + 16
    H = top + card_h + 70

    uid = re.sub(r'[^a-zA-Z0-9]', '', cid)[:24] or 'x'
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'role="img" aria-label="{esc(title)} 知识结构图" font-family="{FONT}">',
        f'<defs><linearGradient id="kghead-{uid}" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity=".4"/>'
        f'</linearGradient></defs>',
        f'<rect width="{W}" height="{H}" rx="18" fill="#f8fafc"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="18" fill="none" stroke="{accent}" '
        f'stroke-opacity=".28" stroke-width="2"/>',
        f'<text x="{pad}" y="58" font-size="32" font-weight="800" fill="#0f172a">{esc(title)}</text>',
        f'<text x="{pad}" y="90" font-size="15" fill="#64748b">知识结构图 · 按本课模块与要点汇编</text>',
        f'<rect x="{pad}" y="104" width="92" height="4" rx="2" fill="url(#kghead-{uid})"/>',
    ]

    rail_y = 122
    cy = top
    cx0 = pad + col_w * 0 + col_w / 2
    cx1 = pad + col_w * (n - 1) + col_w / 2
    parts.append(f'<path d="M{W/2:.1f} {rail_y-14} L{W/2:.1f} {rail_y:.1f}" fill="none" '
                 f'stroke="{accent}" stroke-opacity=".45" stroke-width="2"/>')
    if n > 1:
        parts.append(f'<path d="M{cx0:.1f} {rail_y:.1f} L{cx1:.1f} {rail_y:.1f}" fill="none" '
                     f'stroke="{accent}" stroke-opacity=".45" stroke-width="2"/>')
    parts.append(f'<path d="M{W/2:.1f} {rail_y:.1f} L{cx0:.1f} {rail_y:.1f}" fill="none" '
                 f'stroke="{accent}" stroke-opacity=".45" stroke-width="2"/>')
    for i in range(n):
        cx = pad + col_w * i + col_w / 2
        parts.append(f'<path d="M{cx:.1f} {rail_y:.1f} L{cx:.1f} {cy-6:.1f}" fill="none" '
                     f'stroke="{accent}" stroke-opacity=".45" stroke-width="2"/>')
    for i, (mt, _pts) in enumerate(mods):
        cx = pad + col_w * i + col_w / 2
        bx = cx - box_w / 2
        parts.append(f'<rect x="{bx:.1f}" y="{cy}" width="{box_w:.1f}" height="{card_h}" rx="14" '
                     f'fill="#ffffff" stroke="{accent}" stroke-opacity=".35" stroke-width="2"/>')
        parts.append(f'<path d="M{bx+14:.1f} {cy} h{box_w-28:.1f} a14,14 0 0 1 14,14 v{head_h-14:.1f} '
                     f'h{-box_w:.1f} v{-(head_h-14):.1f} a14,14 0 0 1 14,-14 z" fill="{accent}" fill-opacity=".13"/>')
        for k, ln in enumerate(title_lines[i]):
            parts.append(f'<text x="{bx+17:.1f}" y="{cy+22+k*22:.1f}" font-size="{label_px}" '
                         f'font-weight="700" fill="#0f172a">{esc(ln)}</text>')
        ty = cy + head_h + 20
        for pl in pt_lines[i]:
            parts.append(f'<circle cx="{bx+16:.1f}" cy="{ty-5:.1f}" r="3.4" fill="{accent}" fill-opacity=".85"/>')
            for ln in pl:
                parts.append(f'<text x="{bx+28:.1f}" y="{ty:.1f}" font-size="{pt_px}" '
                             f'fill="#334155">{esc(ln)}</text>')
                ty += 22
    parts.append(f'<text x="{W-pad}" y="{H-24}" font-size="13" fill="#94a3b8" text-anchor="end">'
                 f'TeachAny · {esc(cid)}</text>')
    parts.append('</svg>')
    return '\n'.join(parts)


def figure(cid: str, title: str) -> str:
    return (
        '\n<section class="section ta-diagram-section" data-tts>\n'
        f'  <figure class="ta-standard-figure">\n'
        f'    <img src="./assets/knowledge-map.svg" alt="{esc(title)} 知识结构图：本课模块与要点关系" '
        f'loading="lazy" style="width:100%;height:auto;border-radius:16px">\n'
        f'    <figcaption>{esc(title)} · 知识结构图：把本课各模块与要点放在一张图上对照</figcaption>\n'
        f'  </figure>\n'
        '</section>\n')


def insert_figure(h: str, fig: str) -> str:
    """插到第一个模块 section 之前（没有就插到 </body> 前）。"""
    m = re.search(r'<section\b[^>]*id="(module-1|s-1|core-1)"', h)
    if m:
        return h[:m.start()] + fig + h[m.start():]
    m = re.search(r'<section\b[^>]*class="[^"]*\bsection\b', h)
    if m:
        k = h.find('<section', m.start() + 8)
        if k == -1:
            k = m.start()
        return h[:k] + fig + h[k:]
    i = h.rfind('</body>')
    return (h[:i] + fig + h[i:]) if i != -1 else h + fig


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-list', required=True)
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    if args.limit:
        cids = cids[: args.limit]

    ok = bad = 0
    for cid in cids:
        f = ROOT / 'community' / cid / 'index.html'
        if not f.is_file():
            print(f'  ✗ {cid}: 无 index.html')
            bad += 1
            continue
        h = f.read_text(encoding='utf-8')
        if 'assets/knowledge-map.svg' in h:
            continue
        svg = build_svg(cid, h)
        if not svg:                          # 素材不足 → 不写空图、不动 HTML
            bad += 1
            print(f'  ↷ {cid}: 可提取的模块不足 2 个，跳过')
            continue
        title = course_title(h)
        fig = figure(cid, title)
        new = insert_figure(h, fig)
        if not args.apply:
            out = ROOT / 'community' / cid / 'assets' / 'knowledge-map.svg'
            out.write_text(svg, encoding='utf-8')
            print(f'  试跑 {cid}: 模块 {len(modules_of(h))} 个，svg {len(svg)}B → {out.name}')
            ok += 1
            continue
        (ROOT / 'community' / cid / 'assets').mkdir(parents=True, exist_ok=True)
        (ROOT / 'community' / cid / 'assets' / 'knowledge-map.svg').write_text(svg, encoding='utf-8')
        good, why = apply_guarded(f, new, cid)
        if good:
            ok += 1
        else:
            bad += 1
            (ROOT / 'community' / cid / 'assets' / 'knowledge-map.svg').unlink(missing_ok=True)
            print(f'  ✗ {cid}: {why}')
    print(f'图已生成 {ok} 门，失败 {bad} 门' + ('' if args.apply else '（试跑，未写入 HTML）'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
