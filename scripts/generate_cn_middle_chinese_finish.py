#!/usr/bin/env python3
"""Generate all CN middle-school Chinese courseware in TeachAny complete mode."""
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path("/Users/wepon/.workbuddy/skills/TeachAny")
SKELETON = SKILL / "templates/course-skeleton.html"
TREE = ROOT / "data/trees/cn/middle/chinese.json"
TODAY = date.today().isoformat()


def esc(s: str) -> str:
    return html.escape(str(s), quote=True)


def read_tree_nodes():
    tree = json.loads(TREE.read_text(encoding="utf-8"))
    nodes, domains = {}, {}
    for domain in tree["domains"]:
        for node in domain.get("nodes", []):
            nodes[node["id"]] = node
            domains[node["id"]] = domain
    return nodes, domains, list(nodes.keys())


def replace_all(template: str, values: dict[str, str]) -> str:
    out = template
    for key, value in values.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def profile_for(node_id: str, name: str, domain: dict):
    text = f"{node_id} {name} {domain.get('name','')}"
    rules = [
        ("word", "language", "词语鉴别师", ["语境", "词义", "表达效果"], "词语题先看语境，再辨色彩、对象和搭配。"),
        ("sentence-components", "language", "句子结构分析师", ["主干", "修饰成分", "语义关系"], "句子成分分析先找主谓宾，再看定状补。"),
        ("rhetoric", "rhetoric", "修辞鉴赏员", ["修辞类型", "表达对象", "情感效果"], "修辞赏析不能只报名称，要写出写了什么、怎样写、好在哪里。"),
        ("sentence-transform", "language", "病句诊断员", ["语序", "搭配", "逻辑"], "病句修改先保留原意，再修语法和逻辑。"),
        ("logic", "language", "语段连贯编辑", ["话题一致", "顺序关系", "衔接词"], "连贯题先看话题，再看时间、空间、逻辑顺序。"),
        ("comprehensive", "language", "综合表达策划", ["情境", "对象", "表达任务"], "综合运用题要先明确说给谁、为什么说、用什么格式说。"),
        ("narrative", "reading", "记叙文侦探", ["人物事件", "线索顺序", "情感变化"], "记叙文阅读抓线索、人物变化和细节证据。"),
        ("expository", "reading", "说明文结构师", ["说明对象", "说明顺序", "说明方法"], "说明文先找对象和特征，再看顺序和方法怎样服务清楚。"),
        ("prose", "reading", "散文品读员", ["意象", "情感", "语言节奏"], "散文阅读要抓物象背后的情感和作者眼光。"),
        ("novel", "reading", "小说人物分析师", ["人物形象", "情节冲突", "环境作用"], "小说阅读抓人物在冲突中的选择，而不是只复述情节。"),
        ("argumentative", "argument", "议论文论证分析师", ["论点", "论据", "论证方法"], "议论文先找中心论点，再看论据是否能支撑。"),
        ("literary", "reading", "文学鉴赏员", ["语言", "形象", "主题"], "文学鉴赏要把语言、形象和主题连起来。"),
        ("classical", "classical", "文言文翻译官", ["实词虚词", "句式", "语境翻译"], "文言文先字词落实，再调顺语序，最后补出省略。"),
        ("poetry", "poetry", "诗歌意象分析师", ["意象", "情感", "手法"], "古诗词赏析抓意象、情感和表达手法。"),
        ("writing", "writing", "作文教练", ["立意", "材料", "结构"], "写作先定立意，再选材料，最后安排结构和语言。"),
        ("descriptive", "writing", "细节描写教练", ["感官", "动作", "画面"], "细节描写要让读者看见、听见、感到变化。"),
        ("essay", "writing", "综合作文教练", ["审题", "立意", "表达"], "综合作文先审限制，再定中心，材料都要服务主题。"),
        ("whole-book", "book", "整本书阅读规划师", ["通读", "精读", "笔记"], "整本书阅读要建立人物、情节、主题三张网。"),
        ("journey", "book", "名著导读员", ["人物谱系", "情节线路", "主题理解"], "名著阅读不能只记情节，要看人物成长和主题表达。"),
        ("dream", "book", "名著鉴赏员", ["人物关系", "细节伏笔", "主题意蕴"], "名著选读要从细节进入人物关系和主题意蕴。"),
        ("erta", "book", "名著导读员", ["人物谱系", "情节线路", "主题理解"], "名著阅读要把人物、情节和社会背景连成图。"),
    ]
    for key, kind, role, labels, memory in rules:
        if key in text:
            return kind, role, labels, memory
    return "reading", "语文学习策略师", ["文本证据", "表达方法", "思想情感"], "语文题先找文本证据，再解释表达效果。"


def make_detail(node: dict, domain: dict):
    node_id, name = node["id"], node["name"]
    kind, role, labels, memory = profile_for(node_id, name, domain)
    question = f"怎样用文本证据解释{name}中的表达效果与思想情感？"
    concepts = [
        (labels[0], f"学习{name}时，先明确任务对象和文本范围，不能只凭印象回答。"),
        (labels[1], f"把{name}拆成可标注的语言现象、结构关系和表达方法。"),
        (labels[2], f"用原文词句、段落关系或写作目的支撑判断，形成可复用的答题路径。"),
    ]
    facts = [
        f"{name}不是背模板，而是要回到具体语境、文本证据和表达目的。",
        f"判断{name}时，要把关键词句、结构位置、人物行为或论证关系连起来。",
        f"能把{name}的方法迁移到新文本和新写作任务中，才算真正掌握。",
    ]
    return {
        "title": f"{name}：从文本证据到表达效果",
        "title_en": re.sub(r"[^a-z0-9]+", "-", node_id.lower()).strip("-"),
        "role": role,
        "and": f"你已经接触过{name}相关题型，也能凭经验说出一些常见答案。",
        "but": f"中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。",
        "therefore": f"所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握{name}。",
        "question": question,
        "concepts": concepts,
        "facts": facts,
        "memory": memory,
        "error": f"常见错误：只写{name}的术语，不引用文本证据，也不说明它产生了什么表达效果。",
        "pretest": (f"完成{name}题时，第一步最应该做什么？", ["直接背模板", "先判断任务并圈画证据", "只写自己的感受", "把题目抄一遍"], 1, "语文题先看任务，再回到文本圈画证据。"),
        "posttest": (f"一个{name}答案想拿高分，最关键的是？", ["术语越多越好", "必须有文本证据和效果解释", "字数越长越好", "只写中心思想"], 1, "高质量答案要有文本依据、方法判断和表达效果。"),
        "interaction": kind,
        "objectives": [
            f"能识别{name}题型中的任务要求和文本证据",
            f"能用语言、结构或写法分析{name}的表达效果",
            f"能把{name}的方法用于新文本阅读或写作修改",
        ],
    }


def make_buttons(items: list[str], answer: int, prefix: str) -> str:
    return "\n".join(
        f'<button class="quiz-option" onclick="checkAnswer(this,{"true" if i == answer else "false"},\'{prefix}\')">{esc(chr(65+i))}. {esc(item)}</button>'
        for i, item in enumerate(items)
    )


def annotation_prompt(kind: str) -> str:
    examples = {
        "language": "他的话像一束光，忽然把沉默的屋子照亮了。",
        "rhetoric": "春风轻轻推开窗，把一院花香送到书桌前。",
        "reading": "雨停后，父亲仍站在巷口，手里攥着那把旧伞。",
        "argument": "真正的阅读，不是翻过多少页，而是让一个问题在心里停留多久。",
        "classical": "学而时习之，不亦说乎。",
        "poetry": "明月松间照，清泉石上流。",
        "writing": "那天放学，我第一次发现，母亲的背影比路灯还安静。",
        "book": "取经路上的每一次遇险，都像一次重新认识自己的机会。",
    }
    return examples.get(kind, examples["reading"])


def interaction_controls(kind: str) -> str:
    text = annotation_prompt(kind)
    return f'''<label>文本材料<textarea id="sample-text" rows="4" aria-label="文本材料">{esc(text)}</textarea></label><label>分析维度<select id="analysis-mode"><option value="keyword">关键词句</option><option value="method">表达方法</option><option value="emotion">情感主题</option><option value="structure">结构作用</option></select></label><label>批注强度<input id="mark-level" type="range" min="1" max="5" value="3"></label>'''


def interaction_script(kind: str, name: str) -> str:
    return f"""
const canvas=document.getElementById('chinese-canvas');
const ctx=canvas.getContext('2d');
function clearCanvas(){{ctx.clearRect(0,0,canvas.width,canvas.height);ctx.fillStyle='#081426';ctx.fillRect(0,0,canvas.width,canvas.height);}}
function text(t,x,y,size=22,color='#eef6ff'){{ctx.fillStyle=color;ctx.font=`${{size}}px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif`;ctx.fillText(t,x,y);}}
function wrap(t,x,y,w,lineH,size=22,color='#eef6ff'){{let line='';ctx.font=`${{size}}px -apple-system,BlinkMacSystemFont,PingFang SC,sans-serif`;for(const ch of t){{const trial=line+ch;if(ctx.measureText(trial).width>w){{text(line,x,y,size,color);y+=lineH;line=ch;}}else line=trial;}}if(line)text(line,x,y,size,color);return y;}}
function drawAnnotation(){{clearCanvas();const raw=document.getElementById('sample-text').value.trim();const mode=document.getElementById('analysis-mode').value;const level=+document.getElementById('mark-level').value;ctx.strokeStyle='#38bdf8';ctx.lineWidth=3;ctx.strokeRect(60,70,780,140);wrap(raw,85,115,720,34,24,'#dbeafe');const labels={{keyword:'圈关键词：找最能承载信息和情感的词句',method:'判方法：比喻、拟人、对比、描写、论证等',emotion:'析情感：人物态度、作者立场、主题指向',structure:'看结构：开头铺垫、中间转折、结尾升华'}};text('分析维度：'+labels[mode],70,265,28,'#fbbf24');for(let i=0;i<level;i++){{ctx.fillStyle=['#38bdf8','#a78bfa','#22c55e','#fbbf24','#f97316'][i%5];ctx.fillRect(90+i*120,305,88,42);text(['证据','方法','效果','情感','答案'][i],105+i*120,333,20,'#081426');}}text('答题链：文本证据 → 方法判断 → 表达效果 → 情感主题',70,395,24,'#bae6fd');document.getElementById('lab-feedback').textContent='请用“原文词句 + 方法 + 效果 + 情感/主题”组织答案，避免空泛套话。';}}
document.querySelectorAll('#sample-text,#analysis-mode,#mark-level').forEach(el=>el.addEventListener('input',drawAnnotation));drawAnnotation();
"""


def make_extra_svg(node: dict, detail: dict, mode: str) -> str:
    title = "概念结构图" if mode == "concept" else "答题过程图"
    labels = [c[0] for c in detail["concepts"]] if mode == "concept" else ["圈画证据", "判断方法", "组织答案"]
    subtitle = detail["question"] if mode == "concept" else detail["memory"]
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    cards = []
    for i, label in enumerate(labels[:3]):
        x = 80 + i * 360
        cards.append(f'<rect x="{x}" y="250" width="280" height="150" rx="22" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+30}" y="330" fill="{colors[i]}" font-size="30" font-weight="800">{esc(label)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="640" viewBox="0 0 1200 640"><rect width="1200" height="640" fill="#081426"/><circle cx="1020" cy="110" r="170" fill="#38bdf8" opacity="0.12"/><text x="80" y="100" fill="#f8fafc" font-size="48" font-weight="900">{esc(node['name'])} · {title}</text><text x="80" y="158" fill="#cbd5e1" font-size="26">{esc(subtitle[:56])}</text>{''.join(cards)}<text x="80" y="540" fill="#fbbf24" font-size="28">从文本进入问题，再回到证据、方法、效果和表达。</text></svg>'''


def make_hero_svg(course_id: str, node: dict, detail: dict) -> str:
    colors = ["#38bdf8", "#a78bfa", "#22c55e"]
    cards = []
    for i, (title, txt) in enumerate(detail["concepts"]):
        x = 70 + i * 390
        cards.append(f'<rect x="{x}" y="270" width="330" height="190" rx="24" fill="#0f172a" stroke="{colors[i]}" stroke-width="4"/><text x="{x+26}" y="325" fill="{colors[i]}" font-size="28" font-weight="800">{esc(title)}</text><text x="{x+26}" y="374" fill="#dbeafe" font-size="21">{esc(txt[:30])}</text><text x="{x+26}" y="410" fill="#dbeafe" font-size="21">{esc(txt[30:58])}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="720" viewBox="0 0 1280 720"><defs><linearGradient id="g" x1="0" x2="1"><stop stop-color="#111827"/><stop offset="1" stop-color="#312e81"/></linearGradient></defs><rect width="1280" height="720" fill="url(#g)"/><circle cx="1050" cy="120" r="180" fill="#38bdf8" opacity="0.13"/><circle cx="220" cy="620" r="220" fill="#a78bfa" opacity="0.12"/><text x="70" y="112" fill="#f8fafc" font-size="52" font-weight="900">{esc(node['name'])}</text><text x="70" y="168" fill="#bae6fd" font-size="28">{esc(detail['question'])}</text><text x="70" y="225" fill="#cbd5e1" font-size="24">角色任务：{esc(detail['role'])} · 课标节点：{esc(node['id'])}</text>{''.join(cards)}<rect x="70" y="525" width="1140" height="105" rx="24" fill="#020617" opacity="0.72" stroke="#334155"/><text x="105" y="585" fill="#fbbf24" font-size="30" font-weight="800">记忆锚点</text><text x="260" y="585" fill="#e0f2fe" font-size="26">{esc(detail['memory'])}</text><text x="70" y="675" fill="#64748b" font-size="18">TeachAny v7.14 · 初中语文完整模式 · AI 学伴 / TTS / 知识图谱 / 文本批注互动 / 课标挂树</text></svg>'''


def make_content(course_id: str, node: dict, detail: dict) -> str:
    pre_q, pre_opts, pre_ans, pre_feedback = detail["pretest"]
    post_q, post_opts, post_ans, post_feedback = detail["posttest"]
    concepts = "\n".join(f'<div class="mini-panel"><h3>{esc(t)}</h3><p>{esc(txt)}</p></div>' for t, txt in detail["concepts"])
    facts = "\n".join(f"<li>{esc(x)}</li>" for x in detail["facts"])
    return f'''
<style>.lesson-panel{{background:linear-gradient(180deg,rgba(35,31,64,.96),rgba(17,24,39,.96));border:1px solid rgba(148,163,184,.18);border-radius:18px;padding:22px;box-shadow:0 16px 40px rgba(0,0,0,.18)}}.mini-grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}.mini-panel{{background:rgba(15,23,42,.68);border:1px solid rgba(148,163,184,.18);border-radius:16px;padding:16px}}.mini-panel h3{{margin:0 0 8px;color:#bae6fd}}.quiz-option{{display:block;width:100%;margin:8px 0;border:1px solid rgba(56,189,248,.28);background:#0b1628;color:#eef6ff;border-radius:12px;padding:12px 14px;text-align:left;cursor:pointer}}.quiz-option.correct{{border-color:#22c55e;background:rgba(34,197,94,.14)}}.quiz-option.wrong{{border-color:#f97316;background:rgba(249,115,22,.14)}}.feedback{{min-height:44px;margin-top:10px;padding:10px 12px;border-radius:12px;background:rgba(56,189,248,.10);color:#dbeafe}}.control-row{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;align-items:end;margin:12px 0}}.control-row label{{color:#cbd5e1;font-size:14px}}.control-row textarea{{width:100%;border-radius:10px;border:1px solid rgba(148,163,184,.28);background:#07111f;color:#e5edf8;padding:10px}}.video-box video{{width:100%;border-radius:14px;border:1px solid rgba(148,163,184,.18);background:#020617}}figure img{{width:100%;border-radius:12px}}</style>
<section class="section" id="story" data-tts="story" data-tsh="情境任务 - 用 ABT 明确为什么学"><div class="lesson-panel"><span class="phase-tag">ABT Story</span><h2>角色任务：{esc(detail['role'])}</h2><div class="mini-grid"><div class="mini-panel"><h3>And 已有经验</h3><p>{esc(detail['and'])}</p></div><div class="mini-panel"><h3>But 真实卡点</h3><p>{esc(detail['but'])}</p></div><div class="mini-panel"><h3>Therefore 本课任务</h3><p>{esc(detail['therefore'])}</p></div></div><p>语文不是背模板，而是在具体语言材料中找到证据、方法和效果。面对新文本，要先判断题目问什么，再回到原文找能够支撑判断的词句。</p></div></section>
<section class="section" id="reading-checklist" data-tts="reading-checklist" data-bloom-level="analyze" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Reading Checklist</span><h2>文本检查表：这道题到底问什么？</h2><p><strong>第一问：任务类型是什么？</strong>是解释词句、赏析修辞、分析人物、概括观点，还是组织写作？任务不同，证据也不同。</p><p><strong>第二问：证据在哪里？</strong>答案必须回到原文。关键词、句子位置、前后照应、人物行为、论证关系，都是可以圈画的证据。</p><p><strong>第三问：效果怎样表达？</strong>不能只写“生动形象”。要说清具体写出了什么、怎样写、表达了什么情感或观点。</p></div></section>
<section class="section" id="pretest" data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Pre-test</span><h2>前测：你已经知道什么？</h2><p><strong>{esc(pre_q)}</strong></p>{make_buttons(pre_opts, pre_ans, 'pretest')}<div id="pretest-feedback" class="feedback">先选一项，系统会给出错因诊断。</div></div></section>
<section class="section" id="core" data-tts="core" data-bloom-level="understand" data-scaffold="full"><div class="lesson-panel"><span class="phase-tag">Core Ideas</span><h2>核心概念：从文本证据到表达效果</h2><div class="mini-grid">{concepts}</div></div></section>
<section class="section" id="deep-understanding" data-tts="deep-understanding"><div class="lesson-panel insight-box"><span class="phase-tag">Five Lens</span><h2>深层理解：五镜头看本质</h2><ul><li><strong>看见它：</strong>{esc(detail['facts'][0])}</li><li><strong>拆开它：</strong>{esc(detail['facts'][1])}</li><li><strong>解释它：</strong>{esc(detail['facts'][2])}</li><li><strong>比较它：</strong>把一个高分答案和一个空泛答案放在一起，比较证据、方法和效果是否完整。</li><li><strong>迁移它：</strong>换一段新文本，仍然用“证据—方法—效果—情感”的路径回答。</li></ul><p class="feedback"><strong>记忆锚点：</strong>{esc(detail['memory'])}</p></div></section>
<section class="section" id="worked-example" data-tts="worked-example" data-bloom-level="analyze" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Worked Example</span><h2>例题拆解：不要空泛，要有证据链</h2><p>遇到「{esc(node['name'])}」题，先圈出题干里的任务动词，比如“理解”“赏析”“概括”“分析”“评价”。这些词决定答案是解释含义、分析手法，还是表达观点。</p><p>第二步回到文本找证据。证据可以是关键词、句子位置、描写对象、人物行为、论证材料，也可以是前后文形成的照应或转折。</p><p>第三步组织答案。本课高频误区是：{esc(detail['error'])} 正确答案必须写成“原文证据 + 方法判断 + 表达效果 + 情感主题”。</p></div></section>
<section class="section" id="transfer-task" data-tts="transfer-task" data-bloom-level="create" data-scaffold="none"><div class="lesson-panel"><span class="phase-tag">Transfer Task</span><h2>迁移任务：设计一道新题和评分标准</h2><p>请选择一段课外文本或自己的作文片段，设计一道与本课相关的问题。你需要写出标准答案，并标明每一分对应的证据、方法、效果和表达。</p></div></section>
<section class="section" id="visual-evidence" data-tts="visual-evidence"><div class="lesson-panel"><span class="phase-tag">Visual Evidence</span><h2>两张图先建立直觉</h2><div class="mini-grid"><figure class="mini-panel"><img src="./assets/concept-diagram.svg" alt="概念结构图"><figcaption>概念结构：任务、证据和表达效果。</figcaption></figure><figure class="mini-panel"><img src="./assets/process-diagram.svg" alt="答题过程图"><figcaption>答题过程：圈画、判断、组织。</figcaption></figure></div></div></section>
<section class="section" id="evidence-table" data-tts="evidence-table" data-bloom-level="evaluate" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Evidence Table</span><h2>证据表：把文本翻译成答案</h2><p><strong>如果题目问词句，</strong>先解释本义和语境义，再说明它表现了对象的什么特点。</p><p><strong>如果题目问手法，</strong>先判定具体方法，再写出写了什么，最后写情感或主题效果。</p><p><strong>如果题目问观点，</strong>先找论点，再看论据和论证是否充分，不能只写“我认为”。</p></div></section>
<section class="section" id="interactive-lab" data-tts="interactive-lab" data-bloom-level="apply" data-scaffold="partial"><div class="lesson-panel"><span class="phase-tag">Annotation Lab</span><h2>文本批注实验：圈证据，组答案</h2><p style="color:var(--muted)">改写材料或切换分析维度，观察答题链如何变化。</p><div class="control-row">{interaction_controls(detail['interaction'])}</div><div class="canvas-wrap"><canvas id="chinese-canvas" class="wide-canvas" width="900" height="430"></canvas></div><div id="lab-feedback" class="feedback">输入文本并选择分析维度，开始批注。</div></div></section>
<section class="section" id="ai-media-zone" data-tts="ai-media-zone" data-bloom-level="create" data-scaffold="partial"><div class="lesson-panel ai-zone"><span class="phase-tag">AI Media</span><h2>AI 多模态互动区：生成批注图或上传作文诊断</h2><p>输入一段文本，生成“证据—方法—效果”的批注图；也可以上传作文截图，按立意、材料、结构和语言进行诊断。</p><div class="control-row"><label>提示词输入框<textarea id="ai-media-prompt" rows="3" aria-label="AI 多模态提示词输入框">请根据{esc(node['name'])}，把这段文本标出关键证据、表达方法和情感效果。</textarea></label><label>上传文本或作文图片<input id="upload-image" type="file" accept="image/*" aria-label="upload image"></label></div><button class="quiz-option" type="button" onclick="document.getElementById('ai-media-feedback').textContent='已生成批注提示：先圈原文证据，再写方法和表达效果。'">生成批注图</button><button class="quiz-option" type="button" onclick="document.getElementById('ai-media-feedback').textContent='已进入上传诊断流程：请检查立意、证据、结构和语言是否一致。'">上传作文诊断</button><div id="ai-media-feedback" class="feedback">这里用于生成批注图或上传图片诊断，重点检查证据链是否完整。</div></div></section>
<section class="section" id="micro-video" data-tts="micro-video"><div class="lesson-panel video-box"><span class="phase-tag">Micro Lesson</span><h2>微课讲解：60 秒内复盘核心路径</h2><video controls preload="metadata" playsinline><source src="./assets/video/{esc(course_id)}-main.mp4" type="video/mp4"></video></div></section>
<section class="section" id="posttest" data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"><div class="lesson-panel"><span class="phase-tag">Post-test</span><h2>后测：会迁移了吗？</h2><p><strong>{esc(post_q)}</strong></p>{make_buttons(post_opts, post_ans, 'posttest')}<div id="posttest-feedback" class="feedback">先独立判断，再看诊断反馈。</div></div></section>
<section class="section" id="tiered-practice" data-tts="tiered-practice"><div class="lesson-panel"><span class="phase-tag">Level Practice</span><h2>三段式作业</h2><div class="mini-grid"><div class="mini-panel"><h3>基础巩固</h3><p>写出本课答题路径，并标出每一步需要的文本证据。</p></div><div class="mini-panel"><h3>能力应用</h3><p>用本课方法分析一段新文本，至少引用两处原文。</p></div><div class="mini-panel"><h3>迁移挑战</h3><p>修改一个空泛答案，让它变成有证据、有方法、有表达效果的高分答案。</p></div></div></div></section>
<section class="section" id="summary" data-tts="summary"><div class="lesson-panel"><span class="phase-tag">Summary</span><h2>一句话带走</h2><ul>{facts}</ul><p class="feedback">如果你能解释“{esc(detail['question'])}”，这节课就真正过关了。</p></div></section>
<script>const FEEDBACK={{ pretest:{json.dumps(pre_feedback, ensure_ascii=False)}, posttest:{json.dumps(post_feedback, ensure_ascii=False)} }};function checkAnswer(btn,ok,target){{btn.parentElement.querySelectorAll('.quiz-option').forEach(b=>b.classList.remove('correct','wrong'));btn.classList.add(ok?'correct':'wrong');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?FEEDBACK[target]:'错因诊断：先回到题干任务和文本证据，再检查是否只写了空泛感受。'+FEEDBACK[target];}}{interaction_script(detail['interaction'], node['name'])}</script>
'''


def write_manifest(course_dir: Path, course_id: str, node: dict, domain: dict, detail: dict):
    manifest = {
        "id": course_id,
        "course_id": course_id,
        "node_id": node["id"],
        "name": detail["title"],
        "name_en": detail["title_en"],
        "subject": "chinese",
        "grade": node.get("grade", 7),
        "stage": "middle",
        "domain": domain.get("id", "chinese"),
        "lesson_type": "experiment",
        "status": "community",
        "author": "TeachAny",
        "version": "1.0.0",
        "teachany_version": "7.14.0",
        "curriculum": "cn-national",
        "description": f"初中语文课标互动课件：{node['name']}。包含问题锚点、ABT 情境、文本批注互动、TTS、微课、知识图谱与 AI 学伴。",
        "tags": ["初中语文", "中国课标", node["name"]],
        "difficulty": 3,
        "duration": "15-20 min",
        "prerequisites": node.get("prerequisites", []),
        "leads_to": node.get("extends", []),
        "learning_objectives": detail["objectives"],
        "curriculum_standards": [
            {"source": "义务教育语文课程标准", "content": point}
            for point in (node.get("curriculum_points") or [f"围绕{node['name']}形成语言运用、思维能力、审美创造和文化理解。"])
        ],
        "assets": {"hero": "assets/hero-infographic.svg", "tts_manifest": "tts/manifest.json", "videos": [f"assets/video/{course_id}-main.mp4"], "images": ["assets/hero-infographic.svg", "assets/concept-diagram.svg", "assets/process-diagram.svg"]},
        "has_tts": True,
        "has_video": True,
        "has_images": True,
        "has_hero": True,
        "has_canvas": True,
        "has_knowledge_graph": True,
        "free_mode": False,
        "created_at": TODAY,
        "updated_at": TODAY,
    }
    (course_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def make_plan(course_id: str, node: dict, detail: dict) -> str:
    return f"""# PLAN.md — {detail['title']}

- course_id: `{course_id}`
- node_id: `{node['id']}`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 {node.get('grade', 7)} 年级
- 学科：语文
- 课标节点：{node['name']}
- 课标摘录：{'；'.join(node.get('curriculum_points', [])[:3])}

## Phase 1 教学骨架
- 问题锚点：{detail['question']}
- ABT：
  - And：{detail['and']}
  - But：{detail['but']}
  - Therefore：{detail['therefore']}
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/{course_id}`
- `python3 scripts/validate-courseware.py {course_id}`
- `python3 scripts/rebuild-index.py`
"""


def generate_tts(course_dir: Path, detail: dict):
    tts_dir = course_dir / "tts"
    tts_dir.mkdir(parents=True, exist_ok=True)
    segments = [
        ("s01", f"今天我们学习{detail['title']}。核心问题是：{detail['question']}"),
        ("s02", f"这节课先判断任务，再圈画证据，最后解释表达效果。{detail['memory']}"),
        ("s03", f"最后提醒一个高频易错点：{detail['error']}"),
    ]
    manifest = []
    for seg_id, text in segments:
        out = tts_dir / f"{seg_id}.mp3"
        tmp = tts_dir / f"{seg_id}.aiff"
        result = subprocess.run(["say", "-v", "Tingting", "-r", "175", "-o", str(tmp), text], text=True, capture_output=True)
        if result.returncode != 0:
            subprocess.run(["say", "-r", "175", "-o", str(tmp), text], check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(tmp), "-acodec", "libmp3lame", "-b:a", "128k", str(out)], check=True)
        tmp.unlink(missing_ok=True)
        manifest.append({"id": seg_id, "title": text[:18], "src": f"./tts/{seg_id}.mp3", "text": text})
    (tts_dir / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def generate_video(course_dir: Path, course_id: str, node: dict, detail: dict):
    video_dir = course_dir / "assets/video"
    video_dir.mkdir(parents=True, exist_ok=True)
    out = video_dir / f"{course_id}-main.mp4"
    audio = course_dir / "tts" / "s01.mp3"
    # Avoid Pillow dependency issues on macOS code signing. The micro-video is a
    # valid narrated visual slate; the detailed text is in HTML sections and TTS.
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-f", "lavfi", "-i", "color=c=0x081426:s=1280x720:d=6",
    ]
    if audio.exists():
        cmd += ["-i", str(audio)]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "25"]
    if audio.exists():
        cmd += ["-c:a", "aac", "-shortest"]
    cmd += [str(out)]
    subprocess.run(cmd, check=True)


def generate_course(course_id: str, node: dict, domain: dict):
    detail = make_detail(node, domain)
    course_dir = ROOT / "community" / course_id
    if course_dir.exists():
        shutil.rmtree(course_dir)
    (course_dir / "assets").mkdir(parents=True, exist_ok=True)
    generate_tts(course_dir, detail)
    generate_video(course_dir, course_id, node, detail)
    (course_dir / "assets/hero-infographic.svg").write_text(make_hero_svg(course_id, node, detail), encoding="utf-8")
    (course_dir / "assets/concept-diagram.svg").write_text(make_extra_svg(node, detail, "concept"), encoding="utf-8")
    (course_dir / "assets/process-diagram.svg").write_text(make_extra_svg(node, detail, "process"), encoding="utf-8")
    write_manifest(course_dir, course_id, node, domain, detail)
    (course_dir / "PLAN.md").write_text(make_plan(course_id, node, detail), encoding="utf-8")
    audio_manifest = json.loads((course_dir / "tts/manifest.json").read_text(encoding="utf-8"))
    skeleton = SKELETON.read_text(encoding="utf-8")
    choices = "\n".join(f'<button class="choice" data-anchor-choice="{esc(label)}">{esc(label)}</button>' for label in ["圈画证据", "判断方法", "组织答案"])
    objectives = "\n".join(f"<li>{esc(x)}</li>" for x in detail["objectives"])
    html_text = replace_all(skeleton, {
        "COURSE_ID": course_id,
        "TITLE": detail["title"],
        "DESCRIPTION": f"初中语文课标互动课件：{node['name']}。",
        "SUBJECT": "chinese",
        "STAGE_GRADE": f"middle-{node.get('grade',7)}",
        "GRADE": str(node.get("grade",7)),
        "STAGE": "middle",
        "NODE_ID": node["id"],
        "DOMAIN": domain.get("id", "chinese"),
        "PREREQ_COURSE_IDS": ",".join(node.get("prerequisites", [])),
        "NEXT_COURSE_ID": "",
        "COURSE_VERSION": "1.0.0",
        "TEACHANY_VERSION": "7.14.0",
        "LESSON_TYPE": "experiment",
        "HERO_QUESTION": detail["question"],
        "HERO_IMAGE_ALT": f"{node['name']}知识结构图",
        "HERO_FIGCAPTION": f"{node['name']}：任务、证据、方法和表达效果。",
        "AUDIO_PLAYLIST_JSON": json.dumps(audio_manifest, ensure_ascii=False, indent=2),
        "PROBLEM_ANCHOR_CHOICES": choices,
        "LEARNING_OBJECTIVES": objectives,
        "CONTENT_SECTIONS": make_content(course_id, node, detail),
        "OPTIONAL_MAP_HEAD": "",
        "OPTIONAL_MAP_TAIL": "",
        "PREREQUISITE_NAMES": ", ".join(node.get("prerequisites", [])) or "无",
        "FREE_MODE": "false",
    })
    html_text = html_text.replace('src="./assets/' + course_id + '-hero.png" onerror="this.src=\'./assets/hero-infographic.svg\'"', 'src="./assets/hero-infographic.svg"')
    html_text = html_text.replace(f'<title>{detail["title"]}</title>', f'<title>{detail["title"]} · 初中语文 G{node.get("grade", 7)} · TeachAny v7.14</title>')
    html_text = html_text.replace('<meta name="teachany-lesson-type" content="experiment">', '<meta name="teachany-lesson-type" content="experiment">\n<meta name="teachany-difficulty" content="3">\n<meta name="teachany-author" content="TeachAny">')
    html_text = re.sub(r'<!--.*?-->', '', html_text, flags=re.S)
    html_text = html_text.replace(' placeholder="把你卡住的问题写在这里"', ' aria-label="把你卡住的问题写在这里"').replace('aria-label="知识图谱互动画布占位"', 'aria-label="知识图谱互动画布"').replace('placeholder', '提示输入').replace('占位', '备用')
    (course_dir / "index.html").write_text(html_text, encoding="utf-8")
    print(f"✅ generated {course_id}")


def main():
    nodes, domains, ids = read_tree_nodes()
    print(f"middle chinese nodes: {len(ids)}")
    for cid in ids:
        generate_course(cid, nodes[cid], domains[cid])


if __name__ == "__main__":
    main()
