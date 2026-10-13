#!/usr/bin/env python3
"""Append one topic-specific 常见误区 paragraph to chn-m depth sections.

Run after upgrade-chn-m-depth.py. Several courses still fall a little short of
the 1800-char effective-text threshold; this adds a substantive misconception
note inside the existing lesson-method card. Idempotent via id="lesson-pitfall".
"""
from __future__ import annotations

import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

PITFALLS = {
    "chn-m-classical-appreciation": "常见误区是把鉴赏写成翻译，只复述文意而不谈情感与写法；或空喊“语言优美、感情真挚”却不引原文分析。正确做法是先概括情感志趣，再引具体语句佐证，最后点明手法的表达效果，做到观点、依据、分析三者齐备。",
    "chn-m-classical-prose": "常见误区是被生僻字词绊住，逐句翻译却理不清全文脉络，也分不清哪些是叙事、哪些是议论抒情。应先用一句话概括写了什么事、抒了什么情，再找过渡句和点旨句画出结构，把景、事与作者态度对应起来理解。",
    "chn-m-classical-sentences": "常见误区是只凭语感翻译，忽略特殊句式，导致语序错乱、成分缺失。要先判断句式类型，宾语前置需把宾语移回动词后，状语后置需前移，省略成分要补全，再按现代汉语习惯组织语句，做到既忠实又通顺。",
    "chn-m-classical-translation": "常见误区是随意意译、增删原意，或把古今异义词按今义硬套。翻译要以直译为主，落实关键实词、活用与句式这些采分点，用“留删补换调”逐字处理，最后通读润色，切忌漏译、错译或凭想象改写。",
    "chn-m-classical-words": "常见误区是死记单一义项，遇到语境变化就套错义，或把古今异义词当今义理解。应结合上下文语境推断词义，善用结构对称和成语印证，虚词按用法分类积累，做题时把选项代回原句验证是否通顺合理。",
    "chn-m-argumentative-writing-m": "常见误区是“观点加例子”两张皮，摆了事例却不分析，或论点不集中、论据不典型。举例后一定要扣住论点作分析，说明事例为何能证明观点；分论点要围绕中心展开，综合运用多种论证方法增强说服力。",
    "chn-m-descriptive-writing": "常见误区是堆砌“美丽、漂亮”等空泛形容词，笼统概括而缺少画面感。描写要抓住对象特征，调动多种感官，选取传神细节精雕细刻，并把情感融入景物，做到情景交融，让读者如见其形、如闻其声。",
    "chn-m-narrative-writing-m": "常见误区是记流水账，事事都写却平均用力，中心不突出。应围绕中心选材，最能表现中心的情节详写，其余略写；用动作、语言、神态、心理等细节把人物写活，做到以小见大，开头结尾相呼应。",
    "chn-m-essay-comprehensive": "常见误区是不审题就动笔，抓不住关键词和限制条件，写着写着就偏题跑题。动笔前应四步审题、列好提纲，规划每段内容与过渡；写作紧扣中心选材，完成后通读检查是否切题、结构是否完整顺畅。",
    "chn-m-expository-reading": "常见误区是把说明文当记叙文读，只关注内容而忽略说明方法和语言的准确性。分析说明方法要指出方法名称并说清其作用；品味语言要关注“大约、左右”等词体现的准确性，说明删去后表意会发生怎样的变化。",
    "chn-m-narrative-reading": "常见误区是只复述故事情节，抓不住线索和作者情感，答赏析题只写“生动形象”而不结合内容。应先理清线索概括情节，再品析关键词句和细节的表达效果，联系上下文体会人物形象与文章主旨。",
    "chn-m-novel-reading": "常见误区是只看热闹情节，脱离描写空谈人物性格，或忽视环境描写的作用。分析人物要有具体描写作依据，说明情节的巧妙安排如何服务主题，并结合社会环境理解作者意图，把三要素与主题勾连起来。",
    "chn-m-prose-reading": "常见误区是被“形散”迷惑，觉得材料零散抓不住中心。要先找文眼和抒情议论句明确“神”，再分析各段材料如何从不同侧面表现中心，理解看似松散的内容其实统一于作者的情感与主旨。",
    "chn-m-literary-appreciation": "常见误区是赏析只会说“写得好、很生动”，却讲不出好在哪里。赏析语句要先指出修辞、用词或描写角度等手法，再分析它写出了什么、表达了什么情感、有什么效果，并用文本细节印证自己的审美判断。",
    "chn-m-whole-book-reading": "常见误区是把整本书读成若干片段，缺少整体把握，读完记不住人物关系和结构。应边读边圈点批注、绘制人物关系与情节脉络图，读完围绕一个专题搜集全书证据、比较分析，形成有依据的阅读发现。",
    "chn-m-comprehensive-language": "常见误区是把综合性学习做成抄资料、走过场，缺少真实的实践与合作。开展活动要明确主题目标、分工协作、制订计划，注重搜集资料和规范表达，最后整理成果展示交流并反思收获，做到既动脑又动手。",
    "chn-m-poetry-appreciation": "常见误区是脱离意象空谈情感，或只翻译诗句而不品意境。鉴赏要先找出主要意象、描摹画面，体会营造的意境氛围，联系诗人处境把握情感，再赏析炼字与手法，答题先点情感再引诗句佐证。",
    "chn-m-poetry-comparison": "常见误区是只分别赏析两首诗而不真正比较，或比较点不明确、泛泛而谈。应先确定意象、情感、手法、风格等比较角度，逐项对照异同，再归纳造成差异的原因，分点作答并各自引诗句为证。",
    "chn-m-poetry-imagery": "常见误区是生硬套用意象的固定含义，脱离具体诗境理解，或把普通景物都当意象。应结合语境判断景物是否寄托情感，由象入境、由境悟情，说明诗人借此意象组合表达的具体思想感情。",
    "chn-m-poetry-recitation": "常见误区是不理解诗意就一味求快求流利，节奏含混、情感平淡。诵读前应划分节奏、标出重音和韵脚，把握诗歌的情感基调，再用轻重缓急、抑扬顿挫的语调反复吟诵，做到声情并茂、以声传情。",
    "chn-m-poetry-techniques": "常见误区是只答出手法名称却不分析效果，或张冠李戴分不清相近手法。赏析要先准确判断手法，再结合诗句说明它写出了什么、表达了什么情感、有什么效果，做到手法、内容、效果三者齐全、言之有据。",
    "chn-m-rhetoric-analysis": "常见误区是只写“运用了比喻”便草草结束，不结合句子内容分析效果。赏析修辞句要先指出修辞格，再说明它把什么写得怎样、表达了什么情感，最后点明表达效果，做到有辨识、有分析、有落实。",
    "chn-m-rhetoric-figures": "常见误区是混淆相近修辞，如把借代当比喻、把反问当设问。判断要抓各自特征：比喻本体喻体有相似关系，借代以相关事物代替；设问自问自答，反问只问不答表强调，逐一比对特征再下结论。",
    "chn-m-sentence-components": "常见误区是分不清主干与附加成分，把定语、状语误当主干，导致病句判断出错。应先抓主谓宾主干，再借助“的、地、得”识别定语、状语、补语，理清成分后判断搭配是否得当、成分是否残缺。",
    "chn-m-sentence-logic": "常见误区是关联词误用或搭配错乱，如“因为……但是”，以及语序不当、前后矛盾。应先判断分句间的逻辑关系，再选用匹配的关联词，检查时留意语序、关联词和事理是否合乎逻辑并加以修改。",
    "chn-m-sentence-transformations-zh": "常见误区是变换句式时改变了原意，或引语转换忘改人称和标点。变换前先明确目标句式和原句意思，按规则调整语气或结构，变换后回读确认意思没变、语句通顺，这是句式变换不可逾越的底线。",
    "chn-m-word-usage": "常见误区是只凭语感选词，忽略词义轻重、感情色彩和适用对象，导致褒贬误用或对象错位。辨析近义词要比较细微差别并结合语境选最贴切的一个，判断成语是否恰当也要看含义、色彩与对象是否与语境一致。",
    "chn-m-dream-red-mansions": "常见误区是只当言情故事看，理不清庞杂的人物关系，也读不出作品的批判意味。应抓住宝黛爱情与贾府兴衰的主线，绘制人物关系图，结合判词与诗词理解人物命运，体会作品深沉的悲剧意蕴与社会批判。",
    "chn-m-journey-west": "常见误区是只看打斗热闹，忽视人物性格和作品寓意。阅读应从三打白骨精等典型情节分析孙悟空等人物性格，透过神魔故事体会对现实的影射，理解作品惩恶扬善、追求理想与歌颂坚韧的精神内涵。",
    "chn-m-erta-essay-collection": "常见误区是零散地读单篇，读完记不住作者的整体风格和思想倾向。应在精读代表篇目、品味语言情感的基础上，横向比较各篇主题与写法，归纳作者一贯的风格，围绕自然、亲情等专题整合全集内容。",
    "chn-m-erta-foreign-novel": "常见误区是脱离时代背景理解人物，用本土经验硬套异域故事，读不出文化差异。应先了解作者与社会背景，分析人物性格的社会成因，关注叙事视角与艺术特色，并与中国小说比较题材写法的异同。",
    "chn-m-erta-stories": "常见误区是只记住有趣情节，读完却说不出故事的道理和情感。应能简要复述故事的起因、经过、结果，分析人物在事件中的表现与成长，提炼其中蕴含的道理，并联系生活谈自己的真实感受。",
    "chn-m-erta-tales-heroes": "常见误区是只崇拜英雄的武艺，忽略人物性格的丰富性和作品颂扬的精神。应抓住表现人物的典型情节，从言行分析英雄的性格特征，比较不同英雄的异同，领会作品所歌颂的忠义、勇敢与反抗精神。",
}


def patch(course_id: str, text: str) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-pitfall"' in source:
        return False, "already patched"
    anchor = '<div class="worked-example">'
    idx = source.find(anchor)
    if idx < 0:
        return False, "worked-example anchor not found"
    para = (
        f'<p id="lesson-pitfall" class="chnm-pitfall">'
        f'<strong>常见误区：</strong>{html.escape(text)}</p>\n      '
    )
    source = source[:idx] + para + source[idx:]
    path.write_text(source, encoding="utf-8")
    return True, "pitfall paragraph added"


def main() -> int:
    changed = failed = 0
    for course_id, text in PITFALLS.items():
        ok, msg = patch(course_id, text)
        if ok:
            changed += 1
        elif msg == "already patched":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
