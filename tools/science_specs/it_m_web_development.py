# -*- coding: utf-8 -*-
"""初中信息科技 · 网页与在线应用制作（G7）—— 补齐课标「互联网应用与创新」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-web-development-fig1.webp'
F2 = './assets/it-m-web-development-fig2.webp'

TTS = {
    "hero": "先看一个真实的需求。班级的图书漂流角越来越热闹，可登记还靠一张纸，写着写着就找不到是谁什么时候借走的。有人提议：做一个能填、能交、能立刻看到结果的登记页面。这件事听起来要写很多代码，其实它只由三部分组成：描述内容的结构、控制外观的样式、响应操作的行为。这节课我们就动手把这三块拼起来。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道一个页面到底由哪几部分组成，还是想知道点了按钮之后究竟发生了什么，又或者你想亲手做出一个能真正填表、能挡住错误输入的登记页面。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出网页由结构、表现、行为三部分组成，并说明三者分工不同的好处。第二，能用标记描述内容的结构，并说出文档树是怎么形成的。第三，能描述一次交互的完整链路：用户输入、事件触发、更新数据、刷新界面。第四，能为一个真实需求设计表单，写出必填与格式校验规则，并说明为什么只收集必要的信息。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "一个页面由三部分分工完成。结构用标记来描述内容，它只说明这一段是什么：是标题、是段落、是一份列表，还是一个可以填写的输入框，它不负责好不好看。表现用样式规则控制外观，颜色、字号、间距都在这里定。行为用脚本响应操作，读写页面里的节点。三者分开写，改外观的时候不会碰坏内容，内容也能被朗读软件准确读出来。",
    "lab-1": "现在亲手搭一次结构。屏幕左边是一组结构卡片，每张卡片代表内容里的一个部分。点一张卡片，它就会进入右边的文档树，同时下方的预览区立刻渲染出对应的样子。注意两件事：容器卡片要先进去，里面的子卡片才有地方放；树上的节点数会随着你的每一次点击变化。",
    "module-2": "点了按钮之后到底发生了什么？完整的一条链路是四步：用户输入内容，输入或点击触发了事件，事件的处理过程把数据更新掉，最后界面按照新的数据重新渲染一次。这四步会不断循环。最容易搞混的一点是：改了数据，界面并不会自己变——必须由处理过程明确地去刷新它。反过来，如果只在界面上做手脚而数据没变，下一次刷新时改动就消失了。",
    "lab-2": "现在把这条链路跑一遍，并且故意让它出一次错。输入一条书目，点添加，你会看到四个数字同步变化：输入内容、数据条数、界面条数、文档树节点数。然后把刷新开关关掉再添加一条，盯住数据条数和界面条数——它们会不一致。这个不一致，就是前端最典型的一类问题。",
    "worked-example": "我们一起分析一个真实的故障。有同学做了一个登记页面，点提交之后没有任何反应，他以为是样式写错了。第一步，看清现象：点击有响应，但界面没有变化。第二步，检查事件有没有被接上：按钮上确实绑定了点击处理。第三步，检查数据有没有被更新：在点击之后打印数据，发现条数根本没变，处理过程在中途遇到了一个不存在的节点就停住了。第四步，定位并修复：先确认要操作的那个节点在文档树里真的存在，再让数据更新，最后才刷新界面——顺序不能颠倒。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次产品设计者。班级要做一个图书漂流登记页面，需要填三类信息：书名、借出日期，以及可填可不填的联系方式。请你先把表单搭出来，再定下校验规则，然后亲自试几次：把书名为空、把日期写成不存在的日期、把联系方式填成几位乱码，看看你的规则能不能把它们都拦下来，并且说清楚到底哪里不对。",
    "posttest": "最后用新情境检验一下。这次出现了活动报名和页面被人填写乱码的情况，看看你能不能把三层分工和校验规则用上去。",
    "summary": "这节课我们弄明白了三件事。第一，页面由结构、表现、行为三部分组成，结构说清楚这是什么，表现决定长什么样，行为负责响应操作，三者分开写才改得动。第二，标记会被解析成文档树，脚本通过这棵树读写页面；一次交互要走完输入、事件、更新数据、刷新界面四步。第三，做表单要先想清楚需要哪些信息，再为每一项定下校验规则；能挡住的错误就在提交前拦住，并且要只收集真正必要的信息。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出结构、表现、行为三部分各自负责什么，并写出一次完整交互的四个步骤。第二层能力应用，动手做：为图书漂流登记页面写出三条校验规则，并说明每一条对应什么错误。第三层迁移挑战，选做：为班级设计一个真实需要的小型在线应用，先写出需求，再拆成结构、表现、行为三份清单，说明你为什么不收集某一项信息。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 结构、表现、行为三层分工", "lab-1": "实验室一 结构拼装台",
    "module-2": "概念二 事件驱动的四步链路", "lab-2": "实验室二 数据与视图同步",
    "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 登记表单与校验", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-tree { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 13px; list-style: none;
  margin: 0; padding: 0; }
.ta-tree li { padding: 4px 8px; border-radius: 7px; color: var(--text-secondary); }
.ta-tree li.root { background: var(--brand-soft); color: var(--text-strong); font-weight: 700; }
.ta-tree li.lv1 { margin-left: 16px; border-left: 2px solid var(--line-subtle); }
.ta-tree li.lv2 { margin-left: 34px; border-left: 2px solid var(--line-subtle); }
.ta-tree li.empty { color: var(--muted); }
.ta-log { list-style: none; margin: 10px 0 0; padding: 0; font-size: 13.5px; }
.ta-log li { padding: 7px 10px; border-radius: 8px; margin-bottom: 6px;
  border-left: 3px solid var(--line-subtle); background: var(--bg-subtle); color: var(--text-secondary); }
.ta-log li.ok { border-left-color: var(--brand-2); color: var(--text-strong); }
.ta-log li.bad { border-left-color: var(--danger); color: var(--text-strong); background: rgba(239, 68, 68, .07); }
.ta-log li.now { border-left-color: var(--brand); color: var(--text-strong); background: var(--brand-soft); }
.ta-pick { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 6px; }
.ta-pick .choice { flex: 1 1 46%; font-size: 14px; padding: 11px 12px; }
.ta-view { border: 1px solid var(--line-subtle); border-radius: 12px; background: var(--card); padding: 14px; }
.ta-view h4 { font-size: 16px; font-weight: 800; margin: 0 0 6px; color: var(--text-strong); }
.ta-view p { margin: 0 0 8px; font-size: 14px; color: var(--text-secondary); }
.ta-view ul { margin: 0 0 8px; padding-left: 20px; font-size: 14px; color: var(--text-secondary); }
.ta-view .fake-input { display: inline-block; min-width: 120px; padding: 7px 10px; border-radius: 8px;
  border: 1px dashed var(--line); color: var(--muted); font-size: 13px; }
.ta-view .fake-form { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
.ta-view .fake-btn { display: inline-block; padding: 7px 14px; border-radius: 8px; font-size: 13px;
  font-weight: 700; background: var(--brand); color: #fff; }
.ta-view .item-row { display: flex; align-items: center; gap: 8px; padding: 6px 8px; margin-bottom: 5px;
  border-radius: 8px; background: var(--bg-subtle); font-size: 14px; }
.ta-view .item-row .no { width: 20px; height: 20px; border-radius: 50%; display: grid; place-items: center;
  background: var(--brand-2); color: #fff; font-size: 11px; font-weight: 800; flex-shrink: 0; }
.ta-field { margin-bottom: 10px; }
.ta-field label { display: block; font-size: 13px; font-weight: 700; margin-bottom: 4px; }
.ta-field input { padding: 10px 12px; font-size: 14px; }
.ta-field .req { color: var(--danger); }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-web-development 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 结构拼装台：结构卡片 → 文档树 → 实时预览
   3) 事件驱动链路：输入 → 事件 → 数据 → 视图（含不同步演示）
   4) 登记表单与校验规则
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

  /* ---------- 2. 结构拼装台 ---------- */
  var CARDS = [
    { id: 'title', label: '标题卡片', kind: 'title', role: '标题', text: '班级图书漂流登记', parent: null },
    { id: 'intro', label: '段落卡片', kind: 'text', role: '段落', text: '请填写书名与借出日期后提交。', parent: null },
    { id: 'list', label: '列表容器卡片', kind: 'list', role: '列表', text: '已登记书目', parent: null },
    { id: 'item1', label: '列表项卡片', kind: 'item', role: '列表项', text: '《十万个为什么》', parent: 'list' },
    { id: 'item2', label: '列表项卡片', kind: 'item', role: '列表项', text: '《海底两万里》', parent: 'list' },
    { id: 'form', label: '表单容器卡片', kind: 'form', role: '表单', text: '', parent: null },
    { id: 'input', label: '输入框卡片', kind: 'input', role: '输入框', text: '书名', parent: 'form' },
    { id: 'button', label: '按钮卡片', kind: 'button', role: '按钮', text: '提交', parent: 'form' }
  ];
  var l1 = document.getElementById('lab1-stage');

  if (l1) {
    var chosen = [];
    var ePool = document.getElementById('l1-pool');
    var eTree = document.getElementById('l1-tree');
    var eView = document.getElementById('l1-view');
    var eOut1 = document.getElementById('l1-out');
    var eNodes = document.getElementById('l1-nodes');
    var eDepth = document.getElementById('l1-depth');

    function card(id) { return CARDS.filter(function (c) { return c.id === id; })[0]; }

    function pool() {
      ePool.innerHTML = '';
      CARDS.forEach(function (c) {
        if (chosen.indexOf(c.id) >= 0) return;
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.cssText = 'text-align:left;font-size:14px;padding:10px 12px';
        b.textContent = c.label;
        b.addEventListener('click', function () { add(c); });
        ePool.appendChild(b);
      });
      if (ePool.children.length === 0) {
        var tip = document.createElement('p');
        tip.style.cssText = 'color:var(--muted);margin:0;font-size:14px';
        tip.textContent = '卡片都用完了。看看右边的文档树层级，再想想每一项为什么放在那里。';
        ePool.appendChild(tip);
      }
    }

    function add(c) {
      if (c.parent && chosen.indexOf(c.parent) < 0) {
        eOut1.className = 'result error';
        eOut1.innerHTML = '<strong>放不进去：</strong>「' + c.label + '」是容器里的子节点，' +
          '文档树里现在还没有它的父节点「' + card(c.parent).label + '」。<strong>错因提醒：</strong>' +
          '很多同学误认为每一项都是平铺的，其实文档树是分层的——子节点必须先有父节点，才挂得上去。';
        return;
      }
      chosen.push(c.id);
      eOut1.className = 'result';
      eOut1.innerHTML = '<strong>已加入：</strong>' + c.role + '「' + c.text + '」。' +
        (c.parent ? '它是' + card(c.parent).role + '的子节点。' : '它是根节点下的一项。');
      render1();
    }

    function remove(id) {
      chosen = chosen.filter(function (x) { return x !== id; });
      if (id === 'list') chosen = chosen.filter(function (x) { return !card(x).parent || card(x).parent !== 'list'; });
      if (id === 'form') chosen = chosen.filter(function (x) { return !card(x).parent || card(x).parent !== 'form'; });
      render1();
    }

    function render1() {
      eTree.innerHTML = '';
      var root = document.createElement('li');
      root.className = 'root';
      root.textContent = '文档（根节点）';
      eTree.appendChild(root);

      var depth = 0;
      chosen.forEach(function (id) {
        var c = card(id);
        var li = document.createElement('li');
        li.className = c.parent ? 'lv2' : 'lv1';
        li.style.display = 'flex';
        li.style.alignItems = 'center';
        li.style.gap = '8px';
        li.innerHTML = '<span>' + c.role + '：' + (c.text || '（容器）') + '</span>';
        var del = document.createElement('button');
        del.className = 'toolbar-btn';
        del.style.cssText = 'margin-left:auto;width:26px;height:26px;font-size:13px';
        del.textContent = '×';
        del.title = '移除';
        del.addEventListener('click', function () { remove(id); });
        li.appendChild(del);
        eTree.appendChild(li);
        depth = Math.max(depth, c.parent ? 2 : 1);
      });
      if (chosen.length === 0) {
        var e = document.createElement('li');
        e.className = 'empty';
        e.textContent = '（空）从这里开始：先点一张卡片。';
        eTree.appendChild(e);
      }

      eNodes.textContent = (chosen.length + 1) + ' 个';
      eDepth.textContent = chosen.length === 0 ? '—' : (depth + 1) + ' 层';

      renderPreview();
      pool();
    }

    function renderPreview() {
      var html = '';
      var i = 0;
      while (i < chosen.length) {
        var c = card(chosen[i]);
        if (c.kind === 'list') {
          var items = [], j = i + 1;
          while (j < chosen.length && card(chosen[j]).kind === 'item') { items.push(card(chosen[j]).text); j += 1; }
          html += '<p><strong>' + c.text + '</strong></p><ul>' +
            items.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>';
          i = j; continue;
        }
        if (c.kind === 'form') {
          var inner = [], k = i + 1;
          while (k < chosen.length && (card(chosen[k]).kind === 'input' || card(chosen[k]).kind === 'button')) {
            inner.push(card(chosen[k])); k += 1;
          }
          html += '<div class="fake-form">' + inner.map(function (x) {
            return x.kind === 'input'
              ? '<span class="fake-input">' + x.text + '</span>'
              : '<span class="fake-btn">' + x.text + '</span>';
          }).join('') + '</div>';
          i = k; continue;
        }
        if (c.kind === 'title') html += '<h4>' + c.text + '</h4>';
        else if (c.kind === 'text') html += '<p>' + c.text + '</p>';
        else if (c.kind === 'item') html += '<ul><li>' + c.text + '</li></ul>';
        i += 1;
      }
      eView.innerHTML = html || '<p style="color:var(--muted);margin:0">预览区还是空的。</p>';
    }

    pool();
    eOut1.className = 'result warn';
    eOut1.textContent = '先点「列表容器卡片」和「表单容器卡片」，再往里面放子节点。';
    render1();
  }

  /* ---------- 3. 事件驱动的四步链路 ---------- */
  var l2 = document.getElementById('lab2-stage');

  if (l2) {
    var data = [];
    var eInput = document.getElementById('l2-input');
    var eAdd = document.getElementById('l2-add');
    var eClear = document.getElementById('l2-clear');
    var eRefresh = document.getElementById('l2-refresh');
    var eLog2 = document.getElementById('l2-log');
    var eList = document.getElementById('l2-list');
    var eDataN = document.getElementById('l2-data-n');
    var eViewN = document.getElementById('l2-view-n');
    var eNodeN = document.getElementById('l2-node-n');

    function log2(cls, text) {
      var li = document.createElement('li');
      li.className = cls;
      li.innerHTML = text;
      eLog2.appendChild(li);
      while (eLog2.children.length > 8) eLog2.removeChild(eLog2.firstChild);
    }

    function paint() {
      eList.innerHTML = '';
      data.forEach(function (d, k) {
        var row = document.createElement('div');
        row.className = 'item-row';
        row.innerHTML = '<span class="no">' + (k + 1) + '</span><span>' + d.text + '</span>';
        eList.appendChild(row);
      });
      if (data.length === 0) {
        eList.innerHTML = '<p style="color:var(--muted);margin:0;font-size:14px">还没有登记内容。</p>';
      }
      eViewN.textContent = data.length + ' 条';
      eNodeN.textContent = (2 + data.length * 2) + ' 个';
    }

    eAdd.addEventListener('click', function () {
      var t = (eInput.value || '').trim();
      if (!t) {
        log2('bad', '<strong>第一步就断了：</strong>输入框是空的。空内容不应该进入数据，否则后面每一条都要处理这个空值。');
        return;
      }
      log2('now', '<strong>第 1 步 · 用户输入：</strong>拿到内容「' + t + '」。');
      log2('now', '<strong>第 2 步 · 事件触发：</strong>按钮上的点击处理被调用，处理过程开始执行。');
      data.push({ text: t });
      eDataN.textContent = data.length + ' 条';
      log2('ok', '<strong>第 3 步 · 更新数据：</strong>数据条数从 ' + (data.length - 1) + ' 变成 ' + data.length + ' 条。');

      if (eRefresh.checked) {
        paint();
        log2('ok', '<strong>第 4 步 · 刷新界面：</strong>按照新的数据重新渲染，界面条数与数据条数一致。');
      } else {
        log2('bad', '<strong>第 4 步被跳过了：</strong>刷新开关是关着的。数据已经变了，但界面没有跟着变——这正是前端最常见的一类问题。');
      }
      eInput.value = '';
    });

    eClear.addEventListener('click', function () {
      data = [];
      eLog2.innerHTML = '';
      eDataN.textContent = '0 条';
      paint();
      log2('ok', '<strong>已清空：</strong>数据和界面同时回到初始状态，两边保持一致。');
    });

    eRefresh.addEventListener('change', function () {
      if (eRefresh.checked) {
        paint();
        log2('ok', '<strong>重新打开刷新：</strong>界面按当前数据重新渲染了一次。注意——刚才界面少掉的那一条，现在又出现了，因为数据一直都在。');
      }
    });

    eInput.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { ev.preventDefault(); eAdd.click(); }
    });

    eDataN.textContent = '0 条';
    paint();
    log2('now', '输入一条书目，点「添加一条」，看四个数字怎么同步变化。');
  }

  /* ---------- 4. 登记表单与校验规则 ---------- */
  var syn = document.getElementById('syn-stage');

  if (syn) {
    var eBook = document.getElementById('syn-book');
    var eDate = document.getElementById('syn-date');
    var eContact = document.getElementById('syn-contact');
    var eNeedContact = document.getElementById('syn-need-contact');
    var eRun = document.getElementById('syn-run');
    var eLog3 = document.getElementById('syn-log');
    var eOut = document.getElementById('syn-out');

    eNeedContact.addEventListener('change', function () {
      eContact.disabled = !eNeedContact.checked;
      eContact.style.opacity = eNeedContact.checked ? '1' : '.5';
      if (!eNeedContact.checked) eContact.value = '';
    });

    function isDate(s) {
      var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s);
      if (!m) return false;
      var y = Number(m[1]), mo = Number(m[2]), d = Number(m[3]);
      if (mo < 1 || mo > 12 || d < 1 || d > 31) return false;
      var dt = new Date(y, mo - 1, d);
      return dt.getFullYear() === y && dt.getMonth() === mo - 1 && dt.getDate() === d;
    }

    eRun.addEventListener('click', function () {
      var book = (eBook.value || '').trim();
      var date = (eDate.value || '').trim();
      var contact = (eContact.value || '').trim();
      var errs = [];

      if (book === '') errs.push({ f: '书名', m: '这一项是必填的，空着提交没有意义。' });
      if (date === '') errs.push({ f: '借出日期', m: '这一项是必填的，没写日期就无法知道什么时候借出去的。' });
      else if (!isDate(date)) errs.push({ f: '借出日期', m: '格式应该是四位年份-两位月份-两位日期，而且要是一个真实存在的日期。你填的是「' + date + '」。' });
      if (contact !== '' && !/^\d{11}$/.test(contact)) errs.push({ f: '联系方式', m: '既然留了这一项，就要是 11 位数字；你填的是 ' + contact.length + ' 位字符，长度或内容对不上。' });

      eLog3.innerHTML = '';
      errs.forEach(function (e) {
        var li = document.createElement('li');
        li.className = 'bad';
        li.innerHTML = '<strong>' + e.f + '：</strong>' + e.m;
        eLog3.appendChild(li);
      });

      if (errs.length > 0) {
        var okLi = document.createElement('li');
        okLi.className = 'now';
        okLi.innerHTML = '<strong>校验结果：</strong>提交被拦下了，一共 ' + errs.length +
          ' 处问题。检查规则的作用，就是在数据进入系统之前先把不合格的挡在外面。';
        eLog3.appendChild(okLi);
        eOut.className = 'result error';
        eOut.innerHTML = '<strong>没有提交。</strong>请按上面的提示改好再来。注意：前端校验是为了让用户更快得到反馈，但服务端仍然必须再校验一次——因为前端是可以被绕过的。';
        return;
      }

      var pass = document.createElement('li');
      pass.className = 'ok';
      pass.innerHTML = '<strong>校验通过：</strong>书名「' + book + '」，借出日期 ' + date +
        (contact ? '，联系方式已填写 11 位' : '，未收集联系方式');
      eLog3.appendChild(pass);
      eOut.className = 'result';
      eOut.innerHTML = '<strong>登记成功。</strong>本次只收集了 ' + (contact ? '3' : '2') +
        ' 项信息。没有被要求填身份证号、住址这些与登记无关的内容——<strong>只收集必要的、够用就好</strong>，这是设计任何在线应用都该守住的一条底线。';
    });

    eContact.disabled = true;
    eContact.style.opacity = '.5';
    var welcome = document.createElement('li');
    welcome.className = 'now';
    welcome.innerHTML = '填写上面的内容，点「提交登记」看校验规则如何逐条给出针对性提示。';
    eLog3.appendChild(welcome);
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：一个页面是由什么组成的？", TTS["pretest"], [
        {"q": "下面哪一组的说法是正确的？",
         "options": [("结构描述内容是什么，表现控制外观，行为响应操作", True),
                     ("结构、表现、行为只是三种叫法，实际是一回事", False),
                     ("只要外观做得好看，结构和行为都不重要", False)],
         "explain": "三者分工不同：结构说明这一段是什么，表现决定它长什么样，行为负责响应操作。<strong>错因提醒：</strong>把三者混在一起，是这一课最常见的错误，也是后面改一处坏一处的根源。"},
        {"q": "把一篇文章的所有字都放大加粗，最合适的做法是：",
         "options": [("改样式规则，让内容本身一个字都不动", True),
                     ("把文章里的每个字都换成更大的写法", False),
                     ("把整段删掉重新写一遍", False)],
         "explain": "外观归表现管。改样式不动内容，这就是三层分开写的好处。"},
        {"q": "点了按钮之后界面没有变化。下面哪种判断更合理？",
         "options": [("有可能数据确实变了，只是没有刷新界面", True),
                     ("一定是电脑坏了", False),
                     ("一定是因为颜色配得不好看", False)],
         "explain": "改了数据不等于界面会跟着变，这个区别先记在心里，等下做实验时你会亲眼看到数据条数和界面条数不一致。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "页面由结构、表现、行为三层分工完成", TTS["module-1"], f'''
        {LAB_CSS}
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道网页是靠网络取回来的，<strong>但真正的问题出现了</strong>：取回来的那一堆内容，凭什么能在屏幕上变成有标题、有段落、有按钮的页面？<strong>所以</strong>我们需要把你手上的一句需求（要登记书名和日期）翻译成计算机看得懂的结构，再配上外观和交互，这就是做网页这件事的全过程。</p>
        </div>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>结构</strong></p>
            <p style="color:var(--muted)">用标记描述内容：这一段是标题、是段落、是一份列表，还是一个可以填写的输入框。它不负责好不好看。</p>
          </div>
          <div class="inner-card">
            <p><strong>表现</strong></p>
            <p style="color:var(--muted)">用样式规则控制外观：颜色、字号、间距、边框。换一套规则，内容一个字都不用改。</p>
          </div>
          <div class="inner-card">
            <p><strong>行为</strong></p>
            <p style="color:var(--muted)">用脚本响应操作：监听点击与输入，读写页面里的节点，把结果反馈给用户。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="从标记到渲染：文档被解析成文档树，再渲染成可见页面">
          <figcaption>标记被解析成文档树，文档树再渲染成你看到的页面；脚本读写的正是这棵树</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧭</span><div><strong>记忆锚点：</strong>像盖房子。结构是墙和房间（哪里是客厅、哪里是卧室），表现是装修（颜色、灯光、地板），行为是电路和开关（按一下灯就亮）。房间没改，换一套装修完全不影响结构。</div></div>
{insight_box([
    {"lens": "拆开它", "text": "任何一个页面都能拆成这份清单：有哪些内容块（结构）、它们长什么样（表现）、能做什么操作（行为）。先列清单，再动手写。"},
    {"lens": "比较它", "text": "三层混在一起写，改颜色可能改坏结构；三层分开写，改外观不碰内容，内容还能被朗读软件正确读出来。"},
    {"lens": "迁移它", "text": "做幻灯片、排一份通知也是这样：先定内容层级，再定样式。先想清楚「这是什么」，再想「它长什么样」。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "结构拼装台：点一张卡片，长出一个节点", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">左边点卡片，右边的文档树会跟着长，下面的预览区会立刻渲染出对应的样子。注意容器和子节点的先后顺序。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <p style="margin:0 0 8px"><strong>结构卡片池</strong></p>
              <div class="ta-pick" id="l1-pool"></div>
            </div>
            <div>
              <p style="margin:0 0 8px"><strong>文档树（实时）</strong></p>
              <ul class="ta-tree" id="l1-tree"></ul>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">文档树节点数</span><span class="v green" id="l1-nodes">1 个</span></div>
            <div class="readout-cell"><span class="k">树的层数</span><span class="v" id="l1-depth">—</span></div>
          </div>
          <p style="margin:14px 0 8px"><strong>预览区（按当前结构渲染）</strong></p>
          <div id="lab1-stage"><div class="ta-view" id="l1-view"></div></div>
          <p class="result warn" id="l1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌲</span><div><strong>想一想：</strong>为什么列表项加不进去？因为文档树是分层的，子节点要先有父节点。试着先把「列表容器卡片」放进去，再点列表项看看。</div></div>
    ''', tag="制作实验室", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "一次交互要走完四步：输入、事件、更新数据、刷新界面", TTS["module-2"], f'''
        {LAB_CSS}
        <p style="font-size:17px;margin:0 0 12px">脚本通过<strong>文档树</strong>读写页面。你点一下按钮，屏幕上的变化背后其实走了四步。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>用户输入：</strong>在输入框里填内容，或者完成一次点击。</div></div>
          <div class="step"><span class="n">2</span><div><strong>事件触发：</strong>绑定在这个元素上的处理过程被调用，程序开始执行。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>更新数据：</strong>把新的内容写进数据里——数据才是这一屏真正的依据。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>刷新界面：</strong>按照新的数据重新渲染一次，用户才看得到变化。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="事件驱动的四步链路：用户输入、事件触发、更新数据、刷新界面并回到第一步">
          <figcaption>四步循环：用户输入 → 事件触发 → 更新数据 → 刷新界面，然后回到第一步等待下一次输入</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个最容易搞混的地方。第一，误认为改了数据界面就会自动变——不会，必须有人明确地刷新它。第二，反过来在界面上直接做手脚而不改数据——看起来对了，但下一次刷新时这点改动就消失了。判断标准很简单：<strong>数据变了，界面必须跟着变；界面变了，数据也必须跟着变。</strong></p>
        </div>
        <div class="inner-card">
          <p><strong>顺带说一件重要的事：</strong>数据是先到你的浏览器、再发到服务器去的，所以用户能改到的东西都不算数。前端校验是为了让人更快看到提示，<strong>真正说了算的校验必须放在服务端</strong>再做一遍。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "数据与视图：四个数字应该同时变化", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">添加几条书目，盯住四个数字。然后把「刷新界面」开关关掉再加一条，看看会发生什么。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <p style="margin:0 0 8px"><strong>输入与操作</strong></p>
              <div class="ta-field">
                <label for="l2-input">书名</label>
                <input id="l2-input" type="text" placeholder="例如：《昆虫记》">
              </div>
              <div class="ta-pick" id="lab2-stage">
                <button class="choice" id="l2-add" style="text-align:center">添加一条</button>
                <button class="choice" id="l2-clear" style="text-align:center">全部清空</button>
              </div>
              <label style="display:flex;align-items:center;gap:8px;margin-top:12px;font-size:14px">
                <input type="checkbox" id="l2-refresh" checked style="width:auto;min-height:auto">
                添加后刷新界面
              </label>
            </div>
            <div>
              <p style="margin:0 0 8px"><strong>当前界面（按数据渲染）</strong></p>
              <div class="ta-view" id="l2-list"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">数据条数</span><span class="v" id="l2-data-n">0 条</span></div>
            <div class="readout-cell"><span class="k">界面条数</span><span class="v green" id="l2-view-n">0 条</span></div>
            <div class="readout-cell"><span class="k">列表节点数</span><span class="v" id="l2-node-n">2 个</span></div>
          </div>
          <ul class="ta-log" id="l2-log"></ul>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>关键对比：</strong>关掉刷新之后，数据条数照样加一，界面条数却停住了。再把开关打开，那条内容立刻出现——说明数据一直都在，只是没有人让界面重新渲染。</div></div>
    ''', tag="制作实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：点了提交没反应，问题出在哪一步", TTS["worked-example"], f'''
        {LAB_CSS}
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(245,158,11,.55)">
          <p style="margin:0"><strong>题目：</strong>一个登记页面，点「提交」之后界面毫无变化。作者说样式写得没问题。请按四步链路定位问题，并说明你的排查顺序。</p>
        </div>
        <div class="inner-card">
          <p style="margin:0 0 6px"><strong>第一步　看清现象：</strong>点击有反应，说明事件没有被完全丢掉；界面不变，说明第四步没有发生。</p>
          <p style="margin:0 0 6px"><strong>第二步　查第二步（事件）：</strong>确认处理过程确实绑在了按钮上，并且被调用了。</p>
          <p style="margin:0 0 6px"><strong>第三步　查第三步（更新数据）：</strong>在处理过程里打印数据，发现条数根本没变——原因是在中途访问了一个并不存在的节点，执行到那里就停住了。</p>
          <p style="margin:0"><strong>第四步　修复并自查：</strong>先确认要操作的节点在文档树里真的存在，再更新数据，最后刷新界面。顺序不能颠倒：数据没更新就刷新，刷出来的还是旧内容。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">最常见的错误判断是「界面不变，那一定是外观的问题」，然后一头扎进颜色和字号里找，越找越远。另一个常见错误是把顺序做反：先刷新界面再更新数据，结果每次看到的都是上一次的内容。记住这条排查顺序：<strong>事件接上了吗 → 数据变了吗 → 界面刷新了吗</strong>，从前往后查，一步都不会漏。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("只要数据更新了，就需要有人明确地刷新界面，用户才能看到变化", True),
                     ("数据一改，界面一定会自动跟着变", False),
                     ("只要界面看起来对了，数据对不对无所谓", False)],
         "explain": "数据是依据，界面是它的呈现，两者之间需要一次明确的刷新。<strong>错因提醒：</strong>把「数据变了」和「界面变了」搞混，是这一课最高频的常见错误，排查时一定要分开看。"},
        {"q": "有人把页面上的字直接改掉，让统计看起来是对的，但数据里没有变化。最可能发生的是：",
         "options": [("下一次刷新时，这点改动会消失，界面回到数据的真实样子", True),
                     ("数据也跟着变了，一切正常", False),
                     ("页面会永久记住这个改动", False)],
         "explain": "界面是按数据渲染出来的。绕过数据改界面，等于在沙滩上写字。<strong>错因提醒：</strong>误认为「看起来对就是对的」，是初学者很容易踩的坑。"},
        {"q": "一个报名页面只在提交前做了校验。有人说这样已经很安全了，因为填错就提交不了。这个说法：",
         "options": [("不准确，前端校验可以被绕过，服务端必须再校验一次", True),
                     ("完全正确", False),
                     ("只要校验规则写得足够多就完全正确", False)],
         "explain": "前端校验的价值是让人更快得到反馈；但数据最终要交到服务器上，那里必须再检查一遍。<strong>错因提醒：</strong>误认为「界面上挡住了就等于挡住了」，是安全设计上最典型的错误判断。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给登记页面定下校验规则", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">需求：登记书名、借出日期，联系方式可填可不填。请先定下规则，再故意填错几次，看看你的规则能不能都拦住。</p>
        <div class="lab-panel">
          <div id="syn-stage">
            <div class="ta-field">
              <label for="syn-book">书名 <span class="req">（必填）</span></label>
              <input id="syn-book" type="text" placeholder="例如：《十万个为什么》">
            </div>
            <div class="ta-field">
              <label for="syn-date">借出日期 <span class="req">（必填）</span></label>
              <input id="syn-date" type="text" placeholder="例如：2026-09-20">
            </div>
            <label style="display:flex;align-items:center;gap:8px;margin:6px 0 10px;font-size:14px">
              <input type="checkbox" id="syn-need-contact" style="width:auto;min-height:auto">
              顺便留下联系方式（选填，不留也可以）
            </label>
            <div class="ta-field">
              <label for="syn-contact">联系方式</label>
              <input id="syn-contact" type="text" placeholder="11 位数字">
            </div>
          </div>
          <div class="ta-pick">
            <button class="choice" id="syn-run" style="text-align:center">提交登记</button>
          </div>
          <ul class="ta-log" id="syn-log"></ul>
          <p class="result" id="syn-out" style="margin-top:12px"></p>
        </div>
        <div class="inner-card">
          <p><strong>写下来，说给同桌听：</strong>你定了几条规则？每条规则拦住的是哪一类错误？为什么联系方式要设计成选填，而不是必填？</p>
          <textarea id="syn-answer" rows="3" placeholder="我一共定了……条规则：第一条……第二条……因为……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "一个活动报名页面，同学们反映「填了看不到自己报上名没有」。最该补上的是：",
         "options": [("提交之后按新数据显示一份报名成功的回执，让用户看到反馈", True),
                     ("把按钮做得更大更显眼", False),
                     ("把页面背景换成更亮的颜色", False)],
         "explain": "用户需要看到自己操作的结果，这属于行为这一层的职责。按钮大小和背景颜色是表现层的事，解决不了「没有反馈」这个问题。"},
        {"q": "有人把别人的作文整段复制到自己的班级主页上，还删掉了原作者的名字。下面评价正确的是：",
         "options": [("使用他人内容应当注明来源，删掉署名是不对的", True),
                     ("网上能搜到的东西就可以随意使用", False),
                     ("只要把文字换成不一样的字体就不算复制", False)],
         "explain": "做在线应用不只是技术问题，还要守住责任：注明来源、尊重他人成果，这是数字公民的基本要求。"},
        {"q": "同学设计的登记页面要求填写身份证号和家庭住址。最合理的改进建议是：",
         "options": [("这两项与图书漂流登记无关，应当去掉，只收集必要的信息", True),
                     ("字段越多越完整，应该再加几项", False),
                     ("把字段保留但改成不必填", False)],
         "explain": "能说明「为什么需要它」，才值得收集。与目的无关的信息，多收集一项就多一份泄露风险。<strong>错因提醒：</strong>误认为「字段越多越专业」，是设计在线应用时常见的一种错误观念。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>三层分工</strong>：结构用标记描述内容是什么，表现用样式控制外观，行为用脚本响应操作；分开写才改得动。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>四步链路</strong>：用户输入 → 事件触发 → 更新数据 → 刷新界面；数据变了界面才跟着变，两边必须一致。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>表单与责任</strong>：先想清楚需要哪些信息，再为每一项定下校验规则；前面拦住是为了体验，服务端再校验才是安全，只收集必要的信息。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(245,158,11,.55)">
          <p style="margin:0"><strong>回到开头那张纸：</strong>把纸质登记变成在线应用，改的不只是一张脸的样式。结构上要列出书名、日期、联系方式这几个内容块；表现上让它们排得清楚好填；行为上接住每一次提交、逐条校验、给出反馈。三块都做到位，这张纸才算真正搬到了网上。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「结构、表现、行为、刷新」这四个词，说清楚点一次提交之后，从你按下按钮到看到结果经历了什么。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出结构、表现、行为各自负责什么，并各举一个页面上的例子。",
            "写出一次完整交互的四个步骤，并说明哪一步跳过了会导致「界面没有变化」。",
            "画出一段结构对应的文档树，标出哪些节点是父子关系。",
        ],
        [
            "为图书漂流登记页面写出三条校验规则，说明每一条拦住的是哪一类错误输入。",
            "打开实验室二，关掉刷新开关连续添加两条内容，记录「数据条数」和「界面条数」的差值，并解释这个差值说明什么。",
            "为你自己的登记页面设计三个内容块，分别写出它们的结构、表现、行为各是什么。",
        ],
        [
            "为班级设计一个真实需要的小型在线应用，先写清需求，再拆成结构、表现、行为三份清单。",
            "检查一个你用过的在线表单，找出它收集了哪些信息，判断有没有与用途无关的项目，并写一段改进建议；同时说明你会怎样保护自己填写过的个人信息。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-web-development",
    "node_id": "it-m-web-development",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "网页与在线应用制作",
    "name_en": "Building Web Pages and Online Applications",
    "grade": 7,
    "grade_cn": "七年级",
    "domain": "internet-innovation",
    "domain_cn": "互联网应用与创新",
    "lesson_type": "design-implementation",
    "version": "1.0.0",
    "description": "从一个真实的班级登记需求出发，理解网页由结构、表现、行为三层分工完成，掌握标记到文档树再到渲染的过程，能描述一次交互的四步链路并保证数据与视图一致，能为真实需求设计表单与校验规则并守住只收集必要信息的底线。",
    "tags": ["网页制作", "结构表现行为", "文档树", "事件驱动", "表单校验", "信息安全责任"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「互联网应用与创新」——运用工具制作简单网页或在线应用，服务真实需求；在使用中遵守信息社会的法律与伦理规范。",
    "hero_question": "一句「做一个登记页面」的需求，怎样变成能填、能交、能立刻看到结果的在线应用？",
    "hero_alt": "网页制作知识结构图：结构、表现、行为三栏",
    "hero_caption": "结构描述内容 · 表现控制外观 · 行为响应操作：三层分开写，四步链路跑通一次交互",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "一个页面到底由哪几部分组成？", "d": "为什么结构、外观、操作要分开写", "v": "一个页面到底由哪几部分组成"},
        {"t": "点了按钮之后究竟发生了什么？", "d": "从按下到看到结果中间有几步", "v": "点了按钮之后究竟发生了什么"},
        {"t": "为什么填错了会被拦住？", "d": "那些规则是怎么写出来的", "v": "为什么填错了会被拦住"},
        {"t": "怎样做一个真正能用的登记页面？", "d": "从需求到能提交要经过哪些事", "v": "怎样做一个真正能用的登记页面"},
    ],
    "objectives": [
        "能说出网页由结构、表现、行为三部分组成，并说明三者分工不同的好处",
        "能用标记描述内容结构，说出文档树是怎么形成的，并知道脚本读写的就是这棵树",
        "能描述一次交互的完整链路：用户输入、事件触发、更新数据、刷新界面，并能定位其中断掉的一步",
        "能为真实需求设计表单与校验规则，并说明为什么只应收集必要的信息",
    ],
    "objectives_plain": [
        "能说出网页由结构、表现、行为三部分组成，并说明三者分工不同的好处",
        "能用标记描述内容结构，说出文档树是怎么形成的，并知道脚本读写的就是这棵树",
        "能描述一次交互的完整链路：用户输入、事件触发、更新数据、刷新界面，并能定位其中断掉的一步",
        "能为真实需求设计表单与校验规则，并说明为什么只应收集必要的信息",
    ],
    "standards": [
        {"content": "运用工具制作简单网页或在线应用，服务真实需求。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》互联网应用与创新 · 初中"},
        {"content": "在使用在线应用的过程中遵守法律法规与伦理规范，保护个人信息，尊重他人成果。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》互联网应用与创新 · 初中"},
    ],
    "prereqs": ["it-m-internet-architecture"],
    "prereqs_name": "互联网结构与协议初识",
    "prereqs_meta": "it-m-internet-architecture",
    "leads_to": ["it-m-cloud-collaboration"],
    "next_meta": "it-m-cloud-collaboration",
    "section_images": ["assets/it-m-web-development-fig1.webp", "assets/it-m-web-development-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一句「做个登记页面」的需求，怎样变成能填能交的在线应用？带着这个问题开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己把一份需求拆成结构、表现、行为三份清单。",
        "objectives": "看清四件事：说出三层分工、说出文档树的来历、描述四步交互链路、为需求设计校验规则。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "结构说这是什么，表现决定长什么样，行为负责响应操作；三层分开写，改一处不碰另两处。",
        "lab-1": "先放容器卡片，再放子节点卡片。盯住文档树节点数和树的层数怎么变。",
        "module-2": "输入 → 事件 → 更新数据 → 刷新界面。数据变了界面才跟着变，两边必须一致。",
        "lab-2": "关掉刷新开关再加一条，比较数据条数和界面条数——不一致的地方就是问题所在。",
        "worked-example": "按「事件接上了吗 → 数据变了吗 → 界面刷新了吗」的顺序查，一步都不会漏。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "故意把书名为空、日期写成不存在的日期、联系方式填成乱码，看你的规则能不能都拦住。",
        "posttest": "换了活动报名和内容署名的场景，看看你还能不能用上三层分工与责任意识。",
        "summary": "用「结构、表现、行为、刷新」四个词，把一次提交的完整过程讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「互联网应用与创新」领域长期空缺的制作类一课。设计上不引入任何具体开发工具与产品名称，只用通用的结构、表现、行为三层概念，把力气花在三件可观察的事上：用结构拼装台把「标记 → 文档树 → 渲染」变成看得见的节点数与层级，用数据与视图同步器把「数据条数」与「界面条数」做成两个可以故意不一致的数字，用登记表单把校验规则做成逐条给出的针对性提示。价值取向上，全课以班级真实需求驱动，并在概念二与综合任务两处收束到「前端校验可被绕过、服务端必须再校验」与「只收集必要信息」这两条责任底线。",
    "plan_table": """| 1 | cover | 网页与在线应用制作 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：一个页面是由什么组成的？ | 起·前测（暴露直觉） |
| 5 | concept | 页面由结构、表现、行为三层分工完成 | 承·概念一 |
| 6 | interactive | 结构拼装台：点一张卡片，长出一个节点 | 承·实验室一（节点数与层级可观察） |
| 7 | concept | 一次交互要走完四步：输入、事件、更新数据、刷新界面 | 承·概念二 |
| 8 | interactive | 数据与视图：四个数字应该同时变化 | 承·实验室二（数据与界面可对比） |
| 9 | concept | 例题示范：点了提交没反应，问题出在哪一步 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给登记页面定下校验规则 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：结构 / 表现 / 行为三栏标注\n- P5 从标记到渲染示意图（已生成）：文档 → 文档树 → 渲染出的页面\n- P7 事件驱动四步链路图（已生成）：用户输入 → 事件触发 → 更新数据 → 刷新界面\n- 若需补充：纸质登记表与在线登记页的对比照片（用于情境引入，需去除任何产品标识）",
}
