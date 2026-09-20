# -*- coding: utf-8 -*-
"""小学信息科技 · 算法步骤与流程图（G3）—— 补齐知识树「算法与程序」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课不背术语，只做两件真能上手的事：
  ① 把"机器看得懂的顺序"一步一步点出来（点击排序 + 逐条即时反馈）
  ② 把每一步放进正确的图形里（椭圆 / 方框 / 菱形三分类）
最后收口到一条可带走的规则：先定头尾 → 写清中间 → 找出要判断的地方 → 用箭头连起来。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-algorithm-steps-fig1.webp'
F2 = './assets/it-e-algorithm-steps-fig2.webp'

TTS = {
    "hero": "先请你想象一件事。教室里有一个机器人，它看不见你，也听不见你心里在想什么。你想让它帮你把桌子擦干净，你该怎么告诉它？你只能一步一步说给它听：先做什么，再做什么，最后做什么。像这样一条一条、有先后顺序的办法，就是算法。今天这节课，我们既要学会把办法说清楚，还要学会把它画成一张流程图，让别人一眼就能看懂。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道自己心里想好的办法，机器人为什么听不懂，还是想知道一个办法要写成什么样才算清楚，又或者你想学会看懂流程图里那些方框和菱形，再或者你想弄明白，为什么步骤的顺序不能随便换。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出算法就是解决问题的、有先后顺序的清楚步骤。第二，能把一件小事按正确的先后顺序排出来，并说出为什么不能调换。第三，能认出流程图里的三种基本图形：椭圆表示开始和结束，方框表示要做的一件事，菱形表示需要判断的地方。第四，能给一个简单的任务排出算法，并把它画成一张带箭头的流程图。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先说什么叫算法。你早上到校，要先交作业，再擦桌子，最后坐下来读书，事情才能做完。把这件小事一条一条、按先后写出来，就是一条算法。要记住三件事：每一步都要说得清楚，别人照着做不会做错；每一步都有先后，不能随便调换；步数有限，做得到头。算法不是只有电脑才用，你写下来的一二三四，就是你的算法。",
    "lab-1": "光说还不够，我们动手排一次。下面有七张卡片，它们是让教室里那台电脑放出一段视频的全部步骤，可是顺序被打乱了。请你从第一步开始，一步一步点出来。点对了，卡片会进入下面的流程图里；点错了，会告诉你为什么这一步还早。",
    "module-2": "步骤一多，光用文字写就容易看乱。这时候要用流程图。流程图里只有几种基本图形：椭圆表示开始和结束，方框表示要做的一件事，菱形表示需要判断的地方，箭头表示谁接着谁。记住一句口诀：椭圆开口收尾，方框干活，菱形问话，箭头指路。判断的地方一定是一个问题，所以方框里写的是事情，菱形里写的是问句。",
    "lab-2": "现在请你当一次整理员。下面有六张卡片，你要把每一张放进正确的图形筐里：它是开始或结束，还是要做的一件事，还是一个需要判断的问题？放对了会告诉你理由，放错了也会给你一个提示，可以再试一次。",
    "worked-example": "我们一起把一件小事画成流程图。任务是这样的：小明早上从起床到出门，要完成一个出门前的算法。第一步，先定头尾，第一件事是起床，最后一件事是出门，它们都用椭圆。第二步，写清中间每一步，按发生的先后写下来，它们是方框。第三步，找出需要判断的地方，出门前有一件事要判断：今天下雨了吗？这是菱形。第四步，用箭头把它们连起来，从头读一遍，看看有没有哪一步没接上、有没有哪一步会卡住。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。花盆里的花要不要浇水，可以让一个自动浇花器来决定。下面有六张卡片被打乱了，请你按正确的顺序点出来，排出这条算法：先看一看土，再判断土是不是干的，干了就浇水，不干就先不浇，最后结束。排完之后，你会发现这条算法里有一个菱形。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现电梯、红灯和一段看不懂的流程图，看看你能不能把学到的规则用上去。",
    "summary": "这节课我们记住了三句话。第一句，算法就是解决问题的、清楚的步骤，有先后，能做完。第二句，流程图里椭圆开口收尾，方框干活，菱形问话，箭头指路。第三句，画流程图有四步：先定头尾，再写清中间的每一步，然后找出要判断的地方，最后用箭头连起来读一遍。回到开头那个问题，机器人听不懂你心里想的办法，但只要你把步骤排好、画成流程图，它就能照着做。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：用一句一句话写出整理书包的算法，至少四步，每步都要说得清楚。第二层能力应用，动手做：把你写的整理书包算法画成流程图，画出开始、结束和中间的方框，用箭头连起来。第三层迁移挑战，选做：给自动浇花设计一条算法，里面要有一个判断，画出带菱形的流程图，并说明是和不这两条路分别走到哪里去。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 什么叫做算法", "lab-1": "动手一 步骤排一排", "module-2": "概念二 流程图的三种图形",
    "lab-2": "动手二 图形符号配对", "worked-example": "例题讲解 画一张流程图", "conceptest-1": "概念测试",
    "synthesis": "综合任务 自动浇花的算法", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 动手一：被打乱的七张卡片（含开始/结束）
FLOW_NODES = [
    ("start", "开始", "term"),
    ("power", "按下开机键", "step"),
    ("wait", "等屏幕亮起来", "step"),
    ("find", "找到要播放的视频", "step"),
    ("open", "打开这个视频", "step"),
    ("play", "按下播放键", "step"),
    ("end", "结束", "term"),
]

# 动手二：六张卡片放进三个图形筐
SYMBOL_CARDS = [
    ("start", "开始", "term", "开始和结束都用椭圆——它是这张图的头和尾，一个进、一个出。"),
    ("finish", "结束", "term", "结束也表示成椭圆。看到椭圆，就知道这段流程走到头了。"),
    ("kettle", "拿起水壶去接水", "step", "这是一件要动手去做的事，用方框（矩形）表示。"),
    ("pour", "把水浇在花盆里", "step", "这也是一件要做的事，同样是方框。方框里写的都是「做什么」。"),
    ("dry", "土壤是不是干的？", "decision", "句尾是个问号，答案只有「是」或「不是」两条路——所以它用菱形。"),
    ("sun", "今天太阳晒得厉害吗？", "decision", "这也是一个需要判断的问题，答案是或不是，所以也用菱形。"),
]

BINS = [
    ("term", "🔵 起点和终点（椭圆）"),
    ("step", "🟦 要做的一件事（方框）"),
    ("decision", "🔶 需要判断（菱形）"),
]

# 综合任务：自动浇花算法
WATER_STEPS = [
    ("w1", "开始", "term"),
    ("w2", "看一看花盆里的土", "step"),
    ("w3", "土壤是干的吗？", "decision"),
    ("w4", "是 → 打开水泵浇水", "step"),
    ("w5", "否 → 今天先不浇水", "step"),
    ("w6", "结束", "term"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-algorithm-steps 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：七张卡片按顺序点出来 → 每次都渲染成一张流程图
   3) 动手二：六张卡片放进 椭圆 / 方框 / 菱形 三个筐
   4) 综合任务：自动浇花算法（含一个菱形）
   ============================================================ */
(function () {
  'use strict';

  /* 流程图节点样式（注入，避免写死颜色，统一走主题变量） */
  var st = document.createElement('style');
  st.textContent =
    '.flow-track{display:flex;flex-direction:column;align-items:center;gap:0;padding:10px 0;}' +
    '.flow-node{display:inline-flex;align-items:center;justify-content:center;min-width:190px;max-width:100%;' +
    'padding:10px 18px;font-size:14px;font-weight:700;text-align:center;background:var(--card);' +
    'border:2px solid var(--brand);color:var(--text);}' +
    '.flow-node[data-shape="term"]{border-radius:999px;background:var(--brand-soft);}' +
    '.flow-node[data-shape="step"]{border-radius:8px;}' +
    '.flow-node[data-shape="decision"]{border-radius:8px;border-style:dashed;border-color:var(--warm);' +
    'background:var(--warm-soft);transform:none;}' +
    '.flow-arrow{color:var(--muted);font-size:15px;line-height:1.1;margin:2px 0;}' +
    '.flow-empty{color:var(--muted);font-size:14px;}';
  document.head.appendChild(st);

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

  /* ---------- 2. 动手一：按顺序点出来 ---------- */
  var bank1 = document.getElementById('flow-bank');
  if (bank1) {
    var RIGHT = ['start', 'power', 'wait', 'find', 'open', 'play', 'end'];
    var TIPS = {
      start: '开始是这段算法的第一个框，先把它放上去。',
      power: '开机是第一步——不按开机键，后面的事情都不会发生。',
      wait: '开机以后要等屏幕亮起来，这两步是紧挨着的。',
      find: '电脑准备好了，才去找要播放的那个视频。',
      open: '找到视频以后，才谈得上把它打开。',
      play: '按下播放键是最后一步，视频这才开始放。',
      end: '最后用「结束」把这段算法收住，它表示这件事做完了。'
    };
    var track1 = document.getElementById('flow-track');
    var out1 = document.getElementById('flow-out');
    var placed1 = [];

    function render1() {
      track1.innerHTML = '';
      if (!placed1.length) {
        var e = document.createElement('p');
        e.className = 'flow-empty';
        e.textContent = '还没有排出第一步。点上面任意一张卡片，试着把第一步放进来。';
        track1.appendChild(e);
      }
      placed1.forEach(function (k, i) {
        if (i > 0) {
          var a = document.createElement('div');
          a.className = 'flow-arrow';
          a.textContent = '↓';
          track1.appendChild(a);
        }
        var btn = bank1.querySelector('[data-step="' + k + '"]');
        var n = document.createElement('div');
        n.className = 'flow-node';
        n.dataset.shape = btn ? btn.dataset.shape : 'step';
        n.textContent = btn ? btn.textContent.trim() : k;
        track1.appendChild(n);
      });
      bank1.querySelectorAll('[data-step]').forEach(function (b) {
        var done = placed1.indexOf(b.dataset.step) !== -1;
        b.classList.toggle('done', done);
        b.disabled = done;
      });
      document.getElementById('flow-count').textContent= placed1.length + ' / 7 步';
    }

    bank1.querySelectorAll('[data-step]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.step;
        if (placed1.indexOf(k) !== -1) return;
        if (RIGHT[placed1.length] === k) {
          placed1.push(k);
          out1.className = 'result';
          if (placed1.length === 7) {
            out1.innerHTML = '<strong>七步全排对了！</strong>你刚刚做的事，就是给电脑写了一条算法。' +
              '注意看最上面和最下面那两个椭圆——它们把这段算法包了起来，一个开头，一个收尾。';
          } else {
            out1.innerHTML = '<strong>第 ' + placed1.length + ' 步放对了。</strong>' + TIPS[k];
          }
        } else {
          out1.className = 'result error';
          out1.innerHTML = '<strong>这一步现在还太早。</strong>' + TIPS[k] +
            '<br><span style="color:var(--muted)">常见错误：把中间某两步的顺序调换了，心里想的是"反正都做了"。' +
            '可电脑不会自己判断，顺序一乱，它就走不下去了。</span>';
        }
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 动手二：图形符号配对 ---------- */
  var bank2 = document.getElementById('symbol-bank');
  if (bank2) {
    var picked2 = null, done2 = 0, wrong2 = 0;
    var out2 = document.getElementById('symbol-out');

    bank2.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        bank2.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked2 = card;
        out2.className = 'result warn';
        out2.textContent = '已选中「' + card.textContent.trim() + '」，现在点下面你认为对的那个筐。';
      });
    });

    document.querySelectorAll('[data-symbol-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked2) {
          out2.className = 'result warn';
          out2.textContent = '先点上面的一张卡片，再点筐。';
          return;
        }
        var want = picked2.dataset.kind, got = bin.dataset.symbolBin;
        picked2.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked2.textContent.trim() + ' ✓';
          bin.querySelector('.bin-body').appendChild(tag);
          picked2.classList.add('done');
          picked2.disabled = true;
          done2++;
          out2.className = 'result';
          out2.innerHTML = '<strong>放对了！</strong>' + picked2.dataset.why;
          picked2 = null;
          if (done2 === 6) {
            out2.className = 'result';
            out2.innerHTML = '<strong>六张卡片全部归位。</strong>诀窍在这里：<strong>看句尾</strong>——' +
              '句尾是问号、答案只有"是"或"不是"的，就是菱形；动手去做的，就是方框；表示开头和结尾的，就是椭圆。';
          }
        } else {
          wrong2++;
          out2.className = 'result error';
          out2.innerHTML = '<strong>再想一下：「' + picked2.textContent.trim() + '」</strong>' +
            '先问自己两句话：这是一件"要做的事"，还是一个"要判断的问题"？<br>' +
            '<span style="color:var(--muted)">常见错误：把需要判断的问题也画成方框。这样一画，是和不这两条路就没了，' +
            '流程图也只能一直往前走。</span>';
          picked2.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
      });
    });
  }

  /* ---------- 4. 综合任务：自动浇花算法 ---------- */
  var bank3 = document.getElementById('water-bank');
  if (bank3) {
    var RIGHT3 = ['w1', 'w2', 'w3', 'w4', 'w5', 'w6'];
    var TIPS3 = {
      w1: '算法要从「开始」这个椭圆进入。',
      w2: '要先看一看土，才知道后面该判断什么。',
      w3: '看完土，接着判断：土壤是干的吗？这一步是菱形。',
      w4: '判断的结果是"是"，干的就打开水泵浇水。',
      w5: '另一个结果是"否"，不干就今天先不浇。',
      w6: '最后走回「结束」，这一段算法就完成了。'
    };
    var track3 = document.getElementById('water-track');
    var out3 = document.getElementById('water-out');
    var placed3 = [];

    function render3() {
      track3.innerHTML = '';
      if (!placed3.length) {
        var e = document.createElement('p');
        e.className = 'flow-empty';
        e.textContent = '还没有排出第一步。';
        track3.appendChild(e);
      }
      placed3.forEach(function (k, i) {
        if (i > 0) {
          var a = document.createElement('div');
          a.className = 'flow-arrow';
          a.textContent = '↓';
          track3.appendChild(a);
        }
        var btn = bank3.querySelector('[data-wstep="' + k + '"]');
        var n = document.createElement('div');
        n.className = 'flow-node';
        n.dataset.shape = btn ? btn.dataset.shape : 'step';
        n.textContent = btn ? btn.textContent.trim() : k;
        track3.appendChild(n);
      });
      bank3.querySelectorAll('[data-wstep]').forEach(function (b) {
        var done = placed3.indexOf(b.dataset.wstep) !== -1;
        b.classList.toggle('done', done);
        b.disabled = done;
      });
    }

    bank3.querySelectorAll('[data-wstep]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.wstep;
        if (placed3.indexOf(k) !== -1) return;
        if (RIGHT3[placed3.length] === k) {
          placed3.push(k);
          out3.className = 'result';
          if (placed3.length === 6) {
            out3.className = 'result';
            out3.innerHTML = '<strong>自动浇花的算法排好了！</strong>这段算法里有一个菱形，' +
              '从菱形出发有两条路：「是」去浇水，「否」今天先不浇，两条路最后都走到「结束」。' +
              '这就叫带判断的算法——电脑靠它自己做决定。';
          } else {
            out3.innerHTML = '<strong>第 ' + placed3.length + ' 步放对了。</strong>' + TIPS3[k];
          }
        } else {
          out3.className = 'result error';
          out3.innerHTML = '<strong>先别急。</strong>' + TIPS3[k] +
            '<br><span style="color:var(--muted)">常见错误：把「打开水泵浇水」放到「土壤是干的吗？」前面。' +
            '还没判断，它怎么知道该不该浇呢？</span>';
        }
        render3();
      });
    });
    render3();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你的办法，别人能照着做吗？", TTS["pretest"], [
        {"q": "下面哪一句可以直接当作算法里的一步？",
         "options": [("把水倒进杯子里", True),
                     ("把水弄好就行了", False),
                     ("想一想水该怎么弄", False)],
         "explain": "「把水倒进杯子里」说清了做什么、在哪里做，别人照着就不会做错。"
                    "<strong>错因提醒：</strong>常见错误是把步骤写得太笼统，像「弄好」「处理一下」这种说法听着省事，"
                    "实际上没人知道该做什么——这也正是机器人听不懂你的原因。"},
        {"q": "擦桌子的算法里，「用干布把水擦干」和「用湿布擦一遍」，哪一步应该先做？",
         "options": [("先用湿布擦，再用干布擦干", True),
                     ("先用干布擦，再用湿布擦", False),
                     ("两步谁先都行，反正都擦了", False)],
         "explain": "顺序变了，结果就变了：先擦干再擦湿，桌子最后还是湿的。"
                    "<strong>错因提醒：</strong>不少同学误认为「每一步都做了就没问题」。"
                    "算法里真正要紧的恰恰是谁先谁后。"},
        {"q": "流程图里，表示「需要判断的地方」的图形是：",
         "options": [("菱形", True), ("矩形方框", False), ("椭圆", False)],
         "explain": "菱形里写的都是一个问题，答案只有「是」或「不是」两条路。"
                    "<strong>错因提醒：</strong>容易把判断画成方框——那样两条岔路就画不出来了，"
                    "整张图只剩一条直路。椭圆是起点和终点，方框才是要做的事。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "算法：把解决问题的步骤，一步一步说清楚", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们平时做事，凭感觉就能做完（And）；但这件事如果交给一个看不见你、也猜不到你想法的机器去做，它只会一个口令一个动作，感觉帮不上忙（But）；所以我们要学会把办法拆成清楚的步骤，写下来、画出来，让机器和别人都能照着做（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">为了解决一个问题，把要做的事按<strong>先后顺序</strong>一条一条写清楚，这些步骤合起来就叫<strong>算法</strong>。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>① 说得清楚</strong></p><p style="color:var(--muted)">每一步别人照着做，都不会做错。</p></div>
          <div class="inner-card"><p><strong>② 有先有后</strong></p><p style="color:var(--muted)">顺序不能随便换，换了结果就不一样。</p></div>
          <div class="inner-card"><p><strong>③ 做得完</strong></p><p style="color:var(--muted)">步数有限，一步一步走得到头。</p></div>
        </div>
        <div class="inner-card">
          <p><strong>举个例子：接半杯温水</strong></p>
          <p style="color:var(--muted)">① 拿出一个杯子 → ② 接半杯冷水 → ③ 兑一点热水 → ④ 用手背试一下温度 → ⑤ 太烫就等一会儿。五步写完，这件事谁都做得出来了。</p>
        </div>
        <div class="kid-note"><span class="emoji">🤖</span><div><strong>小提示：</strong>算法不是只有电脑才用。你写在本子上的「先……然后……最后……」，只要清楚、有先后、能做完，就是一条算法。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一件小事，你可以直接做完，也可以一格一格地写下来——写下来的那串格子，就是算法。"},
    {"lens": "解释它", "text": "为什么机器一定要先把步骤写清楚？因为它不会「看情况」，也不会「差不多就行」，它只会严格按顺序走。"},
    {"lens": "比较它", "text": "同一个问题，往往不止一条算法。擦桌子的算法，是先擦桌角还是先擦中间，做得到就行——但每一条都必须自己说得清楚。"},
])}
    ''', tag="概念一"))

    node_btns = "\n".join(
        f'            <button class="sort-item" data-step="{k}" data-shape="{shape}">{t}</button>'
        for k, t, shape in FLOW_NODES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：把被打乱的步骤，按顺序点回来", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">任务：让教室里的电脑放出一段视频。下面七张卡片的顺序被打乱了，请从第一步开始，一步一步点出来。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 待排的步骤卡片（点它，放进去）</div>
          <div class="sort-bank" id="flow-bank">
{node_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">已排出的步骤</span><span class="v" id="flow-count">0 / 7 步</span></div>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 你排出来的流程图</div>
          <div class="canvas-wrap"><div class="flow-track" id="flow-track"></div></div>
          <p class="result warn" id="flow-out" style="margin-top:12px">请点出你认为的第一步。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>排完以后看一眼：</strong>最上面和最下面那两个椭圆，一个写着「开始」，一个写着「结束」。它们把整段算法包在中间，中间那五个方框，才是真正要动手做的事。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "流程图：椭圆收尾，方框干活，菱形问话", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">步骤一多，光用文字写就容易看乱。这时候把每一步放进图形里，再用箭头连起来，就是<strong>流程图</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n green">椭</span><div><strong>椭圆 · 开始 / 结束</strong>：一张流程图的头和尾，一个进、一个出。</div></div>
          <div class="step"><span class="n">框</span><div><strong>方框 · 做一件事</strong>：里面写的都是"要动手做什么"。</div></div>
          <div class="step"><span class="n">菱</span><div><strong>菱形 · 需要判断</strong>：里面写的是一个问句，答案是或不，走出两条路。</div></div>
          <div class="step"><span class="n">↓</span><div><strong>箭头 · 谁接着谁</strong>：箭头指到哪儿，下一步就去哪儿。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="流程图三种基本图形示意图：椭圆表示开始和结束、方框表示要做的一件事、菱形表示需要判断的问题，用箭头连接">
          <figcaption>示意图：流程图的三种基本图形与箭头。椭圆开口收尾，方框干活，菱形问话，箭头指路</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">把需要判断的<strong>问题</strong>也画成方框。这样一画，「是」和「不是」两条路就没了，整张图只能一直往前走——判断也就丢掉了。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>椭圆开口收尾，方框干活，菱形问话，箭头指路。</div></div>
    ''', tag="概念二"))

    card_btns = "\n".join(
        f'          <button class="sort-item" data-kind="{kind}" data-why="{why}">{t}</button>'
        for _k, t, kind, why in SYMBOL_CARDS
    )
    bin_html = "\n".join(f'''            <div class="sort-bin" data-symbol-bin="{k}">
              <h4>{label}</h4>
              <div class="bin-body"></div>
            </div>''' for k, label in BINS)
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：每一张卡片，该用哪种图形？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张卡片，再点你认为对的那个筐。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待归位的六张卡片</div>
          <div class="sort-bank" id="symbol-bank">
{card_btns}
          </div>
          <div class="sort-bins" style="grid-template-columns:repeat(3,1fr)">
{bin_html}
          </div>
          <p class="result warn" id="symbol-out" style="margin-top:12px">点一张卡片开始归位。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💡</span><div><strong>一个最快的判断办法：</strong>先看句尾。句尾是问号、答案只有「是」或「不是」的，一定是菱形；动手去做的，是方框；表示开头和结尾的，是椭圆。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：把小明的出门前算法画成流程图", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>请把小明的算法画成一张流程图——起床、洗脸刷牙、穿好衣服、吃早饭、看看外面下雨了没有、下雨就带伞、出门。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="左边的文字步骤与右边的流程图画法对照示意图，步骤被放进椭圆、方框和菱形里并用箭头连接">
          <figcaption>示意图：左边是文字写下来的步骤，右边一步步放进图形里——头尾用椭圆，动作放进方框，要判断的地方放进菱形</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先定头尾：</strong>第一件事是起床，最后一件事是出门，它们都用<strong>椭圆</strong>。椭圆一上一下，流程就有了边界。</div></div>
          <div class="step"><span class="n">2</span><div><strong>写清中间：</strong>洗脸刷牙、穿衣服、吃早饭，按发生的先后写进<strong>方框</strong>里。</div></div>
          <div class="step"><span class="n">3</span><div><strong>找出要判断的地方：</strong>「外面下雨了吗？」这是<strong>菱形</strong>，从它出发有两条路——下雨就带伞，不下雨就直接出门。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>用箭头连起来，再从头读一遍：</strong>每一步都接得上吗？有没有哪一步会卡住？读得通，这张流程图才算画完。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学只画了「起床 → 出门」两个椭圆，说「中间的事我记着就行」。可是流程图是画给别人和机器看的，中间那几步<strong>必须一个不落地写进方框</strong>，不然别人照着做还是做不成。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "下面哪一句话，可以作为算法里的一个步骤？",
         "options": [("把书包里的作业本拿出来，放到讲台上", True),
                     ("把作业的事处理一下", False),
                     ("想想作业该交给谁", False)],
         "explain": "说清了做什么、在哪里做、对什么做，别人照着就能完成。"
                    "<strong>错因提醒：</strong>「处理一下」「弄一弄」听着像步骤，其实谁也不知道该做什么，"
                    "这是写算法时最常见的错误。"},
        {"q": "在流程图里看到一个菱形，说明这段算法：",
         "options": [("有一个需要判断的地方，会走出两条路", True),
                     ("一定出错了，菱形不该出现", False),
                     ("表示这里要动手做一件事", False)],
         "explain": "菱形专门留给判断：答案是或不是，两条路各自往下走。"
                    "<strong>错因提醒：</strong>容易把菱形和方框搞混。记住：方框里是「做什么」，菱形里是「问什么」。"},
        {"q": "下面这段算法少了哪一步：「开始 → 拿起水壶 → 把水浇进花盆 → 结束」",
         "options": [("少了判断土壤干不干这一步", True),
                     ("少了结束这一步", False),
                     ("一步也没少，可以照着做", False)],
         "explain": "浇水之前要先判断土壤干不干，不然可能把花浇坏。少了判断，这条算法就不完整。"
                    "<strong>错因提醒：</strong>很多同学误认为「只要动作都写了就算完整」，其实判断也是算法的一部分。"}
    ], tag="概念测试"))

    water_btns = "\n".join(
        f'            <button class="sort-item" data-wstep="{k}" data-shape="{shape}">{t}</button>'
        for k, t, shape in WATER_STEPS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给自动浇花器排一条算法", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">自动浇花器要自己决定浇不浇水。下面六张卡片被打乱了，请按正确的顺序点出来。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 待排的卡片</div>
          <div class="sort-bank" id="water-bank">
{water_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 你排出来的算法</div>
          <div class="canvas-wrap"><div class="flow-track" id="water-track"></div></div>
          <p class="result warn" id="water-out" style="margin-top:12px">请点出你认为的第一步。</p>
        </div>
        <div class="inner-card">
          <p><strong>排完之后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">这条算法里的菱形在问什么？从它出发的两条路，最后都走到哪里去了？如果把它画成流程图，哪几个框是椭圆，哪几个是方框？</p>
          <textarea id="syn-answer" rows="3" placeholder="菱形里问的是……两条路分别走到……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，规则还在不在", TTS["posttest"], [
        {"q": "电梯的算法是「先关门，再上升」。如果把这两步调换，会怎么样？",
         "options": [("门还开着就上升，很危险，说明顺序不能换", True),
                     ("没关系，反正两件事都做了", False),
                     ("电梯会自己改成正确的顺序", False)],
         "explain": "顺序变了，结果就变了。算法的先后是有意义的，不能随意调换。"
                    "<strong>错因提醒：</strong>常见错误是认为「每一步都做了就行」——顺序本身也是算法的一部分。"},
        {"q": "让机器人「看到红灯就停下，绿灯就前进」，画流程图时，「现在是红灯吗？」这个框应该画成：",
         "options": [("菱形，因为这是一个需要判断的问题", True),
                     ("方框，因为要停下或者前进", False),
                     ("椭圆，因为这是开头", False)],
         "explain": "它的答案只有「是」或「不是」，走出停和走两条路，所以是菱形。"
                    "<strong>错因提醒：</strong>不要误认为「跟动作有关的就画方框」——判断句该住的是菱形。"},
        {"q": "一段算法这样写：① 打开水龙头 ② 拿起杯子 ③ 接水。它的问题在哪里？",
         "options": [("顺序错了，应该先拿起杯子再打开水龙头", True),
                     ("步骤太少，至少要写十步", False),
                     ("没问题，这样做也能接到水", False)],
         "explain": "空着手去开水龙头，水就白流了。步骤得按事情真正发生的先后写。"
                    "<strong>错因提醒：</strong>这一步最容易忽略，因为它「好像也能做」——但算法要求的是能稳稳当当做成。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把算法讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>什么是算法：</strong>解决问题的、清楚的步骤——说得明白、有先后、能做完。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>怎么看流程图：</strong>椭圆开口收尾，方框干活，菱形问话，箭头指路。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>怎么画流程图：</strong>先定头尾 → 写清中间每一步 → 找出要判断的地方 → 用箭头连起来，再从头读一遍。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个机器人：</strong>它听不懂你心里想的办法。可一旦你把步骤排好、画成流程图，它就照着一步一步走——这也正是电脑干活的方式。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「算法、顺序、判断」这三个词，说清楚整理书包这件事该怎么做、哪一步需要判断。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出来</strong>——在你的本子上画四个方框，用箭头连起来，写出你明天早上出门的算法。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "用一句一句话写出「整理书包」的算法，至少四步，每一步都要说得清楚。",
            "说出流程图里三种图形各表示什么：椭圆、方框、菱形。",
        ],
        [
            "把你写的「整理书包」算法画成一张流程图：画出开始和结束的椭圆，中间的动作放进方框，用箭头连起来。",
            "找一个家里的电器，看看它的使用说明是按照什么顺序写的，把它的步骤抄下来。",
        ],
        [
            "给「自动浇花」设计一条算法，里面要有一个判断。画出带菱形的流程图，并说清楚「是」和「否」两条路分别走到哪里去。",
            "想一想：如果一条算法里有三个需要判断的地方，流程图会长成什么样子？画草图试试看。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-algorithm-steps",
    "node_id": "it-e-algorithm-steps",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "算法步骤与流程图",
    "name_en": "Algorithm Steps and Flowcharts",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "algorithm-programming",
    "domain_cn": "算法与程序",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学三年级：知道算法就是解决问题的清楚步骤，能有先后地说出并排出简单算法；认识流程图里的椭圆、方框、菱形和箭头，能把一件小事画成带箭头的流程图，并知道判断的地方要走两条路。",
    "tags": ["算法", "步骤顺序", "流程图", "判断", "动手操作"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「算法与程序」——用自然语言和流程图描述解决问题的步骤。",
    "hero_question": "机器人看不见你，也猜不到你的想法——你该怎么把办法告诉它？",
    "hero_alt": "算法步骤与流程图知识结构图：算法是什么、流程图的三种图形、画流程图四步",
    "hero_caption": "算法：说得清楚、有先后、能做完 · 流程图：椭圆收尾，方框干活，菱形问话 · 画法：定头尾 → 写步骤 → 找判断 → 连箭头",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "我心里想好的办法，机器人为什么听不懂？", "d": "它是怎么「读」一个办法的", "v": "我心里想好的办法机器人为什么听不懂"},
        {"t": "一个办法要写成什么样才算清楚？", "d": "怎么判断自己写的步骤合格了", "v": "一个办法要写成什么样才算清楚"},
        {"t": "流程图里的方框和菱形都是什么意思？", "d": "想学会看懂别人画的流程图", "v": "流程图里的方框和菱形都是什么意思"},
        {"t": "为什么步骤的顺序不能随便换？", "d": "换一下真的会出问题吗", "v": "为什么步骤的顺序不能随便换"},
    ],
    "objectives": [
        "能说出算法就是解决问题的、有先后顺序的清楚步骤",
        "能把一件小事按正确的先后顺序排出来，并说出为什么不能调换",
        "能认出流程图里的椭圆、方框和菱形各表示什么",
        "能给一个简单任务排出算法并画成带箭头的流程图，知道判断的地方有两条路",
    ],
    "objectives_plain": [
        "能说出算法就是解决问题的、有先后顺序的清楚步骤",
        "能把一件小事按正确的先后顺序排出来，并说出为什么不能调换",
        "能认出流程图里的椭圆、方框和菱形各表示什么",
        "能给一个简单任务排出算法并画成带箭头的流程图，知道判断的地方有两条路",
    ],
    "standards": [
        {"content": "用自然语言和流程图描述解决问题的步骤",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 算法与程序"},
        {"content": "在真实任务中体验「把办法拆成步骤」的过程，初步形成把问题说清楚、按顺序做事的意识",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 计算思维"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是信息科技小学段「算法与程序」的起始课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["it-e-block-programming"],
    "next_meta": "it-e-block-programming",
    "section_images": ["assets/it-e-algorithm-steps-fig1.webp", "assets/it-e-algorithm-steps-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "机器人听不懂你的心思，只认一步一步的指令。把办法写清楚，它才动得起来。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能排出一条清楚的算法，还能把它画成流程图。",
        "objectives": "看清四件事：算法是什么、顺序为什么不能换、三种图形各是什么、怎么画一张流程图。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "算法不只属于电脑：说得清楚、有先后、能做完，你写下的一二三四就是算法。",
        "lab-1": "从第一步开始点，点对了卡片会走进下面的流程图里，点错了会告诉你为什么还早。",
        "module-2": "椭圆开口收尾，方框干活，菱形问话，箭头指路——四个图形各自只管一件事。",
        "lab-2": "最快的判断办法是看句尾：问号、只有是或不是，就一定是菱形。",
        "worked-example": "四步走：先定头尾、写清中间、找出要判断的地方、用箭头连起来再读一遍。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "这条算法里有一个菱形。想想从它出发的两条路，最后都走到哪里去了。",
        "posttest": "电梯、红绿灯和一段写错顺序的算法，看看你能不能把规则用上去。",
        "summary": "三句话：算法是什么、怎么看流程图、怎么画流程图。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「算法与程序」的起始一课。三年级学生的难点不在记术语，而在两件事：一是心里想好的办法说不清楚，二是把判断当成普通的一步。所以全课只做两件真能上手的事——把让电脑放视频的七个步骤按顺序一步步点出来（每次点击都会即时反馈为什么早/为什么对，排完就长成一张流程图），再把六张卡片分进椭圆、方框、菱形三个筐里。概念页把判断收成一句可带走的规则与口诀（椭圆开口收尾，方框干活，菱形问话，箭头指路），例题页用「出门前」这件小事示范画流程图的四步，综合任务落到带菱形的自动浇花算法，让「判断会走出两条路」这件事被亲手排过一遍。",
    "plan_table": """| 1 | cover | 算法步骤与流程图 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你的办法，别人能照着做吗？ | 起·前测（暴露直觉） |
| 5 | concept | 算法：把解决问题的步骤，一步一步说清楚 | 承·概念一（含三个要求） |
| 6 | interactive | 动手一：把被打乱的步骤，按顺序点回来 | 承·排序模拟（逐步即时反馈，排出即流程图） |
| 7 | concept | 流程图：椭圆收尾，方框干活，菱形问话 | 承·概念二（三种图形 + 口诀 + 反例） |
| 8 | interactive | 动手二：每一张卡片，该用哪种图形？ | 承·图形分类（椭圆/方框/菱形三分类） |
| 9 | concept | 例题示范：把小明的出门前算法画成流程图 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给自动浇花器排一条算法 | 合·迁移应用（含菱形的算法） |
| 12 | quiz | 后测：换几个情境，规则还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把算法讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：算法是什么 / 流程图三种图形 / 画流程图四步 三栏\n- P7 流程图基本图形示意图（已生成）：椭圆、方框、菱形与箭头\n- P9 文字步骤与流程图画法对照图（已生成）\n- 三张图均为教学示意图，不涉及任何真实软件界面、截图或商标\n- 若需补充：学生手绘流程图的实拍照片（需获得授权后使用）",
}
