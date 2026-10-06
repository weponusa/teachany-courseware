#!/usr/bin/env python3
"""apply-pretest-b2.py — 写入第 2 批课前诊断题（人工撰写，非模板生成）

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
    "chn-e-pathological-sentence": (
        "下列句子没有语病的是哪一句？",
        [("通过这次活动，使我明白了许多道理", False),
         ("我们要不断改进学习方法，提高学习效率", True),
         ("他经常回忆过去的往事", False)],
        "第一句用「通过…使…」两个介词短语连用，句子就没有主语了，删去「通过」"
        "或「使」即可；第三句「过去的」和「往事」的「往」意思重复。第二句搭配"
        "恰当，没有语病。",
    ),
    "chn-e-poetry-appreciation": (
        "欣赏一首古诗时，理解诗意最重要的第一步是？",
        [("把诗里每个字都查一遍字典", False), ("先把诗背下来", False),
         ("读懂关键字词，再想象画面", True)],
        "古诗语言凝练，先弄懂关键字词的意思，再把它们连成画面，才能体会意境。"
        "不理解的背诵只记住了声音，谈不上鉴赏；逐字查字典则容易只顾字面、"
        "丢了整体。",
    ),
    "chn-e-poetry-recitation": (
        "背诵古诗时，记得又快又牢的方法是？",
        [("一句一句读顺，理解意思后再背", True), ("一口气把整首读二十遍", False),
         ("只背第一句和最后一句", False)],
        "先一句一句读顺、弄懂意思，再连起来背，记得牢也不容易串。不理解地死读"
        "很多遍，当下会背，过几天就忘；只背首尾则根本背不全。",
    ),
    "chn-e-rhetoric-in-writing": (
        "在作文中使用比喻，最主要的作用是？",
        [("把事物写得具体可感、更生动", True), ("让文章的字数变多", False),
         ("显得自己词汇量大", False)],
        "比喻是为了把陌生、抽象的事物写得具体可感，让读者仿佛亲眼看见。单纯堆"
        "砌修辞来凑字数或炫耀词汇，反而会让文章显得空洞、不自然。",
    ),
    "chn-e-sentence-types": (
        "「这里的风景真美啊！」这句话属于哪种句子类型？",
        [("疑问句", False), ("感叹句", True), ("祈使句", False)],
        "句末用感叹号、表达赞美或强烈感情的是感叹句；提出问题是疑问句，提出"
        "请求或发出命令的是祈使句。判断时既要看语气，也要看句末标点。",
    ),
    "chn-e-syllable-spelling": (
        "一个汉语音节一般由哪几部分组成？",
        [("声母、韵母、字母", False), ("元音、辅音、声调", False),
         ("声母、韵母、声调", True)],
        "音节由声母、韵母和声调三部分组成。字母是书写单位，元音辅音是语音学的"
        "说法，小学阶段按声母、韵母、声调来记最清楚。",
    ),
    "chn-e-tang-poetry": (
        "唐诗在句式上最常见的特点是？",
        [("每句五字或七字，全诗四句或八句", True), ("每句三字，全诗两句", False),
         ("每句字数多少都可以", False)],
        "唐诗中的绝句四句、律诗八句，每句多为五言或七言。句式整齐、讲究平仄和"
        "押韵，是唐诗形式上的重要特点，也是它读起来朗朗上口的原因。",
    ),
    "chn-m-argumentative-reading": (
        "阅读议论文时，判断作者观点的依据是什么？",
        [("文章里举的例子", False), ("作者在文中明确表达的主张", True),
         ("文章最后的号召", False)],
        "论点是作者明确表达的主张，通常是一个完整的陈述句，常在标题、开头或"
        "结尾出现。举的例子属于论据，是用来证明论点的，不能把论据当成论点。",
    ),
    "chn-m-argumentative-writing-m": (
        "写议论文时，论据的主要作用是？",
        [("让文章的篇幅更长", False), ("把道理讲得生动有趣", False),
         ("用来证明论点是成立的", True)],
        "议论文讲究以理服人，论点必须靠论据来支撑。论据要真实、典型，并且与"
        "论点一致；只堆材料不分析，即使写得很长也说不服人。",
    ),
    "chn-m-classical-appreciation": (
        "鉴赏文言文时，理解句意最基础的一步是？",
        [("弄清重点实词和虚词的意思", True), ("先把全文背诵下来", False),
         ("查找作者的生平经历", False)],
        "文言文的字词含义与现代汉语差别较大，先落实重点实词、虚词，才能准确"
        "翻译句子、读懂内容。作者生平属于拓展了解，不能替代对文本本身的理解。",
    ),
    "chn-m-classical-prose": (
        "翻译文言文句子时，最常用的方法是？",
        [("逐字对译，一个字都不调整", False), ("保留原文，不做任何补充", False),
         ("以直译为主，适当调整语序、补充省略", True)],
        "文言文常有成分省略和语序倒装，翻译时要以直译为主，把省略的成分补出来、"
        "把倒装的语序顺过来，句子才通顺。逐字硬译往往读不通。",
    ),
    "chn-m-classical-sentences": (
        "下列句子中，属于宾语前置的一句是？",
        [("甚矣，汝之不惠", False), ("何陋之有", True), ("一鼓作气，再而衰", False)],
        "「何陋之有」就是「有何陋」，疑问代词作宾语时要前置；「甚矣，汝之不惠」"
        "是主谓倒装，谓语「甚矣」提前表示强调；「再而衰」是省略句，「再」后面"
        "省略了「鼓」。",
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
