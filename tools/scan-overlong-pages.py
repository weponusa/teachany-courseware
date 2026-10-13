#!/usr/bin/env python3
"""批量浏览器实测：找出所有存在超长页（>1.6x 视口，产生嵌套滚动）的课件。

用法:
  python3 tools/scan-overlong-pages.py [--limit N] [--out /tmp/overlong.json]

依赖: 本地静态服务 http://127.0.0.1:8801（仓库根目录）。
输出: JSON [{cid, pages, dots, nested, worst:{page,type,height}, over:[...]}]
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8801'

JS = r'''() => {
  const c = document.getElementById('slide-container');
  if (!c) return {skip: 'no slide-container'};
  const pages = [...c.querySelectorAll(':scope > .slide-page')];
  if (!pages.length) return {skip: 'no pages'};
  const vh = c.clientHeight || 1;
  const hs = pages.map((p, i) => ({
    page: i + 1,
    type: p.getAttribute('data-page-type') || '?',
    height: +(p.scrollHeight / vh).toFixed(2),
  }));
  const over = hs.filter(x => x.height > 1.6);
  return {
    pages: pages.length,
    dots: document.querySelectorAll('.sidenav-dot').length,
    nested: c.querySelectorAll('.slide-page').length - pages.length,
    worst: hs.reduce((a, x) => (x.height > a.height ? x : a)),
    over,
  };
}'''


def migrated_courses():
    out = []
    for base in ('community', 'examples'):
        d = ROOT / base
        if not d.is_dir():
            continue
        for c in sorted(d.iterdir()):
            f = c / 'index.html'
            if not f.is_file() or c.name == 'drafts':
                continue
            h = f.read_text(encoding='utf-8', errors='ignore')
            if 'id="slide-container"' in h and 'data-page-type=' in h:
                out.append((base, c.name))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--out', default='/tmp/overlong.json')
    ap.add_argument('--conc', type=int, default=6)
    args = ap.parse_args()

    courses = migrated_courses()
    if args.limit:
        courses = courses[:args.limit]
    print(f'扫描 {len(courses)} 门已分页课件…', flush=True)

    import asyncio
    from playwright.async_api import async_playwright

    results = []

    async def run():
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            sem = asyncio.Semaphore(args.conc)
            done = [0]

            async def check(item):
                base, cid = item
                async with sem:
                    ctx = await browser.new_context(viewport={'width': 1280, 'height': 800})
                    pg = await ctx.new_page()
                    try:
                        await pg.goto(f'{BASE}/{base}/{cid}/', wait_until='load', timeout=20000)
                        await pg.wait_for_timeout(900)
                        r = await pg.evaluate(JS)
                        r['cid'] = cid
                        r['base'] = base
                    except Exception as e:  # noqa: BLE001
                        r = {'cid': cid, 'base': base, 'error': str(e)[:120]}
                    finally:
                        await ctx.close()
                    results.append(r)
                    done[0] += 1
                    if done[0] % 25 == 0:
                        print(f"  {done[0]}/{len(courses)}", flush=True)

            await asyncio.gather(*(check(c) for c in courses))
            await browser.close()

    asyncio.run(run())

    Path(args.out).write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding='utf-8')
    bad = [r for r in results if r.get('over')]
    err = [r for r in results if r.get('error')]
    nest = [r for r in results if r.get('nested')]
    print(f'\n完成 {len(results)} 门: 超长 {len(bad)} 门, 嵌套页 {len(nest)} 门, 加载失败 {len(err)} 门')
    print(f'明细 → {args.out}')
    for r in sorted(bad, key=lambda x: -x['worst']['height'])[:40]:
        w = r['worst']
        over_desc = ','.join(f"#{o['page']}{o['type']}:{o['height']}x" for o in r['over'][:4])
        print(f"  {r['cid']:42s} 最坏 #{w['page']}({w['type']}) {w['height']}x  [{over_desc}]")


if __name__ == '__main__':
    sys.exit(main())
