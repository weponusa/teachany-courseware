# -*- coding: utf-8 -*-
"""高中 · 心理健康 · 同伴支持与合作学习（高二）—— 补齐知识树「人际交往」空缺

铁规：语气温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀与暴力情节。
核心模拟：想帮忙时怎么说——对比台（同一情境两种回应 → 对方感受与后续）。
另含：什么时候必须转给大人——判断台（八种情形 → 先陪着说 / 告诉老师或家长）
      + 互评改写台（五句常见说法 → 选出能接着往下做的那一句）。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-h-g11-peer-support-fig1.webp'
F2 = './assets/psych-h-g11-peer-support-fig2.webp'

TTS = {
    "hero": "先说一个很常见的时刻。朋友跟你说他这次考砸了，你想帮上忙，可话到嘴边又停住——好像说什么都不太对。又或者小组作业里，有一个人一直没交他那部分，你替他把活干完，心里却堵着。这节课我们只练两件在同学之间最用得上的事。第一件是怎么听、怎么说：先听完，不急着给建议，也不说这有什么大不了。第二件是分工与互评：一次合作里，活怎么分、话怎么评，才不至于做完事却生分了。中间还有一件事要说清楚：有些情形，靠同伴是不够的，那时候要找老师或者家长。",
    "problem-anchor": "在开始之前，先选出最贴近你最近状态的一项。是想知道朋友难受的时候该说什么，还是想知道什么时候该找老师或家长，又或者是想知道小组合作里怎么分工、怎么互评。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出三种好意却帮不上的回应，并各自改成一句能接得住的话。第二，会按先听再说的顺序，为同一个情境写出两种回应，并比较它们分别把人带到哪里。第三，能说出什么时候必须把事情告诉老师或家长，并知道转之前该怎么说。第四，能给一次小组合作做分工与互评，把话说成能接着做下去的那一种。",
    "pretest": "先做三道小题，凭你平时的习惯选就行，没有对错，也不打分。选完会立刻出现解释，正好帮你看清自己现在习惯怎么回应别人。",
    "module-1": "我们先把最要紧的一件事说清楚：支持是从听开始的，不是从给办法开始的。有三种回应，出发点是好的，却常常帮不上忙。第一种是急着给建议：对方话还没说完，你就开始告诉他该怎么做。第二种是把事情说小了：这有什么大不了的、我早就经历过了。第三种是比惨：你这算什么，我那次更惨。这三种有一个共同点——对方的话没有被接住，他还要额外花力气跟你解释一遍自己的感受。而先听，做起来只有三个动作：停一下不打断，把他说的那件事重复一小句，再问一句你愿意多说点吗。请留意，这不是让你从此不能给建议，而是把顺序换一下：先听完，再问他要不要。",
    "lab-1": "现在打开对比台。先选一个你大概真的遇到过的情境，再把两种回应各点开一次，看看它们分别可能把后面的对话带到哪里。请留意，两种回应都可能是好意，差别在于对方还要不要多解释一层。这里的说法都是可能，不是一定。",
    "module-2": "还有一件事必须说清楚：有些情形，一个人扛不住，也不该由同伴来扛。怎么判断？看三条线。第一条是时间：这件事已经持续了一段时间，不是今天一天。第二条是程度：已经影响到吃饭、睡觉、上课，或者他自己也说不知道该怎么办。第三条是安全：涉及身体被伤害、被威胁，或者有人被反复针对。这三条里只要碰到一条，就应该告诉老师或者家长。转之前有一件事可以做：先跟同伴说你要去找谁、为什么，能一起去找更好；如果来不及说，事后也要告诉他。这不是打小报告，这是把一件超出你能力的事，交给能处理它的人。",
    "lab-2": "下面有八个情形，每个情形选一个做法：先陪着他说，或者要告诉老师或家长。选完会给出解释。请留意，选转给大人不等于你不管他了，你仍然可以在他旁边。",
    "worked-example": "我们完整走一遍。情境是：老师布置了一个小组调查，四个人，两周后交。第一步，先分活：把任务切成四块，每一块写清什么时候交、交给谁。第二步，认领之前先问三句：你比较想做什么、你哪几天时间紧、有哪一块你最没把握。第三步，留一个中途碰头的时间，不要等到交之前那一晚。第四步，互评只说三件事：哪一部分帮到了我、哪一处我有点跟不上、下一步我建议怎么改。第五步，如果有人一直没交，先说清时间和那部分，再一起想办法，必要时跟老师说明情况。",
    "conceptest-1": "现在用三个容易弄混的说法考考你。请仔细读每一个选项，选出你认为更合适的那个，然后看解释。",
    "synthesis": "最后练一练互评。下面有五句在小组里很常听到的评价，每一句我给三个说法。请你选出那个能接着往下做的说法。选完会给出解释，也请你留意，哪一种说法会让对方愿意再改一次。",
    "posttest": "最后换几个新情境检验一下。这次的问题出现在一段聊天里、一次小组合作里，还有一次你需要决定要不要找老师的时候。",
    "summary": "这节课我们弄明白了三件事。第一，支持从听开始：不急着给建议，不把事情说小，不急着比惨。第二，有些情形不该由同伴扛：时间久了、影响到吃饭睡觉上课、或者涉及安全，就要告诉老师或者家长，转之前先说一声。第三，合作学习里，分工要写清时间和交付，互评只说哪一部分帮到了我、哪一处我跟不上、下一步怎么改。最后把要求放低一点：不必去做那个什么都能解决的人，做一个愿意听、也知道什么时候找人的人，就已经够了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写下三种好意却帮不上的回应，各用一句话说明它为什么帮不上。第二层能力应用，动手做：找一个最近真实发生过的情境，写出两种回应，再写出它们分别可能把对话带到哪里。第三层迁移挑战，选做：在一次真实的小组合作里，试着按分工四问分一次活，并在结束时用互评三句式说一次反馈，一周后回看对方的反应。",
    "knowledge-graph": "这张图展示了这节课在知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 支持从听开始", "lab-1": "核心模拟 想帮忙时怎么说对比台",
    "module-2": "概念二 有些情形要交给大人", "lab-2": "判断台 什么时候转给大人",
    "worked-example": "例题示范", "conceptest-1": "概念测试",
    "synthesis": "综合任务 互评改写台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   psych-h-g11-peer-support 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 核心模拟：想帮忙时怎么说——对比台（情境 × 两种回应 → 感受与后续）
   3) 判断台：什么时候必须转给大人（八种情形 → 先陪 / 转给大人）
   4) 互评改写台（五句常见说法 → 选出能接着往下做的那一句）
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

  /* ---------- 2. 对比台：想帮忙时怎么说 ---------- */
  var CMP = {
    exam: {
      n: '朋友说：这次考试我真的是彻底不行了。',
      a: '你就是没好好复习，下次早点开始就行。',
      b: '听起来这次挺让你难受的。要不要说说，是哪一段最卡？',
      ao: '这句话里没有他能接住的地方，他还得先跟你解释一遍自己的感受。他大概不会再跟你说第二句了。',
      bo: '他可能还是不想细说，但至少不用先解释自己。往下说的门还开着——他愿意说就说，不愿意也没关系。'
    },
    mom: {
      n: '同学说：我跟我妈又吵了一架，烦死了。',
      a: '这有什么大不了的，我妈也这样。',
      b: '听起来这两天在家挺累的。',
      ao: '这句话把他刚说的事变小了，等于告诉他这不值得说。他下次多半不会挑你讲。',
      bo: '先接住，不接着追问。他不必马上回答，可以自己决定要不要多说一点。有时候这样就够了。'
    },
    tire: {
      n: '同桌说：我这次什么都没复习，反正也没用。',
      a: '别这么说，你肯定行的！',
      b: '你这么说，是发生什么事了吗？',
      ao: '这句话是好意，但它跳过了他刚说的那件事，等于让他重新去接一句安慰。',
      bo: '把话头交回给他：他可以讲，也可以不讲。比起替他打气，他往往更需要有人先问一句。'
    },
    class: {
      n: '组员说：我这两天不太想去上课。',
      a: '别啊，不去更完蛋。',
      b: '听你这么说我有点在意。是最近发生什么了吗？我在。',
      ao: '这句话只说了后果，没问他怎么了。他本来是想说点什么才开口的。',
      bo: '先接住，再看他说不说。接下来可以陪他去找班主任聊一聊——有些事，本来就不该由同伴一个人扛。'
    }
  };
  var cmpStage = document.getElementById('cmp-stage');
  if (cmpStage) {
    var cs = 'exam';
    var picked = {};
    function renderCmp() {
      var C = CMP[cs];
      document.getElementById('cmp-scene').textContent = '情境：' + C.n;
      document.getElementById('cmp-a-txt').textContent = C.a;
      document.getElementById('cmp-b-txt').textContent = C.b;
      document.querySelectorAll('[data-cmp-scene]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.cmpScene === cs);
      });
      ['a', 'b'].forEach(function (k) {
        var out = document.getElementById('cmp-' + k + '-out');
        var btn = document.querySelector('[data-cmp-pick="' + k + '"]');
        if (picked[cs + k]) {
          out.style.display = 'block';
          out.className = 'result' + (k === 'a' ? ' warn' : '');
          out.innerHTML = (k === 'a'
            ? '<strong>这样回应，可能会：</strong>' + C.ao + '<br>还可以试试另一种说法。'
            : '<strong>这样回应，可能会：</strong>' + C.bo);
          btn.style.display = 'none';
        } else {
          out.style.display = 'none';
          btn.style.display = 'block';
        }
      });
      var note = document.getElementById('cmp-note');
      if (picked[cs + 'a'] && picked[cs + 'b']) {
        note.className = 'result';
        note.innerHTML = '<strong>两种都点开了。</strong>两种回应都可能是好意，差别在于对方还要不要多解释一层' +
          '——以及他下一次还愿不愿意开口。这就是先听再说的用处。';
      } else {
        note.className = 'result warn';
        note.innerHTML = '把两种回应都点开一次，比较一下它们分别把后面的对话带到哪里。';
      }
    }
    document.querySelectorAll('[data-cmp-scene]').forEach(function (b) {
      b.addEventListener('click', function () { cs = b.dataset.cmpScene; renderCmp(); });
    });
    document.querySelectorAll('[data-cmp-pick]').forEach(function (b) {
      b.addEventListener('click', function () {
        picked[cs + b.dataset.cmpPick] = true;
        renderCmp();
      });
    });
    renderCmp();
  }

  /* ---------- 3. 判断台：什么时候必须转给大人 ---------- */
  var HAND = [
    { t: '朋友说这次考砸了，心里堵得慌，但今天已经能说笑了。', a: 'stay',
      stay: '今天这件事还在他能自己消化的范围里。先陪着他说几句，比急着出主意有用。',
      refer: '这一条还不需要交给大人。先跟着他走一段，看他接下来几天怎么样。' },
    { t: '同学连着两个星期说吃不下、睡不着，人也瘦了一圈。', a: 'refer',
      stay: '你陪他已经陪了两周，这件事超过了同伴能处理的范围。',
      refer: '时间够久、已经影响到吃饭和睡觉——这两条都碰到了。要告诉老师或家长。' },
    { t: '组员因为分工的事跟你发了脾气，第二天主动来找你说话。', a: 'stay',
      stay: '一次闹别扭、第二天又主动来和好，通常你们两个人就能处理完。',
      refer: '这一条还不需要交给大人。你们自己已经往前走了。' },
    { t: '班里有人在群里反复发同一个同学的照片取笑他。', a: 'refer',
      stay: '这不是你们两个人之间的事，也不是私下说说就能停下来的。',
      refer: '被反复针对、又是在群里发生——一个人挡不住。告诉老师，也可以让家长知道。' },
    { t: '好朋友说他和家里人吵了一架，想找你说说话。', a: 'stay',
      stay: '他想找个人说说话，这件事有人听就往下走了。',
      refer: '这一条还不需要交给大人。先听他把话说完。' },
    { t: '同学说他被几个人堵过两次，还被警告不许告诉别人。', a: 'refer',
      stay: '涉及身体被伤害，又被人要求保密——这不是能替他瞒着的事。',
      refer: '只要碰到安全这一条，就要告诉老师或家长。这是把他的安全放在第一位，不是不守约定。' },
    { t: '同桌这次没考好，怕回家，问你能不能陪他走一段。', a: 'stay',
      stay: '他要的是有人陪着走一段，这件事你正好做得到。',
      refer: '这一条还不需要交给大人。陪他走一段，路上听他说说就好。' },
    { t: '朋友说他最近总是提不起劲，已经好几周了，自己也不知道该怎么办。', a: 'refer',
      stay: '好几个星期，连他自己也说不知道该怎么办——这已经不是陪一陪就能过去的。',
      refer: '时间够久、他自己也没办法，这两条都碰到了。和他一起去找老师或家长会更稳。' }
  ];
  var handStage = document.getElementById('hand-stage');
  if (handStage) {
    function renderHand() {
      handStage.innerHTML = HAND.map(function (c, i) {
        var btns = [['stay', '先陪着他说'], ['refer', '要告诉老师或家长']].map(function (k) {
          var cls = 'choice';
          if (c.picked === k[0]) cls += (k[0] === c.a ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-hand="' + i + '" data-hand-pick="' + k[0] +
            '" style="text-align:center;font-size:13px">' + k[1] + '</button>';
        }).join('');
        return '<div class="plain-row" style="padding:12px 14px;border-radius:12px;background:var(--bg-subtle);' +
          'border:1px solid var(--line-subtle);margin:8px 0">' +
          '<p style="margin:0 0 8px"><strong>' + (i + 1) + '. ' + c.t + '</strong></p>' +
          '<div class="grid" style="grid-template-columns:repeat(2,1fr);gap:6px">' + btns + '</div>' +
          (c.picked ? '<p class="result ' + (c.picked === c.a ? '' : 'warn') + '" style="margin:8px 0 0">' +
            (c.picked === c.a ? '<strong>这个判断挺合适。</strong>' : '<strong>还可以再想想：</strong>') +
            c[c.picked] + '</p>' : '') +
          '</div>';
      }).join('');
      handStage.querySelectorAll('[data-hand]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.hand, 10);
          if (HAND[i].picked) return;
          HAND[i].picked = b.dataset.handPick;
          renderHand();
          var done = HAND.filter(function (x) { return x.picked; }).length;
          var out = document.getElementById('hand-out');
          out.style.display = 'block';
          out.className = 'result' + (done >= 8 ? '' : ' warn');
          out.innerHTML = '<strong>已判断 ' + done + '/8 个情形。</strong>' +
            '三条线是时间、程度和安全——只要碰到一条，就该交给能处理它的人。' +
            '转之前记得先说一声：告诉他你要去找谁、为什么，能一起去找更好。' +
            (done >= 8 ? '<br>八个都判断完了。你可以回头看看，有没有哪个情形是你之前会自己扛下来的。' : '');
        });
      });
    }
    renderHand();
  }

  /* ---------- 4. 互评改写台 ---------- */
  var FB = [
    { q: '组员交上来的那部分写得很简单，你想说它不够。',
      o: [['你这也太敷衍了吧。', 0, '这一句评价的是人，不是那部分内容。对方多半先要为自己辩解，改的事就往后放了。'],
          ['这一部分我看得有点跟不上，能不能再补两个例子？', 1, '说的是那部分内容，还给出了一个具体动作。对方知道下一步做什么，也更容易接。'],
          ['算了，我自己重写一遍。', 0, '这样活是干完了，只是他不知道自己哪里不够，下次还会一样。']] },
    { q: '你想说自己提的那个点被漏掉了。',
      o: [['每次都这样，你们根本没听我说。', 0, '说的是人，而且是每一次。对方第一反应会是反驳，不是去补。'],
          ['上一条我提的那个点没被写进去，我来补在第三段，可以吗？', 1, '说的是具体位置和具体动作，还留了一个可以商量的口子。这是最容易接着做的一句。'],
          ['随便吧。', 0, '这一句把话收回去了。问题还在，你也憋着。']] },
    { q: '你想给同学提一个改进建议。',
      o: [['你会不会做图啊。', 0, '这一句问的是能力，不是图。对方收到的是评价，不是建议。'],
          ['我觉得第 2 页那张图换一张会更清楚，你方便换吗？', 1, '指出位置、说出理由、提出请求，三样都在，对方知道改哪里。'],
          ['挺好的，没意见。', 0, '跳过不提，问题还在那儿，只是留到了最后一天。']] },
    { q: '你想说这次合作里哪一块帮到了你。',
      o: [['你总算做了点事。', 0, '这句话里带着账本。就算对方真的做了，听完也不会舒服。'],
          ['还行吧。', 0, '省了力气，也省掉了那句能让人愿意再来一次的谢谢。'],
          ['谢谢你昨天把数据整理完，我省了很多时间。', 1, '说出具体做了哪件事、省了你什么。这种反馈最容易被记住，也最容易被重复。']] },
    { q: '你想提醒组员时间快到了。',
      o: [['你又要拖到最后一天吗？', 0, '说的是他的习惯，不是这次的时间。对方先要证明自己不是那样的人。'],
          ['离交还有三天，剩下这一块要不要今晚定个时间？', 1, '说清时间，把决定权留给他。既提醒了，也没有把人推到墙角。'],
          ['我就不说了，等着看。', 0, '不说，时间也不会自己变多，最后往往还是你加班。']] }
  ];
  var fbStage = document.getElementById('fb-stage');
  if (fbStage) {
    function renderFb() {
      fbStage.innerHTML = FB.map(function (c, i) {
        var opts = c.o.map(function (o, j) {
          var cls = 'choice';
          if (c.picked === j) cls += (o[1] ? ' correct' : ' wrong');
          return '<button class="' + cls + '" data-fb="' + i + '" data-fb-pick="' + j +
            '" style="font-size:13px;padding:10px 14px">' + o[0] + '</button>';
        }).join('');
        return '<div class="plain-row" style="padding:12px 14px;border-radius:12px;background:var(--bg-subtle);' +
          'border:1px solid var(--line-subtle);margin:8px 0">' +
          '<p style="margin:0 0 8px"><strong>' + (i + 1) + '. ' + c.q + '</strong></p>' +
          '<div class="grid" style="gap:6px">' + opts + '</div>' +
          (c.picked !== undefined ? '<p class="result ' + (c.o[c.picked][1] ? '' : 'warn') +
            '" style="margin:8px 0 0">' + (c.o[c.picked][1] ? '<strong>这一句能接着往下做。</strong>' :
            '<strong>还可以再想想：</strong>') + c.o[c.picked][2] + '</p>' : '') +
          '</div>';
      }).join('');
      fbStage.querySelectorAll('[data-fb]').forEach(function (b) {
        b.addEventListener('click', function () {
          var i = parseInt(b.dataset.fb, 10);
          if (FB[i].picked !== undefined) return;
          FB[i].picked = parseInt(b.dataset.fbPick, 10);
          renderFb();
          var done = FB.filter(function (x) { return x.picked !== undefined; }).length;
          var out = document.getElementById('fb-out');
          out.style.display = 'block';
          out.className = 'result' + (done >= 5 ? '' : ' warn');
          out.innerHTML = '<strong>已选 ' + done + '/5 句。</strong>' +
            '互评只说三件事：哪一部分帮到了我、哪一处我跟不上、下一步我建议怎么改。' +
            '说的是那部分活，不是那个人。' +
            (done >= 5 ? '<br>五句都选完了。你可以看看，自己原来习惯用哪一种说法。' : '');
        });
      });
    }
    renderFb();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：同伴开口的时候，你习惯怎么接？", TTS["pretest"], [
        {"q": "朋友跟你说他这次考砸了，特别难受。下面哪一种回应更可能让他愿意往下说？",
         "options": [("那你下次早点开始复习不就行了", False),
                     ("听起来这次挺让你难受的，要不要说说哪一段最卡", True),
                     ("这有什么大不了的，一次考试而已", False)],
         "explain": "先把他说的事接住，他才知道往下说不用先解释自己。<strong>错因提醒：</strong>常见错误是误认为越快给出办法越有用——话还没说完就递办法，对方往往先要花力气跟你解释一遍感受。"},
        {"q": "下面哪一条更像「先听」该有的样子？",
         "options": [("停一下不打断，把他说的那件事重复一小句，再问他要不要多说点", True),
                     ("一边听一边想下一句该说什么", False),
                     ("先说说自己更惨的经历，让他觉得不是一个人", False)],
         "explain": "重复一小句，是让对方知道你听清了；问一句要不要，是把决定权交回给他。<strong>错因提醒：</strong>容易把「比惨」搞混成共情——讲自己更惨的经历，常常会让对方把话收回去。"},
        {"q": "关于「告诉老师或家长」，下面哪一种说法更合适？",
         "options": [("这是打小报告，能不说就不说", False),
                     ("涉及安全、或者已经持续很久又影响到吃饭睡觉上课，就该交给大人", True),
                     ("只有对方同意，才可以告诉老师", False)],
         "explain": "把超出自己能力的事交给能处理它的人，是对同伴的照顾，不是出卖。<strong>错因提醒：</strong>误认为任何情况下都必须替对方保密，会让一件本来可以早点处理的事拖得更久。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "支持从「听」开始，不是从给办法开始", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">有三种回应，出发点是好的，却常常帮不上忙。先认出它们，再换成一句能接得住的话。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>为什么要先学这个？</strong>你已经知道朋友难受时该关心他；<strong>但</strong>话一急，往往先递办法、先说这没什么；<strong>所以</strong>先把顺序换过来——先听完，再问他要不要。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>急着给建议：</strong>对方话还没说完，你就开始告诉他该怎么做。他要的是有人听，不是一份方案。</div></div>
          <div class="step"><span class="n">2</span><div><strong>把事情说小：</strong>这有什么大不了的、我早就经历过了。等于告诉他这件事不值得说。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>急着比惨：</strong>你这算什么，我那次更惨。话头一下转到你身上，他只好把话收回去。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">👂</span><div><strong>先听的三个动作：</strong>停一下不打断；把他说的那件事重复一小句；再问一句你愿意多说点吗。三个动作加起来，通常不超过两句话。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为先听就是不说话、不给建议。其实顺序换一下就行：先听完，再问他<strong>要不要</strong>听你的想法。给建议不是错，抢在他讲完之前给才是。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="三种好意却帮不上的回应示意图：急着给建议、把事情说小、急着比惨">
          <figcaption>三个常见的岔口：急着给建议、把事情说小、急着比惨——绕开它们，对话才有往下走的余地</figcaption>
        </figure>
{insight_box([
    {"lens": "解释它", "text": "为什么抢着给建议反而帮不上？因为对方开口的时候，要的常常是把话说出来，而不是马上解决问题。"},
    {"lens": "比较它", "text": "「别难过了」和「听起来这次挺让你难受的」，长度差不多，但后者把他的话接住了，前者让他把话吞回去。"},
    {"lens": "迁移它", "text": "这一套不只对朋友管用。家里人抱怨的时候、同学在群里发牢骚的时候，先复述一句再问要不要，同样管用。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "cmp", 5, "lab-1", "核心模拟：想帮忙时怎么说——对比台", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先选一个你真的遇到过的情境，再把两种回应各点开一次，比较它们分别把后面的对话带到哪里。</p>
        <div class="lab-panel" id="cmp-stage">
          <div class="flex-row" style="flex-wrap:wrap">
            <button class="choice" data-cmp-scene="exam" style="text-align:center;font-size:13px">朋友说这次彻底不行了</button>
            <button class="choice" data-cmp-scene="mom" style="text-align:center;font-size:13px">同学说又跟妈妈吵架了</button>
            <button class="choice" data-cmp-scene="tire" style="text-align:center;font-size:13px">同桌说反正也没用</button>
            <button class="choice" data-cmp-scene="class" style="text-align:center;font-size:13px">组员说不太想去上课</button>
          </div>
          <p class="result" id="cmp-scene" style="margin-top:12px"></p>
          <div class="grid grid-2" style="margin-top:10px">
            <div class="inner-card">
              <p><strong>回应 A</strong></p>
              <p id="cmp-a-txt" style="color:var(--muted)"></p>
              <button class="choice" data-cmp-pick="a" style="text-align:center;font-size:13px">点开：对方可能的感受与后续</button>
              <p class="result warn" id="cmp-a-out" style="display:none;margin-top:8px"></p>
            </div>
            <div class="inner-card">
              <p><strong>回应 B</strong></p>
              <p id="cmp-b-txt" style="color:var(--muted)"></p>
              <button class="choice" data-cmp-pick="b" style="text-align:center;font-size:13px">点开：对方可能的感受与后续</button>
              <p class="result" id="cmp-b-out" style="display:none;margin-top:8px"></p>
            </div>
          </div>
          <p class="result warn" id="cmp-note" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💬</span><div><strong>四个情境都试完之后：</strong>选出你自己最常说的那一句，把它改成能接得住的那一种。改一句就够，不必四句都改。</div></div>
    ''', tag="核心模拟", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "有些情形，不该由同伴一个人扛", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">陪伴有它的位置，也有它的边界。下面三条线，只要碰到一条，就该交给能处理它的人。</p>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="什么时候要交给大人的三条判断线示意图：时间、程度、安全">
          <figcaption>三条判断线：时间够不够久、有没有影响到吃饭睡觉上课、有没有涉及安全</figcaption>
        </figure>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>时间：</strong>这件事已经持续了一段时间，不是今天一天，也不是一两次。</div></div>
          <div class="step"><span class="n">2</span><div><strong>程度：</strong>已经影响到吃饭、睡觉、上课，或者他自己也说不知道该怎么办。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>安全：</strong>涉及身体被伤害、被威胁，或者有人被反复针对。这一条最优先。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🤝</span><div><strong>转之前先说一声：</strong>告诉他你要去找谁、为什么；能一起去找更好；如果来不及说，事后也要告诉他。这不是打小报告，是把一件超出你能力的事交给能处理它的人。</div></div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为「答应过保密就不能说」。保密的前提是这件事还在你们能处理的范围内；一旦碰到安全，先保证他安全，再解释你为什么要说。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "hand", 7, "lab-2", "判断台：什么时候必须转给大人？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">八个情形，每个选一个做法。选完会给出解释——选转给大人，不等于你不管他了。</p>
        <div class="lab-panel" id="hand-stage"></div>
        <p class="result warn" id="hand-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong></p>
          <p style="color:var(--muted)">如果以后真的遇到要交给大人的情形，你打算怎么跟同伴开这个口？写一句你大概会说的话。</p>
          <textarea id="hand-answer" rows="3" placeholder="我想我会这样说：我知道这件事你不想让别人知道，但……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="动手实验室", bloom="evaluate"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：一次小组合作，从卡住到推进", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>情境：</strong>老师布置了一个小组调查，四个人，两周后交。上一次你们拖到最后一天才动手。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先分活：</strong>把任务切成四块，每一块写清什么时候交、交给谁。写下来的和口头说的，效果不一样。</div></div>
          <div class="step"><span class="n">2</span><div><strong>认领之前问三句：</strong>你比较想做什么、你哪几天时间紧、有哪一块你最没把握。</div></div>
          <div class="step"><span class="n">3</span><div><strong>留一次中途碰头：</strong>不要等到交之前那一晚。中途看一眼，比最后返工省力。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>互评只说三件事：</strong>哪一部分帮到了我、哪一处我有点跟不上、下一步我建议怎么改。</div></div>
          <div class="step"><span class="n">5</span><div><strong>有人一直没交怎么办：</strong>先说清时间和那部分，再一起想办法；必要时跟老师说明情况。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">两个方向都容易走偏：一种是<strong>不分工、自己全做完</strong>，事是交了，关系却生分了；另一种是<strong>把互评说成对人的评价</strong>，比如你会不会做图啊——对方第一反应是辩解，改的事就往后放了。</p>
        </div>
        <div class="inner-card">
          <p><strong>把期待放在合适的位置：</strong>这些做法不保证每次合作都顺利，也不保证每个人都会配合。它们能做的是：让活有清楚的分界，让话有地方可以说。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "「这有什么大不了的，我早就经历过了」——这句话最需要改的地方是：",
         "options": [("它把他说的那件事变小了，等于告诉他这件事不值得说", True),
                     ("它说得太肯定了，应该加一个也许", False),
                     ("它没有给出任何解决办法", False)],
         "explain": "把事说小，通常会让对方把话收回去。换成先复述一小句，往下才有余地。<strong>错因提醒：</strong>常见错误是误认为讲自己的经历能让对方好受，其实那常常把话头转到自己身上。"},
        {"q": "关于「先听」，下面哪种理解更合适？",
         "options": [("先听就是不说话，也不能给任何建议", False),
                     ("先听完，再问他愿不愿意听你的想法——顺序换一下就好", True),
                     ("先给出方案，再听他补充", False)],
         "explain": "给建议不是错，抢在他讲完之前给才是。<strong>错因提醒：</strong>容易把「先听」搞混成「不能给建议」，于是明明有话也不说，反而让对方觉得你在敷衍。"},
        {"q": "同学说他连着两个星期吃不下、睡不着，还越来越瘦。下面哪种做法更合适？",
         "options": [("继续陪着他，等他自己想说的时候再说", False),
                     ("告诉他你会去找老师或家长，可以一起去找更好", True),
                     ("答应他绝对不告诉任何人", False)],
         "explain": "时间够久、已经影响到吃饭和睡觉，这两条都碰到了，就该交给能处理它的人。<strong>错因提醒：</strong>误认为替对方保密才是讲义气，结果常让一件本来可以早点处理的事拖得更久。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "fb", 10, "synthesis", "综合任务：互评改写台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">五句在小组里很常听到的话，每句选出那个能接着往下做的说法。留意哪一种会让对方愿意再改一次。</p>
        <div class="lab-panel" id="fb-stage"></div>
        <p class="result warn" id="fb-out" style="display:none;margin-top:12px"></p>
        <div class="inner-card">
          <p><strong>写下来，留给自己：</strong></p>
          <p style="color:var(--muted)">给最近一次合作里的一位组员，写一句真实的互评：哪一部分帮到了我、哪一处我跟不上、下一步我建议怎么改。</p>
          <textarea id="syn-answer" rows="3" placeholder="哪一部分帮到了我……哪一处我跟不上……下一步我建议……" style="margin-top:8px"></textarea>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🤝</span><div><strong>还有一件事想告诉你：</strong>如果你自己这段时间也觉得撑不住，不必等到别人来问你——找一位你信得过的同学、家长或者老师说一句，也是照顾自己的方式。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，看看方法还在不在", TTS["posttest"], [
        {"q": "晚自习后，同学在走廊跟你说：我真的不知道该怎么办了。这时更合适的第一步是：",
         "options": [("先停一下，说一句听起来你这两天很不好过，再问他要不要说说", True),
                     ("马上把他最近可能做得不对的地方一条条指出来", False),
                     ("告诉他别想太多，睡一觉就好了", False)],
         "explain": "先接住，再问要不要——把决定权交给他。<strong>错因提醒：</strong>常见错误是误认为必须马上给出方案才算帮上忙，其实很多时候他只差一个能把话说出来的人。"},
        {"q": "小组里有一位同学三次碰头都没到，任务后天要交。下面哪种做法更合适？",
         "options": [("把剩下的都自己做完，以后不再跟他一组", False),
                     ("跟大家说清现在缺哪一块、还差多少时间，再商量怎么办，必要时跟老师说明", True),
                     ("在小组群里说他这个人就是靠不住", False)],
         "explain": "说清事实和时间，是让活能往前走的第一步。<strong>错因提醒：</strong>容易把「说清情况」搞混成「告状」——前者说的是那部分活，后者说的是那个人。"},
        {"q": "你发现同学最近状态一直不好，还说过不想来学校。你打算怎么做？",
         "options": [("先陪他说说话，同时告诉他你要去找班主任或家长，可以一起去找更好", True),
                     ("答应他绝对不说出去，自己慢慢劝", False),
                     ("当作没听见，怕自己多事", False)],
         "explain": "陪伴和转给大人可以同时做，先说不等于出卖。<strong>错因提醒：</strong>误认为只有对方同意才能告诉老师，可有些事等不到他同意；先保证他有人帮，再解释你为什么说。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把这件事讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>先听再说</strong>：不急着给建议，不把事情说小，不急着比惨。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>该转就转</strong>：时间久了、影响到吃饭睡觉上课、涉及安全，就交给老师或家长，转之前先说一声。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>合作两件事</strong>：分工写清时间和交付，互评只说那部分活，不说那个人。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgb(var(--warm-rgb) / .45)">
          <p style="margin:0"><strong>回到开头那个时刻：</strong>朋友说他考砸了，话到嘴边停住的时候，你不必想出一句完美的话。先说一句听起来你挺难受的，再问他要不要说说——门就还开着。</p>
        </div>
        <div class="inner-card">
          <p><strong>记忆锚点：</strong>三句话帮你记住——<strong>先接住、再问要不要、扛不住就找人</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「接住、要不要、找人」这三个词，说说你上一次本来可以怎么回应一个来找你说话的同学。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写下三种好意却帮不上的回应，各用一句话说明它为什么帮不上。",
            "写出「先听」的三个动作，每个动作用一句话说清怎么做。",
            "写出什么时候该把事情告诉老师或家长的三条判断线。",
        ],
        [
            "找一个最近真实发生过的情境，写出两种回应，再写出它们分别可能把对话带到哪里。",
            "给一次小组合作写一份分工表：四块活、每块的时间、每块交给谁。",
        ],
        [
            "在一次真实的小组合作里，试着按分工四问分一次活，结束时用互评三句式说一次反馈，一周后回看对方的反应。",
            "把「先接住、再问要不要、扛不住就找人」讲给一位同学听，再用他的一件真事一起练一次，注意只改一句话就够。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-h-g11-peer-support",
    "node_id": "psych-h-g11-peer-support",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "high",
    "stage_cn": "高中",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 高中",
    "title": "同伴支持与合作学习：听他说完，再一起把事做完",
    "name_en": "Peer Support and Cooperative Learning",
    "grade": 11,
    "grade_cn": "高二",
    "domain": "interpersonal",
    "domain_cn": "人际交往",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向高二学生的同伴支持与合作学习课：先讲支持从听开始——认出三种好意却帮不上的回应（急着给建议、把事情说小、急着比惨），并练先听的三个动作；再用核心模拟「想帮忙时怎么说」对比台，把同一个情境的两种回应并排摆开，看它们分别把后面的对话带到哪里；接着讲有些情形不该由同伴一个人扛——时间、程度、安全三条判断线，并用「什么时候必须转给大人」判断台做八个情形的判断；最后用「互评改写台」练合作学习里的互评说法。全课明确写出陪伴有它的边界、转给大人不是不义气，语气温和、不评判、不贴标签，不出现任何诊断性表述。",
    "tags": ["同伴支持", "倾听", "什么时候找大人", "合作学习", "分工与互评", "高二"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 高中》人际交往——培养人际沟通能力，在合作学习中建立支持性同伴关系；促进积极情感反应和体验。",
    "hero_question": "想帮上忙，和真的帮上忙，中间差了什么？",
    "hero_alt": "同伴支持与合作学习知识结构图三栏：先听、怎么说、什么时候交给大人",
    "hero_caption": "先听 · 恰当回应 · 什么时候交给大人——再加上合作学习里的分工与互评",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个最贴近你最近状态的困惑，后面的内容都会围着它展开。",
    "anchor_choices": [
        {"t": "朋友难受的时候我该说什么？", "d": "想安慰又怕说错话，干脆不开口", "v": "朋友难受的时候我该说什么"},
        {"t": "什么时候该找老师或家长？", "d": "怕被说成打小报告，又担心不说会出事", "v": "什么时候该找老师或家长"},
        {"t": "小组合作总有人不出力怎么办？", "d": "每次都自己做完，心里堵得慌", "v": "小组合作总有人不出力怎么办"},
        {"t": "怎么给同伴提意见才不伤关系？", "d": "想说真话，又怕说完就生分了", "v": "怎么给同伴提意见才不伤关系"},
    ],
    "objectives": [
        "能说出三种好意却帮不上的回应，并各自改成一句能接得住的话",
        "会按先听再说的顺序，为同一个情境写出两种回应，并比较它们分别把人带到哪里",
        "能说出什么时候必须把事情告诉老师或家长，并知道转之前该怎么说",
        "能给一次小组合作做分工与互评，把话说成能接着做下去的那一种",
    ],
    "objectives_plain": [
        "能说出三种好意却帮不上的回应，并各自改成一句能接得住的话",
        "会按先听再说的顺序，为同一个情境写出两种回应，并比较它们分别把人带到哪里",
        "能说出什么时候必须把事情告诉老师或家长，并知道转之前该怎么说",
        "能给一次小组合作做分工与互评，把话说成能接着做下去的那一种",
    ],
    "standards": [
        {"content": "培养人际沟通能力，在合作学习中建立支持性同伴关系",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 人际交往"},
        {"content": "促进积极情感反应和体验",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》高中 · 人际交往"},
    ],
    "prereqs": ["psych-h-g11-exam-wellness"],
    "prereqs_name": "考试心理与身心健康",
    "prereqs_meta": "psych-h-g11-exam-wellness",
    "leads_to": ["psych-h-g12-career-choice"],
    "next_meta": "psych-h-g12-career-choice",
    "section_images": ["assets/psych-h-g11-peer-support-fig1.webp", "assets/psych-h-g11-peer-support-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "想帮上忙，和真的帮上忙之间差了点什么——这个问题先放在心里往下看。",
        "problem-anchor": "先定一个小目标：这节课结束时，你有一句能接得住的话和一条转给大人的判断线。",
        "objectives": "看清四件事：三种帮不上的回应、先听再说、什么时候转给大人、分工与互评。",
        "pretest": "凭平时的习惯选就好，不打分。前测只是帮你看清自己现在习惯怎么回应别人。",
        "module-1": "三种帮不上的回应：急着给建议、把事情说小、急着比惨。",
        "lab-1": "同一个情境的两种回应都点开，比较它们把对话带到哪里。",
        "module-2": "三条判断线：时间、程度、安全。碰到一条，就该交给能处理它的人。",
        "lab-2": "八个情形各选一个做法，全部判断完会看到一段小结。",
        "worked-example": "五步：分活、问三句、中途碰头、互评三句式、有人没交怎么办。",
        "conceptest-1": "三个选项里藏着最常见的几个误解，选完请把每条解释读一遍。",
        "synthesis": "五句互评说法各选一句，全部选完会看到一段小结。",
        "posttest": "一段聊天、一次小组合作、一次要不要找老师，三个新情境看看方法还在不在。",
        "summary": "记住三句：先接住，再问要不要，扛不住就找人。",
        "homework": "三层练习，前两层做完就算通关，第三层留给愿意更进一步的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给一个最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是高中「人际交往」板块里长期空缺的一课。设计上不讲大道理，只练同学之间最用得上的两件事。核心模拟是「想帮忙时怎么说」对比台——四个真实情境（朋友说考砸了、同学说跟家里吵架、同桌说反正也没用、组员说不想去上课），每个情境把两种回应并排摆开，点开就能看到对方可能的感受和后续；第二个台子是「什么时候必须转给大人」判断台，八个情形逐一判断是先陪着说还是要找老师或家长，落点是时间、程度、安全三条判断线；综合任务用「互评改写台」把五句常见的伤人说法改成能接着往下做的那一句。全课明确写出陪伴有它的边界、转给大人不是不义气，语气温和、不评判、不贴标签。",
    "plan_table": """| 1 | cover | 同伴支持与合作学习：听他说完，再一起把事做完 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：同伴开口的时候，你习惯怎么接？ | 起·前测（暴露现有习惯） |
| 5 | concept | 支持从「听」开始，不是从给办法开始 | 承·概念一（三种帮不上的回应 + 三个动作） |
| 6 | interactive | 核心模拟：想帮忙时怎么说——对比台 | 承·核心模拟（情境 × 两种回应 → 感受与后续） |
| 7 | concept | 有些情形，不该由同伴一个人扛 | 承·概念二（时间 / 程度 / 安全 三条线） |
| 8 | interactive | 判断台：什么时候必须转给大人？ | 承·练习台（八种情形 → 先陪 / 转给大人） |
| 9 | concept | 例题示范：一次小组合作，从卡住到推进 | 转·重难点突破（分工五步 + 互评三句式） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：互评改写台 | 合·互评改写（迁移应用） |
| 12 | quiz | 后测：换几个新情境，看看方法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把这件事讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：先听、怎么说、什么时候交给大人 三栏\n- P5 三种帮不上的回应示意图（已生成）：三个圆角卡片配抽象几何符号\n- P7 三个判断线示意图（已生成）：沙漏、上升折线、警示三角三块并列\n- 若需补充：一张可打印的分工表空白模板、一张互评三句式提示卡",
}
