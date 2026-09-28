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



def inject_tail(h, block):
    """把 block 放到"文档真正末尾"。

    ★ 不能简单用 replace('</body>', …)：实测有课件把 </body></html> 写在**文档中间**
      （后面还跟着若干 <section>），那样会把外壳 DOM 插到错位置，
      结果是 getElementById 取不到 → 控制器抛 null 错误、工具栏不显示。
      策略：只有当最后一个 </body> 之后确实没有实质内容时才插在它前面，
      否则直接追加到文件末尾（浏览器会把尾部元素并入 body，功能正常）。
    """
    i = h.rfind('</body>')
    if i >= 0 and not h[i + len('</body>'):].strip():
        return h[:i] + block + h[i:]
    return h + block

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
    # 2) CSS —— ★ 不能假设有 </head>：实测 34 门物理课件**整个 head 没有闭合标签**，
    #    用 replace('</head>', …) 会静默失败（只注入了 JS/尾部 DOM，没注 CSS），
    #    结果没有外壳样式 → 容器沿用旧基线 overflow:visible → 点导航只有计数变、页面不动。
    #    注入点按可靠性依次回退，并在全部失败时报警（不再静默跳过）。
    if '.slide-progress-bar' not in h:
        block = f'<style>\n{css}\n</style>\n'
        if '</head>' in h:
            h = h.replace('</head>', block + '</head>', 1)
            print('     CSS 注入点: </head> 之前')
        elif '<body' in h:
            i = h.find('<body')
            h = h[:i] + block + h[i:]
            print('     CSS 注入点: <body> 之前（该课件没有 </head>，已回退）')
        else:
            i = h.find('<section')
            i = 0 if i < 0 else i
            h = h[:i] + block + h[i:]
            print('     ⚠️ CSS 注入点: 文件开头（连 <body> 都没有，请人工核对）')
    # 3) 进度条
    if M_PROG not in h:
        if '<body' in h:
            h = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + '\n' + head, h, count=1)
        else:
            i = h.find('<section')
            i = 0 if i < 0 else i
            h = h[:i] + head + '\n' + h[i:]
    # 4) 包 container
    if M_CONTAINER not in h:
        first = h.find('<section class="slide-page"')
        last_sec = h.rfind('<section class="slide-page"')
        last = h.find('</section>', last_sec) + len('</section>')
        if first < 0 or last_sec < 0:
            print("❌ 找不到 slide-page 节")
            return 1
        # ★ 必须同时给 class：外壳 CSS 选的是 .slide-container（负责 overflow-y/scroll-snap/高度），
        #   只给 id 会让容器不可滚动、点导航不跳页。实测踩过。
        h = (h[:first] + '<div class="slide-container" id="slide-container">\n' + h[first:last] +
             '\n</div><!-- .slide-container -->\n' + h[last:])
    # 5) 尾部（导航/FAB/工具栏）
    if M_NAV not in h:
        h = inject_tail(h, tail + '\n')
    # 6) 控制器
    # ★ 有些课件（实测 34 门物理）**自带一份旧版控制器**——和本模板同源但更早的修订：
    #   没有空引用加固，且它在 DOM 里位于我注入的外壳之前，取不到 #slide-progress-bar
    #   等元素而抛错。处理：把它整块移除，改用本模板这版已加固、已验证的控制器。
    removed = 0
    for m in list(re.finditer(r'<script(?![^>]*\bsrc=)[^>]*>[\s\S]*?</script>', h)):
        if "getElementById('slide-container')" in m.group(0):
            h = h[:m.start()] + h[m.end():]
            removed += 1
    if removed:
        print(f'     移除了课件自带的 {removed} 个旧控制器（改用加固版）')
    if M_CTRL not in h:
        h = inject_tail(h, f'<script>\n{js}\n</script>\n')
    # 6b) 占位补全：旧课件的一些内联脚本会写
    #     getElementById('course-version-display').textContent=…，而它没有品牌栏的那两个 span，
    #     缺了就整段抛错。补一对隐藏占位（无副作用）。
    if 'id="course-version-display"' not in h:
        stub = ('<div hidden aria-hidden="true" style="display:none">'
                '<span id="course-version-display"></span>'
                '<span id="skill-version-display"></span></div>')
        if '<body' in h:
            h = re.sub(r'(<body[^>]*>)', lambda m: m.group(1) + stub, h, count=1)
        else:
            h = stub + h

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
