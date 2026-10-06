# -*- coding: utf-8 -*-
"""初中信息科技 · 云存储与在线协作（G7）—— 补齐课标「互联网应用与创新」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-m-cloud-collaboration-fig1.webp'
F2 = './assets/it-m-cloud-collaboration-fig2.webp'

TTS = {
    "hero": "先看一个真实场景。小组四个人要交一份实验报告，说好各自把自己那部分写进去。结果第二天打开文件一看，昨天写好的两段不见了，只剩下最后一版。文件明明没删，内容却少了——问题出在哪？其实这不是文件坏了，而是我们对「云存储」和「在线协作」的工作方式理解得还不够。这节课，我们把它弄明白，并学会规范地管理自己的数字作品。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道文件放到云端之后到底存在哪里，还是想知道几个人同时改一份文件为什么不会乱，又或者你更想知道怎样把文件名、版本和权限管理得清清楚楚。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说清楚云存储的基本原理，分清上传、下载和同步三件事。第二，能说明在线协作依靠什么机制让多人同时编辑一份文件。第三，能根据任务需要设置合适的分享范围与权限，并说出其中的安全风险。第四，能用自己的话讲出一套数字作品管理的规范，并照着规范整理文件。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "云存储，是把文件保存到网络上去，而不是只保存在自己这台设备里。它有三个关键点。第一是账号，账号决定了你是谁，也决定了你能看到哪些文件。第二是云端副本，网络上那份文件才是大家公认的版本。第三是同步，设备把本地的改动传上去，再把云端的改动取下来，两边保持一致。这里要分清三个动作：上传，是把本地的东西送到云端；下载，是把云端的东西取回本地；同步，是自动做这两件事，让两边尽量一样。",
    "lab-1": "我们来模拟一次真实的协作事故。左边是本地副本，右边是云端副本，两个版本号会随着操作变化。你可以自己改一处，也可以让同伴在云端改一处，然后选择上传或者下载。请注意观察：当云端已经有了别人的新版本，而你还按老版本上传，会发生什么。",
    "module-2": "在线协作，是几个人同时编辑同一份文件。它靠两样东西维持秩序：一是自动同步和版本记录，每一次保存都会留下一条历史，出问题可以回头看；二是权限设置，决定谁能看、谁只能评论、谁可以改。分享的时候要同时想两件事：给多大的权限，以及分享给多大的范围。范围一旦选成「拿到链接的人」，链接被转发出去，范围之外的人也能看到。",
    "lab-2": "现在你来当一次权限管理员。先选一个权限档位，再选一个分享范围，然后看看查看、评论、编辑、转发这几件事分别会发生什么。选完之后读一读下面的风险提示，想一想：给小组内部共享的一份草稿，用什么样的设置才既方便又安全。",
    "worked-example": "我们一起分析那起协作事故。第一步，看清现象：昨天晚上写好的两段不见了。第二步，找出原因：两个人在各自的设备上各改了一版，甲先上传，乙手里还是旧版本，乙一上传，就把甲那一版覆盖掉了。第三步，判断性质：这不是文件损坏，是版本覆盖。第四步，给出对策：动手改之前先同步一次，看到版本冲突的提示不要直接覆盖，而是先比较两版内容，或者干脆分工到不同章节，各写各的。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你当一次数字作品管理员。屏幕上的工具会按四条规则给你的文件名打分：有没有日期，有没有版本号，有没有多余的空格或符号，主题词是否说得清楚。先输入一个你平时用的文件名试试，看看得几分，再点一下生成规范名，对比一下差别。",
    "posttest": "最后用新情境检验一下。这次出现了共享链接、回收站和同伴协作，看看你能不能把学到的原理用上去。",
    "summary": "这节课我们弄明白了三件事。第一，云存储把文件放在网络上，靠账号区分身份，靠同步让设备和云端保持一致，上传和下载是两个方向相反的动作。第二，在线协作靠自动同步和版本记录维持秩序，靠权限设置决定谁能做什么。第三，数字作品要管好，靠的是规范命名、分类归档、保留版本、定期备份，以及只给必要的人必要的权限。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出上传、下载、同步三个动作的区别，并写出查看、评论、编辑三种权限分别能做什么。第二层能力应用，动手做：把自己云盘里的一个文件夹按规范重新命名和归档，并给它设置一个合适的分享范围。第三层迁移挑战，选做：为小组合作写出一份文件管理约定，说明命名规则、版本规则和分工方式，并解释每条约定是为了防止什么问题。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 云存储原理", "lab-1": "实验室一 同步模拟器", "module-2": "概念二 协作与权限",
    "lab-2": "实验室二 权限检查器", "worked-example": "例题讲解", "conceptest-1": "概念测试",
    "synthesis": "综合任务 作品管理台", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

LAB_CSS = """
<style>
.ta-sync { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
.ta-sync-box { border: 1px solid var(--line-subtle); border-radius: 12px; padding: 12px; background: var(--bg-subtle); }
.ta-sync-box h4 { font-size: 14px; color: var(--text-secondary); margin: 0 0 8px; }
.ta-sync-box .ver { display: inline-block; font-family: ui-monospace, Menlo, monospace; font-size: 12px; font-weight: 700;
  padding: 2px 8px; border-radius: 999px; background: var(--brand-soft); color: var(--link); margin-left: 6px; }
.ta-sync-box .body { min-height: 62px; font-size: 14px; color: var(--text); background: var(--card);
  border: 1px solid var(--line-subtle); border-radius: 9px; padding: 9px 11px; }
.ta-sync-box .body.remote { border-style: dashed; }
.ta-flag { display: inline-block; margin-top: 8px; font-size: 12px; padding: 3px 9px; border-radius: 999px;
  background: var(--brand-2-soft); color: var(--accent-deep); border: 1px solid var(--line-subtle); }
.ta-flag.dirty { background: var(--warm-soft); color: var(--warm-deep); }
.ta-check { display: grid; grid-template-columns: 1fr; gap: 8px; }
.ta-check-row { display: flex; align-items: center; gap: 10px; padding: 10px 12px; border-radius: 11px;
  background: var(--bg-subtle); border: 1px solid var(--line-subtle); font-size: 14px; }
.ta-check-row .mark { flex-shrink: 0; width: 26px; height: 26px; display: grid; place-items: center;
  border-radius: 50%; font-weight: 800; font-size: 14px; }
.ta-check-row.ok .mark { background: rgba(34, 197, 94, .16); color: #15803d; }
.ta-check-row.no .mark { background: rgba(239, 68, 68, .14); color: var(--danger); }
.ta-check-row.wait .mark { background: var(--brand-soft); color: var(--link); }
</style>
"""

CUSTOM_JS = r"""
/* ============================================================
   it-m-cloud-collaboration 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 云同步模拟器：本地版本 / 云端版本 / 冲突检测
   3) 权限与分享范围检查器：四种动作 × 组合设置
   4) 数字作品管理台：文件名规范校验与重命名建议
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

  /* ---------- 2. 云同步模拟器 ---------- */
  var syncRoot = document.getElementById('lab1-sync');
  if (syncRoot) {
    var cloudVer = 1;
    var cloudText = '实验报告 · 第一段：实验目的。';
    var baseVer = 1;
    var localText = cloudText;
    var dirty = false;
    var editCount = 0;
    var OTHER = [
      '实验报告 · 第二段：实验步骤（同伴补写）。',
      '实验报告 · 第三段：数据记录（同伴补写）。',
      '实验报告 · 第四段：结论（同伴补写）。'
    ];

    var eLocalVer = document.getElementById('l1-local-ver');
    var eLocalBody = document.getElementById('l1-local-body');
    var eLocalFlag = document.getElementById('l1-local-flag');
    var eCloudVer = document.getElementById('l1-cloud-ver');
    var eCloudBody = document.getElementById('l1-cloud-body');
    var eCloudFlag = document.getElementById('l1-cloud-flag');
    var eSyncOut = document.getElementById('l1-out');

    function render(label, cls) {
      eLocalVer.textContent = 'v' + (baseVer + (dirty ? 1 : 0));
      eLocalBody.textContent = localText;
      eLocalFlag.textContent = dirty ? '有改动，还没有上传' : '与云端一致';
      eLocalFlag.className = 'ta-flag' + (dirty ? ' dirty' : '');
      eCloudVer.textContent = 'v' + cloudVer;
      eCloudBody.textContent = cloudText;
      eCloudFlag.textContent = cloudVer > baseVer ? '云端有比你更新的版本' : '线上权威版本';
      eCloudFlag.className = 'ta-flag' + (cloudVer > baseVer ? ' dirty' : '');
      eSyncOut.className = 'result ' + (cls || 'warn');
      eSyncOut.innerHTML = label;
    }

    document.getElementById('l1-edit').addEventListener('click', function () {
      localText = '实验报告 · 我补充的这一段（第 ' + (editCount + 1) + ' 次编辑）。';
      dirty = true;
      editCount = editCount + 1;
      render('<strong>你在本地改了一处。</strong>现在左边的内容只存在这台设备上，云端还不知道。如果不点「上传」，换一台设备打开就看不到这段内容。');
    });

    document.getElementById('l1-peer').addEventListener('click', function () {
      if (cloudVer - 1 < OTHER.length) {
        cloudText = OTHER[cloudVer - 1];
      } else {
        cloudText = '实验报告 · 又追加了一段（同伴补写）。';
      }
      cloudVer = cloudVer + 1;
      render('<strong>同伴在云端保存了一次。</strong>云端版本升到 v' + cloudVer +
        '。注意：你手里的是基于 v' + baseVer + ' 的副本，已经落后了。');
    });

    document.getElementById('l1-upload').addEventListener('click', function () {
      if (cloudVer > baseVer) {
        render('<strong>版本冲突！上传被拦下了。</strong>云端已经是 v' + cloudVer +
          '，你手里的是基于 v' + baseVer + ' 改出来的。如果强行上传，云端那一段会被你的旧版本整个替换掉——这就是开头报告少了两段的原因。正确的做法是先下载，把两边的改动合到一起，再上传。', 'error');
        return;
      }
      if (!dirty) {
        render('<strong>没有需要上传的改动。</strong>本地内容和云端一致，这时候上传不会有任何变化。', 'warn');
        return;
      }
      cloudVer = cloudVer + 1;
      baseVer = cloudVer;
      cloudText = localText;
      dirty = false;
      render('<strong>上传成功。</strong>你的改动成为云端的 v' + cloudVer +
        '，本地和云端重新一致。上传的方向是「本地 → 云端」。');
    });

    document.getElementById('l1-download').addEventListener('click', function () {
      if (dirty) {
        render('<strong>先别急着下载。</strong>你本地还有没上传的改动，直接下载会把它们覆盖掉。正确处理是先把两版内容放在一起比较，决定哪些留下，再合并。<strong>错因提醒：</strong>很多同学以为下载总是安全的，其实它和上传一样会覆盖数据，只是覆盖的方向相反。', 'error');
        return;
      }
      localText = cloudText;
      baseVer = cloudVer;
      dirty = false;
      render('<strong>下载完成。</strong>本地更新到 v' + cloudVer +
        '，拿到的就是云端这一版。下载的方向是「云端 → 本地」。');
    });

    document.getElementById('l1-reset').addEventListener('click', function () {
      cloudVer = 1; baseVer = 1;
      cloudText = '实验报告 · 第一段：实验目的。';
      localText = cloudText; dirty = false; editCount = 0;
      render('已重置。现在本地和云端都是 v1，内容一致。先试试「我在本地改一处」。');
    });

    render('现在本地和云端都是 v1，内容一致。先试试「我在本地改一处」。');
  }

  /* ---------- 3. 权限与分享范围检查器 ---------- */
  var permRoot = document.getElementById('lab2-perm');
  if (permRoot) {
    var PERM = {
      view: { n: '只能查看', desc: '对方可以打开阅读，但不能改动内容。' },
      comment: { n: '可以评论', desc: '对方能阅读，还能留下评论和建议，但不能直接改正文。' },
      edit: { n: '可以编辑', desc: '对方能直接修改正文，改动会进入版本记录。' }
    };
    var SCOPE = {
      named: { n: '仅指定的人', risk: 'low', desc: '只有名单里的人能打开，最稳妥。' },
      link: { n: '拿到链接的人', risk: 'mid', desc: '谁拿到链接谁就能打开，链接被转发后范围就失控了。' },
      open: { n: '完全公开', risk: 'high', desc: '所有人都能打开，任何人搜索都可能找到它。' }
    };
    var perm = 'comment', scope = 'named';
    var ePermRows = document.getElementById('l2-rows');
    var ePermOut = document.getElementById('l2-out');

    function judge(action) {
      var canView = true;
      var canComment = perm === 'comment' || perm === 'edit';
      var canEdit = perm === 'edit';
      if (action === 'view') return canView;
      if (action === 'comment') return canComment;
      if (action === 'edit') return canEdit;
      return scope !== 'named';
    }

    function render2() {
      var P = PERM[perm], S = SCOPE[scope];
      var items = [
        { a: 'view', t: '打开来读', extra: '三种权限档位都允许阅读。' },
        { a: 'comment', t: '留下评论', extra: can2('comment') },
        { a: 'edit', t: '直接修改正文', extra: can2('edit') },
        { a: 'share', t: '把链接转发给别人', extra: scope === 'named'
            ? '只有当对方本就在名单里时才有效，名单外的人打开会被拒绝。'
            : '范围是「' + S.n + '」，转发出去的链接别人能直接打开，你无法再收回。' }
      ];
      ePermRows.innerHTML = '';
      items.forEach(function (it) {
        var ok = judge(it.a);
        var row = document.createElement('div');
        row.className = 'ta-check-row ' + (ok ? 'ok' : 'no');
        row.innerHTML = '<span class="mark">' + (ok ? '✓' : '✕') + '</span>' +
          '<span><strong>' + it.t + '</strong>：' + (ok ? '允许' : '不允许') + '。<span style="color:var(--muted)">' + it.extra + '</span></span>';
        ePermRows.appendChild(row);
      });
      var riskText = S.risk === 'low'
        ? '当前设置的风险等级：较低。权限和范围都收得比较紧，适合小组内部还没完成的草稿。'
        : (S.risk === 'mid'
            ? '当前设置的风险等级：中等。链接一旦被转发，范围之外的人也能看到，别把没定稿的内容这样分享。'
            : '当前设置的风险等级：较高。完全公开意味着任何人搜到都能打开，涉及个人信息、成绩、联系方式的内容绝对不能这样分享。');
      var adv = perm === 'edit' ? '另外，' + S.n + '里所有人都能直接改正文，容易互相覆盖，建议改成「可以评论」，由一位同学统一定稿。' : '';
      ePermOut.className = 'result ' + (S.risk === 'high' ? 'error' : (S.risk === 'mid' ? 'warn' : ''));
      ePermOut.innerHTML = '<strong>当前：' + P.n + ' + ' + S.n + '。</strong>' + P.desc + S.desc +
        '<br>' + riskText + adv +
        '<br><strong>信息社会责任：</strong>分享之前先问自己两句——对方真的需要这个权限吗？这份内容里有没有别人的隐私？';
    }
    function can2(a) {
      if (a === 'comment') return '需要「可以评论」或「可以编辑」。';
      return '只有「可以编辑」才允许。';
    }

    document.querySelectorAll('[data-perm]').forEach(function (b) {
      b.addEventListener('click', function () {
        perm = b.dataset.perm;
        document.querySelectorAll('[data-perm]').forEach(function (x) { x.classList.toggle('selected', x === b); });
        render2();
      });
    });
    document.querySelectorAll('[data-scope]').forEach(function (b) {
      b.addEventListener('click', function () {
        scope = b.dataset.scope;
        document.querySelectorAll('[data-scope]').forEach(function (x) { x.classList.toggle('selected', x === b); });
        render2();
      });
    });
    document.querySelector('[data-perm="comment"]').classList.add('selected');
    document.querySelector('[data-scope="named"]').classList.add('selected');
    render2();
  }

  /* ---------- 4. 数字作品管理台 ---------- */
  var mgrRoot = document.getElementById('syn-manager');
  if (mgrRoot) {
    var eInput = document.getElementById('syn-filename');
    var eCheck = document.getElementById('syn-check');
    var eMgrRows = document.getElementById('syn-rows');
    var eName = document.getElementById('syn-suggest');
    var eMgrOut = document.getElementById('syn-out');

    var RULES = [
      { k: 'date', label: '是否写清日期', hint: '建议用 8 位数字开头，例如 20260915，一眼就知道是哪一版。' },
      { k: 'ver', label: '是否标出版本号', hint: '建议用 v1、v2 这样的版本号，改过几轮一目了然。' },
      { k: 'clean', label: '有没有多余空格或符号', hint: '用下划线连接各段，避免空格和括号，跨设备打开才不会乱码。' },
      { k: 'topic', label: '主题词是否说得清楚', hint: '主题至少要有两个汉字，别用「新建文档」「未命名」这种说法。' }
    ];

    function analyse(name) {
      var n = name.trim();
      return {
        date: /\d{8}|\d{4}[-年]\d{1,2}/.test(n),
        ver: /v\s*\d+/i.test(n),
        clean: n !== '' && !/[\s（）()【】\[\]]/.test(n),
        topic: ((n.match(/[\u4e00-\u9fff]/g) || []).length >= 2) &&
               !/未命名|新建|新建文档|文档\d*$/.test(n)
      };
    }

    function render3() {
      var name = eInput.value;
      var res = analyse(name);
      eMgrRows.innerHTML = '';
      if (!name.trim()) {
        eMgrOut.className = 'result warn';
        eMgrOut.textContent = '先在上面输入一个你平时用的文件名，点「检查规范」看看。';
        eName.textContent = '—';
        return;
      }
      var score = 0;
      RULES.forEach(function (r) {
        var ok = res[r.k];
        if (ok) score = score + 1;
        var row = document.createElement('div');
        row.className = 'ta-check-row ' + (ok ? 'ok' : 'no');
        row.innerHTML = '<span class="mark">' + (ok ? '✓' : '✕') + '</span><span><strong>' +
          r.label + '</strong>：' + (ok ? '做到了' : '还差一点') +
          '。<span style="color:var(--muted)">' + r.hint + '</span></span>';
        eMgrRows.appendChild(row);
      });
      var today = '20260915';
      var topic = (name.match(/[\u4e00-\u9fff]{2,6}/) || ['作品'])[0].replace(/未命名|新建文档|新建/g, '') || '作品';
      var v = (name.match(/v\s*(\d+)/i) || [null, '1'])[1];
      eName.textContent = today + '_' + topic + '_v' + v;
      var cls = score === 4 ? '' : (score >= 2 ? 'warn' : 'error');
      var tip = score === 4
        ? '这个文件名已经符合规范，换一台设备、换一个人接手都能看明白。'
        : (score >= 2
            ? '基本能看懂，但还缺几项。一个规范的文件名，应该让人不看内容就知道「什么时候、什么主题、第几版」。'
            : '这个文件名的问题比较多。等到一个月后自己回头看，很可能已经想不起来它是什么了。');
      eMgrOut.className = 'result ' + cls;
      eMgrOut.innerHTML = '<strong>得分：' + score + ' / 4</strong><br>' + tip +
        '<br><strong>易错提醒：</strong>很多同学误认为文件名只要自己看得懂就够了。事实上文件一旦共享给别人，别人不认识你的简称；一旦有了多个版本，没有版本号就分不清哪一版最新。';
    }

    eCheck.addEventListener('click', render3);
    eInput.addEventListener('input', function () {
      if (eMgrRows.children.length > 0) render3();
    });
    eName.textContent = '—';
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：文件到底存在哪里？", TTS["pretest"], [
        {"q": "「上传」和「下载」这两个动作，方向分别是：",
         "options": [("上传是本地送到云端，下载是云端取回本地", True),
                     ("上传是云端取回本地，下载是本地送到云端", False),
                     ("两个动作方向一样，只是说法不同", False)],
         "explain": "上，是往云端去；下，是从云端回来。<strong>错因提醒：</strong>把上传和下载的方向搞反，是这一课最常见的错误，记住「上」对应的方向是往上送出去。"},
        {"q": "把文件保存到云端之后，本地的那份文件会怎么样？",
         "options": [("它还在本地，云端是另一份副本，两边可以保持同步", True),
                     ("本地那份会被自动删除", False),
                     ("本地那份不能再打开", False)],
         "explain": "云存储是在云端多放一份副本，不是把本地的那份搬走。两份保持一致，靠的是同步。"},
        {"q": "小组四个人同时改一份在线文档，最需要提前说清楚的是：",
         "options": [("谁负责哪一部分，以及各自的权限是什么", True),
                     ("谁的电脑配置最好", False),
                     ("谁的网速最快", False)],
         "explain": "这个问题先记在心里，等一下做同步实验时，你会看到没有分工和权限约定会发生什么。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "云存储：账号、云端副本与同步", TTS["module-1"], f'''
        <div class="inner-card">
          <p><strong>为什么要学这一课？</strong>你已经知道互联网是由许多网络互联而成的，数据可以在设备之间传输。<strong>但</strong>传过去的文件存在哪里，谁说了算？<strong>所以</strong>我们需要弄清云存储的工作方式，才能安全地存放和取用自己的数字作品。</p>
        </div>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>账号</strong></p>
            <p style="color:var(--muted)">账号决定你是谁，也决定你能看到哪些文件。账号一旦泄露，你的文件就不再只属于你。</p>
          </div>
          <div class="inner-card">
            <p><strong>云端副本</strong></p>
            <p style="color:var(--muted)">放在网络服务器上的那一份，是大家公认的权威版本；本地只是它的一个副本。</p>
          </div>
          <div class="inner-card">
            <p><strong>同步</strong></p>
            <p style="color:var(--muted)">自动做两件事：把本地改动送上去，把云端更新取下来，让两边尽量一致。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="云存储原理示意图：两台设备通过云端服务器保持副本一致">
          <figcaption>设备 A 与设备 B 各自持有一份副本，改动通过云端服务器传递，两边因此保持一致</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔀</span><div><strong>三个动作别搞混：</strong>上传是「本地 → 云端」，下载是「云端 → 本地」，同步是两个方向都自动做。三个动作都会改动数据，所以做之前要看清新旧。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同一份文件，在手机、平板、教室电脑上各有一个副本，改动却能互相同步——背后是云端那一份在当中转。"},
    {"lens": "解释它", "text": "为什么云存储能防丢失？因为云端服务器通常会把数据复制到多处保存。这属于「冗余」，代价是需要更多存储空间。"},
    {"lens": "迁移它", "text": "同步的思路不止用在文件上：浏览器的书签、笔记应用的记录，都是同一套「一份权威数据 + 多份副本」的模型。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "云同步模拟器：一次版本冲突是怎么发生的", TTS["lab-1"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">左边是你手里这份，右边是云端那份。先自己改一处，再让同伴在云端改一处，然后试着上传，看看会发生什么。</p>
        <div class="lab-panel" id="lab1-sync">
          <div class="ta-sync">
            <div class="ta-sync-box">
              <h4>本地副本<span class="ver" id="l1-local-ver">v1</span></h4>
              <div class="body" id="l1-local-body">实验报告 · 第一段：实验目的。</div>
              <span class="ta-flag" id="l1-local-flag">与云端一致</span>
            </div>
            <div class="ta-sync-box">
              <h4>云端副本<span class="ver" id="l1-cloud-ver">v1</span></h4>
              <div class="body remote" id="l1-cloud-body">实验报告 · 第一段：实验目的。</div>
              <span class="ta-flag" id="l1-cloud-flag">线上权威版本</span>
            </div>
          </div>
          <div class="flex-row">
            <button class="choice" id="l1-edit" style="text-align:center;flex:1">我在本地改一处</button>
            <button class="choice" id="l1-peer" style="text-align:center;flex:1">同伴在云端改一处</button>
          </div>
          <div class="flex-row">
            <button class="choice" id="l1-upload" style="text-align:center;flex:1">上传：本地 → 云端</button>
            <button class="choice" id="l1-download" style="text-align:center;flex:1">下载：云端 → 本地</button>
            <button class="choice" id="l1-reset" style="text-align:center;flex:1">重置</button>
          </div>
          <p class="result warn" id="l1-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>试试这条路线：</strong>先「我在本地改一处」，再点一次「同伴在云端改一处」，最后点「上传」。看到冲突提示后，想一想：如果当时先点一次「下载」，结果会不会不一样？</div></div>
    ''', tag="协作实验室", bloom="analyze"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "在线协作：同步、版本记录与权限", TTS["module-2"], f'''
        <div class="inner-card">
          <p><strong>两样东西维持秩序。</strong>第一是<strong>自动同步与版本记录</strong>：每次保存都留下一条历史，写错了可以回头看、往回转。第二是<strong>权限设置</strong>：决定谁能看、谁只能评论、谁可以改。</p>
        </div>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>只能查看</strong></p>
            <p style="color:var(--muted)">能读，不能改。适合发给需要了解情况的人。</p>
          </div>
          <div class="inner-card">
            <p><strong>可以评论</strong></p>
            <p style="color:var(--muted)">能读，能留建议，不能直接改正文。适合征求意见。</p>
          </div>
          <div class="inner-card">
            <p><strong>可以编辑</strong></p>
            <p style="color:var(--muted)">能直接改正文，改动会进入版本记录。适合同组同学。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="分享范围与权限档位对照示意图：仅指定的人、拿到链接的人、完全公开">
          <figcaption>分享范围决定「谁能进来」，权限档位决定「进来能做什么」，两件事要同时想清楚</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>易错点：只想着给权限，忘了想范围。</strong>「拿到链接的人」和「完全公开」看起来很省事，但链接一旦被转发出去，范围就失控了。涉及个人信息、成绩、联系方式的内容，分享范围必须收在「仅指定的人」。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "权限检查器：这个分享设置安全吗？", TTS["lab-2"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">先选一个权限档位，再选一个分享范围，看看查看、评论、编辑、转发这四件事分别会发生什么。</p>
        <div class="lab-panel" id="lab2-perm">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 给对方多大的权限</div>
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-perm="view" style="text-align:center">只能查看</button>
            <button class="choice" data-perm="comment" style="text-align:center">可以评论</button>
            <button class="choice" data-perm="edit" style="text-align:center">可以编辑</button>
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 分享给多大的范围</div>
          <div class="flex-row" style="margin-top:0">
            <button class="choice" data-scope="named" style="text-align:center">仅指定的人</button>
            <button class="choice" data-scope="link" style="text-align:center">拿到链接的人</button>
            <button class="choice" data-scope="open" style="text-align:center">完全公开</button>
          </div>
          <div class="ta-check" id="l2-rows" style="margin-top:16px"></div>
          <p class="result warn" id="l2-out" style="margin-top:14px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔐</span><div><strong>挑战：</strong>小组正在改一份还没定稿的草稿，既要方便大家一起补充，又不能外传。请找出一组最合适的设置，并说明你为什么这样选。</div></div>
    ''', tag="协作实验室", bloom="evaluate"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：两段内容为什么不见了", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>小组四人合作写实验报告。第二天打开文件，昨天写好的两段不见了。文件没有报错，容量也变小了。请分析原因并提出改进办法。</p>
        </div>
        <div class="inner-card">
          <p style="margin:0 0 6px"><strong>第一步　看清现象：</strong>内容少了，但文件能正常打开，说明不是文件损坏。</p>
          <p style="margin:0 0 6px"><strong>第二步　找出原因：</strong>两个人在各自设备上各改了一版。甲先上传到云端，乙手里还是旧副本，乙一上传，旧副本把甲那一版整个替换掉了。</p>
          <p style="margin:0 0 6px"><strong>第三步　判断性质：</strong>这是<strong>版本覆盖</strong>，不是丢失。云端和本地都存在过旧版本，只是没人发现。</p>
          <p style="margin:0"><strong>第四步　给出对策：</strong>动手前先同步一次；看到冲突提示不要强行覆盖，先比较两版再合并；更稳妥的是分工到不同章节，各自只改自己那一段。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不少同学误认为「上传」总是安全的，只有「下载」才会覆盖别的东西。事实是：上传和下载都会覆盖，只是方向相反。上传覆盖的是云端，下载覆盖的是本地。真正安全的做法不是回避这两个动作，而是<strong>动手之前先看清版本，两边都有改动时先合并</strong>。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "关于云存储，下面哪句话是正确的？",
         "options": [("本地和云端各有一份副本，同步让两边保持一致", True),
                     ("上传之后本地那份就不存在了", False),
                     ("只要存到云端，文件一定不会泄露", False)],
         "explain": "云存储是「多一份副本」，不是「搬家」。<strong>错因提醒：</strong>很多同学把上传误认为搬迁，其实本地那份通常还在。另外，云端安全不等于账号安全，账号泄露照样会出事。"},
        {"q": "你在本地改了文件，同时同伴也在云端改了同一份文件。这时最合适的做法是：",
         "options": [("先把两版内容放在一起比较，合并之后再上传", True),
                     ("直接上传，谁的版本新就用谁的", False),
                     ("两个人都别动，等文件自己变好", False)],
         "explain": "两边都有改动时，直接上传一定覆盖掉另一方。<strong>错因提醒：</strong>把「版本冲突」误认为「文件出错」是常见错误，其实它是提示你要先合并，而不是提示文件坏了。"},
        {"q": "要发一份还没定稿的小组草稿给组内同学补充意见，最合适的分享设置是：",
         "options": [("分享范围设为「仅指定的人」，权限给「可以评论」", True),
                     ("分享范围设为「完全公开」，权限给「只能查看」", False),
                     ("分享范围设为「拿到链接的人」，权限给「可以编辑」", False)],
         "explain": "范围收在名单内，权限刚好够用，既方便又安全。公开或链接分享会让范围失控。<strong>错因提醒：</strong>只盯着权限档位、忘了看分享范围，是最容易被忽略的常见错误。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给你的数字作品改一个规范的名字", TTS["synthesis"], f'''
        {LAB_CSS}
        <p style="color:var(--muted);margin:0 0 12px">规范的文件名，应该让人不看内容就知道「什么时候、什么主题、第几版」。输入你平时用的文件名，看看能得几分。</p>
        <div class="lab-panel" id="syn-manager">
          <div class="flex-row" style="margin-top:0">
            <input id="syn-filename" placeholder="例如：实验报告.docx 或 光的折射 v2" value="新建文档(2).docx" style="flex:1">
            <button class="choice" id="syn-check" style="text-align:center;flex:0 0 120px">检查规范</button>
          </div>
          <div class="ta-check" id="syn-rows" style="margin-top:14px"></div>
          <div class="lab-readout" style="margin-top:14px">
            <div class="readout-cell" style="flex:2">
              <span class="k">按规范应该这样命名</span>
              <span class="v" id="syn-suggest" style="font-size:16px">—</span>
            </div>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:14px"></p>
        </div>
        <div class="inner-card">
          <p><strong>再写一条你自己的规则：</strong>除了日期、主题、版本，你觉得小组文件还应该约定什么？写在下面，说明它是为了防止什么问题。</p>
          <textarea id="syn-answer" rows="3" placeholder="我们还应该约定……因为如果不这样，就会……"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换一个情境，看看规律还在不在", TTS["posttest"], [
        {"q": "同学把一份班级通讯录的分享链接发到了大群里，链接范围是「拿到链接的人」。最可能的风险是：",
         "options": [("链接会被不断转发，同学的姓名和联系方式会流出到范围之外", True),
                     ("文件会变大，占用更多存储空间", False),
                     ("文件会自动变成只读", False)],
         "explain": "「拿到链接的人」这个范围没有边界，转一次就多一圈人。通讯录属于他人个人信息，分享范围必须收在「仅指定的人」。<strong>错因提醒：</strong>误认为「有链接才能看」就等于安全，是最常见的判断失误。"},
        {"q": "误删了一份云端文件，最先应该做的是：",
         "options": [("去回收站或版本记录里找回来，别急着重新做", True),
                     ("马上重新写一份", False),
                     ("把账号注销再重新注册", False)],
         "explain": "云存储通常保留回收站和版本历史，误删和改错大多可以恢复。<strong>错因提醒：</strong>误认为删掉就彻底没了，于是重做一遍，白白浪费时间。"},
        {"q": "小组合作写一份报告，为了减少互相覆盖，最有效的做法是：",
         "options": [("分工到不同章节，各自只改自己负责的那一段，改完先同步再上传", True),
                     ("每个人都在同一个段落上反复修改", False),
                     ("约定大家都不要保存，最后一个人统一写", False)],
         "explain": "分工加同步，是减少版本冲突最直接的办法。它靠的是约定，而不是指望技术自动解决一切。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''
        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>云存储</strong>：账号区分身份，云端副本是权威版本，同步让多设备保持一致；上传是本地到云端，下载是云端到本地。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>在线协作</strong>：靠自动同步和版本记录维持秩序，靠权限设置决定谁能做什么；范围决定谁能进来，权限决定进来能做什么。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>作品管理</strong>：规范命名、分类归档、保留版本、定期备份，只给必要的人必要的权限。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那起事故：</strong>两段内容没有消失，是被旧版本覆盖了。如果当时动手前先同步一次，或者分工到不同章节，这场事故根本不会发生。技术给了我们方便的协作方式，而用得对，靠的是约定和规范。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「云端副本、同步、版本冲突、分享范围」这四个词，说清楚这次事故是怎么发生的、以后怎么避免。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "说出上传、下载、同步三个动作的区别，并各举一个你实际用过的例子。",
            "写出查看、评论、编辑三种权限分别能做什么，以及它们各自适合什么场合。",
            "列出数字作品管理规范的四个要点，每个要点用一句话说明它的作用。",
        ],
        [
            "把自己云盘里的一个文件夹按规范重新命名和归档，把整理前后的文件名对照记录下来。",
            "给自己的一份文件设置一个合适的分享范围与权限，并写下你这样设置的理由。",
        ],
        [
            "为小组合作写出一份文件管理约定，说明命名规则、版本规则和分工方式，并逐条解释每条约定是为了防止什么问题。",
            "找一次你经历过的文件混乱事件（内容丢失、版本搞混、发错人），分析原因属于哪一类，并写出改进办法。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-m-cloud-collaboration",
    "node_id": "it-m-cloud-collaboration",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "middle",
    "stage_cn": "初中",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 初中",
    "title": "云存储与在线协作",
    "name_en": "Cloud Storage and Online Collaboration",
    "grade": 7,
    "grade_cn": "七年级",
    "domain": "internet-innovation",
    "domain_cn": "互联网应用与创新",
    "lesson_type": "application-practice",
    "version": "1.0.0",
    "description": "通过版本冲突模拟与权限组合判定，理解云存储的账号、云端副本与同步机制，掌握在线协作中版本记录与权限设置的作用，并能按规范管理自己的数字作品、安全地分享文件。",
    "tags": ["云存储", "在线协作", "同步", "版本记录", "权限", "数字作品管理"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》初中「互联网应用与创新」——体验云存储与协作工具，规范进行数字作品管理；在互联网应用中遵守法律法规与信息社会责任。",
    "hero_question": "同一份文件，几个人同时在改，为什么有的改动留下了、有的却不见了？",
    "hero_alt": "云存储与在线协作知识结构图：云存储原理、协作与权限、作品管理三栏",
    "hero_caption": "云存储原理 → 在线协作与权限 → 数字作品管理：分清上传下载 · 看清版本与范围 · 规范命名与备份",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "文件放到云端之后，到底存在哪里？", "d": "本地那份还会不会留在电脑里", "v": "文件放到云端之后到底存在哪里"},
        {"t": "几个人同时改一份文件，为什么不会乱？", "d": "背后的同步和版本记录是怎么回事", "v": "几个人同时改一份文件为什么不会乱"},
        {"t": "为什么我昨天写好的内容会不见？", "d": "想弄清版本覆盖到底怎么发生", "v": "为什么我昨天写好的内容会不见"},
        {"t": "分享给谁、给多大的权限才安全？", "d": "怎样既方便又不外泄", "v": "分享给谁给多大的权限才安全"},
    ],
    "objectives": [
        "能说清楚云存储的基本原理，分清上传、下载与同步三个动作",
        "能说明在线协作依靠版本记录与自动同步维持秩序",
        "能根据任务需要选择合适的分享范围与权限，并说出其中的安全风险",
        "能按规范管理数字作品，给文件规范命名、分类归档并保留版本",
    ],
    "objectives_plain": [
        "能说清楚云存储的基本原理，分清上传、下载与同步三个动作",
        "能说明在线协作依靠版本记录与自动同步维持秩序",
        "能根据任务需要选择合适的分享范围与权限，并说出其中的安全风险",
        "能按规范管理数字作品，给文件规范命名、分类归档并保留版本",
    ],
    "standards": [
        {"content": "体验云存储与协作工具，规范进行数字作品管理。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》互联网应用与创新 · 初中"},
        {"content": "在互联网应用中遵守法律法规与伦理规范，保护个人信息，负责任地分享与协作。",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》信息社会责任 · 初中"},
    ],
    "prereqs": ["it-m-internet-architecture"],
    "prereqs_name": "互联网结构与协议初识",
    "prereqs_meta": "it-m-internet-architecture",
    "leads_to": ["it-m-web-development"],
    "next_meta": "it-m-web-development",
    "section_images": ["assets/it-m-cloud-collaboration-fig1.webp", "assets/it-m-cloud-collaboration-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "写好的两段内容第二天不见了，文件却没坏——问题出在哪？带着这个疑问开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己判断一次分享设置安不安全。",
        "objectives": "看清四件事：云存储原理、协作机制、权限与范围、数字作品管理规范。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "账号、云端副本、同步是三个关键点；上传朝上走，下载朝下走，别搞反。",
        "lab-1": "试试「本地改一处 + 同伴改一处 + 上传」，看清版本冲突是怎么被拦下的。",
        "module-2": "范围决定谁能进来，权限决定进来能做什么，两件事要同时想。",
        "lab-2": "先把权限和范围都拉到最松，再一点点收紧，看看风险提示怎么变化。",
        "worked-example": "四步走：看清现象、找出原因、判断性质、给出对策。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "先输入一个你平时用的文件名看看得几分，再对比系统给出的规范名。",
        "posttest": "换了通讯录和误删的新情境，看看你还能不能用上同一条原则。",
        "summary": "用「云端副本、同步、版本冲突、分享范围」四个词，把这次事故讲给同桌听。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是初中「互联网应用与创新」领域长期空缺的一课。设计上不依赖任何具体云服务产品，只把机制拆成可以动手操作的两件事：一是用同步模拟器把「版本冲突」从一个模糊的说法变成可复现的状态变化，学生能亲眼看到旧副本覆盖新版本；二是用权限检查器把「分享范围 × 权限档位」的组合结果一条条判定出来，并给出风险等级。最后落在数字作品管理的规范上，让学生带走一套可执行的命名、归档与备份约定。",
    "plan_table": """| 1 | cover | 云存储与在线协作 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：文件到底存在哪里？ | 起·前测（暴露直觉） |
| 5 | concept | 云存储：账号、云端副本与同步 | 承·概念一 |
| 6 | interactive | 云同步模拟器：一次版本冲突是怎么发生的 | 承·实验室一（状态可复现） |
| 7 | concept | 在线协作：同步、版本记录与权限 | 承·概念二 |
| 8 | interactive | 权限检查器：这个分享设置安全吗？ | 承·实验室二（组合判定，可评估） |
| 9 | concept | 例题示范：两段内容为什么不见了 | 转·重难点突破（分步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给你的数字作品改一个规范的名字 | 合·迁移应用 |
| 12 | quiz | 后测：换一个情境，看看规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：云存储原理 / 协作与权限 / 作品管理三栏标注\n- P5 云存储原理示意图（已生成）：两台设备经云端服务器保持副本一致\n- P7 分享范围与权限档位对照图（已生成）：仅指定的人 / 拿到链接的人 / 完全公开\n- 若需补充：小组协作场景的照片（用于开场情境）",
}
