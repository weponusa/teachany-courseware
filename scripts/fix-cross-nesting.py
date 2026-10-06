#!/usr/bin/env python3
"""fix-cross-nesting.py — 修复课件 HTML 的标签交叉嵌套（模板生成缺陷）

缺陷模式（浏览器会隐式闭合，导致外层容器永远等不到闭合）：
    <figure ...>        ← figure 在外
      <section ...>     ← section 在内
        ...内容...
    </figure>           ← 却先闭 figure → 浏览器隐式闭合 section，
  </section>            ← 随后的 </section> 成为孤儿被丢弃

后果：card / slide-inner / slide-page 等外层容器残留未闭合，
整页后续内容被错误嵌套进第一个卡片内（影响 210 个课件）。

判定方式：用栈精确配对——遇到 </figure> 时若栈顶不是 figure（而是 section
等内层元素），即判定为交叉嵌套。不能用"第一个 </figure> 与 </section> 谁先出现"
来判定：嵌套双 figure（figure A > section > figure B）时，首个 </figure> 属于
内层 B，属正常嵌套，简单比较会误判。

修复：在 </figure> 之前，按栈逆序补全该 figure 之上所有未闭合元素的闭合标签。

用法: python3 fix-cross-nesting.py [cid...]   不传则修全库
      python3 fix-cross-nesting.py --dry      只报告不修改
      python3 fix-cross-nesting.py --tail     额外在 </body> 前补全残余未闭合容器
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

VOID = {"br", "hr", "img", "input", "meta", "link", "source", "area", "base",
        "col", "embed", "track", "wbr", "path", "circle", "rect", "line",
        "polyline", "polygon", "ellipse", "stop", "use", "text"}


class Finder(HTMLParser):
    """定位交叉嵌套：遇到 </figure> 时栈顶不是 figure"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.hits = []          # [(pos_of_</figure>, [需补的tag...])]

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append(tag)

    def _endpos(self):
        # </figure> 的起始位置：handle_endtag 时 getpos() 指向 '>' 之后，
        # 因此开标签起始 = 当前位置 - len('</figure>')
        ln, off = self.getpos()
        return ln, off

    def handle_endtag(self, tag):
        if tag == "figure" and self.stack and self.stack[-1] != "figure":
            if "figure" in self.stack:
                i = len(self.stack) - 1 - self.stack[::-1].index("figure")
                need = list(reversed(self.stack[i + 1:]))
                self.hits.append((self._endpos(), need))
                self.stack = self.stack[:i]
                return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                self.stack = self.stack[:i]
                return


class Leftover(HTMLParser):
    """解析到 </body> 时仍未闭合的元素"""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.left = None

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append(tag)

    def handle_endtag(self, tag):
        if tag == "body":
            self.left = [t for t in self.stack if t not in ("html", "body")]
            self.stack = []
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i] == tag:
                self.stack = self.stack[:i]
                return


def pos_to_index(lines, ln, off):
    """(行号, 列偏移) → 全局字符索引"""
    return sum(len(l) + 1 for l in lines[:ln - 1]) + off


def fix(cid, dry=False, tail=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")

    f = Finder()
    f.feed(html)
    if not f.hits:
        return None
    lines = html.split("\n")

    # 由后往前插入，避免索引偏移
    cross = 0
    for (ln, off), need in sorted(f.hits, reverse=True):
        idx = pos_to_index(lines, ln, off) - len("</figure>")
        if html[idx:idx + 9] != "</figure>":
            continue
        closers = "".join(f"</{t}>" for t in need)
        html = html[:idx] + closers + html[idx:]
        cross += 1

    added_tail = 0
    if tail:
        b = Leftover()
        b.feed(html)
        if b.left:
            closers = "".join(f"</{t}>" for t in reversed(b.left))
            m = re.search(r"\s*</body>", html)
            if m:
                html = html[:m.start()] + "\n" + closers + html[m.start():]
                added_tail = len(b.left)

    if not dry and (cross or added_tail):
        P.write_text(html, encoding="utf-8")
    return {"cross": cross, "tail": added_tail}


def main():
    dry = "--dry" in sys.argv
    tail = "--tail" in sys.argv
    cids = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not cids:
        cids = sorted(p.name for p in COMMUNITY.iterdir()
                      if (p / "index.html").exists())

    done, skipped, failed = [], 0, []
    for cid in cids:
        try:
            r = fix(cid, dry, tail)
            if r is None:
                skipped += 1
            else:
                done.append((cid, r))
        except Exception as e:
            failed.append((cid, str(e)[:60]))

    tc = sum(r["cross"] for _, r in done)
    tt = sum(r["tail"] for _, r in done)
    print(f"扫描 {len(cids)}：修复 {len(done)}（交叉 {tc} 处"
          f"{f'，尾部补全 {tt} 个' if tail else ''}），无此问题 {skipped}，失败 {len(failed)}")
    if dry:
        print("（--dry 模式，未写入文件）")
    for cid, r in done[:10]:
        print(f"  {cid:<40} 交叉{r['cross']}处"
              + (f" 尾部补{r['tail']}个" if tail else ""))
    if len(done) > 10:
        print(f"  ... 另 {len(done)-10} 个")
    for cid, e in failed[:5]:
        print(f"  ❌ {cid}: {e}")


if __name__ == "__main__":
    main()
