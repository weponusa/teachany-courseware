#!/usr/bin/env python3
"""结构归一化 v2：修复 `#slide-container` 标签不平衡（导致拆页器无法定位页边界）。

原理
----
无 JS 打开页面时，浏览器已按容错规则把容器内容解析成**合法 DOM**。
把它序列化回来即可得到平衡结构；关键是静态侧的替换区间要找准：

  起点 = 容器开标签结束
  终点 = 容器之后的第一个「稳定锚点」（页脚脚本 / 静态知识图谱块 / </body>）
  替换内容 = 浏览器序列化的 innerHTML + 补齐的 `</div>`（容器自身闭合）

三重校验（任一不过就跳过，绝不写入）：
  ① 页数：序列化后的 .slide-page 数与浏览器一致；
  ② 文本：静态区间文本 == 浏览器容器文本（归一化后逐字相等，零丢失）；
  ③ 平衡：新文件 section/div/figure 差值不得比原文件差。

用法:
  python3 tools/normalize-container.py --only phy-m-lens --dry
  python3 tools/normalize-container.py --from-overlong /tmp/overlong-final.json --apply
"""
import argparse
import asyncio
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import imbalance  # noqa: E402

BASE = 'http://127.0.0.1:8801'
ANCHORS = [
    '<section class="section" id="knowledge-graph"',
    '<footer',
    '<div class="teachany-footer',
    '<script src="../../assets/script',
    '<script src="./',
    '</body>',
]

GET_JS = r'''() => {
  const c = document.getElementById('slide-container');
  if (!c) return {err: 'no container'};
  const pages = [...c.querySelectorAll(':scope > .slide-page')];
  return {
    inner: c.innerHTML,
    n: pages.length,
    all: c.querySelectorAll('.slide-page').length,
    text: (() => { const cl = c.cloneNode(true);
      cl.querySelectorAll('script,style').forEach(e => e.remove());
      return cl.textContent; })(),
    direct: pages.length,
  };
}'''


def norm(t):
    return re.sub(r'\s+', '', t)


def text_of(html):
    h = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html, flags=re.S)
    return norm(re.sub(r'<[^>]+>', '', h))


def find_region_end_by_text(html, start, target_len):
    """按「可见文本长度」在静态 HTML 中定位容器内容区间的结束位置。

    为什么不用锚点：容器内部也可能出现 <script>/<footer> 等，锚点法会截断。
    这里从左到右累加可见文本（跳过标签、script/style 内容、实体解码），
    累加到与浏览器容器文本等长时，该位置即容器内容结束处。
    """
    import html as _html
    i = start
    acc = 0
    n = len(html)
    while i < n and acc < target_len:
        ch = html[i]
        if ch == '<':
            j = html.find('>', i)
            if j < 0:
                break
            tag = html[i:j + 1].lower()
            if tag.startswith('<script') or tag.startswith('<style'):
                k = tag[:2]
                close = '</script>' if tag.startswith('<script') else '</style>'
                e = html.lower().find(close, j)
                i = (e + len(close)) if e > 0 else n
                continue
            i = j + 1
            continue
        if ch == '&':
            j = html.find(';', i)
            if 0 < j - i <= 8:
                acc += len(re.sub(r'\s+', '', _html.unescape(html[i:j + 1])))
                i = j + 1
                continue
        if not ch.isspace():
            acc += 1
        i += 1
    return i


def container_open_end(html):
    c = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
    return c.end() if c else None


async def run(items, apply=False, conc=4):
    from playwright.async_api import async_playwright
    out = []
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        sem = asyncio.Semaphore(conc)

        async def one(item):
            cid, base = item
            async with sem:
                f = ROOT / base / cid / 'index.html'
                res = {'cid': cid}
                if not f.is_file():
                    return {'cid': cid, 'skip': 'no file'}
                html = f.read_text(encoding='utf-8')
                open_end = container_open_end(html)
                if open_end is None:
                    return {'cid': cid, 'skip': 'no container'}
                ctx = await browser.new_context(viewport={'width': 1280, 'height': 800},
                                                java_script_enabled=False)
                pg = await ctx.new_page()
                try:
                    await pg.goto(f'{BASE}/{base}/{cid}/', wait_until='load', timeout=25000)
                    await pg.wait_for_timeout(400)
                    r = await pg.evaluate(GET_JS)
                    if r.get('err'):
                        res['skip'] = r['err']; return res
                    target_len = len(norm(r['text']))
                    anchor_pos = find_region_end_by_text(html, open_end, target_len)
                    region = html[open_end:anchor_pos]
                    # 校验 ②：文本一致
                    if text_of(region) != norm(r['text']):
                        # 容差：允许浏览器省略 figcaption 空白等；严格比较失败即跳过
                        res['skip'] = '文本不一致（跳过）'
                        return res
                    cands = []
                    for k in range(0, 4):
                        ni = r['inner'] + '</div>' * k
                        nh = html[:open_end] + ni + html[anchor_pos:]
                        cands.append((imbalance(nh), k, ni, nh))
                    cands.sort(key=lambda x: x[0])
                    best_imb, best_k, new_inner, new_html = cands[0]
                    if best_imb > imbalance(html):
                        res['skip'] = f"平衡变差 {imbalance(html)}→{best_imb}（试过 0~3 个闭合）"
                        return res
                    # 校验 ①：页数
                    if len(re.findall(r'<section[^>]*class="[^"]*slide-page', new_inner)) != r['n']:
                        res['skip'] = '页数不一致'
                        return res
                    res.update({'ok': True, 'n': r['n'], 'anchor': 'text-locator',
                                'imbalance_before': imbalance(html),
                                'imbalance_after': imbalance(new_html)})
                    if apply:
                        f.write_text(new_html, encoding='utf-8')
                except Exception as e:  # noqa: BLE001
                    res['skip'] = str(e)[:120]
                finally:
                    await ctx.close()
                return res

        out = await asyncio.gather(*(one(i) for i in items))
        await browser.close()
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    ap.add_argument('--from-overlong', default='')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--conc', type=int, default=4)
    args = ap.parse_args()

    if args.from_overlong:
        data = json.loads(Path(args.from_overlong).read_text(encoding='utf-8'))
        items = [(r['cid'], r.get('base', 'community')) for r in data if r.get('over')]
    else:
        items = [(x.strip(), 'community') for x in args.only.split(',') if x.strip()]
    if not items:
        print('需 --only 或 --from-overlong'); return 1
    print(f'结构归一化 {len(items)} 门（{"写入" if args.apply else "干跑"}）…', flush=True)
    res = asyncio.run(run(items, apply=args.apply, conc=args.conc))
    Path('/tmp/normalize-report.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    ok = [r for r in res if r.get('ok')]
    import collections
    print(f'可归一化 {len(ok)} / {len(res)}')
    print('跳过原因:', dict(collections.Counter(r['skip'][:26] for r in res if r.get('skip'))))
    for r in ok[:8]:
        print(f"  {r['cid']:42s} 页{r['n']:3d} 平衡 {r['imbalance_before']}→{r['imbalance_after']} 锚点={r['anchor'][:24]}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
