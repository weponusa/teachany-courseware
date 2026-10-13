#!/usr/bin/env python3
"""把课件**自带的、却没被引用的**插图嵌入页面，补齐「可视化单元不足」。

规则口径（validate-courseware.py B-3a）
    可视化单元 = 去重后的本地内容图（<img src> 指向本地、按路径去重）
              + 互动可视模块（原生 canvas / data-teachany-kg / data-teachany-map / PhET）
    要求：合计 ≥ 3 且至少 1 张嵌入内容图。

做法（只补真实素材，不造图）
    1. 在课件 assets/ 里找**未被 index.html 引用**的本地图片（svg/webp/png/jpg，>3KB）；
    2. 按语义优先级挑选（concept-diagram > process-diagram > section* > hero-infographic > 其他）；
       跳过 .pre-notext（中间产物）与已被引用的文件；
    3. 插入到最合适的页面：优先 concept/interactive 页；老式结构（无 slide-page）则找正文最厚的 section；
       SVG 会尝试从其内嵌文字生成图注，否则用中性图注（《课程名》+ 素材用途）；
    4. 安全网：标签平衡不得变差 + 官方质检闸门（错误数不得增加）+ 补齐后可视化单元数 ≥3 才写。

用法:
  python3 tools/embed-own-assets.py --from-list /tmp/vis-122.txt --list
  python3 tools/embed-own-assets.py --from-list /tmp/vis-122.txt --apply
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

# 复用官方校验器的可视化计数口径，保证「补完就达标」
sys.path.insert(0, str(ROOT / 'scripts'))
_spec = {}
exec(compile((ROOT / 'scripts' / 'validate-courseware.py').read_text(encoding='utf-8')
             .split('def check_baseline_quality')[0].replace(
                 "ROOT = Path(__file__).resolve().parents[1]", "ROOT = Path('%s')" % ROOT),
             'vc-head', 'exec'), _spec)
count_visualization_units = _spec['count_visualization_units']

NAME_RANK = [
    ('concept-diagram', 0), ('process-diagram', 1), ('section', 2),
    ('hero-infographic', 3), ('infographic', 4), ('diagram', 5), ('illustration', 6),
]
SKIP_PAT = re.compile(r'pre-notext|teachany-icon|\.pre-|logo', re.I)


def rank(name):
    low = name.lower()
    for kw, r in NAME_RANK:
        if kw in low:
            return r
    return 9


def unused_images(course_dir, html):
    used = {u.lstrip('./') for u in re.findall(r"<img[^>]+src=['\"]([^'\"]+)['\"]", html)}
    out = []
    for base in ('assets', 'assets/images', 'images'):
        d = course_dir / base
        if not d.is_dir():
            continue
        for f in sorted(d.iterdir()):
            if f.suffix.lower() not in ('.svg', '.webp', '.png', '.jpg', '.jpeg'):
                continue
            if SKIP_PAT.search(f.name) or f.stat().st_size < 3000:
                continue
            rel = f'{base}/{f.name}'
            if rel in used:
                continue
            out.append((rank(f.name), f.name, rel))
    out.sort()
    return [r for _k, _n, r in out]


def svg_caption(path):
    """从 SVG 内嵌文字里取一句可读图注（前 2 段中文短语）。"""
    try:
        t = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:  # noqa: BLE001
        return ''
    texts = [x.strip() for x in re.findall(r'>([\u4e00-\u9fff][^<>]{1,24})<', t)]
    texts = [x for x in texts if x not in ('核心概念示意', '过程机制示意', '知识结构图')]
    if texts:
        return '：'.join(texts[:2])
    return ''


def targets(html):
    """返回可插入的 (位置, 描述) 列表——优先概念页/正文厚 section。"""
    spans = []
    for m in re.finditer(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', html):
        s = m.start()
        blk = html[s:s + 200]
        t = (re.search(r'data-page-type="([^"]*)"', blk) or [None, ''])[1]
        spans.append(('page', t, s))
    if not spans:
        for m in re.finditer(r'<section\b[^>]*>', html):
            m0 = re.match(r'<section\b[^>]*>', html[m.start():], re.I)
            k = m.start() + m0.end(); d = 1; e = None
            for mm in re.finditer(r'<(/?)section\b[^>]*(/?)>', html[k:], re.I):
                if mm.group(1):
                    d -= 1
                elif not mm.group(2):
                    d += 1
                if d == 0:
                    e = k + mm.end(); break
            if e is None:
                continue
            blk = html[m.start():e]
            cjk = len(re.findall(r'[一-鿿]', re.sub(r'<[^>]+>', '', blk)))
            hid = (re.search(r'id="([^"]*)"', m0.group(0)) or [None, ''])[1]
            if cjk >= 200 and hid not in ('slide-container',):
                spans.append(('section', hid or 'section', m.start()))
    # 概念/互动页优先
    prio = {'concept': 0, 'interactive': 1, 'objectives': 2, 'summary': 3}
    spans.sort(key=lambda x: (prio.get(x[1], 5), x[2]))
    return [(s, f'{kind}:{name}') for kind, name, s in spans]


def insert_pos(html, start, kind):
    """在页面/section 结束前插入（找到该块的闭合标签前）。"""
    tag = 'section'
    m0 = re.match(r'<%s\b[^>]*>' % tag, html[start:], re.I)
    if not m0:
        return None
    k = start + m0.end(); d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, html[k:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return k + mm.start()          # 闭合标签起点
    return None


def course_name(course_dir, html):
    """课件显示名：优先 manifest.name，其次 <title> 里的《…》。"""
    mf = course_dir / 'manifest.json'
    if mf.is_file():
        try:
            import json as _json
            nm = (_json.loads(mf.read_text(encoding='utf-8')) or {}).get('name')
            if nm:
                return str(nm).strip()
        except Exception:  # noqa: BLE001
            pass
    m = re.search(r'<title>\s*《?([^》<|·]{2,24})', html)
    return (m.group(1).strip() if m else course_dir.name)


def caption_for(rel, name, course_dir):
    """按素材语义给可读图注（SVG 有内嵌文字时优先用）。"""
    base = rel.rsplit('/', 1)[-1].lower()
    if base.endswith('.svg'):
        t = svg_caption(course_dir / rel)
        if t:
            return f'《{name}》{t}'
    if 'concept-diagram' in base:
        return f'《{name}》核心概念示意图'
    if 'process-diagram' in base:
        return f'《{name}》过程机制示意图'
    if 'hero-infographic' in base or 'infographic' in base:
        return f'《{name}》知识结构图'
    if re.match(r'section\d', base):
        return f'《{name}》情境示意图（结合图意，说说你看到了什么）'
    if 'illustration' in base:
        return f'《{name}》示意插画'
    return f'《{name}》配套示意图'


def fix(course_dir, need=3):
    html = (course_dir / 'index.html').read_text(encoding='utf-8')
    disp = course_name(course_dir, html)
    imgs, units = count_visualization_units(html)
    total = len(imgs) + units
    if total >= need:
        return {'cid': course_dir.name, 'skip': f'already {total}'}
    cands = unused_images(course_dir, html)
    if not cands:
        return {'cid': course_dir.name, 'skip': 'no-unused-image'}
    tg = targets(html)
    if not tg:
        return {'cid': course_dir.name, 'skip': 'no-target'}
    want = need - total
    ins = []
    used_names = set()
    for i, (rel) in enumerate(cands[:want]):
        if i >= len(tg):
            break
        pos = insert_pos(html, tg[i][0], 'section')
        if pos is None:
            continue
        caption = caption_for(rel, disp, course_dir)
        fig = ('\n<figure class="ta-standard-figure" style="margin-top:16px">'
               f'<img src="./{rel}" alt="{caption}" loading="lazy">'
               f'<figcaption>{caption}</figcaption></figure>')
        ins.append((pos, fig))
        used_names.add(rel)
    if not ins:
        return {'cid': course_dir.name, 'skip': 'no-insert'}
    new = html
    for pos, fig in sorted(ins, reverse=True):
        new = new[:pos] + fig + new[pos:]
    if imbalance(new) > imbalance(html):
        return {'cid': course_dir.name, 'skip': 'balance-worse'}
    ai, au = count_visualization_units(new)
    if len(ai) + au < need:
        return {'cid': course_dir.name, 'skip': f'still {len(ai) + au}'}
    return {'cid': course_dir.name, 'inserted': len(ins), 'files': sorted(used_names),
            'units': f'{total}→{len(ai) + au}', 'new': new}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from-list', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    cids = [x.strip() for x in Path(args.from_list).read_text(encoding='utf-8').split() if x.strip()]
    ch, sk = [], []
    for cid in cids:
        d = ROOT / 'community' / cid
        if not (d / 'index.html').is_file():
            continue
        r = fix(d)
        if r.get('new'):
            if args.apply:
                ok, why = apply_guarded(d / 'index.html', r['new'], cid)
                r['gate'] = why
                if not ok:
                    sk.append(r); continue
            ch.append(r)
        else:
            sk.append(r)
    print('处理 %d 门：补齐 %d 门，跳过 %d 门（%s）' % (len(cids), len(ch), len(sk), '已写入' if args.apply else '干跑'))
    for r in ch[:12]:
        print('  %-38s 嵌入 %d 张 %s %s' % (r['cid'], r['inserted'], r['files'][:2], r['units']))
    for r in sk[:6]:
        print('  跳过 %s: %s' % (r['cid'], r.get('skip')))
    return 0


if __name__ == '__main__':
    sys.exit(main())
