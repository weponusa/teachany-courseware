# -*- coding: utf-8 -*-
"""初中信息科技 · 隐私保护与数据安全（G9）—— 补齐课标「信息安全」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-privacy-protection-fig1.webp'
F2 = './assets/it-m-privacy-protection-fig2.webp'

TTS = {
    "hero": "先看一份这样的名单。它只有四列：年级、小区、出生日期、社团，一个姓名都没有。制表的人说，这已经匿名了，放心用。可是只要把这几列凑在一起看，名单里的某一行就会被指到唯一一个人身上——因为这一届、这个小区、这个出生月份、又在这个社团的同学，全校只有他一个。姓名去掉了，人却还站在那儿。这节课我们要弄清楚：个人信息到底是怎么被认出来的，又要怎样做才算真的把它处理安全。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道哪些信息算个人信息，还是想知道应用为什么要那么多权限，又或者你想亲手试一次：把姓名去掉之后，别人还能不能认出名单里的人。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出个人信息的核心判据是可识别性，并能区分一般个人信息与敏感个人信息。第二，能说出个人信息处理的五项原则：最小必要、目的限定、知情同意、安全保障、可更正可删除。第三，能在实验台上观察准标识符组合怎样造成重识别，并说出泛化与抑制各自的作用和局限。第四，能对一个数据处理流程逐环节审查，指出每个环节缺了哪项必备措施，并评估残余风险。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "判断一条信息是不是个人信息，核心只有一个词：可识别性。单独一条信息就能指到某个人，或者和其他信息结合起来能指到某个人，它就算个人信息。这里有一条分界线要划清楚：一般个人信息和敏感个人信息。像生物识别、行踪轨迹、医疗健康、金融账户，以及不满十四周岁未成年人的信息，一旦泄露或者被滥用，对个人的影响要严重得多，所以需要更严格的保护，通常还要单独取得同意。处理个人信息要守五项原则：最小必要，只收集与用途直接相关的最少信息；目的限定，收集时说的用途，不能拿去用到别处；知情同意，要让对方清楚知道并自愿同意；安全保障，用加密和权限控制把数据护住；可更正可删除，本人有权要求改错和删掉。",
    "lab-1": "现在你当一次应用权限的决策人。这个校园活动应用申请了六项权限，其中两项是核心功能离不开的，一项是可选的，还有三项和这个应用的功能完全无关。请你逐条决定同意还是拒绝，右边的核心功能可用度和隐私暴露面会实时变化。请你自己找一组配置：既让核心功能能用，又不把无关的权限交出去。算完你会发现，「全部拒绝」和「全部同意」都不是答案。",
    "module-2": "数据从进来走到删掉，要经过五个环节，每个环节都有各自的风险。收集环节的风险是过度索权和超范围收集。存储环节是没加密、长期留存。使用与共享环节是没有去标识化、超出原用途共享。传输环节是明文传输。删除环节是删不干净、到期不清理。对应的措施也很清楚：最小授权、加密存储、去标识化后使用、加密传输、到期自动清理。这里要特别提醒一个高频误解：把姓名去掉，不等于匿名。出生日期、小区、年级这些看起来无害的字段，组合起来就能把一个人重新认出来，它们叫准标识符，是重识别最常用的入口。",
    "lab-2": "我们来亲手做一次重识别。下面是一份已经去掉姓名的名单，八条记录。你可以逐列把年级、小区、出生日期、社团加进来，实验台会实时算出每一组有多大、有多少条记录被单独分到了一组。只要某一组里只有一条记录，那个人就被认出来了。你还可以打开两个泛化开关，看看把出生日期只保留年份、把小区合并成片区之后，数字会变成多少。",
    "worked-example": "我们一起分析一份名单。某社团要发布一份活动统计，打算公布这四列：年级、小区、出生日期、社团。制表的人已经去掉了姓名和学号。请判断它是否安全，并给出处理办法。第一步，确定字段，把每一列都列出来。第二步，找出准标识符，也就是那些单独看没什么、组合起来能指到人的字段。第三步，算唯一组合，看看在选定字段下有多少条记录被单独分成一组。第四步，判断重识别风险：只要还有记录是小分组，就说明它可以被指认。第五步，提出处理办法：把出生日期泛化成年龄段、把小区泛化成片区、把高区分度的字段直接抑制掉，再叠加访问权限控制，把能拿到完整表的人限制在最小范围。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次数据合规审查员。场景是校园活动报名系统要处理一批学生信息，流程分五个环节：收集、存储、使用与共享、传输、删除。每个环节都有对应的措施，你来决定开哪几项，然后点评估。系统会逐环节判断必备措施是否齐全，给出残余风险评分。要特别留意另一组动作：它们听起来很专业，其实不解决任何一个环节的问题，还会增加操作负担。",
    "posttest": "最后用新情境检验一下。这次出现了照片、二维码票根和云端的旧文件，看看你能不能把可识别性、敏感个人信息和五项原则用上去。",
    "summary": "这节课我们弄明白了三件事。第一，判断是不是个人信息，只看可识别性；生物识别、行踪轨迹、医疗健康、金融账户和不满十四周岁未成年人的信息，属于敏感个人信息，要更严格地保护。第二，处理个人信息要守五项原则：最小必要、目的限定、知情同意、安全保障、可更正可删除。第三，去掉姓名不等于匿名，准标识符的组合就能把一个人重新认出来，所以要用泛化、抑制、权限控制这些办法把重识别风险压下去。回到开头那份名单：它去掉的只是最显眼的那一列，真正需要去掉的是可被组合利用的那个组合。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出个人信息的核心判据，并举出三类敏感个人信息。第二层能力应用，动手做：用实验台记录四组配置下的唯一可识别记录数，写一句话说明泛化为什么能降低风险，以及它为什么不能把风险降到零。第三层迁移挑战，选做：为你所在班级设计一份活动名单的发布方案，写出保留哪些字段、泛化哪些字段、抑制哪些字段，并说明每一处取舍的理由。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 可识别性与五项原则", "lab-1": "实验室一 权限最小化配置台",
    "module-2": "概念二 五个环节的风险与措施", "lab-2": "实验室二 重识别实验台",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 合规审查台", "posttest": "后测", "summary": "课堂小结",
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
.ta-tag { padding: 4px 10px; border-radius: 999px; font-size: 13px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); color: var(--text-secondary); }
.ta-tag.warn { background: var(--warm-soft); border-color: var(--warm); color: var(--text-strong); font-weight: 700; }
.ta-tag.ok { background: var(--brand-2-soft); border-color: var(--brand-2); color: var(--text-strong); font-weight: 700; }
.ta-mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; }
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
.perm { display: flex; align-items: flex-start; gap: 10px; padding: 10px 12px; border-radius: 12px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); cursor: pointer; font-size: 14px; }
.perm .state { flex: 0 0 58px; text-align: center; padding: 3px 0; border-radius: 999px; font-size: 12px;
  font-weight: 800; background: rgb(var(--paper-rgb) / .18); color: var(--text-secondary); }
.perm.granted .state { background: var(--brand); color: #fff; }
.perm.granted { border-color: var(--brand); }
.perm.bad .state { background: var(--danger); color: #fff; }
.perm .nm { font-weight: 700; }
.perm .why { color: var(--muted); font-size: 13px; }
.bar-row { display: flex; align-items: center; gap: 10px; font-size: 13px; margin-top: 8px; }
.bar-row .lab { flex: 0 0 96px; color: var(--muted); }
.bar-track { flex: 1; height: 12px; border-radius: 999px; background: rgb(var(--paper-rgb) / .18); overflow: hidden; }
.bar-fill { display: block; height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, var(--brand), var(--brand-2)); transition: width .3s ease; }
.bar-fill.danger { background: var(--danger); }
.bar-fill.warnbar { background: var(--warm); }
.bar-row .val { flex: 0 0 92px; text-align: right; font-variant-numeric: tabular-nums; font-weight: 700; }
.tbl { width: 100%; border-collapse: collapse; font-size: 13px; }
.tbl th, .tbl td { padding: 7px 8px; border-bottom: 1px solid var(--line-subtle); text-align: left; }
.tbl th { color: var(--muted); font-weight: 700; }
.tbl td.solo { background: rgb(var(--brand-rgb) / .16); font-weight: 800; }
.tbl td.mut { background: rgb(var(--paper-rgb) / .12); color: var(--muted); }
.tbl .grp { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-privacy-protection 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 权限最小化配置台：6 项权限 × 同意/拒绝 → 核心功能可用度 + 隐私暴露面 + 权限与用途是否匹配
   3) 重识别实验台：准标识符逐列启用 + 泛化开关 → 分组明细 / 唯一记录数 / 最小分组大小
   4) 合规审查台：5 个环节的必备与可选措施 + 一组无效动作 → 逐环节判定与残余风险
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

  /* ---------- 2. 权限最小化配置台 ---------- */
  var PERMS = [
    { k: 'cam',  n: '使用摄像头', need: 'core', sens: 3, why: '扫码签到是核心功能，没有它就用不了。' },
    { k: 'loc',  n: '获取位置信息', need: 'core', sens: 4, why: '显示活动地点与路线是核心功能的一部分。' },
    { k: 'cont', n: '读取通讯录', need: 'opt',  sens: 4, why: '只影响「邀请好友」是否更方便，不是必须。' },
    { k: 'photo',n: '读取相册全部照片', need: 'none', sens: 3, why: '上传头像只需要你自己选中的那一张，读取整个相册超出了用途。' },
    { k: 'mic',  n: '使用麦克风', need: 'none', sens: 4, why: '这个应用没有任何需要录音的功能。' },
    { k: 'sms',  n: '读取短信', need: 'none', sens: 5, why: '与报名功能完全无关，而短信里常常带着验证码。' }
  ];
  var CORE_NUM = PERMS.filter(function (p) { return p.need === 'core'; }).length;
  var OPT_NUM = PERMS.filter(function (p) { return p.need === 'opt'; }).length;
  var s1 = document.getElementById('s1-stage');
  if (s1) {
    var grant = { cam: false, loc: false, cont: false, photo: false, mic: false, sms: false };

    function render1() {
      var ul = document.getElementById('s1-perms');
      ul.innerHTML = PERMS.map(function (p) {
        var g = grant[p.k];
        var cls = 'perm' + (g ? ' granted' : '') + (g && p.need === 'none' ? ' bad' : '');
        return '<li class="' + cls + '" data-perm="' + p.k + '">' +
          '<span class="state">' + (g ? '已同意' : '未同意') + '</span>' +
          '<span><span class="nm">' + p.n + '</span>' +
          '<span class="ta-tag ' + (p.need === 'none' ? 'warn' : 'ok') + '" style="margin-left:6px">' +
          (p.need === 'core' ? '核心必需' : (p.need === 'opt' ? '可选用' : '与用途无关')) + '</span>' +
          '<br><span class="why">' + p.why + '</span></span></li>';
      }).join('');

      var coreOk = PERMS.filter(function (p) { return p.need === 'core' && grant[p.k]; }).length;
      var optOk = PERMS.filter(function (p) { return p.need === 'opt' && grant[p.k]; }).length;
      var exposed = PERMS.filter(function (p) { return grant[p.k]; });
      var score = 0;
      exposed.forEach(function (p) { score += p.sens; });
      var maxScore = 23;   /* 全部同意的敏感度总和 */
      var pct = score / maxScore * 100;
      var over = PERMS.filter(function (p) { return p.need === 'none' && grant[p.k]; });

      document.getElementById('s1-core').textContent = coreOk + ' / ' + CORE_NUM;
      document.getElementById('s1-exp').textContent = score + ' / ' + maxScore;
      document.getElementById('s1-level').textContent = pct < 40 ? '低' : (pct < 70 ? '中' : '高');
      var bar = document.getElementById('s1-bar');
      bar.style.width = pct.toFixed(0) + '%';
      bar.className = 'bar-fill' + (pct >= 70 ? ' danger' : (pct >= 40 ? ' warnbar' : ''));

      var out = document.getElementById('s1-out');
      if (coreOk < CORE_NUM) {
        out.className = 'result error';
        out.innerHTML = '<strong>核心功能不可用。</strong>还差 ' + (CORE_NUM - coreOk) +
          ' 项核心必需权限。要注意：把什么都拒绝，并不等于更安全，那只是让功能没法用。<br>' +
          '<strong>易错点：</strong>不少同学误认为「全部拒绝最安全」。个人信息保护的原则是最小必要——' +
          '收集范围要和用途对得上，而不是一律不收集。该给的要给，不该给的一律不给。';
        return;
      }
      if (over.length) {
        out.className = 'result error';
        out.innerHTML = '<strong>核心功能可以用了，但有 ' + over.length + ' 项权限与用途不匹配。</strong>' +
          '已同意的是：' + over.map(function (p) { return p.n; }).join('、') + '。<br>' +
          over.map(function (p) { return p.n + '——' + p.why; }).join('<br>') +
          '<br><strong>易错点：</strong>常见错误是只盯着「装得上、能用」，把权限请求当成使用许可。' +
          '权限是别人交给你保管的东西，交出去之前要问一句：这个功能真的需要它吗？';
        return;
      }
      out.className = 'result';
      out.innerHTML = '<strong>这是一组很合适的配置。</strong>核心功能全部可用' +
        (optOk > 0 ? '，并按你的需要开了 ' + optOk + ' 项可选权限' : '，可选权限先不急着给') +
        '；隐私暴露面 ' + score + ' / ' + maxScore + ' 分，等级「' +
        (pct < 40 ? '低' : (pct < 70 ? '中' : '高')) + '」。<br>' +
        '判断的标准只有一条：<strong>这项权限和它支持的功能，能不能对得上。</strong>对得上就给，对不上就不给，' +
        '需要时也可以只在使用的那一次同意。';
    }

    document.getElementById('s1-perms').addEventListener('click', function (e) {
      var li = e.target.closest ? e.target.closest('[data-perm]') : null;
      if (!li) return;
      grant[li.dataset.perm] = !grant[li.dataset.perm];
      render1();
    });
    document.getElementById('s1-reset').addEventListener('click', function () {
      Object.keys(grant).forEach(function (k) { grant[k] = false; });
      render1();
    });
    render1();
  }

  /* ---------- 3. 重识别实验台 ---------- */
  var ROWS = [
    { id: 'R1', grade: '七年级', area: '阳光小区', zone: '东片区', birth: '2011-03', year: '2011', club: '篮球社' },
    { id: 'R2', grade: '七年级', area: '阳光小区', zone: '东片区', birth: '2011-09', year: '2011', club: '篮球社' },
    { id: 'R3', grade: '八年级', area: '阳光小区', zone: '东片区', birth: '2010-05', year: '2010', club: '篮球社' },
    { id: 'R4', grade: '八年级', area: '阳光小区', zone: '东片区', birth: '2010-05', year: '2010', club: '合唱团' },
    { id: 'R5', grade: '九年级', area: '翠湖小区', zone: '西片区', birth: '2009-11', year: '2009', club: '篮球社' },
    { id: 'R6', grade: '九年级', area: '翠湖小区', zone: '西片区', birth: '2009-11', year: '2009', club: '合唱团' },
    { id: 'R7', grade: '七年级', area: '翠湖小区', zone: '西片区', birth: '2011-03', year: '2011', club: '合唱团' },
    { id: 'R8', grade: '八年级', area: '城东小区', zone: '东片区', birth: '2010-05', year: '2010', club: '篮球社' }
  ];
  var s2 = document.getElementById('s2-stage');
  if (s2) {
    var use = { grade: true, area: false, birth: false, club: false };
    var gen = { birthYear: false, areaZone: false };

    function valOf(r, f) {
      if (f === 'grade') return r.grade;
      if (f === 'area') return gen.areaZone ? r.zone : r.area;
      if (f === 'birth') return gen.birthYear ? r.year : r.birth;
      return r.club;
    }

    function render2() {
      var fields = ['grade', 'area', 'birth', 'club'].filter(function (f) { return use[f]; });
      document.querySelectorAll('[data-s2-f]').forEach(function (b) {
        b.classList.toggle('selected', !!use[b.dataset.s2F]);
      });
      document.getElementById('s2-genby').classList.toggle('on', gen.birthYear);
      document.getElementById('s2-genarea').classList.toggle('on', gen.areaZone);

      var groups = {};
      ROWS.forEach(function (r) {
        var key = fields.length ? fields.map(function (f) { return valOf(r, f); }).join(' · ') : '（未选择任何字段）';
        (groups[key] = groups[key] || []).push(r);
      });
      var keys = Object.keys(groups);
      var solo = keys.filter(function (k) { return groups[k].length === 1; }).length;
      var minK = keys.length ? Math.min.apply(null, keys.map(function (k) { return groups[k].length; })) : ROWS.length;

      var head = '<tr><th>编号</th>' + fields.map(function (f) {
        var name = { grade: '年级', area: '小区', birth: '出生日期', club: '社团' }[f];
        return '<th>' + name + (f === 'area' && gen.areaZone ? '（已泛化为片区）' : '') +
          (f === 'birth' && gen.birthYear ? '（已泛化为年份）' : '') + '</th>';
      }).join('') + '<th>所在组大小</th></tr>';
      var body = ROWS.map(function (r) {
        var key = fields.length ? fields.map(function (f) { return valOf(r, f); }).join(' · ') : '（未选择任何字段）';
        var size = groups[key].length;
        return '<tr><td class="grp">' + r.id + '</td>' +
          fields.map(function (f) { return '<td>' + valOf(r, f) + '</td>'; }).join('') +
          '<td class="' + (size === 1 ? 'solo' : 'mut') + '">' + size + (size === 1 ? '　可被指认' : '') + '</td></tr>';
      }).join('');
      document.getElementById('s2-table').innerHTML = '<thead>' + head + '</thead><tbody>' + body + '</tbody>';

      document.getElementById('s2-solo').textContent = solo + ' / ' + ROWS.length;
      document.getElementById('s2-k').textContent = 'k = ' + minK;

      var out = document.getElementById('s2-out');
      if (!fields.length) {
        out.className = 'result warn';
        out.textContent = '还没有选择任何字段。先勾选一个字段开始，再逐列加上去，观察数字怎么变。';
        return;
      }
      var msg;
      if (minK >= 3) {
        msg = '当前最小分组大小是 ' + minK + '，每一行都至少有两个人和它完全一样，单独看某一行指不到具体的人。';
        out.className = 'result';
      } else if (minK === 2) {
        msg = '当前最小分组大小是 2，已经有分组小到只差一步就能指认。再加一列高区分度的字段，风险就会跳升。';
        out.className = 'result warn';
      } else {
        msg = '当前有 ' + solo + ' 条记录被单独分到了一组，也就是说这 ' + solo + ' 个人可以被直接认出来。';
        out.className = 'result error';
      }
      out.innerHTML = '<strong>已启用字段：' + fields.length + ' 列，唯一可识别记录 ' + solo + ' / ' + ROWS.length +
        '，最小分组大小 k = ' + minK + '。</strong><br>' + msg + '<br>' +
        '<strong>易错点：</strong>最常见的误解是「去掉了姓名就等于匿名」。姓名只是最显眼的那一列，' +
        '出生日期、小区、年级这些<strong>准标识符</strong>组合起来同样能指到人。泛化能明显降低风险' +
        '（这里从 8 条可指认压到了 1 条），但它<strong>不能把风险降到零</strong>——' +
        '剩下的分辨度还得靠抑制高区分度字段、把出生日期这类数据换成区间，再加上访问权限控制来兜住。';
    }

    document.querySelectorAll('[data-s2-f]').forEach(function (b) {
      b.addEventListener('click', function () {
        use[b.dataset.s2F] = !use[b.dataset.s2F];
        render2();
      });
    });
    document.getElementById('s2-genby').addEventListener('click', function () { gen.birthYear = !gen.birthYear; render2(); });
    document.getElementById('s2-genarea').addEventListener('click', function () { gen.areaZone = !gen.areaZone; render2(); });
    document.getElementById('s2-reset').addEventListener('click', function () {
      use = { grade: true, area: false, birth: false, club: false };
      gen = { birthYear: false, areaZone: false };
      render2();
    });
    render2();
  }

  /* ---------- 4. 合规审查台 ---------- */
  var STAGES = [
    { k: 'collect', n: '① 收集', weight: 30, req: ['minimal'], opt: ['notice'],
      why: '收集环节的必备措施是最小必要：只收与报名直接相关的字段。说明用途与保存期限是加分项。' },
    { k: 'store', n: '② 存储', weight: 20, req: ['encrypt'], opt: ['access'],
      why: '存储环节的必备措施是加密存储；访问权限控制让能碰到数据的人缩到最小。' },
    { k: 'share', n: '③ 使用与共享', weight: 25, req: ['deid'], opt: ['scope'],
      why: '使用与共享环节的必备措施是去标识化后使用；限定共享范围并留审批记录是加分项。' },
    { k: 'trans', n: '④ 传输', weight: 15, req: ['tls'], opt: ['integ'],
      why: '传输环节的必备措施是加密传输；完整性校验可以发现途中被改动。' },
    { k: 'del', n: '⑤ 删除', weight: 10, req: ['expire'], opt: ['self'],
      why: '删除环节的必备措施是到期自动清理；提供自助删除入口是加分项。' }
  ];
  var MEAS = {
    minimal: { n: '只收与报名直接相关的字段', kind: 'req' },
    notice:  { n: '说明用途与保存期限', kind: 'opt' },
    encrypt: { n: '加密存储', kind: 'req' },
    access:  { n: '访问权限控制', kind: 'opt' },
    deid:    { n: '去标识化后使用', kind: 'req' },
    scope:   { n: '限定共享范围并留审批记录', kind: 'opt' },
    tls:     { n: '加密传输', kind: 'req' },
    integ:   { n: '完整性校验', kind: 'opt' },
    expire:  { n: '到期自动清理', kind: 'req' },
    self:    { n: '提供自助删除入口', kind: 'opt' },
    slogan:  { n: '在声明里写一句「我们非常重视您的隐私」', kind: 'none' },
    nick:    { n: '把昵称改成编号，但保留完整手机号', kind: 'none' }
  };
  var syn = document.getElementById('syn-stage');
  if (syn) {
    var on = {};
    Object.keys(MEAS).forEach(function (k) { on[k] = false; });
    var ran = false;

    function renderSyn() {
      Object.keys(MEAS).forEach(function (k) {
        var el = document.getElementById('syn-sw-' + k);
        if (el) el.classList.toggle('on', on[k]);
      });
      var out = document.getElementById('syn-out');
      if (!ran) {
        out.className = 'result warn';
        out.textContent = '选好每个环节要做的措施，然后点「评估这条流程」。';
      }
    }
    document.querySelectorAll('[data-syn-sw]').forEach(function (el) {
      el.addEventListener('click', function () {
        on[el.dataset.synSw] = !on[el.dataset.synSw];
        ran = false; renderSyn();
      });
    });
    document.getElementById('syn-run').addEventListener('click', function () {
      var rows = [], left = 0, okStages = 0, missing = [];
      STAGES.forEach(function (S) {
        var lack = S.req.filter(function (k) { return !on[k]; });
        var bonus = S.opt.filter(function (k) { return on[k]; });
        if (!lack.length) { okStages += 1; }
        else { left += S.weight; missing.push(S.n + ' 缺「' + lack.map(function (k) { return MEAS[k].n; }).join('、') + '」'); }
        rows.push('<li class="' + (lack.length ? 'bad' : 'ok') + '"><span class="tag">' + S.n + '（权重 ' + S.weight + '）</span>' +
          (lack.length
            ? '必备措施缺失：' + lack.map(function (k) { return MEAS[k].n; }).join('、') + '。' + S.why
            : '已达标。' + S.why + (bonus.length ? ' 另外还开了：' + bonus.map(function (k) { return MEAS[k].n; }).join('、') + '。' : '')) + '</li>');
      });
      var score = left;
      var level = score <= 15 ? '低' : (score <= 45 ? '中' : '高');
      rows.push('<li class="' + (score <= 45 ? 'ok' : 'bad') + '"><span class="tag">评估</span>五个环节中 ' + okStages +
        ' 个达标，残余风险 ' + score + ' 分，风险等级：<strong>' + level + '</strong>。' +
        (missing.length ? '待补：' + missing.join('；') + '。' : '') + '</li>');
      var idle = Object.keys(MEAS).filter(function (k) { return MEAS[k].kind === 'none' && on[k]; });
      if (idle.length) {
        rows.push('<li class="bad"><span class="tag">提示</span>「' + idle.map(function (k) { return MEAS[k].n; }).join('」和「') +
          '」不解决任何一个环节的问题。前者是一句没有对应动作的声明，后者留下了手机号这个直接标识符，去标识化等于没做。' +
          '这类动作不会降低风险，只会增加操作负担。</li>');
      }
      if (score === 0) {
        rows.push('<li class="ok"><span class="tag">完成</span>五个环节的必备措施都到位了。请记住：合规不是一次性的检查，而是每个环节都要一直守着。</li>');
      }
      var out = document.getElementById('syn-out');
      out.className = 'result ' + (score <= 15 ? '' : (score <= 45 ? 'warn' : 'error'));
      out.innerHTML = '<ul class="ta-log">' + rows.join('') + '</ul>';
      ran = true;
    });
    document.getElementById('syn-reset').addEventListener('click', function () {
      Object.keys(MEAS).forEach(function (k) { on[k] = false; });
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：哪些信息算个人信息？", TTS["pretest"], [
        {"q": "一份名单去掉了姓名和学号，只留下年级、小区、出生日期和社团。它算不算已经匿名了？",
         "options": [("不算，这几列组合起来仍然可能指到具体的人", True),
                     ("算，姓名去掉了就认不出人了", False),
                     ("要看名单有多少人，人多就一定安全", False)],
         "explain": "判断是不是个人信息，看的是能不能识别到具体的人。姓名只是最显眼的一列，其余几列组合起来同样能做到。<strong>错因提醒：</strong>最常见的错误就是误认为「去掉姓名就等于匿名」，这也是重识别最常走的入口。"},
        {"q": "下面哪一类信息属于敏感个人信息，一旦泄露影响更严重？",
         "options": [("行踪轨迹与医疗健康信息", True),
                     ("参加过的社团名称", False),
                     ("喜欢的运动项目", False)],
         "explain": "生物识别、行踪轨迹、医疗健康、金融账户，以及不满十四周岁未成年人的信息，都属于敏感个人信息，需要更严格的保护，通常还要单独取得同意。<strong>错因提醒：</strong>容易把「和身体有关」当成唯一标准，忽略了行踪轨迹这类同样高影响的信息。"},
        {"q": "一个活动报名应用申请读取短信，但这个应用没有任何和短信相关的功能。这属于：",
         "options": [("超出了用途的权限请求，应当拒绝", True),
                     ("正常做法，装应用都要给这些权限", False),
                     ("可以同意，反正也不会真去读", False)],
         "explain": "最小必要原则要求收集范围与用途对得上。对不上的权限，就是不应该交出去的权限。<strong>错因提醒：</strong>常见误解是「点了同意也没关系」——同意本身就是一次授权，它会改变对方能做什么。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "可识别性：判断个人信息的唯一标准", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道数据在采集、传输、存储的每个环节都可能被人盯上，也学过用加密、权限、多因素认证把这些风险挡住。<strong>但</strong>那些手段回答的是「别人能不能拿到」。还有一件事它们回答不了：哪些数据本来就<strong>不该被收走</strong>，收走之后又该按什么规矩处理。<strong>所以</strong>我们需要先弄清楚「个人信息」到底指什么。</p>
        </div>
        <p style="font-size:17px;margin:12px 0"><strong>个人信息</strong>是指：以电子或者其他方式记录的、能够单独或者与其他信息结合识别到特定自然人的各种信息。判据只有一个词——<strong>可识别性</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>一般个人信息</strong></p>
            <p style="color:var(--muted)">姓名、年级、社团、兴趣爱好等。处理时同样要遵守原则。</p>
          </div>
          <div class="inner-card">
            <p><strong>敏感个人信息</strong></p>
            <p style="color:var(--muted)">生物识别、行踪轨迹、医疗健康、金融账户，以及不满十四周岁未成年人的信息。泄露后影响更严重，通常需要单独同意。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="个人信息处理五个环节的风险与对应保护措施示意图">
          <figcaption>收集 → 存储 → 使用与共享 → 传输 → 删除：五个环节各有风险，也各有对应的措施</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">📏</span><div><strong>记忆锚点：</strong>把五项原则记成五句自问——<strong>最</strong>少要哪些字段（最小必要）、<strong>用</strong>到哪儿去（目的限定）、<strong>说</strong>清楚了吗（知情同意）、<strong>护</strong>住了吗（安全保障）、<strong>能</strong>改能删吗（可更正可删除）。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一个字段，放在不同的组合里，识别能力完全不同。小区单独看是公共场所信息，配上年级和出生日期，就能指到一个具体的人。"},
    {"lens": "解释它", "text": "为什么「去掉了姓名」不够？因为识别靠的是缩小范围，不是靠唯一标识。每多一个字段，符合条件的人就少一批，直到只剩一个。"},
    {"lens": "迁移它", "text": "快递面单上的姓名可以打码，但手机号、地址、订单时间凑在一起，同样能还原出是谁——这就是面单要整体脱敏的原因。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "权限最小化配置台：该给的要给，不该给的一律不给", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">点任意一项权限即可切换「已同意 / 未同意」。右边会实时算出核心功能可用度和隐私暴露面。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">应用申请的权限</p>
              <ul class="ta-log" id="s1-perms" style="cursor:pointer"></ul>
            </div>
            <div id="s1-stage">
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">实时结果</p>
              <div class="lab-readout">
                <div class="readout-cell"><span class="k">核心功能可用度</span><span class="v green" id="s1-core">0 / 2</span></div>
                <div class="readout-cell"><span class="k">隐私暴露面</span><span class="v" id="s1-exp">0 / 23</span></div>
                <div class="readout-cell"><span class="k">暴露等级</span><span class="v" id="s1-level">低</span></div>
              </div>
              <div class="bar-row">
                <span class="lab">隐私暴露面</span>
                <span class="bar-track"><span class="bar-fill" id="s1-bar"></span></span>
              </div>
              <p class="result warn" id="s1-out" style="margin-top:12px"></p>
              <button class="choice" id="s1-reset" style="text-align:center;margin-top:10px">全部重置为未同意</button>
            </div>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>请自己找一组配置：</strong>让核心功能能用，同时不把与用途无关的权限交出去。<strong>易错点：</strong>误认为「全部拒绝最安全」——那只是让功能没法用；也误认为「同意了也没关系」——同意本身就是一次授权。</div></div>
    ''', tag="权限实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "五个环节的风险，对上五类措施", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>数据不是一件事，而是一段流程。</strong>从收进来的那一刻到删掉的那一刻，每个环节都可能出问题，所以保护措施也要一个环节一个环节地放上去。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>收集</strong>：过度索权、超范围收集。措施：最小必要，只收与用途直接相关的最少字段。</div></div>
          <div class="step"><span class="n">2</span><div><strong>存储</strong>：明文存放、长期留存。措施：加密存储，并用访问权限控制把能碰到数据的人缩到最小。</div></div>
          <div class="step"><span class="n">3</span><div><strong>使用与共享</strong>：未去标识化、超出原用途共享。措施：去标识化后使用，并限定共享范围、留下审批记录。</div></div>
          <div class="step"><span class="n">4</span><div><strong>传输</strong>：明文传输，途中被截获或被改动。措施：加密传输，并做完整性校验。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>删除</strong>：到期不清理、删得不彻底。措施：到期自动清理，并提供自助删除入口。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="最小必要收集与准标识符重识别的对比示意图">
          <figcaption>左边是字段与用途的对应：只收有明确用途的字段；右边即使表里没有姓名，准标识符的组合仍可能把某一行指到具体的人</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">三个高频误解：一是<strong>误认为「去掉了姓名就算匿名」</strong>——出生日期、小区、年级这些准标识符组合起来照样能指到人；二是<strong>误认为「勾选了同意就一切都合法」</strong>——同意只是五项原则中的一条，超范围收集、超用途使用仍然不合规；三是<strong>误认为「在应用里删掉记录，数据就没了」</strong>——删除要看的是后台是否真的清理，而不只是你的界面看不到了。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "重识别实验台：去掉姓名之后，人还站在那儿吗？", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">勾选要公开的字段，观察每一条记录所在的组有多大。组大小等于 1，就意味着这条记录能被直接指认。</p>
        <div class="lab-panel">
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-s2-f="grade" style="text-align:center">年级</button>
            <button class="choice" data-s2-f="area" style="text-align:center">小区</button>
            <button class="choice" data-s2-f="birth" style="text-align:center">出生日期</button>
            <button class="choice" data-s2-f="club" style="text-align:center">社团</button>
          </div>
          <div class="sw-wrap" style="margin-top:12px">
            <div class="sw" id="s2-genby"><span class="dot"></span><span><span class="name">泛化：出生日期只保留年份</span><br><span class="desc">把高区分度的精确值换成较粗的区间</span></span></div>
            <div class="sw" id="s2-genarea"><span class="dot"></span><span><span class="name">泛化：小区合并为片区</span><br><span class="desc">阳光小区与城东小区合并为东片区</span></span></div>
          </div>
          <div id="s2-stage" style="margin-top:14px">
            <div style="overflow-x:auto"><table class="tbl" id="s2-table"></table></div>
            <div class="lab-readout">
              <div class="readout-cell"><span class="k">唯一可识别记录</span><span class="v" id="s2-solo">0 / 8</span></div>
              <div class="readout-cell"><span class="k">最小分组大小</span><span class="v green" id="s2-k">k = 8</span></div>
            </div>
          </div>
          <p class="result warn" id="s2-out" style="margin-top:12px"></p>
          <div class="flex-row">
            <button class="choice" id="s2-reset" style="text-align:center">重置字段与泛化</button>
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧩</span><div><strong>请记录四组数据：</strong>只用年级、加上小区、再加上出生日期、再加上社团，各自的最小分组大小 k 是多少。然后打开两个泛化开关，看看 k 能回到多少。<strong>易错点：</strong>泛化能明显降低风险，但不能把它降到零。</div></div>
    ''', tag="重识别实验台", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：这份「匿名」名单能不能发布？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>题目：</strong>某社团要发布一份活动统计，计划公布四列：年级、小区、出生日期、社团。制表时已经去掉了姓名和学号。请判断这份名单是否可以发布，并给出处理办法。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>确定字段：</strong>把每一列都写出来。不要只看「有没有姓名」，要看这张表一共有几列、每列能提供多少分辨度。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找出准标识符：</strong>那些单独看没什么、组合起来能缩小到个人的字段。出生日期、小区、年级都属于这一类，社团同样会提供分辨度。</div></div>
          <div class="step"><span class="n">3</span><div><strong>算唯一组合：</strong>在选定字段下，把每条记录按取值分组，数一数有多少组里只有一条记录。组大小为 1 的记录，就是可以被直接指认的那几个人。</div></div>
          <div class="step"><span class="n">4</span><div><strong>判断重识别风险：</strong>只要还存在小分组，这份表就不能算匿名。要注意，记录数多不等于安全——分辨度是由字段决定的，不是由行数决定的。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>给出处理办法：</strong>把出生日期泛化成年龄段、把小区泛化成片区、把社团这类高区分度字段直接抑制掉；再叠加访问权限控制，把能拿到完整表的人限制在最小范围。如果发布目的只是统计数量，就只给出汇总结果，不给出明细。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最常见的两种错法：一是<strong>误认为去掉姓名就万事大吉</strong>，于是把出生日期这类强分辨度字段原样保留；二是<strong>把泛化当成万能药</strong>，以为处理过就一定安全。事实上泛化只是把分辨度降低，剩下的部分还要靠抑制字段、只发布汇总、限制访问范围来兜住。另一种容易<strong>搞混</strong>的是把「没人认得这张表」当成理由——判断依据是数据本身能不能被关联，不是现在有没有人去看。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("只要信息能被组合起来识别到具体的人，它就属于个人信息", True),
                     ("只有姓名和身份证号才算个人信息", False),
                     ("照片里没有姓名，所以不算个人信息", False)],
         "explain": "判据是可识别性，不是字段名称。照片本身就能识别人，属于个人信息，人脸还是敏感个人信息。<strong>错因提醒：</strong>最常见的就是按字段名称判断，把「看起来不像身份信息」的内容当成无关数据。"},
        {"q": "某应用收集了手机号，说是用于登录，后来又把手机号用于短信推广。这违反了哪一项原则？",
         "options": [("目的限定，收集时说的用途不能拿去用到别处", True),
                     ("安全保障，手机号没有被加密", False),
                     ("可更正可删除，用户无法修改手机号", False)],
         "explain": "收集时说明的用途，就是处理范围的边界。换用途需要重新取得同意。<strong>错因提醒：</strong>容易搞混「用途变了」和「存储不安全」——这两件事对应的是不同原则，判断时要先找准被违反的那一条。"},
        {"q": "把用户昵称改成编号，但表里仍然保留完整手机号。这次去标识化：",
         "options": [("基本没有效果，因为手机号本身就是可以直接识别到人的标识符", True),
                     ("已经足够，昵称是最容易被看到的信息", False),
                     ("效果很好，只要编号不复用就行", False)],
         "explain": "去标识化要去掉的是能直接指到人的标识符，手机号正是最典型的一种。<strong>错因提醒：</strong>常见错误是只处理「最显眼的那一列」，把真正有识别能力的字段留在原地。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次数据合规审查员", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">场景：校园活动报名系统要处理一批学生信息，流程分五个环节。请为每个环节选择要做的措施，然后点评估。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">① 流程的五个环节</p>
              <ul class="ta-log">
                <li><span class="tag">环节</span>收集（权重 30）· 存储（权重 20）</li>
                <li><span class="tag">环节</span>使用与共享（权重 25）</li>
                <li><span class="tag">环节</span>传输（权重 15）· 删除（权重 10）</li>
                <li><span class="tag">说明</span>每个环节都有必须做到的必备措施，也有可选的加分项。</li>
              </ul>
            </div>
            <div>
              <p style="font-weight:700;font-size:14px;margin:0 0 8px">② 可以做的措施</p>
              <div class="sw-wrap" id="syn-stage">
                <div class="sw" id="syn-sw-minimal" data-syn-sw="minimal"><span class="dot"></span><span><span class="name">只收与报名直接相关的字段</span><br><span class="desc">收集环节 · 必备</span></span></div>
                <div class="sw" id="syn-sw-notice" data-syn-sw="notice"><span class="dot"></span><span><span class="name">说明用途与保存期限</span><br><span class="desc">收集环节 · 可选</span></span></div>
                <div class="sw" id="syn-sw-encrypt" data-syn-sw="encrypt"><span class="dot"></span><span><span class="name">加密存储</span><br><span class="desc">存储环节 · 必备</span></span></div>
                <div class="sw" id="syn-sw-access" data-syn-sw="access"><span class="dot"></span><span><span class="name">访问权限控制</span><br><span class="desc">存储环节 · 可选</span></span></div>
                <div class="sw" id="syn-sw-deid" data-syn-sw="deid"><span class="dot"></span><span><span class="name">去标识化后使用</span><br><span class="desc">使用与共享环节 · 必备</span></span></div>
                <div class="sw" id="syn-sw-scope" data-syn-sw="scope"><span class="dot"></span><span><span class="name">限定共享范围并留审批记录</span><br><span class="desc">使用与共享环节 · 可选</span></span></div>
                <div class="sw" id="syn-sw-tls" data-syn-sw="tls"><span class="dot"></span><span><span class="name">加密传输</span><br><span class="desc">传输环节 · 必备</span></span></div>
                <div class="sw" id="syn-sw-integ" data-syn-sw="integ"><span class="dot"></span><span><span class="name">完整性校验</span><br><span class="desc">传输环节 · 可选</span></span></div>
                <div class="sw" id="syn-sw-expire" data-syn-sw="expire"><span class="dot"></span><span><span class="name">到期自动清理</span><br><span class="desc">删除环节 · 必备</span></span></div>
                <div class="sw" id="syn-sw-self" data-syn-sw="self"><span class="dot"></span><span><span class="name">提供自助删除入口</span><br><span class="desc">删除环节 · 可选</span></span></div>
                <div class="sw" id="syn-sw-slogan" data-syn-sw="slogan"><span class="dot"></span><span><span class="name">在声明里写一句「我们非常重视您的隐私」</span><br><span class="desc">听上去很专业，但它不解决任何一个环节</span></span></div>
                <div class="sw" id="syn-sw-nick" data-syn-sw="nick"><span class="dot"></span><span><span class="name">把昵称改成编号，但保留完整手机号</span><br><span class="desc">看起来做了去标识化，实际上留下了直接标识符</span></span></div>
              </div>
            </div>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px"></p>
          <div class="flex-row">
            <button class="choice" id="syn-run" style="text-align:center;flex:1">评估这条流程</button>
            <button class="choice" id="syn-reset" style="text-align:center;flex:1">重置</button>
          </div>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>如果评审时间只够你检查两个环节，你会先查哪两个？请说明理由，并指出你暂时不查的那几个环节可能留下什么风险。</p>
          <textarea id="syn-answer" rows="3" placeholder="我会先查……因为……；暂时不查……可能留下……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，原则还在不在", TTS["posttest"], [
        {"q": "一位同学把活动合影发到了公开的页面上，照片里有其他同学的正脸。最需要注意的是：",
         "options": [("正脸照属于可识别的个人信息，公开前应当先征得本人同意", True),
                     ("只要不写名字，照片就可以随便发", False),
                     ("人多的时候就不算个人信息了", False)],
         "explain": "人脸是可以直接识别到人的信息，属于敏感个人信息，公开前必须取得同意。<strong>错因提醒：</strong>常见错误是误认为「照片没有文字标注就不算信息」，忽略了图像本身就能识别。"},
        {"q": "一张活动的二维码票根被发到群里，上面还有一串编号。可能有什么风险？",
         "options": [("票根可能关联到具体的人和行踪轨迹，属于不该公开的信息", True),
                     ("只是编号，没有姓名，没有风险", False),
                     ("先发出去，活动结束后自然就失效了", False)],
         "explain": "票根常与实名信息绑定，还能反映在什么时间出现在什么地方，也就是行踪轨迹，属于敏感个人信息。<strong>错因提醒：</strong>容易把「看不出是什么」当成「不会被用到」——关联能力取决于数据持有方，不取决于你有没有看懂。"},
        {"q": "手机里存着三年前的一份报名表，上面有同学的手机号。按照教学内容里的原则，最合适的做法是：",
         "options": [("按保存期限及时清理，需要留存的先去掉直接标识符", True),
                     ("存在手机里最安全，比放云端好", False),
                     ("只要不发给别人，存多久都没关系", False)],
         "explain": "可更正可删除与到期清理是五项原则里的要求，长期留存本身就是风险。<strong>错因提醒：</strong>把「没给别人看」等同于「没有风险」，是这一课最需要纠正的想法之一。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>判据</strong>：个人信息看的是<strong>可识别性</strong>——单独或者与其他信息结合能识别到特定自然人的，都算；生物识别、行踪轨迹、医疗健康、金融账户和不满十四周岁未成年人的信息属于敏感个人信息。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>五项原则</strong>：最小必要（只收最少的必要字段）、目的限定（不挪作他用）、知情同意、安全保障、可更正可删除。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>一个可验证的判断</strong>：去掉姓名不等于匿名。准标识符组合起来就能把记录指到人，泛化与抑制能大幅降低重识别风险，但还需要权限控制兜住剩下的部分。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:var(--warm)">
          <p style="margin:0"><strong>回到开头那份名单：</strong>它去掉的只是最显眼的那一列。四列里任意三列凑在一起，就足以让某一行只剩下一个人。真正要做的是把可被组合利用的分辨度降下来——泛化出生日期、合并小区、抑制社团，再把完整表的访问范围收窄。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「可识别性、准标识符、最小必要」三个词，说明为什么「去掉姓名就能发布」这个判断是不成立的。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出个人信息的核心判据，并举出三类敏感个人信息，各写一句为什么它的影响更严重。",
            "写出个人信息处理的五项原则，每一条配一个具体做法。",
            "说明「权限与用途是否对得上」这个判断标准，并举一个对不上的例子。",
        ],
        [
            "用课堂上的重识别实验台记录四组配置（只年级、加小区、加出生日期、加社团）下的最小分组大小 k 和唯一可识别记录数，写一句话说明变化规律。",
            "打开两个泛化开关，记录 k 的变化，并写一句话说明泛化为什么能降低风险，又为什么不能把风险降到零。",
        ],
        [
            "为你所在班级设计一份活动名单的发布方案：写出保留哪些字段、泛化哪些字段、抑制哪些字段、只发布汇总还是发布明细，并逐条说明取舍理由。",
            "找出身边一件含有个人信息的物品（如快递面单、票根、旧的报名表），说明它含有哪些字段、这些字段组合起来能识别到什么程度，并给出两条具体的处理办法。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-privacy-protection",
    "node_id": "it-m-privacy-protection",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "隐私保护与数据安全",
    "name_en": "Privacy Protection and Data Security",
    "grade": 9,
    "grade_cn": "九年级",
    "domain": "security",
    "domain_cn": "信息安全",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "以一份去掉姓名后仍可被指认的名单为起点，理解个人信息的核心判据是可识别性，区分一般个人信息与敏感个人信息，掌握最小必要、目的限定、知情同意、安全保障、可更正可删除五项原则；通过权限最小化配置台在功能可用度与隐私暴露面之间取舍，通过重识别实验台观察准标识符组合、泛化与最小分组大小的变化，并能对整个数据处理流程逐环节审查与评估残余风险。",
    "tags": ["个人信息", "可识别性", "敏感个人信息", "最小必要", "去标识化", "准标识符", "重识别", "数据安全"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「信息安全」——理解个人信息保护原则，安全处理敏感数据。",
    "hero_question": "一份去掉了姓名的名单，为什么还能被人认出来？",
    "hero_alt": "隐私保护与数据安全知识结构图：个人信息判据、处理环节与保护措施三栏",
    "hero_caption": "判据（可识别性 · 一般与敏感之分）→ 处理环节（收集 · 存储 · 使用共享 · 传输 · 删除）→ 措施（最小必要 · 加密 · 去标识化 · 权限控制 · 到期清理）",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "哪些信息算是个人信息？", "d": "有没有一条能照着判断的标准", "v": "哪些信息算是个人信息"},
        {"t": "应用为什么要那么多权限？", "d": "哪些该给，哪些不该给", "v": "应用为什么要那么多权限"},
        {"t": "去掉姓名就真的认不出人了吗？", "d": "想亲手试一次重识别", "v": "去掉姓名就真的认不出人了吗"},
        {"t": "一条数据流程怎么做才算合规？", "d": "想逐环节检查缺了什么", "v": "一条数据流程怎么做才算合规"},
    ],
    "objectives": [
        "能说出个人信息的核心判据是可识别性，并区分一般个人信息与敏感个人信息",
        "能说出个人信息处理的五项原则，并各举一个具体做法",
        "能观察准标识符组合对重识别的影响，并说明泛化与抑制的作用与局限",
        "能对数据处理流程逐环节审查必备措施是否齐全，并评估残余风险等级",
    ],
    "objectives_plain": [
        "能说出个人信息的核心判据是可识别性，并区分一般个人信息与敏感个人信息",
        "能说出个人信息处理的五项原则，并各举一个具体做法",
        "能观察准标识符组合对重识别的影响，并说明泛化与抑制的作用与局限",
        "能对数据处理流程逐环节审查必备措施是否齐全，并评估残余风险等级",
    ],
    "standards": [
        {"content": "理解个人信息保护原则，安全处理敏感数据。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》信息安全 · 初中"},
        {"content": "知道个人信息保护的相关要求，能在真实情境中安全处理敏感数据，尊重他人隐私，承担信息社会责任。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》信息社会责任 · 初中"},
    ],
    "prereqs": ["it-m-cybersecurity"],
    "prereqs_name": "网络安全防护",
    "prereqs_meta": "it-m-cybersecurity",
    "leads_to": [],
    "next_meta": "无（初中信息安全收束）",
    "section_images": ["assets/it-m-privacy-protection-fig1.webp", "assets/it-m-privacy-protection-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一份没有姓名的名单，仍然可能指到具体的人。带着这个反直觉的事实开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能判断一份数据能不能对外发布。",
        "objectives": "看清四件事：说出可识别性、说出五项原则、观察重识别与泛化的效果、能逐环节审查一条数据流程。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "判据是可识别性；敏感个人信息要更严格保护，通常需要单独同意。",
        "lab-1": "自己找一组配置：核心功能能用，同时不交出与用途无关的权限。全同意和全拒绝都不是答案。",
        "module-2": "五个环节各有风险：过度收集、明文存储、未去标识化共享、明文传输、删不干净。",
        "lab-2": "逐列加上字段，盯着「唯一可识别记录」和 k 值的跳变；再打开两个泛化开关对比。",
        "worked-example": "五步走：确定字段、找准标识符、算唯一组合、判断风险、给出处理办法。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "开措施之前先问一句：它守的是哪一个环节？有些动作听起来专业，却不解决任何环节。",
        "posttest": "换了合影、票根和旧文件的场景，看看你还能不能用上可识别性与五项原则。",
        "summary": "用「可识别性、准标识符、最小必要」三个词，说明为什么「去掉姓名就能发布」不成立。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课承接已建成的网络安全课，把视角从「别人能不能拿到数据」转到「哪些数据本来就不该被收走、收走之后该按什么规矩处理」。设计上有两处可观察的核心实验：权限最小化配置台把「最小必要」变成功能可用度与隐私暴露面两个同时变化的数字，让学生亲手发现「全部拒绝」和「全部同意」都不是答案；重识别实验台让学生逐列勾选准标识符，看着最小分组大小 k 从 3 掉到 1，再打开泛化开关看它回升到多少，从而诚实地理解泛化能显著降低风险但不能把风险降到零，剩下的部分需要靠抑制字段与访问权限控制兜住。综合任务把五项原则拆到数据流程的五个环节上，并要求学生识别出「听起来专业却不解决任何环节」的动作。全课不出现任何真实产品与品牌，所有数据均为教学用虚构样例。",
    "plan_table": """| 1 | cover | 隐私保护与数据安全 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：哪些信息算个人信息？ | 起·前测（暴露直觉） |
| 5 | concept | 可识别性：判断个人信息的唯一标准 | 承·概念一（判据与五项原则） |
| 6 | interactive | 权限最小化配置台：该给的要给，不该给的一律不给 | 承·实验室一（双指标取舍可观察） |
| 7 | concept | 五个环节的风险，对上五类措施 | 承·概念二（含高频误解） |
| 8 | interactive | 重识别实验台：去掉姓名之后，人还站在那儿吗？ | 承·实验室二（k 值变化可观察） |
| 9 | concept | 例题示范：这份「匿名」名单能不能发布？ | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次数据合规审查员 | 合·迁移应用（措施对上环节） |
| 12 | quiz | 后测：换一个情境，原则还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：判据 / 处理环节 / 保护措施三栏标注\n- P5 数据生命周期图（已生成）：五个环节的风险与对应措施\n- P7 最小必要与重识别对比图（已生成）：去掉姓名后准标识符组合仍可指认\n- 若需补充：不含任何品牌标识的权限授权界面示意图",
}
