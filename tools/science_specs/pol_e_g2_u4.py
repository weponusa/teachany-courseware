# -*- coding: utf-8 -*-
"""小学道德与法治 · 我爱我们的祖国（G2）—— 补齐知识树课标空缺节点

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断；结论落在「应该怎么做、为什么」，
不做道德说教，也不做法条背诵。

表述口径（本课严格执行）：
  · 国旗、国歌、国徽只用「文字」准确、庄重地表述（国旗是五星红旗；国歌是《义勇军进行曲》；
    国徽是国家的象征），并落实行为要求：升国旗时肃立、行注目礼、认真唱国歌。
    插图一律不绘制国旗、国徽图形，也不绘制任何地图与国界线。
  · 领土表述严格准确：台湾是中国不可分割的一部分；中国香港、中国澳门是中国的特别行政区，
    一律写「中国香港」「中国澳门」，绝不表述为独立国家。
  · 全课不涉及任何政治人物、政党与政府机构，只讲祖国的山水、文化、民族团结和国家象征的礼仪。
插图一律为中性简洁扁平插画，不使用真实人物照片。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g2-u4"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "小朋友，我们的祖国很大很大。同样是一月，最北边的地方已经盖着厚厚的白雪，最南边的海边还穿着短袖；西边是一望无际的草原和高高的雪山，东边是热闹的城市和忙忙碌碌的港口。这么大的一片地方，住着我们所有的亲人、同学和邻居。今天我们就一起看一看：我们的祖国有多大、有哪些不一样的样子；我们都是中国人，有哪些一样的节日和宝贝；还有，升国旗的时候，我们应该怎么做。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道祖国到底有多大、有哪些不一样的地方，还是想知道为什么说我们都是中国人；是想知道升国旗的时候应该怎么做，还是想知道我们可以为祖国做点什么。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出祖国很大，不同地方有不同样子，能举出两个例子。第二，知道我国有五十六个民族，大家都是中国人，要团结友爱。第三，能说出国旗是五星红旗、国歌是《义勇军进行曲》，知道升国旗时要肃立、行注目礼、认真唱国歌。第四，知道台湾是中国不可分割的一部分，中国香港、中国澳门是中国的特别行政区，愿意为祖国做一件力所能及的小事。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先来看祖国有多大。从最北边到最南边，要坐很久很久的车，坐飞机也要好几个小时。这么大的地方，每个地方的样子都不一样。最北边冬天很长，大雪能盖住房顶，人们滑冰、看冰灯；往南走，有河湖很多的地方，小河穿城而过，出门可以坐小船；再往西，是一望无际的草原，牛羊成群，远处有白色的蒙古包；还有地势很高的高原，山上有终年不化的雪，牦牛在高原上慢慢地走；最南边的海边，一年四季都很暖和，长着高高的椰子树。同样是祖国，样子这么多，这就是「美丽中国我们的家」。",
    "lab-1": "现在我们来玩一个配对的游戏。上面是六个地方的名字，下面是六段那里的样子。先点一个地方，再点它对应的样子。配对成功，会告诉你为什么那里是这个样子；配错了也没关系，再想一想就好。",
    "module-2": "接下来我们说第二件事：我们都是中国人。我们国家有五十六个民族，穿的衣服不一样、唱的歌不一样、过节的方式也不完全一样，但大家都是中国人，都是兄弟姐妹，要互相尊重、团结友爱。祖国还有很多共同的宝贝：过年的时候，不管在哪里，中国人家里都要贴春联、挂灯笼、吃团圆饭，红红火火；赛龙舟、包粽子、赏月亮，很多节日我们一起过。还有一些东西是国家的象征，要特别尊敬。国旗是五星红旗，国歌是《义勇军进行曲》，国徽是国家的象征。升国旗的时候，我们要肃立，也就是站直、不乱动；要行注目礼，眼睛看着国旗；还要认真唱国歌。国旗、国歌、国徽不能乱涂乱画，也不能拿来开玩笑，国家专门立了法来保护它们。最后再说清楚一件事：我们的祖国由很多地方组成，台湾是中国不可分割的一部分；中国香港和中国澳门是中国的特别行政区，和内地一样，都是中国的一部分。",
    "lab-2": "下面我们做一轮祖国知识小问答。一共五道题，每题选一个你认为正确的。选对了会告诉你为什么；选得不合适，会告诉你这样可能会有什么问题，还可以试试怎么想。",
    "worked-example": "我们一起来看看，升国旗的时候应该怎么做。第一步，听到国歌响起，立刻停下手里的事：不聊天、不打闹，先站住。第二步，站好，也就是肃立：身体挺直，手上不拿东西，不乱动。第三步，行注目礼：脸朝着国旗，眼睛认真看着国旗升上去。第四步，认真唱国歌：跟着大家一起唱，声音整齐，不哼不笑。这四步看起来很平常，可正是这四步，表达我们对国旗、对国歌、对祖国的尊敬。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "接下来请你当一次设计师，为祖国做一张名片。先写下你想对祖国说的一句话，再从四类元素里每一类挑一个，点一点，一张「祖国名片」就长出来了。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现国歌响起时你在做什么、班上来了一位说话口音不一样的新同学，还有关于祖国各地的问题，看看你能不能用上今天学到的。",
    "summary": "这节课我们记住四句话。第一句，美丽中国我们的家：祖国很大，北边下大雪，南边四季暖和，西边有草原和高原，各地样子都不一样。第二句，我们都是中国人：五十六个民族，大家都是中国人，要团结友爱；春节、端午、中秋，很多节日我们一起过。第三句，国家的象征要尊敬：国旗是五星红旗，国歌是《义勇军进行曲》，国徽是国家的象征；升国旗时肃立、行注目礼、认真唱国歌。第四句，我们的祖国由很多地方组成：台湾是中国不可分割的一部分，中国香港和中国澳门是中国的特别行政区，都是中国的一部分。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出祖国的两个地方，说说那里的样子有什么不一样；再说出升国旗时要做哪三件事。第二层能力应用，动手做：问一问家里人或者查一查书，找出两个关于祖国的知识，说给同学听；做一张自己的祖国名片。第三层迁移挑战，选做：找一张祖国各地的风景图片，说说那里的样子和气候有什么关系；再为祖国做一件小事，比如把国旗、国歌的礼仪教给比自己小的同学。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 美丽中国我们的家", "lab-1": "动手一 祖国各地风貌配对", "module-2": "概念二 我们都是中国人 · 国家象征",
    "lab-2": "动手二 祖国知识小问答", "worked-example": "例题讲解 升国旗的时候怎么做", "conceptest-1": "概念测试",
    "synthesis": "综合任务 做一张祖国名片", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：祖国各地风貌配对 —— 六个地方 ↔ 六段那里的样子 ──
PLACES = [
    {"id": "ne", "n": "东北", "f": "冬天很长，大雪盖住房顶，人们滑冰滑雪、看冰灯",
     "s": "这里的冬天又长又冷，雪很厚。雪和冰不只是天气，也成了人们生活的一部分——滑冰、看冰灯，都是这里的冬天特有的快乐。"},
    {"id": "jn", "n": "江南水乡", "f": "小河穿城而过，出门可以坐小船",
     "s": "这里河湖多、水多，所以桥多、船多。水多的地方，稻田也是一片一片的，鱼虾也格外多。"},
    {"id": "mg", "n": "内蒙古草原", "f": "一望无际的草原，牛羊成群，远处有白色的蒙古包",
     "s": "这里是一眼望不到边的草原。草多，就适合放牧牛羊；蒙古包方便拆和搬，适合在草原上生活。"},
    {"id": "hn", "n": "海南", "f": "一年四季都很暖和，海边长着高高的椰子树",
     "s": "这里天气热、靠着海，所以一年四季都绿绿的，海边长着椰子树。同样是冬天，这里的人还能在海边玩。"},
    {"id": "qz", "n": "青藏高原", "f": "雪山很高，空气稀薄，牦牛在高原上慢慢走",
     "s": "这里地势很高，山上的雪终年不化，空气也比较稀薄。牦牛身上毛长、身体壮，是最能适应高原的动物。"},
    {"id": "ht", "n": "黄土高原", "f": "厚厚的黄土，人们住在窑洞里",
     "s": "这里的黄土又厚又结实，人们顺着土坡挖出窑洞来住，冬暖夏凉。这是在当地条件下想出来的好办法。"},
]
PLACE_FACE_ORDER = [3, 0, 5, 1, 4, 2]  # 风貌卡打乱排列，避免与地方一一对齐

# ── 动手二：祖国知识小问答（五题） ──
QUIZ5 = [
    {"q": "升国旗的时候，我们应该怎么做？",
     "options": [
         {"t": "停下手里的事，站好，行注目礼，认真唱国歌", "ok": True,
          "fb": "做得很对。升国旗是很庄重的事：肃立、行注目礼、认真唱国歌，这三点做到了，就是对国旗、对祖国最好的尊敬。"},
         {"t": "小声和旁边的同学聊天，反正老师看不见", "ok": False,
          "fb": "这样可能会让周围同学也跟着说话，升旗的庄重气氛就没了。还可以试试：先安静站好，想说的话等回到教室再说。"},
         {"t": "升旗是别人的事，我自己在旁边继续玩", "ok": False,
          "fb": "这样可能会让身边的人觉得你不在意，也错过了这件庄重的事。还可以试试：听到国歌就停下来，站好，看着国旗。"},
     ]},
    {"q": "关于我们的祖国，下面哪个说法是正确的？",
     "options": [
         {"t": "台湾是中国不可分割的一部分，中国香港、中国澳门是中国的特别行政区", "ok": True,
          "fb": "说得准确。我们的祖国由很多地方组成，台湾是中国不可分割的一部分；中国香港和中国澳门是中国的特别行政区，和内地一样，都是中国的一部分。"},
         {"t": "祖国的每一个地方都长一个样", "ok": False,
          "fb": "这样可能会认错祖国各地的样子。还可以试试：想一想北边的大雪和南边的海边，差别有多大——祖国各地很不一样。"},
         {"t": "只有汉族才是中国人", "ok": False,
          "fb": "这样可能会伤到同学的心，也是不对的。我国有五十六个民族，大家都是中国人，都是兄弟姐妹，要团结友爱。"},
     ]},
    {"q": "我们国家有多少个民族？",
     "options": [
         {"t": "五十六个民族，大家都是中国人", "ok": True,
          "fb": "对。各民族的衣服、歌舞、过节方式不完全一样，但都是中国人，要互相尊重、团结友爱。"},
         {"t": "只有一个人数最多的民族", "ok": False,
          "fb": "这样可能会忽略别的民族。还可以试试：数一数身边同学会说几种话、家里过几种节——都是我们国家的宝贝。"},
         {"t": "民族不一样，就不能一起玩", "ok": False,
          "fb": "这样可能会让同学觉得孤单。还可以试试：一起玩、一起学，听听他家乡的样子，你会知道更多。"},
     ]},
    {"q": "听到国歌响起，你正在教室里收拾书包，你会：",
     "options": [
         {"t": "立刻停下来，站好，安静地听完、跟着唱", "ok": True,
          "fb": "做得很好。国歌是国家的象征，一听到就要停下、站好——这一停，就是尊敬。"},
         {"t": "先把手里的东西收完再站", "ok": False,
          "fb": "这样可能会错过国歌，也不太庄重。还可以试试：先把东西放下，等国歌结束再收。"},
         {"t": "边收东西边跟着哼两句", "ok": False,
          "fb": "这样可能会让国歌唱得不整齐、不认真。还可以试试：站直、手上不拿东西，认认真真唱完四句。"},
     ]},
    {"q": "有同学说：「我们这里夏天，别的地方也一定夏天。」你觉得：",
     "options": [
         {"t": "不一定。祖国很大，同一个时间，各地天气差别很大", "ok": True,
          "fb": "说得对。同样是一月，北边在下大雪，南边的海边还穿着短袖——祖国的样子多，正是因为地方大。"},
         {"t": "一定，全国天气从来都一样", "ok": False,
          "fb": "这样可能会认错祖国各地的样子。还可以试试：看看天气预报，比较一下最北和最南两个城市。"},
         {"t": "天气的事跟祖国大不大没关系", "ok": False,
          "fb": "这样可能会漏掉一个重要的原因。还可以试试：想一想为什么北边冷、南边暖——这和地方在哪里很有关系。"},
     ]},
]

# ── 综合任务：祖国名片设计台 —— 四类元素各选一个 ──
CARD_CATS4 = [
    {"id": "land", "n": "① 山和水", "opts": ["高高的雪山", "一条奔流的大河", "一眼望不到边的大海"]},
    {"id": "city", "n": "② 城市和乡村", "opts": ["热闹的城市", "安静的村庄", "辽阔的草原"]},
    {"id": "culture", "n": "③ 节日和文化", "opts": ["红红的灯笼和春联", "热闹的龙舟和锣鼓", "各民族一起唱歌跳舞"]},
    {"id": "family", "n": "④ 我们都是一家人", "opts": ["五十六个民族，大家都是中国人", "一方有难，八方支援", "大家一起把日子越过越好"]},
]

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g2-u4 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 祖国各地风貌配对：六个地方 ↔ 六段那里的样子
   3) 祖国知识小问答：五题，反馈为「这样可能会……还可以试试……」
   4) 祖国名片设计台：四类元素各选一个 + 一句祝福 → 实时拼出名片
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

  /* ---------- 2. 祖国各地风貌配对 ---------- */
  var PLACES = __PLACES_JSON__;
  var pStage = document.getElementById('place-stage');
  if (pStage) {
    var pickPlace = null, pickFace = null, donePair = {};
    var pOut = document.getElementById('place-out');

    function placeById(id) {
      for (var i = 0; i < PLACES.length; i++) { if (PLACES[i].id === id) return PLACES[i]; }
      return null;
    }
    function renderP() {
      document.querySelectorAll('[data-place]').forEach(function (b) {
        var k = b.dataset.place;
        b.classList.toggle('selected', k === pickPlace);
        b.classList.toggle('done', !!donePair[k]);
        b.disabled = !!donePair[k];
      });
      document.querySelectorAll('[data-face]').forEach(function (b) {
        var k = b.dataset.face;
        b.classList.toggle('selected', k === pickFace);
        b.classList.toggle('done', !!donePair[k]);
        b.disabled = !!donePair[k];
      });
      var n = Object.keys(donePair).length;
      document.getElementById('place-score').textContent = '已经配对 ' + n + ' / ' + PLACES.length + ' 个地方';
      var bank = document.getElementById('place-done');
      bank.innerHTML = '';
      PLACES.forEach(function (p) {
        if (!donePair[p.id]) return;
        var s = document.createElement('span');
        s.className = 'tag';
        s.textContent = p.n;
        bank.appendChild(s);
      });
      if (!bank.innerHTML) {
        bank.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有配对成功的地方。</span>';
      }
    }
    document.querySelectorAll('[data-place]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (donePair[b.dataset.place]) return;
        pickPlace = b.dataset.place;
        var P = placeById(pickPlace);
        pOut.className = 'result warn';
        pOut.innerHTML = '<strong>你选的地方是：' + P.n + '</strong><br>下面哪一段话是在说这里？点一点。';
        renderP();
      });
    });
    document.querySelectorAll('[data-face]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (donePair[b.dataset.face]) return;
        if (!pickPlace) {
          pOut.className = 'result warn';
          pOut.textContent = '先在左边点一个地方的名字，再来点它对应的样子。';
          return;
        }
        pickFace = b.dataset.face;
        if (pickFace === pickPlace) {
          var P = placeById(pickPlace);
          donePair[P.id] = true;
          pOut.className = 'result';
          pOut.innerHTML = '<strong>配对成功！' + P.n + '——' + P.f + '。</strong>' + P.s;
          pickPlace = null; pickFace = null;
          if (Object.keys(donePair).length === PLACES.length) {
            pOut.className = 'result';
            pOut.innerHTML = '<strong>六个地方全配对成功了！</strong>记一句小口诀：<strong>北边看雪，南边看海，西边草原高原，东边河湖水乡——一个祖国，好多种样子。</strong>';
          }
        } else {
          pOut.className = 'result warn';
          pOut.innerHTML = '<strong>这一段好像不是在说这里。</strong>你选的地方是「' + placeById(pickPlace).n + '」。' +
            '<br><span style="color:var(--muted)">常见错误：容易把「草原」和「高原」搞混——先想一想，那段话里说的是草多、牛羊多，还是说山高、雪不化？看清楚再点。</span>';
        }
        renderP();
      });
    });
    renderP();
  }

  /* ---------- 3. 祖国知识小问答 ---------- */
  var Q5 = __Q5_JSON__;
  var qStage = document.getElementById('q5-stage');
  if (qStage) {
    var qIdx = 0, qDone = {};
    var qOut = document.getElementById('q5-out');

    function renderQ() {
      var item = Q5[qIdx];
      document.getElementById('q5-progress').textContent = '第 ' + (qIdx + 1) + ' / ' + Q5.length + ' 题　（已答对 ' + Object.keys(qDone).length + ' 题）';
      document.getElementById('q5-q').textContent = item.q;
      var box = document.getElementById('q5-opts');
      box.innerHTML = '';
      item.options.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          if (qDone[qIdx] || b.disabled) return;
          var siblings = box.querySelectorAll('.choice');
          if (o.ok) qDone[qIdx] = true;
          Array.prototype.forEach.call(siblings, function (s) {
            s.disabled = true;
            if (s.textContent === o.t && o.ok) s.classList.add('correct');
            if (s.textContent === o.t && !o.ok) s.classList.add('wrong');
          });
          if (o.ok) {
            qOut.className = 'result';
            qOut.innerHTML = '<strong>答对了。</strong>' + o.fb;
          } else {
            qOut.className = 'result warn';
            qOut.innerHTML = '<strong>这个说法还可以再想一想。</strong>' + o.fb;
          }
          renderQ();
        });
        box.appendChild(b);
      });
    }
    document.getElementById('q5-next').addEventListener('click', function () {
      qIdx = (qIdx + 1) % Q5.length;
      qOut.className = 'result warn';
      qOut.textContent = '读一读题目，选一个你认为正确的。';
      renderQ();
    });
    renderQ();
  }

  /* ---------- 4. 祖国名片设计台 ---------- */
  var C4 = __CARD4_JSON__;
  var nStage = document.getElementById('nation-stage');
  if (nStage) {
    var picked = {};
    var wishEl = document.getElementById('nation-wish');
    var nOut = document.getElementById('nation-out');

    function renderN() {
      var done = 0;
      C4.forEach(function (c) { if (picked[c.id] !== undefined) done++; });
      document.querySelectorAll('[data-nat-cat]').forEach(function (b) {
        b.classList.toggle('selected', picked[b.dataset.natCat] === parseInt(b.dataset.natOpt, 10));
      });
      document.getElementById('nation-score').textContent = '已经选好 ' + done + ' / ' + C4.length + ' 类';
      var wish = (wishEl && wishEl.value.trim()) || '我爱我们的祖国';
      var rows = '';
      C4.forEach(function (c) {
        var v = picked[c.id] !== undefined ? c.opts[picked[c.id]] : '<span style="color:var(--muted)">还没有选</span>';
        rows += '<div style="margin:6px 0"><strong>' + c.n.replace(/^[①②③④]\s*/, '') + '：</strong>' + v + '</div>';
      });
      document.getElementById('nation-preview').innerHTML =
        '<div style="font-size:20px;font-weight:800;color:var(--link);margin-bottom:4px">我的祖国名片</div>' +
        '<div style="color:var(--muted);font-size:14px;margin-bottom:8px">' + wish + '</div>' +
        rows;
      if (done === C4.length) {
        nOut.className = 'result';
        nOut.innerHTML = '<strong>四类都选好了，一张祖国名片就做出来了！</strong>把名片读一遍，再想一想：<strong>这里面哪一样是你最想告诉别人的</strong>？把这一样讲给同桌听。';
      } else {
        nOut.className = 'result warn';
        nOut.innerHTML = '<strong>先把四类都选一选。</strong>选的时候想一想：山和水、城市和乡村、节日和文化、我们都是一家人——这四样加起来，就是我们的祖国。';
      }
    }
    document.querySelectorAll('[data-nat-cat]').forEach(function (b) {
      b.addEventListener('click', function () {
        picked[b.dataset.natCat] = parseInt(b.dataset.natOpt, 10);
        renderN();
      });
    });
    if (wishEl) wishEl.addEventListener('input', renderN);
    renderN();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__PLACES_JSON__', json.dumps(PLACES, ensure_ascii=False))
             .replace('__Q5_JSON__', json.dumps(QUIZ5, ensure_ascii=False))
             .replace('__CARD4_JSON__', json.dumps(CARD_CATS4, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "同样是一月，祖国最北边和最南边可能是什么样子？",
         "options": [("北边下大雪、地上结冰，南边的海边还穿着短袖", True),
                     ("两边都是一样的天气", False),
                     ("两边都冷得不能出门", False)],
         "explain": "同样是一月，北边在下大雪，南边的海边还很暖和。祖国很大，各地样子差别很大。"
                    "<strong>错因提醒：</strong>常见错误是误认为「全国天气都一样」——记住地图上从北到南有多远，就知道差别会有多大。"},
        {"q": "我们国家有多少个民族？大家都是什么人？",
         "options": [("五十六个民族，大家都是中国人", True),
                     ("只有一个民族", False),
                     ("每个民族的人都住在很远的地方，互相不来往", False)],
         "explain": "我们国家有五十六个民族，穿的衣服、唱的歌、过节的方式不完全一样，但都是中国人，都是兄弟姐妹。"
                    "<strong>错因提醒：</strong>容易误认为「不一样就不是一家人」——不一样的是风俗，一样的是一家人。"},
        {"q": "升国旗的时候，下面哪个做法是对的？",
         "options": [("停下手里的事，站好，行注目礼，认真唱国歌", True),
                     ("一边说话一边看", False),
                     ("躲在教室里，等升完旗再出来", False)],
         "explain": "国旗是五星红旗，国歌是《义勇军进行曲》。升国旗是很庄重的事，要肃立、行注目礼、认真唱国歌。"
                    "<strong>错因提醒：</strong>有人误认为「操场上人那么多，我不站好也没人看见」——升旗是对国旗、对祖国的尊敬，跟有没有人看见没关系。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "美丽中国我们的家：一个祖国，好多种样子", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们知道自己的家在哪条街、哪栋楼（And）；可祖国有多大、别的地方是什么样子，很多同学还没有真的见过（But）；今天先用图片和文字，把祖国各地走上一圈（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">我们的祖国很大。从最北边到最南边，坐飞机也要飞上好几个小时。这么大的地方，每一个地方的样子都不一样。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>北边和南边</strong></p>
            <p style="color:var(--muted)">最北边冬天很长，大雪能盖住房顶，人们滑冰、看冰灯；最南边的海边一年四季都暖和，长着高高的椰子树。</p>
          </div>
          <div class="inner-card">
            <p><strong>西边和东边</strong></p>
            <p style="color:var(--muted)">西边有一望无际的草原，牛羊成群；还有地势很高的高原，山上有终年不化的雪。东边河湖多，小河穿城而过，出门可以坐小船。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="祖国各地风貌示意图：北方的雪、江南水乡、辽阔的草原、温暖的南方海边，附中文标注">
          <figcaption>示意图：一个祖国，好多种样子——北方的雪 · 江南水乡 · 辽阔的草原 · 温暖的南方海边（教学示意图）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「全国到处都是自己家这个样子」。其实同样是祖国，北边的雪、南边的海、西边的草原、东边的水乡，样子完全不同——这正是我们祖国好看的地方。</p>
        </div>
        <div class="kid-note"><span class="emoji">🗺️</span><div><strong>记一句小口诀：</strong>北边看雪，南边看海，西边草原高原，东边河湖水乡——一个祖国，好多种样子。</div></div>
{insight_box([
    {"lens": "看见它", "text": "同样是一月，照片里这边的人裹着棉衣，那边的人还穿着短袖——不用讲道理，两张照片放在一起就把「祖国很大」说清楚了。"},
    {"lens": "比较它", "text": "比一比：雪多的地方冬天长，水多的地方稻田多，草原多的地方牛羊多，海近的地方椰子多。地方不一样，长出来的东西、过的日子就不一样。"},
    {"lens": "迁移它", "text": "以后看到别的地方的照片、吃到别的地方的饭菜，可以顺着想一想：那地方在哪里？大概什么气候？人们平时怎么过日子？"},
])}
    ''', tag="概念一"))

    place_btns = "\n".join(
        f'            <button class="choice" data-place="{p["id"]}" style="text-align:center">{p["n"]}</button>'
        for p in PLACES
    )
    face_btns = "\n".join(
        f'            <button class="choice" data-face="{PLACES[i]["id"]}" style="text-align:left">{PLACES[i]["f"]}</button>'
        for i in PLACE_FACE_ORDER
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：祖国各地风貌配对", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先在上面点一个地方的名字，再在下面点出它在说哪一段样子。配对了会告诉你为什么。</p>
        <div class="lab-panel" id="place-stage">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 祖国的一个地方</div>
          <div class="grid grid-3">
{place_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 那里的样子是哪一段</div>
          <div class="grid">
{face_btns}
          </div>
          <div class="inner-card" style="margin-top:14px">
            <p><strong>我们已经走过的地方</strong></p>
            <div id="place-done" style="display:flex;flex-wrap:wrap;gap:6px"><span style="color:var(--muted);font-size:14px">还没有配对成功的地方。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">配对进度</span><span class="v" id="place-score">已经配对 0 / 6 个地方</span></div>
          </div>
          <p class="result warn" id="place-out" style="margin-top:12px">先在上面点一个地方的名字。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧭</span><div><strong>拿不准就问自己一句：</strong>这段话里说的是<strong>雪和冰</strong>、是<strong>水和船</strong>、是<strong>草和牛羊</strong>，还是<strong>高原和牦牛</strong>？问完这一句，答案就清楚了。</div></div>
    ''', tag="动手一", bloom="analyze"))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "我们都是中国人 · 国家的象征要尊敬", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">祖国各地样子不同，但我们有很多<strong>一样的东西</strong>：一样的节日，一样的文化，还有一个共同的名字——中国人。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>五十六个民族，大家都是中国人：</strong>穿的衣服、唱的歌、过节的方式不完全一样，但都是兄弟姐妹，要互相尊重、团结友爱。</div></div>
          <div class="step"><span class="n">2</span><div><strong>一起过的节日，一起有的宝贝：</strong>过年贴春联、挂灯笼、吃团圆饭，红红火火；端午赛龙舟、包粽子，中秋赏月亮——很多节日我们一起过。</div></div>
          <div class="step"><span class="n">3</span><div><strong>国家的象征，要特别尊敬：</strong>国旗是五星红旗，国歌是《义勇军进行曲》，国徽是国家的象征。升国旗时要<strong>肃立</strong>、<strong>行注目礼</strong>、<strong>认真唱国歌</strong>；不能乱涂乱画，也不能拿来开玩笑，国家专门立了法保护它们。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>我们的祖国由很多地方组成：</strong>台湾是中国不可分割的一部分；中国香港和中国澳门是中国的特别行政区，和内地一样，都是中国的一部分。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="我们都是中国人示意图：各民族小朋友在一起、节日与文化、我们都是中国人，附中文标注">
          <figcaption>示意图：我们都是中国人——民族团结 · 节日与文化 · 我们都是一家人（教学示意图）</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「只有自己家乡的过节方式才是对的」。其实各民族、各地方的节日和风俗不完全一样，它们都是祖国的宝贝，都值得看一看、学一学。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "把「不一样」和「一样」并排放：衣服不一样、歌舞不一样、过节方式不一样；可是写的是同一种字，过的是共同的节日，认的是同一个祖国。"},
    {"lens": "解释它", "text": "为什么对国家象征要那么庄重？因为国旗、国歌、国徽上写的是整个国家的名字，尊敬它们，就是尊敬共同生活在这片土地上的每一个人。"},
    {"lens": "迁移它", "text": "这份庄重平时也能做出来：看到国旗升起来就站好，听到国歌响起就停下，遇到不同民族、不同地方的同学就多问一问、多听一听。"},
])}
    ''', tag="概念二"))

    q5_html = f'''
        <p style="color:var(--muted);margin:0 0 12px">一共五道题。读题、选一个你认为正确的，选完就会有一段话告诉你为什么，或者还可以怎么想。做完一题点「下一题」。</p>
        <div class="lab-panel" id="q5-stage">
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">进度</span><span class="v" id="q5-progress">第 1 / 5 题</span></div>
          </div>
          <div class="inner-card" style="margin-top:12px">
            <p><strong id="q5-q"></strong></p>
            <div class="grid" id="q5-opts" style="margin-top:10px"></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="q5-next" style="text-align:center;flex:1">下一题</button>
          </div>
          <p class="result warn" id="q5-out" style="margin-top:12px">读一读题目，选一个你认为正确的。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⭐</span><div><strong>说给你听：</strong>国旗是五星红旗，国歌是《义勇军进行曲》，国徽是国家的象征。记住升国旗时要做的三件事：<strong>肃立、行注目礼、认真唱国歌</strong>。</div></div>
    '''
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：祖国知识小问答", TTS["lab-2"], q5_html, tag="动手二", bloom="understand"))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：升国旗的时候，我们应该怎么做", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>星期一早上，操场上响起国歌，国旗正在升上去。这时候，站在队伍里的小明应该怎么做？请你陪他一步一步想清楚。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>立刻停下手里的事：</strong>不聊天、不打闹，先把身子站住。正在收的书包、正在说的话，都先放下。</div></div>
          <div class="step"><span class="n">2</span><div><strong>站好，也就是肃立：</strong>身体挺直，手上不拿东西，不乱动，双脚站好。</div></div>
          <div class="step"><span class="n">3</span><div><strong>行注目礼：</strong>脸朝着国旗，眼睛认真看着国旗一点一点升上去。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>认真唱国歌：</strong>跟着大家一起唱，声音整齐，不哼不笑、不东张西望。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「升旗的时候小声说两句话没关系」；也有的<strong>误认为</strong>「操场上人那么多，我不站好也没人看见」。国旗是五星红旗，国歌是《义勇军进行曲》，升旗是很庄重的事——做得好不好，跟有没有人看见没有关系。</p>
        </div>
        <div class="inner-card">
          <p><strong>说给同桌听：</strong>这四步里，哪一步你以前没做到过？下一次升旗，你打算先把哪一步做好？</p>
        </div>
    ''', tag="例题示范", bloom="apply"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于我们的祖国，下面哪个说法是正确的？",
         "options": [("台湾是中国不可分割的一部分，中国香港、中国澳门是中国的特别行政区", True),
                     ("祖国的每一个地方都长一个样", False),
                     ("只有汉族才是中国人", False)],
         "explain": "我们的祖国由很多地方组成：台湾是中国不可分割的一部分；中国香港和中国澳门是中国的特别行政区，都是中国的一部分。"
                    "<strong>错因提醒：</strong>常见错误是误认为「祖国各地都一样」——北边的雪和南边的海，差别大着呢。另外，我国有五十六个民族，大家都是中国人。"},
        {"q": "国歌响起的时候，班上有的同学还在说话。你会：",
         "options": [("自己先站好、认真唱，手势提醒旁边的同学安静", True),
                     ("跟着一起说，反正大家都在说", False),
                     ("大声喊一句「别说了」，把大家都吓一跳", False)],
         "explain": "自己先做对，再轻轻提醒同学，是最好的办法。国歌是国家的象征，要认真对待。"
                    "<strong>错因提醒：</strong>有人误认为「大家都在说，我说一句也没关系」——正好相反，多一个人做对，气氛就庄重一分。"},
        {"q": "班上新来了一位同学，说话的家乡口音和大家不一样。你会：",
         "options": [("和他一起玩，问问他家乡的样子，也教他说本地话", True),
                     ("笑他说话怪，让大家都听一听", False),
                     ("不和他说话，等他的口音改了再说", False)],
         "explain": "口音不一样，是因为家乡不一样。五十六个民族、各个地方的人都是中国人，都是兄弟姐妹。"
                    "<strong>错因提醒：</strong>容易把「不一样」误认为「不好」——不一样的地方，正是我们国家好看、好听的地方。"}
    ], tag="概念测试"))

    nb = []
    for c in CARD_CATS4:
        btns = "\n".join(
            f'              <button class="choice" data-nat-cat="{c["id"]}" data-nat-opt="{i}" style="text-align:center">{o}</button>'
            for i, o in enumerate(c["opts"])
        )
        nb.append(f'''          <div style="margin-top:12px">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">{c["n"]}</div>
            <div class="grid grid-3">
{btns}
            </div>
          </div>''')
    nation_html = "\n".join(nb)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：做一张「我的祖国名片」", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先写下你想对祖国说的一句话，再从下面四类里<strong>每一类挑一个</strong>，点一点，祖国名片就会一样一样长出来。</p>
        <div class="lab-panel" id="nation-stage">
          <label style="display:block;font-weight:700;font-size:14px;margin-bottom:6px">我想对祖国说的一句话
            <input id="nation-wish" placeholder="例如：我们的祖国真大，也真好看。" style="margin-top:8px">
          </label>
{nation_html}
          <div class="inner-card" style="margin-top:16px;border:2px solid var(--brand);background:var(--card)">
            <div id="nation-preview"><span style="color:var(--muted);font-size:14px">名片还没有做出来，先在上面选一选。</span></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">名片进度</span><span class="v" id="nation-score">已经选好 0 / 4 类</span></div>
          </div>
          <p class="result warn" id="nation-out" style="margin-top:12px">先把四类都选一选。</p>
        </div>
        <div class="inner-card">
          <p><strong>做完名片，再想一想：</strong></p>
          <p style="color:var(--muted)">名片上这四样，哪一样你最想讲给别人听？你打算怎么讲？先在下面写一两句，再说给同桌听。</p>
          <textarea id="syn-answer" rows="3" placeholder="我最想讲的是……，因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，做法还在不在", TTS["posttest"], [
        {"q": "国歌响起时，你正在教室里收拾书包。下面哪个做法是对的？",
         "options": [("立刻停下来，站好，安静认真地听完、跟着唱", True),
                     ("先把手里的东西收完，再站好", False),
                     ("边收东西边小声跟着哼两句", False)],
         "explain": "国歌是《义勇军进行曲》，是国家的象征。一听到就要停下、站好、认真唱——这一停，就是尊敬。"
                    "<strong>错因提醒：</strong>常见错误是误认为「边做别的事边听也算听到了」——国歌要认真对待，手上不该有别的事。"},
        {"q": "班上来了一位说话口音和大家不一样的新同学。你会：",
         "options": [("和他一起玩，听听他家乡的样子，也跟他说说自己家乡的样子", True),
                     ("只和自己口音一样的同学玩", False),
                     ("学他的口音取笑他", False)],
         "explain": "口音是家乡给的。我们国家有五十六个民族、很多个地方，大家都是中国人，要团结友爱。"
                    "<strong>错因提醒：</strong>有人误认为「口音不一样就不好相处」——正好相反，多听一听，你会知道更多有趣的事。"},
        {"q": "有人问你：「祖国那么大，我们要不要知道别的地方的样子？」你的回答是：",
         "options": [("要知道。各地样子不一样，多了解就更爱我们的祖国", True),
                     ("不用，只要知道自己家就行了", False),
                     ("别的地方好不好，跟我没关系", False)],
         "explain": "知道得越多，越会明白祖国有多大、有多好看。北边的雪、南边的海、西边的草原、东边的水乡，都是我们的家。"
                    "<strong>错因提醒：</strong>容易误认为「别的地方和我没关系」——我们同住在一片土地上，别的地方也是祖国的一部分。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清我们的祖国", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>美丽中国我们的家：</strong>祖国很大，北边下大雪，南边四季暖和，西边有草原和高原，各地样子都不一样。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>我们都是中国人：</strong>五十六个民族，大家都是中国人，要团结友爱；春节、端午、中秋，很多节日我们一起过。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>国家的象征要尊敬：</strong>国旗是五星红旗，国歌是《义勇军进行曲》，国徽是国家的象征；升国旗时肃立、行注目礼、认真唱国歌。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>我们的祖国由很多地方组成：</strong>台湾是中国不可分割的一部分；中国香港和中国澳门是中国的特别行政区，都是中国的一部分。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那个问题：</strong>我们的祖国有多大？大到同一个时间里，北边在下雪、南边在海边玩水；大到有五十六个民族一起住在这里。知道她有多大、有多好看，就会从心里说一句：我爱我们的祖国。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「祖国、各地、国旗」这三个词，说清楚你今天最想告诉别人的一件事，说给同桌听。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出祖国的两个地方，说说那里的样子有什么不一样。",
            "说出升国旗时要做哪三件事，并说说为什么国歌响起时要先停下来。",
        ],
        [
            "问一问家里人，或者查一查书，找出两个关于祖国的知识，说给同学听。",
            "动手做一张自己的祖国名片（可以画，也可以剪贴），把四类元素都放上去。",
        ],
        [
            "找一张祖国各地的风景图片，说说那里的样子和当地的气候有什么关系。",
            "为祖国做一件小事，比如把升国旗的礼仪教给比自己小的同学，或者把今天学到的知识讲给家人听。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": ID,
    "node_id": ID,
    "subject": "politics",
    "subject_cn": "道德与法治",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育道德与法治课程标准（2022年版2025年修订）· 小学",
    "title": "我爱我们的祖国",
    "name_en": "I Love Our Motherland",
    "grade": 2,
    "grade_cn": "二年级",
    "domain": "rule-of-law",
    "domain_cn": "法治启蒙",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学二年级的道德与法治课：先看祖国之大与各地风貌的不同，再认识五十六个民族一家亲、共同的节日与文化，并学会庄重地对待国旗、国歌、国徽——升国旗时肃立、行注目礼、认真唱国歌。核心动手是把六个地方与当地风貌配对、做一轮祖国知识小问答、动手拼出一张「我的祖国名片」。领土表述严格准确：台湾是中国不可分割的一部分，中国香港、中国澳门是中国的特别行政区。插图不绘制国旗、国徽与地图，全部为中性简洁扁平插画。",
    "tags": ["我爱我们的祖国", "祖国各地风貌", "五十六个民族", "国旗国歌国徽", "升国旗礼仪", "祖国名片", "二年级"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学——了解基本法律常识，树立规则意识和权利意识；知道国旗、国歌等国家象征的意义。对应统编《道德与法治》二年级上册「我爱我们的祖国」单元：美丽中国我们的家、我们都是中国人、红红火火中国年、祖国，我为您自豪。",
    "hero_question": "我们的祖国有多大？她有哪些不一样的样子？",
    "hero_alt": "我爱我们的祖国知识结构图：美丽中国我们的家、我们都是中国人、祖国我为您自豪 三栏",
    "hero_caption": "我爱我们的祖国：美丽中国我们的家 · 我们都是中国人 · 国家的象征要尊敬 · 我为您自豪",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "祖国到底有多大？有哪些不一样的地方？", "d": "北边的雪、南边的海、西边的草原", "v": "祖国到底有多大有哪些不一样的地方"},
        {"t": "为什么说我们都是中国人？", "d": "五十六个民族和一起过的节日", "v": "为什么说我们都是中国人"},
        {"t": "升国旗的时候应该怎么做？", "d": "肃立、行注目礼、认真唱国歌", "v": "升国旗的时候应该怎么做"},
        {"t": "我可以为祖国做点什么？", "d": "从身边最小的一件事开始", "v": "我可以为祖国做点什么"},
    ],
    "objectives": [
        "能说出祖国很大，不同地方有不同样子，并能举出两个例子",
        "知道我国有五十六个民族，大家都是中国人，要团结友爱",
        "能说出国旗是五星红旗、国歌是《义勇军进行曲》，知道升国旗时要肃立、行注目礼、认真唱国歌",
        "知道台湾是中国不可分割的一部分、中国香港和中国澳门是中国的特别行政区，愿意为祖国做一件力所能及的小事",
    ],
    "objectives_plain": [
        "能说出祖国很大，不同地方有不同样子，并能举出两个例子",
        "知道我国有五十六个民族，大家都是中国人，要团结友爱",
        "能说出国旗是五星红旗、国歌是《义勇军进行曲》，知道升国旗时要肃立、行注目礼、认真唱国歌",
        "知道台湾是中国不可分割的一部分、中国香港和中国澳门是中国的特别行政区，愿意为祖国做一件力所能及的小事",
    ],
    "standards": [
        {"content": "了解基本法律常识，树立规则意识和权利意识；知道国旗、国歌等国家象征的意义",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 法治启蒙"},
        {"content": "美丽中国我们的家；我们都是中国人；红红火火中国年；祖国，我为您自豪",
         "source": "统编《道德与法治》二年级上册「我爱我们的祖国」单元"},
    ],
    "prereqs": ["pol-e-g2-u3"],
    "prereqs_name": "我的家乡美",
    "prereqs_meta": "pol-e-g2-u3",
    "leads_to": ["pol-e-g3-u1"],
    "next_meta": "pol-e-g3-u1",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "从最北的雪到最南的海——今天先把「祖国有多大」看清楚。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能说出祖国的两个地方，还会做升国旗的三件事。",
        "objectives": "看清四件事：祖国各地不一样、五十六个民族一家亲、国家象征要尊敬、为祖国做一件小事。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "祖国很大，同一个时间，北边下雪、南边海边玩水——各地样子都不一样。",
        "lab-1": "先点地方，再点那里的样子。容易把草原和高原搞混，看清楚「草多牛羊多」还是「山高雪不化」。",
        "module-2": "五十六个民族一家亲；国旗是五星红旗，国歌是《义勇军进行曲》，国徽是国家的象征。",
        "lab-2": "五道小问答，答完读一读反馈。答得不合适也没关系，看看还可以怎么想。",
        "worked-example": "升国旗四步：停下手里的事、站好肃立、行注目礼、认真唱国歌。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "四类元素各挑一个，再加上一句想对祖国说的话，就做出了一张祖国名片。",
        "posttest": "出现了国歌响起时、新同学的口音、还有祖国各地，看看你能不能把学到的用上去。",
        "summary": "四句话：祖国各地不一样、五十六个民族一家亲、国家象征要尊敬、祖国由很多地方组成。",
        "homework": "三层小任务，先做前两层，第三层可以和家人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课正对统编教材二年级上册「我爱我们的祖国」单元，补知识树中「国家认同与法治启蒙」这一空缺。二年级学生的困难不是不爱祖国，而是「说不清祖国是什么样子」——所以全课不讲大道理，只做三件能落地的事：一是把祖国之大说清楚（同一时间北边下雪、南边海边玩水，西边草原高原、东边河湖水乡）；二是把「我们都是中国人」说清楚（五十六个民族一家亲、共同的节日与文化）；三是把国家象征的礼仪说清楚（国旗是五星红旗，国歌是《义勇军进行曲》，国徽是国家的象征；升国旗时肃立、行注目礼、认真唱国歌）。三个互动台子都能真的操作：一个是「祖国各地风貌配对」，把六个地方配到六段当地的样子；一个是「祖国知识小问答」，五题即时给出「这样可能会……还可以试试……」的诊断式反馈；一个是「我的祖国名片」，四类元素各挑一个、再写一句想对祖国说的话，名片会实时拼出来。领土表述严格准确：台湾是中国不可分割的一部分，中国香港和中国澳门是中国的特别行政区。国家象征一律只用文字准确、庄重地表述，插图不绘制国旗、国徽与地图，全部为中性简洁扁平插画。",
    "plan_table": """| 1 | cover | 我爱我们的祖国 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 美丽中国我们的家：一个祖国，好多种样子 | 承·概念一（祖国之大与各地风貌） |
| 6 | interactive | 动手一：祖国各地风貌配对 | 承·配对操作（六个地方 ↔ 六段样子） |
| 7 | concept | 我们都是中国人 · 国家的象征要尊敬 | 承·概念二（民族团结 · 文化多样 · 国家象征礼仪 · 领土表述） |
| 8 | interactive | 动手二：祖国知识小问答 | 承·诊断式小问答（五题） |
| 9 | concept | 例题示范：升国旗的时候，我们应该怎么做 | 转·重点突破（分步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：做一张「我的祖国名片」 | 合·迁移应用（选元素 → 拼成名片） |
| 12 | quiz | 后测：换几个新情境，做法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清我们的祖国 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：美丽中国我们的家 / 我们都是中国人 / 祖国我为您自豪 三栏，附中文标注\n- P5 祖国各地风貌示意图（已生成）：北方的雪、江南水乡、辽阔的草原、温暖的南方海边，附中文标注\n- P7 我们都是中国人示意图（已生成）：民族团结、节日与文化、我们都是一家人，附中文标注\n- 三张图均为中性简洁扁平插画，不使用任何真实人物照片或可识别肖像\n- 插图不绘制国旗、国徽图形，不绘制任何地图与国界线；国家象征仅以文字准确表述\n- 若需补充：祖国各地风景的照片（需授权后使用）",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
