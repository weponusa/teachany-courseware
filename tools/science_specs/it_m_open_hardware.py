# -*- coding: utf-8 -*-
"""初中信息科技 · 开源硬件与模块化设计（G8）—— 补齐课标「物联网与模块」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-open-hardware-fig1.webp'
F2 = './assets/it-m-open-hardware-fig2.webp'

TTS = {
    "hero": "先看一台做不成的装置。有人想给教室做一套自动补光装置，灯珠、传感器、主控板都买齐了，接上线以后灯却一会儿亮一会儿灭，换掉一个模块也没用。问题往往不在某个零件上，而在这套东西是怎么被拆成模块、又怎么被接起来的。这节课我们做两件事：把系统拆成能独立替换的模块，再用分段验证的办法把它一步一步调通。",
    "problem-anchor": "开始之前，先挑一个你最想弄明白的问题。是想知道模块之间到底靠什么约定才能互相配合，还是想知道两个模块明明都买对了，为什么接上却不工作，又或者你想亲手按顺序把一台不工作的装置查通。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出模块化设计的三条接口约定：供电、逻辑电平、通信方式，并说明为什么模块可以独立替换。第二，能按模块数量估算总电流，判断供电是否留有足够余量，并识别电流不足的典型现象。第三，能判断两个模块的逻辑电平是否匹配，知道什么时候必须使用电平转换。第四，能按电源、电平、总线、共地的顺序做分段验证，定位并排除一台不工作装置中的故障。",
    "pretest": "先做三道小题，凭现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "模块化设计的第一步，是把一套系统拆成能做独立替换的模块，再给每个模块定好接口。接口约定有三条。第一条是供电：模块要几伏、要多少毫安，能不能都从主控板上取电。第二条是逻辑电平：信号用几伏表示高电平，如果一端是五伏、另一端是三伏三，直接相接就可能读错甚至损坏器件。第三条是通信方式：用哪种总线、占用哪个地址。三条定清楚，模块才能像积木一样换。",
    "lab-1": "我们先把接口算清楚。左边选主控的逻辑电平和模块类型，右边拖动模块数量，下面会出现三个数：模块总电流、含主控的全部电流，以及余量百分比。拖到某个数量，电流会超过供电上限，仪表条会变色。再切换取电方式，看看把大电流模块改成外接电源以后，余量是不是回来了。",
    "module-2": "接对了不等于能用，工程上真正的功夫在调试。调试的核心方法是分段验证：把系统切成几段，一段一段确认，而不是一次把整套接上碰运气。顺序也很讲究——先电源，再电平，后信号，最后才看程序。为什么先电源？因为供电不对，后面所有现象都不可信。这也是分段验证最容易被忽略的一点：跳过供电，后面测到的数据全是白测。",
    "lab-2": "现在你当一次调试工程师。四个插槽，每个插槽可以装一个模块，装好以后点自检。自检会按电源、电平、总线地址、共地四条依次检查，每条都给出结论。注意看第一条不过的那一项，它必须优先解决，后面的结论暂时都不能当真。试试把两个同地址的模块装在同一条总线上，看会发生什么。",
    "worked-example": "我们一起分析一台不工作的装置。现象是：上电以后主控能启动，传感器读数却一直是零。第一步，先看电源，测量模块的供电引脚是否达到额定值，这一步排除了供电。第二步，看接线，确认信号线接到了约定的引脚，这一步发现信号线接错了位置。第三步，看电平，模块是五伏逻辑，主控是三伏三，必须加电平转换。第四步，看总线地址，两个模块地址重复，也要改开。第五步，用最简程序单独读取这个模块，确认改完以后读数正常。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次排障工程师。屏幕上给三个故障现场，你要从动作清单里按顺序挑出三步排查。系统会判定你挑的三步是不是关键项，以及顺序对不对。你会看到一条规律：几乎所有故障都该从电源查起，先隔离、再定位，最后才轮到改程序。顺序错了，花的时间会成倍增加。",
    "posttest": "最后换两个新情境检验一下。这次出现了不同逻辑电平的模块，还有一个电流吃紧的装置，看看你能不能把接口约定和分段验证用上去。",
    "summary": "这节课我们弄清楚了三件事。第一，模块化设计靠接口约定：供电、逻辑电平、通信方式，三条定清楚，模块才能独立替换。第二，逻辑电平不匹配不能直接相接，该用电平转换就必须用；总电流要留余量，大电流负载别都从主控板取电。第三，调试靠分段验证，顺序是电源、电平、信号、程序，第一条不过就不要往下。回到开头那套装置：把模块边界划清楚，再一段一段确认，它就能稳定跑起来。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出模块化设计的三条接口约定，并说明每条约定对应什么故障。第二层能力应用，动手做：为一套四模块的装置列出供电、电平、总线地址三项检查，算出总电流并判断余量。第三层迁移挑战，选做：为学校的一个真实需求设计一套模块化方案，按分段验证的顺序写出调试步骤。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 模块与接口约定", "lab-1": "实验室一 电平与电流预算台",
    "module-2": "概念二 分段验证与调试顺序", "lab-2": "实验室二 上电自检工作台",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 分段排障台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-slot { display: flex; gap: 10px; align-items: center; margin-top: 8px; flex-wrap: wrap; }
.ta-slot label { min-width: 76px; font-weight: 700; font-size: 14px; }
.ta-slot select { flex: 1; min-width: 200px; }
.ta-inline { width: auto !important; min-height: 0 !important; accent-color: var(--brand); }
.ta-check-row { display: flex; align-items: center; gap: 10px; font-size: 14px; margin-top: 10px; }
.ta-log { list-style: none; margin: 0; padding: 0; }
.ta-log li { padding: 9px 12px; margin-bottom: 6px; border-radius: 10px; font-size: 14px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); }
.ta-log li.ok { border-color: var(--ok); }
.ta-log li.no { border-color: var(--danger); }
.ta-log li.pending { opacity: .5; }
.ta-log li .ic { font-weight: 800; margin-right: 7px; }
.ta-chipset { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; min-height: 34px; }
.ta-chip { padding: 6px 12px; border-radius: 999px; font-size: 13px; font-weight: 700;
  background: var(--brand-soft); border: 1px solid var(--line-subtle); }
.ta-meter { display: flex; align-items: center; gap: 10px; margin-top: 10px; }
.ta-meter .bar { flex: 1; height: 10px; border-radius: 999px; background: var(--bg-subtle); overflow: hidden; }
.ta-meter .fill { height: 100%; width: 0; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .35s ease; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-open-hardware 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 电平与电流预算台：接口三维度换算 + Canvas 电流仪表
   3) 上电自检工作台：四插槽按「电源→电平→总线→共地」逐条判定
   4) 分段排障台：按顺序选三步排查动作并判定关键项与顺序
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 0. 主题色读取（不写死颜色，跟随学段主题） ---------- */
  function themeColor(name, fb) {
    try {
      var v = getComputedStyle(document.body).getPropertyValue(name).trim();
      return v || fb;
    } catch (e) { return fb; }
  }
  function rr(ctx, x, y, w, h, r) {
    if (w < 2 * r) r = w / 2;
    if (h < 2 * r) r = h / 2;
    ctx.beginPath();
    ctx.moveTo(x + r, y);
    ctx.arcTo(x + w, y, x + w, y + h, r);
    ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r);
    ctx.arcTo(x, y, x + w, y, r);
    ctx.closePath();
  }

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

  /* ---------- 2. 电平与电流预算台 ---------- */
  var BOARD_SELF = 75;            /* 主控自身工作电流 mA */
  var LOGIC = {
    l33: { v: '3.3 V', n: '3.3 V' },
    l5:  { v: '5 V',   n: '5 V' }
  };
  var MODT = {
    s33:   { n: '3.3 V 传感模块', vcc: '3.3 V', lv: 'l33', cur: 18 },
    s5:    { n: '5 V 传感模块',   vcc: '5 V',   lv: 'l5',  cur: 26 },
    relay: { n: '5 V 执行模块',   vcc: '5 V',   lv: 'l5',  cur: 150 },
    radio: { n: '3.3 V 通信模块', vcc: '3.3 V', lv: 'l33', cur: 45 }
  };
  var SUPPLY = { onboard: { n: '主控板载稳压', cap: 500 }, ext: { n: '外接独立电源', cap: 2000 } };

  var stage1 = document.getElementById('hw1-stage');
  if (stage1) {
    var eLogic = document.getElementById('hw1-logic');
    var eMod = document.getElementById('hw1-mod');
    var eNum = document.getElementById('hw1-num');
    var eSup = document.getElementById('hw1-sup');
    var eConv = document.getElementById('hw1-conv');
    var eNumV = document.getElementById('hw1-num-val');
    var eModCur = document.getElementById('hw1-modcur');
    var eTotal = document.getElementById('hw1-total');
    var eCap = document.getElementById('hw1-cap');
    var eMargin = document.getElementById('hw1-margin');
    var eOut1 = document.getElementById('hw1-out');

    function drawGauge(ratio, state) {
      var cv = document.getElementById('hw-gauge');
      if (!cv || !cv.getContext) return;
      var ctx = cv.getContext('2d');
      var W = cv.width, H = cv.height;
      ctx.clearRect(0, 0, W, H);
      var x0 = 14, x1 = W - 14, barY = 50, barH = 26;
      var safeX = x0 + (x1 - x0) * 0.8;

      ctx.fillStyle = themeColor('--bg-subtle', '#eef2f7');
      rr(ctx, x0, barY, x1 - x0, barH, 13); ctx.fill();

      var fillW = Math.max(0, Math.min(1, ratio)) * (x1 - x0);
      ctx.fillStyle = (state === 'error' ? themeColor('--danger', '#ef4444')
                    : state === 'warn' ? themeColor('--warm', '#f59e0b')
                    : themeColor('--brand', '#3b82f6'));
      rr(ctx, x0, barY, Math.max(fillW, 5), barH, 13); ctx.fill();

      ctx.strokeStyle = themeColor('--warm', '#f59e0b');
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(safeX, barY - 7);
      ctx.lineTo(safeX, barY + barH + 7);
      ctx.stroke();

      ctx.font = '700 15px -apple-system, "PingFang SC", sans-serif';
      ctx.textAlign = 'left';
      ctx.fillStyle = themeColor('--text-secondary', '#475569');
      ctx.fillText('供电占用', x0, barY - 16);
      ctx.fillStyle = themeColor('--warm-deep', '#b45309');
      ctx.textAlign = 'right';
      ctx.fillText('建议余量线 80%', safeX, barY - 16);
      ctx.fillStyle = themeColor('--text-secondary', '#475569');
      ctx.fillText(Math.round(ratio * 100) + '%', x1, barY - 16);

      ctx.textAlign = 'left';
      ctx.font = '500 13px -apple-system, "PingFang SC", sans-serif';
      ctx.fillStyle = themeColor('--muted', '#64748b');
      ctx.fillText('横条＝已用电流 / 供电上限；越过橙色刻度就说明余量不足，越过右端就是超载。', x0, barY + barH + 32);
    }

    function render1() {
      var logic = eLogic.value;
      var mod = MODT[eMod.value];
      var n = Number(eNum.value);
      var sup = SUPPLY[eSup.value];
      var conv = eConv.checked;

      eNumV.textContent = n + ' 个';
      eModCur.textContent = mod.cur + ' mA';

      var modTotal = mod.cur * n;
      var total = BOARD_SELF + modTotal;
      var ratio = total / sup.cap;
      var margin = Math.round((1 - ratio) * 100);

      eTotal.textContent = total + ' mA';
      eCap.textContent = sup.cap + ' mA';
      eMargin.textContent = margin + ' %';

      var levelOk = (mod.lv === logic) || conv;
      var powerState = ratio > 1 ? 'error' : (ratio > 0.8 ? 'warn' : 'ok');
      drawGauge(ratio, powerState === 'ok' ? 'ok' : powerState);

      var parts = [];
      parts.push('<strong>' + sup.n + '、' + n + ' 个' + mod.n + '的账：</strong>模块共 ' + modTotal +
        ' mA，加上主控自身的 ' + BOARD_SELF + ' mA，合计 ' + total + ' mA；上限 ' + sup.cap +
        ' mA，余量 ' + margin + '%。');

      if (ratio > 1) {
        parts.push('<strong>已经超载：</strong>电流超过供电上限，典型现象是电压被拉低，主控反复重启、模块时好时坏。常见错误是只算电压不算电流——' +
          '误认为「标称输出电压对上就行」。两个办法：把大电流模块改成外接独立电源，或者减少同时工作的模块数量。');
      } else if (ratio > 0.8) {
        parts.push('<strong>余量不足：</strong>虽然还没超载，但已经越过建议余量线。' +
          '执行模块在启动的瞬间电流会比平时大不少，余量太薄就容易出现「一动就重启」。');
      } else {
        parts.push('<strong>供电这一项过关：</strong>余量在建议范围内，执行模块启动时的瞬时电流也吃得下。');
      }

      if (levelOk) {
        parts.push('电平这一项：' + (mod.lv === logic
          ? '模块与主控都是 ' + LOGIC[logic].n + ' 逻辑，信号可以直接相接。'
          : '模块是 ' + LOGIC[mod.lv].n + ' 逻辑、主控是 ' + LOGIC[logic].n +
            ' 逻辑，你已声明使用电平转换，这一项过关。'));
      } else {
        parts.push('<strong>电平不匹配：</strong>模块是 ' + LOGIC[mod.lv].n + ' 逻辑，主控是 ' + LOGIC[logic].n +
          ' 逻辑。直接相接时，高电平可能被误判成低电平，长期还可能损坏器件。常见错误是把「电压都接对了」当成「信号也能通」——' +
          '供电和信号是两条独立的约定，必须分别核对，该加电平转换就必须加。');
      }
      parts.push('<strong>易错点：</strong>接口约定有三条——供电、电平、通信。漏掉任何一条，装置都可能「看起来接对了却不工作」。');

      eOut1.className = 'result ' + (ratio > 1 || !levelOk ? 'error' : (ratio > 0.8 ? 'warn' : ''));
      eOut1.innerHTML = parts.join('<br>');
    }
    eLogic.addEventListener('change', render1);
    eMod.addEventListener('change', render1);
    eNum.addEventListener('input', render1);
    eSup.addEventListener('change', render1);
    eConv.addEventListener('change', render1);
    render1();
  }

  /* ---------- 3. 上电自检工作台 ---------- */
  var SLOTMOD = {
    none:  { n: '未安装', cur: 0, lv: null,  addr: null,  bus: false },
    s33:   { n: '3.3 V 传感模块（总线，地址 0x48）', cur: 18,  lv: 'l33', addr: '0x48', bus: true },
    s5:    { n: '5 V 传感模块（总线，地址 0x48）',   cur: 26,  lv: 'l5',  addr: '0x48', bus: true },
    s5w:   { n: '5 V 传感模块（独立信号线）',        cur: 30,  lv: 'l5',  addr: null,   bus: false },
    relay: { n: '5 V 执行模块（继电器）',            cur: 150, lv: 'l5',  addr: null,   bus: false },
    c48:   { n: '3.3 V 通信模块（总线，地址 0x48）', cur: 45,  lv: 'l33', addr: '0x48', bus: true },
    c4a:   { n: '3.3 V 通信模块（总线，地址 0x4A）', cur: 45,  lv: 'l33', addr: '0x4A', bus: true }
  };
  var BOARD_LV = 'l33';      /* 主控逻辑电平：3.3 V */
  var BOARD_CAP = 500;       /* 板载 5 V 稳压上限 mA */

  var stage2 = document.getElementById('hw2-stage');
  if (stage2) {
    var eConv2 = document.getElementById('hw2-conv');
    var eGnd = document.getElementById('hw2-gnd');
    var eLog = document.getElementById('hw2-log');
    var eOut2 = document.getElementById('hw2-out');

    function pickSlots() {
      var picked = [];
      for (var i = 1; i <= 4; i++) {
        var el = document.getElementById('hw-slot-' + i);
        if (!el) continue;
        var k = el.value;
        if (k !== 'none') picked.push({ k: k, m: SLOTMOD[k] });
      }
      return picked;
    }

    function selfCheck() {
      var picked = pickSlots();
      var conv = eConv2.checked;
      var gnd = eGnd.checked;
      var rows = [];
      var firstFail = -1;

      /* ① 电源 */
      var total = BOARD_SELF;
      picked.forEach(function (p) { total += p.m.cur; });
      var pOk = total <= BOARD_CAP;
      rows.push({
        ok: pOk,
        t: '电源：全部模块共 ' + total + ' mA（含主控 ' + BOARD_SELF + ' mA），板载上限 ' + BOARD_CAP + ' mA。' +
          (pOk ? '没有超载' : '已超载——典型现象是主控反复重启、模块时好时坏'),
        hint: pOk ? '' : '优先解决：把大电流模块改用外接独立电源，或减少同时工作的模块。'
      });
      if (!pOk && firstFail < 0) firstFail = rows.length - 1;

      /* ② 电平 */
      var badLv = picked.filter(function (p) { return p.m.lv !== BOARD_LV; });
      var lOk = badLv.length === 0 || conv;
      rows.push({
        ok: lOk,
        t: '逻辑电平：主控是 3.3 V 逻辑，' +
          (badLv.length === 0 ? '已装模块全部匹配' : '有 ' + badLv.length + ' 个模块是 5 V 逻辑') +
          (badLv.length ? (conv ? '，你已声明使用电平转换' : '，且未使用电平转换') : ''),
        hint: lOk ? '' : '优先解决：给 5 V 逻辑的模块加电平转换，或换成 3.3 V 逻辑的模块。'
      });
      if (!lOk && firstFail < 0) firstFail = rows.length - 1;

      /* ③ 总线地址 */
      var seen = {}, dup = [];
      picked.forEach(function (p) {
        if (!p.m.bus || !p.m.addr) return;
        if (seen[p.m.addr]) dup.push(p.m.addr);
        else seen[p.m.addr] = 1;
      });
      var aOk = dup.length === 0;
      rows.push({
        ok: aOk,
        t: '总线地址：同一条总线上 ' +
          (aOk ? '没有重复地址（已占用：' + (Object.keys(seen).join('、') || '无') + '）'
               : '出现重复地址 ' + dup.join('、') + '，两个模块会同时应答，读数必然错乱'),
        hint: aOk ? '' : '优先解决：把其中一个模块的地址改成可选择的其他地址（例如 0x4A）。'
      });
      if (!aOk && firstFail < 0) firstFail = rows.length - 1;

      /* ④ 共地 */
      rows.push({
        ok: gnd,
        t: '共地：' + (gnd ? '已声明全部模块与主控共地' : '尚未确认所有模块与主控共地'),
        hint: gnd ? '' : '优先解决：把各模块的接地引脚与主控接在一起。没有公共参考点，电压高低就没有意义。'
      });
      if (!gnd && firstFail < 0) firstFail = rows.length - 1;

      eLog.innerHTML = '';
      rows.forEach(function (r, i) {
        var li = document.createElement('li');
        li.className = r.ok ? 'ok' : 'no';
        li.innerHTML = '<span class="ic">' + (r.ok ? '✅' : '❌') + '</span>' + r.t +
          (r.hint ? '<br><span style="color:var(--danger)">' + r.hint + '</span>' : '') +
          (i > firstFail && firstFail >= 0 ? '<br><span style="color:var(--muted)">提示：前面那一项还没过，这条结论暂时不能当真。</span>' : '');
        eLog.appendChild(li);
      });

      var pass = firstFail < 0;
      eOut2.className = 'result ' + (pass ? '' : 'error');
      if (pass) {
        eOut2.innerHTML = '<strong>自检通过：可以上电了。</strong>供电、电平、总线地址、共地四项都对得上。' +
          '接下来才是加载程序、读取数据；这一步之前的所有排查，都是为了不让「带病上电」把器件烧掉。';
      } else {
        eOut2.innerHTML = '<strong>自检不通过：从上往下第一条标红的就是要先解决的那一项。</strong>它后面的结论先不要看。' +
          '常见错误是跳过供电和共地，直接去改程序——' +
          '误认为「程序改了就好了」，可实际上信号连参考点都没有，程序再对也读不到正确的数。';
      }
    }
    document.getElementById('hw2-run').addEventListener('click', selfCheck);
    document.getElementById('hw2-reset').addEventListener('click', function () {
      for (var i = 1; i <= 4; i++) {
        var el = document.getElementById('hw-slot-' + i);
        if (el) el.value = (i === 1 ? 's33' : 'none');
      }
      eConv2.checked = false;
      eGnd.checked = false;
      eLog.innerHTML = '';
      eOut2.className = 'result warn';
      eOut2.textContent = '模块装好、下面的两项确认好之后，点「上电自检」。';
    });
  }

  /* ---------- 4. 分段排障台 ---------- */
  var ACT = {
    power: { n: '测量模块供电引脚是否达到额定电压', cat: '电源' },
    cur:   { n: '核对电源额定电流与全部模块总电流（含启动瞬时）', cat: '电源' },
    gnd:   { n: '确认所有模块与主控共地', cat: '连接' },
    iso:   { n: '逐个断开模块，看现象是否消失', cat: '隔离' },
    pin:   { n: '检查信号线是否接到了约定的引脚', cat: '信号' },
    level: { n: '检查两边模块的逻辑电平是否匹配', cat: '信号' },
    addr:  { n: '检查同一总线上的模块地址是否重复', cat: '信号' },
    unit:  { n: '用最简程序单独读取或驱动该模块', cat: '单元' },
    prog:  { n: '先重写主程序逻辑', cat: '程序' }
  };
  var SCEN = {
    dead: {
      n: '上电后整块装置毫无反应，指示灯不亮',
      prio: ['power', 'gnd', 'iso'],
      why: '先确认电到底有没有送到，再看有没有公共参考点，最后用隔离缩小范围。信号层的检查都排在后面。'
    },
    zero: {
      n: '主控能启动，但传感器读数始终是零',
      prio: ['power', 'pin', 'level'],
      why: '读数恒为零，说明「没有有效信号」。先确认模块本身有没有拿到电，再确认信号线接在哪、电平对不对。'
    },
    blink: {
      n: '执行模块动作一下就停，反复如此',
      prio: ['cur', 'gnd', 'iso'],
      why: '「一动就停」是典型的供电被拉低：先算电流够不够，再确认共地，最后隔离出到底是哪个模块拖垮了电压。'
    }
  };
  var stage4 = document.getElementById('ps-stage');
  if (stage4) {
    var seqScen = 'dead';
    var seq = [];

    function renderSeq() {
      var S = SCEN[seqScen];
      document.getElementById('ps-brief').innerHTML = '<strong>故障现场：' + S.n +
        '</strong>　请按顺序挑出三步排查动作（已选 ' + seq.length + ' / 3）';
      var holder = document.getElementById('ps-seq');
      holder.innerHTML = '';
      if (seq.length === 0) {
        holder.innerHTML = '<span style="color:var(--muted);font-size:13px">还没有选择动作。按你认为合理的顺序，从下面点选三步。</span>';
      }
      seq.forEach(function (k, i) {
        var s = document.createElement('span');
        s.className = 'ta-chip';
        s.textContent = (i + 1) + '. ' + ACT[k].n + '（' + ACT[k].cat + '）';
        holder.appendChild(s);
      });
      document.querySelectorAll('[data-ps-act]').forEach(function (b) {
        var k = b.getAttribute('data-ps-act');
        b.classList.toggle('selected', seq.indexOf(k) >= 0);
      });
    }

    document.querySelectorAll('[data-ps-scen]').forEach(function (b) {
      b.addEventListener('click', function () {
        seqScen = b.getAttribute('data-ps-scen');
        seq = [];
        document.querySelectorAll('[data-ps-scen]').forEach(function (x) {
          x.classList.toggle('selected', x === b);
        });
        document.getElementById('ps-out').className = 'result warn';
        document.getElementById('ps-out').textContent = '顺序挑好三步之后，点「提交排查方案」。';
        renderSeq();
      });
    });
    document.querySelectorAll('[data-ps-act]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.getAttribute('data-ps-act');
        var i = seq.indexOf(k);
        if (i >= 0) { seq.splice(i, 1); }
        else if (seq.length < 3) { seq.push(k); }
        else {
          var out = document.getElementById('ps-out');
          out.className = 'result warn';
          out.textContent = '已经选满三步了。想换的话，先点掉上面某个动作。';
          return;
        }
        renderSeq();
      });
    });
    document.getElementById('ps-clear').addEventListener('click', function () {
      seq = [];
      renderSeq();
      document.getElementById('ps-out').className = 'result warn';
      document.getElementById('ps-out').textContent = '顺序挑好三步之后，点「提交排查方案」。';
    });

    document.getElementById('ps-run').addEventListener('click', function () {
      var S = SCEN[seqScen];
      var out = document.getElementById('ps-out');
      if (seq.length < 3) {
        out.className = 'result warn';
        out.textContent = '还差 ' + (3 - seq.length) + ' 步。请按顺序挑满三步再提交。';
        return;
      }
      var hits = seq.filter(function (k) { return S.prio.indexOf(k) >= 0; }).length;
      var orderOk = hits === 3 && seq.every(function (k, i) { return S.prio.indexOf(k) === i; });
      var rows = [];

      seq.forEach(function (k, i) {
        var pos = S.prio.indexOf(k);
        var ok = pos >= 0;
        var extra = '';
        if (!ok) {
          extra = k === 'prog'
            ? '这一步放在最后才有意义，一上来就重写程序，等于跳过了电源和接线两段。'
            : '这一步在本次故障里不是关键项，先做完关键项再回来看它。';
        }
        rows.push('<li class="' + (ok ? 'ok' : 'no') + '"><span class="ic">' + (ok ? '✅' : '❌') + '</span>第 ' +
          (i + 1) + ' 步　' + ACT[k].n + '<br><span style="color:var(--muted)">' +
          (ok ? '命中关键项' + (orderOk ? '，位置也对' : '，但建议的顺序是第 ' + (pos + 1) + ' 步') : extra) + '</span></li>');
      });
      S.prio.forEach(function (k, i) {
        if (seq.indexOf(k) < 0) {
          rows.push('<li><span class="ic">＋</span>漏掉的关键项（应在第 ' + (i + 1) + ' 步）：' + ACT[k].n + '</li>');
        }
      });

      var score = hits + (orderOk ? 1 : 0);
      out.className = 'result ' + (score >= 4 ? '' : 'error');
      out.innerHTML = '<strong>判定：关键项命中 ' + hits + ' / 3' +
        '，顺序' + (orderOk ? '正确' : '需要调整') + '，合计 ' + score + ' / 4。</strong>' +
        '<div class="ta-meter"><div class="bar"><div class="fill" style="width:' + (score * 25) + '%"></div></div><span>' +
        (score * 25) + '%</span></div>' +
        '<br><ul class="ta-log">' + rows.join('') + '</ul>' +
        '<strong>推荐的排查顺序：</strong>' + S.prio.map(function (k, i) { return (i + 1) + '. ' + ACT[k].n; }).join('　') +
        '。' + S.why +
        '<br><strong>易错点：</strong>常见错误是凭感觉挑自己最熟的那一步。' +
        '分段验证的顺序是有道理的——电源决定成败，隔离负责缩小范围，程序永远排在最后。' +
        '顺序错了，不是查不出来，而是要多花好几倍的时间。';
    });
    renderSeq();
  }
})();
"""


def _slots_html():
    mods = [
        ("none", "未安装"),
        ("s33", "3.3 V 传感模块（总线，地址 0x48）"),
        ("s5", "5 V 传感模块（总线，地址 0x48）"),
        ("s5w", "5 V 传感模块（独立信号线）"),
        ("relay", "5 V 执行模块（继电器）"),
        ("c48", "3.3 V 通信模块（总线，地址 0x48）"),
        ("c4a", "3.3 V 通信模块（总线，地址 0x4A）"),
    ]
    rows = []
    for i in range(1, 5):
        opts = "".join(
            f'<option value="{v}"{" selected" if (i == 1 and v == "s33") else ""}>{n}</option>'
            for v, n in mods
        )
        rows.append(f'''          <div class="ta-slot">
            <label for="hw-slot-{i}">插槽 {i}</label>
            <select id="hw-slot-{i}">{opts}</select>
          </div>''')
    return "\n".join(rows)


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：一条线接错，为什么整套都不工作？", TTS["pretest"], [
        {"q": "把一个模块接到主控板上，除了供电和地线，还必须核对的一件事是：",
         "options": [("模块的逻辑电平与主控是否一致", True),
                     ("模块外壳的颜色", False),
                     ("模块出厂时贴的编号", False)],
         "explain": "供电、逻辑电平、通信方式，是模块之间必须约定的三条接口。信号用几伏表示高电平，直接决定能不能互通。<strong>错因提醒：</strong>常见错误是误认为「电压接对了信号就能通」——供电和信号是两条独立的约定，必须分别核对。"},
        {"q": "四个模块各要 150 mA，主控自身 75 mA，板载稳压上限 500 mA。这套装置的问题是：",
         "options": [("总电流 675 mA 已经超载，会出现主控重启、模块时好时坏", True),
                     ("总电流只有 150 mA，完全没有问题", False),
                     ("只要把所有模块都接到同一个电源上，电流就会自动变小", False)],
         "explain": "总电流要按全部模块相加来算，再和供电上限比较。超载的典型现象是电压被拉低导致主控反复重启。<strong>错因提醒：</strong>容易搞混的是只算一个模块的电流——功耗预算永远算「全部同时工作」的总和，还要留出余量。"},
        {"q": "一台装置不工作，下面哪种排查顺序更省时间？",
         "options": [("先确认供电，再确认接线与电平，最后才改程序", True),
                     ("先重写一遍程序，不行再看硬件", False),
                     ("把整套拆掉，从零重新接一遍", False)],
         "explain": "这就是分段验证：按电源、电平、信号、程序的顺序逐段确认。供电不对，后面的现象都不可信。<strong>错因提醒：</strong>许多同学误认为「改程序最快」，可信号连参考点都没有时，程序再对也读不到正确的数。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "模块能独立替换，靠的是三条接口约定", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道物联网由感知、网络、应用三层组成，也认识了常见传感器和执行器。但真正动手时，你会发现零件都买对了却接不起来，<strong>所以</strong>我们需要先给每个模块定好接口约定，再谈怎么搭。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">模块化设计的要点是<strong>把系统切成能独立替换的模块</strong>。切得开不够，还要约定得清楚——约定一旦明确，坏掉的模块直接换掉，边界好的模块还能搬到别的项目里复用。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>供电约定：</strong>模块要几伏、工作电流多少，能不能都从主控板取电。这是「有没有电」的问题。</div></div>
          <div class="step"><span class="n">2</span><div><strong>逻辑电平约定：</strong>信号用几伏表示高电平。一端 5 V、一端 3.3 V 直接相接，会被误判，长期还可能损坏器件。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>通信约定：</strong>走哪条总线、占用哪个地址、按什么时序收发。同一条总线上地址不能重复。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="模块化系统结构示意图：主控模块与输入模块、输出模块、电源模块之间的接口约定">
          <figcaption>主控 + 输入模块 + 输出模块 + 电源模块：每条连线都要回答供电、电平、通信三个问题</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧩</span><div><strong>记忆锚点：</strong>把模块化想成拼插积木。积木能拼在一起，不是因为形状好看，而是因为凸点和凹槽的尺寸被约定了。接口约定就是模块的「凸点尺寸」——看不见，但决定了能不能拼上。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一套功能可以切成不同粒度的模块。切得越细越容易替换，但接口数量也越多，出错的机会跟着增加。"},
    {"lens": "拆开它", "text": "任意一条模块间连线都能拆成三个问题：电从哪来、信号的高低用什么电压表示、数据怎么传。三个问题都答上，这条线才算设计完。"},
    {"lens": "迁移它", "text": "这种「先定接口再各自实现」的做法到处都在用：充电线与插头的标准、打印机的驱动接口、团队协作里的分工约定。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "电平与电流预算台：这套接口到底能不能直连？", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">切换主控逻辑电平与模块类型，拖动模块数量，看电流余量与电平匹配怎么同时说话。</p>
        <div class="lab-panel">
          <div id="hw1-stage">
            <div class="ta-slot">
              <label for="hw1-logic">主控逻辑电平</label>
              <select id="hw1-logic">
                <option value="l33" selected>3.3 V 逻辑</option>
                <option value="l5">5 V 逻辑</option>
              </select>
            </div>
            <div class="ta-slot">
              <label for="hw1-mod">模块类型</label>
              <select id="hw1-mod">
                <option value="s33" selected>3.3 V 传感模块</option>
                <option value="s5">5 V 传感模块</option>
                <option value="relay">5 V 执行模块</option>
                <option value="radio">3.3 V 通信模块</option>
              </select>
            </div>
            <div class="ta-slot">
              <label for="hw1-sup">取电方式</label>
              <select id="hw1-sup">
                <option value="onboard" selected>主控板载稳压（上限 500 mA）</option>
                <option value="ext">外接独立电源（上限 2000 mA）</option>
              </select>
            </div>
            <div class="slider-row">
              <label for="hw1-num">模块数量</label>
              <input type="range" id="hw1-num" min="1" max="6" step="1" value="2">
              <span class="readout-cell" style="flex:0 0 96px"><span class="k">数量</span><span class="v" id="hw1-num-val">2 个</span></span>
            </div>
            <div class="ta-check-row">
              <input type="checkbox" class="ta-inline" id="hw1-conv">
              <label for="hw1-conv">已为不匹配的模块加装电平转换</label>
            </div>
          </div>
          <canvas id="hw-gauge" width="680" height="128" aria-label="供电占用仪表" style="display:block;width:100%;border-radius:12px;background:var(--card);"></canvas>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">单个模块电流</span><span class="v" id="hw1-modcur">—</span></div>
            <div class="readout-cell"><span class="k">全部电流（含主控）</span><span class="v" id="hw1-total">—</span></div>
            <div class="readout-cell"><span class="k">供电上限</span><span class="v" id="hw1-cap">—</span></div>
            <div class="readout-cell"><span class="k">电流余量</span><span class="v green" id="hw1-margin">—</span></div>
          </div>
          <p class="result warn" id="hw1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔎</span><div><strong>试出边界：</strong>把模块类型换成 5 V 执行模块、数量拖到 4 个，看仪表条越过右端时会发生什么；再把取电方式换掉，看余量是不是回来了。同一批模块，取电方式不同，结论完全不同。</div></div>
    ''', tag="设计实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "分段验证：调试是有顺序的", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>接对了不等于能用。</strong>工程上真正的功夫在调试：把系统切成几段，一段一段确认，而不是一次把整套接上碰运气。这个方法叫<strong>分段验证</strong>。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>为什么先查电源？</strong></p>
            <p style="color:var(--muted)">供电不对，后面测到的所有现象都不可信：读数可能是随机的，动作可能是抽搐的。</p>
          </div>
          <div class="inner-card">
            <p><strong>为什么要分段？</strong></p>
            <p style="color:var(--muted)">整套一起查，错误会互相掩盖；切成段以后，能确定问题在哪一段，再往下切。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="分段验证调试流程图：电源、电平、总线地址、共地四个阶段依次确认">
          <figcaption>分段验证的基本顺序：电源 → 逻辑电平 → 总线地址 → 共地 → 单元程序，前一段不过就不往下走</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易搞混的是<strong>把「分段」当成「分模块」</strong>：分段验证要求的是按<strong>电气条件</strong>依次确认，不是按模块逐个试。另一个常见错误是<strong>一次改多处</strong>——同时换了模块、改了程序、重接了线，现象变了也不知道是哪一步起的作用。分段验证的规矩是：一次只改一个地方。</p>
        </div>
{insight_box([
    {"lens": "解释它", "text": "调试的本质是把「整套不工作」这个大问题，切成一串只能回答是或否的小问题。每答完一个，可能的原因就少一批。"},
    {"lens": "比较它", "text": "「一次只改一处」看起来慢，实际比反复瞎换快得多：它保证每一次改动都能得到一条可信的结论。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "上电自检工作台：装好模块，按顺序查一遍", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">四个插槽各装一个模块，确认下面两项，然后点上电自检。自检会按电源、电平、总线地址、共地四条依次判定。</p>
        <div class="lab-panel">
          <div id="hw2-stage">
{_slots_html()}
            <div class="ta-check-row">
              <input type="checkbox" class="ta-inline" id="hw2-conv">
              <label for="hw2-conv">已为 5 V 逻辑的模块加装电平转换</label>
            </div>
            <div class="ta-check-row">
              <input type="checkbox" class="ta-inline" id="hw2-gnd">
              <label for="hw2-gnd">已确认全部模块与主控共地</label>
            </div>
          </div>
          <p style="margin:14px 0 6px;font-weight:700;font-size:14px">上电自检结论（自上而下逐条判定）</p>
          <ul class="ta-log" id="hw2-log"><li class="pending">还没开始自检。装好模块后点下面的按钮。</li></ul>
          <p class="result warn" id="hw2-out" style="margin-top:12px">模块装好、下面的两项确认好之后，点「上电自检」。</p>
          <div class="flex-row">
            <button class="choice" id="hw2-run" style="text-align:center;flex:1">上电自检</button>
            <button class="choice" id="hw2-reset" style="text-align:center;flex:1">恢复初始</button>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>试着造一个故障：</strong>把插槽 2 也换成带总线的模块，地址就会重复，看看自检怎么定位它；再换成地址可选的另一个模块，看结论怎么变。你会体会到：工程排查靠的不是运气，而是一张有顺序的检查表。</div></div>
    ''', tag="设计实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：读数一直是零，怎么一段段查出来？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>一套装置的故障现象是「上电后主控能启动，但传感器读数一直是零」。请按分段验证的顺序列出排查步骤，并说明每一步在排除什么。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先确认供电：</strong>用仪表测量模块供电引脚，看是否达到额定电压。这一步排除「有没有电」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再看接线：</strong>读数恒为零往往是信号根本没进来。核对信号线是否接在约定的引脚上，这一步排除接错位置。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>然后看电平：</strong>模块是 5 V 逻辑、主控是 3.3 V 逻辑，高电平识别不了，必须加电平转换。</div></div>
          <div class="step"><span class="n">4</span><div><strong>接着看总线：</strong>两个模块地址重复会同时应答，读数自然错乱，要把其中一个改成其他可选地址。</div></div>
          <div class="step"><span class="n">5</span><div><strong>最后用单元程序验证：</strong>只读这一个模块，读数正常，说明前面几步的改动真正起了作用；而不是一次性全改，说不清是哪一步解决的。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学误认为<strong>「读数不对一定是程序写错了」</strong>，于是先去改程序。可读数恒为零，恰恰是最典型的硬件侧现象：没供电、线接错、电平不匹配、地址冲突，都会产生同一个现象。另一个容易搞混的地方是<strong>跳过供电直接查信号</strong>——供电这一段的结论没拿到，后面每一步的结论都是悬空的。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("模块能不能独立替换，取决于接口约定是否清楚", True),
                     ("只要买到同一个厂家的模块，接口就一定匹配", False),
                     ("模块化设计就是把所有功能都做进一个模块里", False)],
         "explain": "接口约定清楚，模块才能换、才能复用。<strong>错因提醒：</strong>常见错误是误认为「同来源的模块自动兼容」——供电、电平、通信三条约定必须逐条核对。"},
        {"q": "总电流已经接近供电上限，装置表现出「执行模块一动，主控就重启」。最合理的做法是：",
         "options": [("把大电流模块改用外接独立电源，并保留足够余量", True),
                     ("把供电上限的数值在程序里改大一点", False),
                     ("把执行模块的启动时间改短", False)],
         "explain": "启动瞬间电流更大，余量不足就会被拉低电压。改参数不能凭空造出电流。<strong>错因提醒：</strong>容易搞混的是把供电问题当成程序问题——电流不够是硬件预算的问题，改程序只是把故障掩盖过去。"},
        {"q": "两个模块都装在一条总线上，读数有时正确有时错乱。最该先查的是：",
         "options": [("两个模块的总线地址是否重复", True),
                     ("模块的外壳是否固定牢靠", False),
                     ("主控的运行速度是否够快", False)],
         "explain": "同一条总线上地址重复，两个模块会同时应答，读数就会时好时坏。<strong>错因提醒：</strong>许多同学误认为「时好时坏就是接触不良」——信号层的地址冲突也会产生一模一样的不稳定现象。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次排障工程师，按顺序把故障查通", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">先选一个故障现场，再从动作清单里按你认为合理的顺序挑三步，然后提交判定。</p>
        <div class="lab-panel">
          <div id="ps-stage">
            <p class="result warn" id="ps-brief" style="margin:0 0 14px"></p>
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选择故障现场</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice selected" data-ps-scen="dead" style="text-align:center">整块装置毫无反应</button>
              <button class="choice" data-ps-scen="zero" style="text-align:center">传感器读数始终是零</button>
              <button class="choice" data-ps-scen="blink" style="text-align:center">执行模块一动就停</button>
            </div>
            <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 按顺序挑三步排查动作</div>
            <div class="flex-row" style="margin-top:0">
              <button class="choice" data-ps-act="power" style="text-align:center">测量供电引脚电压</button>
              <button class="choice" data-ps-act="cur" style="text-align:center">核对总电流与供电上限</button>
              <button class="choice" data-ps-act="gnd" style="text-align:center">确认模块与主控共地</button>
              <button class="choice" data-ps-act="iso" style="text-align:center">逐个断开模块做隔离</button>
              <button class="choice" data-ps-act="pin" style="text-align:center">核对信号线接的引脚</button>
              <button class="choice" data-ps-act="level" style="text-align:center">核对逻辑电平是否匹配</button>
              <button class="choice" data-ps-act="addr" style="text-align:center">核对总线地址是否重复</button>
              <button class="choice" data-ps-act="unit" style="text-align:center">用最简程序单独测该模块</button>
              <button class="choice" data-ps-act="prog" style="text-align:center">先重写主程序逻辑</button>
            </div>
            <p style="margin:14px 0 0;font-weight:700;font-size:14px">③ 你选的排查顺序</p>
            <div class="ta-chipset" id="ps-seq"></div>
          </div>
          <p class="result warn" id="ps-out" style="margin-top:12px">顺序挑好三步之后，点「提交排查方案」。</p>
          <div class="flex-row">
            <button class="choice" id="ps-run" style="text-align:center;flex:1">提交排查方案</button>
            <button class="choice" id="ps-clear" style="text-align:center;flex:1">清空重选</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>如果第一步就跳过了供电，后面每一步的结论为什么会变得不可信？</p>
          <textarea id="syn-answer" rows="3" placeholder="因为供电不正常时，读数和现象都可能是随机的，所以……必须先让第一段的结论成立，再……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "装置里有一个 5 V 逻辑的模块，主控是 3.3 V 逻辑。下面哪种判断最站得住脚？",
         "options": [("必须加电平转换，否则高电平可能被误判，长期还可能损坏器件", True),
                     ("只要供电电压都是 5 V，信号就一定能通", False),
                     ("把主控的逻辑电平在程序里改成 5 V 就行", False)],
         "explain": "逻辑电平是硬件属性，程序改不了。供电和信号是两条独立的约定。<strong>错因提醒：</strong>常见错误是把「供电对上」当成「信号能通」——这两件事必须分别核对。"},
        {"q": "一台装置要同时驱动三个继电器模块，每个 150 mA，主控自身 75 mA。下面哪种做法最稳妥？",
         "options": [("把继电器模块改由外接独立电源供电，主控只负责控制信号", True),
                     ("从主控板载取电，因为标称上限够用", False),
                     ("把程序里的动作错开一毫秒，电流就会变小", False)],
         "explain": "总电流 525 mA 已超过板载 500 mA 上限，且启动瞬间电流更大，必须外接电源。<strong>错因提醒：</strong>容易搞混的是「标称上限等于能用」——工程上要留余量，还要考虑瞬时电流。"},
        {"q": "把系统切成分段验证时，下面哪种做法符合「一次只改一处」？",
         "options": [("先只测电源，得到明确结论后再动接线", True),
                     ("同时换模块、改程序、重接线，看现象有没有变化", False),
                     ("把所有模块都换成贵的型号，一次解决", False)],
         "explain": "一次只改一处，每一次改动才能对应一条可信的结论。<strong>错因提醒：</strong>许多同学误认为「多改几处更快」，结果现象变了也说不清是哪一步起的作用。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>接口约定</strong>：供电、逻辑电平、通信方式。三条定清楚，模块才能独立替换、跨项目复用。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>电平与电流</strong>：逻辑电平不匹配必须加电平转换；总电流要留余量，大电流负载别都从主控板取电。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>分段验证</strong>：顺序是电源 → 电平 → 信号 → 程序，前一段不过就不往下，一次只改一处。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那套补光装置：</strong>先把模块边界划清楚，把供电、电平、通信三条约定写在纸上；再按分段验证的顺序一段段确认。同一批零件，接法不变、程序不变，只是把「约定」和「顺序」补上，它就能稳定跑起来了。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「接口约定、余量、分段验证、一次只改一处」这四个词，把一套装置从搭起来到调通的过程讲清楚。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出模块化设计的三条接口约定，并各举一个不满足时会出现的故障现象。",
            "说明为什么逻辑电平不匹配的模块不能直接相接。",
            "写出分段验证的推荐顺序，并解释为什么电源要排在第一位。",
        ],
        [
            "某装置有四个模块：两个各 20 mA 的传感模块、一个 150 mA 的执行模块、一个 45 mA 的通信模块，主控自身 75 mA。算出总电流，判断板载 500 mA 上限是否够用，并给出改进办法。",
            "某装置上电后主控能启动，但两个传感器读数都不对。写出你的三步排查方案，并说明每一步在排除什么。",
        ],
        [
            "为学校的一个真实需求（如教室光照调节、植物浇水提醒）设计一套模块化方案：模块划分、三条接口约定、供电估算写在纸上。",
            "给上面这套方案写一张分段验证检查表，按顺序列出每一步的做法与判据，并说明哪一步不过就不该继续。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-open-hardware",
    "node_id": "it-m-open-hardware",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "开源硬件与模块化设计",
    "name_en": "Open Hardware and Modular Design",
    "grade": 8,
    "grade_cn": "八年级",
    "domain": "iot-modules",
    "domain_cn": "物联网与模块",
    "lesson_type": "project-design",
    "version": "1.0.0",
    "description": "从一台「零件都买对了却跑不起来」的装置出发，学会用供电、逻辑电平、通信方式三条接口约定把系统拆成可独立替换的模块，按模块数量估算总电流并判断余量，识别电平不匹配的危害，最后用分段验证的顺序定位并排除故障。",
    "tags": ["模块化设计", "接口约定", "逻辑电平", "电流预算", "总线地址", "共地", "分段验证"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「物联网与模块」——使用开源硬件完成模块化系统搭建与调试。",
    "hero_question": "从一堆都买对了的零件，到一台能稳定跑起来的装置，中间缺的是哪一步？",
    "hero_alt": "开源硬件与模块化设计知识结构图：模块与接口约定、电平与电流预算、分段验证与排障三栏",
    "hero_caption": "模块要有边界 · 接口要有约定 · 电流要留余量 · 调试要分段",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "模块之间靠什么约定才能配合？", "d": "接口到底约定了哪几件事", "v": "模块之间靠什么约定才能配合"},
        {"t": "零件都对，为什么接上就是不动？", "d": "电平、电流、地址各能造成什么故障", "v": "零件都对，为什么接上就是不动"},
        {"t": "怎么才能一遍就把问题查出来？", "d": "分段验证为什么要讲顺序", "v": "怎么才能一遍就把问题查出来"},
        {"t": "为什么大电流的模块要单独供电？", "d": "余量与瞬时电流是两回事", "v": "为什么大电流的模块要单独供电"},
    ],
    "objectives": [
        "能说出模块化设计的三条接口约定——供电、逻辑电平、通信方式，并说明模块为什么可以独立替换",
        "能按模块数量估算总电流，判断供电是否留有足够余量，并识别电流不足的典型现象",
        "能判断两个模块的逻辑电平是否匹配，知道什么时候必须使用电平转换",
        "能按电源、电平、总线、共地的顺序做分段验证，定位并排除装置故障",
    ],
    "objectives_plain": [
        "能说出模块化设计的三条接口约定——供电、逻辑电平、通信方式，并说明模块为什么可以独立替换",
        "能按模块数量估算总电流，判断供电是否留有足够余量，并识别电流不足的典型现象",
        "能判断两个模块的逻辑电平是否匹配，知道什么时候必须使用电平转换",
        "能按电源、电平、总线、共地的顺序做分段验证，定位并排除装置故障",
    ],
    "standards": [
        {"content": "使用开源硬件完成模块化系统搭建与调试。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》物联网与模块 · 初中"},
        {"content": "在动手实践中理解系统的组成与接口关系，能按一定方法定位并排除常见故障。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》过程与控制 / 问题解决 · 初中"},
    ],
    "prereqs": ["it-m-iot-concept"],
    "prereqs_name": "物联网概念与架构",
    "prereqs_meta": "it-m-iot-concept",
    "leads_to": ["it-m-ai-applications"],
    "next_meta": "it-m-ai-applications",
    "section_images": ["assets/it-m-open-hardware-fig1.webp", "assets/it-m-open-hardware-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一台「零件都买对了却跑不起来」的装置，问题多半在接口约定和调试顺序上。带着它开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把系统拆成模块，并让它稳定跑起来。",
        "objectives": "看清四件事：三条接口约定、电流余量、电平匹配、分段验证的顺序。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "接口约定就三条：供电、逻辑电平、通信方式。三条都答上，模块才能独立替换。",
        "lab-1": "把模块类型换成 5 V 执行模块、数量拖到 4 个，看仪表条越过右端；再换取电方式，看余量变化。",
        "module-2": "分段验证的顺序是电源 → 电平 → 信号 → 程序。前一段不过，后面测到的现象都不可信。",
        "lab-2": "把插槽 2 也换成带总线的模块，地址就会重复；换成地址可选的另一个模块，看结论怎么变。",
        "worked-example": "五步走：供电、接线、电平、总线地址、单元程序。每一步都要说清它在排除什么。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "先选故障现场，再按「先电源、后信号、先隔离、后定位」挑三步。别一上来就重写程序。",
        "posttest": "换了电平不匹配和电流吃紧的新情境，看看你还能不能用上接口约定与分段验证。",
        "summary": "用「接口约定、余量、分段验证、一次只改一处」四个词，把整套流程讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课是「物联网与模块」领域承接概念课之后的硬件实践课。设计上不引入任何品牌、产品与具体型号，把力气花在三个可计算、可观察的环节上：用电平与电流预算台把「接口能不能直连」变成可读的电流数字与仪表条，用上电自检工作台把「电源→电平→总线→共地」变成有顺序的判定日志，用分段排障台让学生在动手之前就体会工程排查的顺序价值。全课贯穿一条工程判断：接口要约定清楚，调试要分段进行，一次只改一处。价值取向上强调按需供电、节约资源，以及动手前先算清楚、排障时不靠运气的工程习惯。",
    "plan_table": """| 1 | cover | 开源硬件与模块化设计 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：一条线接错，为什么整套都不工作？ | 起·前测（暴露直觉） |
| 5 | concept | 模块能独立替换，靠的是三条接口约定 | 承·概念一 |
| 6 | interactive | 电平与电流预算台：这套接口到底能不能直连？ | 承·实验室一（余量可算、仪表可见） |
| 7 | concept | 分段验证：调试是有顺序的 | 承·概念二 |
| 8 | interactive | 上电自检工作台：装好模块，按顺序查一遍 | 承·实验室二（逐条判定可观察） |
| 9 | concept | 例题示范：读数一直是零，怎么一段段查出来？ | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次排障工程师，按顺序把故障查通 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：模块与接口约定 / 电平与电流预算 / 分段验证与排障三栏\n- P5 模块化系统结构图（已生成）：主控 + 输入模块 + 输出模块 + 电源模块及接口标注\n- P7 分段验证流程图（已生成）：电源 → 逻辑电平 → 总线地址 → 共地 → 单元程序\n- 若需补充：模块与主控板的实物照片（不带任何品牌标识、不出现型号文字）",
}
