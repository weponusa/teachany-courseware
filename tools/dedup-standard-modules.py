#!/usr/bin/env python3
"""去重复的标准模块块（知识图谱 / AI 学伴）。

病灶
----
课件里同一个标准模块出现两份：
  ① 页内模块：`<section class="slide-page" data-page-type="knowledge-graph">` / `"ai-tutor"`
  ② 容器外的静态块（历史注入残留）：
       `<section class="section" id="knowledge-graph" ...><div data-teachany-kg=…></div></section>`
       `<section class="ta-standard-section" id="teachany-ai-tutor-card" ...><div data-teachany-tutor-card></div></section>`
两份都会被 JS 渲染 → 页面上看到两个图谱 / 两个学伴入口。

做法
----
保留**页内**模块（v2 标准位置），删除容器外的静态重复块；
若页内容器是空的、而静态块里有 `<canvas class="tkg-fallback-canvas">` 这类无 JS 兜底，
先把兜底内容搬进页内容器再删静态块。

安全网：标签平衡不得变差 + 官方质检闸门（错误数不得增加）+ 逐课报告。

用法:
  python3 tools/dedup-standard-modules.py --from-list /tmp/dup-modules.txt --list
  python3 tools/dedup-standard-modules.py --all-migrated --apply
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402


def balanced_block(s, start, tag):
    """返回从 start 处 <tag ...> 起的整块（含闭合）。"""
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    if not m0:
        return None
    i = start + m0.end()
    d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return s[start:i + mm.end()]
    return None


def strip_scripts(h):
    return re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', h, flags=re.S | re.I)


def container_spans(html, attr):
    """返回所有真实模块容器（含 tag 名与区间），剔除 script/style 内的提及。"""
    out = []
    for m in re.finditer(r'<([a-z]+)[^>]*\b%s\b[^>]*>' % attr, html, re.I):
        end_m = re.search(r'</%s>' % m.group(1), html[m.start():], re.I)
        end = m.start() + (end_m.end() if end_m else len(m.group(0)))
        out.append((m.start(), end, m.group(1)))
    return out


def in_script(html, pos):
    """pos 是否落在 script/style 块内。"""
    for m in re.finditer(r'<(script|style)\b[^>]*>', html, re.I):
        close = re.search(r'</%s>' % m.group(1), html[m.end():], re.I)
        if close and m.end() <= pos <= m.end() + close.end():
            return True
    return False


def enclosing_section(html, pos):
    """返回包住 pos 的最小 <section> 区间（若没有则 None）。"""
    best = None
    for m in re.finditer(r'<section[^>]*>', html[:pos], re.I):
        blk = balanced_block(html, m.start(), 'section')
        if blk and m.start() <= pos < m.start() + len(blk):
            best = (m.start(), m.start() + len(blk), blk)
    return best


def dedup_module(html, module):
    """真实容器数 > 1 → 择优保留一个，删除其余（连同其外层 section）。
    择优：① 在 doc 的模块页里（data-page-type=模块 / data-tts 含模块名）最优；
          ② 在 #slide-container 内次之；③ 带无 JS 兜底（canvas）加分；④ 越靠前越好。
    """
    attr = 'data-teachany-kg' if module == 'knowledge-graph' else 'data-teachany-tutor-card'
    kind = 'knowledge-graph' if module == 'knowledge-graph' else 'ai-tutor'

    cont = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
    if not cont:
        # 无分页壳（老式演示课件）：不做「容器内/外」判断，直接按择优逻辑去重
        o = c = 0
    else:
        o = cont.end()
        c = len(html)
    if cont:
        d = 1
        for mm in re.finditer(r'<(/?)div\b[^>]*(/?)>', html[o:], re.I):
            if mm.group(1):
                d -= 1
            elif not mm.group(2):
                d += 1
            if d == 0:
                c = o + mm.start()
                break

    def spans_of(h):
        return [sp for sp in container_spans(h, attr) if not in_script(h, sp[0])]

    spans = spans_of(html)
    if len(spans) <= 1:
        return html, 'single-container(%d)' % len(spans)

    scored = []
    for (s0, e0, tag) in spans:
        score = 0
        sec = enclosing_section(html, s0)
        sec_txt = sec[2][:400] if sec else ''
        # ★ 内容优先：保留「有真实内容」的模块，删掉注入的空壳
        text_len = len(re.findall(r'[^\s]', re.sub(r'<[^>]+>', '', html[s0:e0])))
        if text_len >= 30:
            score += 50
        elif text_len >= 8:
            score += 20
        # 模块页/模块标签契合
        if ('data-page-type="%s"' % kind) in sec_txt or ('data-tts="%s"' % kind) in sec_txt \
           or ('id="%s"' % kind) in sec_txt or ('id="knowledge-graph"' in sec_txt and kind == 'knowledge-graph') \
           or ('id="teachany-ai-tutor-card"' in sec_txt and kind == 'ai-tutor'):
            score += 10
        if o <= s0 < c:
            score += 3
        if re.search(r'<canvas', html[s0:e0], re.I):
            score += 1
        scored.append((-score, s0, e0, tag, sec))
    scored.sort()
    keeper = scored[0]
    losers = scored[1:]

    # 兜底：把淘汰者里的 canvas 搬到保留者（若保留者为空）
    k_s, k_e, k_tag, k_sec = keeper[1], keeper[2], keeper[3], keeper[4]
    fallback = ''
    for (_n, s0, e0, _t, _sec) in losers:
        mcanvas = re.search(r'<canvas[^>]*>[\s\S]*?</canvas>', html[s0:e0], re.I)
        if mcanvas:
            fallback = mcanvas.group(0)
            break

    # 计算删除区间：优先删外层 section（但外层若包含 slide-page 就只删容器本身）
    targets = []
    for (_n, s0, e0, tag, sec) in losers:
        if sec and 'slide-page' not in sec[2][:300]:
            targets.append((sec[0], sec[1]))
        else:
            blk = balanced_block(html, s0, tag)
            if blk:
                targets.append((s0, s0 + len(blk)))
    if not targets:
        return html, 'no-target'
    # 合并重叠区间，逆序删除
    targets.sort()
    merged = []
    for (b0, b1) in targets:
        if merged and b0 <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b1))
        else:
            merged.append((b0, b1))
    for (b0, b1) in sorted(merged, reverse=True):
        html = html[:b0] + html[b1:]

    # 搬兜底
    moved = ''
    if fallback:
        spans2 = spans_of(html)
        if spans2:
            s2, e2, t2 = spans2[0]
            seg = html[s2:e2]
            if not re.sub(r'<[^>]+>', '', seg).strip():
                seg2 = seg.replace('></%s>' % t2, '>' + fallback + '</%s>' % t2, 1)
                html = html[:s2] + seg2 + html[e2:]
                moved = '+兜底搬运'

    remain = len(spans_of(html))
    if remain != 1:
        return html, '删除后容器数=%d，放弃' % remain
    return html, 'dedup(%d->1)%s' % (len(spans), moved)


def fix_course(f, module_list=('knowledge-graph', 'ai-tutor')):
    html = f.read_text(encoding='utf-8')
    orig = html
    actions = []
    for mod in module_list:
        html, act = dedup_module(html, mod)
        actions.append('%s:%s' % (mod, act))
    if html == orig:
        return {'cid': f.parent.name, 'skip': ';'.join(actions)}
    if imbalance(html) > imbalance(orig):
        return {'cid': f.parent.name, 'skip': '平衡变差'}
    return {'cid': f.parent.name, 'actions': actions, 'new': html}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-list', default='')
    ap.add_argument('--all-migrated', action='store_true')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--conc', type=int, default=1)   # 兼容参数（本工具是静态的）
    args = ap.parse_args()

    if args.from_list:
        cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    else:
        cids = [d.name for d in sorted((ROOT / 'community').iterdir()) if (d / 'index.html').is_file()]
    changed, skipped = [], []
    for cid in cids:
        f = ROOT / 'community' / cid / 'index.html'
        if not f.is_file():
            skipped.append({'cid': cid, 'skip': 'no file'}); continue
        r = fix_course(f)
        if r.get('new'):
            if args.apply:
                ok, why = apply_guarded(f, r['new'], cid)
                r['gate'] = why
                if not ok:
                    skipped.append(r); continue
            changed.append(r)
        else:
            skipped.append(r)
    print(f'处理 {len(cids)} 门：去重 {len(changed)} 门，跳过 {len(skipped)} 门（{"已写入" if args.apply else "干跑"}）')
    import collections
    print('动作统计:', collections.Counter(a for r in changed for a in r['actions']))
    for r in skipped[:8]:
        print('  跳过 %s: %s' % (r['cid'], r.get('skip')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
