#!/usr/bin/env python3
"""超长页拆分器 —— 「先量后拆」：浏览器实测每个顶层块高度 → 静态手术拆页。

为什么这么做
------------
迁移工具早期版本把兜底残留并进了「综合任务」页（页11 interactive 3.7~6.1x 视口），
还有不少 concept/quiz 页单页 2x+。手工拆一门课要半小时，274 门必须自动化。

三步走：
  --plan   浏览器（JS 关）逐课实测超长页里每个顶层块的 offsetHeight/视口高，
           贪心分组（组高 ≤ TARGET），产出拆分计划 plan.json
  --apply  静态手术：按计划在 HTML 里把页拆开（深度平衡扫描找块边界），
           校验：标签平衡 + 文本 100% 保留 + data-page-index 重排
  --verify 浏览器（JS 开）复测，确认无 >1.6x 页、无嵌套、无 JS 错误

用法:
  python3 tools/split-overlong-pages.py --plan   --scan /tmp/overlong.json --out /tmp/split-plan.json
  python3 tools/split-overlong-pages.py --apply  --plan-json /tmp/split-plan.json [--only cid1,cid2]
  python3 tools/split-overlong-pages.py --verify --scan /tmp/overlong.json
"""
import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8801'
TARGET = 1.35       # 每组目标高度（x 视口）
LIMIT = 1.6         # 超过即为超长页

# ---------------------------------------------------------------- plan 阶段
# 对每个超长页：枚举「可拆块」= slide-inner 的顶层子元素；若 slide-inner 只有
# 一个 wrapper 子元素，则取 wrapper 的子元素。单块 >TARGET 时下钻一层。
MEASURE_JS = r'''({pageIndex, target}) => {
  const c = document.getElementById('slide-container');
  const pages = [...c.querySelectorAll(':scope > .slide-page')];
  const page = pages[pageIndex];
  if (!page) return {err: 'no page'};
  const vh = c.clientHeight || 1;
  const inner = page.querySelector(':scope > .slide-inner') || page;

  // 顶层可拆块（下钻到「有多个子元素」的那一层）
  let chunks = [...inner.children];
  if (chunks.length === 1 && chunks[0].children.length > 1) {
    chunks = [...chunks[0].children];
  }
  // 单块超高的下钻一层（保留 wrapper 信息，apply 阶段克隆 wrapper）
  const out = [];
  chunks.forEach((ch, i) => {
    const h = ch.getBoundingClientRect().height / vh;
    const rec = {
      i, tag: ch.tagName.toLowerCase(),
      cls: (ch.className || '').slice(0, 60),
      h: +h.toFixed(3),
      head: (ch.outerHTML || '').slice(0, 120),
      sub: null,
    };
    if (h > target && ch.children.length > 1) {
      rec.sub = [...ch.children].map((s, j) => ({
        j, tag: s.tagName.toLowerCase(),
        cls: (s.className || '').slice(0, 60),
        h: +(s.getBoundingClientRect().height / vh).toFixed(3),
        head: (s.outerHTML || '').slice(0, 120),
      }));
    }
    out.push(rec);
  });
  return {pageH: +(page.scrollHeight / vh).toFixed(2), chunks: out};
}'''


def group_chunks(chunks, target):
    """贪心把连续块分成若干组，每组高度 ≤ target。返回 list[list[chunk]]。
    带 sub 的块在组内视为不可再分（简化：整块进组；只有单块超限时才用 sub 拆分）。"""
    groups = []
    cur, cur_h = [], 0.0
    for ch in chunks:
        h = max(ch['h'], 0.05)
        if cur and cur_h + h > target:
            groups.append(cur)
            cur, cur_h = [], 0.0
        cur.append(ch)
        cur_h += h
    if cur:
        groups.append(cur)
    return groups


def make_plan(scan_path, out_path, conc=6, only=None):
    data = json.loads(Path(scan_path).read_text(encoding='utf-8'))
    bad = [r for r in data if r.get('over')]
    if only:
        bad = [r for r in bad if r['cid'] in only]
    print(f'规划 {len(bad)} 门课件的拆分方案…', flush=True)

    async def run():
        from playwright.async_api import async_playwright
        plans = []
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(conc)
            done = [0]

            async def one(rec):
                cid, base = rec['cid'], rec.get('base', 'community')
                async with sem:
                    # JS 关：量的是静态内容的真实高度（避免 KG/学伴渲染干扰）
                    ctx = await browser.new_context(
                        viewport={'width': 1280, 'height': 800}, java_script_enabled=False)
                    pg = await ctx.new_page()
                    plan = {'cid': cid, 'base': base, 'splits': []}
                    try:
                        await pg.goto(f'{BASE}/{base}/{cid}/', wait_until='load', timeout=20000)
                        await pg.wait_for_timeout(600)
                        for o in rec['over']:
                            r = await pg.evaluate(
                                MEASURE_JS, {'pageIndex': o['page'] - 1, 'target': TARGET})
                            if r.get('err') or len(r.get('chunks', [])) < 2:
                                plan['splits'].append({'page': o['page'], 'height': o['height'],
                                                       'reason': r.get('err') or '块数<2，不可拆',
                                                       'groups': None})
                                continue
                            groups = group_chunks(r['chunks'], TARGET)
                            plan['splits'].append({'page': o['page'], 'height': o['height'],
                                                   'measured': r['pageH'],
                                                   'chunks': r['chunks'],
                                                   'groups': [[c['i'] for c in g] for g in groups]})
                    except Exception as e:  # noqa: BLE001
                        plan['error'] = str(e)[:120]
                    finally:
                        await ctx.close()
                    plans.append(plan)
                    done[0] += 1
                    if done[0] % 20 == 0:
                        print(f"  {done[0]}/{len(bad)}", flush=True)

            await asyncio.gather(*(one(r) for r in bad))
            await browser.close()
        return plans

    plans = asyncio.run(run())
    Path(out_path).write_text(json.dumps(plans, ensure_ascii=False, indent=1), encoding='utf-8')
    doable = [p for p in plans if any(s.get('groups') and len(s['groups']) > 1 for s in p['splits'])]
    print(f'完成：{len(plans)} 门，可拆 {len(doable)} 门 → {out_path}')


# ---------------------------------------------------------------- apply 阶段
def balanced_span(s, start, tag):
    """从 start 的 <tag ...> 起做深度平衡，返回 (end_index)。"""
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    if not m0:
        raise ValueError(f'not a <{tag}> at {start}')
    i = start + m0.end()
    depth = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            depth -= 1
        elif not mm.group(2):
            depth += 1
        if depth == 0:
            return i + mm.end()
    raise ValueError(f'unbalanced <{tag}> at {start}')


def page_spans(html):
    """返回 [(start, end, tag_str)] 顶层 slide-page 区间（按文档序，end=下一页start）。"""
    ms = [(m.start(), m.group(0)) for m in
          re.finditer(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', html)]
    out = []
    for i, (pos, tag) in enumerate(ms):
        end = ms[i + 1][0] if i + 1 < len(ms) else len(html)
        out.append((pos, end, tag))
    return out


def top_chunks(body):
    """与 MEASURE_JS 同构的静态版：取 slide-inner 的顶层子元素；
    只有一个 wrapper 时取其子元素。返回 [(start, end, tag, cls)]（相对 body 偏移）。"""
    mi = re.search(r'<div class="slide-inner">', body)
    container_start = mi.end() if mi else re.match(r'<section[^>]*>', body).end()
    container_tag = 'div' if mi else 'section'

    def children_of(pos):
        """枚举从 pos 开始的顶层子元素（div/section/figure/h2/table/ul 等块级）。"""
        out = []
        depth = 0
        i = pos
        tag_re = re.compile(r'<(/?)(div|section|figure|table|ul|ol|article|aside|h[1-6]|p|form|details)\b[^>]*(/?)>', re.I)
        for m in tag_re.finditer(body, pos):
            closing, tag, selfc = m.group(1), m.group(2).lower(), m.group(3)
            if not closing and not selfc:
                if depth == 0:
                    end = balanced_span(body, m.start(), tag)
                    out.append((m.start(), end, tag, body[m.start():m.end()]))
                    i = end
                    # 跳到 end 后继续
                    return out + children_of(end)
                depth += 1
            elif closing:
                depth -= 1
                if depth < 0:
                    break
        return out

    chunks = children_of(container_start)
    if len(chunks) == 1:
        s, e, tag, _raw = chunks[0]
        sub_open = re.match(r'<%s\b[^>]*>' % tag, body[s:], re.I)
        subs = children_of(s + sub_open.end())
        if len(subs) > 1:
            return subs, (s, tag, _raw)   # 返回子块 + wrapper 信息
    return chunks, None


def apply_plan(plan_path, only=None, dry=False):
    plans = json.loads(Path(plan_path).read_text(encoding='utf-8'))
    changed, skipped = [], []
    for p in plans:
        cid, base = p['cid'], p.get('base', 'community')
        if only and cid not in only:
            continue
        splits = [s for s in p['splits'] if s.get('groups') and len(s['groups']) > 1]
        if not splits:
            skipped.append((cid, '无可拆组'))
            continue
        f = ROOT / base / cid / 'index.html'
        html = f.read_text(encoding='utf-8')
        orig_html = html
        pages = page_spans(html)
        # 页号从大到小处理，避免位移
        ok = True
        for sp in sorted(splits, key=lambda x: -x['page']):
            pno = sp['page']
            if pno > len(pages):
                skipped.append((cid, f'页{pno}不存在')); ok = False; break
            ps, pe, ptag = pages[pno - 1]
            body = html[ps:pe]
            try:
                chunks, wrapper = top_chunks(body)
            except Exception as e:  # noqa: BLE001
                skipped.append((cid, f'页{pno}结构异常: {e}')); ok = False; break
            if len(chunks) < max(len(sp['groups']), 2):
                skipped.append((cid, f'页{pno}静态块数({len(chunks)})与计划不符')); ok = False; break
            # 静态块与计划块按序对齐（数量不等时按高度比例对齐——保守：要求数量一致）
            if len(chunks) != len(sp['chunks']):
                skipped.append((cid, f'页{pno}块数不一致 静态{len(chunks)} vs 浏览器{len(sp["chunks"])}'))
                ok = False; break
            # 构造新页
            new_pages = []
            # 页 tag 属性：克隆原 tag，改 data-tsh 加序号
            base_tsh = re.search(r'data-tsh="([^"]*)"', ptag)
            for gi, grp in enumerate(sp['groups']):
                first, last = grp[0], grp[-1]
                seg = body[chunks[first][0]:chunks[last][1]]
                tag = ptag
                if base_tsh and len(sp['groups']) > 1:
                    suffix = '①②③④⑤⑥'[gi] if gi < 6 else str(gi + 1)
                    tag = ptag.replace(base_tsh.group(0),
                                       f'data-tsh="{base_tsh.group(1)}·{suffix}"')
                if wrapper:
                    wtag = wrapper[2]
                    new_body = (tag + '\n<div class="slide-inner">' + wtag + '\n'
                                + seg + f'\n</{wrapper[1]}>\n</div>\n</section>\n')
                else:
                    new_body = tag + '\n<div class="slide-inner">\n' + seg + '\n</div>\n</section>\n'
                new_pages.append(new_body)
            html = html[:ps] + ''.join(new_pages) + html[pe:]
            pages = page_spans(html)   # 重建索引
        if not ok:
            continue
        # 校验 1：文本保留（拆分不应丢任何文本）
        def text_blocks(s):
            s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
            t = re.sub(r'<[^>]+>', '', s)
            return re.sub(r'\s+', '', t)
        if text_blocks(html) != text_blocks(orig_html):
            skipped.append((cid, '文本不一致，放弃')); continue
        # 校验 2：标签平衡
        bal = all(
            len(re.findall(r'<%s\b' % t, html)) == len(re.findall(r'</%s>' % t, html))
            for t in ('section', 'div', 'figure'))
        if not bal:
            skipped.append((cid, '标签不平衡，放弃')); continue
        # 重排 data-page-index
        n = [0]
        html = re.sub(r'data-page-index="\d+"',
                      lambda m: 'data-page-index="%d"' % (n.__setitem__(0, n[0] + 1) or n[0] - 1),
                      html)
        if not dry:
            f.write_text(html, encoding='utf-8')
        changed.append((cid, len(splits)))
    print(f'apply 完成：改造 {len(changed)} 门，跳过 {len(skipped)} 门')
    for cid, why in skipped[:15]:
        print(f'  跳过 {cid}: {why}')
    return changed, skipped


# ---------------------------------------------------------------- verify 阶段
def verify(scan_path, conc=6):
    data = json.loads(Path(scan_path).read_text(encoding='utf-8'))
    cids = [(r.get('base', 'community'), r['cid']) for r in data if r.get('over')]

    async def run():
        from playwright.async_api import async_playwright
        out = []
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(conc)

            async def one(item):
                base, cid = item
                async with sem:
                    ctx = await browser.new_context(viewport={'width': 1280, 'height': 800})
                    pg = await ctx.new_page()
                    errs = []
                    pg.on('pageerror', lambda e: errs.append(str(e)))
                    try:
                        await pg.goto(f'{BASE}/{base}/{cid}/', wait_until='load', timeout=20000)
                        await pg.wait_for_timeout(900)
                        r = await pg.evaluate(r'''() => {
                          const c = document.getElementById('slide-container');
                          const pages = [...c.querySelectorAll(':scope > .slide-page')];
                          const vh = c.clientHeight || 1;
                          const hs = pages.map(p => +(p.scrollHeight/vh).toFixed(2));
                          return {pages: pages.length, dots: document.querySelectorAll('.sidenav-dot').length,
                                  nested: c.querySelectorAll('.slide-page').length - pages.length,
                                  maxH: Math.max(...hs)};
                        }''')
                        r['cid'] = cid
                        r['jserr'] = len(errs)
                        out.append(r)
                    except Exception as e:  # noqa: BLE001
                        out.append({'cid': cid, 'error': str(e)[:100]})
                    finally:
                        await ctx.close()

            await asyncio.gather(*(one(c) for c in cids))
            await browser.close()
        return out

    res = asyncio.run(run())
    still = [r for r in res if r.get('maxH', 0) > LIMIT]
    nest = [r for r in res if r.get('nested')]
    jserr = [r for r in res if r.get('jserr')]
    print(f'复测 {len(res)} 门：仍超长 {len(still)}，嵌套 {len(nest)}，JS错误 {len(jserr)}')
    for r in sorted(still, key=lambda x: -x['maxH'])[:20]:
        print(f"  {r['cid']:42s} {r['maxH']}x 页数{r['pages']}")
    Path('/tmp/split-verify.json').write_text(
        json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan', action='store_true')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--scan', default='/tmp/overlong.json')
    ap.add_argument('--out', default='/tmp/split-plan.json')
    ap.add_argument('--plan-json', default='/tmp/split-plan.json')
    ap.add_argument('--only', default='')
    ap.add_argument('--conc', type=int, default=6)
    ap.add_argument('--dry', action='store_true')
    args = ap.parse_args()
    only = set(x for x in args.only.split(',') if x)
    if args.plan:
        make_plan(args.scan, args.out, args.conc, only or None)
    elif args.apply:
        apply_plan(args.plan_json, only or None, args.dry)
    elif args.verify:
        verify(args.scan, args.conc)
    else:
        ap.print_help()


if __name__ == '__main__':
    sys.exit(main())
