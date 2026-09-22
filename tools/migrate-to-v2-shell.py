#!/usr/bin/env python3
"""把「半 v1」课件迁移到 v2 分页外壳。

适用对象：**已经有 <section class="slide-page"> 分页节、只是缺整套分页外壳**的课件
（实测全站 199 门）。不含真单页长文（91 门）与内容过少的（1–5 页，320 门）。

本工具只做**已实测零报错**的机械部分：
  1. 注入 v2 外壳 CSS
  2. 注入顶部进度条
  3. 把 .slide-page 包进 #slide-container
  4. 注入侧边导航 + 播放 FAB + 底部工具栏
  5. 注入分页控制器
  6. 重排 data-page-index
  7. 移除旧版 <nav class="teachany-page-nav">

**不做**内容重排（把 10 页补到 16 页、把旧版遗留区块合并成合理的页）——那需要按课判断，
交给 agent。本工具会打印结构报告说明缺什么。

用法：
  python3 tools/migrate-to-v2-shell.py <course_id> [--dry-run]
  python3 tools/migrate-to-v2-shell.py --list      # 列出可迁移对象
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHELL = ROOT / 'tools' / 'v2-shell'

# 用独立 id 作为"已注入"标记 —— 不要用类名，因为 CSS 里也含类名会导致误判
M_CONTAINER = 'id="slide-container"'
M_PROG = 'id="slide-progress-bar"'
M_NAV = 'id="slide-sidenav"'
M_CTRL = 'const container = document.getElementById'

# v2 标准页型（16 页规范）
CANON = ['cover', 'interactive', 'objectives', 'quiz', 'concept', 'interactive',
         'concept', 'interactive', 'concept', 'quiz', 'interactive', 'quiz',
         'summary', 'homework', 'knowledge-graph', 'ai-tutor']


def course_dir(cid):
    for base in ('community', 'examples'):
        d = ROOT / base / cid
        if (d / 'index.html').exists():
            return d
    return None


def list_targets(min_pages=6):
    out = []
    for base in ('community', 'examples'):
        b = ROOT / base
        if not b.is_dir():
            continue
        for d in sorted(b.iterdir()):
            f = d / 'index.html'
            if not f.is_file():
                continue
            h = f.read_text(encoding='utf-8', errors='ignore')
            pages = len(re.findall(r'class="slide-page', h))
            if pages >= min_pages and M_NAV not in h:
                out.append((d.name, pages))
    return out


def report(h):
    """打印结构报告，供 agent 判断还缺什么内容"""
    idx = re.findall(r'<section class="slide-page"([^>]*)>', h)
    types = re.findall(r'data-page-type="([^"]+)"', h)
    legacy = len(re.findall(r'<section class="section[^"]*"', h))
    print(f"  分页节 {len(idx)} 个 | 页型: {types}")
    missing = []
    for t in ('cover', 'objectives', 'summary', 'homework', 'knowledge-graph', 'ai-tutor'):
        if t not in types:
            missing.append(t)
    print(f"  缺的规范页型: {missing or '无'}")
    print(f"  尚未处理的旧版遗留区块（section.section）：{legacy} 个 ← 需 agent 决定合并进哪一页")
    if len(idx) != 16:
        print(f"  ⚠️ 页数 {len(idx)} ≠ 16（规范值），需要 agent 增删/合并页")


def migrate(cid, dry=False):
    d = course_dir(cid)
    if not d:
        print(f"❌ 找不到课件 {cid}")
        return 1
    f = d / 'index.html'
    h = f.read_text(encoding='utf-8')
    before = len(h)

    if M_NAV in h:
        print(f"⏭️  {cid} 已迁移过（存在 #slide-sidenav），跳过")
        report(h)
        return 0

    print(f"📄 {cid}  迁移前 {before} 字节")
    report(h)
    if dry:
        print("   (--dry-run，不写入)")
        return 0

    css = (SHELL / 'shell.css').read_text(encoding='utf-8')
    js = (SHELL / 'shell-controller.js').read_text(encoding='utf-8')
    head = (SHELL / 'shell-head.html').read_text(encoding='utf-8')
    tail = (SHELL / 'shell-tail.html').read_text(encoding='utf-8')

    # 1) 旧版导航条
    h = re.sub(r'<nav class="teachany-page-nav"[\s\S]*?</nav>\s*', '', h, count=1)
    # 2) CSS
    if '.slide-progress-bar' not in h:
        h = h.replace('</head>', f'<style>\n{css}\n</style>\n</head>', 1)
    # 3) 进度条
    if M_PROG not in h:
        h = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + head, h, count=1)
    # 4) 包 container
    if M_CONTAINER not in h:
        first = h.find('<section class="slide-page"')
        last_sec = h.rfind('<section class="slide-page"')
        last = h.find('</section>', last_sec) + len('</section>')
        if first < 0 or last_sec < 0:
            print("❌ 找不到 slide-page 节")
            return 1
        h = (h[:first] + '<div id="slide-container">\n' + h[first:last] +
             '\n</div><!-- .slide-container -->\n' + h[last:])
    # 5) 尾部（导航/FAB/工具栏）
    if M_NAV not in h:
        h = h.replace('</body>', tail + '\n</body>', 1)
    # 6) 控制器
    if M_CTRL not in h:
        h = h.replace('</body>', f'<script>\n{js}\n</script>\n</body>', 1)
    # 7) 重排 data-page-index
    cnt = [0]

    def renum(m):
        cnt[0] += 1
        return f'<section class="slide-page" data-page-index="{cnt[0] - 1}"'

    h = re.sub(r'<section class="slide-page"(?:\s+data-page-index="\d+")?', renum, h)

    f.write_text(h, encoding='utf-8')
    print(f"  ✅ 外壳已注入：{before} → {len(h)} 字节")
    print("  ⚠️ 请务必本地渲染验证（浏览器打开、点导航点、看控制台无报错），"
          "并补足到 16 页规范页型后再提交")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('course_id', nargs='?')
    ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--list', action='store_true')
    a = ap.parse_args()
    if a.list:
        t = list_targets()
        print(f"可迁移对象（≥6 个 slide-page 且未注入外壳）：{len(t)} 门")
        for cid, n in t[:40]:
            print(f"   {cid:42s} {n} 页")
        if len(t) > 40:
            print(f"   … 及另外 {len(t) - 40} 门")
        return 0
    if not a.course_id:
        ap.print_help()
        return 1
    sys.exit(migrate(a.course_id, a.dry_run))


if __name__ == '__main__':
    main()
