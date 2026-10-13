#!/usr/bin/env python3
"""迁移验收（加强版）—— 补上"每页可见内容"这个此前缺失的关键指标。

为什么要这个
------------
之前的验收只查：16 页 / 16 导航点 / 点导航能滚 / 控制台零报错 / 内容保留率。
结果**一个可见字数为 0 的页面能全部通过** —— 实测 `phy-m-lens` 第 4 页可见 0 字、
`chn-h-classical-vocab-h` 的知识图谱页 svg=0 完全空白，都没被拦下。
用户看到的就是"缺模块 / 内容太少"。

本工具逐项断言
--------------
  结构   ：容器**直属** .slide-page == 16、.sidenav-dot == 16、页型序符合规范
  交互   ：点第 8 点后 scrollTop > 0、overflowY == 'auto'
  报错   ：pageerror == 0
  内容 ★ ：**每页可见字符数**，低于阈值单独标出
  JS 模块★：知识图谱页是否有 svg、AI 学伴容器是否恰好 1 个

用法：
  python3 tools/verify-migration.py <course_id> [...]
  python3 tools/verify-migration.py --sample 20      # 从已迁移课件里抽 20 门
"""
import argparse
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'http://127.0.0.1:8801'
CANON = ['cover', 'interactive', 'objectives', 'quiz', 'concept', 'interactive', 'concept',
         'interactive', 'concept', 'quiz', 'interactive', 'quiz', 'summary', 'homework',
         'knowledge-graph', 'ai-tutor']
THIN = 100      # 可见字符数低于此值视为"内容过少"（quiz 单独放宽到 70）


def migrated_courses():
    out = []
    for base in ('community', 'examples'):
        d = ROOT / base
        if not d.is_dir():
            continue
        for c in sorted(d.iterdir()):
            f = c / 'index.html'
            if not f.is_file():
                continue
            h = f.read_text(encoding='utf-8', errors='ignore')
            # ★ 只抽「本工具迁移的」课件：必须同时有分页容器与分页外壳。
            #   否则会把别人迁移的课件（页型是 content/hero/anchor…）算进来，
            #   导致抽样结果 0 通过、完全无法反映本次迁移的状态。
            if 'id="slide-container"' in h and 'id="slide-sidenav"' in h \
               and 'data-page-type="cover"' in h:
                out.append((base, c.name))
    return out


JS = """() => {
  const c = document.getElementById('slide-container');
  if (!c) return {err:'no container'};
  const kids = [...c.children].filter(e => e.classList.contains('slide-page'));
  const cs = getComputedStyle(c);
  const kge = kids.find(e => e.dataset.pageType === 'knowledge-graph');
  return {
    pages: kids.length,
    dots: document.querySelectorAll('.sidenav-dot').length,
    types: kids.map(e => e.dataset.pageType),
    ov: cs.overflowY, ch: c.clientHeight, sh: c.scrollHeight,
    chars: kids.map(e => (e.innerText || '').replace(/\\s/g, '').length),
    tutorInPage: document.querySelectorAll('.slide-page [data-teachany-tutor-card]').length,
    tutorTotal: document.querySelectorAll('[data-teachany-tutor-card]').length,
    kgSvg: kge ? kge.querySelectorAll('svg').length : -1
  };
}"""


def run(ids):
    from playwright.sync_api import sync_playwright
    rows = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for base, cid in ids:
            pg = b.new_page(viewport={'width': 1440, 'height': 900})
            errs = []
            pg.on('pageerror', lambda e: errs.append(str(e)[:80]))
            row = {'id': cid}
            try:
                pg.goto(f'{BASE}/{base}/{cid}/index.html', wait_until='domcontentloaded', timeout=45000)
                pg.wait_for_timeout(2300)
                m = pg.evaluate(JS)
                pg.evaluate("() => document.querySelectorAll('.sidenav-dot')[7]?.click()")
                pg.wait_for_timeout(1200)
                st = pg.evaluate("() => Math.round(document.getElementById('slide-container').scrollTop)")
                m['scroll'] = st
                m['errors'] = len(errs)
                row.update(m)
            except Exception as e:
                row['err'] = str(e)[:70]
            rows.append(row)
            pg.close()
        b.close()
    return rows


def judge(r):
    """返回 (是否通过, 问题列表)"""
    if 'err' in r and r.get('pages') is None:
        return False, [f"加载失败: {r.get('err')}"]
    bad = []
    # ★ 页数不再固定 16（用户明确"没有什么 16 页限制"）：
    #   改为「页数 ≥ 6」+「导航点数 == 页数」+「没有空页」+「页型序是规范序的子序列」
    pages = r.get('pages') or 0
    if pages < 6:
        bad.append(f"页数过少={pages}")
    if r.get('dots') != pages:
        bad.append(f"导航点数({r.get('dots')})≠页数({pages})")
    types = r.get('types') or []
    # 页型：必须是规范序的**子序列**（允许因缺内容而跳页，但不允许乱序）
    # 用子序列判断，不能用 `[t for t in CANON if t in types]`（多重页型会比错）
    it = iter(CANON)
    if not all(any(t == c for c in it) for t in types):
        bad.append("页型序不符规范")
    if (r.get('scroll') or 0) <= 0:
        bad.append("点导航不滚动")
    if r.get('ov') != 'auto':
        bad.append(f"overflowY={r.get('ov')}")
    if r.get('errors'):
        bad.append(f"JS报错×{r['errors']}")
    if r.get('tutorTotal', 1) > 1:
        bad.append(f"AI学伴容器×{r['tutorTotal']}")
    if r.get('kgSvg') == 0:
        bad.append("知识图谱页空白(svg=0)")
    # 空页检查：按页型设阈值 —— 封面/学习目标/小结**本来就短**（一行标题 + 几条要点），
    # 用统一阈值会把正常页误判为"内容过少"。
    # knowledge-graph / ai-tutor 由 JS 渲染，文字天然少，直接不计入。
    MIN_CJK = {'cover': 15, 'objectives': 25, 'summary': 25, 'homework': 40, 'quiz': 70}
    thin = []
    for i, n in enumerate(r.get('chars') or []):
        t = (r.get('types') or [])[i] if i < len(r.get('types') or []) else '?'
        if t in ('knowledge-graph', 'ai-tutor'):
            continue
        if n < MIN_CJK.get(t, THIN):
            thin.append((i, t, n))
    if thin:
        bad.append("内容过少页 " + str([f"#{i}{t}({n}字)" for i, t, n in thin]))
    return (not bad), bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('course_id', nargs='*')
    ap.add_argument('--sample', type=int, default=0)
    a = ap.parse_args()
    if a.course_id:
        ids = []
        for cid in a.course_id:
            for base in ('community', 'examples'):
                if (ROOT / base / cid / 'index.html').exists():
                    ids.append((base, cid))
                    break
    elif a.sample:
        allc = migrated_courses()
        random.seed(42)
        ids = random.sample(allc, min(a.sample, len(allc)))
    else:
        ap.print_help()
        return 1

    rows = run(ids)
    ok = 0
    print(f"{'课件':38s} 结果")
    for r in rows:
        good, bad = judge(r)
        ok += 1 if good else 0
        print(f"{'✅' if good else '❌'} {r['id'][:36]:36s} " + ('通过' if good else ' | '.join(bad)))
    print(f"\n通过 {ok}/{len(rows)}")
    Path('/tmp/verify-migration.json').write_text(json.dumps(rows, ensure_ascii=False), encoding='utf-8')
    print('明细 → /tmp/verify-migration.json')
    return 0 if ok == len(rows) else 1


if __name__ == '__main__':
    sys.exit(main())
