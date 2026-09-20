# -*- coding: utf-8 -*-
"""小学心理健康 · 认识自我与学习兴趣（G3）—— 补齐知识树「认识自我」空缺

学科语气（心理健康）：温和、不评判、不贴标签；不出现任何临床诊断词汇，不涉及自伤自杀。
三年级落点：把「我喜欢」和「我擅长」分成两条不一样的线，自己给一堆卡片归类，做出一张
"我的特点卡"——没有好坏，只有不同；再处理一条认知边界：别人说我笨，不等于我真的笨。

插图一律为中性简洁教学插画，不使用任何真实儿童照片风格人像。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g3-self-know-fig1.webp'
F2 = './assets/psych-e-g3-self-know-fig2.webp'

TTS = {
    "hero": "小朋友，这节课我们要做一件事：认识一下你自己。有的同学会说，我很普通啊，有什么好认识的。可你真的知道吗：你喜欢做什么，你做什么事情的时候心里是高兴的；你又擅长什么，做哪件事的时候你比别人顺一点。这两件事，常常是不一样的。今天我们会给你一堆小卡片，你自己来归类，最后做出一张属于你的特点卡。记住一句话就够了：这件事上，没有好坏，只有不同。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道自己喜欢什么，还是想知道自己擅长什么，或者你想弄清楚「喜欢」和「擅长」到底有什么不一样，再或者，你被别人的一句话说得心里不舒服，想知道该怎么办。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出两件我喜欢做的事，和两件我做得比较顺的事。第二，知道「喜欢」和「擅长」是两条不一样的线，不一样长很正常。第三，能把一堆卡片按自己的想法归类，做出一张自己的特点卡。第四，听到别人说自己不好的时候，能把它分成两半：一半说的是事情，一半是贴的标签，事情可以用，标签可以放下。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说一件很要紧的事：喜欢和擅长，是两条不一样的线。有的事我很喜欢，可现在还做不好，比如我很喜欢画画，但画出来的小动物总是不像；有的事我做得挺好，可心里没那么喜欢，比如我很会整理书包，但说不上有多开心。这两条线不一样长，是很正常的事。还有一件要紧的话：现在还不会，不等于永远不行，只是「还没有」。还没有学会，还没有试够次数，都只是「还没有」。",
    "lab-1": "现在请你当一次自己的小档案员。下面有十二张卡片，都是同学们写过的事。请你一张一张点，再点它应该进的那个筐：喜欢、擅长，或者还想试试。怎么放，你自己说了算，没有标准答案。放好以后，看看你的三个筐。",
    "module-2": "再说一件更要紧的事。有时候，别人会对我们说一句不好听的话，比如「你怎么这么笨」。这时候，请你把这句拆成两半来看。一半说的是事情：哪一道题、哪一次、哪一个小地方。事情是可以改的，改一改就好了。另一半是在给你贴标签，用一个词把你说成一整个人。标签不是事实，它只是别人的一句评价。别人说我笨，不等于我真的笨。",
    "lab-2": "现在请你当一次小侦探，我们来练一练这个分法。下面有六句话，都是同学可能听到的话。请你一句一句看：这句话说的是「这件事」，还是在说「我这个人」。点一句话，再点它应该进的那一半。",
    "worked-example": "我们一起来帮小语想一想。数学卷子发下来，小语错了两道题。同桌看了一眼，说了一句：你怎么这么笨啊。小语心里一下子沉下去，觉得自己什么都不行。第一步，她先把那句话听清楚：他说的是这两道题，还是我这个人呢。他用了笨这个词，这是在给我贴标签。第二步，她再看事实：两道题错在哪里。一道是没看清问题里问的是什么，一道是中间的步骤跳过去了。原来需要再看一遍的是这两道题。第三步，她找一件自己能做的小事：把这两道题抄下来，重新做一遍，标出刚才错在哪。第四步，她给自己换一句话：不是我很笨，而是这两道题我还没弄明白，我去把它们弄明白。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件事交给你。请你选三样：我最喜欢做的一件事、我喜欢它是因为什么、我还想去试试的一件事。三样选好，我就送给你一张「我的特点卡」。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现：我很喜欢但做不好的事、别人说我不如别人、还有我一直学不会的一件事，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住三句话。第一句，喜欢和擅长是两条不一样的线，一条长一条短，很正常。第二句，每个人身上都有别人没有的东西，没有好坏，只有不同。第三句，别人说我笨，不等于我真的笨——把话分成两半，事情可以改，标签可以放下。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写下两件我喜欢做的事，两件我做得比较顺的事。第二层能力应用，动手做：给你的特点卡配一张小画，画一画你最喜欢做那件事的样子。第三层迁移挑战，选做：做一张「还没有」的小清单，写下三件你现在还不会、但想去试试的事，一个月后再回头看。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 喜欢和擅长，是两条不一样的线", "lab-1": "动手一 我的十二张卡片",
    "module-2": "概念二 别人说我笨，不等于我真的笨", "lab-2": "动手二 他说的是这件事，还是我这个人",
    "worked-example": "例题讲解 小语的两道错题", "conceptest-1": "概念测试",
    "synthesis": "综合任务 做出我的特点卡", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：十二张卡片，自己归类（自由归类，不判对错） ──
BUCKETS = {
    "like": "我喜欢",
    "good": "我擅长",
    "trial": "还想试试",
}
BUCKET_NOTE = {
    "like": "做这件事的时候，你心里是高兴的。喜欢一件事，不一定要做得好，做着开心本身就已经够了。",
    "good": "这件事你做起来比别人顺一点，或者做完之后自己心里会说一句：我做到了。",
    "trial": "还没做过，或者只做过一两次，心里还想再往前走一步。放在这里也很好，它是一颗小种子。",
}
CARDS = [
    {"id": "k1", "t": "看关于动物的书",
     "note": "喜欢看书里的动物，常常会顺带记住很多动物的小知识——喜欢和擅长，常常是一起到来的。"},
    {"id": "k2", "t": "在纸上随便画点什么",
     "note": "随手画的时候，人是放松的。画得像不像，和喜不喜欢，是两件事。"},
    {"id": "k3", "t": "听别人讲以前的故事",
     "note": "愿意听别人讲，是一种很珍贵的能力：听得多的人，后来自己也有的讲。"},
    {"id": "k4", "t": "和同学一起打球",
     "note": "喜欢和人一起做的事，往往会越做越顺，因为有人陪着你练。"},
    {"id": "k5", "t": "把东西摆得整整齐齐",
     "note": "这件事你看一眼就知道该放哪里——这就是「擅长」常常给人的感觉：做起来不费力。"},
    {"id": "k6", "t": "记住只走过一次的路",
     "note": "有的本事自己不太当回事，其实别人做不到。你身上可能就有这样的本事。"},
    {"id": "k7", "t": "安慰不开心的同学",
     "note": "能注意到别人的心情，还愿意走过去，这是一件很难得的事。"},
    {"id": "k8", "t": "把一道数学题算对",
     "note": "做对的时候心里会「咚」一下。把这种感觉记下来，它是你继续做下去的动力。"},
    {"id": "k9", "t": "学一样乐器",
     "note": "还没试过的事，先放在这里就好。想试一试，本身就是一个很好的开始。"},
    {"id": "k10", "t": "站到前面给大家讲一件事",
     "note": "这一件可能现在还有点难。没关系，它可以先在「还想试试」里待着。"},
    {"id": "k11", "t": "自己做一个会动的小手工",
     "note": "想自己动手做点什么，是很值得保护的念头。找一个下午试试看。"},
    {"id": "k12", "t": "把一件事坚持做一个月",
     "note": "这一件不着急，先挑一件小的开始。坚持这件事，本来就是慢慢练出来的。"},
]

# ── 动手二：这句话说的是事情，还是在说我这个人 ──
SPLIT_SENTENCES = [
    {"id": "s1", "t": "这道题你算错了。", "half": "thing",
     "why": "它说的是「这道题」，说的是一个一个具体的题目。题目可以再看一遍，改一改就好了。"},
    {"id": "s2", "t": "你怎么这么笨。", "half": "label",
     "why": "「笨」是一个词，它被用来形容你这个人。这不是事实，只是一句评价。别人这样说，不等于你就是这样的。"},
    {"id": "s3", "t": "你这次朗读的声音有点小。", "half": "thing",
     "why": "它说的是「这一次」「声音」这个具体的地方。下一次把声音放大一点，这件事就变了。"},
    {"id": "s4", "t": "你什么都做不好。", "half": "label",
     "why": "「什么都」把一件小事扩大成了全部，还贴上了一个人的标签。这样的话，可以不听。"},
    {"id": "s5", "t": "你这几个字写得有点潦草。", "half": "thing",
     "why": "它说的是「这几个字」，范围很清楚。练习一下，字就会变整齐。"},
    {"id": "s6", "t": "你就是个懒的人。", "half": "label",
     "why": "「懒的人」是给整个人下的一个结论。一次没做，不等于你就是这样的人。"},
]
HALF_NAME = {"thing": "说的是这件事", "label": "说的是我这个人（贴了标签）"}

# ── 综合任务：我的特点卡（三栏各选一样） ──
MY_CARD = {
    "like": {
        "name": "① 我最喜欢做的一件事",
        "items": [
            {"id": "a1", "t": "读故事、看有意思的书"},
            {"id": "a2", "t": "画画、做手工"},
            {"id": "a3", "t": "运动，出一身汗"},
            {"id": "a4", "t": "观察小动物、小植物"},
        ],
    },
    "why": {
        "name": "② 我喜欢它，是因为",
        "items": [
            {"id": "b1", "t": "做的时候心里很安静"},
            {"id": "b2", "t": "做完会有一点「我做到了」的感觉"},
            {"id": "b3", "t": "可以和朋友一起做"},
            {"id": "b4", "t": "总有新的东西等着我去发现"},
        ],
    },
    "next": {
        "name": "③ 我还想去试试的一件事",
        "items": [
            {"id": "c1", "t": "学一样乐器"},
            {"id": "c2", "t": "站到前面给大家讲一件事"},
            {"id": "c3", "t": "自己做一个会动的小手工"},
            {"id": "c4", "t": "把一件事坚持做一个月"},
        ],
    },
}

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g3-self-know 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 我的十二张卡片：自由放进「我喜欢 / 我擅长 / 还想试试」三个筐，不判对错
   3) 他说的是这件事，还是我这个人：六句话分成两半 + 换一种说法
   4) 我的特点卡：三栏各选一样，拼成一张卡
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

  /* ---------- 2. 我的十二张卡片 ---------- */
  var CARDS = __CARDS_JSON__;
  var BNOTE = __BNOTE_JSON__;
  var BNAME = __BNAME_JSON__;
  var cardStage = document.getElementById('card-stage');
  if (cardStage) {
    var pickedK = null, placedK = {}, buckets = { like: [], good: [], trial: [] };
    var outK = document.getElementById('card-out');

    function cardById(id) {
      for (var i = 0; i < CARDS.length; i++) { if (CARDS[i].id === id) return CARDS[i]; }
      return null;
    }
    function countK() { return Object.keys(placedK).length; }
    function renderK() {
      document.querySelectorAll('[data-card]').forEach(function (b) {
        var k = b.dataset.card;
        b.classList.toggle('selected', k === pickedK);
        b.classList.toggle('done', !!placedK[k]);
        b.disabled = !!placedK[k];
      });
      ['like', 'good', 'trial'].forEach(function (bn) {
        var box = document.getElementById('bucket-' + bn);
        if (!box) return;
        box.innerHTML = '';
        buckets[bn].forEach(function (id) {
          var s = document.createElement('span');
          s.className = 'tag';
          s.textContent = cardById(id).t;
          box.appendChild(s);
        });
        if (!box.innerHTML) {
          box.innerHTML = '<span style="color:var(--muted);font-size:13px">还空着，也可以空着。</span>';
        }
        var lab = document.getElementById('bucket-lab-' + bn);
        if (lab) lab.textContent = '（' + buckets[bn].length + ' 张）';
      });
      document.getElementById('card-score').textContent = '已经放好 ' + countK() + ' / ' + CARDS.length + ' 张';
    }
    document.querySelectorAll('[data-card]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placedK[b.dataset.card]) return;
        pickedK = b.dataset.card;
        outK.className = 'result warn';
        outK.innerHTML = '<strong>你选的是：' + b.textContent + '</strong><br>它更像哪一类？放进去看看，怎么放你自己说了算。';
        renderK();
      });
    });
    document.querySelectorAll('[data-bucket]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedK) {
          outK.className = 'result warn';
          outK.textContent = '先在上面点一张卡片，再选筐。';
          return;
        }
        var bn = b.dataset.bucket;
        var c = cardById(pickedK);
        placedK[c.id] = bn;
        buckets[bn].push(c.id);
        var head = '<strong>' + c.t + ' → ' + BNAME[bn] + '</strong><br>';
        if (countK() === CARDS.length) {
          outK.className = 'result';
          outK.innerHTML = head + '十二张都放好了。<strong>看看你的三个筐：三边的卡片不一样多，这很正常。</strong>' +
            '没有好坏，只有不同——这三个筐合起来，就是你现在的样子。';
        } else {
          outK.className = 'result';
          outK.innerHTML = head + BNOTE[bn] + '<br><span style="color:var(--muted)">再想一想：' + c.note + '</span>';
        }
        pickedK = null;
        renderK();
      });
    });
    renderK();
  }

  /* ---------- 3. 他说的是这件事，还是我这个人 ---------- */
  var SENT = __SENT_JSON__;
  var HNAME = __HNAME_JSON__;
  var splitStage = document.getElementById('split-stage');
  if (splitStage) {
    var pickedS = null, placedS = {};
    var outS = document.getElementById('split-out');

    function sentById(id) {
      for (var i = 0; i < SENT.length; i++) { if (SENT[i].id === id) return SENT[i]; }
      return null;
    }
    function renderS() {
      document.querySelectorAll('[data-sent]').forEach(function (b) {
        var k = b.dataset.sent;
        b.classList.toggle('selected', k === pickedS);
        b.classList.toggle('done', !!placedS[k]);
        b.disabled = !!placedS[k];
      });
      var nS = Object.keys(placedS).length;
      document.getElementById('split-score').textContent = '已经分好 ' + nS + ' / ' + SENT.length + ' 句';
      ['thing', 'label'].forEach(function (h) {
        var box = document.getElementById('half-' + h);
        if (!box) return;
        box.innerHTML = '';
      });
      SENT.forEach(function (s) {
        if (!placedS[s.id]) return;
        var box = document.getElementById('half-' + s.half);
        var d = document.createElement('div');
        d.className = 'tag';
        d.style.display = 'block';
        d.style.margin = '4px 0';
        d.textContent = s.t;
        box.appendChild(d);
      });
      ['thing', 'label'].forEach(function (h) {
        var box = document.getElementById('half-' + h);
        if (box && !box.innerHTML) {
          box.innerHTML = '<span style="color:var(--muted);font-size:13px">还空着。</span>';
        }
      });
    }
    document.querySelectorAll('[data-sent]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placedS[b.dataset.sent]) return;
        pickedS = b.dataset.sent;
        outS.className = 'result warn';
        outS.innerHTML = '<strong>「' + b.textContent + '」</strong><br>读两遍，再想一想：它说的是这件事，还是在说我这个人？';
        renderS();
      });
    });
    document.querySelectorAll('[data-half]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickedS) {
          outS.className = 'result warn';
          outS.textContent = '先在上面点一句话，再选它属于哪一半。';
          return;
        }
        var s = sentById(pickedS);
        if (b.dataset.half !== s.half) {
          outS.className = 'result warn';
          outS.innerHTML = '<strong>再读一遍「' + s.t + '」。</strong>' + s.why +
            '<br><span style="color:var(--muted)">常见错误：容易把「说了一件事」和「给整个人下结论」搞混。看范围——它说的是一个具体的题、一次、一处，还是什么都算上了？</span>';
          return;
        }
        placedS[s.id] = s.half;
        var swap = '';
        if (s.half === 'label') {
          swap = '<br><span style="color:var(--muted)">可以换成这样说：把「你怎么这么笨」换成「这道题我们再看一遍」，听起来会不会好受一点？</span>';
        } else {
          swap = '<br><span style="color:var(--muted)">这样的话里面有一个能改的地方，找到它，就知道下一步做什么了。</span>';
        }
        var nS = Object.keys(placedS).length;
        if (nS === SENT.length) {
          outS.className = 'result';
          outS.innerHTML = '<strong>分好了。</strong>' + s.why + swap +
            '<br><strong>六句都分完了：事情可以改，标签可以放下。</strong>别人说我笨，不等于我真的笨。';
        } else {
          outS.className = 'result';
          outS.innerHTML = '<strong>放对了，它属于「' + HNAME[s.half] + '」。</strong>' + s.why + swap;
        }
        pickedS = null;
        renderS();
      });
    });
    renderS();
  }

  /* ---------- 4. 我的特点卡 ---------- */
  var MYC = __MYC_JSON__;
  var myStage = document.getElementById('mycard-stage');
  if (myStage) {
    var chosenM = {}, colsM = ['like', 'why', 'next'];
    var outM = document.getElementById('mycard-out');

    function txtM(col, id) {
      var arr = MYC[col].items;
      for (var i = 0; i < arr.length; i++) { if (arr[i].id === id) return arr[i].t; }
      return '';
    }
    function renderM() {
      colsM.forEach(function (col) {
        document.querySelectorAll('[data-mycard="' + col + '"]').forEach(function (b) {
          b.classList.toggle('selected', chosenM[col] === b.dataset.myId);
        });
        var slot = document.getElementById('mycard-pick-' + col);
        if (slot) {
          slot.textContent = chosenM[col] ? txtM(col, chosenM[col]) : '还没有选';
          slot.style.color = chosenM[col] ? 'var(--text)' : 'var(--muted)';
        }
      });
      var n = colsM.filter(function (c) { return chosenM[c]; }).length;
      document.getElementById('mycard-score').textContent = '特点卡完成 ' + n + ' / 3 项';
      if (n === 3) {
        outM.className = 'result';
        outM.innerHTML = '<strong>我的特点卡：</strong>我最喜欢做的一件事是「' + txtM('like', chosenM.like) +
          '」，我喜欢它，是因为' + txtM('why', chosenM.why) + '。我还想去试试「' + txtM('next', chosenM.next) +
          '」。<br><span style="color:var(--muted)">把这张卡念给同桌听，再请他说一句：我眼里你还有什么不一样的地方。</span>';
      } else {
        outM.className = 'result warn';
        outM.textContent = '三栏各选一样，特点卡就做好了。';
      }
    }
    colsM.forEach(function (col) {
      document.querySelectorAll('[data-mycard="' + col + '"]').forEach(function (b) {
        b.addEventListener('click', function () {
          chosenM[col] = b.dataset.myId;
          renderM();
        });
      });
    });
    renderM();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__CARDS_JSON__', json.dumps(CARDS, ensure_ascii=False))
             .replace('__BNOTE_JSON__', json.dumps(BUCKET_NOTE, ensure_ascii=False))
             .replace('__BNAME_JSON__', json.dumps(BUCKETS, ensure_ascii=False))
             .replace('__SENT_JSON__', json.dumps(SPLIT_SENTENCES, ensure_ascii=False))
             .replace('__HNAME_JSON__', json.dumps(HALF_NAME, ensure_ascii=False))
             .replace('__MYC_JSON__', json.dumps(MY_CARD, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "下面哪一句，说的是「擅长」这件事？",
         "options": [("我做数学题的时候，比别人快一点，做完了心里挺踏实", True),
                     ("我很喜欢画画，可是画出来总是不太像", False),
                     ("我很想学一样乐器，可还没开始学", False)],
         "explain": "「做起来比平时顺一点」更像擅长；「很喜欢」是喜欢；「还没开始」是还想试试。三件事都不一样，都很正常。"
                    "<strong>错因提醒：</strong>常见错误是把「喜欢」和「擅长」搞混——喜欢是心里高兴，擅长是做起来顺，它们常常不是同一件事。"},
        {"q": "同桌对你说了一句：这么简单的题你都不会。下面哪个想法更有帮助？",
         "options": [("他说的是这道题我还没弄明白，我再看一遍", True),
                     ("看来我真的很笨", False),
                     ("以后我再也不做题了", False)],
         "explain": "把这句话落回到具体的那道题上，你就知道下一步做什么了；把它接到「我这个人」身上，只会让人更没力气。"
                    "<strong>错因提醒：</strong>有人误认为「别人说我不好，就一定是我不够好」——别人的话是一句评价，不是一个事实。"},
        {"q": "有一件事我做得不太好，但我很喜欢。下面哪个做法更合适？",
         "options": [("继续做，喜欢就能一直做下去，慢慢会变好", True),
                     ("做不好就别做了，去做我做得好的事", False),
                     ("藏在心里，不让别人知道我做得不好", False)],
         "explain": "喜欢的事情本身就值得做，做着开心就是它的意义。做得久了，常常也会变好。"
                    "<strong>错因提醒：</strong>容易误认为「做不好就不该做」——「喜欢」不需要先通过考试才有资格继续。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "喜欢和擅长，是两条不一样的线", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">二年级的时候，我们已经认识过自己的心情，知道开心和不开心都可以说出来（And）；可是很多同学对自己的了解只停在一句「我很普通」，说不清自己到底喜欢什么、擅长什么（But）；所以这节课我们做一件具体的事——把「喜欢」和「擅长」分成两条线，再自己动手，做出一张属于你的特点卡（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">先说第一件事：<strong>喜欢</strong>说的是心里高不高兴，<strong>擅长</strong>说的是做起来顺不顺。它们<strong>常常不一样长</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>喜欢，但不那么擅长</strong></p>
            <p style="color:var(--muted)">我很喜欢画画，可画出来的小动物总是不太像。没关系——喜欢的事情，做着开心本身就已经够了。</p>
          </div>
          <div class="inner-card">
            <p><strong>擅长，但没那么喜欢</strong></p>
            <p style="color:var(--muted)">我很会整理书包，东西放得又快又齐，可要问我喜不喜欢，我也说不上来。这也是一种真实的样子。</p>
          </div>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先把两件事分开问：</strong>做这件事的时候，我心里高兴吗？这是「喜欢」。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再问第二句：</strong>我做起来比别人顺一点吗？做完会想说「我做到了」吗？这是「擅长」。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>最后加一句「还没有」：</strong>现在还不会，只是<strong>还没有</strong>学会，不是永远都不行。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="喜欢与擅长两条线示意图：一条线标注我喜欢做的事，另一条线标注我做得顺的事，两条线长度不同">
          <figcaption>示意图：「喜欢」和「擅长」是两条不一样的线，一条长一条短很正常；旁边还有一格写着「还没有」（教学示意图，中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「做得好的事才值得花时间，做不好的就没必要做」。其实喜欢的事情本身就值得做：做着开心，会让你更愿意一直做下去；一直做下去，常常也就慢慢做好了。<strong>做不好，不等于不该做。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "从小到大，一定有一些时刻你做一件事做得很投入，连时间都忘了。那些时刻里藏着你的兴趣，值得记下来。"},
    {"lens": "比较它", "text": "把你喜欢的事和你擅长的事各写三条，两条对着看。你会发现它们有的重叠，有的完全不一样——两种都很好。"},
    {"lens": "迁移它", "text": "这个分法到哪里都能用：选课外活动、挑小组任务、想以后做什么，都可以先问问自己这两句话。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>喜欢看的是心里，擅长的看的是手里——<strong>两条线不一样长，这就是我。</strong></div></div>
    ''', tag="概念一"))

    card_btns = "\n".join(
        f'            <button class="choice" data-card="{c["id"]}" style="text-align:left">{c["t"]}</button>'
        for c in CARDS
    )
    bucket_html = "\n".join(
        f'''            <button class="choice" data-bucket="{bn}" style="text-align:center">{BUCKETS[bn]}</button>'''
        for bn in ("like", "good", "trial")
    )
    bucket_boxes = "\n".join(
        f'''            <div class="sort-bin">
              <h4>{BUCKETS[bn]}<span id="bucket-lab-{bn}" style="color:var(--muted);font-weight:400"></span></h4>
              <div id="bucket-{bn}"><span style="color:var(--muted);font-size:13px">还空着，也可以空着。</span></div>
            </div>'''
        for bn in ("like", "good", "trial")
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：我的十二张卡片，自己来归类", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一张卡片，再点它应该进的筐。<strong>怎么放你自己说了算，这里没有标准答案</strong>，放错了也不会扣分。</p>
        <div class="lab-panel" id="card-stage">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 十二张卡片（点一张）</div>
          <div class="grid grid-2" id="card-bank">
{card_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它更像哪一类（点一个筐）</div>
          <div class="grid grid-3">
{bucket_html}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 我的三个筐</div>
          <div class="sort-bins" style="grid-template-columns:1fr">
{bucket_boxes}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">归类进度</span><span class="v" id="card-score">已经放好 0 / 12 张</span></div>
          </div>
          <p class="result warn" id="card-out" style="margin-top:12px">先在上面点一张卡片。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌱</span><div><strong>看看你的三个筐：</strong>三边的卡片不一样多，很正常。<strong>没有好坏，只有不同</strong>——这三个筐合起来，就是你现在的样子。</div></div>
    ''', tag="动手一", bloom="apply"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "别人说我笨，不等于我真的笨", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">有时候，别人会对我们说一句不好听的话。这时候，请把这句<strong>拆成两半</strong>来看。</p>
        <div class="grid grid-2">
          <div class="inner-card" style="border-left:4px solid var(--brand-2)">
            <p><strong>一半说的是事情</strong></p>
            <p style="color:var(--muted)">「这道题你算错了」「你这次朗读声音有点小」——它指向一个具体的题、一次、一处。<strong>事情是可以改的</strong>，改一改就好了。</p>
          </div>
          <div class="inner-card" style="border-left:4px solid var(--warm)">
            <p><strong>一半是在贴标签</strong></p>
            <p style="color:var(--muted)">「你怎么这么笨」「你什么都做不好」——它用一个词把你说成<strong>一整个人</strong>。标签不是事实，它只是别人的一句评价。</p>
          </div>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先分开：</strong>他说的是一件事，还是我这个人？看范围大不大，就知道是哪一半。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再看事实：</strong>哪一道题？哪一次？具体是哪一处？把范围缩小，你就知道下一步做什么。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>换一句自己能用的话：</strong>把「我很笨」换成「这两道题我还没弄明白，我去弄明白它」。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="一句话拆成两半示意图：左半写着说的是这件事，右半写着说的是我这个人贴的标签">
          <figcaption>示意图：别人说的一句话可以拆成两半——「说的是这件事」可以改，「说的是我这个人」是贴的标签，可以放下（教学示意图，中性简洁插画）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「听到不好听的话，就必须马上生气地反驳回去，或者干脆承认自己就是不行」。其实还有第三条路：<strong>先在心里把它分成两半</strong>——事情拿来用，标签可以放下。你不用当场证明什么，只要知道自己不是那句话说的样子。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "听到不好听的话，心里会发紧、发沉，这是很正常的反应。先承认这份不舒服，再慢慢处理那句话，比马上反驳更容易。"},
    {"lens": "拆开它", "text": "拿一张纸，把听到的那句话写在中间，左边写「它说的是哪一件事」，右边写「它给我贴了什么词」。写出来，两半就分开了。"},
    {"lens": "迁移它", "text": "这个办法也可以用在你自己身上：你对自己说「我数学就是不行」的时候，也停一下——是「这道题不行」，还是「我这个人不行」？"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>话分两半看，事情可以改，标签可以放——<strong>别人说我笨，不等于我真的笨。</strong></div></div>
    ''', tag="概念二"))

    sent_btns = "\n".join(
        f'            <button class="choice" data-sent="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in SPLIT_SENTENCES
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：他说的是这件事，还是我这个人", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一句话，再点它属于哪一半。<strong>判定的时候看范围</strong>：它说的是一个具体的题、一次、一处，还是把什么都算上了？</p>
        <div class="lab-panel" id="split-stage">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 六句话（点一句）</div>
          <div class="grid" id="split-bank">
{sent_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 它属于哪一半（点一下）</div>
          <div class="grid grid-2">
            <button class="choice" data-half="thing" style="text-align:center">说的是这件事</button>
            <button class="choice" data-half="label" style="text-align:center">说的是我这个人</button>
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>分好的结果</strong></p>
            <p style="margin:6px 0 4px"><strong>说的是这件事</strong>（可以改）</p>
            <div id="half-thing"><span style="color:var(--muted);font-size:13px">还空着。</span></div>
            <p style="margin:10px 0 4px"><strong>说的是我这个人</strong>（贴的标签）</p>
            <div id="half-label"><span style="color:var(--muted);font-size:13px">还空着。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分句进度</span><span class="v" id="split-score">已经分好 0 / 6 句</span></div>
          </div>
          <p class="result warn" id="split-out" style="margin-top:12px">先在上面点一句话。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>拿不准的时候问自己一句：</strong>这句话说的是<strong>一个具体的题、一次、一处</strong>吗？是，它就属于「这件事」；如果它把什么都算上了，就是「贴标签」。</div></div>
    ''', tag="动手二", bloom="apply"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小语的两道错题", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>数学卷子发下来，小语错了两道题。同桌看了一眼，说了一句：你怎么这么笨啊。小语心里一下子沉下去，觉得自己什么都不行。请你陪她走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先分开这句话：</strong>他说的是这两道题，还是我这个人？他用了「笨」这个词——这是在给整个人贴标签。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再看事实：</strong>两道题错在哪里？一道是没看清问题里问的是什么，一道是中间的步骤跳过去了。需要再看一遍的，是这两道题。</div></div>
          <div class="step"><span class="n">3</span><div><strong>找一件自己能做的小事：</strong>把这两道题抄下来，重新做一遍，标出刚才错在哪一步。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>换一句自己能用的话：</strong>不是「我很笨」，而是「这两道题我还没弄明白，我去把它们弄明白」。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「被说了不好听的话，只有两种选择：要么认了，要么吵回去」。小语这四步里走了第三条路——<strong>她既没认，也没吵，只是把那句话拆开，把能用的那半拿走了。</strong>这样，她省下了吵架的力气，用在了两道题上。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>你有没有听过一句让你心里不舒服的话？把它写在纸上，左边写「它说的是哪一件事」，右边写「它给我贴了什么词」，再换一句你能用的话。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "下面哪一句说的是「这件事」，不是给我整个人下结论？",
         "options": [("你这次朗读的时候，中间有两句没读清楚", True),
                     ("你就不是朗读的料", False),
                     ("你什么都做不好", False)],
         "explain": "「这次」「有两句」把范围说得很清楚，这就是在说事情，改起来也知道从哪里下手。"
                    "<strong>错因提醒：</strong>常见错误是把「这一次没做好」和「我这个人不行」搞混——一件事的结果，不等于对一个人的评价。"},
        {"q": "我很喜欢做手工，可是做出来的东西总是不太好看。下面哪个想法更有帮助？",
         "options": [("喜欢就继续做，多做几次手会越来越熟", True),
                     ("做得不好看，说明我不适合做手工", False),
                     ("以后做手工的时候不让别人看见", False)],
         "explain": "喜欢是心里的事，好不好看是手上的事，两件事会一起变，但不用同时到达。"
                    "<strong>错因提醒：</strong>容易误认为「做不好就等于没天赋」——现在还不熟，只是「还没有」练够次数。"},
        {"q": "有一个同学说自己很想学游泳，可是一直没学过。你会怎么对他说？",
         "options": [("没学过很正常，可以先去试一次，看看喜不喜欢", True),
                     ("你连游泳都不会，太落后了", False),
                     ("那你肯定学不会了", False)],
         "explain": "还没做过的事，只是「还想试试」，属于第三个筐，它是一颗小种子，不是缺点。"
                    "<strong>错因提醒：</strong>有人误认为「没做过等于不行」——把「还没做」当成「做不到」，会白白错过很多好玩的事。"}
    ], tag="概念测试"))

    mycard_blocks = []
    for col in ("like", "why", "next"):
        btns = "\n".join(
            f'              <button class="choice" data-mycard="{col}" data-my-id="{it["id"]}" style="text-align:left">{it["t"]}</button>'
            for it in MY_CARD[col]["items"]
        )
        mycard_blocks.append(f'''          <div class="inner-card">
            <p><strong>{MY_CARD[col]["name"]}</strong>　<span style="color:var(--muted);font-size:13px">已选：</span><span id="mycard-pick-{col}" style="color:var(--muted)">还没有选</span></p>
            <div class="grid" style="margin-top:8px">
{btns}
            </div>
          </div>''')
    mycard_html = "\n".join(mycard_blocks)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：做出我的特点卡", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三栏各选一样，就做好了你的<strong>特点卡</strong>。这张卡不需要和别人比，它只写你现在的样子。</p>
        <div class="lab-panel" id="mycard-stage">
{mycard_html}
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">特点卡进度</span><span class="v" id="mycard-score">特点卡完成 0 / 3 项</span></div>
          </div>
          <p class="result warn" id="mycard-out" style="margin-top:12px">三栏各选一样，特点卡就做好了。</p>
        </div>
        <div class="inner-card">
          <p><strong>再写一句给自己的话：</strong></p>
          <p style="color:var(--muted)">这句话的开头是「我身上的这几样，没有好坏，只有不同」，把它写完。</p>
          <textarea id="syn-answer" rows="3" placeholder="我身上的这几样，没有好坏，只有不同。比如……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "我有一件很喜欢的事，可是做得一直不太好，同桌说：你还是别做了。下面哪个做法更合适？",
         "options": [("继续做，也听一听同桌的建议，看看哪里可以改一改", True),
                     ("从此以后再也不做了", False),
                     ("觉得同桌是在看不起我，以后不理他", False)],
         "explain": "喜欢的事情本来就值得继续；别人的建议里如果有能用的那一半，就拿来用，剩下的可以放下。"
                    "<strong>错因提醒：</strong>常见错误是把「别人给的一个建议」当成「对我整个人的否定」——先看看他说的是哪件事，再决定要不要改。"},
        {"q": "妈妈说：你看看人家，样样都比你强。听到这句话，下面哪个想法更有帮助？",
         "options": [("我和他不一样，他有他的长处，我也有我的", True),
                     ("我确实什么都不如别人", False),
                     ("那我以后就照着他的样子做", False)],
         "explain": "人和人本来就不一样，「哪里都比」不是一个站得住的比法。找到你自己的那两三条，比名次更实在。"
                    "<strong>错因提醒：</strong>有人误认为「比不过别人就说明我不好」——把「比较」和「评价自己」分开，心里会稳得多。"},
        {"q": "有一件事我试了好几次还是不会，心里有点想放弃。下面哪个做法更合适？",
         "options": [("先放一放，过些天再试一次，也可以请人教教我", True),
                     ("试了几次都不会，那我一辈子都不行了", False),
                     ("对自己说：我就是太笨了", False)],
         "explain": "现在不会，只说明「还没有」学会。放一放、换个人请教、把步骤再拆小一点，都是继续往前走的方式。"
                    "<strong>错因提醒：</strong>容易把「还没有学会」说成「永远学不会」——加一个「还」字，事情就不一样了。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清认识自己这件事", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>喜欢和擅长是两条线：</strong>喜欢看的是心里，擅长的看的是手里，不一样长很正常。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>没有好坏，只有不同：</strong>我身上的每一样，都是我的一部分，不用拿去和别人比。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>话要分两半看：</strong>说的是事情，就可以改；贴的是标签，就可以放下。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>每个人的节奏不一样。有的同学很早就知道自己喜欢什么，有的同学要试很多次才知道——这两种都正常，慢慢找也没关系。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「喜欢、擅长、还没有」这三个词，说一说你自己。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画一画</strong>你的三个筐，把卡片写成小纸条贴进去，放在书桌旁边。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写下两件我喜欢做的事，和两件我做得比较顺的事。",
            "写下三件我现在还不会、但想去试试的事（用「还没有」开头）。",
        ],
        [
            "给同桌讲一讲你的三个筐：哪一样最多，哪一样最少，你是怎么想的。",
            "把「话分两半」的办法用在一件事上：记下你听到的一句不好听的话，写出它说的是哪件事、贴的是什么标签。",
        ],
        [
            "给你的特点卡配一张小画，画一画你最喜欢做那件事的样子，贴在书桌前。",
            "采访家里的一位长辈：他小时候最喜欢做什么，现在擅长做什么，这两件事一样吗？写下来讲给同学听。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g3-self-know",
    "node_id": "psych-e-g3-self-know",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "认识自我与学习兴趣",
    "name_en": "Knowing Myself and My Learning Interests",
    "grade": 3,
    "grade_cn": "三年级",
    "domain": "self-awareness",
    "domain_cn": "认识自我",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学三年级的认识自我课：先把「喜欢」和「擅长」分成两条不一样的线，再用十二张卡片自己做一次归类，放进「我喜欢 / 我擅长 / 还想试试」三个筐，最后拼出一张属于自己的特点卡；再处理一条重要的认知边界——把别人说的一句话分两半：说的是这件事就可以改，说的是我这个人只是贴的标签。全课不比较、不评判、不贴标签，落点是一句「没有好坏，只有不同」。",
    "tags": ["认识自我", "学习兴趣", "没有好坏只有不同", "认知边界", "三年级"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中年级》认识自我与学习兴趣——帮助学生了解自我，认识自我；初步培养学生的学习能力，激发学习兴趣和探究精神，树立自信，乐于学习。",
    "hero_question": "你知道自己喜欢什么、擅长什么吗？这两件事，常常不一样。",
    "hero_alt": "认识自我与学习兴趣知识结构图：喜欢和擅长是两条不一样的线、我的三个筐、话要分两半看 三栏",
    "hero_caption": "认识自我与学习兴趣：喜欢与擅长 · 没有好坏，只有不同 · 别人说我笨，不等于我真的笨",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "我喜欢什么？", "d": "哪件事我做起来心里是高兴的", "v": "我喜欢什么"},
        {"t": "我擅长什么？", "d": "哪件事我做起来比别人顺一点", "v": "我擅长什么"},
        {"t": "「喜欢」和「擅长」有什么不一样？", "d": "为什么有的我很喜欢却做不好", "v": "喜欢和擅长有什么不一样"},
        {"t": "别人说我不好，心里不舒服怎么办？", "d": "那句话说的是我这个人吗", "v": "别人说我不好心里不舒服怎么办"},
    ],
    "objectives": [
        "能说出两件我喜欢做的事，和两件我做得比较顺的事",
        "知道「喜欢」和「擅长」是两条不一样的线，不一样长很正常",
        "能把一堆卡片按自己的想法归类，做出一张自己的特点卡",
        "听到别人说自己不好的时候，能把它分成「说的是这件事」和「贴的标签」两半",
    ],
    "objectives_plain": [
        "能说出两件我喜欢做的事，和两件我做得比较顺的事",
        "知道「喜欢」和「擅长」是两条不一样的线，不一样长很正常",
        "能把一堆卡片按自己的想法归类，做出一张自己的特点卡",
        "听到别人说自己不好的时候，能把它分成「说的是这件事」和「贴的标签」两半",
    ],
    "standards": [
        {"content": "帮助学生了解自我，认识自我",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中年级 · 认识自我"},
        {"content": "初步培养学生的学习能力，激发学习兴趣和探究精神，树立自信，乐于学习",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中年级 · 学习辅导"},
    ],
    "prereqs": ["psych-e-g2-emotion-basics"],
    "prereqs_name": "情绪体验与自我控制",
    "prereqs_meta": "psych-e-g2-emotion-basics",
    "leads_to": ["psych-e-g3-social-role"],
    "next_meta": "psych-e-g3-social-role",
    "section_images": ["assets/psych-e-g3-self-know-fig1.webp", "assets/psych-e-g3-self-know-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "喜欢看的是心里，擅长看的是手里——这两条线常常不一样长。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出自己的一两样特点。",
        "objectives": "四件事：说出喜欢与擅长、知道两条线不一样、做出特点卡、把别人的话分两半。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "喜欢是心里高兴，擅长是做起来顺；现在还不会，只是「还没有」。",
        "lab-1": "十二张卡片自己归类，怎么放你说了算，这里没有标准答案。",
        "module-2": "一句话拆两半：说的是事情就可以改，说的是我这个人只是贴的标签。",
        "lab-2": "看范围：它说的是一个具体的题、一次、一处，还是把什么都算上了？",
        "worked-example": "小语四步：分开这句话、看事实、找一件能做的事、换一句自己能用的话。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "三栏各选一样，做好你的特点卡，再念给同桌听一遍。",
        "posttest": "出现了「喜欢却做不好」「和别人比」「试了几次还不会」，看看你能不能用上今天的办法。",
        "summary": "三句话：喜欢和擅长是两条线、没有好坏只有不同、话要分两半看。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「认识自我」在三年级的空缺，正对课标「帮助学生了解自我，认识自我」与「激发学习兴趣和探究精神，树立自信，乐于学习」。三年级学生说「我不行」的时候，其实往往分不清两件事：一件是「我不喜欢」，另一件是「我不擅长」；也很容易把别人的一句评价，听成对自己的整个结论。所以全课只做两件能落地的事——先把「喜欢」和「擅长」分成两条不一样的线，用十二张卡片自己做一次归类，放进「我喜欢 / 我擅长 / 还想试试」三个筐，最后拼出一张属于自己的特点卡（可操作的自我认识）；再把别人说的一句话拆成两半，认清「说的是这件事」和「说的是我这个人」的区别，处理「别人说我笨」这条认知边界。两个互动台子都能真的操作：一个是十二张卡片的自由归类台，一边放卡片一边实时计数，十二张放完给出「三边不一样多很正常」的总结；一个是「他说的是这件事，还是我这个人」的六句分半台，判错会给出范围判据的错因提示，并附换一种说法。综合任务把「最喜欢的一件事 + 为什么喜欢 + 还想试试的一件事」拼成一张特点卡。插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像；全课不出现任何临床诊断词汇，不比较、不贴标签、不评判。",
    "plan_table": """| 1 | cover | 认识自我与学习兴趣 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 喜欢和擅长，是两条不一样的线 | 承·概念一（把喜欢与擅长分开） |
| 6 | interactive | 动手一：我的十二张卡片，自己来归类 | 承·可操作的自我认识（三个筐 + 实时计数） |
| 7 | concept | 别人说我笨，不等于我真的笨 | 承·概念二（认知边界处理） |
| 8 | interactive | 动手二：他说的是这件事，还是我这个人 | 承·分半操作（六句话 + 换一种说法） |
| 9 | concept | 例题示范：小语的两道错题 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：做出我的特点卡 | 合·迁移应用（特点卡拼装） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清认识自己这件事 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：喜欢和擅长是两条不一样的线 / 我的三个筐 / 话要分两半看 三栏\n- P5 两条线示意图（已生成）：一条线标注我喜欢做的事，另一条线标注我做得顺的事，长度不同，旁边一格写着「还没有」，附中文标注\n- P7 一句话拆两半示意图（已生成）：左半「说的是这件事」，右半「说的是我这个人（贴的标签）」，附中文标注\n- 三张图均为中性简洁教学插画，人物只用简单几何图形，不使用任何真实儿童照片或可识别肖像\n- 若需补充：学生自己的特点卡实物照片（需本人同意后才可使用）",
}
