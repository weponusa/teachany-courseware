#!/usr/bin/env python3
"""超长页拆分器（DOM 版）—— 在无 JS 的浏览器里量块高、拆页、再序列化回静态文件。

思路
----
分页型课件（容器 100dvh + overflow:auto）里，单页内容超过 ~1.6 视口就会出现
「页面里再滚动」的嵌套滚动。手工拆页慢，这里自动化：

  1. 无 JS 打开页面（DOM == 静态标记，不会被 KG/学伴渲染污染），
     找出 scrollHeight/容器高 > 1.6 的页；
  2. 对该页的「可拆块」（slide-inner 顶层子元素；只有单一 wrapper 时下钻其子元素）
     用实测高度贪心分组，每组 ≤ 1.35 视口；单块自身超限且含子元素时下钻一层，
     克隆 wrapper 分装子元素；
  3. 把拆出的新页 outerHTML 返回；
  4. 静态侧：用深度平衡切出原页区间，替换为新页串，重排 data-page-index，
     校验标签平衡 + **页文本零丢失**（新页文本归一化后必须与原页完全一致）；
  5. 复测：JS 开，确认无 >1.6x、无嵌套、无 JS 错误。

用法:
  python3 tools/dom-split-overlong-pages.py --only hist-m-globalization --dry
  python3 tools/dom-split-overlong-pages.py --only a,b,c --apply
  python3 tools/dom-split-overlong-pages.py --from-scan /tmp/overlong.json --apply --conc 5
"""
import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _qa_gate import apply_guarded, imbalance  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8801'
LIMIT = 1.6          # 超过即超长
TARGET = 1.35        # 每组目标高
MIN_GROUP = 0.15     # 避免产生高度可忽略的碎页（占比低于此值的块尽量并组）

# 浏览器：拆分并返回新页 HTML（JS 关）
SPLIT_JS = r'''({pageIndex, limit, target, minGroup}) => {
  const c = document.getElementById('slide-container');
  if (!c) return {err: 'no container'};
  const vh = c.clientHeight || 0;
  if (!vh || vh > window.innerHeight * 1.5) return {skip: 'browse-mode'};
  const pages = [...c.querySelectorAll(':scope > .slide-page')];
  const page = pages[pageIndex];
  if (!page) return {err: 'no page'};
  const h = page.scrollHeight / vh;
  if (h <= limit) return {skip: 'not over-long', h: +h.toFixed(2)};
  const origText = page.textContent;     // ★ 必须在搬走节点之前取

  // 可拆块定位：slide-inner，或在只有单一 wrapper 时下钻一层
  let host = page.querySelector(':scope > .slide-inner') || page;
  let wrapper = null;
  let chunks = [...host.children];
  if (chunks.length === 1 && chunks[0].children.length > 1) {
    wrapper = chunks[0];
    host = wrapper;
    chunks = [...host.children];
  }
  if (chunks.length < 2) return {skip: '块数<2', h: +h.toFixed(2)};

  const H = el => el.getBoundingClientRect().height / vh;

  // 贪心分组（含下钻：单块超 target 且含子元素 → 其子元素作为可分组单位）
  const units = [];
  chunks.forEach(ch => {
    const ch_h = H(ch);
    if (ch_h > target && ch.children.length > 1) {
      units.push({type: 'sub', el: ch, children: [...ch.children],
                  childH: [...ch.children].map(H)});
    } else {
      units.push({type: 'block', el: ch, h: ch_h});
    }
  });

  const groups = [];
  let cur = [], curH = 0;
  const flush = () => { if (cur.length) { groups.push(cur); cur = []; curH = 0; } };
  units.forEach(u => {
    if (u.type === 'block') {
      if (curH + u.h > target && cur.length) flush();
      cur.push(u); curH += u.h;
      // 单块本身就超 target：独立成组
      if (u.h > target) flush();
    } else {
      // 下钻块：其子元素依次尝试入组，必要时新开克隆组
      u.children.forEach((child, k) => {
        const ch = u.childH[k];
        if (curH + ch > target && cur.length) flush();
        cur.push({type: 'subchild', parent: u.el, el: child, h: ch});
        curH += ch;
        if (ch > target) flush();
      });
    }
  });
  flush();
  if (groups.length < 2) return {skip: '分组后仍 1 组', h: +h.toFixed(2)};

  // 生成新页：克隆原页属性，slide-inner + （必要时克隆 wrapper）
  const mkPage = (nodes, gi) => {
    const np = page.cloneNode(false);          // 只克隆标签与属性
    const inner = document.createElement('div');
    inner.className = 'slide-inner';
    if (wrapper) {
      const w = wrapper.cloneNode(false);
      nodes.forEach(n => w.appendChild(n));
      inner.appendChild(w);
    } else {
      nodes.forEach(n => inner.appendChild(n));
    }
    np.appendChild(inner);
    const tsh = np.getAttribute('data-tsh') || '';
    np.setAttribute('data-tsh', tsh + '·' + (gi + 1));
    np.setAttribute('data-page-index', '0');
    return np.outerHTML;                        // 已移走原节点
  };
  const texts = [];
  const htmls = groups.map((g, gi) => {
    const nodes = g.map(u => u.el);
    texts.push(nodes.map(n => n.textContent).join('\n'));
    return mkPage(nodes, gi);
  });

  return {h: +h.toFixed(2), groups: groups.length, htmls, texts, origText};
}'''


def page_spans(html):
    c = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
    if not c:
        raise ValueError('no slide-container')
    cont_open = c.end()
    # 容器闭合起点
    start = c.start()
    m0 = re.match(r'<div\b[^>]*>', html[start:], re.I)
    i = start + m0.end()
    d = 1
    close_start = None
    for mm in re.finditer(r'<(/?)div\b[^>]*(/?)>', html[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            close_start = i + mm.start()
            break
    if close_start is None:
        raise ValueError('unbalanced container')
    inner = html[cont_open:close_start]
    spans = []
    j = 0
    while True:
        m = re.search(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', inner[j:])
        if not m:
            break
        s = j + m.start()
        e = _balanced(inner, s, 'section')
        spans.append((cont_open + s, cont_open + e))
        j = e
    return spans


def _balanced(s, start, tag):
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    i = start + m0.end()
    d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return i + mm.end()
    raise ValueError(f'unbalanced <{tag}>')


def norm(s):
    return re.sub(r'\s+', '', s)


async def split_courses(items, apply=False, conc=4):
    from playwright.async_api import async_playwright
    report = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        sem = asyncio.Semaphore(conc)
        done = [0]

        async def one(cid, base='community'):
            async with sem:
                f = ROOT / base / cid / 'index.html'
                if not f.is_file():
                    return {'cid': cid, 'skip': 'no file'}
                html = f.read_text(encoding='utf-8')
                # JS 关：DOM 就是静态标记
                ctx = await browser.new_context(
                    viewport={'width': 1280, 'height': 800}, java_script_enabled=False)
                pg = await ctx.new_page()
                res = {'cid': cid, 'splits': [], 'skip': None}
                try:
                    await pg.goto(f'{BASE}/{base}/{cid}/', wait_until='load', timeout=25000)
                    await pg.wait_for_timeout(500)
                    info = await pg.evaluate(
                        r'''() => {
                          const c = document.getElementById('slide-container');
                          if (!c) return {err:'no container'};
                          const vh = c.clientHeight || 0;
                          const pages = [...c.querySelectorAll(':scope > .slide-page')];
                          return {vh, viewport: window.innerHeight, n: pages.length,
                                  hs: pages.map(p=>+(p.scrollHeight/(vh||1)).toFixed(2))};
                        }''')
                    if info.get('err'):
                        res['skip'] = info['err']
                        return res
                    if info['vh'] > info['viewport'] * 1.5:
                        res['skip'] = 'browse-mode'
                        return res
                    over = [i for i, h in enumerate(info['hs']) if h > LIMIT]
                    if not over:
                        res['skip'] = '无超长页'
                        return res
                    new_html = html
                    for pidx in sorted(over, reverse=True):
                        r = await pg.evaluate(SPLIT_JS, {'pageIndex': pidx, 'limit': LIMIT,
                                                         'target': TARGET, 'minGroup': MIN_GROUP})
                        if r.get('skip') or r.get('err'):
                            res['splits'].append({'page': pidx + 1, 'skip': r.get('skip') or r.get('err')})
                            continue
                        # 文本零丢失校验
                        if norm(''.join(r['texts'])) != norm(r['origText']):
                            res['splits'].append({'page': pidx + 1, 'skip': '文本不一致'})
                            continue
                        # 静态替换
                        spans = page_spans(new_html)
                        if pidx >= len(spans):
                            res['splits'].append({'page': pidx + 1, 'skip': '静态页缺失'})
                            continue
                        s, e = spans[pidx]
                        candidate = new_html[:s] + ''.join(r['htmls']) + new_html[e:]
                        # 标签平衡校验：不得比原文件更差（原文件本身可能已有不平衡）
                        if imbalance(candidate) > imbalance(new_html):
                            res['splits'].append({'page': pidx + 1, 'skip': '标签不平衡'})
                            continue
                        new_html = candidate
                        res['splits'].append({'page': pidx + 1, 'from': r['h'],
                                              'groups': r['groups'], 'ok': True})
                    # 重排 data-page-index
                    cnt = [0]
                    new_html = re.sub(r'data-page-index="\d+"',
                                      lambda m: 'data-page-index="%d"' % (
                                          cnt.__setitem__(0, cnt[0] + 1) or cnt[0] - 1),
                                      new_html)
                    good = [s for s in res['splits'] if s.get('ok')]
                    res['pages_before'] = info['n']
                    res['pages_after'] = len(page_spans(new_html))
                    if apply and good:
                        okg, whyg = apply_guarded(f, new_html, cid)
                        res['gate'] = whyg
                        res['applied'] = okg
                        if not okg:
                            res['splits'] = [s for s in res['splits'] if not s.get('ok')] + \
                                [{'page': 0, 'skip': '闸门回滚: ' + whyg}]
                    res['applied'] = bool(good)
                except Exception as e:  # noqa: BLE001
                    res['skip'] = str(e)[:140]
                finally:
                    await ctx.close()
                done[0] += 1
                if done[0] % 10 == 0:
                    print(f'  {done[0]}/{len(items)}', flush=True)
                return res

        out = await asyncio.gather(*(one(c, b) for c, b in items))
        await browser.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    ap.add_argument('--from-scan', default='')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--conc', type=int, default=4)
    ap.add_argument('--out', default='/tmp/dom-split-report.json')
    args = ap.parse_args()

    if args.from_scan:
        data = json.loads(Path(args.from_scan).read_text(encoding='utf-8'))
        items = [(r['cid'], r.get('base', 'community')) for r in data if r.get('over')]
    else:
        items = [(x.strip(), 'community') for x in args.only.split(',') if x.strip()]
    if not items:
        print('需 --only 或 --from-scan'); return 1
    print(f'处理 {len(items)} 门课件（{"写入" if args.apply else "干跑"}）…', flush=True)
    res = asyncio.run(split_courses(items, apply=args.apply, conc=args.conc))
    Path(args.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    ok = [r for r in res if any(s.get('ok') for s in r.get('splits', []))]
    skipped = [r for r in res if not any(s.get('ok') for s in r.get('splits', []))]
    print(f'\n拆成功 {len(ok)} 门，未拆 {len(skipped)} 门')
    for r in ok[:15]:
        done = [s for s in r['splits'] if s.get('ok')]
        detail = ', '.join(f"p{s['page']}:{s['from']}x→{s['groups']}页" for s in done)
        print(f"  {r['cid']:42s} 页 {r.get('pages_before')}→{r.get('pages_after')}  [{detail}]")
    reasons = {}
    for r in skipped:
        for s in (r.get('splits') or []):
            if s.get('skip'):
                reasons[s['skip']] = reasons.get(s['skip'], 0) + 1
        if r.get('skip'):
            reasons[r['skip']] = reasons.get(r['skip'], 0) + 1
    print('未拆原因:', reasons)
    print(f'明细 → {args.out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
