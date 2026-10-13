# -*- coding: utf-8 -*-
"""小学科学 · 金属：为什么锅是金属做的（G5）—— 补齐课标「物质的结构与性质·1.3 金属及合金是重要的材料」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-metal-materials-fig1.webp'
F2 = './assets/sci-e-metal-materials-fig2.webp'

TTS = {
    "hero": "请你看看家里的厨房。炒菜的锅，锅身是铁的；锅铲的把手，却是塑料或者木头的。再看插线板里的电线，里面是铜丝，外面包着塑料皮。为什么同样是做饭或者用电，有的地方必须用金属，有的地方坚决不能用金属？这节课我们就来弄清楚一件事：材料有什么本领，人们就拿它去做什么事情。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道金属到底有哪些共同的本领，还是想知道人们挑材料的时候在看什么，又或者你想自己当一次工程师，给一件物品挑材料。选好以后，带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出金属的共同性质，包括容易导热、容易导电、有延展性、有金属光泽。第二，能设计简单的检测方法，比较不同材料的导热性和导电性。第三，能说出材料的性质决定了它的用途。第四，能为一件物品选择合适的材料，并说出理由。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上会给你解释，选错了正好知道要重点听哪里。",
    "module-1": "我们先来认识金属。把一根铁丝、一块木头、一块塑料、一片陶瓷摆在一起，只用眼睛看，你会发现金属表面亮亮的，会反光，这叫金属光泽。再动手弯一弯，铁丝能弯成各种形状还不断，木头一掰就裂，陶瓷一敲就碎，这说明金属有延展性，能被拉长、能被压薄。接着把它放进热水里，金属很快就烫手，木头和塑料半天还是温的，说明金属导热快。最后把它接进电路，小灯泡亮了，说明金属容易导电。导热、导电、有延展性、有金属光泽，这四条就是大多数金属共同的性质。",
    "lab-1": "现在请你当一次材料检测员。先选一种材料，再点下面的测试按钮，看看它在导热、导电、弯折这三项测试里的表现。每测完一项，表格里就会记下结果。四种材料都测一测，对比一下，金属和其他材料到底差在哪里。",
    "module-2": "知道了金属的本领，我们就能解释生活里的选择了。为什么要用金属做锅身？因为金属导热快，火一烧，热量很快传到锅里，菜才熟得快。为什么电线里面是铜、外面包一层塑料？因为铜容易导电，可以让电流通过；塑料不容易导电，包在外面就能保护我们不被电到。为什么窗框用金属？因为金属结实，能弯成需要的形状，还不容易坏。为什么雨衣不用金属？因为金属不防水，还会生锈。你看，人们挑材料，看的不是它好不好看，而是它的性质合不合适。",
    "lab-2": "接下来是选材任务。这里有四个任务，每个任务下面有几个候选材料。请你给每件东西挑一种最合适的材料，点一下，马上会告诉你选对了没有，以及为什么。选错了也别急，看看解释，再换一个试试。",
    "worked-example": "我们一起来分析一道题。为什么炒菜锅的锅身用金属做，锅柄却要用塑料或者木头？第一步，先看清两处的共同点，锅身和锅柄都要连着同一口锅，都会变热。第二步，比较两处对材料的要求，锅身需要尽快把火的热量传进锅里，锅柄正好相反，需要尽量不让热量传到手上。第三步，根据性质选材料，金属导热快，适合做锅身；塑料和木头导热慢，适合做锅柄。第四步，说清道理，材料的用途不是随便定的，而是由它的性质决定的。同一口锅上用了两种材料，正是因为两个部位对导热的要求正好相反。",
    "conceptest-1": "下面用三个容易搞混的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后请你当一次小小工程师。你要给一件物品挑选材料，除了选对材料，还要说清楚理由。请你先选一件物品，写出你选什么材料、为什么选它，最后对照右边的自检清单，看看自己的理由是不是完整。",
    "posttest": "最后再用三道题检验一下。这一次有高压锅、有铝合金、也有暖水壶，看看你能不能把「性质决定用途」用上去。",
    "summary": "这节课我们抓住了一条主线。金属有四个共同的性质：容易导热、容易导电、有延展性、有金属光泽。更重要的是，材料的性质决定了它的用途。锅身要导热，所以用金属；锅柄要隔热，所以用塑料或木头；电线的芯要导电，所以用铜；外面要绝缘，所以用塑料。换成别的材料，功能就实现不了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出金属的四条共同性质，每条各举一个用到的例子。第二层能力应用，动手做：在家里找三件物品，写出它们分别用了什么材料，以及为什么用这种材料。第三层迁移挑战，选做：为学校食堂设计一把更安全的勺子，写出你选的材料和理由，并说明这种材料在哪一条性质上满足了需要。",
    "knowledge-graph": "这张图展示了这节课在科学知识网里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 金属的共同性质", "lab-1": "实验室一 性质检测台", "module-2": "概念二 性质决定用途",
    "lab-2": "实验室二 选材任务", "worked-example": "例题讲解 锅身与锅柄", "conceptest-1": "概念测试",
    "synthesis": "综合任务 小小工程师", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

MATERIALS = [
    {"id": "wood", "n": "木头", "heat": "慢", "heat_t": "放在热水里很久，摸上去还是温温的。", "elec": "不导电", "elec_t": "接进电路，小灯泡不亮。", "bend": "不能弯", "bend_t": "用力一掰就裂开，会断。", "metal": False},
    {"id": "plastic", "n": "塑料", "heat": "慢", "heat_t": "放在热水里很久，摸上去还是温温的。", "elec": "不导电", "elec_t": "接进电路，小灯泡不亮。", "bend": "不能弯", "bend_t": "用力弯会发白，接着就断。", "metal": False},
    {"id": "ceramic", "n": "陶瓷", "heat": "很慢", "heat_t": "放在热水里，几乎感觉不到变热。", "elec": "不导电", "elec_t": "接进电路，小灯泡不亮。", "bend": "不能弯", "bend_t": "一敲就碎，完全不能弯。", "metal": False},
    {"id": "metal", "n": "金属（铁丝）", "heat": "快", "heat_t": "一放进热水，很快就烫手了。", "elec": "导电", "elec_t": "接进电路，小灯泡马上就亮了。", "bend": "能弯", "bend_t": "可以弯成各种形状，还不会断。", "metal": True},
]

PICK_TASKS = [
    {"id": "wok", "q": "锅身要很快把火的热量传进锅里，用什么材料？",
     "opts": [("金属", True), ("木头", False), ("塑料", False)],
     "why": "金属导热快，火一烧热量就传进锅里，菜熟得快。木头和塑料导热慢，做锅身煮不熟菜。"},
    {"id": "wire", "q": "电线的芯要让电流顺利通过，用什么材料？",
     "opts": [("铜（金属）", True), ("橡皮", False), ("陶瓷", False)],
     "why": "金属容易导电，铜的导电性很好，所以电线芯用铜。橡皮和陶瓷都不导电，电流过不去。"},
    {"id": "frame", "q": "窗框要结实、能弯成需要的形状，用什么材料？",
     "opts": [("铝合金（金属）", True), ("纸板", False), ("玻璃", False)],
     "why": "金属结实又有延展性，能加工成各种形状，还不容易坏。纸板太软，玻璃太脆。"},
    {"id": "raincoat", "q": "雨衣要挡雨、还要轻软，用什么材料？",
     "opts": [("塑料", True), ("铁皮", False), ("铜丝", False)],
     "why": "塑料不吸水又轻软，适合做雨衣。金属不防水还会生锈，做成雨衣又重又冷。"},
]

MATRIX_TESTS = [("heat", "导热"), ("elec", "导电"), ("bend", "能否弯折")]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-metal-materials 互动逻辑
   1) 选择题接线
   2) 性质检测台：4 种材料 × 3 项测试，即时记录到表格
   3) 选材任务：4 个任务，选材料 → 判定 + 依据
   4) 综合任务：物品选择 + 自检清单（实时计数）
   ============================================================ */
(function () {
  'use strict';

  document.querySelectorAll('[data-quiz-block]').forEach(function (block) {
    block.querySelectorAll('.choice').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (block.dataset.answered === '1') return;
        block.dataset.answered = '1';
        var ok = btn.dataset.correct === '1';
        btn.classList.add(ok ? 'correct' : 'wrong');
        block.querySelectorAll('.choice').forEach(function (b) {
          if (b.dataset.correct === '1') b.classList.add('correct');
          b.disabled = true;
        });
        var ex = block.querySelector('[data-explain]');
        if (ex) ex.style.display = 'block';
      });
    });
  });

  /* ---------- 性质检测台 ---------- */
  var DATA = {
    wood:    { n: '木头',   heat: ['慢', '放在热水里很久，摸上去还是温温的。', 0],
                          elec: ['不导电', '接进电路，小灯泡不亮。', 0],
                          bend: ['不能弯', '用力一掰就裂开，会断。', 0] },
    plastic: { n: '塑料',   heat: ['慢', '放在热水里很久，摸上去还是温温的。', 0],
                          elec: ['不导电', '接进电路，小灯泡不亮。', 0],
                          bend: ['不能弯', '用力弯会发白，接着就断。', 0] },
    ceramic: { n: '陶瓷',   heat: ['很慢', '放在热水里，几乎感觉不到变热。', 0],
                          elec: ['不导电', '接进电路，小灯泡不亮。', 0],
                          bend: ['不能弯', '一敲就碎，完全不能弯。', 0] },
    metal:   { n: '金属（铁丝）', heat: ['快', '一放进热水，很快就烫手了。', 1],
                          elec: ['导电', '接进电路，小灯泡马上就亮了。', 1],
                          bend: ['能弯', '可以弯成各种形状，还不会断。', 1] }
  };
  var stageM = document.getElementById('mat-stage');
  if (stageM) {
    var curMat = 'wood';
    var seen = {};   /* 已测过的组合 */
    var vRes = document.getElementById('mat-result');
    var vProgress = document.getElementById('mat-progress');

    function key(m, t) { return m + '-' + t; }

    function renderMat() {
      document.querySelectorAll('[data-mat]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.mat === curMat);
      });
      document.querySelectorAll('[data-test]').forEach(function (b) {
        var k = key(curMat, b.dataset.test);
        b.classList.toggle('selected', !!seen[k]);
      });
      var total = 0;
      for (var k in seen) { if (seen[k]) total++; }
      vProgress.textContent = total + ' / 12';
      /* 填表 */
      Object.keys(DATA).forEach(function (mk) {
        Object.keys({ heat: 1, elec: 1, bend: 1 }).forEach(function (tk) {
          var cell = document.getElementById('cell-' + mk + '-' + tk);
          if (!cell) return;
          if (seen[key(mk, tk)]) {
            cell.textContent = DATA[mk][tk][0];
            cell.style.background = DATA[mk][tk][2] ? 'rgba(78,205,196,.18)' : 'rgba(255,209,102,.18)';
            cell.style.fontWeight = '700';
          } else {
            cell.textContent = '—';
            cell.style.background = '';
            cell.style.fontWeight = '';
          }
        });
      });
      if (total === 12) {
        vRes.className = 'result';
        vRes.innerHTML = '<strong>十二项全部测完了。</strong>你看这一列：只有金属那一行，导热快、能导电、还能弯。木、塑料、陶瓷都是慢、不导电、不能弯。导热、导电、有延展性，正是金属和其他材料最不一样的地方。';
      }
    }

    document.querySelectorAll('[data-mat]').forEach(function (b) {
      b.addEventListener('click', function () {
        curMat = b.dataset.mat;
        vRes.className = 'result warn';
        vRes.innerHTML = '已选中 <strong>' + DATA[curMat].n + '</strong>。现在点下面三项测试中的任意一项。';
        renderMat();
      });
    });
    document.querySelectorAll('[data-test]').forEach(function (b) {
      b.addEventListener('click', function () {
        var t = b.dataset.test;
        seen[key(curMat, t)] = true;
        var d = DATA[curMat][t];
        vRes.className = 'result ' + (d[2] ? '' : 'warn');
        vRes.innerHTML = '<strong>' + DATA[curMat].n + ' · 测试' + b.textContent.trim() + ' → ' + d[0] + '</strong><br>' + d[1];
        renderMat();
      });
    });
    vRes.className = 'result warn';
    vRes.innerHTML = '先点上面选一种材料，再点下面三项测试中的任意一项。';
    renderMat();
  }

  /* ---------- 选材任务 ---------- */
  var PICK = {
    wok:   { ok: '金属', why: '金属导热快，火一烧热量就传进锅里，菜熟得快。木头和塑料导热慢，做锅身煮不熟菜。' },
    wire:  { ok: '铜（金属）', why: '金属容易导电，铜的导电性很好，所以电线芯用铜。橡皮和陶瓷都不导电，电流过不去。' },
    frame: { ok: '铝合金（金属）', why: '金属结实又有延展性，能加工成各种形状，还不容易坏。纸板太软，玻璃太脆。' },
    raincoat: { ok: '塑料', why: '塑料不吸水又轻软，适合做雨衣。金属不防水还会生锈，做成雨衣又重又冷。' }
  };
  var pickRoot = document.getElementById('pick-root');
  if (pickRoot) {
    var solved = 0;
    var pickOut = document.getElementById('pick-out');
    pickRoot.querySelectorAll('[data-task]').forEach(function (block) {
      var tid = block.dataset.task;
      block.querySelectorAll('.choice').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (block.dataset.done === '1') return;
          var chosen = btn.textContent.trim();
          var info = PICK[tid];
          if (chosen === info.ok) {
            block.dataset.done = '1';
            solved++;
            btn.classList.add('correct');
            block.querySelectorAll('.choice').forEach(function (b) { b.disabled = true; });
            pickOut.className = 'result';
            pickOut.innerHTML = '<strong>选对了！' + chosen + ' —— </strong>' + info.why;
            if (solved === 4) {
              pickOut.className = 'result';
              pickOut.innerHTML = '<strong>四个任务全部完成。</strong>你已经在用一个很有用的思路：先看这件东西需要什么本领，再去找有这种本领的材料。';
            }
          } else {
            btn.classList.add('wrong');
            btn.disabled = true;
            pickOut.className = 'result error';
            pickOut.innerHTML = '<strong>再想一下：</strong>' + chosen + ' 有这样的本领吗？' + '先问自己一句：这个部位最需要什么本领？';
          }
        });
      });
    });
    pickOut.className = 'result warn';
    pickOut.textContent = '给四件东西各挑一种最合适的材料，每选一次都会告诉你理由。';
  }

  /* ---------- 综合任务：自检清单 ---------- */
  var checkRoot = document.getElementById('check-root');
  if (checkRoot) {
    var boxes = checkRoot.querySelectorAll('input[type="checkbox"]');
    var countEl = document.getElementById('check-count');
    var msgEl = document.getElementById('check-msg');
    function refresh() {
      var n = 0;
      boxes.forEach(function (b) { if (b.checked) n++; });
      countEl.textContent = n + ' / ' + boxes.length;
      if (n === boxes.length) {
        msgEl.className = 'result';
        msgEl.innerHTML = '<strong>理由完整了。</strong>你既说了用途需要什么本领，也说了材料有什么性质，还做了对比——这就是工程师说理的方式。';
      } else {
        msgEl.className = 'result warn';
        msgEl.textContent = '还差 ' + (boxes.length - n) + ' 项。把每一项都写进你的理由里，你的方案就站得住脚了。';
      }
    }
    boxes.forEach(function (b) { b.addEventListener('change', refresh); });
    refresh();
  }
})();
"""


def build_pages():
    import json as _json

    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这些东西为什么用这种材料？", TTS["pretest"], [
        {"q": "炒菜锅的锅身为什么用金属做？",
         "options": [("金属导热快，火的热量很快就传进锅里", True), ("金属比较好看", False), ("金属比较便宜", False)],
         "explain": "锅要尽快把火的热量传给菜，所以挑导热快的金属。<strong>错因提醒：</strong>常见错误是只看价格和外观去解释用途。判断材料用途，要先看这个部位需要什么本领。"},
        {"q": "电线的外面为什么要包一层塑料？",
         "options": [("塑料不容易导电，可以保护我们不被电到", True), ("塑料比金属结实", False), ("塑料导热比金属快", False)],
         "explain": "电线外皮要绝缘，所以用不导电的塑料。<strong>错因提醒：</strong>不少同学把导热和导电搞混了。导热说的是传热快慢，导电说的是能不能让电流通过，这是两件事。"},
        {"q": "下面哪一组都是金属的共同性质？",
         "options": [("容易导热、容易导电、有延展性、有金属光泽", True),
                     ("容易导热、不导电、很脆容易碎", False),
                     ("透明、不导电、能弯成任何形状", False)],
         "explain": "导热、导电、延展性、金属光泽是大多数金属的共同点。金属并不透明，也不是一敲就碎。<strong>错因提醒：</strong>把陶瓷「脆」的特点误认为金属的特点，是最常见的混淆。"}
    ], tag="前测"))

    rows = []
    for m in MATERIALS:
        cells = "".join(
            f'<td id="cell-{m["id"]}-{t}" style="border:1px solid var(--line-subtle);padding:6px;text-align:center;font-size:13px;color:var(--muted)">—</td>'
            for t, _ in MATRIX_TESTS
        )
        rows.append(
            f'              <tr><th style="border:1px solid var(--line-subtle);padding:6px;font-size:13px;background:var(--bg-subtle)">{m["n"]}</th>{cells}</tr>'
        )
    matrix_rows = "\n".join(rows)
    matrix_head = "".join(
        f'<th style="border:1px solid var(--line-subtle);padding:6px;font-size:13px;background:var(--bg-subtle)">{label}</th>'
        for _, label in MATRIX_TESTS
    )

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "金属有四个共同的性质：导热、导电、能弯、会反光", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">把铁丝、木头、塑料、陶瓷放在一起比一比，你会发现金属有几条别的材料<strong>同时都不具备</strong>的本领。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>容易导热</strong></p>
            <p style="color:var(--muted)">放进热水，金属很快就烫手；木头和塑料半天还是温的。金属把热量传得快。</p>
          </div>
          <div class="inner-card">
            <p><strong>容易导电</strong></p>
            <p style="color:var(--muted)">接进电路，小灯泡马上亮；换成木头、塑料、陶瓷，灯泡不亮。</p>
          </div>
          <div class="inner-card">
            <p><strong>有延展性</strong></p>
            <p style="color:var(--muted)">铁丝能弯成各种形状还不断，能被拉成细丝、压成薄片。陶瓷一敲就碎。</p>
          </div>
          <div class="inner-card">
            <p><strong>有金属光泽</strong></p>
            <p style="color:var(--muted)">金属表面亮亮的，会反光。这是用眼睛就能看出来的第一条线索。</p>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>注意：</strong>这四条说的是<strong>大多数金属</strong>。不同的金属本领强弱不一样，所以做锅常用铁和铝，做电线芯常用铜。</div></div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="四种材料导热导电弯折对比图：木头、塑料、陶瓷、金属">
          <figcaption>木头、塑料、陶瓷三项测试都是「慢 / 不导电 / 不能弯」，只有金属是「快 / 导电 / 能弯」——这一整行的差别，就是金属的共同性质</figcaption>
        </figure>
{insight_box([
    {"lens": "看见它", "text": "看一行就够：金属那一行三项全中，其他三种材料三项全不中。这不是巧合，是金属这一类材料的共同点。"},
    {"lens": "比较它", "text": "导热和导电是两件不同的事。有些材料导热快却不导电，所以千万不能把「烫手」和「能通电」当成同一件事。"},
    {"lens": "迁移它", "text": "判断一种材料是不是金属，不必认识它：擦亮看有没有光泽，弯一弯看会不会断，放进热水看传热快不快。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "性质检测台：四样材料，三项测试", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选材料，再点测试。每测一项，右下角的表格就会自动记下结果。四项都测完，你就能一眼看出差别。</p>
        <div class="lab-panel" id="mat-stage">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选择要检测的材料</div>
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-mat="wood" style="text-align:center">木头</button>
            <button class="choice" data-mat="plastic" style="text-align:center">塑料</button>
            <button class="choice" data-mat="ceramic" style="text-align:center">陶瓷</button>
            <button class="choice" data-mat="metal" style="text-align:center">金属（铁丝）</button>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 选择要做的测试</div>
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-test="heat" style="text-align:center">放进热水</button>
            <button class="choice" data-test="elec" style="text-align:center">接进电路</button>
            <button class="choice" data-test="bend" style="text-align:center">用力弯折</button>
          </div>
          <p class="result warn" id="mat-result" style="margin-top:12px"></p>
          <div style="display:flex;align-items:center;gap:10px;margin-top:10px">
            <span style="font-size:13px;color:var(--muted)">检测进度</span>
            <span class="readout-cell" style="flex:0 0 auto;padding:4px 12px"><span class="v green" id="mat-progress" style="font-size:16px">0 / 12</span></span>
          </div>
          <table style="width:100%;border-collapse:collapse;margin-top:12px">
            <tr><th style="border:1px solid var(--line-subtle);padding:6px;font-size:13px;background:var(--bg-subtle)">材料 \\ 测试</th>{matrix_head}</tr>
{matrix_rows}
          </table>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>挑战：</strong>把四种材料的三项都测完。然后回答一句话——哪一行三项都是「行」，哪三行三项都是「不行」？</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "材料的性质，决定了它被用来做什么", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">知道了性质，生活里那些「为什么用这种材料」的问题就都有答案了。挑材料的思路只有一条：<strong>先看这个部位需要什么本领，再去找有这种本领的材料。</strong></p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>锅身用金属：</strong>需要导热快，金属正好导热快，火一烧热量就传进锅里。</div></div>
          <div class="step"><span class="n">2</span><div><strong>电线芯用铜、外皮用塑料：</strong>芯要导电，所以用金属；外皮要不导电，所以用塑料。</div></div>
          <div class="step"><span class="n">3</span><div><strong>窗框用铝合金：</strong>要结实又要有延展性，能加工成需要的形状。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>雨衣不用金属：</strong>金属不防水还会生锈，做成雨衣又重又冷，所以用轻软的塑料。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="用途与材料的匹配图：锅身、电线、窗框、雨衣分别用什么材料">
          <figcaption>同一件东西的不同部位，需要不同的本领，就会用不同的材料：锅身要导热用金属，锅柄要隔热用塑料或木头</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学误认为「金属最结实，所以哪里都用金属最好」。可是雨衣用金属就没法穿，锅柄用金属就会烫手。材料没有好坏，只有合不合适。</p>
        </div>
    ''', tag="概念二"))

    tasks_html = []
    for t in PICK_TASKS:
        btns = "\n".join(
            f'              <button class="choice" style="text-align:center">{o[0]}</button>'
            for o in t["opts"]
        )
        tasks_html.append(f'''          <div class="inner-card" data-task="{t["id"]}">
            <p><strong>{t["q"]}</strong></p>
            <div class="grid grid-3" style="margin-top:8px">
{btns}
            </div>
          </div>''')
    tasks_block = "\n".join(tasks_html)

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "选材任务：给四件东西挑材料", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">每件东西都先问一句：它最需要什么本领？然后挑有这种本领的材料。</p>
        <div class="lab-panel" id="pick-root">
{tasks_block}
          <p class="result warn" id="pick-out" style="margin-top:12px">给四件东西各挑一种最合适的材料，每选一次都会告诉你理由。</p>
        </div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：锅身和锅柄，为什么要用两种材料", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>同一口炒菜锅，锅身用金属做，锅柄却用塑料或者木头。请说明为什么两处要用不同的材料。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>锅身和锅柄连在同一口锅上，都会受热，但一个在火那边，一个在手这边。</div></div>
          <div class="step"><span class="n">2</span><div><strong>比较要求：</strong>锅身要求尽快把热量传进锅里；锅柄的要求正好相反，要让热量尽量传不过去。</div></div>
          <div class="step"><span class="n">3</span><div><strong>对照性质：</strong>金属导热快，适合锅身；塑料和木头导热慢，适合锅柄。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>说清道理：</strong>一个部位需要「传热快」，另一个部位需要「传热慢」，要求相反，所以选的材料也相反。这正是性质决定用途的最好例子。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">只答「因为金属导热快」是不完整的。题目问的是两处为什么不同，回答里必须把<strong>两个部位的要求对比</strong>写出来。只说一半，理由就站不住。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：这三种说法错在哪里", TTS["conceptest-1"], [
        {"q": "下面哪种说法是正确的？",
         "options": [("有些材料导热快但不导电，所以导热和导电不能混为一谈", True),
                     ("只要导热快，就一定导电", False),
                     ("金属都很软，一掰就弯", False)],
         "explain": "导热说的是传热，导电说的是通电，是两种不同的性质。<strong>错因提醒：</strong>把两者看成同一件事，是这一课最常见的混淆。"},
        {"q": "厨房里的木铲、木勺，主要利用的是木头的什么性质？",
         "options": [("导热慢，拿在手里不烫", True), ("导电快", False), ("有金属光泽", False)],
         "explain": "木铲要接触热锅，所以必须挑导热慢的材料。<strong>错因提醒：</strong>有同学以为「木头结实」才是原因，忽略了这里最关键的是不烫手。"},
        {"q": "关于材料的选择，下面哪种说法最合理？",
         "options": [("材料没有绝对的好坏，要看这个部位需要什么本领", True),
                     ("金属什么都好，能用金属就用金属", False),
                     ("越贵的材料越合适", False)],
         "explain": "选材料看的是性质合不合适，不是贵不贵。<strong>错因提醒：</strong>误认为金属万能，是生活中的常见错误——雨衣、锅柄都不能用金属。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次小小工程师", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">选一件你熟悉的物品，为它挑选材料，再把理由写完整。右侧的自检清单会实时告诉你理由够不够。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div class="inner-card">
              <p><strong>① 写出你的方案</strong></p>
              <textarea rows="6" placeholder="我选的物品是……&#10;它最需要什么本领……&#10;我选的材料是……&#10;因为这种材料……"></textarea>
            </div>
            <div class="inner-card" id="check-root">
              <p><strong>② 自检清单</strong> <span class="tag" style="float:right"><span id="check-count">0 / 4</span></span></p>
              <label style="display:block;font-size:14px"><input type="checkbox" style="min-height:0;width:auto;margin-right:8px">我写清了这件物品<strong>需要什么本领</strong></label>
              <label style="display:block;font-size:14px"><input type="checkbox" style="min-height:0;width:auto;margin-right:8px">我写清了我选的<strong>材料有什么性质</strong></label>
              <label style="display:block;font-size:14px"><input type="checkbox" style="min-height:0;width:auto;margin-right:8px">我做了<strong>对比</strong>，说出别的材料为什么不合适</label>
              <label style="display:block;font-size:14px"><input type="checkbox" style="min-height:0;width:auto;margin-right:8px">我说清了<strong>性质和使用效果</strong>的关系</label>
              <p class="result warn" id="check-msg" style="margin-top:10px"></p>
            </div>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛠️</span><div>写完之后讲给同桌听，请他指出哪一句理由还缺证据，再补上。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "高压锅的锅身用不锈钢，锅柄用隔热塑料。这样设计主要是因为：",
         "options": [("锅身要传热快，锅柄要传热慢，两个部位的要求相反", True),
                     ("塑料比不锈钢结实", False),
                     ("不锈钢不容易生锈，所以锅柄也该用不锈钢", False)],
         "explain": "要求相反，材料就相反。锅身要快，锅柄要慢，这就是性质决定用途。"},
        {"q": "为什么很多窗框用铝合金，而不是用纯铁？最合理的解释是：",
         "options": [("铝合金比纯铁轻，而且不容易生锈，同时照样结实", True),
                     ("铝合金比铁更透明", False),
                     ("铝合金不导热", False)],
         "explain": "既要结实，又要轻、要耐锈，这三条要求一起考虑，铝合金比纯铁更合适。"},
        {"q": "暖水壶的内胆是双层玻璃，中间抽成接近真空。这样做的主要目的是：",
         "options": [("防止热的传递，让热水凉得慢一些", True),
                     ("让水壶更结实", False),
                     ("让水壶看起来更好看", False)],
         "explain": "真空里几乎没有东西可以传热，所以热量很难跑掉。这也说明：想要保温，就要选不容易导热的材料和结构。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：性质决定用途", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>金属的共同性质</strong>：容易导热、容易导电、有延展性、有金属光泽。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>核心思路</strong>：先看这个部位需要什么本领，再去找有这种本领的材料。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>同一件物品可以有不同的部位</strong>：锅身要导热用金属，锅柄要隔热用塑料或木头。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>材料没有好坏</strong>：适合的才是最好的，雨衣就不该用金属。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那口锅：</strong>锅身是金属，因为它要把火的热量快点传进来；锅柄是塑料或木头，因为它要挡住热量、别烫到手。一口锅上用了两种材料，不是随便选的，而是<strong>两个部位对导热的要求正好相反</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>打个比方记住它：</strong>挑材料就像给球队安排位置。跑得快的去当前锋，个子高的去抢篮板——不是谁最好，而是谁最适合这个位置。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出金属的四条共同性质，每条各举一个生活里用到的例子。",
            "用一句话写出选择材料时的基本思路。",
        ],
        [
            "在家里找三件物品，写出它们分别用了什么材料，并说明为什么用这种材料。",
            "用一盆热水分别泡一根铁丝和一把塑料勺，一分钟后摸一摸，比较两者温度，把结果记下来。",
        ],
        [
            "为学校食堂设计一把更安全的勺子，写出你选的材料、理由，并说明这种材料在哪一条性质上满足了需要。",
            "找一种不是金属但也被广泛使用的材料（比如塑料、陶瓷、玻璃），说明它最适合用在什么地方，说清你的依据。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-metal-materials",
    "node_id": "sci-e-metal-materials",
    "title": "金属：为什么锅是金属做的",
    "name_en": "Metals: Why Are Pots Made of Metal?",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 材料",
    "lesson_type": "experiment-inquiry",
    "version": "1.0.0",
    "description": "通过四材料三测试的性质检测台与四个真实选材任务，让学生自己归纳出金属导热、导电、有延展性、有金属光泽四条共同性质，并建立「材料性质决定用途」的核心思路。",
    "tags": ["金属", "材料性质", "导热", "导电", "延展性", "性质决定用途"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念1「物质的结构与性质」学习内容1.3 金属及合金是重要的材料——5～6年级能举例说出金属的常见性质，知道材料的性质决定其用途。",
    "hero_question": "同一口锅，锅身是铁的，锅柄却是塑料的——人们凭什么这样选材料？",
    "hero_alt": "金属性质与用途知识结构图：导热、导电、延展性、金属光泽，以及性质决定用途",
    "hero_caption": "金属的四个共同性质：容易导热 · 容易导电 · 有延展性 · 有金属光泽；材料的性质决定它的用途",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "金属到底有哪些共同的本领？", "d": "想知道判断金属的四条线索", "v": "金属到底有哪些共同的本领"},
        {"t": "怎么比较两种材料的好坏？", "d": "想知道该用哪些测试去比", "v": "怎么比较两种材料的好坏"},
        {"t": "锅柄为什么不用金属做？", "d": "想弄明白锅上的两种材料", "v": "锅柄为什么不用金属做"},
        {"t": "怎样给一件东西挑材料？", "d": "想自己当一次工程师", "v": "怎样给一件东西挑材料"},
    ],
    "objectives": [
        "能说出金属的共同性质：容易导热、容易导电、有延展性、有金属光泽",
        "能设计简单的检测方法，比较不同材料的导热性与导电性",
        "能说出材料的性质决定了它的用途，并举例说明",
        "能为一件物品选择合适的材料，并说出完整的理由",
    ],
    "objectives_plain": [
        "能说出金属的共同性质：容易导热、容易导电、有延展性、有金属光泽",
        "能设计简单的检测方法，比较不同材料的导热性与导电性",
        "能说出材料的性质决定了它的用途，并举例说明",
        "能为一件物品选择合适的材料，并说出完整的理由",
    ],
    "standards": [
        {"content": "能举例说出金属的常见性质（导热、导电、延展性、金属光泽）",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念1 物质的结构与性质 学习内容1.3 金属及合金是重要的材料（5～6年级）"},
        {"content": "知道材料的性质决定其用途，能根据用途选择合适的材料并说明理由",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念1 物质的结构与性质 学习内容1.3 金属及合金是重要的材料（5～6年级）"},
    ],
    "prereqs": ["sci-e-materials-in-life"],
    "prereqs_name": "生活中的材料",
    "prereqs_meta": "sci-e-materials-in-life",
    "leads_to": ["sci-e-chemical-change"],
    "next_meta": "sci-e-chemical-change",
    "section_images": ["assets/sci-e-metal-materials-fig1.webp", "assets/sci-e-metal-materials-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "同一口锅，锅身是铁的，锅柄却是塑料的——带着这个疑问开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能为一件物品挑材料并说出理由。",
        "objectives": "看清四件事：说出金属四条性质、会比较材料、知道性质决定用途、能完整说理。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "木头、塑料、陶瓷三项测试全不中，只有金属三项全中——这一行就是金属的共同性质。",
        "lab-1": "先选材料，再点测试。十二项全测完，表格里的对比会自己说话。",
        "module-2": "先问这个部位需要什么本领，再去找有这种本领的材料。",
        "lab-2": "四件东西各挑一种材料，选错也别急，看看理由再换一个。",
        "worked-example": "四步走：看清条件、比较要求、对照性质、说清道理。两处的要求是相反的。",
        "conceptest-1": "导热和导电是两件事，别搞混；材料也没有好坏，只有合不合适。",
        "synthesis": "先把方案写出来，再逐条对照自检清单，看理由够不够完整。",
        "posttest": "换了高压锅、铝合金和暖水壶，看看你还能不能用上同一条思路。",
        "summary": "回到开头那口锅：锅身和锅柄为什么用不同的材料？用一句话说清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「物质的结构与性质」里材料板块长期空缺的一课：知识树原有生活中的材料，缺课标明确要求的金属及合金。设计上把结论完全交给学生自己归纳——用四材料三测试的检测台把十二格数据填满，金属那一行的独特性会自己显形；再用四个真实选材任务把「性质决定用途」变成可操作的判断流程，最后用锅身与锅柄这一组相反要求收束，让学生能完整说理而不是只答半句。",
    "plan_table": """| 1 | cover | 金属：为什么锅是金属做的 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这些东西为什么用这种材料？ | 起·前测（暴露直觉） |
| 5 | concept | 金属有四个共同的性质：导热、导电、能弯、会反光 | 承·概念一 |
| 6 | interactive | 性质检测台：四样材料，三项测试 | 承·实验室一（12 格数据自己长出来） |
| 7 | concept | 材料的性质，决定了它被用来做什么 | 承·概念二（含常见错误） |
| 8 | interactive | 选材任务：给四件东西挑材料 | 承·实验室二（真实选材） |
| 9 | concept | 例题示范：锅身和锅柄，为什么要用两种材料 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：这三种说法错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次小小工程师 | 合·迁移应用（含自检清单） |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：性质决定用途 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：金属四条性质 + 性质决定用途\n- P5 四材料三测试对比图（已生成）：木头/塑料/陶瓷/金属导热导电弯折对比\n- P7 用途与材料匹配图（已生成）：锅身、电线、窗框、雨衣分别用什么材料\n- 若需补充：金属光泽的实拍特写、铜丝与铁丝的延展性对比照片",
}
