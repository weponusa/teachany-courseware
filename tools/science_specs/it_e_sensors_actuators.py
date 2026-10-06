# -*- coding: utf-8 -*-
"""小学信息科技 · 传感与执行（初识）（G6）—— 补齐知识树「过程与控制」空缺

学科语气：信息科技 = 概念 + 动手并重。本课不背术语，只做三件真能上手的事：
  ① 元件配对台：给「天黑自动开灯」这个任务，从 5 张感知元件卡 + 4 张执行元件卡里
     各挑一个装上，点「通电测试」，看它能不能自己跑起来（含"只有传感器没有执行器"与
     "只有执行器没有传感器"两种残缺）
  ② 闭环小工坊：三个任务（天黑开灯 / 有人靠近播报 / 土干浇水），从一张混装元件库里
     自己判断该用哪个传感器、哪个执行器，接好试跑
  ③ 智能花房四格归位：把 8 张卡片分进 感知 / 判断 / 动作 / 再感知 四个格子
最后收口到一句可带走的口诀与一条责任提醒：
  感知是感官，判断是大脑，执行是手脚；
  少一样都干不成活——只有传感器没有执行器，就只能看不能动。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)
import json

F1 = './assets/it-e-sensors-actuators-fig1.webp'
F2 = './assets/it-e-sensors-actuators-fig2.webp'

TTS = {
    "hero": "先玩一个猜谜。教室里没有人，灯却在天黑的时候自己亮了；花盆没有人管，土干了却自己浇上了水。这些装置凭什么知道该动手了？答案藏在两种小小的元件里：一种负责感觉，把看不见的变化变成能比较的数据；另一种负责动手，把电变成看得见的动作。今天这节课，我们要认识这两种元件，还要亲手给三个任务配上对的元件。你会发现，少了一样，机器就干不成活。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道机器到底靠什么感觉到外面的变化，还是想知道它凭什么能把事情做出来，又或者你想弄明白为什么有的装置只会看、不会动，再或者你想亲手给一个任务配齐元件。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出感知元件和执行元件分别负责什么，能各举出两个例子。第二，能在几个常用元件里挑出适合某个任务的传感器和执行器。第三，能说清楚只有传感器没有执行器会怎样，只有执行器没有传感器又会怎样。第四，能把一个自动装置拆成感知、判断、动作、再感知四步，说出它其实是一个闭环。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先说感知元件。机器没有眼睛、耳朵和皮肤，它对世界一无所知，所以第一步得给它装上能感觉的元件。这类元件的本事只有一件：把看不见的变化变成能比较的数据。光线有多亮、温度有多高、有没有东西靠近、土里有多湿，都变成一个个能比的数。这样的元件，我们叫做传感器。要特别记住：它只管把变化变成数据，不管该不该动手——那后面再说。",
    "lab-1": "光听还不够，我们来亲手接一次线。任务已经定好：天黑的时候，教室的灯自己亮起来。左边是五张感知元件卡，右边是四张执行元件卡，各挑一张装上去，然后点通电测试。有的组合能跑起来，有的会卡住不动，还有的组合会让装置迷迷糊糊地乱做事——请你留意，它到底缺了哪一样。",
    "module-2": "第二件事，说说执行元件。光能感觉还不够。传感器只是把外面的事变成数据，它自己不会动，也不会响。真正让事情发生的，是另一类元件：把电变成看得见、听得到的动作。灯泡发光、小喇叭发声、小电机转动、小水泵抽水，这些都是执行元件，也叫执行器。所以一台自动装置最少要有两样：一个负责感觉，一个负责动手。少了执行器，它就只能看不能动；少了传感器，它就只能动，却不知道该什么时候动。",
    "lab-2": "现在难度升级。工坊里来了三个任务：天黑自动开灯、有人靠近就播报提醒、土干了自动浇水。元件库里六张卡片是混在一起放的，没有写清哪张是感觉的、哪张是干活的，得靠你自己判断。选一个任务，各挑一张卡片接上，再点试跑，看看它能不能真的把活干完。",
    "worked-example": "我们一起把天黑自动开灯这件事完整拆一遍。第一步感知：光线传感器送来一个数值，告诉我们现在有多亮。第二步判断：拿这个数值和定好的标准比一比，现在是不是比标准暗了。第三步动作：确实是暗了，就接通灯的电源，让灯亮起来。第四步再感知：灯亮了以后，光线传感器要再读一次——现在够亮了吗？还暗就继续开着，够亮了就熄掉。第四步是很多同学会漏掉的，少了它，装置就只能傻乎乎地一直开着。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。学校要造一间智能花房，能自己照看温度、土里的湿度和光线。下面有八张卡片，请你判断每一张该放进哪一格：哪些是它拿到数据的那一步，哪些是它比一比的那一步，哪些是它动手做出来的那一步，哪些是它做完之后再回头看一眼的那一步。放对了会告诉你理由，放错了会给你一个提示，可以再试一次。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现自动门、一个只会响不会做的装置，还有一道关于用电安全的题目，看看你能不能把感知、判断、动作、再感知这四步都用上去。",
    "summary": "这节课我们记住三句话。第一句，一台会自己干活的装置，最少要有两样元件：感知元件负责把看不见的变化变成能比较的数据，执行元件负责把电变成看得见的动作。第二句，只有传感器没有执行器，它就只能看不能动；只有执行器没有传感器，它就只能动，却不知道该什么时候动。第三句，完整的装置是一个闭环：感知、判断、动作，做完以后再感知一次，看看事情有没有办成。回到开头那盏自己亮起来的灯，它靠的就是这四步。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出感知元件和执行元件各负责什么，各举两个生活中的例子。第二层能力应用，动手做：找一个家里的自动装置，写出它的感知元件是什么、执行元件是什么，再画成四步闭环。第三层迁移挑战，选做：给学校设计一台自动浇花装置，写出它的感知元件、判断标准、执行元件和再感知的时机，并说明怎样保证它不会浇太多水。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 感知元件：机器的感官", "lab-1": "动手一 元件配对台", "module-2": "概念二 执行元件：机器的手脚",
    "lab-2": "动手二 闭环小工坊", "worked-example": "例题讲解 拆开天黑自动开灯", "conceptest-1": "概念测试",
    "synthesis": "综合任务 智能花房四格归位", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 动手一：感知元件卡
SA_SENSORS = [
    ("lux", "光线传感器", "能感觉到有多亮"),
    ("temp", "温度传感器", "能感觉到有多热"),
    ("dist", "距离传感器", "能感觉到有没有东西靠近"),
    ("sound", "声音传感器", "能感觉到有多吵"),
    ("humi", "湿度传感器", "能感觉到土里有多湿"),
]

# 动手一：执行元件卡
SA_ACTS = [
    ("lamp", "灯", "能把灯点亮"),
    ("fan", "小风扇", "能吹出风"),
    ("speaker", "小喇叭", "能发出声音"),
    ("motor", "小水泵", "能把水抽上来"),
]

# 动手二：三个任务（传感器 → 执行器 → 干成的活）
WS_TASKS = [
    ("t1", "任务①：天黑自动开灯", "lux", "lamp", "天暗下来，教室的灯自己亮起来"),
    ("t2", "任务②：有人靠近就播报", "dist", "speaker", "有人走过来，小喇叭自动说一句请注意安全"),
    ("t3", "任务③：土干了自动浇水", "humi", "motor", "土里不够湿了，小水泵自己抽水浇花"),
]

# 动手二：混装元件库（六张卡，不标明类型）
WS_CARDS = [
    ("lux", "光线传感器", "s"),
    ("dist", "距离传感器", "s"),
    ("humi", "土湿度传感器", "s"),
    ("lamp", "灯", "a"),
    ("speaker", "小喇叭", "a"),
    ("motor", "小水泵", "a"),
]

# 综合任务：八张卡片，四个格子
SR_CARDS = [
    ("s1", "温度传感器送来的温度数值", "sense", "它是从外面拿回来的数据，住在「感知」这一格。"),
    ("s2", "土里的湿度传感器送来的湿度数值", "sense", "这也是从外面送进来的数据，同样是感知。"),
    ("j1", "比一比：屋里的温度是不是低于 18 ℃", "judge", "这是拿数据和标准比一比的规则，住在「判断」这一格。"),
    ("j2", "比一比：土里的湿度是不是低于 40%", "judge", "这也是照规则算一算，属于判断。"),
    ("a1", "小喇叭发出提示音", "act", "这是装置最后动手做出来的事，住在「动作」这一格。"),
    ("a2", "小水泵抽水浇花", "act", "抽水浇花也是装置做出来的事，属于动作。"),
    ("r1", "浇完水，再看一眼土里的湿度", "re", "做完之后再回头读一次数据，步是「再感知」。"),
    ("r2", "灯亮以后，再看一眼屋里的亮度", "re", "这也是做完之后回头再看一眼，用来确认事情办成了没有。"),
]

SR_BINS = [
    ("sense", "① 感知（把变化变成数据）"),
    ("judge", "② 判断（照规则比一比）"),
    ("act", "③ 动作（动手做出来）"),
    ("re", "④ 再感知（做完再看一眼）"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-sensors-actuators 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：元件配对台（单任务 → 检查 感知口 / 动作口 是否齐全、是否对得上）
   3) 动手二：闭环小工坊（三任务 + 混装元件库）
   4) 综合任务：智能花房八卡四格归位
   ============================================================ */
var WS_TASKS = __WS_TASKS_JSON__;
var WS_CARDS = __WS_CARDS_JSON__;
(function () {
  'use strict';

  /* 元件配对台样式（走主题变量，不写死颜色） */
  var st = document.createElement('style');
  st.textContent =
    '.sa-row{display:flex;align-items:stretch;gap:8px;flex-wrap:wrap;margin-top:14px;}' +
    '.sa-row .inner-card{flex:1;min-width:170px;margin:0;transition:box-shadow .35s ease;}' +
    '.sa-arrow{display:grid;place-items:center;color:var(--muted);font-size:20px;font-weight:800;min-width:20px;}' +
    '.sa-v{color:var(--text-secondary);font-size:14px;line-height:1.6;margin:0;min-height:44px;}' +
    '.sa-cell-lit{box-shadow:0 0 0 2px var(--brand) inset;}' +
    '.sa-steps{display:grid;grid-template-columns:repeat(4,1fr);gap:6px;margin-top:12px;}' +
    '.sa-step{border:1px dashed var(--line);border-radius:12px;padding:8px 6px;text-align:center;font-size:13px;color:var(--muted);background:var(--bg-subtle);transition:all .3s ease;}' +
    '.sa-step.on{border-style:solid;border-color:var(--brand);color:var(--link);background:var(--brand-soft);font-weight:700;}' +
    '.sa-chip{display:inline-block;padding:3px 9px;border-radius:999px;background:var(--brand-soft);border:1px solid var(--line);font-size:12px;margin:2px 4px 0 0;}' +
    '@media (max-width:768px){.sa-steps{grid-template-columns:repeat(2,1fr);}}';
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

  function fill(el, text) {
    if (!el) return;
    el.classList.add('selected');
    el.querySelector('.sa-v').textContent = text;
  }
  function empty(el) {
    if (!el) return;
    el.classList.remove('selected');
    el.querySelector('.sa-v').textContent = '空着';
  }
  function lightSteps(ids, upto) {
    ids.forEach(function (id, i) {
      var el = document.getElementById(id);
      if (el) el.classList.toggle('on', i < upto);
    });
  }

  /* ---------- 2. 动手一：元件配对台 ---------- */
  var panel1 = document.getElementById('sa-panel');
  if (panel1) {
    var S1 = {
      lux:   { n: '光线传感器', say: '能感觉到有多亮', read: '光线读数 = 30（有点暗）' },
      temp:  { n: '温度传感器', say: '能感觉到有多热', read: '温度读数 = 26 ℃' },
      dist:  { n: '距离传感器', say: '能感觉到有没有东西靠近', read: '距离读数 = 120 厘米（没人靠近）' },
      sound: { n: '声音传感器', say: '能感觉到有多吵', read: '声音读数 = 42（很安静）' },
      humi:  { n: '湿度传感器', say: '能感觉到土里有多湿', read: '湿度读数 = 55%（不干不湿）' }
    };
    var A1 = {
      lamp:    { n: '灯', say: '能把灯点亮', action: '灯亮了起来' },
      fan:     { n: '小风扇', say: '能吹出风', action: '风扇转了起来' },
      speaker: { n: '小喇叭', say: '能发出声音', action: '喇叭响了一声' },
      motor:   { n: '小水泵', say: '能把水抽上来', action: '水泵开始抽水' }
    };
    var STEP_IDS = ['sa-st1', 'sa-st2', 'sa-st3', 'sa-st4'];
    var sid = null, aid = null, busy1 = false;
    var v1 = document.getElementById('sa-verdict');
    var slotS = document.getElementById('sa-slot-s');
    var slotJ = document.getElementById('sa-slot-j');
    var slotA = document.getElementById('sa-slot-a');

    panel1.querySelectorAll('[data-sa-s]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (busy1) return;
        sid = sid === b.dataset.saS ? null : b.dataset.saS;
        panel1.querySelectorAll('[data-sa-s]').forEach(function (x) {
          x.classList.toggle('selected', x.dataset.saS === sid);
        });
        lightSteps(STEP_IDS, 0);
        if (sid) fill(slotS, S1[sid].n + '：' + S1[sid].say); else empty(slotS);
        v1.className = 'result warn';
        v1.textContent = sid ? ('感知口装上了' + S1[sid].n + '。别忘了右边还要装一个执行元件。')
                             : '感知口清空了。';
      });
    });
    panel1.querySelectorAll('[data-sa-a]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (busy1) return;
        aid = aid === b.dataset.saA ? null : b.dataset.saA;
        panel1.querySelectorAll('[data-sa-a]').forEach(function (x) {
          x.classList.toggle('selected', x.dataset.saA === aid);
        });
        lightSteps(STEP_IDS, 0);
        if (aid) fill(slotA, A1[aid].n + '：' + A1[aid].say); else empty(slotA);
        v1.className = 'result warn';
        v1.textContent = aid ? ('动作口装上了' + A1[aid].n + '。别忘了左边还要装一个感知元件。')
                             : '动作口清空了。';
      });
    });

    document.getElementById('sa-test').addEventListener('click', function () {
      if (busy1) return;
      busy1 = true;
      lightSteps(STEP_IDS, 0);
      if (!sid && !aid) {
        v1.className = 'result error';
        v1.textContent = '两个口都空着。装置既没有感觉，也不能动手，它只是一堆零件。';
        busy1 = false;
        return;
      }
      if (!aid) {
        fill(slotJ, '有数据了，可是没人能动手。');
        fill(slotA, '空着，什么也做不了');
        v1.className = 'result error';
        v1.innerHTML = '<strong>只有传感器，没有执行器——它只能看不能动。</strong>' +
          S1[sid].n + '老老实实把「' + S1[sid].read + '」送了出来，可是后面没有一样东西能把这笔数据变成动作。' +
          '常见错误：以为装上传感器，装置就会自己干活。传感器只会感觉，动手得靠执行元件。';
        lightSteps(STEP_IDS, 2);
        busy1 = false;
        return;
      }
      if (!sid) {
        fill(slotJ, '不知道该跟什么比——没有数据可看。');
        fill(slotA, A1[aid].n + '：' + A1[aid].say);
        v1.className = 'result error';
        v1.innerHTML = '<strong>只有执行器，没有传感器——它能动，却不知道该什么时候动。</strong>' +
          A1[aid].n + '本身是好的，可它拿不到任何数据，只能等着别人来按开关。' +
          '常见错误：以为换上更好的执行器，装置就聪明了。感觉这一头空着，再多力气也使不到点上。';
        lightSteps(STEP_IDS, 1);
        busy1 = false;
        return;
      }
      /* 两个都装了，按顺序点亮四步 */
      v1.className = 'result warn';
      v1.textContent = '正在通电……先看它感觉到了什么。';
      setTimeout(function () {
        fill(slotS, S1[sid].n + '：' + S1[sid].read);
        lightSteps(STEP_IDS, 1);
      }, 80);
      setTimeout(function () {
        fill(slotJ, '把读数和任务的标准比一比：该动手了吗？');
        lightSteps(STEP_IDS, 2);
      }, 620);
      setTimeout(function () {
        fill(slotA, aid === 'lamp'
          ? '灯亮了起来'
          : (A1[aid].n + '动了起来'));
        lightSteps(STEP_IDS, 3);
      }, 1180);
      setTimeout(function () {
        if (sid === 'lux' && aid === 'lamp') {
          lightSteps(STEP_IDS, 4);
          v1.className = 'result';
          v1.innerHTML = '<strong>跑通了！</strong>光线传感器感觉到天暗下来 → 比一比，确实比标准暗 → 把灯的电源接通 → ' +
            '灯亮之后再看一眼亮度。这一圈走下来，就是一台会自己干活的装置。' +
            '<strong>它是个闭环：</strong>最后那一步「再看一眼」，让它能自己检查有没有把事办好。';
        } else if (sid !== 'lux') {
          v1.className = 'result error';
          v1.innerHTML = '<strong>接头卡住了：' + S1[sid].n + '感觉不到任务需要的那件事。</strong>' +
            '这个任务问的是「天黑了没有」，可它读出来的是「' + S1[sid].read + '」——两件事对不上号，判断这一格没有答案。' +
            '<span style="color:var(--muted)">常见错误：以为随便装一个传感器就行。「传感器」只是一大类，' +
            '每个只管感觉一种变化，选型要和任务对上。</span>';
        } else {
          v1.className = 'result error';
          v1.innerHTML = '<strong>感觉对了，动作却配错了。</strong>' + S1[sid].n + '确实读出了「' + S1[sid].read +
            '」，可任务要的是「让灯亮起来」，装上' + A1[aid].n + '之后，它' + A1[aid].action + '。' +
            '<span style="color:var(--muted)">常见错误：抓来一个执行器就用。执行元件也分很多种，' +
            '该发光的不能换成会响的。</span>';
        }
        busy1 = false;
      }, 1740);
    });

    document.getElementById('sa-clear').addEventListener('click', function () {
      if (busy1) return;
      sid = null; aid = null;
      panel1.querySelectorAll('.sort-bank .choice').forEach(function (x) { x.classList.remove('selected'); });
      empty(slotS); empty(slotA);
      document.getElementById('sa-slot-j').querySelector('.sa-v').textContent = '照规则比一比';
      lightSteps(STEP_IDS, 0);
      v1.className = 'result warn';
      v1.textContent = '清空了。再换一组元件试试，注意观察它缺了哪一样。';
    });
  }

  /* ---------- 3. 动手二：闭环小工坊（三任务） ---------- */
  var panel2 = document.getElementById('ws-panel');
  if (panel2) {
    var CARD = {};
    WS_CARDS.forEach(function (c) { CARD[c[0]] = { n: c[1], kind: c[2] }; });
    var TASK = {};
    WS_TASKS.forEach(function (t) { TASK[t[0]] = { title: t[1], s: t[2], a: t[3], say: t[4], got: false }; });
    var curTask = null, put = [], done2 = 0, busy2 = false;
    var out2 = document.getElementById('ws-out');
    var bar2 = document.getElementById('ws-progress');

    function paint2() {
      panel2.querySelectorAll('[data-ws-task]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.wsTask === curTask);
        b.classList.toggle('done', !!TASK[b.dataset.wsTask].got);
      });
      panel2.querySelectorAll('[data-ws-card]').forEach(function (b) {
        b.classList.toggle('selected', put.indexOf(b.dataset.wsCard) >= 0);
      });
    }
    function paintSlots() {
      var s = put[0], a = put[1];
      if (s) fill(document.getElementById('ws-slot-s'), CARD[s].n); else empty(document.getElementById('ws-slot-s'));
      if (a) fill(document.getElementById('ws-slot-a'), CARD[a].n); else empty(document.getElementById('ws-slot-a'));
    }
    function updateBar() {
      if (bar2) bar2.textContent = '已完成任务：' + done2 + ' / 3';
    }
    updateBar();

    panel2.querySelectorAll('[data-ws-task]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (busy2) return;
        curTask = b.dataset.wsTask;
        put = [];
        paint2(); paintSlots();
        var t = TASK[curTask];
        out2.className = 'result warn';
        out2.innerHTML = t.got
          ? ('<strong>' + t.title + '：已经接好了。</strong>' + t.say)
          : ('现在是 <strong>' + t.title + '</strong>。想一想：要看住什么变化，用哪张卡片？要做出什么动作，用哪张卡片？' +
             '从下面的元件库里挑两张，先点的放感知口，后点的放动作口。');
      });
    });

    panel2.querySelectorAll('[data-ws-card]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (busy2) return;
        var k = b.dataset.wsCard;
        if (!curTask) {
          out2.className = 'result error';
          out2.textContent = '先在上面选一个任务，再来挑元件。';
          return;
        }
        var i = put.indexOf(k);
        if (i >= 0) {
          put.splice(i, 1);
        } else if (put.length >= 2) {
          out2.className = 'result warn';
          out2.textContent = '两个接口都满了。先点一下已选中的卡片，把它取下来，再换新的。';
          paint2(); paintSlots();
          return;
        } else {
          put.push(k);
        }
        paint2(); paintSlots();
        out2.className = 'result warn';
        out2.textContent = put.length === 0
          ? '接口清空了。'
          : ('已接上：' + put.map(function (x) { return CARD[x].n; }).join(' → ') +
             (put.length < 2 ? '。还可以再放一张。' : '。现在点「接好，试跑」。'));
      });
    });

    document.getElementById('ws-test').addEventListener('click', function () {
      if (busy2) return;
      if (!curTask) {
        out2.className = 'result error';
        out2.textContent = '先选一个任务。';
        return;
      }
      if (put.length === 0) {
        out2.className = 'result error';
        out2.textContent = '两个接口都空着。装置没有感觉，也不能动手。';
        return;
      }
      busy2 = true;
      var t = TASK[curTask];
      var sen = put[0] ? CARD[put[0]] : null;
      var act = put[1] ? CARD[put[1]] : null;

      if (!act) {
        out2.className = 'result error';
        out2.innerHTML = '<strong>只有传感器，没有执行器——它只能看不能动。</strong>' +
          sen.n + '把外面的变化读了出来，可是后面没有一样东西能动手，' + t.title.replace(/^任务[①②③]：/, '') +
          '这件事就办不成。缺的是执行元件。';
        busy2 = false;
        return;
      }
      if (sen && sen.kind === 'a') {
        out2.className = 'result error';
        out2.innerHTML = '<strong>接口接反了：感知口里装的是执行元件。</strong>' + sen.n +
          '不会感觉，它只会动。常见错误：把「能亮、能响、能转」的元件当成传感器——' +
          '它做的是动作，不是感觉。感知这一格要放的是能读出数据的元件。';
        busy2 = false;
        return;
      }
      if (act.kind === 's') {
        out2.className = 'result error';
        out2.innerHTML = '<strong>两个接口里装的都是感知元件，没有执行器——只能看，不能动。</strong>' +
          sen.n + '和' + act.n + '都能把变化读出来，可谁也动不了手。装置看得很清楚，就是干不成活。';
        busy2 = false;
        return;
      }
      if (put[0] === t.s && put[1] === t.a) {
        t.got = true;
        done2++;
        updateBar();
        paint2(); paintSlots();
        out2.className = 'result';
        out2.innerHTML = '<strong>接得对，跑通了！</strong>' + sen.n + '感觉到变化 → 比一比，该动手了吗 → ' +
          act.n + '把活干出来 → 干完再看一眼，确认事情办成了。' + t.say + '。' +
          (done2 === 3
            ? '<br><strong>三个任务全部接好了。</strong>回头看看，三个装置走的是同一条路：' +
              '感知 → 判断 → 动作 → 再感知。这就是闭环。'
            : '');
      } else {
        var hint = (sen.kind !== 's')
          ? '感知口里装的是执行元件，它感觉不到任何东西。'
          : (put[0] !== t.s
            ? '这个传感器看不住这个任务要看的那件事。'
            : '感觉这一头是对的，可是执行元件选错了：这件活它干不了。');
        out2.className = 'result error';
        out2.innerHTML = '<strong>这一组跑不起来。</strong>' + hint +
          '<br><span style="color:var(--muted)">常见错误：先挑熟悉的元件，再硬套到任务上。' +
          '正确的顺序是反过来——先问「这个任务要看住什么变化」，再问「它该做出什么动作」。</span>';
      }
      busy2 = false;
    });

    document.getElementById('ws-clear').addEventListener('click', function () {
      if (busy2) return;
      put = [];
      paint2(); paintSlots();
      out2.className = 'result warn';
      out2.textContent = '接口清空了，重新挑两张试试。';
    });
  }

  /* ---------- 4. 综合任务：四格归位 ---------- */
  var bank3 = document.getElementById('sr-bank');
  if (bank3) {
    var picked3 = null, done3 = 0;
    var out3 = document.getElementById('sr-out');
    var bar3 = document.getElementById('sr-progress');

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

    document.querySelectorAll('[data-sr-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked3) {
          out3.className = 'result warn';
          out3.textContent = '先点上面的一张卡片，再点格子。';
          return;
        }
        var want = picked3.dataset.kind, got = bin.dataset.srBin;
        picked3.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked3.textContent.trim() + ' ✓';
          bin.querySelector('.bin-body').appendChild(tag);
          picked3.classList.add('done');
          picked3.disabled = true;
          done3++;
          if (bar3) bar3.textContent = '已归位：' + done3 + ' / 8';
          out3.className = 'result';
          out3.innerHTML = '<strong>放对了！</strong>' + picked3.dataset.why;
          bin.classList.add('ok');
          picked3 = null;
          if (done3 === 8) {
            out3.className = 'result';
            out3.innerHTML = '<strong>八张卡片全部归位。</strong>最快的判断办法是问四句话：' +
              '这件事是它<strong>感觉到的</strong>吗？那是感知。' +
              '是在<strong>比一比</strong>吗？那是判断。' +
              '是它<strong>做出来</strong>的吗？那是动作。' +
              '是<strong>做完之后再回头看一眼</strong>吗？那是再感知——少了这一步，装置就不知道自己有没有把事办好。';
          }
        } else {
          out3.className = 'result error';
          out3.innerHTML = '<strong>再想一下：「' + picked3.textContent.trim() + '」</strong>' +
            '先问自己：这是它感觉到的、比出来的、做出来的，还是做完之后再看一眼？<br>' +
            '<span style="color:var(--muted)">常见错误：把「再感知」当成「感知」。第一次读数据是为了决定该不该动手；' +
            '做完之后再读一次，是为了检查事情有没有办成——两次读的虽然都是数据，位置完全不一样。</span>';
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：机器靠什么知道该动手了？", TTS["pretest"], [
        {"q": "教室里没有人，天黑了灯却自己亮起来。它靠什么知道天黑了？",
         "options": [("靠光线传感器，把「有多亮」变成一个能比较的数", True),
                     ("靠灯自己长了一只眼睛", False),
                     ("靠有人偷偷在旁边按开关", False)],
         "explain": "灯不会看，也不会猜。它靠的是一根光线传感器，把「有多亮」变成一个能比较的数值。"
                    "<strong>错因提醒：</strong>常见错误是把传感器当成「眼睛」。它更像一只手，把变化变成数字，"
                    "真正做决定的是后面的判断。"},
        {"q": "下面哪一样，是把电变成动作的执行元件？",
         "options": [("小水泵", True), ("湿度传感器", False), ("一根连接导线", False)],
         "explain": "执行元件负责动手：小水泵能把水抽上来，这是看得见、听得见的动作。"
                    "<strong>错因提醒：</strong>最容易搞混的就是传感器和执行器——"
                    "问一句就行：它是把变化读成数据，还是把电变成动作？"},
        {"q": "一台自动装置只装了传感器，没有装执行元件。它会怎么样？",
         "options": [("能感觉到变化，却什么也做不了", True),
                     ("照样能把活干完", False),
                     ("会自己长出一个执行元件来", False)],
         "explain": "传感器只会感觉，动手必须靠执行元件。少了它，装置就只能看不能动。"
                    "<strong>错因提醒：</strong>不少同学误认为「装得越高级越好」，"
                    "其实一台装置最少要有两样：一个负责感觉，一个负责动手。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "感知元件：机器用来「感觉」的感官", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们做事凭感觉和想法就够了（And）；可机器没有眼睛耳朵，对世界一无所知，你不告诉它外面发生了什么，它就什么也做不了（But）；所以要给它装上两种元件：一种负责感觉，一种负责动手——先认清这两种元件，后面才谈得上让它自己干活（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">机器要自己干活，第一步是能感觉到外面的变化。这类元件本事只有一件：<strong>把看不见的变化，变成能比较的数据</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card"><p><strong>光线传感器</strong></p><p style="color:var(--muted)">把「有多亮」变成数值，比如 30 勒克斯。</p></div>
          <div class="inner-card"><p><strong>温度传感器</strong></p><p style="color:var(--muted)">把「有多热」变成数值，比如 26 摄氏度。</p></div>
          <div class="inner-card"><p><strong>距离传感器</strong></p><p style="color:var(--muted)">把「有没有东西靠近」变成数值，比如 12 厘米。</p></div>
          <div class="inner-card"><p><strong>湿度传感器</strong></p><p style="color:var(--muted)">把「土里有多湿」变成数值，比如 35%。</p></div>
        </div>
        <p style="font-size:16px;margin:14px 0 0">这一大类元件，我们统称为<strong>传感器</strong>，也叫感知元件。它们只管把变化读成数据，<strong>不管该不该动手</strong>——那是后面的判断和动作要做的事。</p>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="四类常见感知元件示意图：光线、温度、距离、湿度传感器各自把一种看不见的变化变成能比较的数值">
          <figcaption>感知元件做的事只有一件：把光线、温度、距离、湿度这些看不见的变化，变成能比较的数值</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">💡</span><div><strong>记一句口诀：</strong>感知是感官，判断是大脑，执行是手脚。感官没看见，大脑就没得想；大脑没想好，手脚就不知道该怎么动。</div></div>
{insight_box([
    {"lens": "看见它", "text": "身边的自动装置都能拆出「感觉」这一头：声控灯在听、扫地机在碰、自动门在看，它们都在把变化变成数据。"},
    {"lens": "解释它", "text": "为什么非要把变化变成数字？因为机器只会比大小。说「有点暗」它比不了，说「30 比 50 小」它一下就能判断。"},
    {"lens": "迁移它", "text": "你自己做事也是这四步：先看情况（感知），再想一想（判断），然后动手（动作），做完还要回头看看效果（再感知）。机器只是把它拆得更清楚。"},
])}
    ''', tag="概念一"))

    s_btns = "\n".join(
        f'            <button class="choice" data-sa-s="{k}" style="text-align:center"><strong>{n}</strong><br><span style="font-size:13px;color:var(--muted)">{d}</span></button>'
        for k, n, d in SA_SENSORS
    )
    a_btns = "\n".join(
        f'            <button class="choice" data-sa-a="{k}" style="text-align:center"><strong>{n}</strong><br><span style="font-size:13px;color:var(--muted)">{d}</span></button>'
        for k, n, d in SA_ACTS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：元件配对台——给一个任务接上元件", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">今天的任务是这一个：<strong>天黑的时候，教室的灯自己亮起来。</strong>左边挑一个感知元件，右边挑一个执行元件，都装好以后点「通电测试」。</p>
        <div class="lab-panel" id="sa-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 感知元件（负责把变化读成数据）</div>
          <div class="sort-bank">
{s_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 执行元件（负责动手把事情做出来）</div>
          <div class="sort-bank">
{a_btns}
          </div>
          <div class="sa-row">
            <div class="inner-card" id="sa-slot-s"><p><strong>感知口</strong></p><p class="sa-v">空着</p></div>
            <div class="sa-arrow">→</div>
            <div class="inner-card" id="sa-slot-j"><p><strong>判断</strong></p><p class="sa-v">照规则比一比</p></div>
            <div class="sa-arrow">→</div>
            <div class="inner-card" id="sa-slot-a"><p><strong>动作口</strong></p><p class="sa-v">空着</p></div>
          </div>
          <div class="sa-steps">
            <div class="sa-step" id="sa-st1">① 感知</div>
            <div class="sa-step" id="sa-st2">② 判断</div>
            <div class="sa-step" id="sa-st3">③ 动作</div>
            <div class="sa-step" id="sa-st4">④ 再感知</div>
          </div>
          <div class="flex-row">
            <button class="choice" id="sa-test" style="text-align:center">▶ 通电测试</button>
            <button class="choice" id="sa-clear" style="text-align:center">清空重来</button>
          </div>
          <p class="result warn" id="sa-verdict" style="margin-top:12px">先各挑一个元件，再看这盏灯能不能自己亮起来。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>多试几组，留意三件事：</strong>两个口都空着、只装了一个、装了两个但和任务对不上——它们的失败原因各不相同。哪一组能一直跑到第四步「再感知」亮起来？</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "执行元件：机器用来「动手」的手脚", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">光能感觉还不够。传感器只是把外面的事变成了数据，它自己不会动，也不会响。真正让事情发生的，是另一类元件。</p>
        <div class="grid grid-2">
          <div class="inner-card"><p><strong>灯</strong></p><p style="color:var(--muted)">通电就发光——把电变成看得见的光。</p></div>
          <div class="inner-card"><p><strong>小喇叭</strong></p><p style="color:var(--muted)">通电就发声——把电变成听得见的声音。</p></div>
          <div class="inner-card"><p><strong>小电机</strong></p><p style="color:var(--muted)">通电就转起来——把电变成转动的力。</p></div>
          <div class="inner-card"><p><strong>小水泵</strong></p><p style="color:var(--muted)">通电就抽水——把电变成看得见的动作。</p></div>
        </div>
        <p style="font-size:16px;margin:14px 0 0">这一大类元件统称为<strong>执行器</strong>，也叫执行元件。它的本事也只有一件：<strong>把电变成动作</strong>。</p>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="闭环四步示意图：感知把变化变成数据，判断照规则比一比，动作动手做出来，再感知回头再读一次数据确认结果">
          <figcaption>完整的一圈：感知 → 判断 → 动作 → 再感知。少了最后一步，装置就不知道自己有没有把事办好</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">以为只要装上传感器，装置就会自己干活。<strong>只有传感器没有执行器，它就只能看不能动</strong>——数据读出来了，却没有人能把它变成动作。反过来，<strong>只有执行器没有传感器</strong>，它就只能动，却不知道该什么时候动，只能等人来按开关。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🧭</span><div><strong>一句话记住：</strong>感觉和动手，一样都不能少。而且做完以后还要再回来看一眼——这一圈合起来叫<strong>闭环</strong>。</div></div>
    ''', tag="概念二"))

    task_btns = "\n".join(
        f'            <button class="choice" data-ws-task="{k}" style="text-align:center">{title}</button>'
        for k, title, _s, _a, _say in WS_TASKS
    )
    card_btns = "\n".join(
        f'            <button class="choice" data-ws-card="{k}" style="text-align:center">{n}</button>'
        for k, n, _kind in WS_CARDS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：闭环小工坊——三个任务，自己判断该用哪两张卡", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个任务，再从元件库里挑两张卡片：<strong>先点的那张放进感知口，后点的那张放进动作口</strong>。元件库里没写谁是谁，得靠你自己判断。</p>
        <div class="lab-panel" id="ws-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一个任务</div>
          <div class="sort-bank">
{task_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 元件库（六张卡混在一起）</div>
          <div class="sort-bank">
{card_btns}
          </div>
          <div class="sa-row">
            <div class="inner-card" id="ws-slot-s"><p><strong>感知口</strong></p><p class="sa-v">空着</p></div>
            <div class="sa-arrow">→</div>
            <div class="inner-card" id="ws-slot-a"><p><strong>动作口</strong></p><p class="sa-v">空着</p></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="ws-test" style="text-align:center">▶ 接好，试跑</button>
            <button class="choice" id="ws-clear" style="text-align:center">取下重接</button>
          </div>
          <p class="result warn" id="ws-out" style="margin-top:12px">先选一个任务，再挑两张卡片。</p>
          <p class="result" id="ws-progress" style="margin-top:10px">已完成任务：0 / 3</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛠️</span><div><strong>小提示：</strong>选元件有个顺序——先问「这个任务要看住什么变化」，再问「它最后该做出什么动作」。反过来先挑熟悉的元件，很容易配不拢。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：把「天黑自动开灯」拆成四步", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>教室里的灯，天一黑就自己亮，天亮以后自己熄。请把它拆成四步，并说出每一步用到了什么元件。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>感知：</strong>光线传感器送来一个数值——现在有多亮。这是从外面拿回来的数据。</div></div>
          <div class="step"><span class="n">2</span><div><strong>判断：</strong>拿这个数和定好的标准比一比——现在是不是比标准暗了？这一步只比一比，不动手。</div></div>
          <div class="step"><span class="n">3</span><div><strong>动作：</strong>确实暗了，就接通灯的电源，让灯亮起来。这是执行元件干出来的活。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>再感知：</strong>灯亮之后，光线传感器再读一次——现在够亮了吗？够亮就熄掉，还暗就继续开着。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">漏掉第四步「再感知」，把它当成多余的动作。少了它，灯只能傻乎乎地一直亮着，或者一闪一闪停不下来。第四步是整个装置<strong>自己检查有没有把事办好</strong>的那一步。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">✏️</span><div><strong>动手画一画：</strong>在本子上画四个方框，用箭头连成一个圈，分别写上感知、判断、动作、再感知，再从箭头旁边标出用到的元件。圈画好了，这台装置才算想清楚。</div></div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "「只要装上一个传感器，装置就会自己干活了。」这句话对吗？",
         "options": [("不对，传感器只会感觉，动手还得靠执行元件", True),
                     ("对，传感器越贵装置越聪明", False),
                     ("对，传感器会自己变成执行器", False)],
         "explain": "传感器把变化读成数据，可是它不会动。少了执行元件，装置就只能看不能动。"
                    "<strong>错因提醒：</strong>常见错误是把「会感觉」当成了「会干活」——"
                    "感觉和动手是两件不同的元件干的事。"},
        {"q": "一台装置装了执行元件，却没有传感器。它最可能的表现是？",
         "options": [("能动，但不知道该什么时候动，只能等人来按开关", True),
                     ("照样能自动判断该不该动", False),
                     ("会自己猜一个数据出来用", False)],
         "explain": "没有传感器就没有数据，判断这一格什么也拿不到。执行元件只能等人下命令。"
                    "<strong>错因提醒：</strong>容易误认为「力气大就够了」——"
                    "感觉这一头空着，再大的力气也使不到点上。"},
        {"q": "为什么说完整的装置是一个「闭环」？",
         "options": [("因为做完之后还要再感知一次，看看事情有没有办成", True),
                     ("因为它的元件摆成了一个圆圈", False),
                     ("因为它一直不停地重复同一件事", False)],
         "explain": "感知、判断、动作，再加上做完之后的再感知，走完一整圈才是闭环——装置能自己检查效果。"
                    "<strong>错因提醒：</strong>容易把「再感知」当成重复劳动，"
                    "其实第一次读数据是为了决定该不该动手，第二次读是为了确认结果。"}
    ], tag="概念测试"))

    card3 = "\n".join(
        f'          <button class="sort-item" data-kind="{kind}" data-why="{why}">{t}</button>'
        for _k, t, kind, why in SR_CARDS
    )
    bin3 = "\n".join(f'''            <div class="sort-bin" data-sr-bin="{k}">
              <h4>{label}</h4>
              <div class="bin-body"></div>
            </div>''' for k, label in SR_BINS)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给智能花房配一套四步闭环", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张卡片，再点你认为对的那个格子。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待归位的八张卡片</div>
          <div class="sort-bank" id="sr-bank">
{card3}
          </div>
          <div class="sort-bins">
{bin3}
          </div>
          <p class="result warn" id="sr-out" style="margin-top:12px">点一张卡片开始归位。</p>
          <p class="result" id="sr-progress" style="margin-top:10px">已归位：0 / 8</p>
        </div>
        <div class="inner-card">
          <p><strong>放完以后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">这间智能花房要用电来抽水、点亮补光灯。如果它的感知元件被挡住了，或者判断标准写错了，会发生什么？你会怎样让它更安全、更省电？</p>
          <textarea id="syn-answer" rows="3" placeholder="如果传感器被挡住，它就会……；我会把判断标准写成……，并且……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，四步还在不在", TTS["posttest"], [
        {"q": "自动门「有人靠近就打开，人走开就关上」。这里的感知元件和执行元件分别是？",
         "options": [("距离传感器 / 驱动门开合的电机", True),
                     ("电机 / 距离传感器", False),
                     ("门框 / 门上的玻璃", False)],
         "explain": "距离传感器负责感觉「有没有人靠近」，电机负责把门推开——一个感觉，一个动手。"
                    "<strong>错因提醒：</strong>常见错误是把两者搞反。判断办法：读数据的那一头是感知，出力动手的那一头是执行。"},
        {"q": "一个装置只会响，却根本不知道外面发生了什么。它最可能缺了什么？",
         "options": [("缺感知元件，没有数据可以判断", True),
                     ("缺更大的喇叭", False),
                     ("缺一根更长的导线", False)],
         "explain": "它已经能动手了，缺的是感觉这一头。没有数据，判断这一格就是空的。"
                    "<strong>错因提醒：</strong>容易误认为「换更好的执行元件就能变聪明」——"
                    "聪明来自能拿到数据、能做出判断。"},
        {"q": "小组给花房做了自动浇花装置，还想让它更稳妥。下面哪种做法最合适？",
         "options": [("浇完水后再读一次土里的湿度，确认浇够了没有，再决定要不要停", True),
                     ("把水泵一直开着，不用担心浇多浇少", False),
                     ("把湿度传感器用布蒙起来，免得它乱读", False)],
         "explain": "在闭环里补上「再感知」，装置就能自己检查效果，该停的时候停下；一直开着既浪费水又会淹坏花，蒙住传感器等于把眼睛遮上。"
                    "<strong>错因提醒：</strong>常见的错误想法是「只要动起来就行」——"
                    "动手之后不看结果，正是最容易出问题的地方。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把感知与执行讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>两种元件：</strong>感知元件把看不见的变化变成能比较的数据；执行元件把电变成看得见的动作。一样都不能少。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>两种残缺：</strong>只有传感器没有执行器，只能看不能动；只有执行器没有传感器，能动却不知道该什么时候动。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>一条闭环：</strong>感知 → 判断 → 动作 → 再感知。最后那一步，是装置自己检查有没有把事办好。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还有一条不该忘的提醒：</strong>给装置接电线、装水泵的时候，一定要在老师的指导下动手，不在潮湿的地方碰电源。机器能替我们干很多活，但安全这一步，永远得由人把关。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「感知、判断、动作、再感知」这四个词，说清楚一盏路灯是怎样自己亮起来、又自己熄掉的。</p>
          <p style="color:var(--muted)">再动一动手：用四张纸片写上四个词，摆成一个圈，指着讲给同桌听。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出感知元件和执行元件各负责什么，各举两个生活中的例子。",
            "说说为什么「只有传感器没有执行器，就只能看不能动」。",
        ],
        [
            "找一个家里的自动装置（自动感应灯、扫地机、自动晾衣架都可以），写出它的感知元件是什么、执行元件是什么。",
            "把它的工作过程画成四步闭环：感知、判断、动作、再感知，每步各写了什么。",
        ],
        [
            "给学校设计一台自动浇花装置，写出它的感知元件、判断标准、执行元件，以及「再感知」安排在什么时候。",
            "在上面那道题里补充一条：怎样保证它不会浇太多水？如果传感器被挡住了，你会怎样提醒值班的同学？",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-sensors-actuators",
    "node_id": "it-e-sensors-actuators",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "传感与执行（初识）",
    "name_en": "Sensors and Actuators: Giving Machines Senses and Hands",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "process-control",
    "domain_cn": "过程与控制",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学六年级：认识常见传感器与执行器，知道感知元件负责把变化变成能比较的数据、执行元件负责把电变成动作；能按任务挑出合适的传感器与执行器，并理解只有传感器没有执行器就只能看不能动，把自动装置拆成感知、判断、动作、再感知的闭环。",
    "tags": ["传感器", "执行器", "过程与控制", "闭环", "元件选型", "安全用电"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「过程与控制」——认识常见传感器与执行器，体验简单控制项目。",
    "hero_question": "天黑了灯自己亮，土干了水自己浇——机器凭什么知道该动手了？",
    "hero_alt": "传感与执行知识结构图：感知元件把变化变成数据、判断照规则比一比、执行元件把电变成动作，以及四步闭环关系",
    "hero_caption": "两类元件 · 一条闭环：感知是感官 · 判断是大脑 · 执行是手脚 · 做完还要再感知",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "机器靠什么感觉到外面的变化？", "d": "它没有眼睛耳朵，怎么知道天黑了", "v": "机器靠什么感觉到外面的变化"},
        {"t": "它凭什么能把事情做出来？", "d": "感觉和数据是怎么变成动作的", "v": "它凭什么能把事情做出来"},
        {"t": "为什么有的装置只会看、不会动？", "d": "是不是元件装少了", "v": "为什么有的装置只会看不会动"},
        {"t": "怎样给一个任务配齐元件？", "d": "想亲手接一次看看能不能跑起来", "v": "怎样给一个任务配齐元件"},
    ],
    "objectives": [
        "能说出感知元件和执行元件分别负责什么，并各举出两个例子",
        "能在几个常用元件里挑出适合某个任务的传感器和执行器，并说出理由",
        "能说清楚只有传感器没有执行器就只能看不能动，只有执行器没有传感器能动却不知道该什么时候动",
        "能把一个自动装置拆成感知、判断、动作、再感知四步，说出它其实是一个闭环",
    ],
    "objectives_plain": [
        "能说出感知元件和执行元件分别负责什么，并各举出两个例子",
        "能在几个常用元件里挑出适合某个任务的传感器和执行器，并说出理由",
        "能说清楚只有传感器没有执行器就只能看不能动，只有执行器没有传感器能动却不知道该什么时候动",
        "能把一个自动装置拆成感知、判断、动作、再感知四步，说出它其实是一个闭环",
    ],
    "standards": [
        {"content": "认识常见传感器与执行器，体验简单控制项目",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 过程与控制"},
        {"content": "在真实装置中辨认感知元件与执行元件，初步建立「感知—判断—动作—再感知」的闭环意识，并形成安全用电的责任感",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 过程与控制 / 信息社会责任"},
    ],
    "prereqs": ["it-e-input-output"],
    "prereqs_name": "输入-计算-输出模型",
    "prereqs_meta": "it-e-input-output",
    "leads_to": ["it-e-feedback-control"],
    "next_meta": "it-e-feedback-control",
    "section_images": ["assets/it-e-sensors-actuators-fig1.webp", "assets/it-e-sensors-actuators-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "机器没有眼睛耳朵，它凭什么知道天黑了、土干了？答案在两种小元件里。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给一个任务配齐元件，并说清它是怎么走完一圈的。",
        "objectives": "看清四件事：两类元件各干什么、怎么给任务选元件、缺一样会怎样、四步闭环是哪四步。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "感知元件只做一件事：把看不见的变化变成能比较的数据。它不管该不该动手。",
        "lab-1": "两个口都要装满，还要和任务对得上。留意只装一个的时候会发生什么。",
        "module-2": "执行元件把电变成动作：发光、发声、转动、抽水。感觉和动手，一样都不能少。",
        "lab-2": "先问「要看住什么变化」，再问「该做出什么动作」，最后才去元件库里挑卡片。",
        "worked-example": "四步走：感知、判断、动作，最后别忘了再感知一次。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "问四句话就能分清：是感觉到的？是比出来的？是做出来的？还是做完再看一眼？",
        "posttest": "自动门、只会响的装置、还有一道安全题，看看四步闭环管不管用。",
        "summary": "三句话：两种元件、两种残缺、一条闭环。再记住一条安全提醒。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": (CUSTOM_JS
                  .replace("__WS_TASKS_JSON__", json.dumps(WS_TASKS, ensure_ascii=False))
                  .replace("__WS_CARDS_JSON__", json.dumps(WS_CARDS, ensure_ascii=False))),
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「过程与控制」里传感器与执行器的起始一课。六年级学生的难点有三处：一是把「会亮会响的元件」当成传感器，方向分不清；二是以为只要装得够多，装置就会自己干活；三是漏掉「做完之后再感知」这一步，把闭环当成单向流程。所以全课只做三件真能上手的事——先用一个元件配对台，给「天黑自动开灯」这个任务各挑一个感知元件和执行元件，通电测试会分别遇到「两个口都空着」「只有传感器没有执行器」「只有执行器没有传感器」「感觉对了动作配错」「感知元件与任务不匹配」几种失败，每一种都给出不同的错因；再用闭环小工坊，把三个任务放进同一张混装元件库里，学生必须自己判断哪张卡是感觉的、哪张是干活的，选元件时若两个口都塞了传感器，就会撞上「只能看不能动」这条判据；最后用智能花房的八张卡片，把感知、判断、动作、再感知四个格子亲手归位。概念页把两类元件收成一句口诀（感知是感官，判断是大脑，执行是手脚），并把安全用电的提醒放在小结页，不写成口号。",
    "plan_table": """| 1 | cover | 传感与执行（初识） | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：机器靠什么知道该动手了？ | 起·前测（暴露直觉） |
| 5 | concept | 感知元件：机器用来「感觉」的感官 | 承·概念一（四类传感器 + 口诀） |
| 6 | interactive | 动手一：元件配对台 | 承·动手模拟（单任务接元件 → 通电测试 → 四步点亮） |
| 7 | concept | 执行元件：机器用来「动手」的手脚 | 承·概念二（四类执行器 + 两种残缺 + 闭环图） |
| 8 | interactive | 动手二：闭环小工坊 | 承·动手模拟（三任务 + 混装元件库 + 选型错因） |
| 9 | concept | 例题示范：把「天黑自动开灯」拆成四步 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给智能花房配一套四步闭环 | 合·迁移应用（八卡四格归位 + 安全用电讨论） |
| 12 | quiz | 后测：换几个情境，四步还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把感知与执行讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：感知元件 / 判断 / 执行元件 三栏与四步闭环关系\n- P5 四类感知元件示意图（已生成）：光线、温度、距离、湿度传感器各自把变化变成数值\n- P7 闭环四步示意图（已生成）：感知 → 判断 → 动作 → 再感知\n- 三张图均为教学示意图，不涉及任何真实设备界面、截图、品牌或商标\n- 若需补充：光线传感器、小水泵等实物照片（需获得授权后使用）",
}
