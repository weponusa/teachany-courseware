# -*- coding: utf-8 -*-
"""初中信息科技 · 物联网项目设计（G8）—— 补齐课标「物联网与模块」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-iot-project-fig1.webp'
F2 = './assets/it-m-iot-project-fig2.webp'

TTS = {
    "hero": "先看一个真实的麻烦。有人想做一套教室空气质量装置，传感器买好了，程序也写出来了，可装上以后要么一天就耗光电池，要么该报的时候一声不响。问题不在零件，而在设计：需求没变成指标，指标没变成策略。这节课我们就把从一个想法到一套能长期稳定跑起来的方案，中间该补的环节一个个补齐。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道怎么把一句模糊的需求变成能测量、能检验的技术指标，还是想知道采集和上报的频率到底该定多少，又或者你想亲手把一套方案做出来再评审一遍。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能把一句模糊的现场需求，转换成测什么、测多准、多久测一次这样的可测量指标。第二，能根据采样间隔和设备数量，估算出每天的数据量与存储需求，并判断这个间隔会不会漏掉真实事件。第三，能区分定时上报与变化阈值上报两种策略，会用迟滞避免在阈值附近反复报警。第四，能按检查表评审一套物联网方案，指出它的问题并给出改进办法。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "做一个物联网项目，第一步不是买零件，而是把需求翻译成指标。需求通常是模糊的，比如说教室里空气不好；指标必须是可测量的，要回答三件事：测什么物理量、要求测到多准、多久测一次。指标定下来，才能反过来决定选什么量程和分辨率的传感器、用多快的采集节奏。这里最容易出错的是把需求当成指标用：空气不好无法检验，二氧化碳浓度超过一千五百 ppm 才能检验。",
    "lab-1": "我们来实际算一次指标。左边拖采样间隔，右边拖设备台数，下面会出现三个数：每台设备每天采多少条、全部设备每天产生多少数据、一年下来要占多大空间。再拖一拖事件持续时间，看看当前的采样间隔还抓不抓得住一次真实的变化——间隔拖得越长越省数据，但也越容易漏掉短事件。",
    "module-2": "数据采到了，接下来要决定怎么报上去。最直接的是定时上报：每隔一段时间报一次，简单、数据完整，缺点是没用的数据也照报。另一种是变化与阈值触发上报：只在数值跨过阈值或明显变化时才报，省电省流量。用阈值上报必须配迟滞——也就是开始报警和解除报警用两个不同的界限，否则数值在阈值附近来回抖动，系统就会反复报警。阈值本身也要权衡：太低会频繁误报，太高则危险已经发生才报。",
    "lab-2": "现在你当一次方案设计师。屏幕上是一天二十四小时的温度记录，拖动阈值和迟滞，分别切换定时上报与阈值上报，看看这一天系统要报多少次，有没有漏掉真正超温的时刻。你会看到：迟滞设成零，温度在阈值附近抖动会让上报次数猛增；迟滞设得太大，真的超温了却一次都不报。",
    "worked-example": "我们一起分析一个有问题的方案。有同学设计成：传感器每秒钟采集一次并立即上报，温度超过三十度就报警。第一步，看清目标：要解决的是及时发现超温并提醒。第二步，找问题：每秒钟上报一次，一天就是八万六千四百条，绝大多数是重复的室温数据，电池和流量都撑不住。第三步，再找问题：只在三十度报警，没有迟滞，温度在三十度附近抖动会反复报警，老师很快就不看提醒了。第四步，改进：采集可以快，保证不漏事件；上报改成阈值或变化触发，只在有用的时候报；报警加上迟滞；上报失败还要能缓存重试。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次评审专家。屏幕上是一个方案评审工作台，先选一个真实场景，再依次选定感知设备、连接方式、上报策略和触发动作，然后提交评审。系统会按检查表逐条判定，告诉你哪一项对不上、为什么、该怎么改。评审不是打分游戏，它是把方案真正落地之前必须过的那一关。",
    "posttest": "最后用新情境检验一下。这次出现了农场监测和水箱溢流，看看你能不能把指标换算和上报策略用上去。",
    "summary": "这节课我们弄明白了三件事。第一，需求必须转成可测量的指标，回答测什么、测多准、多久测一次；指标定不下来，选型就没有依据。第二，采样间隔决定数据量和漏检风险，这两件事此消彼长，要按需要来定，不能凭感觉。第三，上报策略要区分定时与阈值触发，用迟滞防止在阈值附近反复报警，阈值定得太低会误报、太高会迟报。回到开头那套装置：先把指标定清楚，再让采集快一点、上报省一点、报警稳一点，它才能长期跑下去。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说明采样间隔与数据量、漏检风险之间的关系。第二层能力应用，动手做：为教室空气质量监测写出三项可测量的指标，算出每天的数据量，并判定采样间隔是否够用。第三层迁移挑战，选做：为学校的一个真实需求完成一套方案，按检查表自查，写出发现的问题和改进办法。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 从需求到指标", "lab-1": "实验室一 指标换算台", "module-2": "概念二 上报策略与阈值",
    "lab-2": "实验室二 上报策略设计器", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 方案评审工作台", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-cells { display: flex; gap: 4px; flex-wrap: wrap; }
.ta-cell { width: 32px; padding: 5px 0; text-align: center; border-radius: 7px; font-size: 12px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); font-variant-numeric: tabular-nums; }
.ta-cell.up { background: var(--brand-soft); border-color: var(--brand); font-weight: 700; }
.ta-cell.hot { background: var(--warm-soft); border-color: var(--warm); font-weight: 800; }
.ta-cell.lost { opacity: .35; text-decoration: line-through; }
.ta-check { list-style: none; margin: 0; padding: 0; }
.ta-check li { padding: 9px 12px; margin-bottom: 6px; border-radius: 10px; font-size: 14px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); }
.ta-check li .ic { font-weight: 800; margin-right: 8px; }
.ta-check li.ok { border-color: var(--ok); }
.ta-check li.no { border-color: var(--danger); }
.ta-meter { display: flex; align-items: center; gap: 10px; margin-top: 10px; }
.ta-meter .bar { flex: 1; height: 10px; border-radius: 999px; background: var(--bg-subtle); overflow: hidden; }
.ta-meter .fill { height: 100%; width: 0; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .35s ease; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-iot-project 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 指标换算台：采样间隔 × 设备台数 → 数据量 / 存储 / 漏检风险
   3) 上报策略设计器：定时 vs 阈值触发，含迟滞防抖与漏报判定
   4) 方案评审工作台：按工程检查表逐条判定并给出改进建议
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

  /* ---------- 2. 指标换算台 ---------- */
  var BYTES_PER_RECORD = 8;
  var stage1 = document.getElementById('p1-stage');
  if (stage1) {
    var eGap = document.getElementById('p1-gap');
    var eDev = document.getElementById('p1-dev');
    var eDur = document.getElementById('p1-dur');
    var eGapV = document.getElementById('p1-gap-val');
    var eDevV = document.getElementById('p1-dev-val');
    var eDurV = document.getElementById('p1-dur-val');
    var ePerDev = document.getElementById('p1-perdev');
    var eTotal = document.getElementById('p1-total');
    var eSize = document.getElementById('p1-size');
    var eYear = document.getElementById('p1-year');
    var eOut = document.getElementById('p1-out');

    function fmtBytes(b) {
      if (b < 1024) return b.toFixed(0) + ' B';
      if (b < 1024 * 1024) return (b / 1024).toFixed(1) + ' KB';
      if (b < 1024 * 1024 * 1024) return (b / 1024 / 1024).toFixed(1) + ' MB';
      return (b / 1024 / 1024 / 1024).toFixed(2) + ' GB';
    }

    function render1() {
      var gap = Number(eGap.value), dev = Number(eDev.value), dur = Number(eDur.value);
      eGapV.textContent = gap + ' 秒';
      eDevV.textContent = dev + ' 台';
      eDurV.textContent = dur + ' 秒';

      var perDev = Math.floor(86400 / gap);
      var total = perDev * dev;
      var dayBytes = total * BYTES_PER_RECORD;
      var yearBytes = dayBytes * 365;
      ePerDev.textContent = perDev.toLocaleString('en-US') + ' 条';
      eTotal.textContent = total.toLocaleString('en-US') + ' 条';
      eSize.textContent = fmtBytes(dayBytes);
      eYear.textContent = fmtBytes(yearBytes);

      var captured = Math.floor(dur / gap) + 1;
      var miss = gap > dur;
      var heavy = dayBytes > 5 * 1024 * 1024;

      eOut.className = 'result ' + (miss || heavy ? 'error' : '');
      var parts = [];
      parts.push('<strong>' + gap + ' 秒采一次、' + dev + ' 台的账：</strong>每台每天 ' + perDev.toLocaleString('en-US') +
        ' 条，全部设备每天 ' + fmtBytes(dayBytes) + '，一年 ' + fmtBytes(yearBytes) + '。');
      if (miss) {
        parts.push('<strong>会漏事件：</strong>这次变化只持续 ' + dur + ' 秒，而你要 ' + gap +
          ' 秒才采一次，两次采样之间事件已经结束了——数据再省，没抓到关键那一刻也没用。');
      } else {
        parts.push('<strong>抓得住：</strong>事件持续 ' + dur + ' 秒，采样间隔 ' + gap +
          ' 秒，大约能采到 ' + captured + ' 个点。');
      }
      if (heavy) {
        parts.push('<strong>数据量偏大：</strong>每天超过 5 MB，长期存在设备上或按流量上传都会吃力。想想是不是每次都要报。');
      }
      parts.push('<strong>易错点：</strong>常见错误是误认为「采得越勤越保险」。采样频率和数据量成正比，而设备供电、存储、流量都是有限的——指标要按需要定，不是按心情定。');
      eOut.innerHTML = parts.join('<br>');
    }
    eGap.addEventListener('input', render1);
    eDev.addEventListener('input', render1);
    eDur.addEventListener('input', render1);
    render1();
  }

  /* ---------- 3. 上报策略设计器 ---------- */
  var TEMP24 = [19, 18, 18, 17, 17, 18, 20, 23, 26, 28, 31, 29, 32, 29, 31, 29, 33, 32, 30, 27, 24, 22, 20, 19];
  var stage2 = document.getElementById('p2-stage');
  if (stage2) {
    var mode = 'th';
    var eTh = document.getElementById('p2-th');
    var eHys = document.getElementById('p2-hys');
    var ePeriod = document.getElementById('p2-period');
    var eThV = document.getElementById('p2-th-val');
    var eHysV = document.getElementById('p2-hys-val');
    var ePeriodV = document.getElementById('p2-period-val');
    var eCells = document.getElementById('p2-cells');
    var eOut2 = document.getElementById('p2-out');
    var eCount = document.getElementById('p2-count');
    var eBytes2 = document.getElementById('p2-bytes');

    function thresholdTrace(T, H) {
      var up = 0, down = 0, alarm = false, events = [], hot = 0;
      TEMP24.forEach(function (v, i) {
        if (v > T) hot += 1;
        if (!alarm && v > T + H) { alarm = true; up += 1; events.push(i); }
        else if (alarm && v < T - H) { alarm = false; down += 1; events.push(i); }
      });
      return { up: up, down: down, total: up + down, events: events, hot: hot };
    }

    function timedTrace(P) {
      var events = [];
      for (var i = 0; i < 24; i += P) events.push(i);
      return { total: events.length, events: events };
    }

    function render2() {
      var T = Number(eTh.value), H = Number(eHys.value), P = Number(ePeriod.value);
      eThV.textContent = T.toFixed(1) + ' ℃';
      eHysV.textContent = H.toFixed(1) + ' ℃';
      ePeriodV.textContent = P + ' 小时';

      var tr, title;
      if (mode === 'th') {
        tr = thresholdTrace(T, H);
        title = '阈值触发上报（阈值 ' + T.toFixed(1) + ' ℃，迟滞 ±' + H.toFixed(1) + ' ℃）';
      } else {
        tr = timedTrace(P);
        title = '定时上报（每 ' + P + ' 小时一次）';
      }
      eCount.textContent = tr.total + ' 次';
      eBytes2.textContent = (tr.total * BYTES_PER_RECORD) + ' B';

      eCells.innerHTML = '';
      for (var i = 0; i < 24; i++) {
        var d = document.createElement('div');
        var isHot = TEMP24[i] > T;
        var sent = tr.events.indexOf(i) >= 0;
        d.className = 'ta-cell' + (sent ? ' up' : (isHot ? ' hot' : ''));
        if (isHot && !sent) d.className += ' lost';
        d.textContent = TEMP24[i];
        d.title = i + ' 时 · ' + TEMP24[i] + ' ℃' + (sent ? '（有上报）' : '');
        eCells.appendChild(d);
      }

      var parts = [];
      parts.push('<strong>' + title + '：这一天共上报 ' + tr.total + ' 次，数据量 ' + (tr.total * BYTES_PER_RECORD) + ' 字节。</strong>');
      if (mode === 'th') {
        parts.push('超过阈值的时刻共 ' + tr.hot + ' 个，其中触发超限上报 ' + tr.up + ' 次、恢复上报 ' + tr.down + ' 次。');
        if (tr.total === 0 && tr.hot > 0) {
          parts.push('<strong>一次都没报，出问题了：</strong>温度确实超过了阈值，但迟滞设得太大，系统等到更高才肯报。迟滞是用来防抖动的，不是用来把报警门槛抬高的。');
        } else if (tr.total >= 6 && tr.hot > 0) {
          parts.push('<strong>上报次数偏多，像是抖动：</strong>迟滞设得太小时，数值在阈值附近来回穿越，系统就会反复报「超限」和「恢复」。把迟滞调大一些，报警会稳下来。');
        } else if (tr.up > 0) {
          parts.push('<strong>这个设置比较稳：</strong>该报的时候报了，次数也不多。迟滞让报警只在真正跨过界限时才切换，不会来回抖。');
        }
        parts.push('<strong>易错点：</strong>误认为「阈值越灵敏越好」是常见的错误。阈值定得太低会频繁误报，很快就没人看提醒了；太高则危险已经发生才报。');
      } else {
        var hot = TEMP24.filter(function (v) { return v > T; }).length;
        parts.push('这段时间里超过 ' + T.toFixed(1) + ' ℃ 的时刻共 ' + hot + ' 个。定时上报的好处是数据完整、实现简单，代价是没用的数据也照样报，而且超温发生在两次上报之间时，平台要等下一次才知道。');
        parts.push('<strong>易错点：</strong>误认为「定时上报最可靠」，其实频率越高越费电、越耗流量，关键是让上报节奏和需要配合。');
      }
      eOut2.className = 'result ' + (mode === 'th' && tr.total === 0 ? 'error' : 'warn');
      eOut2.innerHTML = parts.join('<br>');
      document.querySelectorAll('[data-p2-mode]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.p2Mode === mode);
      });
    }
    document.querySelectorAll('[data-p2-mode]').forEach(function (b) {
      b.addEventListener('click', function () { mode = b.dataset.p2Mode; render2(); });
    });
    eTh.addEventListener('input', render2);
    eHys.addEventListener('input', render2);
    ePeriod.addEventListener('input', render2);
    render2();
  }

  /* ---------- 4. 方案评审工作台 ---------- */
  var SCEN = {
    air:   { n: '教室空气质量监测', need: 'gas',   dist: 60,   lag: 60,   acts: ['fan', 'report'],   key: '气体浓度' },
    seat:  { n: '图书馆座位管理',   need: 'pir',   dist: 90,   lag: 60,   acts: ['light', 'report'], key: '有人 / 无人' },
    soil:  { n: '农场土壤监测',     need: 'soil',  dist: 1800, lag: 3600, acts: ['pump', 'report'],  key: '土壤湿度' },
    water: { n: '校园积水预警',     need: 'water', dist: 400,  lag: 60,   acts: ['alarm', 'report'], key: '水位' }
  };
  var PSENSOR = {
    gas:   { n: '气体传感器',   data: '气体浓度（ppm）', bytes: 2 },
    pir:   { n: '人体红外传感器', data: '有人 / 无人',    bytes: 1 },
    soil:  { n: '土壤湿度传感器', data: '土壤湿度（%）',  bytes: 2 },
    water: { n: '水位传感器',   data: '水位（cm）',      bytes: 2 },
    temp:  { n: '温度传感器',   data: '温度（℃）',       bytes: 2 }
  };
  var PLINK = {
    n1: { n: '短距离低功耗无线', dist: 30,   rate: 0.3, power: 1 },
    n2: { n: '实验楼局域网无线', dist: 120,  rate: 20,  power: 8 },
    n3: { n: '移动蜂窝网络',     dist: 5000, rate: 100, power: 30 }
  };
  var PSTRAT = {
    s1: { n: '每 1 秒定时上报',     lag: 1,    perDay: 86400, tag: '数据量极大' },
    s2: { n: '每 1 分钟定时上报',   lag: 60,   perDay: 1440,  tag: '数据量偏大' },
    s3: { n: '变化与阈值触发上报', lag: 0,    perDay: 20,    tag: '按需上报' },
    s4: { n: '每 1 小时定时上报',   lag: 3600, perDay: 24,    tag: '省电但迟' }
  };
  var PACT = {
    fan:    { n: '开启通风设备', need: '气体浓度',   hint: '需要气体浓度作为判断依据' },
    light:  { n: '开启照明',     need: '有人 / 无人', hint: '需要人体存在数据作为判断依据' },
    pump:   { n: '启动灌溉水泵', need: '土壤湿度',   hint: '需要土壤湿度作为判断依据' },
    alarm:  { n: '推送预警提醒', need: '水位',       hint: '需要水位数据作为判断依据' },
    report: { n: '生成统计报表', need: '任意连续量', hint: '连续量数据都可以用来汇总' }
  };
  var stage4 = document.getElementById('ps-stage');
  if (stage4) {
    var sScen = 'air', sSrc = 'gas', sLink = 'n2', sStrat = 's3', sAct = 'fan';

    function renderSyn() {
      [['data-ps-scen', sScen], ['data-ps-sensor', sSrc], ['data-ps-link', sLink], ['data-ps-strat', sStrat], ['data-ps-act', sAct]]
        .forEach(function (pair) {
          document.querySelectorAll('[' + pair[0] + ']').forEach(function (b) {
            b.classList.toggle('selected', b.getAttribute(pair[0]) === pair[1]);
          });
        });
      var S = SCEN[sScen];
      document.getElementById('ps-brief').innerHTML = '<strong>场景：' + S.n +
        '</strong>　关键量：' + S.key + '　设备到平台约 ' + S.dist + ' 米　需要的最迟发现时间：' +
        (S.lag >= 3600 ? '1 小时以内' : S.lag >= 60 ? '1 分钟以内' : '几乎即时');
    }

    function bind(attr, setter) {
      document.querySelectorAll('[' + attr + ']').forEach(function (b) {
        b.addEventListener('click', function () { setter(b.getAttribute(attr)); renderSyn(); });
      });
    }
    bind('data-ps-scen', function (v) { sScen = v; });
    bind('data-ps-sensor', function (v) { sSrc = v; });
    bind('data-ps-link', function (v) { sLink = v; });
    bind('data-ps-strat', function (v) { sStrat = v; });
    bind('data-ps-act', function (v) { sAct = v; });

    document.getElementById('ps-run').addEventListener('click', function () {
      var S = SCEN[sScen], SRC = PSENSOR[sSrc], L = PLINK[sLink], T = PSTRAT[sStrat], A = PACT[sAct];
      var rows = [];
      var score = 0;

      var sensorOk = sSrc === S.need;
      score += sensorOk ? 1 : 0;
      rows.push('<li class="' + (sensorOk ? 'ok' : 'no') + '"><span class="ic">' + (sensorOk ? '✅' : '❌') +
        '</span>感知设备与场景匹配：场景要的是' + S.key + '，你选的是' + SRC.n + '（' + SRC.data + '）。' +
        (sensorOk ? '对得上，应用层的判断有数据可用。'
                  : '对不上——应用层要用的数据采不到，这条链路从一开始就是断的。应该改为采集' + S.key + '的传感器。') + '</li>');

      var distOk = S.dist <= L.dist;
      score += distOk ? 1 : 0;
      rows.push('<li class="' + (distOk ? 'ok' : 'no') + '"><span class="ic">' + (distOk ? '✅' : '❌') +
        '</span>连接方式覆盖距离：设备到平台 ' + S.dist + ' 米，' + L.n + ' 有效距离 ' + L.dist + ' 米。' +
        (distOk ? '够得到，功耗 ' + L.power + ' 单位/天也在可接受范围。'
                : '够不到，数据送不上平台。应该换覆盖更远的连接方式，或者把设备挪近。') + '</li>');

      var lagOk = T.lag <= S.lag;
      var volumeOk = T.perDay <= 2000;
      var stratOk = lagOk && volumeOk;
      score += stratOk ? 1 : 0;
      var stratWhy = !lagOk
        ? '上报太慢：这种策略最迟要 ' + (T.lag >= 3600 ? '1 小时' : T.lag + ' 秒') + '才能发现变化，而这个场景要求 ' +
          (S.lag >= 3600 ? '1 小时以内' : '1 分钟以内') + '，会迟报。'
        : (!volumeOk ? '上报太勤：每天 ' + T.perDay.toLocaleString('en-US') + ' 条，绝大部分是重复数据，电池和流量都撑不住。'
                     : '节奏合适：既能及时发现变化，每天的上报量（约 ' + T.perDay + ' 条）也在可控范围。');
      rows.push('<li class="' + (stratOk ? 'ok' : 'no') + '"><span class="ic">' + (stratOk ? '✅' : '❌') +
        '</span>上报策略：' + T.n + '（' + T.tag + '）。' + stratWhy + '</li>');

      var actOk = sAct === 'report' || A.need === S.key || (sAct === 'light' && sSrc === 'pir') || (sAct === 'alarm' && sSrc === 'water');
      score += actOk ? 1 : 0;
      rows.push('<li class="' + (actOk ? 'ok' : 'no') + '"><span class="ic">' + (actOk ? '✅' : '❌') +
        '</span>触发动作：' + A.n + '。' + A.hint + '。' +
        (actOk ? '与本次采集的数据对得上。' : '对不上——动作需要的是' + A.need + '，当前方案里没有这个数据。') + '</li>');

      rows.push('<li><span class="ic">＋</span>两项工程必备但很容易被忘掉：一是<strong>迟滞</strong>，开始报警与解除报警用两个界限，避免数值在阈值附近来回抖动；二是<strong>失败重试与本地缓存</strong>，网络中断时数据先存着，恢复后补传，否则这段记录就永远丢了。</li>');

      var out = document.getElementById('ps-out');
      out.className = 'result ' + (score >= 4 ? '' : 'error');
      out.innerHTML = '<strong>评审结果：' + S.n + ' · 通过 ' + score + ' / 4 项</strong>' +
        '<div class="ta-meter"><div class="bar"><div class="fill" style="width:' + (score * 25) + '%"></div></div><span>' +
        (score * 25) + '%</span></div>' +
        '<br><ul class="ta-check">' + rows.join('') + '</ul>' +
        (score >= 4 ? '<strong>这套方案可以进入实现阶段了。</strong>接下来才轮到写程序、选硬件、做联调。'
                    : '<strong>先别急着写程序。</strong>方案没过关，代码写得再好也补不回来——先回到不通过的那一项改。');
    });

    document.getElementById('ps-reset').addEventListener('click', function () {
      sScen = 'air'; sSrc = 'gas'; sLink = 'n2'; sStrat = 's3'; sAct = 'fan';
      document.getElementById('ps-out').className = 'result warn';
      document.getElementById('ps-out').textContent = '五样都选好之后，点「提交评审」。';
      renderSyn();
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：一个方案为什么会「装上就出事」？", TTS["pretest"], [
        {"q": "老师提出的需求是「教室里空气太闷了」。要把它变成可测量的技术指标，最该补上的是：",
         "options": [("测哪个物理量、要求测到多准、多久测一次", True),
                     ("买哪个价格的传感器", False),
                     ("装置外壳用什么颜色", False)],
         "explain": "需求要落地，必须回答三件事：测什么、测多准、多久测一次。这三件事定了，选型才有依据。<strong>错因提醒：</strong>把模糊需求直接当成指标用，是项目设计里最常见的错误。"},
        {"q": "把一个采集间隔从 10 秒改成 60 秒，带来的变化是：",
         "options": [("每天的数据量降到原来的六分之一，但持续几十秒的短事件可能被漏掉", True),
                     ("数据量变大，也更容易漏掉事件", False),
                     ("数据量和漏检风险都不变", False)],
         "explain": "采样频率与数据量成正比，与漏检风险成反比，这是一对必须权衡的量。<strong>错因提醒：</strong>容易误认为只有「采得越勤越好」或「省电就要牺牲一切」，两个方向都不是无条件成立的。"},
        {"q": "用阈值触发上报时，必须搭配迟滞，主要原因是：",
         "options": [("避免数值在阈值附近来回穿越，导致系统反复报警", True),
                     ("让报警的阈值变得更高一些", False),
                     ("可以减少传感器的精度要求", False)],
         "explain": "迟滞让开始报警和解除报警用两个不同的界限，把抖动过滤掉。<strong>错因提醒：</strong>很多同学误认为迟滞只是把阈值抬高了，其实它改变的是报警状态的切换条件，不是报警门槛。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "需求要变成可测量的指标，方案才有依据", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道物联网由感知、网络、应用三层组成，也能把场景拆开看了。但真正动手做项目时会发现，一句「教室里空气不好」根本没法直接去实现，<strong>所以</strong>我们需要先把需求翻译成可测量的技术指标，再让指标去决定选什么传感器、用多快的节奏采集。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">指标必须能被检验。「空气不好」无法检验，<strong>「二氧化碳浓度超过 1500 ppm 时上报」</strong>可以检验——前者是需求，后者才是指标。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>测什么：</strong>选定能代表这个需求的物理量。判断空气闷不闷，二氧化碳浓度比温度更有代表性。</div></div>
          <div class="step"><span class="n">2</span><div><strong>测多准：</strong>确定量程与分辨率，也就是传感器能分辨的最小变化。要求过高会浪费成本，过低会看不出差别。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>多久测一次：</strong>确定采集间隔。它一头连着数据量，一头连着漏检风险，是整套方案里最需要权衡的一个数。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="从模糊需求到可测量技术指标的转换过程示意图">
          <figcaption>需求 → 指标：把「太闷了」翻译成测什么、测多准、多久测一次三件事，选型才有依据</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">📏</span><div><strong>记忆锚点：</strong>把指标想象成一把尺子——尺子上必须有刻度，说不清刻度在哪里的要求，都不是指标。谁都能拿这把尺子量一遍、得到同样的结论，才算合格。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一个需求可以对应不同指标：测温度、测二氧化碳、测人数都能部分反映「闷」，但它们的检验标准和成本完全不同。"},
    {"lens": "拆开它", "text": "任何一个采集指标都能拆成三段：测什么（对象）、测多准（精度）、多久一次（频率）。三项缺一项，方案就落不了地。"},
    {"lens": "迁移它", "text": "这种把模糊要求翻译成可检验条款的做法到处都在用：体检报告有参考区间，考试评分有量规，工程验收有验收标准。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "指标换算台：采多久一次，才又准又省？", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">拖动三个滑块，看看采样间隔、设备台数和事件持续时间如何共同决定数据量与漏检风险。</p>
        <div class="lab-panel">
          <div id="p1-stage">
            <div class="slider-row">
              <label for="p1-gap">采样间隔</label>
              <input type="range" id="p1-gap" min="1" max="120" step="1" value="10">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">间隔</span><span class="v" id="p1-gap-val">10 秒</span></span>
            </div>
            <div class="slider-row">
              <label for="p1-dev">设备台数</label>
              <input type="range" id="p1-dev" min="1" max="20" step="1" value="4">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">台数</span><span class="v" id="p1-dev-val">4 台</span></span>
            </div>
            <div class="slider-row">
              <label for="p1-dur">事件持续时间</label>
              <input type="range" id="p1-dur" min="5" max="300" step="5" value="60">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">持续</span><span class="v" id="p1-dur-val">60 秒</span></span>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">每台每天</span><span class="v" id="p1-perdev">—</span></div>
            <div class="readout-cell"><span class="k">全部设备每天</span><span class="v" id="p1-total">—</span></div>
            <div class="readout-cell"><span class="k">每天数据量</span><span class="v green" id="p1-size">—</span></div>
            <div class="readout-cell"><span class="k">一年数据量</span><span class="v" id="p1-year">—</span></div>
          </div>
          <p class="result warn" id="p1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>动手找一找：</strong>把间隔拖到 90 秒，事件持续还是 60 秒，看看会发生什么。再反过来把它拖到 5 秒，看看数据量涨到什么程度。你会发现，这两个指标是一对——想抓得住短事件，就得付出更大的数据量。</div></div>
    ''', tag="设计实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "上报要按需要来：定时上报与阈值触发", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>采集和上报是两件事。</strong>采集是在设备这边按节奏读传感器，上报是把数据送到平台。很多方案在这两件事上搞混了：采集很快，上报也跟着很快，结果电池三天就没了。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>定时上报</strong></p>
            <p style="color:var(--muted)">每隔固定时间报一次。实现简单、数据完整、平台好统计；代价是不管有没有变化都要报，费电也费流量。</p>
          </div>
          <div class="inner-card">
            <p><strong>变化与阈值触发上报</strong></p>
            <p style="color:var(--muted)">只在数值跨过阈值或明显变化时才报。省电、省流量、提醒有针对性；代价是平台看到的是事件而不是连续曲线。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="定时上报与阈值触发上报两种策略的对照示意图">
          <figcaption>定时上报（按固定节奏取点）与阈值触发上报（只在跨过界限时上报，配合迟滞防止反复报警）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易搞混的是<strong>把迟滞当成「把阈值抬高」</strong>。迟滞真正做的事是给报警状态的切换加两个不同的界限：开始报警用高一点的界，解除报警用低一点的界。它不改变你要防的那个界限，只是把抖动挡在外面。另一个常见错误是<strong>忘了失败重试与本地缓存</strong>——网络一断数据就丢，等恢复时那段记录永远补不回来。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "上报策略设计器：这一天该报几次？", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">下面是某间教室一天二十四小时的温度记录。切换两种上报模式，拖动阈值与迟滞，看上报次数和漏报情况怎么变。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-p2-mode="td" style="text-align:center">定时上报</button>
            <button class="choice" data-p2-mode="th" style="text-align:center">阈值触发上报</button>
          </div>
          <div id="p2-stage" style="margin-top:14px">
            <div class="slider-row">
              <label for="p2-th">报警阈值</label>
              <input type="range" id="p2-th" min="20" max="36" step="0.5" value="30">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">阈值</span><span class="v" id="p2-th-val">30.0 ℃</span></span>
            </div>
            <div class="slider-row">
              <label for="p2-hys">迟滞带宽</label>
              <input type="range" id="p2-hys" min="0" max="6" step="0.5" value="1">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">迟滞</span><span class="v" id="p2-hys-val">1.0 ℃</span></span>
            </div>
            <div class="slider-row">
              <label for="p2-period">定时周期</label>
              <input type="range" id="p2-period" min="1" max="12" step="1" value="2">
              <span class="readout-cell" style="flex:0 0 100px"><span class="k">周期</span><span class="v" id="p2-period-val">2 小时</span></span>
            </div>
          </div>
          <p style="margin:14px 0 6px;font-weight:700;font-size:14px">这一天的温度（蓝色＝已上报，橙色加划线＝超过阈值但没报）</p>
          <div class="ta-cells" id="p2-cells"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">上报次数</span><span class="v" id="p2-count">—</span></div>
            <div class="readout-cell"><span class="k">上报数据量</span><span class="v green" id="p2-bytes">—</span></div>
          </div>
          <p class="result warn" id="p2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔎</span><div><strong>试出边界：</strong>迟滞拖到 0，看上报次数怎么涨；再拖到 5 以上，看是不是一次都不报了。一个合格的设计，是让系统「该报的时候报，只报该报的」。</div></div>
    ''', tag="设计实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一个能跑却不好用的方案，怎么改？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>有同学的方案是「温度传感器每 1 秒采集一次并立即上报，温度超过 30 ℃ 就报警」。它确实能跑起来，但装到教室里很快就不适用了。请指出问题并给出改进方案。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清目标：</strong>要解决的是「及时发现教室温度过高并提醒」，不是「记录每一秒钟的温度」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>问题一（数据量）：</strong>每秒报一次，一天就是 86400 条，绝大多数是重复的室温数据。电池、流量、平台都撑不住——这是把采集频率和上报频率当成了同一件事。</div></div>
          <div class="step"><span class="n">3</span><div><strong>问题二（抖动）：</strong>只在 30 ℃ 报警，没有迟滞。温度在 30 ℃ 附近上下摆动时，「超限」和「恢复」会反复出现，提醒很快就没人看了。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>改进：</strong>采集保持够快，保证不漏事件；上报改成阈值与变化触发，只在有用的时候报；报警加迟滞（如 30 ℃ 开始、28 ℃ 解除）；再补上上报失败时的重试与本地缓存。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">很多同学误认为<strong>「上报越勤越可靠」</strong>，把采集频率和上报频率混为一谈。其实可靠性来自三件事：该报的时刻报到了、数据没在中断期间丢掉、报警状态不会来回抖动——这三件事都跟「报得勤」没有必然关系。另一处容易搞混的是<strong>把迟滞当成提高阈值</strong>：迟滞改的是状态切换条件，不是报警门槛。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("采集频率和上报频率是两件可以分开设计的事", True),
                     ("采集多快就必须上报多快", False),
                     ("上报频率越高，方案就越可靠", False)],
         "explain": "设备可以密集采集、按需上报，两者分开设计正是省电省流量的关键。<strong>错因提醒：</strong>把采集与上报混为一谈，是这一课最常见的错误，也是耗电方案的主要来源。"},
        {"q": "为了让报警不会被温度的小幅抖动触发，同时又不至于真的超温也不报，正确的做法是：",
         "options": [("给报警状态加上迟滞：开始报警和解除报警各用一个界限", True),
                     ("把报警阈值直接抬高到很高的位置", False),
                     ("把上报频率降到每小时一次", False)],
         "explain": "迟滞把抖动挡在门外，又保留了原本的警戒门槛。<strong>错因提醒：</strong>容易误认为迟滞就是抬高阈值——抬高阈值会让危险真的发生时也报不出来，是另一个常见错误。"},
        {"q": "一个采集点每天上报 24 次、每次 8 字节。对「校园积水预警」这个场景来说，最需要担心的隐患是：",
         "options": [("上报间隔太长，水位快速上涨时可能来不及预警", True),
                     ("一天 192 字节的数据量太大，存不下", False),
                     ("8 字节一条记录，精度一定不够", False)],
         "explain": "这个数据量微不足道，真正的风险在时效：预警类场景要求几乎即时发现。<strong>错因提醒：</strong>常见错误是盯着数据量算账，忽略了场景对响应时间的要求——评估方案要看场景的关键约束，不是看哪个数大。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次评审专家，把方案审到底", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">先选场景，再依次选好感知设备、连接方式、上报策略和触发动作，然后提交评审。</p>
        <div class="lab-panel">
          <div id="ps-stage">
            <p class="result warn" id="ps-brief" style="margin:0 0 14px"></p>
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选择场景</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-ps-scen="air" style="text-align:center">教室空气质量监测</button>
                <button class="choice" data-ps-scen="seat" style="text-align:center">图书馆座位管理</button>
                <button class="choice" data-ps-scen="soil" style="text-align:center">农场土壤监测</button>
                <button class="choice" data-ps-scen="water" style="text-align:center">校园积水预警</button>
              </div>
            </div>
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">② 感知设备</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-ps-sensor="gas" style="text-align:center">气体传感器</button>
                <button class="choice" data-ps-sensor="pir" style="text-align:center">人体红外传感器</button>
                <button class="choice" data-ps-sensor="soil" style="text-align:center">土壤湿度传感器</button>
                <button class="choice" data-ps-sensor="water" style="text-align:center">水位传感器</button>
                <button class="choice" data-ps-sensor="temp" style="text-align:center">温度传感器</button>
              </div>
            </div>
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">③ 连接方式</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-ps-link="n1" style="text-align:center">短距离低功耗无线</button>
                <button class="choice" data-ps-link="n2" style="text-align:center">实验楼局域网无线</button>
                <button class="choice" data-ps-link="n3" style="text-align:center">移动蜂窝网络</button>
              </div>
            </div>
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">④ 上报策略</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-ps-strat="s1" style="text-align:center">每 1 秒定时上报</button>
                <button class="choice" data-ps-strat="s2" style="text-align:center">每 1 分钟定时上报</button>
                <button class="choice" data-ps-strat="s3" style="text-align:center">变化与阈值触发上报</button>
                <button class="choice" data-ps-strat="s4" style="text-align:center">每 1 小时定时上报</button>
              </div>
            </div>
            <div class="slider-row" style="display:block">
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">⑤ 触发动作</div>
              <div class="flex-row" style="margin-top:0">
                <button class="choice" data-ps-act="fan" style="text-align:center">开启通风设备</button>
                <button class="choice" data-ps-act="light" style="text-align:center">开启照明</button>
                <button class="choice" data-ps-act="pump" style="text-align:center">启动灌溉水泵</button>
                <button class="choice" data-ps-act="alarm" style="text-align:center">推送预警提醒</button>
                <button class="choice" data-ps-act="report" style="text-align:center">生成统计报表</button>
              </div>
            </div>
          </div>
          <p class="result warn" id="ps-out" style="margin-top:12px">五样都选好之后，点「提交评审」。</p>
          <div class="flex-row">
            <button class="choice" id="ps-run" style="text-align:center;flex:1">提交评审</button>
            <button class="choice" id="ps-reset" style="text-align:center;flex:1">重新选择</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>如果评审结果里「感知设备与场景匹配」这一项没通过，为什么不能靠改上报策略来补救？</p>
          <textarea id="syn-answer" rows="3" placeholder="因为感知层没采到的数据……换上报策略只能改变……所以必须改的是……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "农场要监测土壤湿度，位置在离机房 1800 米的田里，靠电池供电，每小时上报一次。下面哪种判断最站得住脚？",
         "options": [("距离超过局域网覆盖范围，应选覆盖更远的连接方式；每小时一次的频率对土壤监测是合适的", True),
                     ("数据量不大，所以随便选哪种连接方式都行", False),
                     ("为了保险，应该改成每秒上报一次", False)],
         "explain": "覆盖是这里的硬约束，而土壤湿度变化慢，每小时一次足够。<strong>错因提醒：</strong>「数据量小就随便选」忽略了覆盖距离这个决定性因素；「改成每秒上报」则会把电池迅速耗光。"},
        {"q": "水箱要防止溢流：水位一到溢流口就要立刻关阀。下面哪一种上报策略最合适？",
         "options": [("变化与阈值触发上报，水位跨过警戒线立即上报", True),
                     ("每 1 小时定时上报一次", False),
                     ("每 1 秒定时上报一次，把每一次读数都存到平台", False)],
         "explain": "溢流是必须即时响应的事件，用阈值触发最合适。<strong>错因提醒：</strong>选「每 1 小时」是漏掉了时效要求，选「每秒全存」是把采集与上报混为一谈，两者都是常见错误。"},
        {"q": "一套方案评审时，检查表里有「是否有失败重试与本地缓存」这一项。它要防的是：",
         "options": [("网络中断期间采集到的数据丢失，恢复后也补不回来", True),
                     ("传感器精度不够导致读数不准", False),
                     ("阈值定得太低导致频繁报警", False)],
         "explain": "重试与缓存解决的是数据可靠送达的问题。<strong>错因提醒：</strong>容易搞混的是把这项与精度、阈值问题混在一起——它们分别属于感知层的选型、应用层的策略和网络层的可靠性，要分开看。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>需求 → 指标</strong>：把模糊需求翻译成测什么、测多准、多久测一次；指标不能检验，方案就没有依据。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>采样间隔</strong>：间隔越小数据量越大、漏检风险越小。这两个量此消彼长，要按需要定，不能凭感觉。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>上报策略</strong>：定时上报图完整，阈值触发图省电；迟滞防抖动，重试与缓存防丢失。阈值太低会误报，太高会迟报。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那套装置：</strong>先定指标（测二氧化碳、分辨率到 50 ppm、每分钟采一次），再把采集与上报分开（采集保持每分钟，上报改为阈值与变化触发并加迟滞），最后补上重试与缓存。同样一批零件，改完这几处，它就能长期跑下去了。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「指标、采样间隔、上报策略、迟滞」这四个词，把一个物联网方案的设计思路讲清楚。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说明采样间隔与数据量、漏检风险之间的关系。",
            "写出把「教室里空气太闷」变成可测量指标的三句话。",
            "说出定时上报和阈值触发上报各自的优点和代价。",
        ],
        [
            "为教室空气质量监测写出三项指标，算出每天的数据量，并判断采样间隔是否够用。",
            "某场景温度在阈值附近反复上下摆动。说明加迟滞前后，上报次数会怎么变化，为什么。",
        ],
        [
            "为学校的一个真实需求完成一套方案：场景、感知设备、连接方式、上报策略、触发动作写全。",
            "按检查表自查上面这套方案，至少找出两处问题，写出改进办法并说明理由。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-iot-project",
    "node_id": "it-m-iot-project",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "物联网项目设计",
    "name_en": "Designing an IoT Project",
    "grade": 8,
    "grade_cn": "八年级",
    "domain": "iot-modules",
    "domain_cn": "物联网与模块",
    "lesson_type": "project-design",
    "version": "1.0.0",
    "description": "从一套「装上就出事」的装置出发，学会把模糊需求转换成可测量的技术指标，按采样间隔与设备数量估算数据量与漏检风险，区分定时上报与阈值触发上报并使用迟滞防止反复报警，最后按检查表评审一套完整的物联网方案。",
    "tags": ["物联网项目", "技术指标", "采样间隔", "数据量估算", "上报策略", "迟滞", "方案评审"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「物联网与模块」——设计并实现简单的物联网应用项目。",
    "hero_question": "从「我想做一个装置」到「它真能长期稳定地跑起来」，中间要补上哪些设计环节？",
    "hero_alt": "物联网项目设计知识结构图：需求与指标、数据量与采样、上报策略与评审三栏",
    "hero_caption": "需求 → 指标 → 采样 → 上报 → 评审：指标要能检验 · 数据量要能估算 · 报警要防抖动 · 方案要过关",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "一句模糊的需求怎么变成能量出来的指标？", "d": "「空气太闷」到底该怎么测", "v": "一句模糊的需求怎么变成能量出来的指标"},
        {"t": "采集频率定多少才合适？", "d": "既怕漏掉事件，又怕数据太多", "v": "采集频率定多少才合适"},
        {"t": "报警为什么会在阈值附近乱跳？", "d": "迟滞到底解决了什么问题", "v": "报警为什么会在阈值附近乱跳"},
        {"t": "一套方案怎么在动手之前就发现毛病？", "d": "评审表能查出什么", "v": "一套方案怎么在动手之前就发现毛病"},
    ],
    "objectives": [
        "能把模糊的现场需求转换成测什么、测多准、多久测一次的可测量指标",
        "能根据采样间隔与设备台数估算数据量与存储需求，并判断是否会漏掉真实事件",
        "能区分定时上报与变化阈值上报两种策略，并用迟滞避免在阈值附近反复报警",
        "能按检查表评审一套物联网方案，指出不匹配的环节并给出改进办法",
    ],
    "objectives_plain": [
        "能把模糊的现场需求转换成测什么、测多准、多久测一次的可测量指标",
        "能根据采样间隔与设备台数估算数据量与存储需求，并判断是否会漏掉真实事件",
        "能区分定时上报与变化阈值上报两种策略，并用迟滞避免在阈值附近反复报警",
        "能按检查表评审一套物联网方案，指出不匹配的环节并给出改进办法",
    ],
    "standards": [
        {"content": "设计并实现简单的物联网应用项目。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》物联网与模块 · 初中"},
        {"content": "在真实情境中采集、组织数据，选用恰当的方法分析和呈现数据，并评估方案是否满足需求。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》数据与编码 / 问题解决 · 初中"},
    ],
    "prereqs": ["it-m-iot-concept"],
    "prereqs_name": "物联网概念与架构",
    "prereqs_meta": "it-m-iot-concept",
    "leads_to": ["it-m-open-hardware"],
    "next_meta": "it-m-open-hardware",
    "section_images": ["assets/it-m-iot-project-fig1.webp", "assets/it-m-iot-project-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一套装上就出事的装置，问题往往不在零件，而在设计。带着这个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把需求变成指标，再把指标变成一套经得起评审的方案。",
        "objectives": "看清四件事：需求转指标、估算数据量与漏检、区分两种上报策略并用迟滞、按检查表评审方案。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "指标要能检验：测什么、测多准、多久测一次。三项缺一项，选型就没有依据。",
        "lab-1": "拖采样间隔和事件持续时间，看数据量与漏检风险怎么此消彼长。间隔大于事件持续时长，就会漏。",
        "module-2": "采集和上报是两件事。定时上报图完整，阈值触发图省电；迟滞改的是状态切换条件，不是把门槛抬高。",
        "lab-2": "迟滞拖到 0 看上报次数怎么涨，拖到 5 以上看会不会一次都不报。稳住又不错过，才是合格设置。",
        "worked-example": "四步走：看清目标、找数据量问题、找抖动问题、给出改进。改进要落在采集、上报、迟滞、重试四处。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "先选场景，再看关键量和要求的最迟发现时间。有一次通过不了，就顺着那一项往回改，别只改上报策略。",
        "posttest": "换了农场监测和水箱溢流的新情境，看看你还能不能用上指标换算和上报策略。",
        "summary": "用「指标、采样间隔、上报策略、迟滞」四个词，把一套方案的设计思路讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课是「物联网与模块」领域承接概念课之后的项目设计课。设计上不引入任何品牌、产品与具体平台，把力气花在三件可计算的事上：用指标换算台把「采样间隔」对数据量与漏检的影响变成可读的数字，用上报策略设计器把「迟滞」与「抖动」变成看得见的时间轴，用方案评审工作台让学生在动手之前就按检查表发现问题。全课贯穿一条工程判断：先定指标，再定策略，最忌把采集频率与上报频率混为一谈。价值取向上强调按需采集、节约资源，以及方案落地前先评审的工程习惯。",
    "plan_table": """| 1 | cover | 物联网项目设计 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：一个方案为什么会「装上就出事」？ | 起·前测（暴露直觉） |
| 5 | concept | 需求要变成可测量的指标，方案才有依据 | 承·概念一 |
| 6 | interactive | 指标换算台：采多久一次，才又准又省？ | 承·实验室一（数据量与漏检可估算） |
| 7 | concept | 上报要按需要来：定时上报与阈值触发 | 承·概念二 |
| 8 | interactive | 上报策略设计器：这一天该报几次？ | 承·实验室二（迟滞防抖可观察） |
| 9 | concept | 例题示范：一个能跑却不好用的方案，怎么改？ | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次评审专家，把方案审到底 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：需求与指标 / 数据量与采样 / 上报策略与评审三栏\n- P5 需求转指标示意图（已生成）：模糊需求 → 测什么·测多准·多久测一次\n- P7 两种上报策略对照图（已生成）：定时上报取点 vs 阈值触发上报 + 迟滞\n- 若需补充：采集设备与传感器的实物照片（不带任何品牌标识）",
}
