#!/usr/bin/env python3
"""apply-pretest-b4.py — 写入第 4 批课前诊断题（人工撰写，非模板生成）

本文件内容由我（模型）逐题撰写：先读课件正文弄清它真正教什么、学生
容易错在哪，再出题。脚本只负责搬运成 HTML。

与 add-missing-modules.py 的 pretest_block 区别：那个用「{知识点}与{主题}
完全无关」之类空壳拼选项，知识点一错整句就荒谬；这里每题的题干、三个
选项、错因诊断都是针对该课真实误区写的。

正确项在 A/B/C 间轮换，避免学生按位置猜答案。
"""
import re
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

# cid → (题干, [(选项文本, 是否正确)], 错因诊断)
DATA = {
    "chn-m-literary-appreciation": (
        "鉴赏文学作品时，所谓「表达效果」指的是？",
        [("文章写了哪些内容", False),
         ("作者用了什么写法，以及这样写带来什么作用", True),
         ("作者的生平经历", False)],
        "表达效果关注的是「怎么写」和「这样写有什么好处」，即写作手法及其作用。"
        "概括文章内容是「写了什么」，作者生平属于创作背景，两者都不是表达效果。",
    ),
    "chn-m-narrative-reading": (
        "阅读记叙文时，概括主要内容通常要抓住什么？",
        [("主要人物和主要事件", True), ("环境描写的句子", False),
         ("文章中的修辞句", False)],
        "概括记叙文要抓住「谁做了什么、结果如何」，也就是主要人物和主要事件。"
        "环境描写、修辞句属于表达上的细节，不能替代对主要内容的概括。",
    ),
    "chn-m-narrative-writing-m": (
        "写记叙文时，最能突出中心的做法是？",
        [("每件事都写得一样详细", False), ("多用成语和华丽的词句", False),
         ("把经过写具体，并围绕中心安排详略", True)],
        "详略要根据中心来定：与中心关系密切的地方详写，关系不大的略写。平均"
        "用笔会让重点被淹没，堆砌华丽词句同样不能突出中心。",
    ),
    "chn-m-novel-reading": (
        "小说的三要素是？",
        [("时间、地点、人物", False), ("人物、情节、环境", True),
         ("开头、经过、结尾", False)],
        "小说三要素是人物、情节、环境。时间地点属于记叙文六要素，开头经过结尾"
        "是事情发展的顺序，两组概念经常混淆，要分清所属文体。",
    ),
    "chn-m-poetry-appreciation": (
        "赏析一首古诗词，第一步通常应该做什么？",
        [("读懂诗句字面意思，把握写了什么", True), ("先分析作者用了什么手法", False),
         ("查找作者的生平", False)],
        "赏析要从读懂诗句入手，先弄清写了什么内容、描绘了什么景象，再进一步"
        "分析手法和情感。跳过内容直接谈手法，赏析就会架空。",
    ),
    "chn-m-poetry-comparison": (
        "比较两首古诗词时，最核心的比较点是？",
        [("判断哪一首写得更好", False), ("比较两首诗的字数多少", False),
         ("在内容和写法上找出异同，并说明原因", True)],
        "比较阅读要围绕同一个比较点（如情感、意象、手法）找出异同，并结合文本"
        "说明原因。简单评判高下或比较字数，都不是真正的比较阅读。",
    ),
    "chn-m-poetry-imagery": (
        "古诗词中的「意象」指的是什么？",
        [("诗中的人物形象", False), ("融入了作者情感的客观物象", True),
         ("诗歌的押韵方式", False)],
        "意象是融入了作者主观情感的客观物象，如「月」常寄托思念、「柳」常寓"
        "送别。多个意象组合在一起就形成意境。它既不是人物形象，也不是格律。",
    ),
    "chn-m-poetry-recitation": (
        "默写古诗文时，避免写错别字最有效的办法是？",
        [("多抄写几遍", False), ("理解字句意思后再背诵", True), ("只背名句", False)],
        "理解字句含义后再背诵，能避免同音字、形近字混淆（如「雁」与「燕」）。"
        "机械抄写容易动手不动脑，只背名句则应付不了整篇默写。",
    ),
    "chn-m-poetry-techniques": (
        "「感时花溅泪，恨别鸟惊心」主要运用了什么手法？",
        [("借景抒情（寓情于景）", True), ("对比", False), ("夸张", False)],
        "诗人把感伤之情移到花、鸟上，说花「溅泪」、鸟「惊心」，是典型的借景"
        "抒情（移情于物）。句中并没有两相对照，也没有故意放大。",
    ),
    "chn-m-prose-reading": (
        "阅读散文时，把握作者情感最关键的是抓什么？",
        [("文章用了多少种修辞", False), ("段落的长短", False),
         ("文中的抒情议论句和反复出现的细节", True)],
        "散文的情感常由抒情议论句直接点明，或寄托在反复出现的细节里。统计修辞"
        "数量、看段落长短都与体会情感没有直接关系。",
    ),
    "chn-m-rhetoric-analysis": (
        "赏析一个比喻句，最完整的思路是？",
        [("指出把什么比作什么", False), ("说明这里用了比喻", False),
         ("指出把什么比作什么，并说明它生动形象地写出了什么特点", True)],
        "赏析修辞要答全三步：判断手法、结合内容具体说明、点明表达效果（写出了"
        "什么特点或情感）。只答手法名称，或只说「比作什么」，都不完整。",
    ),
    "chn-m-rhetoric-figures": (
        "「教室里安静得连一根针掉在地上都听得见」运用了什么修辞？",
        [("比喻", False), ("夸张", True), ("拟人", False)],
        "这句话故意把安静的程度往大里说，属于夸张。比喻要有本体和喻体，拟人"
        "是把物当人来写，这句里两者都没有出现。",
    ),
}


def block(q, opts, diag):
    letters = "ABC"
    btns = ""
    for i, (text, ok) in enumerate(opts):
        L = letters[i]
        corr = ' data-correct="1"' if ok else ""
        d = f' data-diag="{escape(diag)}"' if ok else ""
        btns += (f'<button class="quiz-option" data-q="pre" data-a="{L}"'
                 f'{corr}{d}>{L}. {escape(text)}</button>')
    return (f'\n<section class="section text-module" id="pretest" '
            f'data-bloom-level="remember" data-scaffold="full" data-tts="pretest">'
            f'<div class="panel"><span class="phase-tag">Pretest</span>'
            f'<h2>📝 课前诊断：先暴露一个误区</h2><p>{escape(q)}</p>{btns}'
            f'<div class="feedback" id="fb-pre">选择后显示错因诊断。</div>'
            f'</div></section>\n')


def put(html, frag):
    """插到 objectives 之后，没有则放 hero 后，再没有则 body 前"""
    for sid in ("objectives", "hero-infographic"):
        m = re.search(rf'<section\b[^>]*\bid="{sid}"[^>]*>', html)
        if m:
            end = html.find("</section>", m.end())
            if end > 0:
                return html[:end + 10] + frag + html[end + 10:]
    m = re.search(r"\s*</body>", html)
    if m:
        return html[:m.start()] + frag + html[m.start():]
    return None


def main():
    dry = "--dry" in sys.argv
    n = 0
    for cid, (q, opts, diag) in DATA.items():
        P = COMMUNITY / cid / "index.html"
        if not P.exists():
            print(f"  ⚠ 不存在 {cid}")
            continue
        html = P.read_text(encoding="utf-8", errors="replace")
        if re.search(r'<section\b[^>]*\bid="pretest"', html):
            print(f"  跳过（已有）{cid}")
            continue
        new = put(html, block(q, opts, diag))
        if new is None:
            print(f"  ⚠ 无插入点 {cid}")
            continue
        if not dry:
            P.write_text(new, encoding="utf-8")
        n += 1
    print(f"写入 {n} 个课前诊断题" + ("（--dry 未写入）" if dry else ""))


if __name__ == "__main__":
    main()
