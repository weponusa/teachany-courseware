#!/usr/bin/env python3
"""apply-pretest-b3.py — 写入第 3 批课前诊断题（人工撰写，非模板生成）

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
    "chn-m-classical-translation": (
        "翻译文言文句子时，下列做法最准确的是？",
        [("用现代汉语逐字替换，原文字一个都不动", False),
         ("直译为主，补出省略、调整倒装，使句子通顺", True),
         ("只要把大意写出来，不必管具体字句", False)],
        "文言翻译讲求「信、达、雅」：先要字字落实（信），再补出省略的成分、把"
        "倒装的语序顺过来使语句通顺（达）。只写大意会丢掉关键字的得分点，"
        "逐字硬译则往往读不通。",
    ),
    "chn-m-classical-words": (
        "关于文言实词和虚词，下列说法正确的是？",
        [("实词有实在意义（如名词、动词），虚词主要起连接、语气等作用", True),
         ("实词没有实在意义，虚词才有", False),
         ("虚词数量比实词多，也更重要", False)],
        "实词有实在的词汇意义，包括名词、动词、形容词等；虚词没有完整的词汇"
        "意义，主要起语法作用，如副词、介词、连词、助词。文言文中实词数量远"
        "多于虚词。",
    ),
    "chn-m-comprehensive-language": (
        "综合性学习中拟写宣传标语，最关键的是？",
        [("语言华丽，多用成语", False), ("字数越多，内容越显得完整", False),
         ("紧扣主题，简洁有力、让人容易记住", True)],
        "标语要在极短篇幅内传达核心信息，因此必须紧扣主题、简洁上口。堆砌辞藻"
        "或写得太长，反而让人抓不住重点、记不住。",
    ),
    "chn-m-descriptive-writing": (
        "下列句子中，属于细节描写的是哪一句？",
        [("他是一个善良的人", False), ("他的手很粗糙", False),
         ("他用粗糙的手轻轻擦去桌上的灰尘", True)],
        "细节描写是对动作、神态等作具体细致的刻画。第一句是概括评价，第二句"
        "只是简单形容，第三句用「轻轻擦」这个动作把特点具体化，才是细节描写。",
    ),
    "chn-m-dream-red-mansions": (
        "《红楼梦》的作者是？",
        [("罗贯中", False), ("施耐庵", False), ("曹雪芹", True)],
        "《红楼梦》前八十回为清代曹雪芹所著，后由高鹗续补整理。罗贯中著《三国"
        "演义》，施耐庵著《水浒传》，三部古典名著的作者不要混淆。",
    ),
    "chn-m-erta-essay-collection": (
        "散文最重要的特点，通常被概括为哪一句？",
        [("形散神聚", True), ("情节曲折", False), ("语言华丽", False)],
        "散文取材广博、写法灵活（形散），但始终围绕一个中心情感或主旨（神聚）。"
        "追求情节曲折是小说、戏剧的特点，语言华丽也并非散文的必备特征。",
    ),
    "chn-m-erta-foreign-novel": (
        "《海底两万里》的作者是？",
        [("儒勒·凡尔纳", True), ("笛福", False), ("高尔基", False)],
        "《海底两万里》是法国作家儒勒·凡尔纳的科幻小说；笛福著有《鲁滨逊漂流"
        "记》，高尔基是苏联作家，代表作有《童年》《海燕》。",
    ),
    "chn-m-erta-stories": (
        "《朝花夕拾》的体裁是？",
        [("回忆性散文集", True), ("短篇小说集", False), ("杂文集", False)],
        "《朝花夕拾》收录鲁迅回忆童年和青年时期生活的十篇文章，属于回忆性散文"
        "集。它并非虚构的小说，而是以作者自身经历为素材写成的。",
    ),
    "chn-m-erta-tales-heroes": (
        "《骆驼祥子》中祥子的「三起三落」主要说明了什么？",
        [("只要个人奋斗就能改变命运", False), ("命运不好，只能认命", False),
         ("旧社会不让好人有出路，单靠个人奋斗无法改变命运", True)],
        "祥子勤劳要强却一次次被打回原点，小说正是通过他的堕落揭示旧社会对底层"
        "劳动者的摧残。读成「努力就能成功」或「只能认命」，都偏离了作品主题。",
    ),
    "chn-m-essay-comprehensive": (
        "写考场作文前先列提纲，主要作用是？",
        [("让卷面看起来更整齐", False),
         ("确定中心和层次，避免写着写着偏题", True),
         ("能凑够规定的字数", False)],
        "提纲解决的是「写什么、按什么顺序写」，能保证中心明确、层次清楚，防止"
        "中途偏题。它对卷面整洁和字数多少并没有直接作用。",
    ),
    "chn-m-expository-reading": (
        "说明文中使用「列数字」的说明方法，主要作用是？",
        [("使文章更生动有趣", False), ("增加文章的篇幅", False),
         ("使说明更准确、更有说服力", True)],
        "列数字用具体数据准确地说明事物的特征，增强说服力。使说明更生动通常是"
        "打比方、拟人等说明方法的作用，不属于列数字。",
    ),
    "chn-m-journey-west": (
        "《西游记》中，孙悟空的第一个师傅是？",
        [("唐僧", False), ("菩提祖师", True), ("太上老君", False)],
        "孙悟空学艺时的师傅是菩提祖师，教他七十二变和筋斗云；唐僧是他取经路上"
        "的师父。太上老君并未收他为徒，两者不是师徒关系。",
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
