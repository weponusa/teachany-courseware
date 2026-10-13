# -*- coding: utf-8 -*-
"""初中信息科技 · 物联网概念与架构（G8）—— 补齐课标「物联网与模块」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-iot-concept-fig1.webp'
F2 = './assets/it-m-iot-concept-fig2.webp'

TTS = {
    "hero": "先看一个真实的问题。一间教室，灯忘关了、空气闷了，人进门才知道，全靠人一遍遍去看。能不能让这些东西自己知道、自己上报、甚至自己动手？这就是物联网要解决的事。它并不神秘，靠的是把物理世界的信息变成数字量，再经过网络送到平台，最后由平台来判断和决策。这节课我们就把这三层拆开看清楚。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道物联网到底和互联网有什么不一样，还是想知道传感器是凭什么把温度变成数字的，又或者你想亲手把一条从采集到动作的完整链路搭起来。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出物联网是什么，知道它连接的对象是物，而互联网连接的对象主要是人。第二，能说出感知层的作用，理解传感器把连续变化的物理量转换成有限级数数字量的过程，知道量化误差不可避免。第三，能说出网络层的作用，会根据距离、带宽和功耗为设备选择合适的连接方式。第四，能说出应用层的作用，并把一个真实场景拆成感知层、网络层、应用层三部分。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "物联网就是让物品具备感知、联网和上报的能力。它的定义是：通过感知设备，按约定的方式把物品与网络连接起来，实现对物品的识别、数据采集和远程控制。这里要和互联网分清楚：互联网主要连接人和信息，物联网连接的是物。手机刷视频是互联网，教室里的温湿度采集终端每隔一分钟把数据发回平台，这是物联网。物联网能成立，靠三个环节：先感知，再传输，最后处理。",
    "lab-1": "光看定义不够，我们到感知层去做一次真实的采集。左边选一种传感器，拖动滑块改变环境里的真实物理量，右边的数字会跟着变。请你盯住三个数：环境中真实的值、计算机最终拿到的整数、以及还原出来的传感器读数。你会发现，还原值和真实值之间总有一点偏差，这不是故障，而是把连续量变成有限级数必然付出的代价。",
    "module-2": "一条完整的物联网链路可以分成三层。感知层在最底下，传感器和执行器都在这里，负责把物理世界的信息变成数字量，也负责执行动作。网络层在中间，负责把数据从设备送到平台，它要解决距离、带宽和供电这三件事。应用层在最上面，负责存储、分析、判断和决策，并把结果展示给人。数据从下往上走，控制指令从上往下回，两层之间是双向的。",
    "lab-2": "现在你当一次网络工程师。设备装在哪里、每分钟要传多少数据，都是要提前算清楚的。左滑调距离，右滑调数据量，再选一种连接方式，看看它能不能连上、带宽占了多少、一节电池能撑多久。你会发现：覆盖越远的连接方式，通常越费电。选型没有最好的方案，只有在当前条件下最合适的方案。",
    "worked-example": "我们一起分析一道题。学校要在实验室做一个有害气体超量后自动通风的系统，请指出它的三层分别由什么构成。第一步，看清目标：要解决的是气体超量时要自动通风。第二步，找感知层：气体传感器负责采集浓度，采集终端负责把数据变成数字量，继电器负责执行开窗或启动风机。第三步，找网络层：实验室到学校平台的距离只有几十米，实验楼内的无线局域网就够用，不必用更费电的蜂窝网络。第四步，找应用层：判断浓度有没有超过阈值、什么时候下发指令、报警记录存多久、怎么通知老师。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次物联网系统集成工程师。左边选感知设备，中间选网络方式，右边选应用动作，然后点运行，看这条链路能不能跑通。要特别留意一种情况：如果应用层要用的数据，感知层根本没有采集，这条链路就是断的。这不是程序写错了，而是设计的时候没有前后对齐。",
    "posttest": "最后用新情境检验一下。这次出现了校园积水预警和图书馆座位管理，看看你能不能把三层架构和量化误差用上去。",
    "summary": "这节课我们弄明白了三件事。第一，物联网是让物品能感知、能联网、能上报的技术，它连接的是物，与主要连接人的互联网不是一回事。第二，感知层的核心工作是把连续变化的物理量转换成有限级数的数字量，量化误差是这个过程的正常代价，采样和上报的频率要按需要来定。第三，网络层和网络选型要从距离、带宽和功耗三方面一起权衡，应用层负责判断、决策与展示。回到开头那间教室：装上温湿度传感器和人体红外，数据经实验楼内网络送到平台，平台判断无人且灯亮就下发关闭指令，这间教室就真的能自己管自己了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出物联网三层架构的名称，并各举一个组成部件。第二层能力应用，动手做：为家里的一个场景画出三层链路图，标出数据从下往上走的路径和指令从上往下回的路径。第三层迁移挑战，选做：为学校的某个真实需求设计一个物联网方案，算出每天的数据量和设备续航，说明你为什么这样选连接方式。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 物联网与三个环节", "lab-1": "实验室一 感知层采样台", "module-2": "概念二 三层架构",
    "lab-2": "实验室二 网络层选型台", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 三层链路搭建", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.ta-tag { padding: 4px 10px; border-radius: 999px; font-size: 13px; font-variant-numeric: tabular-nums;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); color: var(--text-secondary); }
.ta-tag.hit { background: var(--warm-soft); border-color: var(--warm); color: var(--text-strong); font-weight: 700; }
.ta-log { list-style: none; margin: 0; padding: 0; font-size: 14px; }
.ta-log li { padding: 8px 10px; margin-bottom: 6px; border-radius: 10px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); white-space: pre-wrap; }
.ta-log li .tag { display: inline-block; margin-right: 8px; padding: 1px 8px; border-radius: 999px;
  font-size: 12px; font-weight: 700; background: var(--brand-soft); color: var(--brand); }
.ta-log li.no .tag { background: var(--warm-soft); color: var(--warm-deep); }
.ta-log li.bad { border-color: var(--danger); }
.ta-log li.ok { border-color: var(--ok); }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-iot-concept 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 感知层采样台：物理量 → 模数转换 → 数字量（量化误差可观察）
   3) 网络层选型台：距离 / 数据量 / 功耗 → 连通性、带宽占用、续航
   4) 三层链路搭建器：感知 → 网络 → 应用，含数据不匹配诊断
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

  /* ---------- 2. 感知层采样台 ---------- */
  var SENSORS = {
    temp:  { n: '温度传感器', unit: '℃',  min: -10, max: 50,   bits: 8,  dec: 1, bytes: 2, kind: '连续量（数值）',
             th: function (v) { return v > 30; }, rule: '超过 30 ℃ 判定为过热' },
    light: { n: '光照传感器', unit: 'lx',  min: 0,   max: 1000, bits: 10, dec: 0, bytes: 2, kind: '连续量（数值）',
             th: function (v) { return v < 200; }, rule: '低于 200 lx 判定为需要开灯' },
    pir:   { n: '人体红外传感器', unit: '', min: 0, max: 1,    bits: 1,  dec: 0, bytes: 1, kind: '开关量（0 或 1）',
             th: function (v) { return v > 0.5; }, rule: '为 1 时判定为有人' }
  };
  var stage1 = document.getElementById('s1-stage');
  if (stage1) {
    var cur = 'temp', total = 0, bytes = 0, history = [];
    var eEnv = document.getElementById('s1-env');
    var eEnvVal = document.getElementById('s1-env-val');
    var eRead = document.getElementById('s1-read');
    var eAdc = document.getElementById('s1-adc');
    var eKind = document.getElementById('s1-kind');
    var eErr = document.getElementById('s1-err');
    var eOut = document.getElementById('s1-out');
    var eCount = document.getElementById('s1-count');
    var eBytes = document.getElementById('s1-bytes');
    var eHist = document.getElementById('s1-hist');

    function real(p) {
      var S = SENSORS[cur];
      return S.min + p / 100 * (S.max - S.min);
    }
    function levels() { return Math.pow(2, SENSORS[cur].bits) - 1; }

    function render1() {
      var S = SENSORS[cur], p = Number(eEnv.value);
      var rv = real(p);
      var lv = levels();
      var adc = Math.round((rv - S.min) / (S.max - S.min) * lv);
      var back = S.min + adc / lv * (S.max - S.min);
      var err = Math.abs(back - rv);
      var over = S.th(back);
      var shown = S.bits === 1 ? (adc ? '有人' : '无人') : back.toFixed(S.dec) + ' ' + S.unit;

      eEnvVal.textContent = rv.toFixed(S.dec) + ' ' + S.unit;
      eRead.textContent = shown;
      eAdc.textContent = S.bits === 1 ? String(adc) : String(adc) + ' / ' + lv;
      eKind.textContent = S.kind;
      eErr.textContent = S.bits === 1 ? '—' : err.toFixed(S.dec) + ' ' + S.unit;
      eCount.textContent = total + ' 条';
      eBytes.textContent = bytes + ' 字节';

      eOut.className = 'result ' + (over ? '' : 'warn');
      eOut.innerHTML = '<strong>' + S.n + '：</strong>用 ' + S.bits + ' 位表示，把 ' +
        S.min + ' ~ ' + S.max + ' 的范围切成 ' + (lv + 1) + ' 级，每级约 ' +
        ((S.max - S.min) / lv).toFixed(S.dec === 0 ? 1 : 3) + ' ' + (S.unit || '级') +
        '。<br>判断规则「' + S.rule + '」，当前' + (over ? '已触发' : '未触发') +
        '。<br><strong>易错点：</strong>还原值和真实值永远对不齐，这段差距叫<em>量化误差</em>，不是传感器坏了——位数越少，误差越大。';

      document.querySelectorAll('[data-s1-sensor]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.s1Sensor === cur);
      });
      renderHist();
    }

    function renderHist() {
      eHist.innerHTML = '';
      if (history.length === 0) {
        var tip = document.createElement('span');
        tip.className = 'ta-tag';
        tip.textContent = '还没有采样记录，点「采集一次」试试';
        eHist.appendChild(tip);
        return;
      }
      history.slice(-8).forEach(function (h) {
        var t = document.createElement('span');
        t.className = 'ta-tag' + (h.hit ? ' hit' : '');
        t.textContent = h.txt;
        eHist.appendChild(t);
      });
    }

    document.querySelectorAll('[data-s1-sensor]').forEach(function (b) {
      b.addEventListener('click', function () { cur = b.dataset.s1Sensor; total = 0; bytes = 0; history = []; render1(); });
    });
    eEnv.addEventListener('input', render1);
    document.getElementById('s1-sample').addEventListener('click', function () {
      var S = SENSORS[cur], p = Number(eEnv.value);
      var rv = real(p), lv = levels();
      var adc = Math.round((rv - S.min) / (S.max - S.min) * lv);
      var back = S.min + adc / lv * (S.max - S.min);
      var txt = S.bits === 1 ? (adc ? '有人' : '无人') : back.toFixed(S.dec) + S.unit;
      total += 1;
      bytes += S.bytes;
      history.push({ txt: txt, hit: S.th(back) });
      render1();
    });
    document.getElementById('s1-reset').addEventListener('click', function () {
      total = 0; bytes = 0; history = []; render1();
    });
    render1();
  }

  /* ---------- 3. 网络层选型台 ---------- */
  var LINKS = {
    n1: { n: '短距离低功耗无线', dist: 30,   rate: 0.3, power: 1,  note: '覆盖几十米，速率低，一节电池能用很久，适合室内的采集节点。' },
    n2: { n: '实验楼局域网无线', dist: 120,  rate: 20,  power: 8,  note: '覆盖一栋楼，速率高，但需要持续供电或频繁换电。' },
    n3: { n: '移动蜂窝网络',     dist: 5000, rate: 100, power: 30, note: '覆盖几公里，几乎不受场地限制，但耗电和费用都最高。' }
  };
  var stage2 = document.getElementById('s2-stage');
  if (stage2) {
    var link = 'n2';
    var eDist = document.getElementById('s2-dist');
    var eData = document.getElementById('s2-data');
    var eDistVal = document.getElementById('s2-dist-val');
    var eDataVal = document.getElementById('s2-data-val');
    var eOut2 = document.getElementById('s2-out');

    function render2() {
      var L = LINKS[link];
      var d = Number(eDist.value), kb = Number(eData.value);
      eDistVal.textContent = d + ' m';
      eDataVal.textContent = kb.toFixed(1) + ' KB/分';
      var need = kb / 60;
      var use = need / L.rate * 100;
      var reach = d <= L.dist;
      var enough = use <= 60;
      var days = Math.floor(300 / L.power);
      var ok = reach && enough;

      eOut2.className = 'result ' + (ok ? '' : 'error');
      eOut2.innerHTML = '<strong>' + L.n + '</strong>：有效距离 ' + L.dist + ' 米，速率 ' + L.rate +
        ' KB/s，平均功耗 ' + L.power + ' 单位/天（电池按 300 单位算，可用约 ' + days + ' 天）。<br>' +
        '当前距离 ' + d + ' 米 → ' + (reach ? '在覆盖范围内' : '超出覆盖范围，连不上') +
        '；带宽占用 ' + use.toFixed(1) + '% → ' + (enough ? '够用' : '超出可用余量，会丢包') + '。<br>' +
        (ok
          ? '<strong>可以选它。</strong>' + L.note
          : '<strong>这条路走不通。</strong>' + (reach
              ? '距离没问题，但数据量太大，带宽吃满了——先把上报间隔调长，或换速率更高的连接方式。'
              : '数据量没问题，但设备装在 ' + d + ' 米外，这种连接方式够不到——要么换覆盖更远的连接方式，要么把设备挪近。'));
      document.querySelectorAll('[data-s2-link]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.s2Link === link);
      });
    }
    document.querySelectorAll('[data-s2-link]').forEach(function (b) {
      b.addEventListener('click', function () { link = b.dataset.s2Link; render2(); });
    });
    eDist.addEventListener('input', render2);
    eData.addEventListener('input', render2);
    render2();
  }

  /* ---------- 4. 三层链路搭建器 ---------- */
  var SRC = {
    temp: { n: '温度传感器',   data: '温度（℃）',      bytes: 2, sample: '26.0 ℃' },
    gas:  { n: '气体传感器',   data: '气体浓度（ppm）', bytes: 2, sample: '812 ppm' },
    pir:  { n: '人体红外传感器', data: '有人 / 无人',    bytes: 1, sample: '有人' }
  };
  var ACT = {
    fan:    { n: '开启通风设备',   need: ['gas'],  rule: '气体浓度超过 800 ppm 时开启通风设备', lack: '气体浓度' },
    light:  { n: '开启照明',       need: ['pir'],  rule: '检测到有人且光照不足时开启照明',       lack: '有人 / 无人' },
    report: { n: '生成日统计报表', need: ['temp', 'gas'], rule: '把连续量数据按小时汇总成报表',   lack: '一个连续量数据（温度或气体浓度）' }
  };
  var synStage = document.getElementById('syn-stage');
  if (synStage) {
    var pickSrc = 'temp', pickLink = 'n2', pickAct = 'fan', ran = false;

    function renderSyn() {
      document.querySelectorAll('[data-syn-sensor]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.synSensor === pickSrc);
      });
      document.querySelectorAll('[data-syn-link]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.synLink === pickLink);
      });
      document.querySelectorAll('[data-syn-act]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.synAct === pickAct);
      });
      var out = document.getElementById('syn-out');
      if (!ran) {
        out.className = 'result warn';
        out.textContent = '三样都选好之后，点「运行链路」看看它能不能跑通。';
      }
    }

    document.querySelectorAll('[data-syn-sensor]').forEach(function (b) {
      b.addEventListener('click', function () { pickSrc = b.dataset.synSensor; ran = false; renderSyn(); });
    });
    document.querySelectorAll('[data-syn-link]').forEach(function (b) {
      b.addEventListener('click', function () { pickLink = b.dataset.synLink; ran = false; renderSyn(); });
    });
    document.querySelectorAll('[data-syn-act]').forEach(function (b) {
      b.addEventListener('click', function () { pickAct = b.dataset.synAct; ran = false; renderSyn(); });
    });

    document.getElementById('syn-run').addEventListener('click', function () {
      var S = SRC[pickSrc], L = LINKS[pickLink], A = ACT[pickAct];
      var out = document.getElementById('syn-out');
      var matched = A.need.indexOf(pickSrc) >= 0;
      var reach = 80 <= L.dist;                 // 本场景：设备装在离平台 80 米处
      var use = 0.6 / 60 / L.rate * 100;        // 本场景：每分钟上报 0.6 KB
      var linkOk = reach && use <= 60;

      var rows = [];
      rows.push('<li><span class="tag">感知层</span>' + S.n + '把物理世界的量变成数字量，输出 1 条数据：' +
        S.sample + '（' + S.bytes + ' 字节）</li>');
      rows.push(reach
        ? '<li' + (linkOk ? '' : ' class="bad"') + '><span class="tag">网络层</span>通过「' + L.n + '」把数据送到应用平台：延迟约 ' +
          (0.6 / 0.3).toFixed(1) + ' 秒，带宽占用 ' + use.toFixed(1) + '%' + (linkOk ? '' : '，超出可用余量，数据会丢') + '</li>'
        : '<li class="bad"><span class="tag">网络层</span>设备装在离平台 80 米处，而「' + L.n + '」只能覆盖 ' +
          L.dist + ' 米——数据根本送不上去，链路在这里就断了</li>');
      rows.push('<li><span class="tag">应用层</span>判断规则：「' + A.rule + '」</li>');
      if (!linkOk) {
        rows.push('<li class="bad"><span class="tag">诊断</span><strong>先解决网络层。</strong>感知层能采到数据，应用层也想好了规则，但中间这一段送不过去。工程上遇到问题，先逐层确认哪一层断了，再动手改。</li>');
      } else if (!matched) {
        rows.push('<li class="bad"><span class="tag">诊断</span><strong>链路对不上。</strong>应用动作「' + A.n +
          '」需要的是' + A.lack + '，而感知层送上来的却是「' + S.data +
          '」。这不是程序写错了，是设计时前后没有对齐——先确定应用层要用什么数据，再回头挑采集它的传感器。</li>');
      } else {
        rows.push('<li class="ok"><span class="tag">执行</span>应用层判定成立，下发指令：' + A.n +
          '；同时把这次数据和指令写入日志，便于事后追溯。</li>');
        rows.push('<li class="ok"><span class="tag">完成</span>三层全部接通：感知层有数据、网络层送得到、应用层用得上。这条链路可以跑起来了。</li>');
      }
      out.className = 'result ' + (matched && linkOk ? '' : 'error');
      out.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
      ran = true;
    });

    document.getElementById('syn-reset').addEventListener('click', function () {
      pickSrc = 'temp'; pickLink = 'n2'; pickAct = 'fan'; ran = false; renderSyn();
    });
    renderSyn();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：物联网到底物在哪里？", TTS["pretest"], [
        {"q": "下面哪一件事属于物联网要做的事？",
         "options": [("把教室里的温度和人数自动采集起来送到平台，并据此决定要不要开窗", True),
                     ("用手机看一段在线视频", False),
                     ("把一份文档存到网盘里", False)],
         "explain": "物联网的关键是「物」自己产生数据：传感器采集、网络传输、平台决策。看视频和存文档连接的都是人和信息，属于互联网。<strong>错因提醒：</strong>把上网和物联网搞混，是这一课最常见的错误。"},
        {"q": "传感器把 0 ℃ 到 50 ℃ 的温度范围用 8 位来表示，这意味着：",
         "options": [("这 50 ℃ 的范围被切成了 256 级，每一级之间还会有一点点误差", True),
                     ("传感器能测到小数点后无限多位", False),
                     ("温度可以完全精确地还原，没有任何误差", False)],
         "explain": "有限位数的数字量只能表示有限个等级，真实值落在两级之间时只能就近取整，这就产生了量化误差。<strong>错因提醒：</strong>很多同学误认为数字量一定比模拟量更精确，其实精度取决于位数和量程。"},
        {"q": "一个装在操场角落的土壤湿度采集点，到机房平台大约有 300 米。选择连接方式时最该优先考虑的是：",
         "options": [("这种连接方式能不能覆盖 300 米，以及它的耗电能不能接受", True),
                     ("哪种连接方式的名字听起来更先进", False),
                     ("哪种连接方式的线最便宜，不用管能不能覆盖", False)],
         "explain": "网络选型看三件事：覆盖距离、带宽、功耗。这个问题先记在心里，等下我们用选型台实际算一算。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "物联网让物品能感知、能联网、能上报", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道互联网能把人和信息连起来，也用过各种在线服务。但你有没有想过：教室里的温度、农田里的湿度、仓库里的货物，它们自己不会说话，<strong>所以</strong>我们需要一套办法，把物理世界的信息变成计算机能处理的数据，再送到平台上去判断和决策——这就是物联网。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">物联网是指通过感知设备，按约定的方式把物品与网络连接起来，实现对物品的识别、数据采集与远程控制。<strong>它连接的对象是物，互联网连接的对象主要是人。</strong></p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>① 感知</strong></p>
            <p style="color:var(--muted)">用传感器把温度、光照、气体浓度等物理量变成数字量。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 传输</strong></p>
            <p style="color:var(--muted)">用有线或无线的连接方式，把数据从设备送到平台。</p>
          </div>
          <div class="inner-card">
            <p><strong>③ 处理</strong></p>
            <p style="color:var(--muted)">平台存储、分析、判断，再决定是否下发控制指令。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="感知层把连续变化的物理量经过采样和模数转换变成数字量的过程示意图">
          <figcaption>感知层的核心工作：把连续变化的物理量，经采样与模数转换变成有限级数的数字量</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔢</span><div><strong>记忆锚点：</strong>把感知层想象成一台「翻译机」——物理世界说的是温度、光照、声音，计算机只听得懂 0 和 1，翻译机负责把前者逐级切分并翻译成后者。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一间教室，装不装传感器是两回事：不装，屋里闷了只能靠人进去才知道；装了，数据会自己流到平台上。"},
    {"lens": "比较它", "text": "互联网连接人和信息，物联网连接物。判断一个系统属不属于物联网，就问一句：数据是「物」自己产生的吗？"},
    {"lens": "迁移它", "text": "量化的思路到处都在用：尺子的最小刻度、电子秤的最小读数、音乐采样率，都是用有限的等级去逼近连续的真实值。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "感知层采样台：温度是怎么变成数字的？", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">选一种传感器，拖动滑块改变环境里的真实物理量，观察「真实值 → 数字量 → 还原读数」三步的变化，再做几次采集。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-s1-sensor="temp" style="text-align:center">温度传感器</button>
            <button class="choice" data-s1-sensor="light" style="text-align:center">光照传感器</button>
            <button class="choice" data-s1-sensor="pir" style="text-align:center">人体红外传感器</button>
          </div>
          <div id="s1-stage" style="margin-top:14px">
            <div class="slider-row">
              <label for="s1-env">环境真实值</label>
              <input type="range" id="s1-env" min="0" max="100" step="1" value="62">
              <span class="readout-cell" style="flex:0 0 104px"><span class="k">真实值</span><span class="v" id="s1-env-val">—</span></span>
            </div>
            <div class="lab-readout">
              <div class="readout-cell"><span class="k">计算机拿到的数字量</span><span class="v" id="s1-adc">—</span></div>
              <div class="readout-cell"><span class="k">还原后的读数</span><span class="v green" id="s1-read">—</span></div>
              <div class="readout-cell"><span class="k">量化误差</span><span class="v" id="s1-err">—</span></div>
              <div class="readout-cell"><span class="k">数据种类</span><span class="v" id="s1-kind">—</span></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">本次已采集</span><span class="v" id="s1-count">0 条</span></div>
            <div class="readout-cell"><span class="k">累计数据量</span><span class="v green" id="s1-bytes">0 字节</span></div>
          </div>
          <p style="margin:14px 0 0;font-weight:700;font-size:14px">最近采样记录</p>
          <div class="ta-tags" id="s1-hist"></div>
          <div class="flex-row">
            <button class="choice" id="s1-sample" style="text-align:center;flex:1">采集一次</button>
            <button class="choice" id="s1-reset" style="text-align:center;flex:1">清空采样记录</button>
          </div>
          <p class="result warn" id="s1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📐</span><div><strong>动手比一比：</strong>把温度滑到同一个位置，再把人体的位数想成 8 位——位数越少，级数越粗，量化误差越大。所以选传感器时，位数不是一个可以随便定的数，它直接决定了你能看多细。</div></div>
    ''', tag="感知层实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "感知层、网络层、应用层，各管一段", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>三层不是三个盒子，是一条流水线。</strong>数据从最底下往上走，控制指令从最上面往下回。链路里任何一层出问题，整条链路都不成立——所以工程上先分层，才能一层一层查。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>感知层</strong>：传感器负责采集，执行器负责动作，采集终端负责把物理量变成数字量。这一层离物理世界最近。</div></div>
          <div class="step"><span class="n">2</span><div><strong>网络层</strong>：把数据从设备送到平台。它要同时回答三个问题——够不够远、够不够快、费不费电。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>应用层</strong>：存储数据、判断条件、下发指令、展示给人看。它决定「数据拿来做什么」。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="物联网三层架构与数据流向示意图，数据向上汇聚、指令向下下发">
          <figcaption>数据自下而上汇聚（感知 → 网络 → 应用），指令自上而下回传（应用 → 网络 → 执行）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易犯的两个错：一是误认为<strong>装了几个传感器就叫物联网</strong>——数据送不出去、平台用不上，就只是一堆孤立的测量；二是误认为<strong>执行器不属于物联网</strong>——只会采集不会动作的系统，永远停在「看见」而没有「做到」，实际项目里执行器和传感器同属感知层。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "网络层选型台：够不够远、够不够快、费不费电", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">设备装在哪、每分钟传多少数据，先算清楚。再选一种连接方式，看看它能不能扛住这个任务。</p>
        <div class="lab-panel">
          <div id="s2-stage">
            <div class="slider-row">
              <label for="s2-dist">设备到平台的距离</label>
              <input type="range" id="s2-dist" min="5" max="1500" step="5" value="80">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">距离</span><span class="v" id="s2-dist-val">80 m</span></span>
            </div>
            <div class="slider-row">
              <label for="s2-data">每分钟上报数据量</label>
              <input type="range" id="s2-data" min="0.1" max="20" step="0.1" value="0.6">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">数据量</span><span class="v" id="s2-data-val">0.6 KB/分</span></span>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" data-s2-link="n1" style="text-align:center">短距离低功耗无线</button>
            <button class="choice" data-s2-link="n2" style="text-align:center">实验楼局域网无线</button>
            <button class="choice" data-s2-link="n3" style="text-align:center">移动蜂窝网络</button>
          </div>
          <p class="result warn" id="s2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔌</span><div><strong>试一试：</strong>把距离拖到 500 米以上，低功耗无线立刻连不上；再把数据量拖到 10 KB/分，局域网无线的带宽余量就吃紧了。工程选型没有「最好的方案」，只有在给定条件下最合适的那一个。</div></div>
    ''', tag="网络层实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一个真实场景，怎么拆成三层", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>学校要在实验室做一个「有害气体超量后自动通风」的系统。请指出它的感知层、网络层、应用层分别由什么构成，并说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清目标：</strong>要解决的不是「测出浓度」，而是「超量时自动通风」——把动作一起看清楚，才知道要采什么、要控什么。</div></div>
          <div class="step"><span class="n">2</span><div><strong>拆感知层：</strong>气体传感器采集浓度，采集终端把浓度变成数字量，继电器或推窗装置执行开窗、启动风机。采集和执行都归这一层。</div></div>
          <div class="step"><span class="n">3</span><div><strong>拆网络层：</strong>实验室到学校平台只有几十米，实验楼内的无线局域网足够；用覆盖几公里的蜂窝网络，白白多花电费和资费。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>拆应用层：</strong>判断浓度是否超过阈值、确认多久才下发指令、报警记录保存多久、怎么通知老师——这些「数据拿来做什么」的事，全在应用层。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少同学误认为「装了气体传感器就是物联网系统」，把三层里的两层都漏掉了：数据没送出去，也没有任何判断和动作。<strong>另一处容易搞混的是把执行器算到应用层</strong>——开窗的装置是物理动作，属于感知层；决定「什么时候开」才是应用层。分层的依据是「管哪一段」，不是「谁更聪明」。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("感知层负责把物理量变成数字量，应用层负责判断和决策", True),
                     ("只要装了传感器，就是一个完整的物联网系统", False),
                     ("执行器属于应用层，因为它是在执行命令", False)],
         "explain": "三层各有分工：感知层采集与执行，网络层传输，应用层判断与决策。<strong>错因提醒：</strong>把「装了传感器」等同于「物联网系统」，是最常见的错误——没有网络与应用，传感器只是一堆孤立读数。"},
        {"q": "某温度传感器的量程是 0 ℃ 到 60 ℃，用 10 位表示。关于它的读数，正确的说法是：",
         "options": [("它能表示有限个等级，真实温度落在两级之间时会有量化误差", True),
                     ("它可以精确到任意小数位", False),
                     ("只要位数足够多，误差就一定为零", False)],
         "explain": "位数决定等级数：10 位是 1024 级，量程 60 ℃ 时每级约 0.06 ℃，误差只会变小、不会消失。<strong>错因提醒：</strong>容易误认为「换成数字量就没有误差了」，其实量化误差是这个过程固有的代价。"},
        {"q": "一个采集点离平台 2 公里，每分钟只上报 0.2 KB 数据。选连接方式时，下面哪种判断最站得住脚？",
         "options": [("先确认候选方案的覆盖距离能否到 2 公里，再比较它们的功耗", True),
                     ("数据量很小，所以任何连接方式都能用", False),
                     ("距离远，所以一定得用速率最高的那种", False)],
         "explain": "覆盖和功耗是主要矛盾，数据量小说明带宽不是瓶颈。<strong>错因提醒：</strong>常见错误是只盯着一个指标下结论——要么以为「数据量小就随便选」，要么以为「距离远就一定要最快」。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：把一条三层链路搭起来并运行", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">场景：一间教室的采集终端装在离平台 80 米处，每分钟上报 0.6 KB 数据。请依次选好三层，再运行这条链路。</p>
        <div class="lab-panel">
          <div id="syn-stage">
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 感知层（选采集设备）</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-syn-sensor="temp" style="text-align:center">温度传感器</button>
                <button class="choice" data-syn-sensor="gas" style="text-align:center">气体传感器</button>
                <button class="choice" data-syn-sensor="pir" style="text-align:center">人体红外传感器</button>
              </div>
            </div>
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">② 网络层（选连接方式）</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-syn-link="n1" style="text-align:center">短距离低功耗无线</button>
                <button class="choice" data-syn-link="n2" style="text-align:center">实验楼局域网无线</button>
                <button class="choice" data-syn-link="n3" style="text-align:center">移动蜂窝网络</button>
              </div>
            </div>
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">③ 应用层（选触发动作）</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-syn-act="fan" style="text-align:center">开启通风设备</button>
                <button class="choice" data-syn-act="light" style="text-align:center">开启照明</button>
                <button class="choice" data-syn-act="report" style="text-align:center">生成日统计报表</button>
              </div>
            </div>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px"></p>
          <div class="flex-row">
            <button class="choice" id="syn-run" style="text-align:center;flex:1">运行链路</button>
            <button class="choice" id="syn-reset" style="text-align:center;flex:1">重新选择</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>如果应用层要判断的是「气体浓度超量」，而感知层只装了温度传感器，这条链路哪个环节错了？应该改哪一层？</p>
          <textarea id="syn-answer" rows="3" placeholder="错在……因为应用层需要的数据是……所以要改的是……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "校园低洼处要做一个积水预警装置：水位超过 30 厘米就发提醒。下列设计里最合理的是：",
         "options": [("用水位传感器采集水位，经网络送到平台判断阈值，超限时推送提醒", True),
                     ("只在低洼处立一块「水深危险」的牌子", False),
                     ("用水位传感器采集水位，把读数存在设备里，不用管平台", False)],
         "explain": "这是感知、传输、应用三层齐备的方案。<strong>错因提醒：</strong>第三个选项是典型的「只有感知层」——数据存下来却没人用，系统等于没建成。"},
        {"q": "图书馆要统计自习座位是否被占用，用红外传感器判断「有人 / 无人」。关于这个数据，正确的说法是：",
         "options": [("它是开关量，只有两种取值，占用 1 位就能表示", True),
                     ("它是连续量，需要很多位才能表示", False),
                     ("它和温度一样，属于模拟量", False)],
         "explain": "「有人 / 无人」只有两种状态，是典型的开关量，1 位就够。温度、光照这类可以连续取值的是连续量。<strong>错因提醒：</strong>容易误认为凡是被传感器采集的都是连续量，其实数据类型由物理量的性质决定。"},
        {"q": "一个部署在郊外的农田监测点，每天要上报一次数据，靠电池供电。最需要权衡的是：",
         "options": [("连接方式的覆盖距离与功耗——用多久换一次电池直接决定这套装置能不能长期用下去", True),
                     ("把上报频率调到每秒一次，数据越多越好", False),
                     ("只要能把数据传回来，功耗多高都无所谓", False)],
         "explain": "郊外供电不便，功耗是决定性的约束；每天一次的频率说明带宽压力很小。<strong>错因提醒：</strong>常见错误是误认为「上报越勤越可靠」，实际上频率越高越费电，超过需要就是浪费。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>物联网</strong>：通过感知设备把物品与网络连起来，实现对物的识别、采集与远程控制；它连接的是物，与连接人的互联网不同。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>三层架构</strong>：感知层采集与执行，网络层负责把数据送到平台，应用层负责判断、决策与展示。数据向上走，指令向下回。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>两个关键量</strong>：感知层要接受量化误差，网络层要在距离、带宽、功耗之间权衡——没有最好的方案，只有最合适的方案。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那间教室：</strong>装上温湿度传感器和人体红外，数据经实验楼内网络送到平台，平台判断「无人且灯还亮着」就下发关闭指令——这间教室自己就能管自己了。整个过程里没有任何一步是神秘的，每一层都在做很清楚的一件事。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「感知层、网络层、应用层」这三个词，说清楚一条完整的物联网链路是怎么跑起来的。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出物联网三层架构的名称，并各举一个组成部件。",
            "区分互联网与物联网：它们连接的对象分别是什么？各举一个例子。",
            "写出一条最低配的物联网链路：从「谁采集」到「谁传输」再到「谁判断」。",
        ],
        [
            "为家里的一个场景（比如阳台浇水、门口亮灯）画出三层链路图，标出数据向上、指令向下两条路径。",
            "某传感器量程 0 ℃ 到 40 ℃，用 8 位表示。算出它的级数和每级代表的温度，并说明量化误差大约有多大。",
        ],
        [
            "为学校的一个真实需求设计物联网方案（比如实验室通风、操场积水预警），给出感知设备、连接方式与判断规则。",
            "在上一题的基础上算一算：每天上报多少次、每天产生多少数据量、用电池供电大概能用多久，并说明你为什么这样选连接方式。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-iot-concept",
    "node_id": "it-m-iot-concept",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "物联网概念与架构",
    "name_en": "Internet of Things: Concepts and Architecture",
    "grade": 8,
    "grade_cn": "八年级",
    "domain": "iot-modules",
    "domain_cn": "物联网与模块",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "从让一间教室自己感知与决策的真实需求出发，理解物联网是让物品能感知、能联网、能上报的技术，掌握感知层、网络层、应用层的基本架构，理解物理量经采样与模数转换变成有限级数数字量的过程及其量化误差，并会按距离、带宽与功耗为设备选择连接方式。",
    "tags": ["物联网", "三层架构", "感知层", "网络层", "应用层", "传感器", "量化误差"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「物联网与模块」——理解物联网感知层、网络层、应用层的基本架构。",
    "hero_question": "一间普通的教室，怎样才能自己「知道」屋里闷了、灯还亮着，并且自己做出反应？",
    "hero_alt": "物联网三层架构知识结构图：感知层、网络层、应用层三栏",
    "hero_caption": "感知层（采集与执行）→ 网络层（距离·带宽·功耗）→ 应用层（判断·决策·展示）：数据向上汇聚，指令向下回传",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "物联网和互联网到底差在哪里？", "d": "不都是联网吗，为什么单分一类", "v": "物联网和互联网到底差在哪里"},
        {"t": "传感器凭什么把温度变成数字？", "d": "物理量怎么才能被计算机读懂", "v": "传感器凭什么把温度变成数字"},
        {"t": "三层架构每层到底在干什么？", "d": "分三层有什么必要", "v": "三层架构每层到底在干什么"},
        {"t": "怎么给设备选一种合适的连接方式？", "d": "距离、速度、耗电怎么权衡", "v": "怎么给设备选一种合适的连接方式"},
    ],
    "objectives": [
        "能说出物联网是什么，区分物联网与互联网连接对象的差别",
        "能说明感知层把物理量转换为数字量的过程，并解释量化误差产生的原因",
        "能根据距离、带宽与功耗，为采集设备选择合适的连接方式",
        "能把一个真实场景拆解为感知层、网络层、应用层三部分并说明各部分作用",
    ],
    "objectives_plain": [
        "能说出物联网是什么，区分物联网与互联网连接对象的差别",
        "能说明感知层把物理量转换为数字量的过程，并解释量化误差产生的原因",
        "能根据距离、带宽与功耗，为采集设备选择合适的连接方式",
        "能把一个真实场景拆解为感知层、网络层、应用层三部分并说明各部分作用",
    ],
    "standards": [
        {"content": "理解物联网感知层、网络层、应用层的基本架构。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》物联网与模块 · 初中"},
        {"content": "在真实情境中采集、组织数据，并借助数据解决问题；认识自主可控技术对信息安全与国家安全的意义。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与编码 / 信息社会责任 · 初中"},
    ],
    "prereqs": [],
    "prereqs_name": "无（初中物联网起点）",
    "prereqs_meta": "无",
    "leads_to": ["it-m-iot-project", "it-m-open-hardware"],
    "next_meta": "it-m-iot-project",
    "section_images": ["assets/it-m-iot-concept-fig1.webp", "assets/it-m-iot-concept-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "让一间教室自己知道屋里闷了、灯还亮着，需要哪几步？带着这个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把任何一个真实场景拆成感知、网络、应用三层。",
        "objectives": "看清四件事：说清物联网是什么、讲明白量化误差、会按距离带宽功耗选连接方式、能把场景拆成三层。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "物联网连接的是物，互联网连接的主要是人；感知、传输、处理三个环节缺一不可。",
        "lab-1": "盯住三个数：真实值、计算机拿到的数字量、还原后的读数。还原值和真实值之间的差距，就是量化误差。",
        "module-2": "感知层采集与执行、网络层传输、应用层判断决策；数据向上走，指令向下回，中间任何一层断了整条链路都不成立。",
        "lab-2": "先拖距离，再拖数据量，最后换个连接方式。覆盖越远的连接方式，通常越费电。",
        "worked-example": "四步走：看清目标、拆感知层、拆网络层、拆应用层。注意执行器归感知层，做决定的才归应用层。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "三样都选好后运行。留意那种「应用层要用的数据感知层没采」的情况——那是设计没对齐，不是程序出错。",
        "posttest": "换了积水预警和座位管理的新情境，看看你还能不能用上三层架构和数据类型的知识。",
        "summary": "用「感知层、网络层、应用层」三个词，把一条完整链路讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「物联网与模块」领域的第一课。设计上不引入任何具体品牌与产品，把力气花在三件可操作的事上：用采样台把「物理量怎么变成数字量」变成看得见的实时读数与量化误差，用选型台把「距离、带宽、功耗」的权衡变成可计算的数字，用链路搭建器让学生亲手把感知、网络、应用三层接起来，并从「应用层要用的数据感知层没采」这类真实设计缺陷中理解分层的意义。价值取向上强调数据只有被正确使用才有价值，也提示设备长期运行要考虑供电与资源的实际约束。",
    "plan_table": """| 1 | cover | 物联网概念与架构 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：物联网到底物在哪里？ | 起·前测（暴露直觉） |
| 5 | concept | 物联网让物品能感知、能联网、能上报 | 承·概念一 |
| 6 | interactive | 感知层采样台：温度是怎么变成数字的？ | 承·实验室一（量化误差可观察） |
| 7 | concept | 感知层、网络层、应用层，各管一段 | 承·概念二 |
| 8 | interactive | 网络层选型台：够不够远、够不够快、费不费电 | 承·实验室二（选型可计算） |
| 9 | concept | 例题示范：一个真实场景，怎么拆成三层 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：把一条三层链路搭起来并运行 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：感知层 / 网络层 / 应用层三栏标注\n- P5 模数转换过程图（已生成）：物理量 → 采样量化 → 有限级数数字量，含量化误差\n- P7 三层架构与数据流向图（已生成）：数据向上汇聚、指令向下回传\n- 若需补充：传感器与采集终端的实物照片（不带任何品牌标识）",
}
