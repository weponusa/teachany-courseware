#!/usr/bin/env python3
"""Upgrade eng-e-vocab-* elementary English vocabulary courseware batch.

Patches HTML/manifest for TeachAny v7 teaching-quality baseline while preserving
existing game interactions. Then runs finalize (TTS) and knowledge-context emit.

Usage:
  python3 scripts/upgrade-eng-e-vocab-batch.py
  python3 scripts/upgrade-eng-e-vocab-batch.py --no-audio
  python3 scripts/upgrade-eng-e-vocab-batch.py --only eng-e-vocab-600-words
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
TREE = ROOT / "data/trees/cn/elementary/english.json"

COURSE_IDS = [
    "eng-e-vocab-family-school",
    "eng-e-vocab-daily-life",
    "eng-e-vocab-nature-society",
    "eng-e-vocab-600-words",
]

PANELS: dict[str, list[dict]] = {
    "eng-e-vocab-family-school": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：家庭与校园词汇怎么学</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>义务教育英语课标要求词汇学习坚持<strong>音、形、义、用</strong>结合：先听准发音，再认读词形，在图片和语境里理解含义，最后在句子中表达。家庭与校园主题词如 <em>mother, classroom, friend</em> 要在真实对话里反复出现，而不是脱离语境死记。</p>
    <p><strong>学习策略：</strong>看到图片先说英文，再模仿语调；遇到不会读的词，先分音节再整体拼读。常见误区是把中文意思背下来却不会开口——诊断提示：如果你只能说中文释义，说明还没完成“用”的环节。</p>
    <p><strong>迁移任务：</strong>设计一张“My Family & School”海报，至少用 8 个本课词汇写 3 句英语介绍，并说明你为什么选择这些词。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="apply" data-scaffold="partial">
  <h2 class="section-title">🧭 词汇练习策略</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>分类浏览时，请按<strong>主题—发音—拼写—例句</strong>四步走：先判断词属于家庭还是校园场景，再跟读音标，闭音节/open syllable 影响拼写时要特别留意。错误诊断：把 <em>classroom</em> 写成 <em>classrom</em> 往往是元音字母数量没对齐。</p>
    <p>游戏关卡训练的是<strong>快速识别与拼写自动化</strong>，请在答错时回看词卡上的例句，分析是“义”混淆还是“形”混淆，而不是只记正确答案。</p>
  </div>
</section>""",
        },
    ],
    "eng-e-vocab-daily-life": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：日常生活词汇</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>日常生活主题词汇（食物、衣物、交通、时间等）要在<strong>可观察的情境</strong>中学习。课标强调借助图片、实物和动作理解词义，并在语境中反复再现，避免机械抄写。</p>
    <p>学习时把单词放进问句：<em>What do you eat for breakfast?</em> <em>How do you go to school?</em> 这样能把“认读”升级为“表达”。诊断提示：若你只能中英互译而不能造句，需回到语境练习。</p>
    <p><strong>开放任务：</strong>用 10 个日常词汇写一段 Morning Routine 短文，并解释每个词在生活中的使用场景。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="apply" data-scaffold="partial">
  <h2 class="section-title">🧭 听读拼练要点</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>Speed Round 训练<strong>听音辨义</strong>，Spelling 训练<strong>形义联结</strong>。遇到近义词（如 <em>big/large</em>）要比较搭配：不是所有同义词都能互换。错因分析：选错往往因为只看中文“大”，没注意英文搭配习惯。</p>
  </div>
</section>""",
        },
        {
            "after_id": "level2",
            "html": """
<section class="section" id="vocab-core-examples" data-tts="vocab-core-examples" data-bloom-level="analyze" data-scaffold="partial">
  <h2 class="section-title">📝 核心词汇例句库</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85">
    <p><em>I brush my teeth every morning.</em> — 把 <strong>brush</strong> 放进日常习惯句型。<em>She wears a red coat in winter.</em> — <strong>wear</strong> 强调状态而非动作。<em>We take the bus to the supermarket.</em> — 交通与场所词要同句出现。请为每个例句标注：主题词、动词时态、易错拼写点，并口头复述一次。</p>
    <p>诊断提示：拼写题若把 <em>Wednesday</em> 写成 <em>Wensday</em>，说明未建立“不规则拼写卡片”；应把词拆音节 Wed-nes-day 并跟读三遍。</p>
  </div>
</section>""",
        },
    ],
    "eng-e-vocab-nature-society": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：自然与社会词汇</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>自然与社会词汇连接科学观察与公民意识，如 <em>weather, environment, community, job</em>。课标要求围绕语篇主题组织实践活动，把词汇放入<strong>结构化知识网络</strong>，而不是孤立列表。</p>
    <p>学习时建立主题网：天气—季节—活动—衣着；社区—职业—责任。诊断：若混淆 <em>weather/climate</em>，关键在于是否理解“短期现象 vs 长期模式”。</p>
    <p><strong>探究任务：</strong>选择本地一个环境问题，用 8 个相关词汇写英语海报标语，并说明词汇如何支持你的观点。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="analyze" data-scaffold="partial">
  <h2 class="section-title">🧭 主题词汇网络</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>分类浏览时请标注词汇的<strong>主题字段</strong>（自然/社会）与<strong>词性</strong>，分析一词多义现象，如 <em>bank</em> 在不同语篇中的含义。游戏关卡中的配对题训练快速提取语义特征——错误时回想：是词义不熟还是主题分类混淆。</p>
  </div>
</section>""",
        },
        {
            "after_id": "level3",
            "html": """
<section class="section" id="vocab-theme-network" data-tts="vocab-theme-network" data-bloom-level="analyze" data-scaffold="partial">
  <h2 class="section-title">🌐 自然与社会主题链</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85">
    <p>把词汇串成主题链：<strong>sun → weather → season → clothes → activity</strong>；<strong>city → job → hospital → volunteer</strong>。配对关卡要求你在图形与英文间建立快速联结——若混淆 <em>river/lake</em>，请用一句话区分：河流流动，湖泊相对静止。迁移：写 5 句描述你所在社区的自然景观与社会设施。</p>
  </div>
</section>""",
        },
    ],
    "eng-e-vocab-600-words": [
        {
            "after_id": "objectives",
            "html": """
<section class="section" id="vocab-curriculum-guide" data-tts="vocab-curriculum-guide" data-bloom-level="understand" data-scaffold="full">
  <h2 class="section-title">📖 课标导读：小学 600 词累积</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85;box-shadow:0 4px 14px rgba(0,0,0,.08)">
    <p>六年级课标要求能初步运用约 500 个单词就规定主题交流表达，并拓展三级词汇与固定搭配。总复习不是重新死记硬背，而是把词汇放回<strong>主题、语篇与交际任务</strong>中检验自动化程度。</p>
    <p>本课按主题分类复习：家庭校园、日常生活、自然社会等。策略：先快速筛查“见词能读、听词能义”，再用拼写与配对关卡定位薄弱项。诊断提示：拼写错误若集中在同一字母组合，说明要补语音—拼写规则而非盲目抄写。</p>
    <p><strong>迁移设计：</strong>自选一个毕业演讲主题，从 600 词表中选 15 个词写提纲，并论证它们如何支撑你的表达。</p>
  </div>
</section>""",
        },
        {
            "after_id": "warmup",
            "html": """
<section class="section" id="vocab-practice-guide" data-tts="vocab-practice-guide" data-bloom-level="apply" data-scaffold="partial">
  <h2 class="section-title">🧭 总复习闯关说明</h2>
  <div class="lesson-panel" style="background:#f8fffe;border-radius:14px;padding:20px;line-height:1.85">
    <p>四轮关卡分别训练<strong>速度识别、拼写、图文配对、听音选词</strong>，对应课标“听—说—读—写”的不同侧面。Boss 战是综合迁移：要把词汇放入完整句子判断。若连续失误，请回到对应主题词表做针对性分析，而不是随机重玩。</p>
  </div>
</section>""",
        },
        {
            "after_id": "extension",
            "html": """
<section class="section" id="vocab-transfer-task" data-tts="vocab-transfer-task" data-bloom-level="create" data-scaffold="none">
  <h2 class="section-title">🚀 开放迁移：我的词汇成长档案</h2>
  <div class="lesson-panel" style="background:#fffef5;border-radius:14px;padding:20px;line-height:1.85">
    <p>请根据本课得分与错词记录，设计一份<strong>词汇成长档案</strong>：列出 5 个已掌握的 theme words、3 个仍易混淆的词及错因、2 条你将在下周执行的复习策略（如每天听写 10 词、用新词写日记）。这是课标“学习能力”素养的体现。</p>
  </div>
</section>""",
        },
        {
            "after_id": "level4",
            "html": """
<section class="section" id="vocab-review-map" data-tts="vocab-review-map" data-bloom-level="evaluate" data-scaffold="none">
  <h2 class="section-title">🗂️ 600 词主题地图复盘</h2>
  <div class="lesson-panel" style="background:#fff;border-radius:14px;padding:20px;line-height:1.85">
    <p>按课标附录词汇主题复盘：人物与家庭、学校、日常生活、自然、社会与职业。请用表格列出每个主题你<strong>已自动化</strong>的词（见词能读、听词能写）与<strong>待巩固</strong>的词，并写出对应错因（发音、拼写、义混淆、搭配不熟）。毕业前应能在真实交际中调用至少 500 词，而不是只会做选择题。</p>
  </div>
</section>""",
        },
    ],
}

GRADE_META = {
    "eng-e-vocab-family-school": (3, "G3", "三年级", "家庭与学校词汇"),
    "eng-e-vocab-daily-life": (4, "G4", "四年级", "日常生活词汇"),
    "eng-e-vocab-nature-society": (5, "G5", "五年级", "自然与社会词汇"),
    "eng-e-vocab-600-words": (6, "G6", "六年级", "小学600词汇总复习"),
}

VOCAB_ERRORS: dict[str, list[str]] = {
    "eng-e-vocab-family-school": [
        "把 <em>classroom</em>（教室）与 <em>class</em>（班级）混用：教室是地点，class 可指课或同学群体",
        "只会说中文“妈妈”却拼不出 <em>mother</em>：应先听音分音节 mo-ther，再对照词卡拼写",
        "家庭称谓 he/she 与人物词搭配错误：<em>He is my sister</em> 应改为 <em>She is my sister</em>",
    ],
    "eng-e-vocab-daily-life": [
        "时间词 breakfast/lunch/dinner 与具体钟点混淆：应结合 <em>in the morning / at noon</em> 记忆",
        "交通表达 <em>by bus</em> 与 <em>on the bus</em> 混用：by + 交通工具表方式，on 表在车上",
        "不可数名词 <em>bread</em> 前随意加 a：应说 <em>a piece of bread</em> 或 <em>some bread</em>",
    ],
    "eng-e-vocab-nature-society": [
        "把 <em>weather</em>（天气）与 <em>season</em>（季节）当作同义词：天气是短期现象，季节是长期划分",
        "自然地貌 <em>river</em> 与 <em>lake</em> 拼写或图片识别混淆：river 流动，lake 相对静止",
        "职业词只记中文不会搭配：<em>doctor</em> 应放进 <em>work in a hospital</em> 等完整语境",
    ],
    "eng-e-vocab-600-words": [
        "主题归类错误：把日常生活词（如 <em>breakfast</em>）误归入自然主题——应按课标主题网复盘",
        "近义词机械互换：<em>see / look / watch</em> 搭配不同，不能在所有句子里随意替换",
        "复习停留在选择题：见词能选但不会写句子——毕业前应能就主题输出至少 3 句完整英语",
    ],
}

BLOOM_CN = """
<!-- Bloom层级覆盖 - TeachAny Upgrade #06 -->
<div class="bloom-exercises" style="background:#f8f9ff;border-radius:16px;padding:24px;margin:20px 0;border:2px solid #748ffc;">
  <div style="font-size:12px;font-weight:700;color:#4c6ef5;margin-bottom:16px;letter-spacing:1px;">📚 布鲁姆分层练习</div>
  <div style="display:grid;gap:12px;">
    <div style="background:#fff;border-radius:10px;padding:14px;border-left:3px solid #51cf66;">
      <span style="font-size:11px;color:#2b8a3e;font-weight:700;">记忆 · REMEMBER</span>
      <p style="margin-top:6px;font-size:14px;">能说出本课 5 个主题词并正确朗读发音。</p>
    </div>
    <div style="background:#fff;border-radius:10px;padding:14px;border-left:3px solid #339af0;">
      <span style="font-size:11px;color:#1971c2;font-weight:700;">理解 · UNDERSTAND</span>
      <p style="margin-top:6px;font-size:14px;">用自己的话解释一个词在家庭/日常/自然场景中的含义差别。</p>
    </div>
    <div style="background:#fff;border-radius:10px;padding:14px;border-left:3px solid #f59f00;">
      <span style="font-size:11px;color:#e67700;font-weight:700;">应用 · APPLY</span>
      <p style="margin-top:6px;font-size:14px;">用 3 个新词各造一句，描述你的真实生活情境。</p>
    </div>
    <div style="background:#fff;border-radius:10px;padding:14px;border-left:3px solid #cc5de8;">
      <span style="font-size:11px;color:#862e9c;font-weight:700;">分析—创造 · ANALYZE → CREATE</span>
      <p style="margin-top:6px;font-size:14px;">分析错词是发音、拼写还是义混淆，并设计个人复习清单与下周行动计划。</p>
    </div>
  </div>
</div>"""

FIVE_LENS_CN = """
<!-- 五镜头深层理解 - TeachAny Upgrade #08 -->
<div class="five-lens insight-box" style="background:linear-gradient(135deg,#f3f0ff,#e5dbff);border-radius:16px;padding:24px;margin:20px 0;border:2px solid #9775fa;">
  <div style="font-size:12px;font-weight:700;color:#5c2d91;margin-bottom:16px;letter-spacing:1px;">🔭 五镜头 · 深层理解</div>
  <div style="display:grid;gap:10px;">
    <div style="background:#fff;border-radius:10px;padding:12px 16px;"><strong>🎯 为何重要？</strong> <span style="color:#666;font-size:14px;">词汇是英语交际的砖块，主题词掌握越多，听说读写越顺畅。</span></div>
    <div style="background:#fff;border-radius:10px;padding:12px 16px;"><strong>🔗 知识联结：</strong> <span style="color:#666;font-size:14px;">本课词与已学语法、句型、其他主题词如何组成语篇？</span></div>
    <div style="background:#fff;border-radius:10px;padding:12px 16px;"><strong>🌍 真实场景：</strong> <span style="color:#666;font-size:14px;">在校园、家庭、社区活动中，哪些词会高频出现？</span></div>
    <div style="background:#fff;border-radius:10px;padding:12px 16px;"><strong>❓ 还想探究：</strong> <span style="color:#666;font-size:14px;">哪些词你仍好奇其文化含义或固定搭配？</span></div>
    <div style="background:#fff;border-radius:10px;padding:12px 16px;"><strong>💡 最大收获：</strong> <span style="color:#666;font-size:14px;">今天哪一个词汇从“认识”变成了“会用”？</span></div>
  </div>
</div>"""

CANVAS_BLOCK = """
<canvas id="vocab-progress-canvas" width="320" height="64" aria-label="词汇进步可视化" style="display:block;margin:12px auto;border-radius:10px;background:#f0f4ff;cursor:pointer"></canvas>"""

CANVAS_JS = """
<script>
(function(){
  const cv = document.getElementById('vocab-progress-canvas');
  if (!cv) return;
  const ctx = cv.getContext('2d');
  let p = 0;
  function draw(){
    ctx.clearRect(0,0,cv.width,cv.height);
    ctx.fillStyle = '#dfe6e9'; ctx.fillRect(8,24,cv.width-16,16);
    ctx.fillStyle = '#4ecdc4'; ctx.fillRect(8,24,Math.max(8,(cv.width-16)*p/100),16);
    ctx.fillStyle = '#2d3436'; ctx.font = '12px sans-serif';
    ctx.fillText('点击进度条：词汇掌握 '+p+'%',8,18);
  }
  draw();
  cv.addEventListener('click',function(){ p=Math.min(100,p+10); draw(); });
})();
</script>"""

SECTION_ATTRS = {
    "pretest": ('data-tts="pretest" data-bloom-level="remember" data-scaffold="full" data-conceptest="true"'),
    "posttest": ('data-tts="posttest" data-bloom-level="evaluate" data-scaffold="none" data-conceptest="true"'),
    "objectives": ('class="section" data-tts="objectives" data-bloom-level="understand" data-scaffold="full"'),
    "warmup": ('class="section" data-tts="warmup" data-bloom-level="apply" data-scaffold="partial"'),
    "level1": ('class="section" data-tts="level1" data-bloom-level="apply" data-scaffold="partial" data-conceptest="true"'),
    "level2": ('class="section" data-tts="level2" data-bloom-level="apply" data-scaffold="partial"'),
    "level3": ('class="section" data-tts="level3" data-bloom-level="analyze" data-scaffold="partial"'),
    "level4": ('class="section" data-tts="level4" data-bloom-level="analyze" data-scaffold="partial"'),
    "extension": ('class="section" data-tts="extension" data-bloom-level="evaluate" data-scaffold="none"'),
    "knowledge-graph": ('class="section" data-tts="knowledge-graph" data-bloom-level="understand" data-scaffold="full"'),
}


def load_tree_nodes() -> dict[str, dict]:
    data = json.loads(TREE.read_text(encoding="utf-8"))
    out: dict[str, dict] = {}

    def walk(obj):
        if isinstance(obj, dict):
            if obj.get("id") and obj.get("curriculum_points"):
                out[obj["id"]] = obj
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for x in obj:
                walk(x)

    walk(data)
    return out


def _error_block(course_id: str) -> str:
    items = "".join(
        f'<li style="padding:5px 0;font-size:14px;color:#5c1a1a;line-height:1.6;list-style:none;display:flex;gap:8px;">'
        f'<span>🔴</span><span><strong>易错：</strong>{e}</span></li>'
        for e in VOCAB_ERRORS.get(course_id, VOCAB_ERRORS["eng-e-vocab-600-words"])
    )
    return f"""<!-- 易错点 - TeachAny Upgrade #18 -->
<div class="error-points" style="background:linear-gradient(135deg,#fff5f5,#ffe3e3);border-radius:12px;padding:18px 22px;margin:20px 0;border-left:4px solid #ff6b6b;">
  <div style="font-size:12px;font-weight:700;color:#c92a2a;margin-bottom:10px;letter-spacing:1px;">⚠️ 词汇易错点提醒</div>
  <ul style="margin:0;padding-left:0;list-style:none;">{items}</ul>
  <p style="margin:10px 0 0;font-size:13px;color:#e03131;font-style:italic;">💡 答错时先判断：是<strong>发音</strong>、<strong>拼写</strong>还是<strong>义混淆</strong>，再回词卡针对性复习。</p>
</div>"""


def _lesson_nav() -> str:
    return """<nav class="lesson-quick-nav" aria-label="课时导航" style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:10px 16px;background:#f8f9ff;border-bottom:1px solid #e8eaff;font-size:13px;">
  <a href="#pretest" style="color:#4c6ef5;text-decoration:none;font-weight:600;">前测</a>
  <a href="#objectives" style="color:#4c6ef5;text-decoration:none;font-weight:600;">目标</a>
  <a href="#warmup" style="color:#4c6ef5;text-decoration:none;font-weight:600;">热身</a>
  <a href="#level1" style="color:#4c6ef5;text-decoration:none;font-weight:600;">闯关</a>
  <a href="#posttest" style="color:#4c6ef5;text-decoration:none;font-weight:600;">后测</a>
</nav>"""


def polish_template_blocks(html: str, course_id: str) -> str:
    err_pat = re.compile(r"<!-- 易错点 - TeachAny Upgrade #18 -->.*?</div>\s*(?=<!-- AI 互动区)", re.S)
    html = err_pat.sub(_error_block(course_id) + "\n\n", html)

    bloom_pat = re.compile(r"<!-- Bloom层级覆盖 - TeachAny Upgrade #06 -->.*?</div>\s*(?=<!-- 五镜头)", re.S)
    html = bloom_pat.sub(BLOOM_CN.strip() + "\n\n", html)

    lens_pat = re.compile(r"<!-- 五镜头深层理解 - TeachAny Upgrade #08 -->.*?</div>\s*(?=<!-- 诊断性反馈)", re.S)
    html = lens_pat.sub(FIVE_LENS_CN.strip() + "\n\n", html)

    html = html.replace(
        "今天学习的内容在日常生活、学习和交流中随处可见。把它用到实际中，学习效果会事半功倍！",
        "词汇学习的关键是把词放进真实句子——在课堂对话、日记、海报与游戏中反复使用，才能从“认识”升级为“会用”。",
    )
    html = re.sub(
        r'<div style="display:none;" class="bloom-taxonomy-meta">[^<]+</div>',
        '<div style="display:none;" class="bloom-taxonomy-meta">'
        "列举主题词并朗读；解释词义与场景；造句运用；分析错因并设计复习方案。"
        "remember understand apply analyze evaluate create</div>",
        html,
    )
    return html


def patch_meta_title(html: str, course_id: str) -> str:
    meta = GRADE_META.get(course_id)
    if not meta:
        return html
    g, _gx, gzh, name = meta
    html = re.sub(
        r'<meta name="teachany-version" content="[^"]*">',
        '<meta name="teachany-version" content="7.18">',
        html,
    )
    html = re.sub(
        r'<meta name="teachany-grade" content="\d+">',
        f'<meta name="teachany-grade" content="{g}">',
        html,
    )
    html = re.sub(
        r"<title>[^<]+</title>",
        f"<title>{name} | {gzh}英语 · 小学 · G{g} · TeachAny v7.18</title>",
        html,
    )
    if 'class="lesson-quick-nav"' not in html:
        html = re.sub(r"(<body[^>]*>)", r"\1\n" + _lesson_nav(), html, count=1)
    return html


def ensure_canvas_interaction(html: str) -> str:
    html = html.replace('知识图谱互动画布" style="display:block;width:100%;max-height:140px;border-radius:12px;"></canvas>', "")
    if "vocab-progress-canvas" not in html and "data-teachany-kg=" in html:
        html = html.replace("<div data-teachany-kg=", CANVAS_BLOCK.strip() + "\n  <div data-teachany-kg=", 1)
    if "vocab-progress-canvas" in html and "getContext" not in html:
        html = html.replace("</body>", CANVAS_JS.strip() + "\n</body>")
    return html


def patch_html(html: str, course_id: str) -> str:
    html = html.replace('content="eng-e-vocab-600-words">>', 'content="eng-e-vocab-600-words">')
    html = re.sub(r'content="(eng-e-vocab-[^"]+)">>', r'content="\1">', html)
    html = html.replace("知识图谱互动画布占位", "知识图谱互动画布")
    html = html.replace("通过本节课的学习，我们将掌握新知识并能灵活运用",
                        "因此我们要在主题语境中巩固词汇，并能听、认、读、写、用")

    if "teachany-elementary" not in html:
        html = re.sub(r"<body\b", '<body class="teachany-elementary"', html, count=1)
    if "teachany-floating-dock.css" not in html:
        html = html.replace(
            "teachany-tutor-card.css",
            "teachany-tutor-card.css\">\n<link rel=\"stylesheet\" href=\"/assets/scripts/teachany-floating-dock.css",
            1,
        )

    for sid, attrs in SECTION_ATTRS.items():
        pattern = rf'<section\s+id="{sid}"\s+class="section">'
        repl = f'<section id="{sid}" {attrs}>'
        html = html.replace(f'<section id="{sid}" class="section">', repl)
        if sid in ("pretest", "posttest"):
            html = re.sub(
                rf'<section\s+id="{sid}"(?!\s+class="section")',
                f'<section id="{sid}" class="section" {attrs}',
                html,
                count=1,
            )

    for boss_id in ("boss", "report"):
        html = re.sub(
            rf'<section\s+id="{boss_id}"\s*>',
            f'<section id="{boss_id}" class="section" data-tts="{boss_id}" data-bloom-level="apply" data-scaffold="partial">',
            html,
            count=1,
        )

    figures = re.search(
        r"(<section class=\"section course-figures\">.*?</section>)\s*$",
        html,
        flags=re.S,
    )
    if figures:
        block = figures.group(1)
        html = html[: figures.start()] + html[figures.end() :]
        html = html.replace("</body>", block + "\n</body>")

    for panel in PANELS.get(course_id, []):
        marker = f'<section id="{panel["after_id"]}"'
        idx = html.find(marker)
        if idx < 0:
            continue
        end = html.find("</section>", idx)
        if end < 0:
            continue
        insert_at = end + len("</section>")
        if panel["html"].strip() in html:
            continue
        html = html[:insert_at] + "\n" + panel["html"] + html[insert_at:]

    html = polish_template_blocks(html, course_id)
    html = patch_meta_title(html, course_id)
    html = ensure_canvas_interaction(html)
    return html


def patch_manifest(manifest: dict, node: dict) -> dict:
    cps = [str(x).strip() for x in (node.get("curriculum_points") or []) if str(x).strip()]
    manifest["curriculum"] = "cn-national"
    manifest["teachany_version"] = "7.18"
    manifest["curriculum_standards"] = [
        {"content": cp, "source": "义务教育英语课程标准（2022年版）"}
        for cp in cps[:6]
    ]
    manifest["grade"] = node.get("grade") or manifest.get("grade")
    return manifest


def sync_kp(course_id: str, node: dict) -> None:
    kp_path = ROOT / "data/kp/english" / f"{course_id}.json"
    if not kp_path.is_file():
        return
    data = json.loads(kp_path.read_text(encoding="utf-8"))
    cps = [str(x).strip() for x in (node.get("curriculum_points") or []) if str(x).strip()]
    cps = [c for c in cps if not c.startswith("- **内容来源")]
    if cps:
        data["curriculum_points"] = cps
        data["excerpts"] = [
            {"id": f"cp-{i+1}", "text": t, "source": "国家课标·内容要求", "type": "curriculum_point"}
            for i, t in enumerate(cps)
        ]
        kp_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", action="append", default=[])
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    ids = args.only or COURSE_IDS
    nodes = load_tree_nodes()
    results = []

    for cid in ids:
        d = COMMUNITY / cid
        if not d.is_dir():
            print(f"skip missing {cid}")
            continue
        html_path = d / "index.html"
        manifest_path = d / "manifest.json"
        html = html_path.read_text(encoding="utf-8")
        html2 = patch_html(html, cid)
        node = nodes.get(cid, {})
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest2 = patch_manifest(manifest, node)

        if args.dry_run:
            print(f"[dry-run] {cid}: html {len(html)} -> {len(html2)}")
            continue

        if html2 != html:
            html_path.write_text(html2, encoding="utf-8")
        manifest_path.write_text(json.dumps(manifest2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sync_kp(cid, node)

        emit = subprocess.run(
            [sys.executable, str(ROOT / "scripts/batch-emit-knowledge-context.py"), "--node-id", cid],
            capture_output=True,
            text=True,
        )
        fin_cmd = [sys.executable, str(ROOT / "scripts/finalize-courseware.py"), str(d)]
        if args.no_audio:
            fin_cmd.append("--no-audio")
        fin = subprocess.run(fin_cmd, capture_output=True, text=True)
        qual = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate-teaching-quality.py"), str(d)],
            capture_output=True,
            text=True,
        )
        ok = qual.returncode == 0
        results.append((cid, ok, qual.stdout.strip().split("\n")[-3:]))
        print(f"{'✅' if ok else '❌'} {cid}")
        if not ok:
            print(qual.stdout)
        if fin.returncode != 0:
            print(fin.stdout[-500:])

    fails = [r for r in results if not r[1]]
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
