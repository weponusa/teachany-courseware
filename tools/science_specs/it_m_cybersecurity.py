# -*- coding: utf-8 -*-
"""初中信息科技 · 网络安全防护（G8）—— 补齐课标「信息安全」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-cybersecurity-fig1.webp'
F2 = './assets/it-m-cybersecurity-fig2.webp'

TTS = {
    "hero": "先看一件真实会发生的事。一个同学的账号在深夜被登录，他自己什么都没做；等到发现时，绑定在里面的信息已经被翻过一遍。数据是怎样在无人察觉的情况下被拿走的？网络安全要回答的就是这个问题：信息在存储、传输、使用的每一个环节，都可能被人盯上。这节课我们把常见风险找出来，再用能算清楚、能验证的防护手段把它挡住。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道口令到底多长才算够，还是想知道在公共网络上提交的资料会不会被人看到，又或者你想亲手配一套防护方案，看它能不能挡住攻击。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出信息安全的三个基本目标：机密性、完整性、可用性，并各举一个例子。第二，能说出钓鱼、口令爆破、恶意代码、窃听、未修复漏洞这些常见风险各自的原理和入口。第三，能根据搜索空间和熵，判断一个口令抵抗爆破的能力，并说明为什么还需要多因素认证。第四，能针对一个真实场景配置防护措施，并判断每条攻击路径是否被阻断、还剩多少风险。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "网络安全不是一句口号，它有明确的目标。机密性，指只有该看到的人才能看到，靠加密和权限控制来实现。完整性，指数据没有被偷偷改动，靠校验摘要来发现。可用性，指需要的时候能用得上，靠备份和冗余来保障。这三条合起来，就是信息安全的基本目标。而它们都建立在一个前提上：先确认对方到底是谁，这就是身份认证。把口令、一次性验证码、设备指纹这些不同的凭据组合起来，就是多因素认证——它的意义在于，即使口令泄露，攻击者也还差一步。",
    "lab-1": "光说口令要长，说服力不够，我们来算。左边选口令用到的字符种类，右边拖长度，中间会实时算出三件事：一共有多少种可能、折算成多少位熵、以及按离线破解的速度估算，平均要试多久才能碰到。请你自己找一组数：多加一个字符，和把字符种类从一种扩到四种，哪一种提升更大？算完你会发现，长度对搜索空间的贡献是按倍数放大的。",
    "module-2": "风险通常从五个入口进来。钓鱼靠伪装成可信的来源骗取凭据，突破口是人，不是技术。口令爆破利用弱口令，或者你在别处泄露过的那一个口令。恶意代码把自己伪装成正常文件，等你亲手运行。窃听发生在传输途中，在公共网络上传输明文，等于把内容写在明信片上寄出去。未修复漏洞则是系统里已知的缺陷一直没补。对应的防护也很清楚：不从陌生链接进入、长口令加多因素认证、只从可信来源安装、使用加密连接、及时安装安全更新。要注意，没有绝对的安全，只有把风险降到可以接受的程度。",
    "lab-2": "现在你当一次中间的攻击者视角，看看同一条消息在两种传输方式下有什么不同。先选传输通道，再决定要不要加密，然后点发送。观测台上会同时列出你写进去的原文和链路上被看到的内容。加密之后，窃听者拿到的是一段看不出含义的数据；而只要完整性校验开着，任何偷偷改动都会在到达时被发现。",
    "worked-example": "我们一起分析一次账号被盗事件。第一步，界定资产和影响：可能被拿走的是登录凭据、通讯录和绑定的其他账号。第二步，找入口：登录记录显示异地、连续失败几十次之后成功，说明这不是被猜中心思，而是被反复尝试——原因通常是口令强度不够，而且没有开多因素认证。第三步，判损失范围：如果他多个平台用同一个口令，那么泄露一个就等于泄露全部，这叫撞库。第四步，处置：立刻修改口令、开启多因素认证、退出所有设备的登录、检查第三方授权、打开登录提醒。第五步，加固与复盘：改用长口令且不复用、不在未加密页面提交凭据、重要数据定期备份。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次安全加固工程师。左边是四条常见的攻击路径，右边是四项防护措施，你来决定开哪几项，然后点评估。系统会逐条判断每条路径能不能被挡住，最后给出残余风险评分。要特别留意一件事：防护措施不是越多越好，而是要和它挡住的那条路径对得上——开了一项却挡不住任何路径，等于没有作用。",
    "posttest": "最后用新情境检验一下。这次出现了公共无线网络和长期未更新的设备，看看你能不能把三要素、口令强度和防护配置用上去。",
    "summary": "这节课我们弄明白了三件事。第一，信息安全有三个基本目标：机密性、完整性、可用性，它们都建立在身份认证这个前提上。第二，风险主要从五个入口进来——钓鱼、口令爆破、恶意代码、窃听和未修复漏洞，对应五类可验证的防护措施。第三，安全不是绝对状态，而是把风险降到可接受的程度：长口令提升搜索空间，多因素认证补上最后一道闸，加密连接保护传输过程，及时更新和备份让损失可控。回到开头那个账号：只要当初开过多因素认证，就算口令被别人拿到，那次深夜登录也不会成功。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出一致性三要素各自的含义，并举出对应的防护手段。第二层能力应用，动手做：用课堂上的估算台比较三组口令的搜索空间和估算时长，写一句话说明长度与字符种类哪一个影响更大。第三层迁移挑战，选做：为家里的一台常用设备做一份加固清单，逐条说明它挡住了哪一条攻击路径，以及还剩哪些风险没能覆盖。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 三个基本目标与身份认证", "lab-1": "实验室一 口令强度估算台", "module-2": "概念二 五个入口与五类防护",
    "lab-2": "实验室二 传输链路观测台", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 防护策略配置台", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
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
.ta-mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; word-break: break-all; }
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
.bar-row .lab { flex: 0 0 96px; color: var(--muted); }
.bar-track { flex: 1; height: 12px; border-radius: 999px; background: rgb(var(--paper-rgb) / .18); overflow: hidden; }
.bar-fill { display: block; height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .3s ease; }
.bar-fill.danger { background: var(--danger); }
.bar-row .val { flex: 0 0 92px; text-align: right; font-variant-numeric: tabular-nums; font-weight: 700; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-cybersecurity 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 口令强度估算台：字符集 + 长度 → 搜索空间 / 熵 / 估算时长
   3) 传输链路观测台：通道 × 加密 × 完整性 → 窃听者所见与篡改是否暴露
   4) 防护策略配置台：4 条攻击路径 × 5 项措施 → 逐条阻断判定与残余风险
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

  /* ---------- 通用：数字与时长格式化 ---------- */
  function sci(n) {
    if (!isFinite(n)) return '无法估算';
    if (n < 1e4) return String(Math.round(n));
    if (n < 1e12) return (n / 1e4).toFixed(0) + ' 万';
    var e = Math.floor(Math.log10(n));
    return (n / Math.pow(10, e)).toFixed(2) + ' × 10<sup>' + e + '</sup>';
  }
  var SEC_YEAR = 31536000;
  function dur(s) {
    if (!isFinite(s)) return '无法估算';
    if (s <= 0.5) return '不到 1 秒';
    var units = [['秒', 1], ['分', 60], ['小时', 3600], ['天', 86400], ['年', SEC_YEAR],
                 ['万年', SEC_YEAR * 1e4], ['亿年', SEC_YEAR * 1e8]];
    var pick = units[0];
    for (var i = 0; i < units.length; i++) { if (s >= units[i][1]) pick = units[i]; }
    var v = s / pick[1];
    var txt = v >= 1000 ? String(Math.round(v)) : v.toFixed(v < 10 ? 1 : 0);
    return txt + ' ' + pick[0];
  }

  /* ---------- 2. 口令强度估算台 ---------- */
  var CHARSETS = {
    lower: { n: '小写字母', size: 26 },
    upper: { n: '大写字母', size: 26 },
    digit: { n: '数字', size: 10 },
    sym:   { n: '常用符号', size: 33 }
  };
  var GUESS_PER_SEC = 1e10;   // 估算前提：离线暴力尝试速度（专用硬件量级）
  var s1 = document.getElementById('s1-stage');
  if (s1) {
    var chosen = { lower: true, upper: false, digit: true, sym: false };
    var eLen = document.getElementById('s1-len');
    var eLenVal = document.getElementById('s1-len-val');
    var ePool = document.getElementById('s1-pool');
    var eSpace = document.getElementById('s1-space');
    var eEnt = document.getElementById('s1-ent');
    var eTime = document.getElementById('s1-time');
    var eBar = document.getElementById('s1-bar');
    var eBarVal = document.getElementById('s1-bar-val');
    var eOut = document.getElementById('s1-out');

    function render1() {
      var size = 0, names = [];
      Object.keys(chosen).forEach(function (k) {
        if (chosen[k]) { size += CHARSETS[k].size; names.push(CHARSETS[k].n); }
      });
      var L = Number(eLen.value);
      eLenVal.textContent = L + ' 位';
      document.querySelectorAll('[data-s1-set]').forEach(function (b) {
        b.classList.toggle('selected', !!chosen[b.dataset.s1Set]);
      });

      if (size === 0) {
        ePool.textContent = '—'; eSpace.textContent = '—'; eEnt.textContent = '—'; eTime.textContent = '—';
        eBar.style.width = '0%'; eBarVal.textContent = '—';
        eOut.className = 'result error';
        eOut.innerHTML = '<strong>至少选一种字符。</strong>没有候选字符，就没有可估算的搜索空间。';
        return;
      }
      var pool = names.join(' + ') + ' 共 ' + size + ' 种字符';
      var space = Math.pow(size, L);
      var ent = L * Math.log2(size);
      var avg = space / 2 / GUESS_PER_SEC;      // 平均尝试次数约为搜索空间的一半

      ePool.textContent = pool;
      eSpace.innerHTML = sci(space) + ' 种';
      eEnt.textContent = ent.toFixed(1) + ' 位';
      eTime.textContent = dur(avg);

      var score = Math.max(0, Math.min(100, ent / 90 * 100));
      eBar.style.width = score.toFixed(1) + '%';
      eBar.className = 'bar-fill' + (score < 45 ? ' danger' : '');
      eBarVal.textContent = score.toFixed(0) + ' / 100';

      // 找一个还没被选中的字符集，用来说明「补一种字符」到底把底数抬到多少
      var spare = 0;
      Object.keys(chosen).forEach(function (k) { if (!chosen[k] && CHARSETS[k].size > spare) spare = CHARSETS[k].size; });
      var cmpTip = spare > 0
        ? '从公式看，多一位是把搜索空间乘上 ' + size + ' 倍；而补一种字符只是把底数从 ' + size + ' 抬到 ' + (size + spare) + '，' +
          '大约只乘 ' + ((size + spare) / size).toFixed(2) + ' 倍。'
        : '从公式看，多一位是把搜索空间乘上 ' + size + ' 倍；而字符种类已经全选上了，再想变强就只能继续加长。';

      var grade, advice;
      if (ent < 40) { grade = '很弱'; advice = '这样的搜索空间用普通设备就能在很短时间内试完，必须加长，并且一定要开多因素认证。'; }
      else if (ent < 60) { grade = '偏弱'; advice = '已经能挡住随手一猜，但挡不住有备而来的离线破解。再长几位，或补上一种字符。'; }
      else if (ent < 80) { grade = '够用'; advice = '搜索空间足够大，离线破解的代价已经很高。仍然建议开多因素认证，因为泄露未必来自破解。'; }
      else { grade = '强'; advice = '搜索空间非常大，估算时长已经远远超出攻击者愿意付出的成本。别忘了口令再强也挡不住钓鱼。'; }

      eOut.className = 'result ' + (ent < 40 ? 'error' : (ent < 60 ? 'warn' : ''));
      eOut.innerHTML = '<strong>当前口令：' + L + ' 位，字符集 ' + size + ' 种，强度评估为「' + grade + '」。</strong><br>' +
        '搜索空间 = ' + size + '<sup>' + L + '</sup>，约等于 ' + sci(space) + ' 种组合；' +
        '熵约 ' + ent.toFixed(1) + ' 位。<br>' +
        '按每秒尝试 ' + GUESS_PER_SEC.toExponential(0) + ' 次的估算前提，平均要试 ' +
        dur(avg) + ' 才可能碰到一次（平均尝试次数约为搜索空间的一半）。<br>' +
        '<strong>易错点：</strong>很多同学误认为「加一个符号」比「多一位」更管用。' +
        cmpTip + '长度对搜索空间的贡献在指数位置上，这也是安全规范都强调「口令要够长」的原因。<br>' + advice;
    }

    document.querySelectorAll('[data-s1-set]').forEach(function (b) {
      b.addEventListener('click', function () {
        chosen[b.dataset.s1Set] = !chosen[b.dataset.s1Set];
        render1();
      });
    });
    eLen.addEventListener('input', render1);
    render1();
  }

  /* ---------- 3. 传输链路观测台 ---------- */
  var CHANNELS = {
    home: { n: '可信的校园网（有人维护）', risk: 0.15, note: '接入点由学校统一管理，被旁路窃听的难度较高。' },
    public: { n: '公共场所的开放无线网络', risk: 0.85, note: '任何人都在同一个广播域里，旁路窃听的可行性很高。' }
  };
  var s2 = document.getElementById('s2-stage');
  if (s2) {
    var ch = 'public', enc = false, integ = false, sent = false;

    function mask(t) {
      var out = '';
      for (var i = 0; i < t.length; i++) { out += (((i * 7 + 3) % 10 < 6) ? String.fromCharCode(0x4E00 + ((i * 137 + t.charCodeAt(i)) % 900)) : '#'); }
      return out;
    }

    function render2() {
      document.querySelectorAll('[data-s2-ch]').forEach(function (b) { b.classList.toggle('selected', b.dataset.s2Ch === ch); });
      document.getElementById('s2-enc').classList.toggle('on', enc);
      document.getElementById('s2-integ').classList.toggle('on', integ);
      var ePlain = document.getElementById('s2-plain');
      var eSeen = document.getElementById('s2-seen');
      var eOut = document.getElementById('s2-out');
      var text = document.getElementById('s2-text').value || '（请在下面写一条要发送的内容）';
      if (!sent) {
        ePlain.textContent = text;
        eSeen.textContent = '—';
        eOut.className = 'result warn';
        eOut.innerHTML = '选好通道、设置好两个开关之后，点「发送并观测」。';
        return;
      }
      ePlain.textContent = text;
      var seen = enc ? mask(text) : text;
      eSeen.textContent = seen;

      var snoop = CHANNELS[ch].risk >= 0.5;
      var rows = [];
      rows.push('<li><span class="tag">发送方</span>把内容「' + text + '」交给传输通道。</li>');
      rows.push('<li><span class="tag">通道</span>' + CHANNELS[ch].n + '：' + CHANNELS[ch].note + '</li>');
      if (snoop) {
        rows.push('<li' + (enc ? '' : ' class="bad"') + '><span class="tag">窃听者</span>截获到：<span class="ta-mono">' +
          (enc ? seen : text) + '</span> —— ' +
          (enc ? '这是一段加密后的数据，没有密钥就无法还原出原文。' : '<strong>原文完整可读</strong>，凭据等于直接交了出去。') + '</li>');
      } else {
        rows.push('<li><span class="tag">窃听者</span>在这个通道上很难旁路截获数据。注意：这只是难度更高，不等于不可能。</li>');
      }
      rows.push('<li' + (integ ? ' class="ok"' : ' class="bad"') + '><span class="tag">完整性</span>' +
        (integ ? '接收方校验摘要一致，内容在途中没有被改动过。' : '没有任何校验手段，途中被改动过也发现不了——收到的内容不可信。') + '</li>');
      rows.push('<li' + ((!snoop || enc) && integ ? ' class="ok"' : ' class="bad"') +
        '><span class="tag">结论</span>' +
        ((!snoop || enc) && integ
          ? '这条链路同时守住了机密性和完整性：内容看不到，改动瞒不了。'
          : (!enc && snoop
              ? '<strong>机密性失守。</strong>在开放网络上传输不加密的内容，只要被旁路截获，原文就直接暴露。'
              : '<strong>完整性没有保障。</strong>内容改过也看不出来，接收方无法判断数据是否可信。')) + '</li>');
      eOut.className = 'result ' + ((!snoop || enc) && integ ? '' : 'error');
      eOut.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
    }

    document.querySelectorAll('[data-s2-ch]').forEach(function (b) {
      b.addEventListener('click', function () { ch = b.dataset.s2Ch; sent = false; render2(); });
    });
    document.getElementById('s2-enc').addEventListener('click', function () { enc = !enc; sent = false; render2(); });
    document.getElementById('s2-integ').addEventListener('click', function () { integ = !integ; sent = false; render2(); });
    document.getElementById('s2-text').addEventListener('input', function () { render2(); });
    document.getElementById('s2-send').addEventListener('click', function () { sent = true; render2(); });
    document.getElementById('s2-reset').addEventListener('click', function () { ch = 'public'; enc = false; integ = false; sent = false; render2(); });
    render2();
  }

  /* ---------- 4. 防护策略配置台 ---------- */
  var PATHS = {
    brute: { n: '口令爆破 / 撞库', weight: 30, by: 'mfa',
             why: '多因素认证要求「口令之外再加一个因素」，口令即使泄露也不够用。' },
    phish: { n: '钓鱼骗取凭据', weight: 30, by: 'entry',
             why: '固定从官方入口进入、不打开陌生链接，能阻断大多数伪装页面。' },
    vuln:  { n: '利用未修复漏洞', weight: 25, by: 'patch',
             why: '及时安装安全更新，把已知缺陷这个入口关掉。' },
    sniff: { n: '开放网络窃听', weight: 25, by: 'tls',
             why: '使用加密连接，让链路上的内容无法被直接读懂。' }
  };
  var MEASURES = {
    mfa:   { n: '多因素认证', desc: '口令之外再加一道验证' },
    entry: { n: '只走官方入口', desc: '不点陌生链接，从书签或官方入口进入' },
    patch: { n: '及时安装安全更新', desc: '把已公开的缺陷尽快补上' },
    tls:   { n: '使用加密连接', desc: '在加密通道里提交凭据' },
    backup:{ n: '定期备份重要数据', desc: '不阻断攻击，但把损失压到可恢复' }
  };
  var syn = document.getElementById('syn-stage');
  if (syn) {
    var on = { mfa: false, entry: false, patch: false, tls: false, backup: false };
    var ran = false;

    function renderSyn() {
      Object.keys(MEASURES).forEach(function (k) {
        var el = document.getElementById('syn-sw-' + k);
        if (el) el.classList.toggle('on', on[k]);
      });
      var out = document.getElementById('syn-out');
      if (!ran) {
        out.className = 'result warn';
        out.textContent = '选好要开启的措施，然后点「评估这份方案」。';
      }
    }

    document.querySelectorAll('[data-syn-sw]').forEach(function (el) {
      el.addEventListener('click', function () {
        on[el.dataset.synSw] = !on[el.dataset.synSw];
        ran = false;
        renderSyn();
      });
    });

    document.getElementById('syn-run').addEventListener('click', function () {
      var rows = [], left = 0, blocked = 0;
      Object.keys(PATHS).forEach(function (k) {
        var P = PATHS[k];
        var stop = !!on[P.by];
        if (stop) blocked++; else left += P.weight;
        rows.push('<li' + (stop ? ' class="ok"' : ' class="bad"') + '><span class="tag">' + P.n + '</span>' +
          (stop ? '已阻断。' + P.why : '未被阻断，权重 ' + P.weight + ' 分。目前没有任何一项措施对上这条路径。') + '</li>');
      });
      var score = Math.max(0, left - (on.backup ? 10 : 0));
      var level = score <= 15 ? '低' : (score <= 45 ? '中' : '高');
      rows.push('<li class="' + (score <= 45 ? 'ok' : 'bad') + '"><span class="tag">评估</span>' +
        '共 ' + Object.keys(PATHS).length + ' 条攻击路径，已阻断 ' + blocked + ' 条；' +
        '残余风险 ' + left + ' 分' + (on.backup ? '，定期备份再减轻 10 分（它不阻断攻击，但把损失变成可恢复）' : '') +
        '，最终评分 ' + score + ' 分，风险等级：<strong>' + level + '</strong>。</li>');
      var idle = Object.keys(MEASURES).filter(function (k) { return on[k] && !Object.keys(PATHS).some(function (p) { return PATHS[p].by === k; }); });
      if (idle.length) {
        rows.push('<li class="bad"><span class="tag">提示</span>「' + idle.map(function (k) { return MEASURES[k].n; }).join('」和「') +
          '」没有对上任何一条路径。防护措施要看它挡的是谁，开一项挡不住任何东西的措施，只是增加了操作负担。</li>');
      }
      if (score === 0) rows.push('<li class="ok"><span class="tag">完成</span>四条已识别的路径都被覆盖。请记住：这只是把已知风险降到可接受，新的路径会不断出现，安全是一项持续的工作。</li>');
      var out = document.getElementById('syn-out');
      out.className = 'result ' + (score <= 30 ? '' : (score <= 45 ? 'warn' : 'error'));
      out.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
      ran = true;
    });

    document.getElementById('syn-reset').addEventListener('click', function () {
      on = { mfa: false, entry: false, patch: false, tls: false, backup: false };
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：数据是在哪一步丢掉的？", TTS["pretest"], [
        {"q": "下面哪一件事属于「保护数据的完整性」？",
         "options": [("让接收方能够发现内容在传输途中被人改过", True),
                     ("让无关的人看不到内容", False),
                     ("保证系统随时都能打开、不会中断", False)],
         "explain": "完整性针对的是「有没有被改动」，机密性针对「谁能看」，可用性针对「能不能用上」。<strong>错因提醒：</strong>这三个目标最容易搞混，判断的关键是问一句：这条措施防的到底是「被别人看到」、「被别人改」还是「用不上」。"},
        {"q": "一个口令由 8 位小写字母组成，另一个由 12 位小写字母组成。关于它们的搜索空间，正确的说法是：",
         "options": [("12 位那个的搜索空间是 8 位那个的 26⁴ 倍，差距被指数放大", True),
                     ("只多了 4 位，搜索空间大约只差一倍", False),
                     ("两者差不多，因为用的字符种类完全一样", False)],
         "explain": "搜索空间是「字符种类数的位数次方」，多一位就乘以一次底数。<strong>错因提醒：</strong>同学常误认为「多几位只是多一点点」，把加法直觉套到指数上——这里差的不是 4，而是 26 的四次方。"},
        {"q": "在公共场所的开放无线网络上登录账号，最需要警惕的是：",
         "options": [("同一网络里的人可能旁路截获你发送的内容", True),
                     ("网速会比家里慢一些", False),
                     ("路由器的外观可能会被别人看到", False)],
         "explain": "开放网络里，旁路截获的可行性明显更高——所以要用加密连接。<strong>错因提醒：</strong>常见错误是只盯着「快不快」，把传输安全当成性能问题。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "机密性、完整性、可用性，安全有三个明确目标", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道数据可以采集、传输、存储，也用过各种在线服务。但你有没有想过：数据在存储、传输、使用的每一个环节，都可能被人盯上。<strong>所以</strong>我们需要先给「安全」下可检验的定义——否则就只能靠感觉说「我觉得这样比较安全」，而感觉是没办法验证的。</p>
        </div>
        <p style="font-size:17px;margin:12px 0">信息安全有三个基本目标：<strong>机密性</strong>（只有该看到的人才能看到，靠加密与权限控制实现）、<strong>完整性</strong>（数据没有被偷偷改动，靠校验摘要来发现）、<strong>可用性</strong>（需要的时候能用得上，靠备份与冗余来保障）。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>① 机密性</strong></p>
            <p style="color:var(--muted)">防「被看到」。靠加密和权限控制实现。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 完整性</strong></p>
            <p style="color:var(--muted)">防「被改」。靠校验摘要及时发现改动。</p>
          </div>
          <div class="inner-card">
            <p><strong>③ 可用性</strong></p>
            <p style="color:var(--muted)">防「用不上」。靠备份和冗余撑住。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="信息安全三要素示意图，机密性、完整性与可用性三者关系及对应手段">
          <figcaption>机密性、完整性、可用性——三个目标各有各的对手，也各有各的技术手段</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔑</span><div><strong>记忆锚点：</strong>把三个目标记成三句反问——「这个别人能看到吗」对应机密性，「这个被人改过吗」对应完整性，「这个现在还打得开吗」对应可用性。再加一个前提：<strong>先确认对方是谁</strong>，这就是身份认证；把口令之外的第二种凭据也加上，就是多因素认证。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一份数据，在一台没人管的终端上和在加密、有权限、有备份的环境里，面对的风险完全不同——安全是环境的属性，不只是数据自己的属性。"},
    {"lens": "比较它", "text": "加密是为了防止别人看懂，摘要校验是为了防止别人改完不认账。一个管「看不懂」，一个管「改不了瞒得住」，不能互相替代。"},
    {"lens": "迁移它", "text": "快递要密封（机密性）、要有封条和重量校验（完整性）、还要保证按时送达（可用性）——思路完全一样。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "口令强度估算台：多长才够，多一种字符能顶几位？", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">先选口令用到的字符种类，再拖长度，观察搜索空间、熵和估算时长怎么变。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-s1-set="lower" style="text-align:center">小写字母 26</button>
            <button class="choice" data-s1-set="upper" style="text-align:center">大写字母 26</button>
            <button class="choice" data-s1-set="digit" style="text-align:center">数字 10</button>
            <button class="choice" data-s1-set="sym" style="text-align:center">常用符号 33</button>
          </div>
          <div id="s1-stage" style="margin-top:14px">
            <div class="slider-row">
              <label for="s1-len">口令长度</label>
              <input type="range" id="s1-len" min="4" max="20" step="1" value="8">
              <span class="readout-cell" style="flex:0 0 96px"><span class="k">长度</span><span class="v" id="s1-len-val">8 位</span></span>
            </div>
            <div class="lab-readout">
              <div class="readout-cell" style="min-width:200px"><span class="k">候选字符集</span><span class="v" id="s1-pool" style="font-size:15px">—</span></div>
              <div class="readout-cell"><span class="k">搜索空间</span><span class="v" id="s1-space">—</span></div>
              <div class="readout-cell"><span class="k">熵（bit）</span><span class="v green" id="s1-ent">—</span></div>
              <div class="readout-cell"><span class="k">平均估算时长</span><span class="v" id="s1-time">—</span></div>
            </div>
            <div class="bar-row">
              <span class="lab">强度评分</span>
              <span class="bar-track"><span class="bar-fill" id="s1-bar"></span></span>
              <span class="val" id="s1-bar-val">—</span>
            </div>
          </div>
          <p class="result warn" id="s1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">📐</span><div><strong>估算前提说清楚：</strong>「每秒尝试 10 的 10 次方次」指的是离线暴力尝试在专用硬件上的量级，用来说明不同口令的相对强弱，不代表我们在尝试攻破任何系统。真正要记住的是：<strong>长度对搜索空间的贡献是指数级的</strong>。</div></div>
    ''', tag="口令实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "五个入口，五类防护，一条一条对上", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>风险不是抽象的，它总是从某个具体的入口进来。</strong>把入口找出来，防护措施才有地方可放；找不到入口的防护，多半只是心理安慰。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>钓鱼（社会工程）</strong>：伪装成可信来源骗取凭据，突破口是人不是技术。对策：不点陌生链接，固定从官方入口进入，可疑请求要二次确认。</div></div>
          <div class="step"><span class="n">2</span><div><strong>口令爆破与撞库</strong>：利用弱口令，或你在别处泄露过的那一个口令。对策：够长的口令 + 多因素认证。</div></div>
          <div class="step"><span class="n">3</span><div><strong>恶意代码</strong>：把自己伪装成正常文件，等你亲手运行。对策：只从可信来源获取，及时更新系统。</div></div>
          <div class="step"><span class="n">4</span><div><strong>窃听与中间人</strong>：在传输途中读取或篡改内容。对策：全程使用加密连接，并对内容做完整性校验。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>未修复漏洞</strong>：系统里已经公开的缺陷一直没补。对策：及时安装安全更新，关闭用不到的服务与端口。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="常见网络风险入口与对应防护策略对照示意图">
          <figcaption>五条常见入口，对上五类可验证的防护措施——措施必须打在入口上</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最容易犯的两个错：一是<strong>误认为口令足够复杂就万事大吉</strong>——钓鱼和撞库根本不靠猜，所以多因素认证不是可选项；二是<strong>搞混「加密」与「完整」</strong>——加密只让内容看不懂，挡不住别人把内容改掉，要发现改动还得靠完整性校验。另外要接受一件事：<strong>没有绝对的安全</strong>，只有把风险降到可以接受的程度。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "传输链路观测台：同一条消息，被看到的内容一样吗？", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">选一条传输通道，再决定要不要加密、要不要做完整性校验，然后发送并观测。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-s2-ch="home" style="text-align:center">可信的校园网</button>
            <button class="choice" data-s2-ch="public" style="text-align:center">公共场所的开放无线网络</button>
          </div>
          <div id="s2-stage" style="margin-top:14px">
            <div class="sw-wrap">
              <div class="sw" id="s2-enc"><span class="dot"></span><span><span class="name">对传输内容加密</span><br><span class="desc">在加密通道里发送，链路上只能看到密文</span></span></div>
              <div class="sw" id="s2-integ"><span class="dot"></span><span><span class="name">校验内容完整性</span><br><span class="desc">接收方核对摘要，发现途中被改动过</span></span></div>
            </div>
            <label style="display:block;margin-top:12px;font-weight:700;font-size:14px">要发送的内容
              <input id="s2-text" value="登录凭据：账号与口令" style="margin-top:6px">
            </label>
            <div class="lab-readout">
              <div class="readout-cell" style="min-width:220px"><span class="k">你写下的原文</span><span class="v ta-mono" id="s2-plain" style="font-size:14px;font-weight:600">—</span></div>
              <div class="readout-cell" style="min-width:220px"><span class="k">链路上被看到的内容</span><span class="v ta-mono" id="s2-seen" style="font-size:14px;font-weight:600">—</span></div>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" id="s2-send" style="text-align:center;flex:1">发送并观测</button>
            <button class="choice" id="s2-reset" style="text-align:center;flex:1">重置</button>
          </div>
          <p class="result warn" id="s2-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛡️</span><div><strong>动手比一比：</strong>先在开放网络上不加密发一次，看看链路上显示什么；再打开加密发一次。同一个通道，两种结果。<strong>易错点：</strong>加密之后内容看不懂了，但如果没开完整性校验，内容被改掉仍然发现不了——这两件事必须一起做。</div></div>
    ''', tag="传输实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一次账号被盗，怎么一步步查清楚", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>某同学的账号在深夜被异地登录。请分析可能的入口，给出处置步骤和加固方案。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>界定资产与影响：</strong>可能被拿走的不只是登录凭据，还有通讯录、聊天记录，以及绑定的其他平台账号。先算清楚「丢了什么」，才知道要处置到什么程度。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找入口：</strong>登录记录显示异地、连续失败几十次之后成功。连续失败说明是被反复尝试，而不是被猜中心思——入口很可能是口令强度不足，并且没有开启多因素认证。</div></div>
          <div class="step"><span class="n">3</span><div><strong>判断扩散范围：</strong>如果他在多个平台用了同一个口令，泄露一个就等于泄露全部，这就是撞库。要逐个平台检查。</div></div>
          <div class="step"><span class="n">4</span><div><strong>处置：</strong>立刻修改为互不复用的长口令、开启多因素认证、退出所有设备的登录、检查第三方授权应用并撤销可疑授权、打开异地登录提醒。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>加固与复盘：</strong>不在未加密页面提交凭据、只从官方入口进入、及时安装安全更新、重要数据定期备份。写下来的是清单，做出来的才叫防护。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少同学误认为「账号被盗一定是被破解了密码」，于是只想着换一个更复杂的口令。但钓鱼和撞库根本不靠猜——如果入口是钓鱼页面，再长的口令也是自己交出去的，这时候唯一能救场的是多因素认证。另一处容易搞混的是把「改口令」当成处置的全部：<strong>没有退出其他设备的登录、没有检查第三方授权</strong>，攻击者手里的凭据可能依然有效。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("加密让内容看不懂，完整性校验让改动瞒不住，两者不能相互替代", True),
                     ("只要加密了，内容就一定不会被改动", False),
                     ("设置了复杂口令，就不需要再开多因素认证", False)],
         "explain": "机密性与完整性防的是两件事：一个防「被看到」，一个防「被改」。<strong>错因提醒：</strong>最常见的是误认为加密顺带把完整性也解决了；实际上加密之后内容依然可能被替换成另一段合法密文。"},
        {"q": "一个口令由 10 位构成，只用数字；另一个由 8 位构成，使用小写字母加数字。关于它们的搜索空间，正确的是：",
         "options": [("数字 10 位是 10 的 10 次方，约 1 亿的 100 倍；字母数字 8 位是 36 的 8 次方，量级相当甚至更大", True),
                     ("字符种类多的那个一定更强，与长度无关", False),
                     ("数字 10 位明显更弱，因为数字只有 10 种", False)],
         "explain": "要分别算底数的位数次方，再比较量级：10¹⁰ ≈ 1×10¹⁰，36⁸ ≈ 2.8×10¹²。<strong>错因提醒：</strong>容易只盯着字符种类下结论，忘记长度在指数位置上——这正是这一课要纠正的加法直觉。"},
        {"q": "关于「防护措施」，下面哪种判断最站得住脚？",
         "options": [("一项措施要靠得上某条攻击路径，否则开了也没用", True),
                     ("防护措施开得越多越安全，不必考虑它挡的是谁", False),
                     ("只要把系统更新到最新，就不需要其他措施了", False)],
         "explain": "防护要有针对性：措施与路径一一对应，才是有效配置。<strong>错因提醒：</strong>常见错误是把安全当成「堆措施」——开了一堆按钮却挡不住任何一条实际路径，只是增加了操作负担。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给一位同学配一份防护方案", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">场景：同学甲的日常设备要长期使用，目前四项防护都没有开。请决定开启哪几项，然后点评估。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">① 已识别的攻击路径</p>
              <ul class="ta-log">
                <li><span class="tag">路径</span>口令爆破 / 撞库（权重 30）</li>
                <li><span class="tag">路径</span>钓鱼骗取凭据（权重 30）</li>
                <li><span class="tag">路径</span>利用未修复漏洞（权重 25）</li>
                <li><span class="tag">路径</span>开放网络窃听（权重 25）</li>
              </ul>
            </div>
            <div>
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">② 可开启的措施</p>
              <div class="sw-wrap" id="syn-stage">
                <div class="sw" id="syn-sw-mfa" data-syn-sw="mfa"><span class="dot"></span><span><span class="name">多因素认证</span><br><span class="desc">口令之外再加一道验证</span></span></div>
                <div class="sw" id="syn-sw-entry" data-syn-sw="entry"><span class="dot"></span><span><span class="name">只走官方入口</span><br><span class="desc">不点陌生链接，从官方入口进入</span></span></div>
                <div class="sw" id="syn-sw-patch" data-syn-sw="patch"><span class="dot"></span><span><span class="name">及时安装安全更新</span><br><span class="desc">把已公开的缺陷补上</span></span></div>
                <div class="sw" id="syn-sw-tls" data-syn-sw="tls"><span class="dot"></span><span><span class="name">使用加密连接</span><br><span class="desc">在加密通道里提交凭据</span></span></div>
                <div class="sw" id="syn-sw-backup" data-syn-sw="backup"><span class="dot"></span><span><span class="name">定期备份重要数据</span><br><span class="desc">不阻断攻击，把损失压到可恢复</span></span></div>
              </div>
            </div>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px"></p>
          <div class="flex-row">
            <button class="choice" id="syn-run" style="text-align:center;flex:1">评估这份方案</button>
            <button class="choice" id="syn-reset" style="text-align:center;flex:1">重置</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>如果只允许开一项措施，你会开哪一项？请说明理由，以及它没能覆盖的那几条路径你打算怎么处理。</p>
          <textarea id="syn-answer" rows="3" placeholder="我会先开……因为它挡住了……这条路径；剩下没覆盖的是……我打算……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "一位同学在图书馆的开放无线网络上要提交一份资料。下面哪种做法最合理？",
         "options": [("确认地址栏是加密连接后再提交，并尽量避免在开放网络上处理敏感内容", True),
                     ("开放网络速度快，直接提交就好", False),
                     ("先把资料存到本地，等下次用自己的网络再提交——但不必关心是否加密", False)],
         "explain": "开放网络旁路截获的可行性更高，所以传输过程必须加密。<strong>错因提醒：</strong>常见错误是误认为「换个时间提交」就等于安全了；只要在未加密的页面上提交，风险始终存在。"},
        {"q": "一台设备长期提示有安全更新但没有安装。主要风险是：",
         "options": [("已公开的缺陷一直没补，等于给攻击者留了一个已知入口", True),
                     ("设备会变慢，其余没有影响", False),
                     ("更新会占用空间，所以不更新反而更安全", False)],
         "explain": "未修复漏洞是五条常见入口之一，而且它的特点是被公开过、利用方式明确。<strong>错因提醒：</strong>很多同学把安全更新当成「性能优化」，误认为它只影响速度，其实它补的是可被利用的缺陷。"},
        {"q": "小李说：「我的口令有 16 位，非常强，所以不需要开多因素认证。」这个说法的问题在于：",
         "options": [("长口令提升的是抵抗爆破的能力，而钓鱼、撞库根本不靠猜，仍需要第二道凭据", True),
                     ("16 位其实不够长，加固到 24 位就可以了", False),
                     ("多因素认证只是为了方便找回账号，和安全没关系", False)],
         "explain": "口令强度和身份认证是两个层面：前者让「猜」变难，后者让「拿到口令也不够用」。<strong>错因提醒：</strong>把强度当成万能，是这一课最需要纠正的想法。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>三个目标</strong>：机密性防「被看到」，完整性防「被改」，可用性防「用不上」；它们都建立在身份认证这个前提上。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>五个入口</strong>：钓鱼、口令爆破、恶意代码、窃听、未修复漏洞——防护措施必须对得上具体的入口，否则只是操作负担。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>两个可算的量</strong>：口令的搜索空间是「字符种类数的位数次方」，长度贡献在指数位置上；加密与完整性校验解决的是两件不同的事。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那个深夜被登录的账号：</strong>如果当初开了多因素认证，即使口令已经泄露，攻击者也还差一步，那次登录就不会成功。整个防护过程里没有一步是神秘的——每一项措施都对应着一条明确的攻击路径。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「机密性、完整性、可用性」三个词，再挑两条攻击路径，说清楚这个场景里应该配哪些措施、为什么配它们。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出一致性三要素（机密性、完整性、可用性）各自的含义，并为每一项举出一个对应的技术手段。",
            "列举四条常见的安全风险入口，并各写一句它的突破口在哪里（人、口令、文件、链路还是系统缺陷）。",
            "说明身份认证与多因素认证的区别：多因素认证多出来的那「一个因素」解决了什么问题？",
        ],
        [
            "用课堂上的估算台比较三组口令，记录各自的搜索空间和估算时长，写一句话说明长度与字符种类哪一个影响更大。",
            "画一条「你 → 网络 → 服务器」的传输链路，在图上标出窃听点与篡改点，并标出加密和完整性校验分别在哪一步起作用。",
        ],
        [
            "为家里的一台常用设备做一份加固清单，逐条说明它挡住了哪一条攻击路径，并指出还剩哪些风险没有被覆盖。",
            "在上述清单基础上评估：如果只允许保留三项措施，你会留下哪三项？请用「残余风险」的说法说明取舍理由。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-cybersecurity",
    "node_id": "it-m-cybersecurity",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "网络安全防护",
    "name_en": "Cybersecurity: Risks and Protection",
    "grade": 8,
    "grade_cn": "八年级",
    "domain": "security",
    "domain_cn": "信息安全",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "从一次账号被异地登录的真实事件出发，理解信息安全机密性、完整性、可用性三个基本目标，识别钓鱼、口令爆破、恶意代码、窃听与未修复漏洞等常见风险入口，会用搜索空间与熵估算口令抵抗爆破的能力，并能为真实场景配置与攻击路径对应的防护措施、评估残余风险。",
    "tags": ["网络安全", "机密性", "完整性", "可用性", "多因素认证", "搜索空间", "防护策略"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「信息安全」——识别常见网络攻击方式，掌握基本防护策略。",
    "hero_question": "一个账号在深夜被人登录，本人却什么都没做——数据是在哪一步丢掉的？",
    "hero_alt": "网络安全防护知识结构图：风险入口、安全目标与防护措施三栏",
    "hero_caption": "风险入口（钓鱼·爆破·恶意代码·窃听·漏洞）→ 安全目标（机密性·完整性·可用性）→ 防护措施（认证·更新·加密·校验·备份）",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "口令到底要多长才算够？", "d": "长度和字符种类哪个更管用", "v": "口令到底要多长才算够"},
        {"t": "在公共网络上提交资料，别人能看到吗？", "d": "传输过程中数据是怎么被读走的", "v": "在公共网络上提交资料，别人能看到吗"},
        {"t": "常见的攻击方式有哪些，各从哪里进来？", "d": "为什么说突破口常常是人", "v": "常见的攻击方式有哪些，各从哪里进来"},
        {"t": "怎样配一套真正挡得住的防护方案？", "d": "措施要不要一条条对上攻击路径", "v": "怎样配一套真正挡得住的防护方案"},
    ],
    "objectives": [
        "能说出机密性、完整性、可用性的含义，并各举一个对应的技术手段",
        "能说明钓鱼、口令爆破、恶意代码、窃听、未修复漏洞各自的风险入口与基本原理",
        "能根据搜索空间与熵估算口令抵抗爆破的能力，并解释为什么还需要多因素认证",
        "能针对真实场景配置与攻击路径对应的防护措施，并评估残余风险等级",
    ],
    "objectives_plain": [
        "能说出机密性、完整性、可用性的含义，并各举一个对应的技术手段",
        "能说明钓鱼、口令爆破、恶意代码、窃听、未修复漏洞各自的风险入口与基本原理",
        "能根据搜索空间与熵估算口令抵抗爆破的能力，并解释为什么还需要多因素认证",
        "能针对真实场景配置与攻击路径对应的防护措施，并评估残余风险等级",
    ],
    "standards": [
        {"content": "识别常见网络攻击方式，掌握基本防护策略。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》信息安全 · 初中"},
        {"content": "在真实情境中理解数据安全与个人信息保护要求，具备一定的安全防护能力，承担信息社会责任。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》信息社会责任 · 初中"},
    ],
    "prereqs": [],
    "prereqs_name": "无（初中信息安全起点）",
    "prereqs_meta": "无",
    "leads_to": ["it-m-privacy-protection"],
    "next_meta": "it-m-privacy-protection",
    "section_images": ["assets/it-m-cybersecurity-fig1.webp", "assets/it-m-cybersecurity-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "账号在深夜被登录，本人什么都没做——数据是在哪一步丢掉的？带着这个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能为任何一个场景指出风险入口并配上对应的防护。",
        "objectives": "看清四件事：说清三个安全目标、认出五个风险入口、会估算口令强度、能配出并评估一份防护方案。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "机密性防被看到、完整性防被改、可用性防用不上，三者的共同前提是身份认证。",
        "lab-1": "分别动一动长度和字符种类，比较搜索空间的变化量级。长度在指数位置上，影响大得多。",
        "module-2": "五个入口各有一个突破口：人、口令、文件、链路、系统缺陷。防护措施要对得上入口。",
        "lab-2": "同一个通道，先不加密发一次，再打开加密发一次；最后补上完整性校验，看结论怎么变。",
        "worked-example": "五步走：界定资产、找入口、判扩散范围、处置、加固复盘。别把「改口令」当成处置的全部。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "开措施之前先问一句：它挡的是哪一条路径？挡不住任何路径的措施只是负担。",
        "posttest": "换了开放网络和未更新设备的新情境，看看你还能不能用上三要素与搜索空间的知识。",
        "summary": "用「机密性、完整性、可用性」三个词，把一份防护方案讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「信息安全」领域的基础课。设计上不引入任何真实产品与品牌，把力气花在三件可操作、可观察的事上：用口令强度估算台把「搜索空间与熵」变成随参数实时变化的数字与估算时长，让学生自己发现长度在指数位置上的作用；用传输链路观测台把「加密」与「完整性校验」的差别变成链路上可见的原文与密文、以及是否发现篡改；用防护策略配置台让学生亲手把措施一条条对到攻击路径上，并从「开了一项却挡不住任何路径」这种真实配置缺陷里理解安全不是堆措施。价值取向上强调没有绝对的安全，只有把风险降到可接受，也提示所有估算仅用于比较防护强弱。",
    "plan_table": """| 1 | cover | 网络安全防护 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：数据是在哪一步丢掉的？ | 起·前测（暴露直觉） |
| 5 | concept | 机密性、完整性、可用性，安全有三个明确目标 | 承·概念一 |
| 6 | interactive | 口令强度估算台：多长才够，多一种字符能顶几位？ | 承·实验室一（搜索空间可观察） |
| 7 | concept | 五个入口，五类防护，一条一条对上 | 承·概念二 |
| 8 | interactive | 传输链路观测台：同一条消息，被看到的内容一样吗？ | 承·实验室二（加密与完整性可观察） |
| 9 | concept | 例题示范：一次账号被盗，怎么一步步查清楚 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给一位同学配一份防护方案 | 合·迁移应用（措施对上路径） |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：风险入口 / 安全目标 / 防护措施三栏标注\n- P5 信息安全三要素图（已生成）：机密性、完整性、可用性及对应手段\n- P7 风险入口与防护对照图（已生成）：五条入口对应五类措施\n- 若需补充：不含任何品牌标识的终端与网络设备示意图",
}
