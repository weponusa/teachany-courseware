#!/usr/bin/env python3
"""apply-pretest-b5.py — 写入第 5 批课前诊断题（人工撰写，非模板生成）

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
    "chn-m-sentence-components": (
        "「小明在教室里认真地读书」一句中，「在教室里」是什么成分？",
        [("状语", True), ("定语", False), ("补语", False)],
        "「在教室里」表示读书的地点，修饰动词「读」，是状语。定语修饰名词"
        "（如「安静的教室」里的「安静」），补语补充说明动作的结果或程度，"
        "两者都与这里的作用不同。",
    ),
    "chn-m-sentence-logic": (
        "填入横线最恰当的关联词是：「____天下着大雨，他还是准时到了。」",
        [("因为", False), ("如果", False), ("虽然", True)],
        "「下大雨」和「准时到达」在意思上是转折关系，用「虽然……还是……」最贴切。"
        "「因为」表因果，「如果」表假设，放进句里都会让逻辑讲不通。",
    ),
    "chn-m-sentence-transformations-zh": (
        "把「他完成了作业」改成被动句，正确的是？",
        [("作业被他完成了", True), ("他被作业完成了", False), ("作业把他完成了", False)],
        "被动句强调受事者，格式是「受事＋被＋施事＋动作」。「作业」是被完成的"
        "对象，应作主语；另两句都把施事和受事的关系弄反了。",
    ),
    "chn-m-whole-book-reading": (
        "读整本书时，下列做法最有助于把握全书内容的是？",
        [("只看自己感兴趣的章节", False),
         ("先读目录了解结构，再按计划通读", True),
         ("只读书评和故事梗概", False)],
        "目录能帮你先建立全书框架，再通读才能形成整体理解。只读部分章节容易"
        "片面，只看梗概则跳过了作品本身的语言和内容，都不能代替读原著。",
    ),
    "chn-m-word-usage": (
        "表示「毫不犹豫地」接受任务，横线上最恰当的词是？",
        [("居然", False), ("偶然", False), ("毅然", True)],
        "「毅然」表示坚决果断、毫不犹豫；「居然」表示出乎意料，「偶然」表示"
        "事理上不一定要发生。三个词意思差别很大，选词要看具体语境。",
    ),
    "eng-e-consonant-sounds": (
        "下列字母中，属于辅音字母的是？",
        [("b", True), ("a", False), ("e", False)],
        "英语字母分为元音字母（a、e、i、o、u）和辅音字母（其余字母）。b 是"
        "辅音字母，a 和 e 都属于元音字母。",
    ),
    "eng-e-listening-speaking": (
        "当你没听清对方说什么时，最礼貌的说法是？",
        [("What?", False), ("Pardon? / Could you say that again?", True),
         ("I don't know.", False)],
        "没听清时应说「Pardon?」或「Could you say that again, please?」，语气"
        "礼貌。直接说「What?」显得生硬；「I don't know.」是「我不知道」，"
        "属于答非所问。",
    ),
    "eng-e-phonics-consonants": (
        "单词 cat 中，字母 c 发什么音？",
        [("/s/", False), ("/t/", False), ("/k/", True)],
        "字母 c 在 a、o、u 前通常发 /k/，如 cat、cup；在 e、i、y 前常发 /s/，"
        "如 city、nice。cat 里 c 后面跟的是 a，所以发 /k/。",
    ),
    "eng-e-phonics-vowels": (
        "单词 cake 中的元音字母 a 发什么音？",
        [("/æ/", False), ("/eɪ/", True), ("/ɑː/", False)],
        "cake 属于「元音＋辅音＋不发音的 e」结构：词尾的 e 不发音，前面的 a 读"
        "字母本身的音 /eɪ/。而 cat 里的 a 发短音 /æ/，两者要分清。",
    ),
    "eng-e-vowel-sounds": (
        "英语中通常被称为元音字母的是哪一组？",
        [("a, e, i, o, u", True), ("b, c, d, f, g", False),
         ("a, e, i, o, u 和 y", False)],
        "英语有 5 个元音字母：a、e、i、o、u。字母 y 有时起元音的作用，但通常"
        "不列入元音字母；其余字母都是辅音字母。",
    ),
    "ext-72948119-truss-topology": (
        "在理想的桁架结构中，杆件主要承受什么力？",
        [("弯矩", False), ("扭矩", False), ("沿杆轴方向的拉力或压力", True)],
        "桁架的理想化假定是节点铰接、荷载只作用在节点上，因此杆件只承受沿杆轴"
        "的拉力或压力。弯矩、扭矩主要出现在梁、轴这类构件里，分析时要注意"
        "两种受力模型的区别。",
    ),
    "ext-7be00e85": (
        "纸张的纤维方向对其抗弯挺度有什么影响？",
        [("没有影响", False), ("顺纹方向更容易弯折，横纹方向更挺", True),
         ("横纹方向更容易弯折", False)],
        "纸张纤维沿抄造方向排列：顺纹方向容易弯折、挺度低；横纹方向纤维彼此"
        "支撑，挺度更高。做纸桥时合理安排纤维方向，能明显提高承载能力。",
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
