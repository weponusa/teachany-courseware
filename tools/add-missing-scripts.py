#!/usr/bin/env python3
"""补上缺失的共享脚本引用（知识图谱 / AI 学伴）。

背景：实测已迁移的 641 门里，84 门没引用 `teachany-knowledge-graph.js`、
192 门没引用 `teachany-tutor-card.js`（原版即如此）。缺引用 → 这两页 JS 渲染不出内容
→ 用户看到的是"两页空白"（误判为缺模块）。

插入位置：紧邻已有的 `teachany-knowledge-graph.js` / `teachany-section-hints.js` 等共享脚本之后，
没有参照时就插在分页控制器脚本之前，保证在 DOM 就绪前加载。

用法：--list 列出；--apply 实际写入。
"""
import argparse, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WANT = [
    ('teachany-knowledge-graph.js', r'teachany-knowledge-graph\.js'),
    ('teachany-tutor-card.js',      r'teachany-tutor-card\.js'),
]
ANCHOR = re.compile(
    r'([ \t]*<script[^>]*src="(?:\.\./\.\./)?assets/scripts/teachany-[a-z-]+\.js"[^>]*>\s*</script>)', re.I)


def targets():
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
            if 'id="slide-sidenav"' not in h:
                continue
            need = [n for n, pat in WANT if not re.search(pat, h)]
            if need:
                out.append((c.name, f, need))
    return out


def add(f, need):
    h = f.read_text(encoding='utf-8')
    tags = ''.join(f'  <script src="../../assets/scripts/{n}" defer></script>\n' for n in need)
    m = None
    for m in ANCHOR.finditer(h):
        pass                      # 取最后一个匹配（共享脚本块尾部）
    if m:
        h = h[:m.end()] + '\n' + tags + h[m.end():]
    else:
        i = h.rfind('</body>')
        if i < 0:
            return False
        h = h[:i] + tags + h[i:]
    f.write_text(h, encoding='utf-8')
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--apply', action='store_true')
    a = ap.parse_args()
    t = targets()
    if a.list or not a.apply:
        print(f'缺脚本引用的课件：{len(t)} 门')
        for cid, _, need in t[:15]:
            print(f'   {cid:40s} 缺 {", ".join(need)}')
        if len(t) > 15:
            print(f'   … 及另外 {len(t)-15} 门')
        if not a.apply:
            print('\n加 --apply 实际写入')
        return 0
    ok = 0
    for cid, f, need in t:
        if add(f, need):
            ok += 1
    print(f'已补 {ok}/{len(t)} 门')
    return 0


if __name__ == '__main__':
    sys.exit(main())
