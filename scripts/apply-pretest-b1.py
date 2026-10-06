#!/usr/bin/env python3
"""apply-pretest-b1.py — 写入第 1 批课前诊断题（人工撰写，非模板生成）

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
    "chn-e-dictionary-skills": (
        "小明遇到一个字，会读但不会写，他应该用哪种查字法？",
        [("部首查字法", False), ("数笔画查字法", False), ("音序查字法", True)],
        "知道读音用音序查字法；知道字形、不知道读音用部首查字法；"
        "既读不出音又难定部首才用数笔画查字法。三种方法要看清前提条件。",
    ),
    "chn-e-essay-structure": (
        "一篇完整的文章，最基本的结构是哪三部分？",
        [("开头—正文—结尾", True), ("时间—地点—人物", False), ("起因—经过—结果", False)],
        "时间地点人物是记叙文六要素里的三个，起因经过结果是事情发展的顺序，"
        "说的都是「写了什么」；而文章结构指的是开头、正文、结尾怎么安排。",
    ),
    "chn-e-figurative-language": (
        "下列句子中，使用了「拟人」的是哪一句？",
        [("月亮像一个大玉盘", False), ("月亮悄悄爬上了树梢", True), ("月亮又大又圆", False)],
        "拟人是把事物当成人来写，「悄悄爬」是人的动作；「像玉盘」是把一物比作"
        "另一物，属于比喻。区分关键：有没有出现人的动作、神态或情感。",
    ),
    "chn-e-listen-speak-basic": (
        "别人说话的时候，我们应该怎么做？",
        [("眼睛看着对方，认真听", True), ("马上插嘴说自己想说的", False), ("一边玩一边听", False)],
        "听的基本要求是专心：眼睛看着对方、不打断。插嘴会让对方说不完，"
        "边玩边听则容易漏掉内容，两种做法都听不清别人在说什么。",
    ),
    "chn-e-main-idea-summary": (
        "概括一篇文章的主要内容，最合适的方法是？",
        [("把每段第一句抄下来", False), ("把文章从头到尾缩写成一句话", False),
         ("抓住主要人物和主要事件", True)],
        "抄各段首句会漏掉藏在段落中间的重要信息；全篇缩写容易变成复述、越长越啰嗦。"
        "概括要抓主要人物和主要事件，次要情节一律舍去。",
    ),
    "chn-e-narrative-writing": (
        "写记叙文时，事情的「经过」应该怎么写？",
        [("一句话带过就行", False), ("写具体，分步骤写清楚", True), ("只写结果不写过程", False)],
        "经过是记叙文的核心，最能体现事情的意义，要写具体、分步骤。"
        "只写结果或一笔带过，读者就不知道事情是怎么发生的。",
    ),
    "chn-e-nasal-vowels": (
        "下面哪一个是鼻韵母？",
        [("an", True), ("a", False), ("ai", False)],
        "鼻韵母以 n 或 ng 结尾，an 是前鼻韵母；a 是单韵母，ai 是复韵母。"
        "判断时看结尾有没有鼻音，而不是看字母多少。",
    ),
    "chn-e-oral-presentation": (
        "上台发言时，下列做法最恰当的是？",
        [("低着头小声说", False), ("背对大家看着黑板说", False), ("声音响亮，看着大家说", True)],
        "口头表达要声音响亮、面向听众。低头小声大家听不见，背对听众则看不到你的"
        "表情和口型，都会影响表达效果。",
    ),
    "chn-e-paragraph-analysis": (
        "一段话中，能概括整段主要意思的句子叫什么？",
        [("总起句", False), ("中心句", True), ("过渡句", False)],
        "中心句概括段落的主要意思；总起句在段首引出下文，过渡句负责承上启下。"
        "中心句可能在段首、段中或段尾，要通读全段再判断。",
    ),
    "chn-e-paragraph-structure": (
        "一段话常见的结构方式是哪一组？",
        [("总分、分总、总分总", True), ("开头、中间、结尾", False), ("时间、地点、人物", False)],
        "总分、分总、总分总说的是一段内部的组织方式；开头中间结尾是整篇文章的"
        "结构，时间地点人物是记叙要素，层级不同，不要混用。",
    ),
    "chn-e-paragraph-writing": (
        "一个完整的段落中，用来具体说明总起句的句子是？",
        [("总结句", False), ("过渡句", False), ("支撑句", True)],
        "总起句提出要说的意思，支撑句用事例、细节把它说清楚，总结句收束全段。"
        "写段落时支撑句要围绕总起句展开，不能写着写着就跑题。",
    ),
    "chn-e-parts-of-speech": (
        "下列词语中，全部属于动词的一组是？",
        [("美丽、高大、聪明", False), ("奔跑、思考、歌唱", True), ("桌子、铅笔、教室", False)],
        "动词表示动作、行为或心理活动；「美丽、高大、聪明」是形容词，用来描写"
        "样子或性质；「桌子、铅笔、教室」是表示事物名称的名词。",
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
