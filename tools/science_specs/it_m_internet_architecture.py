# -*- coding: utf-8 -*-
"""初中信息科技 · 互联网结构与协议初识（G7）—— 补齐课标「互联网应用与创新」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-internet-architecture-fig1.webp'
F2 = './assets/it-m-internet-architecture-fig2.webp'

TTS = {
    "hero": "先看一个真实的过程。你在教室里按了一下发送，几毫秒之后，另一座城市的一台机器收到了这条消息。中间没有一根线从你这里直接连到那里，你也不知道它到底走了哪条路。这节课我们就来拆开这个看不见的过程：互联网到底是由什么组成的，协议是做什么用的，数据又是怎样一段一段走过去的。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道一条消息到底走了哪条路，还是想知道为什么要把协议分成好几层，又或者你想弄清楚数据被切成一个个小包之后，凭什么还能不丢不乱。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出互联网是许多网络互联而成，并能说明分层的作用。第二，能说出协议是通信双方共同遵守的规则，能对应说出各层的主要职责。第三，能描述数据被切分成数据包、由路由器逐段转发的完整过程。第四，能按自下而上的顺序，分层定位一个网络故障出在哪一层。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "互联网不是一台很大的机器，它是许多网络互联起来形成的网络。这么多设备要互相通信，就必须先约定好规矩，这套规矩就叫协议。把协议分成几层，是为了让每一层只解决一件事：应用层管收发具体的服务请求，传输层管端到端的可靠传输，网络层管寻址和选择路径，网络接口层管在链路上传输信号。上层向下层提出请求，下层为上层提供服务。",
    "lab-1": "现在我们把发送过程跑一遍。先选要发送的数据量，系统会按每个数据包最多携带一千字节把它切开，再让这些包一个一个沿路径转发过去。你可以打开丢包开关，看看其中一个包在路上丢掉之后会发生什么。盯住四个数字：分包数、已送达、重传次数、重组结果。",
    "module-2": "数据不是一整条直接过去的。它被切成许多数据包，每个包有自己的包头，包头里写着源地址、目的地址和序号。路由器连接着不同的网络，它只看包头的目的地址，决定下一跳往哪里送，并不需要知道完整路线。正因为每个包都带地址，它们可以各走各的，到目的地再按序号重新排好。",
    "lab-2": "再来看另一种看不见的过程。你在地址栏里输入的是一个域名，可机器之间只认地址里的数字，中间要做一次翻译，这个过程叫域名解析。点开始解析，你会看到查询一层一层往上走，最后拿回一个地址。拿回地址之后，数据包还要经过若干次转发才能到达目的地，每经过一台路由器，记录的跳数就加一。",
    "worked-example": "我们一起分析一个真实的故障。有同学报告说，他的机器能打开校内的共享文件夹，却打不开外网的一个网站。第一步，看清现象：局域网内通，出网不通。第二步，按分层自下而上定位：先看本机地址配置，再看网关是否可达。第三步，这两层都通过了，说明问题在更上层，于是检查域名解析，发现域名服务器地址配置错误。第四步，说清道理并修复：数据包要送到目的地，必须先拿到对方的地址；地址拿不到，后面的路再通也走不了。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次网络工程师。机房的一台机器打不开图书馆的网站，报修单递到你手上。你要按自下而上的顺序，逐层检查本机地址、网关连通、域名解析、服务端口这四项，把故障定位到具体的某一层，最后交出一份诊断报告。",
    "posttest": "最后用新情境检验一下。这次出现了视频卡顿和换一台设备就正常的情况，看看你能不能把分层和分包的知识用上去。",
    "summary": "这节课我们弄明白了三件事。第一，互联网是许多网络互联形成的网络，协议是通信双方共同遵守的规则，分层是为了让每一层只解决一件事。第二，数据被切成带有序号和地址的数据包，由路由器逐段转发，到目的地再按序号重排。第三，排查网络问题要自下而上分层定位，先确认本机地址和网关，再看域名解析，最后看服务端口。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出四层的名称和各自的主要职责，并说出协议在通信中起什么作用。第二层能力应用，动手做：画出一次发送过程中数据包从本机到服务器的路径，标出每一步负责转发的是哪一类设备。第三层迁移挑战，选做：找一个你遇到过的上网问题，写一份自下而上的排查步骤，说明你判断故障在哪一层的依据。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 网络的网络与协议分层", "lab-1": "实验室一 数据包传输模拟器",
    "module-2": "概念二 数据包、地址与转发", "lab-2": "实验室二 域名解析与路径",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 分层排障", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-flow { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.ta-node { flex: 1; min-width: 66px; text-align: center; padding: 10px 6px; border-radius: 10px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); font-size: 13px; font-weight: 700; }
.ta-node.hot { border-color: var(--brand); background: var(--brand-soft); color: var(--text-strong); }
.ta-pkts { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 12px; }
.ta-pkt { display: flex; flex-direction: column; align-items: center; justify-content: center;
  width: 54px; height: 54px; border-radius: 10px; font-size: 13px; font-weight: 800;
  font-variant-numeric: tabular-nums; background: var(--bg-subtle); border: 1px solid var(--line-subtle); }
.ta-pkt small { font-weight: 600; color: var(--muted); font-size: 10px; margin-top: 2px; }
.ta-pkt.wait { opacity: .55; }
.ta-pkt.fly { border-color: var(--brand); background: var(--brand-soft); }
.ta-pkt.ok { border-color: var(--brand-2); background: var(--brand-2-soft); }
.ta-pkt.lost { border-color: var(--danger); background: rgba(239, 68, 68, .10); color: var(--danger); }
.ta-log { list-style: none; margin: 10px 0 0; padding: 0; font-size: 13.5px; }
.ta-log li { padding: 7px 10px; border-radius: 8px; margin-bottom: 6px;
  border-left: 3px solid var(--line-subtle); background: var(--bg-subtle); color: var(--text-secondary); }
.ta-log li.ok { border-left-color: var(--brand-2); color: var(--text-strong); }
.ta-log li.bad { border-left-color: var(--danger); color: var(--text-strong); background: rgba(239, 68, 68, .07); }
.ta-log li.now { border-left-color: var(--brand); color: var(--text-strong); background: var(--brand-soft); }
.ta-pick { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-internet-architecture 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 数据包传输模拟器：分包 → 转发 → 丢包 → 重传 → 重组
   3) 域名解析与路径跳数
   4) 分层排障工作台：自下而上定位故障层
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. 选择题 ---------- */
  document.querySelectorAll('[data-quiz-block]').forEach(function (block) {
    block.querySelectorAll('.choice').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (block.dataset.answered === '1') return;
        block.dataset.answered = '1';
        btn.classList.add(btn.dataset.correct === '1' ? 'correct' : 'wrong');
        block.querySelectorAll('.choice').forEach(function (b) {
          if (b.dataset.correct === '1') b.classList.add('correct');
          b.disabled = true;
        });
        var ex = block.querySelector('[data-explain]');
        if (ex) ex.style.display = 'block';
      });
    });
  });

  /* ---------- 2. 数据包传输模拟器 ---------- */
  var PAYLOAD = 1;                 /* 每个数据包最多携带 1 千字节 */
  var HOP_MS = 420;                /* 每个包经过一跳的演示耗时 */
  var l1 = document.getElementById('lab1-stage');

  if (l1) {
    var eSize = document.getElementById('l1-size');
    var eSizeV = document.getElementById('l1-size-val');
    var eCount = document.getElementById('l1-count');
    var eArrived = document.getElementById('l1-arrived');
    var eRetry = document.getElementById('l1-retry');
    var eState = document.getElementById('l1-state');
    var eBox = document.getElementById('l1-packets');
    var eOut = document.getElementById('l1-out');
    var eLoss = document.getElementById('l1-loss');
    var eSend = document.getElementById('l1-send');
    var eReset = document.getElementById('l1-reset');
    var nodeEls = l1.querySelectorAll('[data-hop]');

    var packets = [], retry = 0, lossOn = true, running = false, timer = null;

    function sizeKb() { return Number(eSize.value); }
    function packetTotal() { return Math.ceil(sizeKb() / PAYLOAD); }

    function build() {
      packets = [];
      var n = packetTotal();
      for (var i = 1; i <= n; i++) packets.push({ id: i, bytes: PAYLOAD, state: '待发' });
      retry = 0;
      running = false;
      if (timer) { clearInterval(timer); timer = null; }
      eSend.disabled = false;
      eSend.textContent = '发送数据';
      render();
    }

    function markNodes(idx) {
      nodeEls.forEach(function (el, k) { el.classList.toggle('hot', k === idx); });
    }

    function render() {
      var arrived = packets.filter(function (p) { return p.state === '已送达'; }).length;
      var lost = packets.filter(function (p) { return p.state === '丢失'; }).length;
      eCount.textContent = packets.length + ' 个';
      eArrived.textContent = arrived + ' / ' + packets.length;
      eRetry.textContent = String(retry);
      eState.textContent = lost > 0 ? '缺少 ' + lost + ' 个包' : (arrived === packets.length ? '完整' : '待发');

      eBox.innerHTML = '';
      packets.forEach(function (p) {
        var d = document.createElement('div');
        d.className = 'ta-pkt';
        if (p.state === '在途') d.className += ' fly';
        else if (p.state === '已送达') d.className += ' ok';
        else if (p.state === '丢失') d.className += ' lost';
        else d.className += ' wait';
        d.innerHTML = '第 ' + p.id + ' 包<small>' + p.state + '</small>';
        eBox.appendChild(d);
      });
    }

    function summary() {
      var arrived = packets.filter(function (p) { return p.state === '已送达'; }).length;
      var missing = packets.filter(function (p) { return p.state !== '已送达'; });
      if (missing.length === 0) {
        markNodes(3);
        eOut.className = 'result';
        eOut.innerHTML = '<strong>重组成功：</strong>' + packets.length + ' 个数据包按序号一、二、三……重排，' +
          '还原出 ' + sizeKb() + ' 千字节的完整数据。' + (retry > 0 ? '这一次一共重传了 ' + retry + ' 次。' : '');
      } else {
        eOut.className = 'result error';
        eOut.innerHTML = '<strong>暂时无法重组：</strong>接收方还缺 ' + missing.length + ' 个包（' +
          missing.map(function (p) { return '第 ' + p.id + ' 包'; }).join('、') +
          '）。接收方不会凭猜测补上缺失的内容，它会要求发送方重传。';
      }
    }

    eSend.addEventListener('click', function () {
      if (running) return;
      running = true;
      eSend.disabled = true;
      eSend.textContent = '正在发送…';
      var lostId = lossOn ? 3 : -1;
      if (lostId > packets.length) lostId = -1;
      var i = 0;

      timer = setInterval(function () {
        if (i >= packets.length) {
          clearInterval(timer); timer = null;
          markNodes(3);
          var lostList = packets.filter(function (p) { return p.state === '丢失'; });
          if (lostList.length > 0) {
            retry += 1;
            render();
            eOut.className = 'result warn';
            eOut.innerHTML = '<strong>发生丢包：</strong>第 ' + lostList[0].id +
              ' 包没有到达接收方。传输层会启动超时重传，把这个包再发一次——重传次数加一。';
            setTimeout(function () {
              lostList.forEach(function (p) { p.state = '已送达'; });
              render(); summary();
              eSend.textContent = '发送数据';
              running = false;
            }, 1100);
          } else {
            summary();
            eSend.textContent = '发送数据';
            running = false;
          }
          return;
        }
        var p = packets[i];
        markNodes(i < packets.length / 2 ? 1 : 2);
        p.state = '在途';
        render();
        setTimeout(function () {
          p.state = (lostId === p.id) ? '丢失' : '已送达';
          render();
          if (p.state === '丢失') {
            eOut.className = 'result warn';
            eOut.innerHTML = '<strong>第 ' + p.id + ' 包在路上丢失了。</strong>' +
              '注意：后面的包照常往前走，不会因为前面丢了一个就全部停下来——这正是分组交换的特点。';
          }
        }, HOP_MS * 0.6);
        i += 1;
      }, HOP_MS);
    });

    eLoss.addEventListener('click', function () {
      lossOn = !lossOn;
      eLoss.textContent = lossOn ? '丢包开关：开' : '丢包开关：关';
      eLoss.classList.toggle('selected', lossOn);
    });
    eReset.addEventListener('click', build);
    eSize.addEventListener('input', function () {
      eSizeV.textContent = sizeKb() + ' 千字节';
      markNodes(0);
      build();
    });

    eLoss.classList.add('selected');
    eSizeV.textContent = sizeKb() + ' 千字节';
    markNodes(0);
    build();
  }

  /* ---------- 3. 域名解析与路径跳数 ---------- */
  var DOMAINS = {
    library: { name: '图书室.example', ip: '203.0.113.42', hops: 5, ms: 3 },
    study: { name: '学习角.example', ip: '203.0.113.18', hops: 6, ms: 4 },
    weather: { name: '气象站.example', ip: '198.51.100.7', hops: 8, ms: 6 }
  };
  var l2 = document.getElementById('lab2-stage');

  if (l2) {
    var eLog = document.getElementById('l2-log');
    var eOut2 = document.getElementById('l2-out');
    var eIp = document.getElementById('l2-ip');
    var eHops = document.getElementById('l2-hops');
    var eCost = document.getElementById('l2-cost');
    var eGo = document.getElementById('l2-go');
    var eHop = document.getElementById('l2-hop');
    var curDomain = 'library';
    var busy = false, timer2 = null, timer3 = null;

    function chain(d) {
      return [
        { t: '本机缓存', m: '查本机最近的记录：没有 ' + d.name + '，缓存未命中。', ok: false },
        { t: '本地域名服务器', m: '把问题转给本地域名服务器：它也没有这条记录，需要继续往上问。', ok: false },
        { t: '根域名服务器', m: '根域名服务器不直接给出地址，它回答：这个域名归顶级域服务器管，去问它。', ok: false },
        { t: '顶级域服务器', m: '顶级域服务器回答：这个域名的权威记录在那台权威域名服务器上。', ok: false },
        { t: '权威域名服务器', m: '权威域名服务器给出最终答案：' + d.name + ' 对应的地址是 ' + d.ip + '。', ok: true }
      ];
    }

    function clearAll() {
      if (timer2) { clearInterval(timer2); timer2 = null; }
      if (timer3) { clearInterval(timer3); timer3 = null; }
      eLog.innerHTML = '';
      eIp.textContent = '—';
      eHops.textContent = '—';
      eCost.textContent = '—';
      eHop.textContent = '—';
      eGo.disabled = false;
      eGo.textContent = '开始解析';
      busy = false;
    }

    function pick(key) {
      curDomain = key;
      document.querySelectorAll('[data-l2-domain]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.l2Domain === key);
      });
      clearAll();
      eOut2.className = 'result warn';
      eOut2.innerHTML = '已选域名 <strong>' + DOMAINS[key].name + '</strong>，点「开始解析」看它怎样一步步被翻译成地址。';
    }

    document.querySelectorAll('[data-l2-domain]').forEach(function (b) {
      b.addEventListener('click', function () { if (!busy) pick(b.dataset.l2Domain); });
    });

    eGo.addEventListener('click', function () {
      if (busy) return;
      busy = true;
      eGo.disabled = true;
      var d = DOMAINS[curDomain];
      var steps = chain(d);
      var i = 0;
      eLog.innerHTML = '';
      eIp.textContent = '解析中…';
      eGo.textContent = '解析中…';
      timer2 = setInterval(function () {
        if (i >= steps.length) {
          clearInterval(timer2); timer2 = null;
          eIp.textContent = d.ip;
          eCost.textContent = d.ms + ' 毫秒';
          eOut2.className = 'result';
          eOut2.innerHTML = '<strong>解析完成：</strong>域名 ' + d.name + ' 翻译成地址 ' + d.ip +
            '，一共问了 5 层，耗时约 ' + d.ms + ' 毫秒。拿到地址之后，数据包才谈得上往哪里送。';
          eGo.textContent = '解析完成';
          return;
        }
        var s = steps[i];
        var li = document.createElement('li');
        li.className = s.ok ? 'ok' : 'now';
        li.innerHTML = '<strong>第 ' + (i + 1) + ' 步 · ' + s.t + '</strong>：' + s.m;
        eLog.appendChild(li);
        i += 1;
      }, 620);
    });

    eHop.addEventListener('click', function () {
      var d = DOMAINS[curDomain];
      if (timer3) { clearInterval(timer3); timer3 = null; }
      var ttl = 64, k = 0;
      eHops.textContent = '0 跳';
      eHop.disabled = true;
      eHop.textContent = '转发中…';
      timer3 = setInterval(function () {
        k += 1;
        ttl -= 1;
        eHops.textContent = k + ' 跳';
        eOut2.className = 'result warn';
        eOut2.innerHTML = '<strong>第 ' + k + ' 跳：</strong>数据包抵达第 ' + k +
          ' 台路由器，它只看包头里的目的地址 ' + d.ip + '，把包转给下一跳；同时把剩余生存时间减到 ' + ttl + '。';
        if (k >= d.hops) {
          clearInterval(timer3); timer3 = null;
          eOut2.className = 'result';
          eOut2.innerHTML = '<strong>已抵达目的地：</strong>从本机到 ' + d.name + ' 一共经过 ' + d.hops +
            ' 台路由器。注意：每一台都只知道自己该往哪里转，没有哪一台掌握完整路线。';
          eHop.disabled = false;
          eHop.textContent = '再走一遍';
        }
      }, 700);
    });

    eOut2.className = 'result warn';
    eOut2.innerHTML = '先选一个域名，点「开始解析」看地址是怎么来的；再点「看数据包怎么走」看它经过几跳。';
    eHops.textContent = '—';
    document.querySelectorAll('[data-l2-domain]').forEach(function (b) {
      b.classList.toggle('selected', b.dataset.l2Domain === curDomain);
    });
  }

  /* ---------- 4. 分层排障工作台 ---------- */
  var CHECKS = [
    { id: 'addr', layer: '本机地址', order: 1,
      pass: true, ok: '本机地址 10.20.30.41，掩码 24 位，默认网关 10.20.30.1。地址配置正常。',
      bad: '本机没有拿到有效地址，后面所有检查都无从谈起。' },
    { id: 'gw', layer: '网关连通', order: 2,
      pass: true, ok: '网关 10.20.30.1 回应耗时 1 毫秒，本机到本地网络这段是通的。',
      bad: '网关没有回应，说明问题就在本地这一段。' },
    { id: 'dns', layer: '域名解析', order: 3,
      pass: false, ok: '域名解析正常，拿到了目标地址。',
      bad: '向域名服务器 10.20.30.254 发出查询，一直没有回应，超时。域名换不成地址，后面的路再通也没用。' },
    { id: 'port', layer: '服务端口', order: 4,
      pass: true, ok: '直接使用地址 203.0.113.42 的 443 端口，连接建立成功，页面能打开。',
      bad: '目标端口没有响应，说明服务本身不可用。' }
  ];
  var syn = document.getElementById('syn-stage');

  if (syn) {
    var eSynLog = document.getElementById('syn-log');
    var eSynOut = document.getElementById('syn-out');
    var eSynFix = document.getElementById('syn-fix');
    var done = {}, visited = 0, orderWarn = 0;

    function refreshSyn() {
      document.querySelectorAll('[data-syn-check]').forEach(function (b) {
        var c = CHECKS.filter(function (x) { return x.id === b.dataset.synCheck; })[0];
        b.classList.toggle('selected', !!done[c.id]);
      });
    }

    document.querySelectorAll('[data-syn-check]').forEach(function (b) {
      b.addEventListener('click', function () {
        var id = b.dataset.synCheck;
        if (done[id]) return;
        var c = CHECKS.filter(function (x) { return x.id === id; })[0];
        var earlierOpen = CHECKS.filter(function (x) { return x.order < c.order && !done[x.id]; });

        var li = document.createElement('li');
        li.className = c.pass ? 'ok' : 'bad';
        li.innerHTML = '<strong>检查' + c.order + ' · ' + c.layer + '</strong>：' + (c.pass ? c.ok : c.bad);
        eSynLog.appendChild(li);
        done[id] = true;
        visited += 1;
        refreshSyn();

        var prefix = '';
        if (earlierOpen.length > 0) {
          orderWarn += 1;
          prefix = '<strong>提醒：</strong>你跳过了更靠下的「' +
            earlierOpen.map(function (x) { return x.layer; }).join('、') +
            '」。工程上排查网络问题习惯自下而上：下层的问题会让上层一起失灵，先查下层才不会白跑。<br>';
        }

        if (!c.pass) {
          eSynOut.className = 'result error';
          eSynOut.innerHTML = prefix + '<strong>故障定位：</strong>问题出在「' + c.layer +
            '」这一层。前面几层都通过了，说明线路和地址都没问题，是这一步把后面的路断了。';
          eSynFix.style.display = 'block';
          eSynFix.className = 'result';
          eSynFix.innerHTML = '<strong>修复方案：</strong>把本机的域名服务器地址改成正确的 ' +
            '10.20.30.53，再重新解析一次即可。改完之后，从本机到网关、从域名到地址、从地址到服务端口，链条才完整。';
        } else {
          eSynOut.className = 'result warn';
          eSynOut.innerHTML = prefix + '<strong>这一层通过：</strong>继续往下（更靠近应用）检查，看看断点在哪里。';
        }
      });
    });

    eSynFix.style.display = 'none';
    eSynOut.className = 'result warn';
    eSynOut.textContent = '按自下而上的顺序，依次检查四项。每查一项都会给出这一层的结果。';
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：网络到底是怎么连起来的？", TTS["pretest"], [
        {"q": "关于「互联网」，下面哪种说法更准确？",
         "options": [("互联网是许多网络互相连接形成的网络", True),
                     ("互联网就是一台容量特别大的服务器", False),
                     ("互联网就是一根很长的网线，把所有电脑串起来", False)],
         "explain": "互联网的名字本来就说明了它的结构：网络与网络互联。任何一台机器都只是其中一个节点。<strong>错因提醒：</strong>把互联网想成一台大机器，是最常见的一类误解，它会让你在后面理解转发与寻址时处处卡住。"},
        {"q": "通信双方要能互相听懂，最不能缺的是什么？",
         "options": [("双方共同遵守的一套规则，也就是协议", True),
                     ("两台机器用同一个厂家的产品", False),
                     ("两边的网速必须完全一样", False)],
         "explain": "只要双方遵守同一套协议，用什么设备、什么线路都能互通——这正是协议存在的意义。"},
        {"q": "为什么要把网络通信的规则分成好几层，而不是写成一大本？",
         "options": [("分层之后，每一层只解决一件事，改一层不影响其他层", True),
                     ("分层只是为了方便背诵", False),
                     ("层数越多传输速度越快", False)],
         "explain": "分层是一种分工：上层向下层提出请求，下层为上层提供服务。某一层的技术更新了，其他层可以不动。这个问题先记在心里，等下我们看数据包的时候会用上。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "互联网是网络的网络，协议分层让每一层各管一件事", TTS["module-1"], f'''
        {LAB_CSS}
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道，两台计算机之间可以互相传文件；但当联网的设备从两台变成几百万台，链路从一种变成几十种，<strong>但真正的问题出现了</strong>：谁规定怎么开口、怎么找路、出错了怎么办？<strong>所以</strong>需要一套共同遵守的规则（协议），并且把它分层，让每一层只解决一件事。这就是网络工程师每天打交道的对象。</p>
        </div>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>互联网：网络的网络</strong></p>
            <p style="color:var(--muted)">终端设备连到本地网络，本地网络通过路由器接入更大的网络。你发出的数据不会走一条专属的线，而是被一段一段接力送过去。</p>
          </div>
          <div class="inner-card">
            <p><strong>协议：共同遵守的规则</strong></p>
            <p style="color:var(--muted)">协议规定了数据长什么样、按什么顺序交换、出了错怎么处理。只要遵守同一套协议，不同设备、不同线路都能互通。</p>
          </div>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>应用层：</strong>收发具体的服务请求，比如取一个页面、发一条消息。</div></div>
          <div class="step"><span class="n">2</span><div><strong>传输层：</strong>负责端到端的传输，管住数据是否到达、是否需要重传。</div></div>
          <div class="step"><span class="n">3</span><div><strong>网络层：</strong>负责寻址与选择路径，决定这个包下一步交给谁。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>网络接口层：</strong>负责在具体的链路上把信号送出去。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="四层协议模型示意图：应用层、传输层、网络层、网络接口层及各自职责">
          <figcaption>分层模型：上层向下层提出请求，下层为上层提供服务；每一层只解决一件事</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧭</span><div><strong>记忆锚点：</strong>像寄快递。你只管把东西交给快递点（应用层），快递公司负责逐站转运（网络层），最后一段由派件员送到门口（网络接口层）。你不需要知道它走了哪条高速，只要地址写对。</div></div>
{insight_box([
    {"lens": "拆开它", "text": "任何一次通信都能拆成同一条链条：上层说要做什么 → 下层负责把这件事送到 → 到了对面再一层层交回去。"},
    {"lens": "解释它", "text": "为什么必须分层？因为下层一改，全世界的设备都要跟着改。分层把变化关在了一层的门里。"},
    {"lens": "迁移它", "text": "打电话、寄信、点外卖背后也是同样的分层协作——每一层只需要把自己的那一件事做对。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "数据包传输模拟器：分包、转发、丢包、重传", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">先选要发送的数据量，再点「发送数据」。打开丢包开关，你会看到其中一个包在路上丢掉之后，整个流程是怎样补救的。</p>
        <div class="lab-panel" id="lab1-stage">
          <div class="ta-flow">
            <div class="ta-node hot" data-hop="0">本机</div>
            <div class="ta-node" data-hop="1">路由器一</div>
            <div class="ta-node" data-hop="2">路由器二</div>
            <div class="ta-node" data-hop="3">服务器</div>
          </div>
          <div class="slider-row">
            <label for="l1-size">数据量</label>
            <input type="range" id="l1-size" min="1" max="12" step="1" value="4">
            <span class="readout-cell" style="flex:0 0 120px"><span class="k">要发送</span><span class="v" id="l1-size-val">4 千字节</span></span>
          </div>
          <div class="ta-pkts" id="l1-packets"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分包数</span><span class="v" id="l1-count">—</span></div>
            <div class="readout-cell"><span class="k">已送达</span><span class="v green" id="l1-arrived">—</span></div>
            <div class="readout-cell"><span class="k">重传次数</span><span class="v" id="l1-retry">0</span></div>
            <div class="readout-cell"><span class="k">接收方状态</span><span class="v" id="l1-state">待发</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="l1-send" style="text-align:center;flex:1">发送数据</button>
            <button class="choice" id="l1-loss" style="text-align:center;flex:1">丢包开关：开</button>
            <button class="choice" id="l1-reset" style="text-align:center;flex:1">重新开始</button>
          </div>
          <p class="result warn" id="l1-out" style="margin-top:12px">点「发送数据」开始。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📦</span><div><strong>注意看两件事：</strong>第一，每个包只带一小块数据，所以出错时只需要重传一个包，不用把整份数据重发。第二，丢了一个包，后面的包照样继续往前走——它们各自独立，到目的地再按序号重排。</div></div>
    ''', tag="网络实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "数据被切成带地址的数据包，由路由器逐段转发", TTS["module-2"], f'''
        {LAB_CSS}
        <p style="font-size:17px;margin:0 0 12px">数据不是一整条直接过去的。它被<strong>切成许多数据包</strong>，每个包自带包头，包头里写着目的地址和序号。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>包头里有什么</strong></p>
            <p style="color:var(--muted)">源地址、目的地址、序号。地址告诉网络这个包要去哪里，序号让接收方知道该把它排在第几位。</p>
          </div>
          <div class="inner-card">
            <p><strong>路由器做什么</strong></p>
            <p style="color:var(--muted)">路由器连接着不同的网络。它只看包头里的目的地址，决定下一跳交给谁，并不需要知道完整路线。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="分组交换示意图：数据被切成带编号的数据包，经路由器逐段转发后按编号重组">
          <figcaption>分组交换：一份数据切成若干带编号的包，各自沿路径转发，到目的地按编号重新排好</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少同学误认为数据是「一整条」从出发地直达目的地的，还误认为路由器上存着一张完整的地图、知道全程怎么走。事实是：每个包只带着目的地址上路，每一台路由器只负责把它交给更接近目的地的下一跳。</p>
        </div>
        <div class="inner-card">
          <p><strong>还有一件必须知道的事：</strong>数据包要经过许多台不属于你的设备才能到达对面。如果内容是明文，任何一台设备上都能被读取。<strong>所以</strong>承载敏感信息的传输必须加密——这也是安全传输协议存在的根本原因。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "域名解析与路径：域名怎样变成地址，包又走了几跳", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">机器之间只认地址里的数字，可我们输入的是域名。先看这一次翻译是怎么完成的，再看数据包实际要走几跳。</p>
        <div class="lab-panel">
          <p style="margin:0 0 6px"><strong>① 选一个域名</strong></p>
          <div class="ta-pick">
            <button class="choice" data-l2-domain="library" style="text-align:center">图书室.example</button>
            <button class="choice" data-l2-domain="study" style="text-align:center">学习角.example</button>
            <button class="choice" data-l2-domain="weather" style="text-align:center">气象站.example</button>
          </div>
          <div class="lab-readout" style="margin-top:12px">
            <div class="readout-cell"><span class="k">解析出的地址</span><span class="v" id="l2-ip">—</span></div>
            <div class="readout-cell"><span class="k">解析耗时</span><span class="v green" id="l2-cost">—</span></div>
            <div class="readout-cell"><span class="k">经过跳数</span><span class="v" id="l2-hops">—</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="l2-go" style="text-align:center;flex:1">开始解析</button>
            <button class="choice" id="l2-hop" style="text-align:center;flex:1">看数据包怎么走</button>
          </div>
          <div id="lab2-stage"><ul class="ta-log" id="l2-log"></ul></div>
          <p class="result warn" id="l2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔎</span><div><strong>观察：</strong>解析是从下往上一步步问出来的，没有人手里存着全世界的域名表。等换一个域名再解析一次，你会发现耗时和跳数都不一样——路径是逐台设备接力决定的。</div></div>
    ''', tag="网络实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：局域网通、外网不通，问题出在哪一层", TTS["worked-example"], f'''
        {LAB_CSS}
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(245,158,11,.55)">
          <p style="margin:0"><strong>题目：</strong>一间机房里，一台机器能打开校内的共享文件夹，却怎么也打不开外网的一个网站。请判断问题最可能出在哪一层，并说明你的排查过程。</p>
        </div>
        <div class="inner-card">
          <p style="margin:0 0 6px"><strong>第一步　看清现象：</strong>局域网内通，出外网不通。这说明本机和本地网络这一段是好的。</p>
          <p style="margin:0 0 6px"><strong>第二步　先查更靠下的层：</strong>本机地址、掩码、默认网关是否配置正确；网关能不能回应。</p>
          <p style="margin:0 0 6px"><strong>第三步　再往上查：</strong>网关既然通，就检查域名解析。结果发现向域名服务器发出的查询一直没有回应。</p>
          <p style="margin:0"><strong>第四步　定位并修复：</strong>问题出在域名解析这一层——域名服务器地址配置错了。改成正确的地址后重新解析，页面立刻就能打开。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易犯的错是一上来就重启设备，或者直接下结论「断网了」。还有人误认为「能打开校内共享文件夹，就说明网络没问题」——其实局域网通只证明最下面两层是好的，上面几层完全没有验证过。排查网络问题的正确姿势是<strong>自下而上、逐层排除</strong>：下层不通，上层必然不可用；下层通了，才轮到查上层。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("数据被切成数据包传输，其中一个包丢了只需要重传这一个包", True),
                     ("数据必须整块一起传输，中间断开就要全部重发", False),
                     ("数据包一定会沿着同一条路线按顺序到达", False)],
         "explain": "分包的意义正在于此：出错时只补发受影响的那一小块。<strong>错因提醒：</strong>很多同学误认为数据包会按发送顺序、走同一条路到达；实际上它们可以各走各的，靠序号在目的地重排。"},
        {"q": "路由器决定把一个数据包往哪里送，主要依据是：",
         "options": [("包头里的目的地址", True),
                     ("数据包里装的内容", False),
                     ("发这个包的人是谁", False)],
         "explain": "路由器只看目的地址，选一个更接近目的地的下一跳，不需要读懂包里的内容。<strong>错因提醒：</strong>容易误认为路由器要打开包看内容才能转发——如果需要看内容，那加密传输就没法实现了。"},
        {"q": "有人把网页地址换成了另一台服务器的地址，页面就打不开了。如果只能改一个地方，最该先检查的是：",
         "options": [("域名解析得到的地址是否正确", True),
                     ("显示屏的亮度", False),
                     ("本机的键盘是否好用", False)],
         "explain": "域名要先被翻译成地址，包才谈得上往哪里送。翻译错了，后面的路全错。<strong>错因提醒：</strong>遇到「打不开」就断定是线路问题，是常见的错误判断；这一次断的其实是上面那一层。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：按分层顺序，把故障定位到具体一层", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">报修单：机房 3 号机打不开图书馆网站。你有四项检查权限，请按自下而上的顺序使用它们，找出断点在哪一层。</p>
        <div class="lab-panel">
          <div class="ta-pick" id="syn-stage">
            <button class="choice" data-syn-check="addr" style="text-align:center">检查一 · 本机地址</button>
            <button class="choice" data-syn-check="gw" style="text-align:center">检查二 · 网关连通</button>
            <button class="choice" data-syn-check="dns" style="text-align:center">检查三 · 域名解析</button>
            <button class="choice" data-syn-check="port" style="text-align:center">检查四 · 服务端口</button>
          </div>
          <ul class="ta-log" id="syn-log"></ul>
          <p class="result warn" id="syn-out" style="margin-top:12px"></p>
          <p class="result" id="syn-fix" style="margin-top:10px;display:none"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>你是按什么顺序检查的？为什么这个顺序比随机点开一项更省时间？如果把「检查三」放在第一步就点了，你会得到什么结论，又可能错过什么？</p>
          <textarea id="syn-answer" rows="3" placeholder="我先查……因为……如果先点检查三，我会以为……"></textarea>
        </div>
    ''', tag="综合任务", bloom="analyze"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "看在线视频时画面偶尔卡一下，但聊天消息照常收发。最合理的解释是：",
         "options": [("视频数据量大，被切成很多包，只要有一个包没能及时补上，画面就会停顿一下", True),
                     ("网络彻底断了，只是恰好还能发消息", False),
                     ("聊天消息的传输不需要经过网络", False)],
         "explain": "视频对时延和丢包比文字更敏感，同样的链路下，包多、量大的那一方先受影响。这正是分包与重传机制要做的事。"},
        {"q": "同一间教室里，你的机器打不开某个页面，借来同桌的机器却能打开。最先该怀疑的是：",
         "options": [("问题出在你这台机器自己的配置上，而不是整条线路", True),
                     ("整个网络都瘫痪了", False),
                     ("那个页面本身被删掉了", False)],
         "explain": "同一时间、同一网络下只有一台机器异常，说明公共部分（链路、网关、域名服务器）是好的，差异只在这台机器自己。<strong>错因提醒：</strong>把个别机器的问题当成全网故障，是排查时最常见的误判。"},
        {"q": "一位同学说：「我知道目的地址是 203.0.113.42，所以我的机器一定知道全部路线。」这句话：",
         "options": [("不准确，知道目的地址不等于知道完整路线，路线是逐台设备接力决定的", True),
                     ("完全正确", False),
                     ("只在网络空闲时正确", False)],
         "explain": "每一台路由器只需要知道自己该把包交给谁。谁都不掌握全程，但包依然能到——这就是逐段转发的妙处。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>结构</strong>：互联网是许多网络互联形成的网络；协议是通信双方共同遵守的规则。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>分层</strong>：应用层收发请求，传输层管端到端可靠传输，网络层管寻址与选路，网络接口层管链路上的信号；上层提请求，下层提供服务。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>传输</strong>：数据切成带有序号和地址的数据包，由路由器逐段转发，到目的地按序号重排；丢了哪一个就重传哪一个。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(245,158,11,.55)">
          <p style="margin:0"><strong>回到开头那一下发送：</strong>你按下的那一刻，应用层把内容交下去，传输层把它切成若干数据包并记下序号，网络层给每个包写上目的地址，网络接口层把它送上网线；接着一台台路由器只看地址、逐段接力，最后在对面按序号重排还原。整个过程没有人掌握全局，却准确完成了。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「协议、分层、数据包、地址」这四个词，说清楚一条消息从你这里到对面经历了什么。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出四层协议模型的名称，并为每一层写一句「它负责什么」。",
            "用自己的话说出「协议」的含义：协议规定了哪三件事（数据长什么样、按什么顺序交换、出错怎么办）？",
            "画出一个数据包的包头示意，标出源地址、目的地址、序号分别放在哪里。",
        ],
        [
            "画出一次发送过程：从本机出发，经过两台路由器，到达服务器。在图上标出每一段负责转发的是哪一类设备。",
            "把模拟器里的数据量从 4 千字节改成 10 千字节，记录分包数和重传次数，说明它们为什么这样变化。",
            "记录一次真实的域名解析：换两个不同的域名各解析一次，把解析出的地址、耗时、跳数填进表格并比较。",
        ],
        [
            "为自己遇到过的某一个上网问题，写一份自下而上的排查步骤，说明你判断断点在哪一层的依据。",
            "查阅资料了解：为什么传送敏感信息的传输必须加密？请从「数据包要经过许多台设备」这个角度解释，并给出两条你可以做到的保护个人信息的做法。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-internet-architecture",
    "node_id": "it-m-internet-architecture",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "互联网结构与协议初识",
    "name_en": "Internet Architecture and Protocols: An Introduction",
    "grade": 7,
    "grade_cn": "七年级",
    "domain": "internet-innovation",
    "domain_cn": "互联网应用与创新",
    "lesson_type": "concept-simulation",
    "version": "1.0.0",
    "description": "从一次真实的发送出发，认识互联网是许多网络互联形成的网络，理解协议分层「每层只管一件事」的设计，掌握数据分包、地址寻址与路由器逐段转发的完整过程，并能按自下而上的顺序分层定位网络故障。",
    "tags": ["互联网结构", "协议", "分层", "数据包", "域名解析", "路由器", "分层排障"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「互联网应用与创新」——理解互联网基本结构，知道常见协议的作用；能对常见网络问题作出初步判断。",
    "hero_question": "你按了一下发送，数据穿过看不见的网络到达另一台机器——它到底走了哪条路，按什么规则走？",
    "hero_alt": "互联网知识与协议结构图：网络结构、协议分层、数据传输三栏",
    "hero_caption": "网络结构 · 协议分层 · 数据传输：互联网是网络的网络，每层只管一件事，数据分包逐段转发",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "一条消息是怎么走过去的？", "d": "中间没有一根线直连，它是怎么到的", "v": "一条消息是怎么走过去的"},
        {"t": "为什么要把协议分成好几层？", "d": "不分层会有什么麻烦", "v": "为什么要把协议分成好几层"},
        {"t": "数据被切成一个个包，凭什么不丢不乱？", "d": "丢了包以后发生了什么", "v": "数据被切成一个个包凭什么不丢不乱"},
        {"t": "输入域名就能打开页面，中间发生了什么？", "d": "域名和地址是什么关系", "v": "输入域名就能打开页面中间发生了什么"},
    ],
    "objectives": [
        "能说出互联网是许多网络互联形成的网络，并说明协议分层的作用",
        "能说出协议是通信双方共同遵守的规则，并能对应说出各层的主要职责",
        "能描述数据被切分成数据包、由路由器逐段转发的完整过程，说明丢失重传与按序号重排",
        "能按自下而上的顺序分层定位一个网络故障，说明判断依据",
    ],
    "objectives_plain": [
        "能说出互联网是许多网络互联形成的网络，并说明协议分层的作用",
        "能说出协议是通信双方共同遵守的规则，并能对应说出各层的主要职责",
        "能描述数据被切分成数据包、由路由器逐段转发的完整过程，说明丢失重传与按序号重排",
        "能按自下而上的顺序分层定位一个网络故障，说明判断依据",
    ],
    "standards": [
        {"content": "理解互联网基本结构，知道常见协议的作用。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》互联网应用与创新 · 初中"},
        {"content": "能对身边的网络使用现象作出解释，具备初步的网络问题排查意识与信息安全意识。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》互联网应用与创新 · 初中"},
    ],
    "prereqs": [],
    "prereqs_name": "无（初中互联网起点）",
    "prereqs_meta": "无",
    "leads_to": ["it-m-web-development", "it-m-cloud-collaboration"],
    "next_meta": "it-m-web-development",
    "section_images": ["assets/it-m-internet-architecture-fig1.webp", "assets/it-m-internet-architecture-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "你按了一下发送，数据穿过看不见的网络到了另一台机器。它走了哪条路？带着这个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己讲清一次发送的完整过程，并能判断故障出在哪一层。",
        "objectives": "看清四件事：说出互联网的结构、说出协议分层的作用、描述分包与转发、按层定位故障。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "互联网是网络的网络；协议是共同遵守的规则；分层是为了让每一层只解决一件事。",
        "lab-1": "盯住四个数字：分包数、已送达、重传次数、接收方状态。打开丢包开关看补救过程。",
        "module-2": "数据切成带地址和序号的数据包；路由器只看目的地址决定下一跳；到目的地按序号重排。",
        "lab-2": "先看域名怎么一层层被翻译成地址，再看数据包经过了几跳、每跳做了什么。",
        "worked-example": "四步走：看清现象、先查下层、再查上层、定位并修复。重点记住自下而上。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "按自下而上的顺序点四项检查。跳过下层会有提醒，想想为什么工程上要这样排。",
        "posttest": "换了视频卡顿和换机器就正常的场景，看看你还能不能用上分层与分包。",
        "summary": "用「协议、分层、数据包、地址」四个词，把一次发送讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「互联网应用与创新」领域长期空缺的入门一课。设计上不出现任何具体厂商设备与软件产品，只用通用的结构、协议与设备类别名称，把力气花在三件可观察的事上：用分包传输模拟器把「切包—转发—丢包—重传—重组」变成看得见的实时状态，用域名解析与跳数演示把「域名换地址」和「逐段接力」变成可测量的数据，用分层排障工作台让学生亲手把故障定位到某一层。价值取向上，全课贯穿「掌握全局的其实没有任何一台设备」这一结构之美，并在概念二点明数据包要经过多处设备、敏感信息必须加密的防护意识。",
    "plan_table": """| 1 | cover | 互联网结构与协议初识 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：网络到底是怎么连起来的？ | 起·前测（暴露直觉） |
| 5 | concept | 互联网是网络的网络，协议分层让每一层各管一件事 | 承·概念一 |
| 6 | interactive | 数据包传输模拟器：分包、转发、丢包、重传 | 承·实验室一（状态可观察） |
| 7 | concept | 数据被切成带地址的数据包，由路由器逐段转发 | 承·概念二 |
| 8 | interactive | 域名解析与路径：域名怎样变成地址，包又走了几跳 | 承·实验室二（数据可测量） |
| 9 | concept | 例题示范：局域网通、外网不通，问题出在哪一层 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：按分层顺序，把故障定位到具体一层 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：网络结构 / 协议分层 / 数据传输三栏标注\n- P5 四层协议模型图（已生成）：应用层 / 传输层 / 网络层 / 网络接口层及各自职责\n- P7 分组交换示意图（已生成）：切包 → 经路由器转发 → 按编号重组，含丢包重传标注\n- 若需补充：教室内交换机与路由器端口的实拍照片（用于情境引入，需去除厂商标识）",
}
