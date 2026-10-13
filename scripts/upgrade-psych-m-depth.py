#!/usr/bin/env python3
"""Add two core-knowledge modules to failing psych-m courses.

Like pol-m, these middle-school psychology units pass text/section counts but
fail with module_like < 3. Each gets one concept module + one method module
(diagnostic + 常见误区), both id="lesson-*"/class core-knowledge-module.
No mp4. Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-09"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
                example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit)


COURSES = {
    "psych-m-g7-interpersonal": C(
        "人际交往：亲子、师生与同伴", "良好的人际关系是心理健康的重要支撑。与父母交往贵在理解与沟通，与老师交往贵在尊重与信任，与同伴交往贵在真诚与平等。青春期我们渴望独立又需要接纳，学会换位思考、尊重差异，才能建立温暖而稳定的关系。",
        "方法：用倾听与表达经营关系", "改善人际关系可用“积极倾听 + 我信息表达”：先认真听懂对方的意思和感受，再用“我觉得……我希望……”的方式表达自己，而不是指责对方。遇到冲突先冷静，就事论事，寻找双方都能接受的办法。",
        "小明和同桌因借文具闹别扭，他没有指责，而是说“我担心用完找不到，希望用完能还我”，两人很快和好。",
        "与同伴发生矛盾时，最有助于化解的做法是？", ["互相指责", "用‘我信息’表达感受并倾听对方", "冷战到底", "找人报复"], 1,
        "先倾听、再用‘我信息’表达，能减少对立、化解矛盾。",
        "常见误区是把人际矛盾归咎于对方、习惯指责。应认识到关系需要经营，用积极倾听和‘我信息’表达代替指责，尊重差异、就事论事，才能建立良好关系。"),
    "psych-m-g7-study-adapt": C(
        "学习适应与情绪管理", "进入中学，学习科目增多、要求提高，需要主动适应。良好的学习适应包括合理规划时间、掌握适合自己的方法、保持稳定的学习情绪。焦虑、畏难等情绪会影响学习，学会觉察和调节情绪，是提高学习效率的前提。",
        "方法：目标分解加情绪调节", "适应学习可把大目标拆成每日小任务，用计划表和番茄钟管理时间；遇到畏难情绪时先接纳它，再用深呼吸、积极自我暗示等方式放松，把“我不行”换成“我可以一步步来”，在小成功中积累信心。",
        "面对堆积的作业，小丽把任务列清单、按重要性排序，每完成一项就打勾，焦虑减轻、效率提高。",
        "面对学习焦虑，较好的调节方式是？", ["逃避不学", "分解任务并积极自我暗示", "熬夜硬撑", "自我否定"], 1,
        "分解任务、积极暗示能缓解焦虑、提升效率。",
        "常见误区是把学习焦虑当成能力不足而自我否定或逃避。应认识到适度焦虑正常，可通过目标分解、时间管理和情绪放松来调节，在小成功中重建信心。"),
    "psych-m-g8-puberty-relation": C(
        "青春期交往与情绪调适", "青春期身心迅速变化，情绪起伏大，对异性产生好感是正常心理现象。健康的异性交往应自然、适度、真诚，把握好交往的分寸。学会识别和调适情绪，正确看待青春期的心理变化，有助于顺利度过这一阶段。",
        "方法：把握交往分寸与情绪调适", "青春期交往要做到自然大方、互相尊重、把握分寸，把对异性的欣赏转化为共同学习进步的动力。情绪波动时，用运动、倾诉、写日记等方式疏导，遇到困惑主动向家长、老师或心理老师求助。",
        "小刚对同班女生有好感，他选择把这份欣赏化为学习上的相互鼓励，交往自然而有分寸。",
        "青春期对异性产生好感，正确的态度是？", ["视为错误加以压抑", "认识到是正常现象并把握分寸", "盲目早恋", "自我羞愧"], 1,
        "对异性有好感是正常心理，关键是自然、适度、把握分寸。",
        "常见误区是把青春期对异性的好感看作错误而羞愧压抑，或放任发展。应认识到这是正常心理现象，健康交往贵在自然、真诚、把握分寸，并学会调适情绪。"),
    "psych-m-g8-role-identity": C(
        "角色认同与社会适应", "随着成长，我们在家庭、学校和社会中扮演越来越多的角色，每种角色都伴随相应的期待和责任。正确认识自己的多重角色、协调角色之间的关系，形成稳定的自我认同，是社会适应的重要内容。", 
        "方法：厘清角色、承担责任", "适应角色变化，先厘清自己在不同情境中的角色和相应责任，再学会在角色冲突时分清主次、合理安排。主动承担与年龄相符的责任，如在家分担家务、在班级服务同学，在履行角色中增强自我认同和归属感。",
        "小丽既是女儿又是班干部，考试周她合理安排时间，先完成学习和班务，周末再帮家里做事，协调好了多重角色。",
        "面对多重角色带来的冲突，恰当的做法是？", ["逃避所有责任", "分清主次、合理安排、承担责任", "只做喜欢的角色", "抱怨他人"], 1,
        "分清主次、合理安排并承担责任，才能适应角色变化。",
        "常见误区是遇到角色冲突就逃避责任或只挑轻松的做。应认识到成长伴随多重角色和责任，要厘清角色、分清主次、主动担当，在履行角色中形成稳定的自我认同。"),
    "psych-m-g8-stress-coping": C(
        "学业压力与挫折应对", "适度的压力能激发动力，过度的压力则影响身心健康。挫折是成长中不可避免的，面对挫折的态度决定其影响。培养抗挫折能力（心理韧性），学会正确归因、积极应对，能把压力和挫折转化为成长的契机。",
        "方法：正确归因加积极应对", "应对压力和挫折可用“正确归因 + 问题解决 + 情绪调节”：把失败更多归于可努力改变的因素（如方法、努力），而非“我天生不行”；分析问题、制订对策；同时用运动、倾诉等方式缓解情绪，必要时寻求帮助。",
        "考试失利后，小明不再说“我太笨”，而是分析失分原因、调整方法，并坚持锻炼放松，成绩逐步回升。",
        "面对考试挫折，较健康的归因是？", ["我天生就笨", "这次方法和努力不够，可以改进", "都怪运气差", "以后再也不考了"], 1,
        "把挫折归于可改变的努力和方法，更利于积极应对。",
        "常见误区是遇挫折就归因于‘天生能力差’或运气，导致习得性无助。应学会正确归因，把失败归于可努力改变的因素，用问题解决和情绪调节积极应对，增强心理韧性。"),
    "psych-m-g9-career-explore": C(
        "升学择业与生涯探索", "生涯探索要认识自我与了解外部世界相结合。认识自我包括兴趣、能力、性格和价值观；了解外部包括升学路径、职业种类和社会需求。初中阶段做好生涯启蒙，有助于在升学选择中更有方向感。",
        "方法：自我探索加信息搜集", "生涯探索可用“认识自我 + 搜集信息 + 尝试体验”：通过反思、量表初步了解自己的兴趣与优势；搜集高中、职校和不同职业的信息；参加职业体验、社会实践进行验证，逐步明确阶段目标并制订行动计划。",
        "小华喜欢动手且擅长逻辑，他了解了普高和职校的不同路径，并参加机器人社团体验，逐渐明确了努力方向。",
        "初中阶段进行生涯探索，首先要做的是？", ["盲目跟风选择", "认识自我并了解升学与职业信息", "完全交给父母决定", "不用考虑未来"], 1,
        "先认识自我、了解外部信息，才能作出合适的生涯选择。",
        "常见误区是把生涯选择完全交给家长或盲目跟风。应把认识自我与了解升学、职业信息结合，通过体验验证，逐步明确方向并制订可行的行动计划。"),
    "psych-m-g9-mental-health": C(
        "心理健康素养与求助", "心理健康是指个体能够正确认识自我、调节情绪、适应环境、建立良好人际关系并有效应对压力的状态。心理健康和身体健康同样重要。出现心理困扰是常见的，主动寻求帮助是勇敢和智慧的表现，而不是软弱。",
        "方法：自我调适加主动求助", "维护心理健康，日常要保持规律作息、适度运动、培养兴趣、维系良好人际关系；当情绪持续低落、影响学习生活时，及时向信任的家长、老师或专业心理咨询、心理援助热线求助，学会借助社会支持系统走出困境。",
        "小丽连续两周情绪低落、失眠，她鼓起勇气找心理老师倾诉并接受辅导，逐渐恢复了状态。",
        "当心理困扰持续影响生活时，正确做法是？", ["独自硬扛", "及时向信任的人或专业机构求助", "认为是自己软弱", "放任不管"], 1,
        "主动求助是勇敢与智慧，能借助支持系统走出困境。",
        "常见误区是把心理求助看作软弱、羞于开口而独自硬扛。应认识到心理健康与身体健康同样重要，出现困扰很常见，主动向可信任的人或专业机构求助是明智之举。"),
    "psych-m-g9-social-adapt": C(
        "社会适应与责任意识", "社会适应能力是指个体调整自己以适应社会环境、并在其中健康发展的能力，包括人际适应、规则适应和角色适应等。增强社会适应，要培养责任意识，主动关心他人和集体，积极参与社会实践，在服务社会中实现自我成长。",
        "方法：在实践中提升适应力", "提升社会适应可通过“参与实践 + 遵守规则 + 承担责任”：主动参加志愿服务、社团和社会实践，在真实情境中学会合作、沟通与解决问题；自觉遵守公共规则，主动承担对家庭、集体和社会的责任，逐步成长为负责任的社会成员。",
        "毕业前小刚坚持参加社区志愿服务，学会了与陌生人沟通、按规则办事，社会适应能力明显增强。",
        "增强社会适应能力，重要途径是？", ["回避社会交往", "积极参与社会实践并承担责任", "只顾自己", "抗拒一切规则"], 1,
        "在社会实践中遵守规则、承担责任，能提升社会适应力。",
        "常见误区是把社会适应理解为被动服从或干脆回避社交。应认识到社会适应是主动调整并健康发展，要在实践中锻炼合作沟通、遵守规则、承担责任。"),
}


STYLE = """
<style id="psychm-depth-css">
.psychm-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.psychm-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(129,140,248,.08);border:1px solid rgba(129,140,248,.24)}
.psychm-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.psychm-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.psychm-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.psychm-depth .psychm-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.psychm-depth .psychm-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="psychm-depth-js">
function psychmDepthCheck(button, isCorrect, feedbackId, explanation) {
  var box = button.closest('.module-check');
  if (!box || box.dataset.answered) return;
  box.dataset.answered = '1';
  box.querySelectorAll('button').forEach(function (item) {
    item.disabled = true;
    if (item.dataset.correct === '1') item.classList.add('correct');
  });
  if (!isCorrect) button.classList.add('wrong');
  var feedback = document.getElementById(feedbackId);
  if (feedback) {
    feedback.style.display = 'block';
    feedback.textContent = (isCorrect ? '正确。' : '再想想。') + explanation;
  }
}
</script>
"""


def build_block(cfg: dict) -> str:
    feedback_id = "psychm-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "psychmDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false", f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False))
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0", h=html.escape(handler, quote=True),
                letter=chr(65 + idx), opt=html.escape(opt)))
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section psychm-depth core-knowledge-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section psychm-depth core-knowledge-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="psychm-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="psychm-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-focus"' in source:
        return False, "already upgraded"
    dpos = source.find('id="deep-understanding"')
    if dpos < 0:
        dpos = source.find('id="transfer-task"')
    if dpos < 0:
        return False, "insert anchor not found"
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, dpos)
    if insert_at < 0:
        return False, "insert marker not found"
    block = build_block(cfg)
    source = source[:insert_at] + block + "\n" + source[insert_at:]
    if 'id="psychm-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="psychm-depth-js"' not in source:
        source = source.replace("</body>", CHECK_SCRIPT + "\n</body>", 1)
    source = re.sub(r"[ \t]+\n", "\n", source)
    path.write_text(source, encoding="utf-8")
    manifest_path = path.parent / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        changed = False
        for key, value in {"version": COURSE_VERSION, "updated_at": UPDATED_AT}.items():
            if manifest.get(key) != value:
                manifest[key] = value
                changed = True
        if changed:
            manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True, "2 core modules + metadata"


def main() -> int:
    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
