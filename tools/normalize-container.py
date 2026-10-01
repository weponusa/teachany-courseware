#!/usr/bin/env python3
"""结构归一化：用无 JS 浏览器的容错解析把「标签不平衡」的容器内容重排为合法结构。

适用症状
--------
`#slide-container` 里有缺失/多余的 </div></section>（历史遗留区块未闭合、把整段
<section class="section"> 塞在页与页之间等），导致：
  · 静态工具无法定位页边界（unbalanced container）→ 无法拆分/重排；
  · 浏览器虽然能容错渲染，但页可能被嵌套、导航点与页数不符。

做法
----
1. 无 JS 打开页面，浏览器已把容器内内容解析成一棵**已纠正**的 DOM 树；
2. 取 `container.innerHTML` 序列化回来；
3. 静态替换容器内区间，校验：
   · 页数一致（.slide-page 数量）；
   · 每页 textContent 与原文件页文本**逐一相等**（零内容丢失/错位）；
   · 标签平衡（section/div/figure）；
4. 成功后原文件即可被拆分器正常处理。

用法:
  python3 tools/normalize-container.py --only phy-m-lens --dry
  python3 tools/normalize-container.py --from-skip /tmp/dom-split-apply.json --apply
"""
import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8801'

GET_JS = r'''() => {
  const c = document.getElementById('slide-container');
  if (!c) return {err: 'no container'};
  const pages = [...c.querySelectorAll(':scope > .slide-page')];
  return {
    inner: c.innerHTML,
    n: pages.length,
    texts: pages.map(p => p.textContent),
    dots: document.querySelectorAll('.sidenav-dot').length,
  };
}'''


def balanced_close_start(s, start, tag):
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    i = start + m0.end()
    d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return i + mm.start()
    return None


def norm(t):
    return re.sub(r'\s+', '', t)


def static_pages(inner):
    """把容器内容按 slide-page 切块（要求已平衡）。"""
    pages, i = [], 0
    while True:
        m = re.search(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', inner[i:])
        if not m:
            break
        s = i + m.start()
        m0 = re.match(r'<section\b[^>]*>', inner[s:], re.I)
        j = s + m0.end()
        d = 1
        e = None
        for mm in re.finditer(r'<(/?)section\b[^>]*(/?)>', inner[j:], re.I):
            if mm.group(1):
                d -= 1
            elif not mm.group(2):
                d += 1
            if d == 0:
                e = j + mm.end()
                break
        if e is None:
            return None
        pages.append(inner[s:e])
        i = e
    return pages


def text_of(block):
    b = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', block, flags=re.S)
    return norm(re.sub(r'<[^>]+>', '', b))


async def run(items, apply=False, conc=4):
    from playwright.async_api import async_playwright
    out = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        sem = asyncio.Semaphore(conc)

        async def one(cid, base='community'):
            async with sem:
                f = ROOT / base / cid / 'index.html'
                if not f.is_file():
                    return {'cid': cid, 'skip': 'no file'}
                html = f.read_text(encoding='utf-8')
                ctx = await browser.new_context(viewport={'width': 1280, 'height': 800},
                                                java_script_enabled=False)
                pg = await ctx.new_page()
                res = {'cid': cid}
                try:
                    await pg.goto(f'{BASE}/{base}/{cid}/', wait_until='load', timeout=25000)
                    await pg.wait_for_timeout(400)
                    r = await pg.evaluate(GET_JS)
                    if r.get('err'):
                        res['skip'] = r['err']
                        return res
                    c = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
                    open_end = c.end()
                    close_start = balanced_close_start(html, c.start(), 'div')
                    if close_start is None:
                        # 容器自己都不平衡：用旧内容末尾做边界（按最后一个 </section> 之后的 </div>）
                        res['skip'] = '容器闭合无法定位'
                        return res
                    old_inner = html[open_end:close_start]
                    new_inner = r['inner']
                    # 校验 1：页数一致
                    if len(re.findall(r'<section[^>]*class="[^"]*slide-page', new_inner)) != r['n']:
                        res['skip'] = f"序列化页数 {r['n']} 与标记不一致"
                        return res
                    # 校验 2：逐页文本相等
                    old_pages = static_pages(old_inner)
                    new_pages = static_pages(new_inner)
                    if not old_pages or not new_pages or len(old_pages) != len(new_pages):
                        res['skip'] = '页切分失败或页数不等'
                        return res
                    for i, (a, b) in enumerate(zip(old_pages, new_pages)):
                        if text_of(a) != text_of(b):
                            res['skip'] = f'第{i+1}页文本不一致'
                            return res
                    new_html = html[:open_end] + new_inner + html[close_start:]
                    # 校验 3：标签平衡
                    for t in ('section', 'div', 'figure'):
                        if len(re.findall(r'<%s\b' % t, new_html)) != len(re.findall(r'</%s>' % t, new_html)):
                            res['skip'] = f'<{t}> 仍不平衡'
                            return res
                    res.update({'ok': True, 'n': r['n'], 'dots': r['dots'],
                                'size_before': len(html), 'size_after': len(new_html)})
                    if apply:
                        f.write_text(new_html, encoding='utf-8')
                except Exception as e:  # noqa: BLE001
                    res['skip'] = str(e)[:120]
                finally:
                    await ctx.close()
                return res

        out = await asyncio.gather(*(one(c, b) for c, b in items))
        await browser.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    ap.add_argument('--from-skip', default='')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--conc', type=int, default=4)
    ap.add_argument('--out', default='/tmp/normalize-report.json')
    args = ap.parse_args()

    if args.from_skip:
        data = json.loads(Path(args.from_skip).read_text(encoding='utf-8'))
        items = []
        for r in data:
            for s in (r.get('splits') or []):
                if s.get('skip') and ('unbalanced' in s['skip'] or '不平衡' in s['skip']):
                    items.append((r['cid'], 'community'))
                    break
    else:
        items = [(x.strip(), 'community') for x in args.only.split(',') if x.strip()]
    if not items:
        print('需 --only 或 --from-skip'); return 1
    print(f'归一化 {len(items)} 门（{"写入" if args.apply else "干跑"}）…', flush=True)
    res = asyncio.run(run(items, apply=args.apply, conc=args.conc))
    Path(args.out).write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    ok = [r for r in res if r.get('ok')]
    print(f'成功 {len(ok)} / {len(res)}')
    for r in ok[:12]:
        print(f"  {r['cid']:42s} 页{r['n']:3d} 点{r['dots']:3d}")
    import collections
    print('失败原因:', dict(collections.Counter(r['skip'][:40] for r in res if r.get('skip'))))
    return 0


if __name__ == '__main__':
    sys.exit(main())
