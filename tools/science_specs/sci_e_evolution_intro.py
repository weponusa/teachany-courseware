# -*- coding: utf-8 -*-
"""小学科学 · 生物的进化：长脖子是怎么来的（G6）—— 补齐课标「生命的延续与进化·8.6 生物的进化」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-evolution-intro-fig1.webp'
F2 = './assets/sci-e-evolution-intro-fig2.webp'

TTS = {
    "hero": "先看一个想不通的问题。长颈鹿的脖子那么长，它到底是怎么来的？有人说是长颈鹿天天伸脖子去够高处的树叶，伸着伸着就变长了。可是，天天伸手能把手变长吗？这节课我们就跟着化石的记录，把长脖子到底怎么来的这件事，一步一步弄清楚。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道化石是什么、能告诉我们什么，还是想知道长脖子到底怎么来的，又或者你想亲手做一次自然选择的模拟实验。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出同种生物的后代之间总有差异，这种差异叫做变异。第二，能举出化石作为生物进化直接证据的例子，知道越深的地层里化石越古老。第三，能用自然选择的说法解释长脖子是怎么一代代留下来的。第四，能区分用进废退和自然选择这两种说法有什么不同。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "我们先看第一个问题：同一种生物，长得都一样吗？当然不是。同一个妈妈生的几只小狗，毛色、个头、脾气都不一样；同一棵树结的果子，也有的大有的小。这种同种生物后代之间的差异，叫做变异。变异不是偶尔才发生的意外，它是普遍存在的，而且是可遗传的。变异给进化准备了一堆不同的原材料。接下来再看化石。化石是指保存在岩层里的古生物遗体或者遗迹。岩层是一层一层叠起来的，越往下面越古老，里面的化石也越古老。把不同地层的化石按顺序排起来，我们就能看到：生物不是一直长现在这个样子的，它们真的变过。化石是生物进化最直接的证据。",
    "lab-1": "现在请你当一次考古队员，去挖一挖地层。下面有五层岩石，从最上面最新的那一层，一直挖到最下面最古老的那一层。点一点每一层，看看那一层里藏着什么化石，再想想它们和现在的生物比起来有什么不一样。挖完之后你会发现，越深的地层里，生物的样子越陌生。",
    "module-2": "弄清楚了变异和化石，我们回头解决长脖子的问题。假设很久以前的长颈鹿祖先，脖子有的长一点，有的短一点，这是变异。它们生活的地方，低处的树叶被吃光了，只剩下高处的树叶。这时候，脖子长一点的个体能吃到树叶，活了下来，还能生宝宝；脖子短一点的吃不到，慢慢就活不下去，留下的后代也少。环境就像一个筛子，把更适合在这里生存的个体筛了出来，这个过程叫做自然选择。一代一代筛下去，长脖子的个体越来越多，短脖子的越来越少，几百万年积累下来，长颈鹿的脖子就变长了。这里要特别注意，不是长颈鹿想变长就变长，而是先有了长短不同的变异，再由环境筛出能活下来的那一批。",
    "lab-2": "现在请你亲手做一次自然选择的模拟。草地上有一群小虫，有的偏绿，有的偏枯黄，一开始两种数量差不多。你可以改变环境，让草地从绿油油变成一片枯黄，然后点繁殖按钮，让它们一代一代生下去。每一代都会把更容易被天敌发现的个体筛掉。看看十几代之后，与环境颜色接近的个体比例会变成多少。",
    "worked-example": "我们一起来分析一道题。有人说：长颈鹿因为天天想吃高处的树叶，所以拼命伸长脖子，脖子就变长了，还传给了宝宝。这个说法对吗？第一步，看清题目要我们判断的是什么：说的是脖子变长的原因。第二步，找出这句话里的问题：它说的是长颈鹿先努力，身体再改变，然后这个改变还能遗传给孩子。第三步，用学过的知识对照：一辈子练出来的变化，不能写进遗传信息里，所以不会直接传给后代。第四步，换成正确的说法：长颈鹿祖先里本来就有脖子长一点和短一点的变异，环境筛出了脖子长的那一批，让它们留下更多后代，一代代积累，脖子才慢慢变长。所以那句话错在把顺序弄反了，也错在把练出来的变化当成能遗传的变化。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次小小解说员。博物馆里有一块展板，旁边站着很多好奇的小朋友。请你用「变异、环境筛选、一代代积累、化石证据」这四个词，写一段三到五句话的解说词，把长颈鹿长脖子的来历讲清楚，让别人一听就明白。",
    "posttest": "最后用新的情境检验一下。这次的问题里出现了细菌、杀虫剂和地雀，看看你能不能把变异和环境筛选这两件事用上去。",
    "summary": "这节课我们弄明白了三件事。第一，同种生物的后代之间总有差异，这种差异叫做变异，它是进化的原材料。第二，环境会筛掉不那么适合生存的个体，留下更适合的个体，一代代积累下来，就形成了进化，这个过程叫做自然选择。第三，化石是生物进化的直接证据，越深的地层里化石越古老。回到开头的问题，长脖子不是伸出来的，而是先有长短的变异，再被环境一代代筛出来的。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出变异、自然选择、化石三个词的意思，并各配一个例子。第二层能力应用，动手做：和家人一起玩一次自然选择模拟，把每一代保护色个体的比例记成一张表格，看看变化的趋势。第三层迁移挑战，选做：选一种你熟悉的生物，画一张三步推理图，说清楚它的某个特点可能是被什么环境筛出来的。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 变异与化石", "lab-1": "实验室一 地层化石时间轴", "module-2": "概念二 环境筛选出长脖子",
    "lab-2": "实验室二 自然选择模拟", "worked-example": "例题讲解 脖子是伸长的吗", "conceptest-1": "概念测试",
    "synthesis": "综合任务 小小解说员", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 地层化石时间轴数据（层序：由上到下 = 由新到老）
STRATA = [
    {"t": "第 1 层（最上面）", "age": "约 100 万年前至今",
     "life": "人类祖先、现代哺乳动物、现代鸟类",
     "note": "最上面的岩层最年轻，里面的化石已经和今天的生物很像了。"},
    {"t": "第 2 层", "age": "约 6600 万年前",
     "life": "恐龙、菊石、早期哺乳动物",
     "note": "恐龙和菊石的化石只出现在这一带以下，往上就突然不见了。"},
    {"t": "第 3 层", "age": "约 2.5 亿年前",
     "life": "刚出现的恐龙、裸子植物森林",
     "note": "这时候陆地上的动植物和今天差别已经很大。"},
    {"t": "第 4 层", "age": "约 3.6 亿年前",
     "life": "繁盛的鱼类、最早的两栖动物、高大蕨类",
     "note": "生命主要在水里，刚刚开始爬上陆地。"},
    {"t": "第 5 层（最下面）", "age": "约 5 亿年前",
     "life": "三叶虫、腕足类等海洋生物",
     "note": "最下面的岩层最古老，那时的生物样子最陌生，全都生活在海里。"},
]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-evolution-intro 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 地层化石时间轴：点击地层 → 显示年代、代表生物与说明
   3) 自然选择模拟：改变环境 + 让种群繁殖 → 保护色个体比例变化
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. 选择题 ---------- */
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

  /* ---------- 2. 地层化石时间轴 ---------- */
  var fossilStage = document.getElementById('fossil-stage');
  if (fossilStage) {
    var fOut = document.getElementById('fossil-out');
    var cur = 0;
    function renderFossil() {
      var band = fossilStage.querySelector('[data-stratum="' + cur + '"]');
      var age = band.dataset.age, life = band.dataset.life, note = band.dataset.note;
      fOut.className = 'result';
      fOut.innerHTML = '<strong>' + band.dataset.name + '　' + age + '</strong><br>' +
        '代表性的化石：' + life + '<br>' + note +
        '<br><span style="color:var(--muted)">化石是指保存在岩层里的古生物遗体或遗迹。越往下的地层越古老。</span>';
      fossilStage.querySelectorAll('[data-stratum]').forEach(function (b) {
        b.style.outline = (b === band) ? '3px solid var(--brand)' : 'none';
        b.style.transform = (b === band) ? 'translateX(10px)' : 'none';
      });
    }
    fossilStage.querySelectorAll('[data-stratum]').forEach(function (b) {
      b.addEventListener('click', function () { cur = parseInt(b.dataset.stratum, 10); renderFossil(); });
    });
    renderFossil();
  }

  /* ---------- 3. 自然选择模拟 ---------- */
  var evoStage = document.getElementById('evo-stage');
  if (evoStage) {
    var TOTAL = 20;
    var pop = { green: 10, dry: 10 };
    var env = 'green';
    var gen = 0;
    var evoOut = document.getElementById('evo-out');
    var evoBar = document.getElementById('evo-bar');
    var evoGen = document.getElementById('evo-gen');
    var evoRatio = document.getElementById('evo-ratio');

    function camoName() { return env === 'green' ? '绿色个体' : '枯黄个体'; }
    function camoCount() { return env === 'green' ? pop.green : pop.dry; }

    function paint() {
      var html = '';
      for (var i = 0; i < pop.green; i++) {
        html += '<span style="display:inline-block;width:16px;height:16px;border-radius:50%;margin:2px;background:#5aa86a;border:1px solid rgba(0,0,0,.15)"></span>';
      }
      for (var j = 0; j < pop.dry; j++) {
        html += '<span style="display:inline-block;width:16px;height:16px;border-radius:50%;margin:2px;background:#d8c06a;border:1px solid rgba(0,0,0,.15)"></span>';
      }
      evoBar.innerHTML = html;
      evoGen.textContent = '第 ' + gen + ' 代';
      evoRatio.textContent = Math.round(100 * camoCount() / TOTAL) + '%';
    }

    function reproduce() {
      var w = (env === 'green') ? { green: 0.95, dry: 0.5 } : { green: 0.5, dry: 0.95 };
      var sg = pop.green * w.green, sd = pop.dry * w.dry;
      var tot = sg + sd;
      if (tot <= 0) { tot = 1; sg = 1; sd = 1; }
      var ng = Math.round(TOTAL * sg / tot);
      if (ng < 1) ng = 1;
      if (ng > TOTAL - 1) ng = TOTAL - 1;
      pop.green = ng;
      pop.dry = TOTAL - ng;
      gen++;
      paint();
      var camo = camoCount();
      if (gen === 1) {
        evoOut.className = 'result warn';
        evoOut.innerHTML = '<strong>第 1 代繁殖完成。</strong>环境是' + (env === 'green' ? '绿色的草地' : '枯黄的草地') + '，' +
          '被天敌发现得少的<strong>' + camoName() + '</strong>更容易活下来，留下的后代也更多。多点几次，看比例怎么变。';
      } else if (camo >= 19) {
        evoOut.className = 'result';
        evoOut.innerHTML = '<strong>' + camoName() + '已经占到 ' + camo + '/20。</strong>' +
          '草地颜色没有改变任何一只小虫的身体，是环境一代代筛掉了不合适的个体——这就是自然选择。点「重置」可以换一种环境再试一次。';
      } else {
        evoOut.className = 'result';
        evoOut.innerHTML = '<strong>第 ' + gen + ' 代：' + camoName() + ' ' + camo + '/20。</strong>' +
          '继续点「让种群繁殖」，看看这个比例会不会一代比一代高。';
      }
    }

    function reset() {
      pop = { green: 10, dry: 10 };
      gen = 0;
      paint();
      evoOut.className = 'result warn';
      evoOut.innerHTML = '现在已经重置：绿色个体和枯黄个体各 10 只，都从第 0 代开始。先选一个环境，再点「让种群繁殖」。';
    }

    document.querySelectorAll('[data-env]').forEach(function (b) {
      b.addEventListener('click', function () {
        env = b.dataset.env;
        document.querySelectorAll('[data-env]').forEach(function (x) { x.classList.toggle('selected', x === b); });
        evoStage.style.background = (env === 'green')
          ? 'linear-gradient(180deg,#f7fbff 0%, #dff3e2 60%, #c4e6c9 100%)'
          : 'linear-gradient(180deg,#fffdf5 0%, #f7eec6 60%, #e6d79a 100%)';
        reset();
      });
    });
    document.getElementById('evo-breed').addEventListener('click', reproduce);
    document.getElementById('evo-reset').addEventListener('click', reset);
    paint();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：长脖子到底是怎么来的？", TTS["pretest"], [
        {"q": "长颈鹿的脖子很长，下面哪种说法最接近科学的解释？",
         "options": [("祖先里本来就有脖子长和短的差异，环境把脖子长的留了下来", True),
                     ("长颈鹿天天伸脖子够树叶，脖子就慢慢变长了", False),
                     ("长颈鹿一出生脖子就都一样长，后来才变长的", False)],
         "explain": "进化的顺序是：先有变异，再由环境筛选，最后一代代积累。<strong>错因提醒：</strong>常见错误是把顺序弄反，误认为生物先努力改变身体，再把改变传给孩子。"},
        {"q": "同一个妈妈生的几只小狗，毛色和个头都不太一样。这种现象叫做：",
         "options": [("变异", True), ("进化", False), ("遗传病", False)],
         "explain": "同种生物后代之间的差异叫做变异，它是进化的原材料。<strong>错因提醒：</strong>不要把变异和进化搞混——变异是每一代都会出现的差异，进化是很多代积累之后的结果。"},
        {"q": "科学家凭什么说几亿年前的生物和现在不一样？",
         "options": [("因为不同地层里挖出的化石不一样，越深的地层化石越古老", True),
                     ("因为古书上写着", False),
                     ("因为现在的动物自己说的", False)],
         "explain": "化石保存在一层层岩层里，越往下的越古老。把化石按地层顺序排起来，就能看到生物确实变了。这个问题先记在心里，等下我们要挖一挖地层。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "后代之间总有差异，化石记下了生物的变", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">要弄明白长脖子，得先备好两样东西：<strong>变异</strong>这份原材料，和<strong>化石</strong>这本记录本。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>变异</strong></p>
            <p style="color:var(--muted)">同种生物的后代之间总有差异，而且这种差异能遗传下去。</p>
          </div>
          <div class="inner-card">
            <p><strong>化石</strong></p>
            <p style="color:var(--muted)">化石是指保存在岩层里的古生物遗体或遗迹，是进化最直接的证据。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="地层与化石时间轴示意图：越深的地层越古老，化石越陌生">
          <figcaption>岩层一层层叠起来，越靠下的越古老，里面的化石和今天的生物差别也越大</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">📚</span><div><strong>打个比方：</strong>地层就像一本从下往上写的日记，最下面那页是地球最早的记录，每一层都夹着当时的"生物照片"——化石。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一个妈妈生的孩子、同一棵树结的果子，都不会一模一样。差异是普遍存在的，不是偶然。"},
    {"lens": "解释它", "text": "为什么化石能证明进化？因为不同年代的岩层里埋着不同的生物，把它们按顺序排起来，就看到了生物样子的变化过程。"},
    {"lens": "比较它", "text": "变异是每一代都在发生的小差异；进化是很多很多代积累之后才能看出来的大变化。一个短，一个长，不要搞混。"},
])}
    ''', tag="概念一"))

    strata_html = "\n".join(
        f'''            <button class="sort-item" data-stratum="{i}" data-name="{s["t"]}" data-age="{s["age"]}"
                    data-life="{s["life"]}" data-note="{s["note"]}"
                    style="display:block;width:100%;text-align:left;margin:0 0 6px;padding:12px 14px;transition:all .2s">{s["t"]}
              <span style="color:var(--muted);font-size:13px">　{s["age"]}</span>
            </button>'''
        for i, s in enumerate(STRATA)
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手挖一挖：地层里的化石时间轴", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一点每一层岩石，看看那一层里埋着什么化石，再比一比它和今天的生物像不像。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">岩层剖面（上面最新，下面最古老）</div>
          <div id="fossil-stage" style="border-radius:14px;padding:12px;background:linear-gradient(180deg,#f7f2e6 0%,#efe3c8 55%,#d9c49a 100%);border:1px solid var(--line-subtle)">
{strata_html}
          </div>
          <p class="result warn" id="fossil-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⛏️</span><div><strong>挖完想一想：</strong>为什么恐龙化石只出现在中间几层，再往上就找不到了？这个"找不到"，本身就是化石在告诉我们的话。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "环境像筛子，把长脖子一代代筛了出来", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">备齐了变异和化石，就能回答开头的问题了：<strong>先有长短不同的变异，再被环境筛出活下来的那一批</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div>很久以前的长颈鹿祖先里，脖子有长一点、也有短一点的，这是变异。</div></div>
          <div class="step"><span class="n">2</span><div>低处的树叶被吃光了，只剩高处有叶子。脖子长一点的能吃到，活下来并生下后代。</div></div>
          <div class="step"><span class="n green">3</span><div>环境一代代筛下去，长脖子的个体越来越多，短脖子的越来越少——这就是自然选择。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="自然选择示意图：草地由绿变枯黄后，与环境颜色接近的个体比例逐代升高">
          <figcaption>草地变枯黄以后，与环境颜色接近的个体不容易被发现，一代代活下来的比例越来越高</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为"长颈鹿想变长就变长"，这是把顺序弄反了。正确顺序是：<strong>先有变异</strong>，再由环境筛选，最后<strong>一代代积累</strong>。一辈子练出来的变化，不会写进遗传信息里传给后代。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "自然选择模拟器：草地变黄了，谁还能活下来", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一种环境，然后连点几次「让种群繁殖」，观察与环境颜色接近的个体比例怎么变化。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="evo-stage" style="height:150px;background:linear-gradient(180deg,#f7fbff 0%, #dff3e2 60%, #c4e6c9 100%);padding:14px">
            <div id="evo-bar" style="line-height:0"></div>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice selected" data-env="green" style="text-align:center">🌿 绿色草地</button>
            <button class="choice" data-env="dry" style="text-align:center">🍂 枯黄草地</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">代数</span><span class="v" id="evo-gen">第 0 代</span></div>
            <div class="readout-cell"><span class="k">与环境颜色接近的个体</span><span class="v green" id="evo-ratio">50%</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="evo-breed" style="text-align:center;flex:1">让种群繁殖（+1 代）</button>
            <button class="choice" id="evo-reset" style="text-align:center">重置</button>
          </div>
          <p class="result warn" id="evo-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>对比一下：</strong>换成枯黄草地再繁殖十几代，比例会朝另一边倒。环境没有改变任何一只小虫的身体，它只是决定了谁能留下后代。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：脖子是「伸」长的，还是「筛」出来的", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>有人说，长颈鹿因为天天想吃高处的树叶，就拼命把脖子伸长，脖子变长以后又传给了宝宝。这个说法对吗？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清要判断什么：</strong>这句话在解释长脖子变长的原因。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找出问题所在：</strong>它说的是先努力、身体再改变，然后这个改变还能遗传给孩子。</div></div>
          <div class="step"><span class="n">3</span><div><strong>对照已学知识：</strong>一辈子练出来的变化不会写进遗传信息，不能直接传给后代。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>换成正确说法：</strong>祖先里本来就有脖子长短的变异，环境筛出了脖子长的那一批，让它们留下更多后代，一代代积累，脖子才变长。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">把"用进废退"当成进化。它错在两点：一是把顺序弄反了，误认为用得多的器官会自己变强；二是把练出来的变化当成了能遗传的变化。请记住那句口诀：<strong>变异是原料，环境是筛子，时间攒出来</strong>。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("同种生物的后代之间总有差异，这种差异叫变异", True),
                     ("只有长颈鹿会变异，别的生物不会", False),
                     ("变异就是进化", False)],
         "explain": "变异在一切生物身上都普遍存在，它是进化的原材料，不等于进化本身。<strong>错因提醒：</strong>把变异和进化搞混，是这一课最高频的常见错误。"},
        {"q": "长颈鹿的祖先里，脖子长的个体为什么能留下更多后代？",
         "options": [("低处树叶不够吃时，它们能吃到高处的叶子，更容易活下来", True),
                     ("因为它们更努力", False),
                     ("因为它们脖子长看起来更漂亮", False)],
         "explain": "能不能活下来，看的是这个特点在当下环境里有没有用。<strong>错因提醒：</strong>容易误认为「努力」能直接改变身体并遗传，其实努力不改变遗传信息，活下来的机会才决定谁留下后代。"},
        {"q": "越深的地层里，化石有什么特点？",
         "options": [("年代越古老，生物的样子和现在差别越大", True),
                     ("年代越新，因为上面的岩层后来才压上去", False),
                     ("和浅层的化石完全一样", False)],
         "explain": "岩层一层层沉积，越下面越早形成，所以越深处的化石越古老。<strong>错因提醒：</strong>常见错误是把地层上下顺序搞反，误认为最上面那层最古老。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给博物馆写一段解说词", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">博物馆的长颈鹿展板缺一段解说词。请你当一次解说员，把长脖子的来历讲给小朋友听。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>必须用上这四个词：</strong>变异 · 环境筛选 · 一代代积累 · 化石证据</p>
        </div>
        <div class="inner-card">
          <p><strong>第一步：先想好顺序</strong></p>
          <p style="color:var(--muted)">先说什么，再说什么，最后用什么证据收尾？把顺序写在下面。</p>
          <textarea id="syn-order" rows="2" placeholder="先有……再有……最后有……"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>第二步：写解说词（三到五句话）</strong></p>
          <textarea id="syn-answer" rows="5" placeholder="很久以前，长颈鹿的祖先里……"></textarea>
        </div>
        <div class="kid-note"><span class="emoji">🗣️</span><div>写完之后读给同桌听，请他挑出一句话，说说里面有没有把顺序说反。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "田里长期使用同一种杀虫剂后，抗药的小虫越来越多。用今天学的说法解释，最合理的是：",
         "options": [("小虫里本来就有抗药和不抗药的变异，杀虫剂把不抗药的筛掉了", True),
                     ("小虫为了活命，主动练出了抗药本领", False),
                     ("杀虫剂让小虫变强了", False)],
         "explain": "又是先有变异、再被筛选的老规律。<strong>错因提醒：</strong>不要误认为生物能「为了」生存而主动改变自己，变异是随机出现的，环境只负责筛选。"},
        {"q": "某片断崖上的地雀，喙又厚又大；附近平原上的同种地雀，喙又细又小。最合理的解释是：",
         "options": [("两地食物不同，环境筛出了适合吃当地食物的喙型", True),
                     ("断崖上的地雀更用力，所以喙变厚了", False),
                     ("两地的地雀不是同一种生物", False)],
         "explain": "同种生物在不同环境里被筛选出不同特点，时间久了就出现明显差别。"},
        {"q": "如果一片草原一直不发生变化，草丛里的小虫会怎么样？",
         "options": [("与环境颜色接近的个体依然更容易活下来，比例大体保持稳定", True),
                     ("所有小虫都会变成同一种颜色", False),
                     ("自然选择就完全停止，再也没有变异", False)],
         "explain": "只要环境不变，筛选的方向就基本不变，比例会稳定下来；变异仍然存在，只是没有朝一个方向积累的动力。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>原材料</strong>：同种生物的后代之间总有差异，这种差异叫做变异，还能遗传下去。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>筛选器</strong>：环境筛掉不太适合的个体，留下更合适的个体，一代代积累就是<strong>自然选择</strong>。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>证据本</strong>：化石是生物进化的直接证据，越深的地层里化石越古老。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头的问题：</strong>长脖子不是伸出来的，也不是想出来的。是祖先里先有了脖子长短的变异，环境把能吃到高处叶子的那一批留了下来，一代一代积累，才筛出了今天的长颈鹿。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用"变异、环境筛选、一代代积累"这三个词，说清长脖子是怎么来的。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出变异、自然选择、化石三个词的意思，每个词配一个例子。",
            "把地层化石的顺序排一排：越往下地层越（　），里面的化石越（　）。",
            "判断对错并说明理由：长颈鹿因为天天伸脖子，所以脖子变长了。",
        ],
        [
            "和家人一起玩课件里的自然选择模拟：分别在绿色草地和枯黄草地上繁殖 10 代，记下每一代保护色个体的比例，画成一张折线图。",
            "找一找身边「同种生物长得不一样」的例子，至少写三组，并说明差异是什么。",
        ],
        [
            "选一种你熟悉的生物（例如骆驼的驼峰、企鹅的翅膀、仙人掌的刺），画一张三步推理图：先有变异 → 环境怎么筛 → 结果是什么。",
            "如果要写一本《我家的地层日记》，你会把哪三件「化石」放进去？说说它们各自记录了哪一段时间。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-evolution-intro",
    "node_id": "sci-e-evolution-intro",
    "title": "生物的进化：长脖子是怎么来的？",
    "name_en": "Evolution: How did the long neck come about?",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "life-science",
    "domain_cn": "生命科学 · 生命的延续与进化",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "从长颈鹿长脖子这个经典疑问出发，用变异、环境筛选、一代代积累三步推理理解自然选择，并以地层化石时间轴与种群繁殖模拟，让进化成为学生能自己讲清楚的结论。",
    "tags": ["进化", "变异", "自然选择", "化石", "地层"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念8「生命的延续与进化」学习内容8.6 生物的遗传变异和环境因素的共同作用导致了生物的进化——5～6年级能简单描述生物的多样性和进化现象。",
    "hero_question": "长颈鹿的脖子那么长，是它自己努力伸长的，还是一代代被选出来的？",
    "hero_alt": "生物进化知识结构图：变异、环境筛选、化石证据三栏",
    "hero_caption": "变异是原材料 · 环境是筛子 · 一代代积累就是进化 · 化石是直接证据",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的探究都会围着它转。",
    "anchor_choices": [
        {"t": "化石到底是什么？它能告诉我们什么？", "d": "想知道考古学家怎么读出化石里的故事", "v": "化石到底是什么它能告诉我们什么"},
        {"t": "长脖子到底是怎么来的？", "d": "是伸长的，还是被选出来的", "v": "长脖子到底是怎么来的"},
        {"t": "为什么同一家的宝宝长得不一样？", "d": "差异是怎么出现的", "v": "为什么同一家的宝宝长得不一样"},
        {"t": "我也想当一次自然选择的实验员", "d": "亲手让一个种群繁殖十几代", "v": "我也想当一次自然选择的实验员"},
    ],
    "objectives": [
        "能说出同种生物的后代之间总有差异，知道这种差异叫做变异",
        "能举出化石作为生物进化直接证据的例子，知道越深的地层里化石越古老",
        "能用自然选择解释长颈鹿长脖子的来历，说清先有变异、再被筛选、一代代积累",
        "能区分用进废退和自然选择这两种说法有什么不同",
    ],
    "objectives_plain": [
        "能说出同种生物的后代之间总有差异，知道这种差异叫做变异",
        "能举出化石作为生物进化直接证据的例子，知道越深的地层里化石越古老",
        "能用自然选择解释长颈鹿长脖子的来历，说清先有变异、再被筛选、一代代积累",
        "能区分用进废退和自然选择这两种说法有什么不同",
    ],
    "standards": [
        {"content": "能简单描述生物的多样性和进化现象，知道化石是生物进化的证据",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念8 生命的延续与进化（5～6年级）"},
        {"content": "知道生物的遗传变异和环境因素的共同作用导致了生物的进化",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学习内容8.6（5～6年级）"},
    ],
    "prereqs": ["sci-e-heredity-intro"],
    "prereqs_name": "遗传与变异初识",
    "prereqs_meta": "sci-e-heredity-intro",
    "leads_to": ["sci-e-ecosystem"],
    "next_meta": "sci-e-ecosystem",
    "section_images": ["assets/sci-e-evolution-intro-fig1.webp", "assets/sci-e-evolution-intro-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "长脖子是伸出来的，还是被选出来的？带着这个矛盾开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己用三句话讲清长脖子的来历。",
        "objectives": "看清四件事：说出变异、用化石做证据、解释长脖子、区分两种说法。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "变异是每一代都在发生的差异，化石是把这些变化记下来的本子。",
        "lab-1": "从上往下点五层岩石，比一比每一层的化石像不像今天的生物。",
        "module-2": "先有变异，再有筛选，最后一代代积累——顺序不能反。",
        "lab-2": "换一种环境，连点十几次繁殖，看保护色个体的比例怎么倒过来。",
        "worked-example": "四步走：看清问题、找出毛病、对照知识、换成正确说法。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "写解说词时，先说变异，再说筛选，最后用化石收尾。",
        "posttest": "换了杀虫剂和地雀的新情境，看看你还能不能用上同一条规律。",
        "summary": "回到开头那只长颈鹿：它凭什么长出长脖子？用三句话讲清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「生命的延续与进化」在小学高段的空缺：知识树原有遗传与变异初识，但没有一课处理课标明确要求的进化现象。设计上把进化收敛成一句学生能带走的口诀——变异是原料、环境是筛子、时间攒出来；再用地层化石时间轴把「证据」变成可点可看的操作，用种群繁殖模拟把「筛选」变成可以重复十几代的实验，最后用长颈鹿、抗药小虫、地雀三个真实情境收束。",
    "plan_table": """| 1 | cover | 生物的进化：长脖子是怎么来的？ | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：长脖子到底是怎么来的？ | 起·前测（暴露直觉） |
| 5 | concept | 后代之间总有差异，化石记下了生物的变 | 承·概念一（变异与化石证据） |
| 6 | interactive | 动手挖一挖：地层里的化石时间轴 | 承·实验室一（地层化石时间轴） |
| 7 | concept | 环境像筛子，把长脖子一代代筛了出来 | 承·概念二（自然选择） |
| 8 | interactive | 自然选择模拟器：草地变黄了，谁还能活下来 | 承·实验室二（种群繁殖模拟） |
| 9 | concept | 例题示范：脖子是"伸"长的，还是"筛"出来的 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给博物馆写一段解说词 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：变异 / 环境筛选 / 化石证据 三栏标注\n- P5 地层化石时间轴示意图（已生成）：五层岩层与各年代代表生物\n- P7 自然选择示意图（已生成）：草地变枯黄前后保护色个体比例对比\n- 若需补充：长颈鹿取食实拍照片、真实化石照片、达尔文雀喙型对比图",
}
