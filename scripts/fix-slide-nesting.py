#!/usr/bin/env python3
"""fix-slide-nesting.py — 修复 slide-page 互相嵌套（模板生成缺陷，影响 90.6% 课件）

缺陷：幻灯片页 <section class="slide-page"> 之间不应嵌套，但模板生成时
常漏写页尾闭合标签，导致：
    第1页 <section class="slide-page">   ← 缺 </section>
      第2页 <section class="slide-page"> ← 被嵌套进第1页内部
        ...
后果：整页 DOM 层层嵌套，卡片背景/边框错误地包裹后续所有内容，
间距与层级样式逐级劣化。

修复：遇到新的 slide-page 时，若上一个 slide-page 仍未闭合，
则在其前按栈逆序补全缺失的闭合标签（保持浏览器既有渲染层级不变——
浏览器也是在此处隐式闭合，补全只是将其显式化）。

用法: python3 fix-slide-nesting.py [cid...]   不传则修全库
      python3 fix-slide-nesting.py --dry      只报告不修改
      python3 fix-slide-nesting.py --tail     额外在 </body> 前补全残余未闭合容器
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
# svg 内部元素由 svg 自身闭合，不参与结构补全
SKIP_CLOSE = {"svg", "defs", "g"}

# 安全护栏：只允许生成这些真实 HTML 标签的闭合，
# 杜绝把 class 名（如 slide-page）误当成标签名写入文件
VALID_CLOSE = {
    "html", "body", "head", "div", "section", "article", "aside", "nav",
    "header", "footer", "main", "figure", "figcaption", "ul", "ol", "li",
    "p", "span", "a", "table", "thead", "tbody", "tr", "td", "th",
    "form", "label", "button", "select", "option", "textarea", "details",
    "summary", "dl", "dt", "dd", "blockquote", "pre", "code", "video",
    "audio", "picture", "template", "style", "script", "noscript",
}


# slide-page 开标签：`[^>]*` 可跨行匹配，位置由正则直接给出，绝对精确
SLIDE_RE = re.compile(r"<section\b[^>]*>", re.I)
SCRIPT_RE = re.compile(r"<script\b[\s\S]*?</script>", re.I)


def script_ranges(html):
    """返回所有 <script> 区块的 (start, end)，用于过滤 JS 内的伪标签"""
    return [(m.start(), m.end()) for m in SCRIPT_RE.finditer(html)]


def in_ranges(idx, ranges):
    return any(s <= idx < e for s, e in ranges)


def slide_positions(html):
    """定位真实 slide-page 开标签，跳过 <script> 内 JS 字符串里的伪标签"""
    rs = script_ranges(html)
    return [m.start() for m in SLIDE_RE.finditer(html)
            if "slide-page" in m.group(0) and not in_ranges(m.start(), rs)]


def make_closers(tags):
    """生成闭合标签串，跳过非法标签名并返回实际生成的数量"""
    out = []
    for t in tags:
        if t in VALID_CLOSE:
            out.append(f"</{t}>")
    return "".join(out), len(out)


# 损坏模式：闭合标签被插进另一个标签的属性中间，如
#   <div class="x" r</section>ole="status">
# 特征：开标签未闭合（缺 '>'）就出现了闭合标签，且其后紧跟属性字符
CORRUPT_RE = re.compile(r"<[a-zA-Z][^<>]*></(?:section|div|figure)>[a-zA-Z=\"']")


def is_corrupt(html):
    """检查是否被插入位置错误而破坏（闭合标签落在他人标签内部）

    必须先剔除 <script>：JS 字符串常含 HTML 片段
    （如 innerHTML='<div class="qz">'+x+'</div>'+y+'<div ...'），
    会被误判为「闭合标签插在标签中间」。
    """
    body = SCRIPT_RE.sub("", html)
    return bool(CORRUPT_RE.search(body))


class SlideNest(HTMLParser):
    """记录每个 slide-page 开标签处需要补全的闭合标签

    只记录「第几个 slide-page 需要补、补什么」，不记录字符位置——
    位置改由正则精确匹配得出，避免 getpos() 在标签跨行或含实体引用时
    推算出错误的插入点（曾导致闭合标签被插入 <div ... r|</section>|ole="x"> 中间）。
    """

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []          # [(tag, is_slide)]
        self.fixups = []         # [(ordinal, [需补tag...])]  ordinal 从 1 起
        self.ordinal = 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        d = dict(attrs)
        # 注意：栈中一律存「标签名」，slide-page 只是 class，绝不能当标签名用
        is_slide = (tag == "section" and "slide-page" in (d.get("class") or ""))
        if is_slide:
            self.ordinal += 1
            j = self._prev_slide()
            if j is not None:
                # 上一个 slide-page 未闭合 → 补全到该层（含它自身）
                need = [t for t, _ in reversed(self.stack[j:]) if t not in SKIP_CLOSE]
                if need:
                    self.fixups.append((self.ordinal, need))
                self.stack = self.stack[:j]
            self.stack.append((tag, True))
        else:
            self.stack.append((tag, False))

    def _prev_slide(self):
        """返回栈中最内层未闭合 slide-page 的下标，无则 None"""
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][1]:
                return i
        return None

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.stack = self.stack[:i]
                return


# 结构标签：括号匹配只针对这三类，避免 svg 内部元素干扰
STRUCT = {"div", "section", "figure"}


def unclosed_by_bracket(html):
    """用括号匹配找出 </body> 前仍未闭合的结构标签（按出现顺序）

    比 HTMLParser 更可靠：HTMLParser 的「截断到匹配位置」语义会把交叉嵌套中的
    未闭合元素一并丢弃，导致漏检（例如 slide-container 永远查不出来）。
    """
    body = html
    m = re.search(r"</body>", html, re.I)
    if m:
        body = html[:m.start()]
    stack = []
    for mm in re.finditer(r"<(/?)(div|section|figure)\b", body, re.I):
        closing, tag = bool(mm.group(1)), mm.group(2).lower()
        if closing:
            if stack and stack[-1] == tag:
                stack.pop()
            # 不匹配（交叉嵌套）时忽略该闭标签，保持栈稳定
        else:
            stack.append(tag)
    return stack


def fix(cid, dry=False, tail=False):
    P = COMMUNITY / cid / "index.html"
    html = P.read_text(encoding="utf-8", errors="replace")
    lines = html.split("\n")

    s = SlideNest()
    s.feed(html)
    # 无 slide 嵌套时仍需继续：尾部计数差（如 slide-container 漏闭）也要补
    if not s.fixups and not tail:
        return None

    n = 0
    if s.fixups:
        # 用正则精确定位每个 slide-page 开标签的起始索引（跳过 script 内伪标签）
        pos = slide_positions(html)

        # 缺失额度：每类标签的补全量不得超过其原始缺失数。
        # 否则对「计数已配平、仅嵌套关系错」的课件会补多，反而破坏配平。
        deficit = {}
        for t in ("section", "div", "figure"):
            o = len(re.findall(rf"<{t}\b", html))
            c = len(re.findall(rf"</{t}>", html))
            deficit[t] = max(0, o - c)

        # 由后往前插入，避免索引偏移
        for ordinal, need in sorted(s.fixups, reverse=True):
            if ordinal - 1 >= len(pos):
                continue
            allowed = []
            for t in need:
                if deficit.get(t, 0) > 0:
                    allowed.append(t)
                    deficit[t] -= 1
            closers, _ = make_closers(allowed)
            if not closers:
                continue
            idx = pos[ordinal - 1]
            html = html[:idx] + closers + html[idx:]
            n += 1

    tail_n = 0
    if tail:
        # 按「计数差」补全最外层残留容器（如 slide-container）。
        # 不用括号匹配：原文存在交叉嵌套时，括号匹配会把大量正常标签误判为未闭合，
        # 导致过度补全（实测会多补 6~8 个）。
        # 生成顺序 figure → div → section，保证由内到外闭合。
        need = []
        for tag in ("figure", "div", "section"):
            o = len(re.findall(rf"<{tag}\b", html))
            c = len(re.findall(rf"</{tag}>", html))
            need += [tag] * max(0, o - c)
        if need:
            closers, tail_n = make_closers(need)
            m = re.search(r"\s*</body>", html)
            if m and closers:
                html = html[:m.start()] + "\n" + closers + html[m.start():]

    # 安全护栏：写入前确认没有把闭合标签插进别的标签内部
    if not dry:
        if is_corrupt(html):
            return {"pages": n, "tail": tail_n, "rejected": True}
        P.write_text(html, encoding="utf-8")
    return {"pages": n, "tail": tail_n, "rejected": False}


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

    tp = sum(r["pages"] for _, r in done)
    tt = sum(r["tail"] for _, r in done)
    rj = [c for c, r in done if r.get("rejected")]
    print(f"扫描 {len(cids)}：修复 {len(done)}（补页尾 {tp} 处"
          f"{f'，尾部补全 {tt} 个' if tail else ''}），无此问题 {skipped}，失败 {len(failed)}"
          f"，护栏拦截 {len(rj)}")
    if rj:
        print(f"  ⚠ 以下课件检测到插入位置异常，已拒绝写入：{', '.join(rj[:5])}")
    if dry:
        print("（--dry 模式，未写入文件）")
    for cid, r in done[:8]:
        print(f"  {cid:<40} 补页尾{r['pages']}处"
              + (f" 尾部补{r['tail']}个" if tail else ""))
    if len(done) > 8:
        print(f"  ... 另 {len(done)-8} 个")
    for cid, e in failed[:5]:
        print(f"  ❌ {cid}: {e}")


if __name__ == "__main__":
    main()
