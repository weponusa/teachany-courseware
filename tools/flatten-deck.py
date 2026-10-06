#!/usr/bin/env python3
"""把 v2 deck 型课件（.slide-container 内部滚动幻灯片）拍平为普通长页。

解决「页中页」嵌套：deck 容器固定一屏高、内部滚动、scroll-snap，
夹在平铺内容中间形成双重滚动 + 下一页露头的嵌套观感。

拍平动作（对单个 index.html）：
1. 删除 deck 外与 deck 页内容重复的平铺 section（可选 --drop-dup，默认开）：
   hero-infographic / objectives / anchor / module-N 这些 section 的内容
   已被复制进 deck 的 cover/情境/目标/概念页里。
2. `<section class="slide-page" ...><div class="slide-inner">X</div></section>`
   → `<section class="section" ...>X</section>`（div 变体同样处理，保留 id 与 data-*）
3. 剥掉 `<div class="slide-container">` 壳。
4. 删除 deck 专属 DOM：slide-progress-bar、slide-sidenav、play-mode-fab、
   页内 slide-toolbar。
5. 删除 deck 专属 JS（pages/sidenav/fab/toolbar/autoplay IIFE），
   保留其中的版本号回填逻辑（course-version-display）。
6. 注入覆盖 CSS：容器/页面恢复自然高度、解锁 body 滚动、去 scroll-snap。

用法：
    python3 tools/flatten-deck.py community/phy-m-joule-law/index.html --apply
    python3 tools/flatten-deck.py community/phy-m-joule-law/index.html --dry-run
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

RE_SLIDE_CONTAINER_OPEN = re.compile(
    r'[ \t]*<div class="slide-container"[^>]*>\n?')
RE_SLIDE_PAGE = re.compile(
    r'<(section|div)\s+class="slide-page([^"]*)"([^>]*)>\s*<div class="slide-inner">([\s\S]*?)</div>\s*</\1>',
    re.I)
RE_TOOLBAR = re.compile(
    r'[ \t]*<div class="slide-toolbar"\b[\s\S]*?<!-- /?slide-toolbar -->[ \t]*\n?'
    r'|[ \t]*<div class="slide-toolbar"\b[^>]*>[\s\S]*?</div>\s*(?=</div>|</section>)', re.I)
RE_PROGRESS = re.compile(r'[ \t]*<div class="slide-progress-bar"[^>]*></div>[ \t]*\n?', re.I)
RE_SIDENAV = re.compile(r'[ \t]*<nav class="slide-sidenav"[\s\S]*?</nav>[ \t]*\n?', re.I)
RE_FAB = re.compile(r'[ \t]*<button class="play-mode-fab"[\s\S]*?</button>[ \t]*\n?', re.I)

# deck IIFE：以 slide-container 开头的整段 script
RE_DECK_JS = re.compile(
    r'[ \t]*<script>\s*\(function\(\) \{\s*\'use strict\';\s*const container = document\.getElementById\(\'slide-container\'\)[\s\S]*?\}\)\(\);\s*</script>[ \t]*\n?')

VERSION_KEEPER = """<script>
(function() {
  document.addEventListener('DOMContentLoaded', () => {
    const cv = document.querySelector('meta[name="course-version"]')?.content;
    const sv = document.querySelector('meta[name="teachany-version"]')?.content;
    const cvEl = document.getElementById('course-version-display');
    const svEl = document.getElementById('skill-version-display');
    if (cv && cvEl) cvEl.textContent = cv;
    if (sv && svEl) svEl.textContent = sv.replace(/^v/, '');
  });
})();
</script>
"""

FLATTEN_CSS = """
<style id="ta-deck-flattened">
/* deck 已拍平：恢复文档流，去掉内部滚动与 snap */
.slide-container, div[id="slide-container"] { height: auto !important; max-height: none !important; overflow: visible !important; scroll-snap-type: none !important; }
.slide-page, section.slide-page, div.slide-page { min-height: 0 !important; height: auto !important; scroll-snap-align: none !important; scroll-margin-top: 76px; }
body { overflow: visible !important; max-height: none !important; }
body.play-mode .slide-container { overflow: visible !important; }
.slide-progress-bar, .slide-sidenav, .play-mode-fab { display: none !important; }
</style>
"""

# 注意：不删 hero-infographic —— 硬规则 #57 要求页面里必须有
# `<img class="hero-cover-img" src="./assets/<cid>-hero.png">`，而 deck 的 cover 页
# 未必带该引用，删掉唯一带引用的 section 会直接触发「缺少 hero 主图引用」阻断。
DROP_DUP_IDS = re.compile(
    r'\n?[ \t]*<section\b[^>]*\bid="(objectives|anchor|module-\d+)"[^>]*>[\s\S]*?</section>[ \t]*\n?')


def flatten(html: str, drop_dup: bool = True) -> tuple[str, list[str]]:
    notes: list[str] = []
    out = html

    # 1) 删除 deck 外重复平铺 section
    if drop_dup:
        out, n = DROP_DUP_IDS.subn("\n", out)
        if n:
            notes.append(f"drop-dup-sectionsx{n}")

    # 2) slide-page → section（保留 id/data-*，剥 slide-inner）
    def page_repl(m):
        tag, extra_cls, attrs, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        # class 里必须带 module（质检的 module_like 判定认 module|lesson|concept，
        # 否则「实质 section 数」会骤降、连带「有效教学文本」不足而报错）
        cls = "section module" + (extra_cls if extra_cls.strip() else "")
        return f'<section class="{cls}"{attrs}>{inner}</section>'
    out, n = RE_SLIDE_PAGE.subn(page_repl, out)
    if n:
        notes.append(f"pages-flattened{n}")

    # 3) 剥 slide-container 壳：优先深度配对找闭标签；找得到就剥壳+删闭标签，
    #    找不到（原文件 div 本就不配平，浏览器兜底闭合）则只删开标签。
    m = re.search(r'<div class="slide-container"[^>]*>\n?', out)
    if m:
        depth = 1
        close_start = None
        for t in re.finditer(r'<div\b|</div>', out[m.end():]):
            depth += 1 if t.group(0) == '<div' else -1
            if depth == 0:
                close_start = m.end() + t.start()
                break
        if close_start is not None:
            inner = out[m.end():close_start]
            out = out[:m.start()] + inner + out[close_start + len('</div>'):]
        else:
            out = out[:m.start()] + out[m.end():]
        notes.append("container-unwrapped")

    # 4) 删 deck 专属 DOM
    for name, pat in (("toolbar", RE_TOOLBAR), ("progress", RE_PROGRESS),
                      ("sidenav", RE_SIDENAV), ("fab", RE_FAB)):
        out, n = pat.subn("\n", out)
        if n:
            notes.append(f"del-{name}x{n}")

    # 5) 删 deck JS，保留版本号回填
    out, n = RE_DECK_JS.subn("\n" + VERSION_KEEPER, out)
    if n:
        notes.append("deck-js-replaced")

    # 7) 给拍平后的 section 补 data-bloom-level / data-scaffold
    #    原 deck 页大多没带这两个标注（标注只打在被删掉的平铺 section 上），
    #    拍平后质检会报「Bloom 层级覆盖不足」「脚手架分级不足」。
    out, n = re.subn(
        r'<section class="section"([^>]*?)>',
        lambda m: f'<section class="section"{ensure_attrs(m.group(1))}>',
        out)
    if n:
        notes.append(f"attrs-ensured{n}")

    # 8) 覆盖 CSS（放在 </head> 前）
    if "ta-deck-flattened" not in out:
        out = out.replace("</head>", FLATTEN_CSS + "</head>", 1)
        notes.append("flatten-css")

    return out, notes


# 按主题（data-tsh）推断 Bloom 层级与脚手架分级
BLOOM_MAP = [
    (r'迁移|挑战|任务|综合', 'create', 'partial'),
    (r'知识图谱|图谱|节点位置|辨析|对比', 'analyze', 'full'),
    (r'互动|实验|探究|范例|即练|检验|后测|前测', 'apply', 'partial'),
    (r'概念|精讲|原理|规律|定律', 'understand', 'full'),
    (r'概览|目标|导入|带着问题|锚点|模块', 'remember', 'full'),
]


def ensure_attrs(attrs: str) -> str:
    """缺失时补 data-bloom-level 与 data-scaffold（按 data-tsh 主题推断）。"""
    if 'data-bloom-level' in attrs and 'data-scaffold' in attrs:
        return attrs
    tsh = re.search(r'data-tsh="([^"]*)"', attrs)
    tsh = tsh.group(1) if tsh else ''
    bloom, scaffold = 'understand', 'full'
    for pat, b, s in BLOOM_MAP:
        if re.search(pat, tsh):
            bloom, scaffold = b, s
            break
    out = attrs
    if 'data-bloom-level' not in out:
        out += f' data-bloom-level="{bloom}"'
    if 'data-scaffold' not in out:
        out += f' data-scaffold="{scaffold}"'
    return out


def main() -> int:
    args = [a for a in sys.argv[1:]]
    apply = "--apply" in args
    args = [a for a in args if not a.startswith("--")]
    drop_dup = "--keep-dup" not in sys.argv
    if not args:
        print(__doc__)
        return 2
    p = Path(args[0])
    src = p.read_text(encoding="utf-8")
    out, notes = flatten(src, drop_dup=drop_dup)
    print(f"{p}: {notes or '无可拍平内容'}")
    if notes and apply:
        p.write_text(out, encoding="utf-8")
        print("已写入")
    return 0


if __name__ == "__main__":
    sys.exit(main())
