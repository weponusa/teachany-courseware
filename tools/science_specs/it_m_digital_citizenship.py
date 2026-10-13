# -*- coding: utf-8 -*-
"""初中信息科技 · 信息社会责任与数字公民（G9）—— 补齐课标「人工智能与智慧社会」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-digital-citizenship-fig1.webp'
F2 = './assets/it-m-digital-citizenship-fig2.webp'

TTS = {
    "hero": "先看一件几乎每天都在发生的事。班级群里出现一条消息，说下周作息要有变化。第一眼看上去它像真的：有截图，有具体时间，语气也很急。半小时之内，这条消息被转到了几十个群里。可是没有人能说清它最初是谁发的。技术课教会了我们怎么保护数据不被拿走，却没有回答另一个问题：这条消息，我到底该不该转出去？这节课我们要弄清楚的是——在数字社会里，一个负责任的成员应该怎么做。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道一条消息到底怎么判断真假，还是想知道转发到底要不要承担责任，又或者你想亲手试一次：如果换一种做法，这条消息会走到哪里去。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出数字公民的含义，知道权利和责任是一起出现的。第二，能说出信息社会责任的三个层面：守住法律底线、遵守伦理规范、保持理性参与。第三，能在模拟器里观察一条消息的传播过程，说出核实为什么能让失真停下来。第四，能对一个真实情境里的处置动作逐条判断：它守住了哪一条责任，又放大了哪一种风险。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "数字公民，是指在数字社会中生活、学习、参与的成员。这个身份和现实里的公民身份一样，权利和责任是一起出现的：你有获取信息、表达意见、使用服务的权利，同时也要承担相应的责任。责任落在三个层面上。第一是法律底线：不造谣、不传谣，不侵犯他人的隐私和肖像，不侵害他人的知识产权。第二是伦理规范：尊重他人，诚实表达，不利用信息不对称去欺骗。第三是理性参与：核实来源，独立思考，不被情绪推着走。请注意，这三个层面不是口号，它们各自对应着可以观察、可以判断的具体行为。",
    "lab-1": "光说转发要慎重，说服力不够，我们把传播过程跑一遍。左边可以选择转发的速度和两个开关，点开始之后，每一轮的新增触达人数、累计人数和消息失真度都会实时算出来，消息本身的样子也会跟着变形。请你自己对比两组：核实关闭时跑到底，和核实打开时跑到底，看看累计触达和失真度差了多少。你会发现，核实让传播变慢，但它换来的是失真不再累积，以及澄清能追上来。",
    "module-2": "在数字社会里，最容易踩的是三条线。第一条是真实性线：未经核实的消息不转发，因为信息在每一次转述里都会走样，转发的人越多，走样越厉害。第二条是尊重线：不窥探、不传播他人的隐私与肖像，引用他人的成果要注明出处，这是知识产权的基本要求。第三条是边界线：用人工智能生成的内容要标注清楚，不能拿它冒充真人或真实事件；而推荐算法会把我们圈在同类信息里，需要主动拓宽信息面。这三条线对应的是同一个判断：我做的这件事，会不会让别人受到伤害。",
    "lab-2": "现在看第二条技术性的影响。推荐算法会记录你点开过什么，然后把你更可能点击的内容排到前面。这个循环是自动完成的，你甚至感觉不到它。下面有四个内容品类和一个多样性指数，点几次同一类，看看指数会掉到什么位置；再试试每轮换一类，看看指数能不能维持。指数低意味着什么，请你自己说出来。",
    "worked-example": "我们一起判断一条消息。班级群里出现一条消息：说下周作息有调整，附了一张看不清出处的截图。请决定转还是不转，并说明理由。第一步，看来源：谁发的、什么时候、有没有署名和原始出处。第二步，交叉核对：这件事实在权威渠道能不能找到同样的说法。第三步，评估影响：如果它是错的，会波及哪些人、造成什么后果。第四步，定位责任：我在这条传播链里处于什么位置，我转发之后要承担什么。第五步，处置：不转，或者转到求证渠道，或者转发的同时附上你核实到的结论。走完这五步，答案往往就清楚了。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次内容审核员。场景是班级公众号要发一篇科普文章：它是用人工智能辅助生成的，素材从网上转载，配图里出现了同学的照片，原始出处一时找不到。左边有七个可以做的动作，你来决定做哪几个，然后点评估。系统会按真实性、知情同意、知识产权、表述严谨四个维度逐条判断，最后给出残余风险评分。要特别留意：有的动作看起来是在帮忙，其实是在放大风险。",
    "posttest": "最后用新情境检验一下。这次出现了群里的求助信息、公开的聊天记录和删不掉的转发，看看你能不能把三个责任层面用上去。",
    "summary": "这节课我们弄明白了三件事。第一，数字公民的含义是：在数字社会里，权利和责任是一起出现的。第二，责任落在三个层面——法律底线、伦理规范、理性参与，每一个都能落到具体行为上。第三，核实让传播变慢，却让失真停下来，也让澄清有机会追上来，这就是负责任的做法在数据上的样子。回到开头那条消息：它的真假也许一时查不清，但要不要转发，是当下就能决定的一件事。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出数字公民的三个责任层面，各配一个具体行为。第二层能力应用，动手做：用课堂上的传播模拟器做两组对照，记录累计触达和失真度，写一句话说明核实换来了什么。第三层迁移挑战，选做：找一个真实发生过的网络传言，梳理它的传播链条，标出可以介入的三个环节，并为每个环节设计一个具体做法。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 数字公民与三层责任", "lab-1": "实验室一 传播链模拟器",
    "module-2": "概念二 真实·尊重·边界三条线", "lab-2": "实验室二 推荐与视野模拟器",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 内容审核台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-log { list-style: none; margin: 0; padding: 0; font-size: 14px; }
.ta-log li { padding: 8px 10px; margin-bottom: 6px; border-radius: 10px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); white-space: pre-wrap; }
.ta-log li .tag { display: inline-block; margin-right: 8px; padding: 1px 8px; border-radius: 999px;
  font-size: 12px; font-weight: 700; background: var(--brand-soft); color: var(--brand); }
.ta-log li.bad { border-color: var(--danger); }
.ta-log li.ok { border-color: var(--ok); }
.ta-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
.ta-tag { padding: 4px 10px; border-radius: 999px; font-size: 13px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); color: var(--text-secondary); }
.ta-tag.warn { background: var(--warm-soft); border-color: var(--warm); color: var(--text-strong); font-weight: 700; }
.ta-tag.ok { background: var(--brand-2-soft); border-color: var(--brand-2); color: var(--text-strong); font-weight: 700; }
.sw-wrap { display: grid; grid-template-columns: 1fr; gap: 8px; }
.sw { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 12px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); cursor: pointer; font-size: 14px; }
.sw .dot { flex: 0 0 34px; height: 20px; border-radius: 999px; background: rgb(var(--paper-rgb) / .3); position: relative; transition: background .2s; }
.sw .dot::after { content: ""; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; border-radius: 50%; background: #fff; transition: transform .2s; }
.sw.on .dot { background: var(--brand); }
.sw.on .dot::after { transform: translateX(14px); }
.sw.on { border-color: var(--brand); background: var(--brand-soft); }
.sw .name { font-weight: 700; }
.sw .desc { color: var(--muted); font-size: 13px; }
.bar-row { display: flex; align-items: center; gap: 10px; font-size: 13px; margin-top: 8px; }
.bar-row .lab { flex: 0 0 92px; color: var(--muted); }
.bar-track { flex: 1; height: 12px; border-radius: 999px; background: rgb(var(--paper-rgb) / .18); overflow: hidden; }
.bar-fill { display: block; height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .3s ease; }
.bar-fill.danger { background: var(--danger); }
.bar-fill.warnbar { background: var(--warm); }
.bar-row .val { flex: 0 0 92px; text-align: right; font-variant-numeric: tabular-nums; font-weight: 700; }
.msg-card { position: relative; border-radius: 14px; padding: 14px 16px; background: var(--card);
  border: 1px solid var(--line-subtle); box-shadow: 0 4px 14px rgb(var(--paper-rgb) / .16); }
.msg-card .who { font-size: 12px; color: var(--muted); margin-bottom: 6px; }
.msg-card .body { font-size: 15px; font-weight: 700; line-height: 1.6; }
.dot-row { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 10px; }
.dot-row i { width: 10px; height: 10px; border-radius: 50%; background: var(--brand); display: block; }
.dot-row i.pale { background: rgb(var(--paper-rgb) / .3); }
.stream { list-style: none; margin: 0; padding: 0; }
.stream li { display: flex; align-items: center; gap: 10px; padding: 7px 10px; margin-bottom: 6px;
  border-radius: 10px; background: var(--bg-subtle); border: 1px solid var(--line-subtle); font-size: 14px; }
.stream li .nm { flex: 0 0 88px; font-weight: 700; }
.stream li .pc { flex: 0 0 52px; text-align: right; font-variant-numeric: tabular-nums; font-weight: 700; }
.stream li .track { flex: 1; height: 10px; border-radius: 999px; background: rgb(var(--paper-rgb) / .18); overflow: hidden; }
.stream li .track span { display: block; height: 100%; border-radius: 999px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-digital-citizenship 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 传播链模拟器：传播速度 × 核实开关 × 旧消息识别 → 触达 / 失真度 / 风险等级
   3) 推荐流与视野模拟器：点击偏好 → 内容分布 → 观点多样性指数
   4) 内容审核台：6 个处置动作 × 4 个责任维度 → 逐条判定与残余风险
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

  /* ---------- 2. 传播链模拟器 ---------- */
  var MAX_INFORMED = 300;
  var s1 = document.getElementById('s1-stage');
  if (s1) {
    var st1 = { round: 0, informed: 1, distortion: 0, halted: false, verify: false, old: false, fanout: 3 };

    /* 失真度越高，消息在转述中丢掉的原始信息越多 */
    function claimOf(d) {
      if (d <= 0) return '原话：某班级群通知，下周作息时间可能有调整。';
      if (d < 40) return '转述一次：说是下周作息要变，具体时间记不清了。';
      if (d < 70) return '转述多次：下周要提前放假，时间就在这两天。';
      return '已经走样成另一件事：下周全校停课，通知都发出来了。';
    }

    function render1() {
      document.getElementById('s1-round').textContent = st1.round + ' 轮';
      document.getElementById('s1-reach').textContent = st1.informed + ' 人';
      document.getElementById('s1-dist').textContent = st1.distortion + ' / 100';
      var body = document.getElementById('s1-msg');
      body.textContent = claimOf(st1.distortion);
      body.style.color = st1.distortion >= 70 ? 'var(--danger)' : (st1.distortion >= 40 ? 'var(--warm-deep)' : 'var(--text-strong)');
      document.getElementById('s1-dots').innerHTML =
        new Array(Math.min(st1.informed, 60)).join('<i></i>') + '<i></i>' +
        (st1.informed > 60 ? '<span style="font-size:12px;color:var(--muted);align-self:center;margin-left:6px">后面还有 ' + (st1.informed - 60) + ' 人</span>' : '');

      var dBar = document.getElementById('s1-dbar');
      dBar.style.width = st1.distortion + '%';
      dBar.className = 'bar-fill' + (st1.distortion >= 70 ? ' danger' : (st1.distortion >= 40 ? ' warnbar' : ''));
      document.getElementById('s1-dval').textContent = st1.distortion >= 70 ? '高' : (st1.distortion >= 40 ? '中' : '低');

      document.getElementById('s1-verify').classList.toggle('on', st1.verify);
      document.getElementById('s1-old').classList.toggle('on', st1.old);
      document.querySelectorAll('[data-s1-fan]').forEach(function (b) {
        b.classList.toggle('selected', Number(b.dataset.s1Fan) === st1.fanout);
      });
    }

    function log1(rows, cls) {
      var el = document.getElementById('s1-out');
      el.className = 'result ' + (cls || 'warn');
      el.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
    }

    function step1() {
      if (st1.halted) return false;
      var rows = [];
      st1.round += 1;
      var before = st1.informed;
      var add;
      if (st1.verify) {
        add = Math.max(1, Math.round(before * 1.6)) - before;
        st1.informed = Math.min(MAX_INFORMED, before + add);
        rows.push('<li class="ok"><span class="tag">第 ' + st1.round + ' 轮</span>转发前先核实来源：新增 ' + add +
          ' 人，累计 ' + st1.informed + ' 人。核实要花时间，传播明显变慢。</li>');
        rows.push('<li class="ok"><span class="tag">失真度</span>保持 ' + st1.distortion +
          ' / 100。每一手转述前都被校准过，原始信息没有被替换掉。</li>');
      } else {
        add = before * st1.fanout;
        st1.informed = Math.min(MAX_INFORMED, before + add);
        st1.distortion = Math.min(100, st1.distortion + 18);
        rows.push('<li class="bad"><span class="tag">第 ' + st1.round + ' 轮</span>直接转发：新增 ' + add +
          ' 人，累计 ' + st1.informed + ' 人。</li>');
        rows.push('<li class="bad"><span class="tag">失真度</span>升到 ' + st1.distortion +
          ' / 100。消息每被转述一次，就丢掉一点原始信息，也被补上一点猜测。</li>');
      }
      if (st1.old) {
        st1.halted = true;
        rows.push('<li class="ok"><span class="tag">时间线核对</span>发现这条消息是三天前的，当时就已经被澄清过。传播在第 ' +
          st1.round + ' 轮停下来——核对时间线，是最省力的一步。</li>');
      } else if (st1.verify && st1.round >= 2) {
        st1.halted = true;
        rows.push('<li class="ok"><span class="tag">澄清追上来了</span>因为有人在转发前核对了来源，澄清信息得以沿着同一条链条回传，传播在第 ' +
          st1.round + ' 轮停下来。</li>');
      }
      if (st1.distortion >= 70 && !st1.halted) {
        rows.push('<li class="bad"><span class="tag">注意</span>失真度过高，消息已经变成另一件事。这时候再澄清，代价要大得多——被误导的人需要先接受「自己刚才传错了」。</li>');
      }
      if (!st1.halted && st1.round >= 5) {
        st1.halted = true;
        rows.push('<li class="bad"><span class="tag">达到观察上限</span>已经跑了 5 轮，这条消息的传播还在继续。请把两个开关打开再跑一次，对比同一条消息会走到哪里去。</li>');
      }
      if (st1.halted) {
        var cls = st1.verify || st1.old ? '' : 'error';
        rows.push('<li class="' + (cls ? 'bad' : 'ok') + '"><span class="tag">结果</span>共 ' + st1.round +
          ' 轮，累计触达 ' + st1.informed + ' 人，失真度 ' + st1.distortion + ' / 100。' +
          (st1.verify || st1.old
            ? '核实换来的不是「传播得更快」，而是「信息没有走样、澄清来得及」。'
            : '请对比一下：如果再开一次核实，同样跑到底，这两个数字会变成多少。') + '</li>');
      }
      log1(rows, st1.halted ? (st1.distortion >= 70 ? 'error' : '') : 'warn');
      render1();
      return !st1.halted;
    }

    document.getElementById('s1-verify').addEventListener('click', function () { st1.verify = !st1.verify; render1(); });
    document.getElementById('s1-old').addEventListener('click', function () { st1.old = !st1.old; render1(); });
    document.querySelectorAll('[data-s1-fan]').forEach(function (b) {
      b.addEventListener('click', function () { st1.fanout = Number(b.dataset.s1Fan); render1(); });
    });
    document.getElementById('s1-step').addEventListener('click', function () { step1(); });
    document.getElementById('s1-run').addEventListener('click', function () {
      for (var i = 0; i < 5; i++) { if (!step1()) break; }
    });
    document.getElementById('s1-reset').addEventListener('click', function () {
      st1 = { round: 0, informed: 1, distortion: 0, halted: false, verify: st1.verify, old: st1.old, fanout: st1.fanout };
      log1(['<li><span class="tag">已重置</span>发布者 1 人，失真度 0 / 100。设置好开关和速度，再点开始。</li>'], 'warn');
      render1();
    });
    log1(['<li><span class="tag">准备就绪</span>发布者 1 人，失真度 0 / 100。选好转发的速度与开关，然后点「走一轮」或「跑到底」。</li>'], 'warn');
    render1();
  }

  /* ---------- 3. 推荐流与视野模拟器 ---------- */
  var CATS = [
    { k: 'sport', n: '体育' },
    { k: 'game', n: '游戏' },
    { k: 'sci', n: '科普' },
    { k: 'news', n: '时事' }
  ];
  var s2 = document.getElementById('s2-stage');
  if (s2) {
    var w = { sport: 25, game: 25, sci: 25, news: 25 };
    var clicks = 0, streak = '';

    function norm() {
      var sum = 0;
      CATS.forEach(function (c) { sum += w[c.k]; });
      if (sum <= 0) return;
      CATS.forEach(function (c) { w[c.k] = w[c.k] / sum * 100; });
    }
    /* 香农熵归一化到 0–100：四类完全平均时为 100，全押一类时趋近 0 */
    function diversity() {
      var h = 0;
      CATS.forEach(function (c) {
        var p = w[c.k] / 100;
        if (p > 0) h -= p * Math.log(p) / Math.LN2;
      });
      return h / 2 * 100;
    }

    function render2() {
      var ul = document.getElementById('s2-stream');
      ul.innerHTML = CATS.map(function (c) {
        var v = w[c.k];
        return '<li><span class="nm">' + c.n + '</span><span class="track"><span style="width:' + v.toFixed(1) + '%"></span></span>' +
          '<span class="pc">' + v.toFixed(1) + '%</span></li>';
      }).join('');
      var d = diversity();
      document.getElementById('s2-div').textContent = d.toFixed(0) + ' / 100';
      var bar = document.getElementById('s2-divbar');
      bar.style.width = Math.max(0, d) + '%';
      bar.className = 'bar-fill' + (d < 40 ? ' danger' : (d < 70 ? ' warnbar' : ''));
      document.getElementById('s2-clicks').textContent = clicks + ' 次';
      var out = document.getElementById('s2-out');
      if (clicks === 0) {
        out.className = 'result warn';
        out.textContent = '现在四类内容各占 25%，多样性指数 100。点几次你感兴趣的那一类，看看分布会怎样变化。';
        return;
      }
      var top = CATS.slice().sort(function (a, b) { return w[b.k] - w[a.k]; })[0];
      var grade = d < 40 ? '很窄' : (d < 70 ? '偏窄' : '较宽');
      out.className = 'result ' + (d < 40 ? 'error' : (d < 70 ? 'warn' : ''));
      out.innerHTML = '<strong>本轮之后：' + top.n + '类内容已经占到 ' + w[top.k].toFixed(1) +
        '%，视野广度指数 ' + d.toFixed(0) + ' / 100，属于「' + grade + '」。</strong><br>' +
        '机制说清楚：算法只是把你点开过的东西排到前面，它没有替你决定要看什么，是你每一次点击在给它指令。' +
        '指数下降不会报错、不会有提示，这才是它最难被发现的地方。<br>' +
        '<strong>易错点：</strong>很多同学误认为「推荐不准是算法的问题」。事实上，只看同一类内容次数越多，指数就越低，' +
        (streak && clicks >= 3 ? '你已经连续点了同一类 ' + clicks + ' 次。' : '换着点几类，指数可以维持住。') +
        '主动拓宽信息面，是可以由自己完成的一步。';
    }

    document.querySelectorAll('[data-s2-cat]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.s2Cat;
        clicks += 1;
        CATS.forEach(function (c) { w[c.k] = (c.k === k) ? w[c.k] * 1.5 : w[c.k] * 0.9; });
        norm();
        render2();
      });
    });
    document.getElementById('s2-reset').addEventListener('click', function () {
      w = { sport: 25, game: 25, sci: 25, news: 25 };
      clicks = 0; render2();
    });
    render2();
  }

  /* ---------- 4. 内容审核台 ---------- */
  var DIMS = {
    truth: { n: '真实性', weight: 35, note: '来源可追溯、内容经过核实' },
    consent: { n: '知情同意与肖像', weight: 25, note: '涉及他人影像、信息要先取得同意' },
    ip: { n: '知识产权与出处', weight: 20, note: '转载要注明出处，尊重原作者' },
    rigor: { n: '表述严谨', weight: 20, note: '不夸大、不把推测说成结论' }
  };
  var ACTS = [
    { k: 'verify', n: '追溯原始来源与发布时间', desc: '找到最初发布者与时间线', up: 'truth', down: null },
    { k: 'label', n: '标注「本文由 AI 辅助生成」', desc: '向读者说明内容的生产方式', up: 'truth', down: null },
    { k: 'consent', n: '取得照片中同学的同意，或做遮挡处理', desc: '涉及他人影像的先取得同意', up: 'consent', down: null },
    { k: 'credit', n: '注明转载出处与原作者', desc: '按规范标注来源', up: 'ip', down: null },
    { k: 'factcheck', n: '逐句核对数据与结论，去掉没有出处的绝对化说法', desc: '把「一定」「必然」换回有依据的表述', up: 'rigor', down: null },
    { k: 'smooth', n: '把「可能」改成「一定」，标题更吸引人', desc: '提高点击率的常见做法', up: null, down: 'rigor' },
    { k: 'quick', n: '先发布出去，被指出问题再改', desc: '抢时效的常见做法', up: null, down: 'truth' }
  ];
  var syn = document.getElementById('syn-stage');
  if (syn) {
    var on = {}, ran = false;
    ACTS.forEach(function (a) { on[a.k] = false; });

    function renderSyn() {
      ACTS.forEach(function (a) {
        var el = document.getElementById('syn-sw-' + a.k);
        if (el) el.classList.toggle('on', on[a.k]);
      });
      var out = document.getElementById('syn-out');
      if (!ran) {
        out.className = 'result warn';
        out.textContent = '选好要做的动作，然后点「评估这份内容」。';
      }
    }
    document.querySelectorAll('[data-syn-sw]').forEach(function (el) {
      el.addEventListener('click', function () {
        on[el.dataset.synSw] = !on[el.dataset.synSw];
        ran = false; renderSyn();
      });
    });
    document.getElementById('syn-run').addEventListener('click', function () {
      var rows = [], left = 0, covered = 0;
      Object.keys(DIMS).forEach(function (dk) {
        var D = DIMS[dk];
        var ups = ACTS.filter(function (a) { return a.up === dk && on[a.k]; });
        var downs = ACTS.filter(function (a) { return a.down === dk && on[a.k]; });
        var stopped = ups.length > 0;
        if (stopped) covered += 1;
        var risk = stopped ? (downs.length ? Math.round(D.weight * 0.5) : 0) : D.weight;
        left += risk;
        rows.push('<li class="' + (risk === 0 ? 'ok' : 'bad') + '"><span class="tag">' + D.n + '</span>' +
          (stopped
            ? (risk === 0
                ? '已守住。' + ups.map(function (a) { return a.n; }).join('；') + '，' + D.note + '。'
                : '只守住一半。已经做了「' + ups.map(function (a) { return a.n; }).join('；') +
                  '」，但同时又选了「' + downs.map(function (a) { return a.n; }).join('；') +
                  '」，把刚守住的那部分又削弱了，残余风险计 ' + risk + ' 分。')
            : '没有守住。' + D.note + '，目前没有任何一个动作对上这一项，残余风险 ' + D.weight + ' 分。') + '</li>');
      });
      var score = left;
      var level = score <= 15 ? '低' : (score <= 45 ? '中' : '高');
      rows.push('<li class="' + (score <= 45 ? 'ok' : 'bad') + '"><span class="tag">评估</span>四个责任维度中已守住 ' +
        covered + ' 个，残余风险 ' + score + ' 分，风险等级：<strong>' + level + '</strong>。</li>');
      var harmful = ACTS.filter(function (a) { return a.down && on[a.k]; });
      if (harmful.length) {
        rows.push('<li class="bad"><span class="tag">提示</span>「' + harmful.map(function (a) { return a.n; }).join('」和「') +
          '」看起来是在提高传播效果，实际上是在放大风险。它们不解决任何一个责任维度，只会让自己变成问题的一部分。</li>');
      }
      if (score === 0) {
        rows.push('<li class="ok"><span class="tag">完成</span>四个维度都被守住。请记住：这份清单不复杂，难的是发布之前肯不肯走一遍。</li>');
      }
      var out = document.getElementById('syn-out');
      out.className = 'result ' + (score <= 15 ? '' : (score <= 45 ? 'warn' : 'error'));
      out.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
      ran = true;
    });
    document.getElementById('syn-reset').addEventListener('click', function () {
      ACTS.forEach(function (a) { on[a.k] = false; });
      ran = false; renderSyn();
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这条消息你会怎么处理？", TTS["pretest"], [
        {"q": "群里有人转发一条「下周作息要调整」的消息，附了一张看不清出处的截图，还说是朋友的朋友发的。下面哪种做法更合适？",
         "options": [("先不转，到权威渠道核对，确认不了就不往外发", True),
                     ("看着像真的，先转到自己班上，让大家有个准备", False),
                     ("截图在这里，随手一转不算什么，反正不是我编的", False)],
         "explain": "判断的第一件事是来源能不能追溯。截图可以伪造，\"朋友的朋友\"等于没有来源。<strong>错因提醒：</strong>常见错误是误认为「不是我编的就不用负责」——传播本身就是参与，链条上每一手都在放大后果。"},
        {"q": "关于「数字公民」这个说法，下面哪一句更准确？",
         "options": [("在数字社会里，获取信息和表达意见的权利，与相应的责任是一起出现的", True),
                     ("只要不上网，就不需要承担信息社会责任", False),
                     ("数字公民就是会用各种软件的人", False)],
         "explain": "数字公民强调的是成员身份，权利和责任同时存在，与熟练程度无关。<strong>错因提醒：</strong>容易把「会操作」当成「负责任」，这是把技能和素养搞混了。"},
        {"q": "一条消息被很多人反复转述之后，内容常常和最初不一样。最合理的解释是：",
         "options": [("每一手转述都会丢掉一部分原始信息，也被补上一点猜测，失真会累积", True),
                     ("是第一个发消息的人故意改了内容", False),
                     ("转的人多了，消息自己会变", False)],
         "explain": "失真来自转述过程本身，不一定有人故意造假。转发的人越多、越不核实，走样越厉害。<strong>错因提醒：</strong>不要一看到走样就认定有人恶意篡改，那样会忽略掉真正可以控制的那个环节。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "数字公民：权利和责任是一起出现的", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道数据可以被采集、传输和存储，也学过怎么识别风险、怎么配置防护。<strong>但</strong>那些办法解决的都是「别人来拿走我的数据」——它们回答不了另一个问题：我在数字社会里做过的事，会带来什么后果。<strong>所以</strong>我们需要一套判断「我该怎么做」的准则，这就是信息社会责任，也是「数字公民」这个身份的核心。</p>
        </div>
        <p style="font-size:17px;margin:12px 0"><strong>数字公民</strong>是指：在数字社会中生活、学习、参与的成员。这个身份的权利和责任是一起出现的——你有获取信息、表达意见、使用服务的权利，也要承担相应的责任。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>① 法律底线</strong></p>
            <p style="color:var(--muted)">不造谣不传谣，不侵犯隐私与肖像，不侵害知识产权。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 伦理规范</strong></p>
            <p style="color:var(--muted)">尊重他人，诚实表达，不利用信息不对称去欺骗。</p>
          </div>
          <div class="inner-card">
            <p><strong>③ 理性参与</strong></p>
            <p style="color:var(--muted)">核实来源，独立思考，不被情绪推着走。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="数字公民的权利与三个责任层面结构示意图">
          <figcaption>数字公民：权利与责任同时存在，责任落在法律底线、伦理规范、理性参与三个层面</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧭</span><div><strong>记忆锚点：</strong>把三个层面记成三句自问——「这么做违法吗」对法律底线，「这么做会伤害谁吗」对伦理规范，「我是不是被情绪推着走」对理性参与。一句话总结：<strong>线上做过的事，会被留下来、被检索到、被复制走</strong>，这正是责任被放大的原因。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一句话，在教室里说完就散了；发到网上会长期留存、能被检索、能被无限复制。载体变了，后果的量级也变了。"},
    {"lens": "比较它", "text": "技术防护解决「别人能不能拿到我的数据」，信息社会责任解决「我拿别人的数据去做了什么」。一个是守门，一个是自律，缺一不可。"},
    {"lens": "迁移它", "text": "现实生活里，随手转述一句没核实的传闻也会造成麻烦；数字社会只是把这件事的速度和范围放大了很多倍，判断的道理没有变。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "传播链模拟器：核实让传播变慢，却让失真停下来", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">选好转发的速度和两个开关，然后点「走一轮」逐步观察，或者「跑到底」一次看完。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-s1-fan="2" style="text-align:center">每轮每人转给 2 人</button>
            <button class="choice" data-s1-fan="3" style="text-align:center">每轮每人转给 3 人</button>
            <button class="choice" data-s1-fan="5" style="text-align:center">每轮每人转给 5 人</button>
          </div>
          <div class="sw-wrap" style="margin-top:12px">
            <div class="sw" id="s1-verify"><span class="dot"></span><span><span class="name">转发前先核实来源</span><br><span class="desc">花时间核对，信息不再走样，澄清也能沿着链条回传</span></span></div>
            <div class="sw" id="s1-old"><span class="dot"></span><span><span class="name">核对时间线，识别出这是旧消息</span><br><span class="desc">发现它三天前就出现过，并且已被澄清过</span></span></div>
          </div>
          <div id="s1-stage" style="margin-top:14px">
            <div class="msg-card">
              <div class="who">群消息 · 当前内容</div>
              <div class="body" id="s1-msg">原话：某班级群通知，下周作息时间可能有调整。</div>
              <div class="dot-row" id="s1-dots"></div>
            </div>
            <div class="lab-readout">
              <div class="readout-cell"><span class="k">已进行轮次</span><span class="v" id="s1-round">0 轮</span></div>
              <div class="readout-cell"><span class="k">累计触达</span><span class="v green" id="s1-reach">1 人</span></div>
              <div class="readout-cell"><span class="k">消息失真度</span><span class="v" id="s1-dist">0 / 100</span></div>
            </div>
            <div class="bar-row">
              <span class="lab">失真度</span>
              <span class="bar-track"><span class="bar-fill" id="s1-dbar"></span></span>
              <span class="val" id="s1-dval">低</span>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" id="s1-step" style="text-align:center">走一轮</button>
            <button class="choice" id="s1-run" style="text-align:center">跑到底</button>
            <button class="choice" id="s1-reset" style="text-align:center">重置</button>
          </div>
          <p class="result warn" id="s1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📊</span><div><strong>请做两组对照：</strong>先把两个开关都关掉跑到底，记下累计触达和失真度；再打开「转发前先核实来源」跑一次，对比这两个数字。<strong>易错点：</strong>误认为核实没有用，因为「传播变慢了」。核实的作用不是传得更快，而是让信息不走样、让澄清追得上。</div></div>
    ''', tag="传播实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "三条最容易踩的线：真实、尊重、边界", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>责任不是抽象的态度，它总能落到一个具体动作上。</strong>把动作找出来，判断才有地方可依。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>真实性线：</strong>未经核实的消息不转发。信息在每一次转述里都会走样，转发的人越多、越不核对，走样越厉害。对策：看来源、核时间线、交叉比对。</div></div>
          <div class="step"><span class="n">2</span><div><strong>尊重线：</strong>不窥探、不传播他人的隐私与肖像；引用他人的成果要注明出处，这是知识产权的基本要求。对策：涉及他人影像和信息，先取得同意。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>边界线：</strong>用人工智能生成的内容要标注清楚，不能拿它冒充真人或真实事件；推荐算法会把我们圈在同类信息里，需要有意识地拓宽信息面。对策：标注生成方式，主动换着看几类内容。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="信息传播链条上失真放大的过程与三条责任线示意图">
          <figcaption>一次不核实的转发，经过几手之后可能变成另一件事；三条线分别管住真实性、尊重与边界</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">三个高频误解：一是<strong>误认为「我只是转发，责任在原发者」</strong>——传播本身就是参与，链条上的每一手都在放大后果；二是<strong>把「我在开玩笑」当成免责理由</strong>——玩笑的判定看的是对方受到了什么影响，不是说话人的意图；三是<strong>误认为「网上公开的就能随便用」</strong>——公开可见不等于授权使用，转载要注明出处，涉及他人影像还要先取得同意。</p>
        </div>
{insight_box([
    {"lens": "解释它", "text": "为什么失真会累积？因为转述不是复制，每一次转述都是一次「理解之后再说一遍」——记不清的部分会被补上，补上的部分就成了新的「事实」。"},
    {"lens": "比较它", "text": "技术手段能帮你验证来源是否可信，但要不要点「转发」这个动作，只能由你自己决定。工具管得到链路，管不到那个按钮。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "推荐流与视野模拟器：点几次同一类，会发生什么", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">点下面的内容品类，就相当于点开了一条该类的推荐。观察四类占比和视野广度指数怎么变。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-s2-cat="sport" style="text-align:center">体育</button>
            <button class="choice" data-s2-cat="game" style="text-align:center">游戏</button>
            <button class="choice" data-s2-cat="sci" style="text-align:center">科普</button>
            <button class="choice" data-s2-cat="news" style="text-align:center">时事</button>
          </div>
          <div id="s2-stage" style="margin-top:14px">
            <p style="font-weight:700;font-size:14px;margin:0 0 8px">推荐流里的内容分布</p>
            <ul class="stream" id="s2-stream"></ul>
            <div class="lab-readout">
              <div class="readout-cell"><span class="k">点击次数</span><span class="v" id="s2-clicks">0 次</span></div>
              <div class="readout-cell"><span class="k">视野广度指数</span><span class="v green" id="s2-div">100 / 100</span></div>
            </div>
            <div class="bar-row">
              <span class="lab">视野广度</span>
              <span class="bar-track"><span class="bar-fill" id="s2-divbar"></span></span>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" id="s2-reset" style="text-align:center">重置偏好</button>
          </div>
          <p class="result warn" id="s2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔄</span><div><strong>两组对照：</strong>先连点同一个品类 8 次，记下指数；再重置，改为每轮换一个品类点 8 次，对比两次的指数。<strong>易错点：</strong>指数下降时系统不会报错、不会提示，它只是安静地把你更想看的内容排到前面——这是它最难被发现的地方。</div></div>
    ''', tag="视野实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：这条消息要不要转发？五步走一遍", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>班级群里出现一条消息，说下周作息有调整，附了一张看不清出处的截图。请你判断：转还是不转？并说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看来源：</strong>谁发的、什么时候发的、有没有署名与原始出处。「朋友的朋友」等于来源不可追溯，截图可以伪造，这两条都不能算证据。</div></div>
          <div class="step"><span class="n">2</span><div><strong>交叉核对：</strong>这件事实在权威渠道能不能找到同样的说法。如果只有同一条消息在小范围里互相转发，说明它还没有第二个独立来源。</div></div>
          <div class="step"><span class="n">3</span><div><strong>评估影响：</strong>如果它是错的，会波及哪些人？作息信息一旦传错，会让很多人白等或者白跑，这就是后果的具体样子。</div></div>
          <div class="step"><span class="n">4</span><div><strong>定位责任：</strong>我在这条链条里是第几手？我转发之后，这会成为别人眼里的「又一个来源」。很多人转发，恰恰会让假消息看起来更可信。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>处置：</strong>不转；或者转到求证渠道，让有权限核实的人去确认；如果已经核实过，转发时就把你核实到的结论一起带上。三种做法都成立，唯独「先转了再说」不成立。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少同学<strong>误认为「先转出去，反正后面会有老师澄清」</strong>。问题在于：澄清只能沿着链条回传，而链条在爆发式转发之后已经散开了，澄清追不上；这正是模拟器里失真度冲到 70 分以上之后才补救的代价。另一处容易<strong>搞混</strong>的是把「我没有恶意」当成免责条件——判断的是造成的影响，不是出发点。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("转发未核实的消息，转发的人也在参与传播，同样要承担后果", True),
                     ("只要不是自己编造的，转发就没有责任", False),
                     ("消息内容看起来合理，就可以直接转发", False)],
         "explain": "责任看的是行为本身：转发是一次传播行为，链条上每一手都在放大后果。<strong>错因提醒：</strong>最常见的就是误认为「不是我编的就没有责任」，这个想法会让你成为传谣链条里最省力的那一环。"},
        {"q": "小李把一段同学之间的聊天记录截图发到了班级群里，说「让大家看看」。主要问题在于：",
         "options": [("涉及他人隐私与肖像，公开前需要取得当事人同意", True),
                     ("截图不够清晰，看不清内容", False),
                     ("聊天记录属于平台所有，不能转发", False)],
         "explain": "聊天记录属于他人不愿公开的私人信息，公开前必须取得同意，这与截图是否清晰无关。<strong>错因提醒：</strong>容易搞混「在群里说过」和「可以被公开」——小范围的交流不等于授权对外发布。"},
        {"q": "一篇用人工智能辅助生成的文章，发布时最应当做的是：",
         "options": [("明确标注内容的生成方式，并对事实部分完成核实", True),
                     ("只要读起来通顺就可以直接发布，不必说明", False),
                     ("把文中的表述都改成更吸引人的说法，提高阅读量", False)],
         "explain": "标注生成方式，是让读者知道自己在读什么；核实事实，是对内容负责。这两件事一起做才算到位。<strong>错因提醒：</strong>把「通顺」当成「真实」是很常见的误认为——生成的内容读起来越顺，越需要你自己去核对。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次班级公众号的内容审核员", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">场景：公众号要发一篇科普文章。它由人工智能辅助生成，素材从网上转载，配图里有同学的照片，原始出处一时找不到。请决定做哪几个动作，然后点评估。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">① 这个情境里，责任落在四个维度上</p>
              <ul class="ta-log">
                <li><span class="tag">维度</span>真实性（权重 35）</li>
                <li><span class="tag">维度</span>知情同意与肖像（权重 25）</li>
                <li><span class="tag">维度</span>知识产权与出处（权重 20）</li>
                <li><span class="tag">维度</span>表述严谨（权重 20）</li>
              </ul>
            </div>
            <div>
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">② 可以做的动作</p>
              <div class="sw-wrap" id="syn-stage">
                <div class="sw" id="syn-sw-verify" data-syn-sw="verify"><span class="dot"></span><span><span class="name">追溯原始来源与发布时间</span><br><span class="desc">找到最初发布者与时间线</span></span></div>
                <div class="sw" id="syn-sw-label" data-syn-sw="label"><span class="dot"></span><span><span class="name">标注「本文由 AI 辅助生成」</span><br><span class="desc">向读者说明内容的生产方式</span></span></div>
                <div class="sw" id="syn-sw-consent" data-syn-sw="consent"><span class="dot"></span><span><span class="name">取得照片中同学的同意，或做遮挡处理</span><br><span class="desc">涉及他人影像的先取得同意</span></span></div>
                <div class="sw" id="syn-sw-credit" data-syn-sw="credit"><span class="dot"></span><span><span class="name">注明转载出处与原作者</span><br><span class="desc">按规范标注来源</span></span></div>
                <div class="sw" id="syn-sw-factcheck" data-syn-sw="factcheck"><span class="dot"></span><span><span class="name">逐句核对数据与结论，去掉没有出处的绝对化说法</span><br><span class="desc">把「一定」「必然」换回有依据的表述</span></span></div>
                <div class="sw" id="syn-sw-smooth" data-syn-sw="smooth"><span class="dot"></span><span><span class="name">把「可能」改成「一定」，标题更吸引人</span><br><span class="desc">提高点击率的常见做法</span></span></div>
                <div class="sw" id="syn-sw-quick" data-syn-sw="quick"><span class="dot"></span><span><span class="name">先发布出去，被指出问题再改</span><br><span class="desc">抢时效的常见做法</span></span></div>
              </div>
            </div>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px"></p>
          <div class="flex-row">
            <button class="choice" id="syn-run" style="text-align:center;flex:1">评估这份内容</button>
            <button class="choice" id="syn-reset" style="text-align:center;flex:1">重置</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>如果只允许保留三个动作，你会留哪三个？剩下没有覆盖到的那个维度，你打算用什么别的办法处理？</p>
          <textarea id="syn-answer" rows="3" placeholder="我会保留……因为它们守住了……这个维度；剩下的……我打算……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看判断还在不在", TTS["posttest"], [
        {"q": "群里有人发消息说「附近有同学走失，请帮转」，但没有留联系人，也没说具体地点。合适的做法是：",
         "options": [("先看是否有可核实的来源，核实不了就先转到求证渠道，不盲目扩散", True),
                     ("这种事宁可信其有，赶紧转发让更多人看到", False),
                     ("先转，如果后来发现是假的再删掉", False)],
         "explain": "真实性线同样适用于看起来「出于好意」的消息——善意不能替代核实，虚假的求助同样会造成伤害。<strong>错因提醒：</strong>常见错误是误认为「出发点是好的就不算传谣」，判断依据仍然是来源能不能核实。"},
        {"q": "一位同学发现，网上关于自己的一个说法已经被人转到很多群里，很难全部收回。这件事最值得记住的是：",
         "options": [("数字内容一旦扩散就很难收回，所以发布之前就该想清楚", True),
                     ("只要当事人不出来回应，事情就会自己过去", False),
                     ("转发的人太多，说明这个说法一定有一定道理", False)],
         "explain": "可复制、可检索、可长期留存，是数字内容的基本特点，所以责任的落点在发布之前。<strong>错因提醒：</strong>把「转发的人多」当成可信度证据，是典型的从众误认为。"},
        {"q": "某位同学长期只看同一个品类的内容，视野广度指数掉到了 30 以下。最有效的改善办法是：",
         "options": [("有意识地去看几个不同的品类，让自己的点击偏好分散开", True),
                     ("把算法关掉，以后就不看推荐了", False),
                     ("等系统自己调整，看的内容多了自然会变平衡", False)],
         "explain": "推荐分布来自你自己的点击，拓宽信息面是可以由自己完成的一步。<strong>错因提醒：</strong>容易误认为这是算法的问题、与自己无关——正好相反，每一次点击都在给它指令。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>身份</strong>：数字公民是指在数字社会中生活、学习、参与的成员，<strong>权利和责任是一起出现的</strong>。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>三个层面</strong>：法律底线（不造谣不传谣、不侵犯隐私与肖像、不侵害知识产权）、伦理规范（尊重与诚实）、理性参与（核实来源、独立思考、拓宽信息面）。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>一个可观察的证据</strong>：核实会让传播变慢，但累计触达更小、失真度不再累积、澄清追得上——负责任的做法在数据上就是这个样子。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那条消息：</strong>它的真假也许一时查不清，但「要不要转发」是当下就能决定的一件事。在模拟器里我们看到，选择核实的人少转了很多人，却让信息一直没有走样——这就是一个数字公民在链条里的作用。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「来源、失真、责任」三个词，说明为什么「先转了再说」不是一个小问题。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出数字公民的三个责任层面，每个层面各配一个具体到你自己的行为。",
            "说明「转发」为什么会让自己成为传播链条上的一环，并举一个例子。",
            "写出核实一条消息来源的三个具体动作。",
        ],
        [
            "用课堂上的传播链模拟器做两组对照：核实关闭与核实打开各跑到底，把累计触达和失真度记在表格里，写一句话说明核实换来了什么。",
            "用视野模拟器做两组对照：连点同一类 5 次，和每轮换一类点 5 次，记录两次的视野广度指数，并解释这个差别的来源。",
        ],
        [
            "找一个真实发生过的网络传言，梳理它的传播链条，标出三个可以介入的环节，并为每个环节设计一个具体做法。",
            "围绕「人工智能生成的内容怎样使用才合适」，写一份不超过三百字的班级倡议，要求每一条都指出它对应的是哪一个责任层面。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-digital-citizenship",
    "node_id": "it-m-digital-citizenship",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "信息社会责任与数字公民",
    "name_en": "Digital Citizenship and Information Responsibility",
    "grade": 9,
    "grade_cn": "九年级",
    "domain": "ai-society",
    "domain_cn": "人工智能与智慧社会",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "从一条无法追溯来源的群消息出发，理解数字公民的权利与责任是一起出现的，掌握法律底线、伦理规范、理性参与三个责任层面；用传播链模拟器观察核实对触达人数与失真度的实际影响，用推荐流模拟器观察点击偏好如何收窄视野，并能在真实情境中逐条判断处置动作守住了哪一条责任、又放大了哪一种风险。",
    "tags": ["数字公民", "信息社会责任", "信息失真", "核实来源", "知识产权", "算法推荐", "AI 生成内容标注"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「人工智能与智慧社会」——遵守法律法规与伦理规范，理性参与数字社会。",
    "hero_question": "一条看不出出处的群消息，半小时转遍几十个群——我到底该不该转出去？",
    "hero_alt": "信息社会责任知识结构图：三层责任、传播链条与处置动作三栏",
    "hero_caption": "责任三层（法律底线 · 伦理规范 · 理性参与）→ 传播链条（来源 · 转述 · 失真累积）→ 处置动作（核实 · 标注 · 取得同意 · 注明出处）",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "一条消息到底怎么判断真假？", "d": "有没有一套可以照着走的核对步骤", "v": "一条消息到底怎么判断真假"},
        {"t": "转发要不要承担责任？", "d": "只是随手一点，为什么也算参与传播", "v": "转发要不要承担责任"},
        {"t": "核实真的有用吗？", "d": "能不能看到核实前后的差别", "v": "核实真的有用吗"},
        {"t": "为什么我总是只看到同类内容？", "d": "想弄清推荐算法是怎么收窄视野的", "v": "为什么我总是只看到同类内容"},
    ],
    "objectives": [
        "能说出数字公民的含义，知道权利与责任是同时存在的",
        "能说出信息社会责任的三个层面，并各举一个具体行为",
        "能在传播链模拟器中观察核实对累计触达与失真度的影响，并解释其机制",
        "能对真实情境中的处置动作逐条判断，指出它守住了哪一条责任、又放大了哪一种风险",
    ],
    "objectives_plain": [
        "能说出数字公民的含义，知道权利与责任是同时存在的",
        "能说出信息社会责任的三个层面，并各举一个具体行为",
        "能在传播链模拟器中观察核实对累计触达与失真度的影响，并解释其机制",
        "能对真实情境中的处置动作逐条判断，指出它守住了哪一条责任、又放大了哪一种风险",
    ],
    "standards": [
        {"content": "遵守法律法规与伦理规范，理性参与数字社会。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》人工智能与智慧社会 · 初中"},
        {"content": "在数字社会中理解并遵守相关法律法规与伦理规范，保护知识产权，负责任地使用人工智能生成的内容，具备信息社会责任感。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》信息社会责任 · 初中"},
    ],
    "prereqs": ["it-m-cybersecurity"],
    "prereqs_name": "网络安全防护",
    "prereqs_meta": "it-m-cybersecurity",
    "leads_to": [],
    "next_meta": "无（初中人工智能与智慧社会收束）",
    "section_images": ["assets/it-m-digital-citizenship-fig1.webp", "assets/it-m-digital-citizenship-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一条查不到出处的消息，半小时转遍几十个群。真假一时查不清，但要不要转发是当下就能决定的。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给任何一个处置动作指出它守住了哪一条责任。",
        "objectives": "看清四件事：说出数字公民的含义、说出三个责任层面、观察核实对传播的影响、能逐条评估处置动作。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "数字公民的关键是权利和责任一起出现，责任落在法律底线、伦理规范、理性参与三个层面。",
        "lab-1": "做两组对照：开关全关跑到底，再打开核实跑一次，比一比累计触达和失真度。",
        "module-2": "真实性线管来源，尊重线管他人隐私与知识产权，边界线管 AI 生成内容与信息面。",
        "lab-2": "连点同一类 5 次，再换着点 5 次。指数下降不会有任何提示，这才是它难被发现的地方。",
        "worked-example": "五步走：看来源、交叉核对、评估影响、定位责任、处置。唯独「先转了再说」不成立。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "开动作之前先问一句：它守住的是哪一个责任维度？有些动作看起来在帮忙，其实在放大风险。",
        "posttest": "换了求助消息、删不掉的说法和收窄的视野，看看你还能不能用上三个责任层面。",
        "summary": "用「来源、失真、责任」三个词，说明为什么「先转了再说」不是小问题。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「人工智能与智慧社会」领域的一课，承接已建成的网络安全课。安全课解决的是「别人能不能拿到我的数据」，这一课解决的是「我拿别人的信息去做了什么」，两课合起来才构成完整的信息社会责任。设计上没有停在倡议层面，而是把责任做成两件可观察的事：用传播链模拟器把「核实」的代价与收益同时显示出来（触达变小、失真度不再累积、澄清追得上），让学生看到负责任的做法在数据上的样子；用推荐流与视野模拟器把「算法收窄视野」变成随点击实时变化的分布与指数，说明收窄是自己每次点击累积的结果。综合任务让学生亲手把七个处置动作对到四个责任维度上，并从中识别出「看着在帮忙、其实在放大风险」的动作。全课不出现任何真实产品与品牌，所有估算与模拟仅用于说明机制。",
    "plan_table": """| 1 | cover | 信息社会责任与数字公民 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这条消息你会怎么处理？ | 起·前测（暴露直觉） |
| 5 | concept | 数字公民：权利和责任是一起出现的 | 承·概念一（三层责任） |
| 6 | interactive | 传播链模拟器：核实让传播变慢，却让失真停下来 | 承·实验室一（触达与失真可观察） |
| 7 | concept | 三条最容易踩的线：真实、尊重、边界 | 承·概念二（含高频误解） |
| 8 | interactive | 推荐流与视野模拟器：点几次同一类，会发生什么 | 承·实验室二（分布与指数可观察） |
| 9 | concept | 例题示范：这条消息要不要转发？五步走一遍 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次班级公众号的内容审核员 | 合·迁移应用（动作对上责任维度） |
| 12 | quiz | 后测：换一个情境，看看判断还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：责任三层 / 传播链条 / 处置动作三栏标注\n- P5 权责结构图（已生成）：数字公民的权利与三个责任层面\n- P7 传播与责任线图（已生成）：转述过程中失真放大的链条与三条责任线\n- 若需补充：不含任何品牌标识的群聊界面示意图",
}
