# -*- coding: utf-8 -*-
"""小学信息科技 · 输入-计算-输出模型（G5）—— 补齐知识树「过程与控制」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课不背术语，只做三件真能上手的事：
  ① 三格数据流动器：选输入 + 选规则 → 点执行 → 输入/计算/输出 三格依次亮起
  ② 怪结果实验：把不合适的输入喂给机器，看它算出什么样的怪结果（含隐私提醒）
  ③ 拆解任务：把生活里的一个"自动装置"拆成 输入 / 计算 / 输出 三格
最后收口到一句可带走的口诀与一条责任提醒：
  输入是眼睛，计算是脑袋，输出是手脚；
  机器不会怀疑数据，数据错了它照样算——所以最后把关的还得是人。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-input-output-fig1.webp'
F2 = './assets/it-e-input-output-fig2.webp'

TTS = {
    "hero": "先看一件小事。天慢慢黑了，教室里的灯自己亮了起来，没有人去按开关。灯是怎么知道天黑的？它看不见，也不会猜，它只是把光线变成了一个能比较的数值，送进机器里，机器再按一条想好的规则算一算，最后决定把灯打开。把这件事说清楚，就只剩三格：输入、计算、输出。今天这节课，我们就来把这三格弄明白，还会亲手喂给机器一些不合适的输入，看看它会算出什么样的怪结果。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道机器到底从哪儿拿到数据，还是想知道它凭什么能自己做决定，又或者你想弄明白为什么有时候它算出来的结果特别奇怪，再或者你想亲手拆开一个自动装置，看看它的三格分别是什么。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出输入、计算、输出分别是什么意思，知道它们是有先后的三步。第二，能在三格模型里指出一个自动装置的数据从哪里来、按什么规则算、最后做了什么。第三，能说出输入的数值或类型不对时，机器算出来的结果就会很奇怪。第四，能说出一条使用数据的规矩，比如别人的个人信息不能随便拿来当输入。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先说三格模型。机器做事，其实只有三步。第一步是输入，就是它先拿到要处理的数据，比如光线有多亮、温度是多少、按钮有没有被按下。第二步是计算，就是它按一条想好的规则，把这些数据比一比、算一算。第三步是输出，就是它照着算出来的结果动手做事，比如把灯打开、把门打开、发出报警声。要特别记住一件事：这三步是有先后的。没有输入，就没有可以算的东西；没有算，就不知道该输出什么。",
    "lab-1": "光听还不够，我们来亲手跑一遍。左边选一个输入，就是给机器一个它可以处理的数据；中间选一条规则，就是告诉它该怎么想；然后点执行。你会看到三格一个接一个亮起来，数据像小球一样从输入滚到计算，再滚到输出。试试看，有的组合会很顺，有的组合却会卡在中途，请你留意为什么。",
    "module-2": "第二件事，说说计算里面到底在做什么。计算不是机器在猜，也不是它自己想出来的，它只是拿着一条我们写好的规则，照着走一遍。比如这条规则：如果光线低于五十，就去开灯。机器做的事只有一件，就是拿输入进来的那个数，和五十比一比。比出来是真的，就走开灯这条路；比出来不是，就什么都不做。所以规则写错了，机器就跟着错——它不会怀疑，也不会变通。",
    "lab-2": "现在我们做一件有点坏的事：故意喂给机器一些不合适的输入。规则是固定的一条，如果温度超过二十六摄氏度就打开风扇。下面有四张输入卡片，你一张一张点过去，看看机器会算出什么。有的输入它会算不出来，有的输入它算得理直气壮、结果却明显不对，还有一张卡片，压根就不该被拿来做输入。",
    "worked-example": "我们一起完整地拆一次。任务是这样的：走廊上的自动感应灯，人来就亮，人走一会儿就灭。第一步找输入：它拿到的是传感器送来的一个信号，意思是这个范围内有没有人。第二步看计算：规则是，如果检测到有人，就去开灯；如果检测不到人，就等一会儿再关灯。第三步看输出：灯亮起来，或者灯熄灭。第四步再回头检查一遍：输入的信号对不对？规则写得全不全？输出会不会影响别人？三步都对上了，这个装置才算想清楚了。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。学校想在教室里装一台小助手，能自己判断光线够不够，还能提醒大家安静阅读。下面有六张卡片，请你把它们放进正确的格子里：哪些是它要拿到的输入，哪些是它要照着算的规则，哪些是它最后做出来的输出。放对了会告诉你理由，放错了会给你一个提示，可以再试一次。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现自动门、一个算错了的温度，还有一道关于数据安全的题目，看看你能不能把学到的三格模型和那条责任提醒都用上去。",
    "summary": "这节课我们记住了三句话。第一句，机器做事只有三步：输入拿到数据，计算按规则算一算，输出动手做事，三步有先后，不能调换。第二句，计算就是拿着一条规则去比一比、算一算，机器不会猜，也不会变通。第三句，输入不对，结果就怪：类型不对它算不出来，数值抄错它会照着算错，而别人的个人信息压根就不该被随便拿来做输入。回到开头那盏自己亮起来的灯，它靠的就是这三格——而最后该由人把关的那一步，永远还是人。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：用输入、计算、输出三个词，说出电饭煲是怎么把饭煮好的。第二层能力应用，动手做：找一个家里的自动装置，把它的三格写在一张纸上，再写清楚它的输入是从哪个传感器来的。第三层迁移挑战，选做：给教室设计一个自动小助手，写出它的输入、计算、输出，并说明你会怎样防止它拿到不该拿的数据。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 机器做事的三步", "lab-1": "动手一 三格数据流动器", "module-2": "概念二 计算就是照规则",
    "lab-2": "动手二 输入不对结果就怪", "worked-example": "例题讲解 拆开自动感应灯", "conceptest-1": "概念测试",
    "synthesis": "综合任务 教室小助手三格拆解", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 动手一：可选的输入（模拟传感器送来的数据）
IO_INPUTS = [
    ("lux30", "光线传感器：30 勒克斯", "lux", "30 勒克斯"),
    ("lux80", "光线传感器：80 勒克斯", "lux", "80 勒克斯"),
    ("press", "按钮：被按下了", "button", "按钮已被按下"),
    ("dist120", "距离传感器：120 厘米", "dist", "120 厘米"),
]

# 动手一：可选的规则
IO_RULES = [
    ("dark", "如果光线低于 50 勒克斯，就去开灯", "lux", "光线的亮度数值"),
    ("press", "如果按钮被按下，就去开门", "button", "按钮被按下的信号"),
    ("near", "如果距离小于 30 厘米，就报警", "dist", "距离的数值"),
]

# 动手二：固定规则下的四张输入卡片（其中三张是坑）
BAD_CASES = [
    ("ok", "输入卡片 ①：温度 28 ℃",
     "拿 28 和 26 比一比：28 > 26，条件成立。",
     "机器把风扇打开了。输入是数值、单位没错、大小也合理，它算得又快又准——这是最顺的一种情况。",
     ""),
    ("text", "输入卡片 ②：温度「很热」",
     "这条规则要拿一个数去和 26 比大小，可送进来的是一句「很热」。比不了。",
     "机器算不出来，风扇一动不动。它不会猜「很热」到底是几度——机器只认能比较的数据。",
     "常见错误：以为机器「听懂意思」就能干活。它听不懂话里的意思，只认数据。"),
    ("unit", "输入卡片 ③：温度 268 ℃",
     "拿 268 和 26 比一比：268 > 26，条件成立。算得一点没错。",
     "风扇呼呼转了起来——可教室里只有 26.8 ℃。原来是抄数据时把 26.8 写成了 268。机器不会怀疑数据，数值错一位，它就照错一位算下去。",
     "常见错误：误认为「机器算出来的就一定对」。它只是不算错，不代表你给的数据没错。"),
    ("privacy", "输入卡片 ④：同学的手机号 13X****5678",
     "这条规则要的是温度，送进来的却是别人的手机号。类型对不上，也没必要拿来做输入。",
     "机器拒绝执行。就算它算得出来，我们也不该这样做——别人的姓名、手机号、住址都是个人信息，不能随便拿来当输入，更不能打包上传。",
     "常见错误：觉得「手边有什么数据就用什么」。用数据之前先问一句：这个数据，我该不该拿？"),
]

# 综合任务：六张卡片放进三个格子
TRIPLE_CARDS = [
    ("lux", "光线传感器送来的亮度数值", "in", "它是装置从外面拿回来的数据，住在输入这一格。"),
    ("btn", "同学按下按钮的信号", "in", "这也是外面送进来的数据，同样是输入。"),
    ("rule1", "比较一下：亮度小于 50 吗？", "calc", "这是一条要比一比的规则，住在计算这一格。"),
    ("rule2", "判断一下：按钮被按下了吗？", "calc", "这也是照规则算一算，属于计算。"),
    ("out1", "教室的灯亮起来", "out", "这是装置最后动手做出来的事，住在输出这一格。"),
    ("out2", "屏幕显示「请安静阅读」", "out", "屏幕上出现提示，也是装置做出来的输出。"),
]

TRIPLE_BINS = [
    ("in", "① 输入（数据从哪儿来）"),
    ("calc", "② 计算（照着规则算一算）"),
    ("out", "③ 输出（最后做了什么）"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-input-output 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：三格数据流动器（输入 + 规则 → 执行 → 三格依次亮起）
   3) 动手二：怪结果实验（不合适的输入 → 算不出来 / 算得没错结果却怪）
   4) 综合任务：六张卡片放进 输入 / 计算 / 输出 三格
   ============================================================ */
(function () {
  'use strict';

  /* 三格模型样式（走主题变量，不写死颜色） */
  var st = document.createElement('style');
  st.textContent =
    '.io-row{display:flex;align-items:stretch;gap:8px;flex-wrap:wrap;margin-top:14px;}' +
    '.io-row .inner-card{flex:1;min-width:170px;margin:0;transition:box-shadow .35s ease;}' +
    '.io-arrow{display:grid;place-items:center;color:var(--muted);font-size:20px;font-weight:800;min-width:20px;}' +
    '.io-v{color:var(--text-secondary);font-size:14px;line-height:1.6;margin:0;min-height:44px;}' +
    '.io-cell-lit{box-shadow:0 0 0 2px var(--brand) inset;}';
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

  function setCell(el, text) {
    if (!el) return;
    el.classList.add('selected');
    el.querySelector('.io-v').textContent = text;
  }
  function resetCells(ids) {
    ids.forEach(function (id) {
      var el = document.getElementById(id);
      if (!el) return;
      el.classList.remove('selected');
      el.querySelector('.io-v').textContent = '—';
    });
  }

  /* ---------- 2. 动手一：三格数据流动器 ---------- */
  var panel1 = document.getElementById('io3-panel');
  if (panel1) {
    var IN = {
      lux30:  { label: '光线传感器：30 勒克斯', kind: 'lux', show: '光线亮度 = 30 勒克斯' },
      lux80:  { label: '光线传感器：80 勒克斯', kind: 'lux', show: '光线亮度 = 80 勒克斯' },
      press:  { label: '按钮：被按下了', kind: 'button', show: '按钮信号 = 已按下' },
      dist120:{ label: '距离传感器：120 厘米', kind: 'dist', show: '距离 = 120 厘米' }
    };
    var RULE = {
      dark:  { label: '如果光线低于 50 勒克斯，就去开灯', need: 'lux', needCn: '光线的亮度数值',
               cmp: function (v) { return v < 50; }, yes: '把灯打开', no: '什么都不做（灯不亮）',
               ask: '这条规则要把光线的亮度和 50 比一比。' },
      press: { label: '如果按钮被按下，就去开门', need: 'button', needCn: '按钮被按下的信号',
               cmp: function () { return true; }, yes: '把门打开', no: '门不动',
               ask: '这条规则要检查按钮有没有被按下。' },
      near:  { label: '如果距离小于 30 厘米，就报警', need: 'dist', needCn: '距离的数值',
               cmp: function (v) { return v < 30; }, yes: '发出报警声', no: '不报警',
               ask: '这条规则要把距离和 30 厘米比一比。' }
    };
    var VALUE = { lux30: 30, lux80: 80, dist120: 120 };
    var curIn = null, curRule = null, busy = false;
    var out1 = document.getElementById('io3-verdict');
    var ids1 = ['io3-in', 'io3-calc', 'io3-out'];

    function refresh1() {
      panel1.querySelectorAll('[data-io-in]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.ioIn === curIn);
      });
      panel1.querySelectorAll('[data-io-rule]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.ioRule === curRule);
      });
    }

    panel1.querySelectorAll('[data-io-in]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (busy) return;
        curIn = b.dataset.ioIn;
        resetCells(ids1);
        refresh1();
        out1.className = 'result warn';
        out1.textContent = '输入选好了：' + IN[curIn].label + '。现在再选一条规则，然后点「执行」。';
      });
    });
    panel1.querySelectorAll('[data-io-rule]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (busy) return;
        curRule = b.dataset.ioRule;
        resetCells(ids1);
        refresh1();
        out1.className = 'result warn';
        out1.textContent = '规则选好了：' + RULE[curRule].label + '。现在点「执行」，看着数据一格格走过去。';
      });
    });

    document.getElementById('io3-run').addEventListener('click', function () {
      if (busy) return;
      if (!curIn || !curRule) {
        out1.className = 'result error';
        out1.textContent = '还缺一样：输入和规则都要选好，机器才有东西可算。';
        return;
      }
      busy = true;
      resetCells(ids1);
      var I = IN[curIn], R = RULE[curRule];
      out1.className = 'result warn';
      out1.textContent = '正在执行……先看输入这一格。';
      setTimeout(function () {
        setCell(document.getElementById('io3-in'), I.show);
        out1.textContent = '数据到了输入格里。接着往前走，看计算这一格。';
      }, 120);
      setTimeout(function () {
        if (I.kind !== R.need) {
          setCell(document.getElementById('io3-calc'),
            R.ask + '可是送进来的却是「' + I.show + '」，两样东西对不上号，这条规则用不上。');
          out1.className = 'result error';
          out1.textContent = '卡在计算这一格了：这条规则要的是' + R.needCn +
            '，输入却是另一种数据。常见错误：以为机器会「变通一下」——它只会照规则算，对不上就停在这儿。';
          setTimeout(function () {
            setCell(document.getElementById('io3-out'), '没有输出。装置什么也没做。');
            busy = false;
          }, 620);
          return;
        }
        var ok;
        if (I.kind === 'button') {
          ok = true;
          setCell(document.getElementById('io3-calc'), '检查按钮状态：确实被按下了，条件成立。');
        } else {
          ok = R.cmp(VALUE[curIn]);
          setCell(document.getElementById('io3-calc'),
            '拿 ' + VALUE[curIn] + ' 和规则里的数比一比：' + (ok ? '条件成立。' : '条件不成立。'));
        }
        out1.textContent = '算完了。最后看输出这一格。';
        setTimeout(function () {
          setCell(document.getElementById('io3-out'), ok ? R.yes : R.no);
          out1.className = 'result';
          out1.innerHTML = ok
            ? '<strong>跑通了：</strong>输入 → 计算 → 输出，三格一格格走完。注意——<strong>顺序不能调换</strong>，没有输入就没有可算的东西，没算完也不知道该输出什么。'
            : '<strong>也算跑通了：</strong>条件不成立的时候，机器「什么都不做」，这本身就是一个正确的输出。' +
              '别以为它坏了——规则里本来就写着，不满足条件就不动手。';
          busy = false;
        }, 700);
      }, 700);
    });

    document.getElementById('io3-reset').addEventListener('click', function () {
      if (busy) return;
      curIn = null; curRule = null;
      resetCells(ids1);
      refresh1();
      out1.className = 'result warn';
      out1.textContent = '清空了。再选一组输入和规则试试。';
    });
  }

  /* ---------- 3. 动手二：怪结果实验 ---------- */
  var panel2 = document.getElementById('bad-panel');
  if (panel2) {
    var CASES = {
      ok: {
        calc: '拿 28 和 26 比一比：28 > 26，条件成立。',
        out: '风扇打开。',
        msg: '输入是数值、单位没错、大小也合理，机器算得又快又准——这是最顺的一种情况。',
        kind: 'ok'
      },
      text: {
        calc: '这条规则要拿一个数去和 26 比大小，可送进来的是「很热」。比不了。',
        out: '算不出来，风扇一动不动。',
        msg: '机器不会猜「很热」到底是几度。常见错误：以为机器「听懂意思」就能干活——它只认能比较的数据，不会变通。',
        kind: 'error'
      },
      unit: {
        calc: '拿 268 和 26 比一比：268 > 26，条件成立。算得一点没错。',
        out: '风扇打开了。',
        msg: '可教室里只有 26.8 ℃ —— 抄数据时把 26.8 写成了 268。机器不会怀疑数据，你错一位，它就跟着错一位。常见错误：误认为「机器算出来的就一定对」，它只是不算错，不代表你给的数据没错。',
        kind: 'error'
      },
      privacy: {
        calc: '这条规则要的是温度，送进来的却是别人的手机号。类型对不上，也不该拿它来做输入。',
        out: '装置拒绝执行，并且弹出一句提醒。',
        msg: '同学姓名、手机号、住址都是个人信息，不能随便拿来当输入，更不能打包上传。常见错误：觉得「手边有什么数据就用什么」——用之前先问一句：这个数据，我该不该拿？',
        kind: 'privacy'
      }
    };
    var ids2 = ['bad-in', 'bad-calc', 'bad-out'];
    var out2 = document.getElementById('bad-verdict');

    panel2.querySelectorAll('[data-bad]').forEach(function (b) {
      b.addEventListener('click', function () {
        var c = CASES[b.dataset.bad];
        panel2.querySelectorAll('[data-bad]').forEach(function (x) { x.classList.remove('selected'); });
        b.classList.add('selected');
        resetCells(ids2);
        setTimeout(function () {
          setCell(document.getElementById('bad-in'), b.textContent.trim().replace(/^输入卡片\s*[①②③④]：/, '输入 = '));
        }, 60);
        setTimeout(function () {
          setCell(document.getElementById('bad-calc'), c.calc);
        }, 520);
        setTimeout(function () {
          setCell(document.getElementById('bad-out'), c.out);
          out2.className = 'result ' + (c.kind === 'ok' ? '' : (c.kind === 'privacy' ? 'error' : 'warn'));
          out2.innerHTML = c.kind === 'privacy'
            ? '<strong>这一条不只是算错，是不该算。</strong>' + c.msg
            : (c.kind === 'ok'
              ? '<strong>结果正常。</strong>' + c.msg
              : '<strong>结果很怪——但机器一点没错。</strong>' + c.msg);
        }, 980);
      });
    });
  }

  /* ---------- 4. 综合任务：三格分类 ---------- */
  var bank3 = document.getElementById('triple-bank');
  if (bank3) {
    var picked3 = null, done3 = 0;
    var out3 = document.getElementById('triple-out');

    bank3.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        bank3.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked3 = card;
        out3.className = 'result warn';
        out3.textContent = '已选中「' + card.textContent.trim() + '」，现在点下面你认为对的那个格子。';
      });
    });

    document.querySelectorAll('[data-triple-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked3) {
          out3.className = 'result warn';
          out3.textContent = '先点上面的一张卡片，再点格子。';
          return;
        }
        var want = picked3.dataset.kind, got = bin.dataset.tripleBin;
        picked3.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked3.textContent.trim() + ' ✓';
          bin.querySelector('.bin-body').appendChild(tag);
          picked3.classList.add('done');
          picked3.disabled = true;
          done3++;
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了！</strong>' + picked3.dataset.why;
          bin.classList.add('ok');
          picked3 = null;
          if (done3 === 6) {
            out3.className = 'result';
            out3.innerHTML = '<strong>六张卡片全部归位。</strong>最快的判断办法是问三句话：' +
              '这份数据是从外面<strong>拿进来</strong>的吗？那它是输入。' +
              '这一句是在<strong>比一比、算一算</strong>吗？那它是计算。' +
              '这件事是装置最后<strong>做出来</strong>的吗？那它是输出。';
          }
        } else {
          out3.className = 'result error';
          out3.innerHTML = '<strong>再想一下：「' + picked3.textContent.trim() + '」</strong>' +
            '先问自己：它是从外面拿进来的数据，是要照规则算一算，还是装置最后做出来的事？<br>' +
            '<span style="color:var(--muted)">常见错误：把「数据」和「规则」搞混了。' +
            '数据是别人送来的，规则是我们自己写好的——规则像一句话，数据像一个数。</span>';
          picked3.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
      });
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：机器是怎么知道天黑的？", TTS["pretest"], [
        {"q": "教室的灯，天一黑就自己亮了。它真的是「看见」天黑了吗？",
         "options": [("不是，是光线传感器把亮度变成了一个数，送进机器里", True),
                     ("是，灯自己长了一只眼睛", False),
                     ("是，有同学在旁边帮它按开关", False)],
         "explain": "灯不会看，也不会猜。它靠的是一根光线传感器，把「有多亮」变成一个能比较的数值。"
                    "<strong>错因提醒：</strong>常见错误是把传感器当成「眼睛」。它更像一只把光变成数字的手，"
                    "真正做决定的是后面的计算。"},
        {"q": "下面哪一样，是智能台灯的「输入」？",
         "options": [("光线的亮度数值", True), ("灯亮起来这件事", False), ("灯泡的玻璃外壳", False)],
         "explain": "送进去给机器处理的数据，才是输入；灯亮起来是它最后做出来的事，那是输出。"
                    "<strong>错因提醒：</strong>最容易搞混的就是「输入的」和「输出的」——"
                    "记住方向：从外面送进来的叫输入，从装置做出去的叫输出。"},
        {"q": "风扇在温度超过 26 ℃ 时自动转起来。它要先做什么？",
         "options": [("先测到当前的温度", True), ("先让风扇转起来试试", False), ("先自己猜一个温度", False)],
         "explain": "顺序是：先有输入，才有计算，最后才有输出。没有数据，机器什么也算不出来。"
                    "<strong>错因提醒：</strong>不少同学误认为机器会「先动手再说」，"
                    "其实它每一步都要等上一步的结果。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "机器做事只有三步：输入、计算、输出", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们平时做事凭感觉就够了（And）；可像自动感应灯这种装置，它没有眼睛也没有想法，只会一件事一件事地做（But）；所以我们得把它做的事拆成看得清的三步——输入、计算、输出，才能看懂它，也才能自己动手做一个（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">不管是自动感应灯、电饭煲还是智能台灯，抽象地看，它们做的事都只有三步。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>① 输入</strong></p><p style="color:var(--muted)">先拿到要处理的数据：光线多亮、温度多少、按钮有没有被按下。</p></div>
          <div class="inner-card"><p><strong>② 计算</strong></p><p style="color:var(--muted)">按一条写好的规则，把这些数据比一比、算一算。</p></div>
          <div class="inner-card"><p><strong>③ 输出</strong></p><p style="color:var(--muted)">照着算出来的结果动手做事：开灯、开门、报警。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="输入、计算、输出三格模型示意图：传感器送来的数据进入输入格，在计算格里按规则比较判断，最后从输出格做出动作">
          <figcaption>三格模型：数据从输入进来，在计算格被按规则比一比，最后从输出格做出去</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>举个例子：自动感应门</strong></p>
          <p style="color:var(--muted)">输入——门边的传感器送来一个信号：这个范围内有没有人 → 计算——照规则比一比：检测到人了吗 → 输出——有人就把门打开，没人就把门关上。</p>
        </div>
        <div class="kid-note"><span class="emoji">💡</span><div><strong>记一句口诀：</strong>输入是眼睛，计算是脑袋，输出是手脚。眼睛没看见，脑袋就没得想；脑袋没想好，手脚就不知道该做什么。</div></div>
{insight_box([
    {"lens": "看见它", "text": "身边每一个「会自己做事」的装置，都能拆出这三格：路灯、扫地机、自动晾衣架，一个都不例外。"},
    {"lens": "解释它", "text": "为什么顺序不能调换？因为没有输入就没有数据可算，没算完就不知道输出什么——每一步都得等上一步。"},
    {"lens": "迁移它", "text": "你自己做事也是这三步：先看清情况（输入），再想一想（计算），最后动手（输出）。差别只在于人会变通，机器不会。"},
])}
    ''', tag="概念一"))

    in_btns = "\n".join(
        f'            <button class="choice" data-io-in="{k}" style="text-align:center">{label}</button>'
        for k, label, _kind, _show in IO_INPUTS
    )
    rule_btns = "\n".join(
        f'            <button class="choice" data-io-rule="{k}" style="text-align:center">{label}</button>'
        for k, label, _need, _cn in IO_RULES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：三格数据流动器", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">给机器一个输入，再给它一条规则，然后点「执行」。三格会一个个亮起来，看数据怎样从左边走到右边。</p>
        <div class="lab-panel" id="io3-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个输入（传感器送来的数据）</div>
          <div class="sort-bank">
{in_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 选一条规则（机器该怎么想）</div>
          <div class="sort-bank">
{rule_btns}
          </div>
          <div class="io-row">
            <div class="inner-card" id="io3-in"><p><strong>① 输入</strong></p><p class="io-v">—</p></div>
            <div class="io-arrow">→</div>
            <div class="inner-card" id="io3-calc"><p><strong>② 计算</strong></p><p class="io-v">—</p></div>
            <div class="io-arrow">→</div>
            <div class="inner-card" id="io3-out"><p><strong>③ 输出</strong></p><p class="io-v">—</p></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="io3-run" style="text-align:center">▶ 执行</button>
            <button class="choice" id="io3-reset" style="text-align:center">重新开始</button>
          </div>
          <p class="result warn" id="io3-verdict" style="margin-top:12px">请先选一个输入，再选一条规则。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>多试几组，你会发现两种「跑不通」：</strong>一种是条件没满足，机器什么都不做——这没错，规则本来就这么写的；另一种是输入和规则<strong>对不上号</strong>，它算不下去，卡在中间那一格。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "计算不是猜：它只会照着规则走一遍", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">「计算」这一格里，机器看不出任何聪明。它只做一件事：拿规则里的条件，和输入的数据<strong>比一比</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>取出数据：</strong>把输入格里的那个数拿出来。</div></div>
          <div class="step"><span class="n">2</span><div><strong>比一比：</strong>按规则的条件比较，比如「28 是不是大于 26」。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>得出结论：</strong>成立就走一条路，不成立就走另一条路——结果只有两种，没有第三种。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="三张输入卡片对比示意图：数值合理的输入得到正常结果，文字输入算不出来，抄错单位的数值算出怪结果">
          <figcaption>同样一条规则，换三张输入卡片：数值合理就正常，类型不对就算不出来，数值抄错就会算出怪结果</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">以为机器会「看着办」、会「变通一下」。它不会。规则说比大于，它就只比大于；送进来的东西没法比，它就卡在原地。所以设备出的怪结果，多半不是机器的问题，而是<strong>输入或规则写错了</strong>。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🧭</span><div><strong>一句话记住：</strong>机器只是不算错，不代表它给的数据没错。最后看结果的人，还是我们。</div></div>
    ''', tag="概念二"))

    bad_btns = "\n".join(
        f'            <button class="choice" data-bad="{k}" style="text-align:center">{label}</button>'
        for k, label, _c, _o, _m in BAD_CASES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：输入不对劲，它会算出什么？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">规则固定是这一条：<strong>如果温度超过 26 ℃，就打开风扇。</strong>下面四张输入卡片，一张一张点过去，看看机器各会算出什么。</p>
        <div class="lab-panel" id="bad-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">可选的四张输入卡片</div>
          <div class="sort-bank">
{bad_btns}
          </div>
          <div class="io-row">
            <div class="inner-card" id="bad-in"><p><strong>① 输入</strong></p><p class="io-v">—</p></div>
            <div class="io-arrow">→</div>
            <div class="inner-card" id="bad-calc"><p><strong>② 计算</strong></p><p class="io-v">—</p></div>
            <div class="io-arrow">→</div>
            <div class="inner-card" id="bad-out"><p><strong>③ 输出</strong></p><p class="io-v">—</p></div>
          </div>
          <p class="result warn" id="bad-verdict" style="margin-top:12px">点一张输入卡片，看机器怎么反应。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛡️</span><div><strong>四张里有一张，不是算得对不对的问题，而是该不该算。</strong>别人的姓名、手机号、住址都是个人信息。数据可以帮机器做事，但不是什么数据都能拿——这条规矩，比三格模型本身更重要。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：把自动感应灯拆成三格", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>走廊上的自动感应灯，人来就亮，人走一会儿就灭。请把它拆成输入、计算、输出三格，并说说为什么要这样分。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>找输入：</strong>它从传感器拿到一个信号——这个范围内<strong>有没有人</strong>。这是从外面送进来的数据。</div></div>
          <div class="step"><span class="n">2</span><div><strong>看计算：</strong>规则是「检测到有人就开灯；检测不到人就等一会儿再关灯」。这是照着规则比一比的判断。</div></div>
          <div class="step"><span class="n">3</span><div><strong>看输出：</strong>灯亮起来，或者灯熄灭。这是装置最后做出来的事。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>回头检查：</strong>输入的信号准不准？规则写得全不全（人走之后要不要延迟）？输出会不会打扰到别人？三步都对上了，这个装置才算想清楚。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">把「灯亮了」写成输入。灯亮是装置<strong>做出去</strong>的事，是输出。判断方向有个笨办法但很管用：问一句「这是别人给它的，还是它给别人的？」别人给它的，就是输入。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "「输入 → 计算 → 输出」这三格的顺序，能不能调换？",
         "options": [("不能，先有数据才谈得上算，算完才知道输出什么", True),
                     ("能，反正三件事最后都做了", False),
                     ("能，机器会自己重新排一遍", False)],
         "explain": "顺序就是这条模型的骨架：没有输入，计算这一格没有东西可拿；没有算完，输出也不知道该做什么。"
                    "<strong>错因提醒：</strong>容易误认为「三步都做了就行」——顺序一换，机器就停在中间动不了。"},
        {"q": "小智想做「有人靠近就亮灯」，却装了一个只会测温度的传感器。会发生什么？",
         "options": [("输入和规则对不上，计算进行不下去，也就没有输出", True),
                     ("灯照样会亮，机器会变通一下", False),
                     ("传感器会自动变成测人的", False)],
         "explain": "规则要的是距离或人的信号，送进来的却是温度，两边对不上号，机器就卡在计算这一格。"
                    "<strong>错因提醒：</strong>常见错误是以为机器会「看着办」——它不会变通，输入和规则必须配套。"},
        {"q": "为什么说「机器算出来的结果，还得我们再看一眼」？",
         "options": [("因为输入要是抄错了，机器也会照着算出一个怪结果", True),
                     ("因为机器算得比较慢", False),
                     ("因为机器会故意骗人", False)],
         "explain": "机器只是不算错，不代表你给的数据没错。数据错一位，它就跟着错一位。"
                    "<strong>错因提醒：</strong>误认为「机器算的就是对的」，是这一课最需要改掉的一个想法。"}
    ], tag="概念测试"))

    card_btns = "\n".join(
        f'          <button class="sort-item" data-kind="{kind}" data-why="{why}">{t}</button>'
        for _k, t, kind, why in TRIPLE_CARDS
    )
    bin_html = "\n".join(f'''            <div class="sort-bin" data-triple-bin="{k}">
              <h4>{label}</h4>
              <div class="bin-body"></div>
            </div>''' for k, label in TRIPLE_BINS)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给教室小助手配好三格", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张卡片，再点你认为对的那个格子。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待归位的六张卡片</div>
          <div class="sort-bank" id="triple-bank">
{card_btns}
          </div>
          <div class="sort-bins" style="grid-template-columns:repeat(3,1fr)">
{bin_html}
          </div>
          <p class="result warn" id="triple-out" style="margin-top:12px">点一张卡片开始归位。</p>
        </div>
        <div class="inner-card">
          <p><strong>放完以后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">如果这台小助手要记录班上同学的阅读时长，它会拿到哪些数据？这些数据里有没有不该随便收集的？你会怎样写规则，让它既好用又不越界？</p>
          <textarea id="syn-answer" rows="3" placeholder="它的输入有……其中……不该随便收集，所以我的规则会……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，三格还在不在", TTS["posttest"], [
        {"q": "自动门的输入是「门边有没有人」，输出是「开门或关门」。中间「计算」那一格在做什么？",
         "options": [("按规则判断「有人」这个条件成不成立", True),
                     ("把门推开", False),
                     ("负责给门供电", False)],
         "explain": "计算格里只有一件事：照规则比一比、判断一下。推门是输出，供电是另一回事。"
                    "<strong>错因提醒：</strong>常见错误是把「动手做的那件事」也算进计算里——动手的都属于输出。"},
        {"q": "一个智能温度计显示教室有 268 ℃。最可能发生了什么？",
         "options": [("输入的数据抄错了单位，26.8 被写成了 268", True),
                     ("教室真的变热了", False),
                     ("温度计自己坏了，和输入无关", False)],
         "explain": "268 确实大于 26，机器算得一点没错。问题出在送进去的数据上——这就是「算得没错，结果很怪」。"
                    "<strong>错因提醒：</strong>容易误认为「结果怪就是机器坏了」。先回头查输入，多半错在那一格。"},
        {"q": "小组想做一个「记录同学喝水次数」的小程序，把全班同学的姓名和学号当成输入。下面哪种做法最稳妥？",
         "options": [("只在班里内部使用，不公开名单，不上传到公开的地方，用完就删", True),
                     ("发到班级群里让大家都看看", False),
                     ("顺手把家长的电话也一起录进去", False)],
         "explain": "姓名、学号、电话都是个人信息，够用就好、不外传、用完就删，这是最基本的一条规矩。"
                    "<strong>错因提醒：</strong>常见的错误想法是「反正是班里的，没关系」——"
                    "个人信息一旦传出去，就收不回来了。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把三格模型讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>三步是什么：</strong>输入拿到数据，计算按规则算一算，输出动手做事——三步有先后，不能调换。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>计算是什么：</strong>拿出输入的数据，和规则里的条件比一比，得出成立或不成立——机器不会猜，也不会变通。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>输入为什么重要：</strong>类型不对它算不出来，数值抄错它会算出怪结果——它只是不算错，不代表数据没错。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还有一条不该忘的规矩：</strong>不是所有数据都能当输入。别人的姓名、手机号、住址是个人信息，够用就好、不外传、用完就删。机器可以帮我们做事，但把关的永远是人。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「输入、计算、输出」这三个词，说清楚一盏路灯是怎样自己亮起来的。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出来</strong>——在本子上画三个方框，用箭头连起来，左边写输入，中间写规则，右边写输出。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "用「输入、计算、输出」三个词，说出电饭煲是怎么把饭煮好的。",
            "说出三格模型里每一格各表示什么，并说说为什么顺序不能调换。",
        ],
        [
            "找一个家里的自动装置（自动晾衣架、扫地机、智能台灯都可以），把它的三格写在一张纸上。",
            "写清楚这个装置的输入是从哪个传感器来的，输出又是靠什么做出来的。",
        ],
        [
            "给教室设计一台自动小助手，写出它的输入、计算、输出，并画成三个方框加箭头的示意图。",
            "在上面那道题里补充一条：如果它要收集同学的数据，你会用哪些数据、不用哪些数据，为什么？",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-input-output",
    "node_id": "it-e-input-output",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "输入-计算-输出模型",
    "name_en": "Input, Process, Output: How Machines Decide",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "process-control",
    "domain_cn": "过程与控制",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学五年级：知道控制系统做的事可以拆成输入、计算、输出三步，能在一个自动装置里指出数据从哪里来、按什么规则算、最后做了什么；并通过给机器喂不合适输入的小实验，理解计算的局限与数据的责任。",
    "tags": ["输入", "计算", "输出", "控制系统", "传感器", "数据安全"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「过程与控制」——理解控制系统中输入、计算、输出的基本模型。",
    "hero_question": "教室的灯，天一黑就自己亮了——它到底是怎么知道的？",
    "hero_alt": "输入-计算-输出模型知识结构图：输入是什么、计算在做什么、输出做什么，以及三格的先后关系",
    "hero_caption": "三格模型：输入拿到数据 · 计算按规则比一比 · 输出动手做事 · 顺序不能调换",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "机器是从哪儿拿到数据的？", "d": "它凭什么知道天黑了、有人来了", "v": "机器是从哪儿拿到数据的"},
        {"t": "它凭什么能自己做决定？", "d": "中间那一格到底在算什么", "v": "它凭什么能自己做决定"},
        {"t": "为什么有时候它算出来的结果特别奇怪？", "d": "是不是机器也会出错", "v": "为什么有时候它算出来的结果特别奇怪"},
        {"t": "怎样把一个自动装置拆成三格？", "d": "想自己动手拆一个试试", "v": "怎样把一个自动装置拆成三格"},
    ],
    "objectives": [
        "能说出输入、计算、输出分别是什么意思，知道三步有先后、不能调换",
        "能在三格模型里指出一个自动装置的数据从哪里来、按什么规则算、最后做了什么",
        "能说出输入的类型或数值不对时，机器会算不出来或算出怪结果",
        "能说出一条使用数据的规矩，例如别人的个人信息不能随便拿来当输入",
    ],
    "objectives_plain": [
        "能说出输入、计算、输出分别是什么意思，知道三步有先后、不能调换",
        "能在三格模型里指出一个自动装置的数据从哪里来、按什么规则算、最后做了什么",
        "能说出输入的类型或数值不对时，机器会算不出来或算出怪结果",
        "能说出一条使用数据的规矩，例如别人的个人信息不能随便拿来当输入",
    ],
    "standards": [
        {"content": "理解控制系统中输入、计算、输出的基本模型",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 过程与控制"},
        {"content": "在真实装置中观察并拆解「数据从哪儿来、按什么规则算、做了什么」，初步形成用数据说话的意识和保护个人信息的责任感",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 过程与控制 / 信息社会责任"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是信息科技小学段「过程与控制」的起始课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["it-e-sensors-actuators"],
    "next_meta": "it-e-sensors-actuators",
    "section_images": ["assets/it-e-input-output-fig1.webp", "assets/it-e-input-output-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "天一黑灯就自己亮——它看不见、也不会猜，那它是靠什么知道的？",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把一个自动装置拆成清清楚楚的三格。",
        "objectives": "看清四件事：三步各是什么、怎么拆一个装置、输入错了会怎样、数据该不该拿。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "输入是眼睛，计算是脑袋，输出是手脚——三格有先后，一步也少不了。",
        "lab-1": "选输入、选规则、点执行。留意两种跑不通：条件没满足，和输入跟规则对不上号。",
        "module-2": "计算只是拿数据和规则里的条件比一比。它不猜、不变通，规则错了它跟着错。",
        "lab-2": "四张输入卡片里，有一张不是算得对不对的问题，而是该不该算。",
        "worked-example": "四步走：找输入、看计算、看输出，再回头检查一遍。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "问三句话就能分清：数据是从外面拿进来的？是在比一比算一算？是装置最后做出来的？",
        "posttest": "自动门、错位的温度、还有一道数据安全的题，看看三格模型管不管用。",
        "summary": "三句话：三步是什么、计算是什么、输入为什么重要。再记住一条用数据的规矩。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「过程与控制」的起始一课。五年级学生的难点有两处：一是把「动手做的那件事」当成输入，方向分不清；二是以为机器会「看着办」。所以全课只做三件真能上手的事——用一个三格数据流动器，让学生自己选输入、选规则、点执行，看数据一格一格地走过去（其中特意埋了「输入与规则对不上号」的组合，让机器卡在中间）；再用四张输入卡片做一次「怪结果实验」，把「算不出来」「算得没错结果却怪」「压根不该算」三种情况分开摆出来；最后用教室小助手的六张卡片，把输入、计算、输出三格亲手归位。概念页把三格收成一句口诀（输入是眼睛，计算是脑袋，输出是手脚），责任落点放在第四张卡片上——别人的个人信息不该被随便拿来做输入。",
    "plan_table": """| 1 | cover | 输入-计算-输出模型 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：机器是怎么知道天黑的？ | 起·前测（暴露直觉） |
| 5 | concept | 机器做事只有三步：输入、计算、输出 | 承·概念一（三格 + 口诀 + 生活例子） |
| 6 | interactive | 动手一：三格数据流动器 | 承·动手模拟（选输入+选规则→执行→三格依次亮起） |
| 7 | concept | 计算不是猜：它只会照着规则走一遍 | 承·概念二（计算的本质 + 常见错误） |
| 8 | interactive | 动手二：输入不对劲，它会算出什么？ | 承·怪结果实验（类型不对 / 数值抄错 / 不该拿的数据） |
| 9 | concept | 例题示范：把自动感应灯拆成三格 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给教室小助手配好三格 | 合·迁移应用（三格分类 + 数据责任讨论） |
| 12 | quiz | 后测：换几个情境，三格还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把三格模型讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：输入 / 计算 / 输出 三栏与先后关系\n- P5 三格模型示意图（已生成）：传感器数据进入输入格，在计算格被按规则比较，最后从输出格做出动作\n- P7 三张输入卡片对比图（已生成）：数值合理正常、文字输入算不出来、抄错单位算出怪结果\n- 三张图均为教学示意图，不涉及任何真实设备界面、截图或商标\n- 若需补充：光线传感器、自动门等实物照片（需获得授权后使用）",
}
