# -*- coding: utf-8 -*-
"""小学心理健康 · 悦纳自我与学习动机（G5）—— 补齐知识树「认识自我」空缺

学科语气（心理健康）：温和、不评判、不贴标签；严禁临床诊断词汇；不涉及自伤自杀；插图一律中性简洁插画。
五年级落点：① 看清一件事的两种理由——「喜欢这件事本身」和「为了得到什么才做」；
  ② 把「我必须考第一」这类想法改成站得住的版本（不降低要求，而是把要求放到能做的事上）；
  ③ 把喜欢的样子、吃力的样子、想多试试的样子放在一起看，在各种活动中悦纳自己。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/psych-e-g5-self-accept-fig1.webp'
F2 = './assets/psych-e-g5-self-accept-fig2.webp'

TTS = {
    "hero": "五年级的同学，先想一想：你做一件事的时候，心里那句话是「我必须考第一，考不到就完了」，还是「我想把这几道题弄懂」？这两种说法，带来的感受很不一样。这节课我们做三件事。第一件，看清一件事的两种理由——是因为喜欢它本身，还是为了得到什么。第二件，把「我必须」改成站得住的版本，并且马上看到心里那块地方松开了多少。第三件，把喜欢的样子、有点吃力的样子和想多试试的样子放在一起看一看。",
    "problem-anchor": "开始之前，先选一个你最想知道的事。是想知道喜欢这件事本身和为了奖励才做到底差在哪里，还是想把「我必须考第一」改一改却不知道怎么改，或者你最想问的是要求降低了是不是就等于不努力了，再或者你想弄清楚，怎么才能真的喜欢上自己做的事。选好了，就带着它往下看。",
    "objectives": "这节课有四个小目标。第一，能说出一件事的两种理由，知道理由在事情里面和在事情外面有什么不一样。第二，能把「我必须考第一」这类想法改成站得住的版本，并说出心里的感受有什么变化。第三，能说出站得住的说法和降低要求不是一回事。第四，能把自己的喜欢、有点吃力和想多试试的样子放在一起看一看，说出三个样子都是自己。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "我们先说第一件事：做一件事的理由。有的理由在事情里面，比如我想把这首曲子弹给奶奶听，我一直好奇这道题为什么会这样；做的时候就已经在享受了。有的理由在事情外面，比如做完才有奖励，不做完会被说；它也能让人动起来，可是别人不说了、奖励拿完了，力气就小了。两种理由我们都会有，这很正常。要留意的是，外面的理由撑不了太久，所以可以在外面那个理由旁边，慢慢加上一个里面的理由。",
    "lab-1": "现在请你当一次理由辨别员。下面有八句话，都是我们做一件事时心里的理由。点一句话，再点上面两栏中的一个。分得不太合适也不会说你错，我会告诉你这个理由能陪你走多久，还可以怎么加上一个里面的理由。",
    "module-2": "第二件事：把「我必须」改一改。像我必须考第一、我不能出一点错，这些话有一个共同点，它们把结果提前写死了，而结果并不完全由我决定。这样说的时候，心里像被一根绳子绷住，手反而抬不起来。站得住的说法是这样的：我希望考得好，我更想弄懂这几道题，这周我先把错题整理一遍。请你留意，这不是把要求降低，而是把要求放到自己能做的那一部分上，同时接受结果不一定刚刚好。",
    "lab-2": "现在请你用一次改写台。下面有五句「我必须」，点开一句，你会看到三种改写。选一个之后，下面两根条会马上动起来：上面那根是绷紧的程度，下面那根是手上能做的事。你会看到同一件事换一种说法，心里的感受真的不一样。",
    "worked-example": "我们一起帮小禾想一想。第二次月考，小禾考了班里第三名。成绩一出来，她一整天都提不起劲，心里那句话是——我必须考第一，第三名就是没考好。我们陪她走四步。第一步，看看这句「我必须」：它把名次提前写死了，可是名次要看好几个因素，并不全由她决定。第二步，把想法改一改：我希望考得好，我更想弄懂这次错的三道题。第三步，找一找喜欢这件事本身的地方：小禾最喜欢语文课上的那篇课文，读的时候会忘记时间，今天她先把那一篇读第二遍，只为了读。第四步，看看自己的三个样子：喜欢做的事是读故事，做起来有点吃力的事是列竖式容易漏掉进位，想多试试的事是在小组里讲一次自己读到的故事。三个样子都是她，不用改掉哪一个才值得被喜欢。",
    "conceptest-1": "接下来用三个说法考考你，每一个里面都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件大事交给你。先选一件你正在做的事，再挑一句你心里冒出来的「我必须」，把它改成「我想要……因为……」，配一件喜欢这件事本身的小事，最后写下你的三个样子。做完，你会得到一张自己的学习理由卡。",
    "posttest": "最后一轮，换三个新的小情境来考考你。这次会出现练了三个月后来停下的跳绳、每次都希望老师满意的作文，还有好朋友画得比你好，看看你能不能把「我必须」改成站得住的版本。",
    "summary": "这节课我们记住三句话。第一句，做一件事的理由可以在事情里面，也可以在事情外面；外面的理由撑不了太久，可以慢慢加上一个里面的理由。第二句，「我必须考第一」把结果提前写死了，改成我希望考得好、我更想弄懂这几道题，要求还在，只是放到了能做的事情上。第三句，喜欢的样子、有点吃力的样子、想多试试的样子，三个都是你。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出三件你正在做的事，每件事写下你现在的理由，再说说这个理由在事情里面还是外面。第二层能力应用，动手做：挑一句你心里说过的「我必须」，把它改写成站得住的版本，再把心里的变化写两句。第三层迁移挑战，选做：这一周里，为一件你本来只为奖励才做的事，找一个你喜欢的那个点，记下你做完以后的感受，写三句话。",
    "knowledge-graph": "这张图展示了这节课在心理健康知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 理由在事情里面，还是在事情外面", "lab-1": "动手一 理由辨别员",
    "module-2": "概念二 把「我必须考第一」改一改", "lab-2": "动手二 「我必须」改写台",
    "worked-example": "例题讲解 小禾的第二次月考", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的学习理由卡", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：理由辨别员（八张卡片） ──
MOTIVE_BINS = [
    {"id": "inner", "name": "① 理由在事情里面"},
    {"id": "outer", "name": "② 理由在事情外面"},
]

MOTIVES = [
    {"id": "c1", "bin": "inner", "t": "我把这首曲子练熟了，因为我想弹给奶奶听。",
     "fb": "理由在事情里面——想把曲子弹给别人听，练的时候就已经在享受了。"},
    {"id": "c2", "bin": "outer", "t": "我练琴，因为练够十次就可以换一个新玩具。",
     "fb": "理由在事情外面。玩具拿到以后，琴可能就不想练了。可以加上一个里面的理由：我想把最好听的那两小节弹顺。"},
    {"id": "c3", "bin": "inner", "t": "我想把这道题弄懂，因为我一直好奇它为什么会这样。",
     "fb": "好奇是最经用的理由，它不用别人来给你加油。"},
    {"id": "c4", "bin": "outer", "t": "我写作业，因为不写完妈妈会说我。",
     "fb": "这个理由也能让人动起来，只是它靠别人的话撑着；别人不说了，力气就小了。"},
    {"id": "c5", "bin": "inner", "t": "我读这本书，因为我很想知道后面怎么样了。",
     "fb": "理由在事情里面——故事本身就在拉着你往前走。"},
    {"id": "c6", "bin": "outer", "t": "我举手回答问题，因为答对了会得小星星。",
     "fb": "小星星是外面的理由，留着它也没关系。可以再加一个里面的理由：我想把我知道的说出来。"},
    {"id": "c7", "bin": "inner", "t": "我画这张画，因为我喜欢颜色在纸上慢慢变出来的样子。",
     "fb": "这句话里没有别人，只有你和这件事本身。"},
    {"id": "c8", "bin": "outer", "t": "我跑这一次，因为跑第一就会有人夸我。",
     "fb": "被夸很开心，可它不由你决定。可以加上一句：我想看看自己能跑多快。"},
]

# ── 动手二：「我必须」改写台（含实时感受数据：绷紧程度 / 手上能做的事） ──
MUSTS = [
    {"id": "a1", "t": "我必须考第一。",
     "opts": [
         {"t": "我希望考得好，我更想弄懂这几道题。这周我先把错题整理一遍。", "ok": True, "tense": 3, "room": 8,
          "feel": "胸口松开一些，手上有事可做——要求还在，只是放在了能做的事上。",
          "fb": "这句把「一定要第一」换成了「我希望」加「我更想弄懂」，再配一个今天能做的小事。"},
         {"t": "我必须考第一，考不到就完了。", "ok": False, "tense": 9, "room": 2,
          "feel": "越想越紧，还没开考，人已经被绳子绷住了。",
          "fb": "这样可能会让你把注意力放在名次上，而不是放在题目上。还可以试试：说出你今天想弄懂的那一道题。"},
         {"t": "算了吧，第几都无所谓，随便考考。", "ok": False, "tense": 3, "room": 1,
          "feel": "不那么紧了，可手也停下来了——这不是站得住，这是把要求整个扔掉了。",
          "fb": "这样可能会让你连本来会的也不想做了。还可以试试：把要求放低一点但留着它——「我希望考得好，先弄懂两道错题」。"},
     ]},
    {"id": "a2", "t": "我不能出一点错。",
     "opts": [
         {"t": "我想把我会的做对。有不确定的题先圈出来，回来再看一遍。", "ok": True, "tense": 3, "room": 8,
          "feel": "肩膀松下来，手上多了一个可以做的动作。",
          "fb": "「把我会的做对」是能做的，「一点错都不出」是谁也做不到的。换一个能做的，力气才使得上。"},
         {"t": "一个字都不能错，错一处就太丢人了。", "ok": False, "tense": 9, "room": 2,
          "feel": "握着笔的手有点发紧，越怕错越不敢往下写。",
          "fb": "这样可能会让检查变成一件可怕的事。还可以试试：给自己一个具体的检查顺序——先看计算，再看题目要求。"},
         {"t": "错了就错了，反正我也不看。", "ok": False, "tense": 4, "room": 1,
          "feel": "心里不那么紧了，可是错题也留在了原地。",
          "fb": "这样可能会让同一个地方一直丢分。还可以试试：只挑一道错题看一眼，找出它错在哪一步。"},
     ]},
    {"id": "a3", "t": "我必须每次都比同桌快。",
     "opts": [
         {"t": "我想比上一次的自己快一点。今天我先把昨天的错题改完。", "ok": True, "tense": 3, "room": 8,
          "feel": "心里安定了，目标变成自己看得见的那一小步。",
          "fb": "把比自己换成比昨天的自己，这一条你能说了算，也更容易做到。"},
         {"t": "他写那么快，我永远都追不上，我太慢了。", "ok": False, "tense": 8, "room": 2,
          "feel": "越比越沉，眼睛一直在看别人的本子。",
          "fb": "这样可能会让你忘了自己做到哪一步了。还可以试试：只说今天的自己——「我昨天改了三道错题，今天接着改」。"},
         {"t": "比什么比，我不写了。", "ok": False, "tense": 4, "room": 1,
          "feel": "不紧了，可是笔也放下了。",
          "fb": "这样可能会让你把一件本来会做的事一起放下。还可以试试：给自己换一个能算得清的目标——今天先写完前三行。"},
     ]},
    {"id": "a4", "t": "我必须让老师满意。",
     "opts": [
         {"t": "我想把这篇作文写得让自己也想再读一遍。写完先自己读一次，改一处。", "ok": True, "tense": 3, "room": 8,
          "feel": "手里的笔有自己的方向了，不再只在等一个人点头。",
          "fb": "把「让别人满意」换成「让自己也想再读一遍」，标准回到了你能摸到的地方。"},
         {"t": "老师要是有一点不满意，就说明我特别差。", "ok": False, "tense": 9, "room": 2,
          "feel": "每次交作业都像在等一个判决。",
          "fb": "这样可能会让你把一句评语当成对自己的结论。还可以试试：只挑评语里的一条，改一个地方。"},
         {"t": "反正怎么都不满意，那我就不认真了。", "ok": False, "tense": 4, "room": 1,
          "feel": "不紧张了，可是也不想使劲了。",
          "fb": "这样可能会让你连自己喜欢的那部分也丢掉。还可以试试：先只为自己写一段，看看自己满不满意。"},
     ]},
    {"id": "a5", "t": "我必须拿到那个奖。",
     "opts": [
         {"t": "我很想拿到那个奖，我更想把这件作品做到我自己满意。今天先改一个地方。", "ok": True, "tense": 3, "room": 8,
          "feel": "心里既有期待，也有能马上动手的地方。",
          "fb": "「很想拿到」和「必须拿到」不一样：前者留着空间，后者把结果提前写死了。"},
         {"t": "拿不到奖就等于白做了，那我就不做了。", "ok": False, "tense": 8, "room": 2,
          "feel": "还没开始，手里的材料就先放下了。",
          "fb": "这样可能会让你错过本来能做完的东西。还可以试试：先把目标改成做完，再想拿奖的事。"},
         {"t": "反正奖都是给别人的，我随便交一个算了。", "ok": False, "tense": 4, "room": 1,
          "feel": "心里空落落的，手也不太想动。",
          "fb": "这样可能会让你把喜欢这件事的那部分一起丢掉。还可以试试：找出这件作品里你最喜欢的一处，先把它做好。"},
     ]},
]

# ── 综合任务：我的学习理由卡 ──
CARD_SCENARIOS = [
    {"id": "music", "name": "练一样乐器",
     "musts": ["我必须一次就弹对", "我必须弹得比同学好", "我每天都必须练够一小时"],
     "wants": ["我想把这首曲子完整弹下来，因为我喜欢它安静下来的那一段。这周我先把最难的两小节单独练。",
               "我想弹给家里人听，因为我喜欢他们听完时的那个表情。今天先练到能连着弹完第一段。",
               "我想弄明白这个节奏是怎么回事。今天把这两小节放慢一半，练五遍。"],
     "likes": ["把最好听的那两小节多弹几遍，只为了听它", "录一小段，听一听自己这一周的变化",
               "找一首自己喜欢的曲子，随便弹着玩一会儿"]},
    {"id": "sport", "name": "参加一项运动",
     "musts": ["我必须跑第一", "我不能输给任何人", "我必须每天都练"],
     "wants": ["我想看看自己能跑多快，因为我喜欢跑到后来呼吸变匀的那种感觉。这周我先跑三次，每次只记时间。",
               "我想把动作做顺，因为我喜欢球进筐的那一下。今天先练二十次投篮，只数手感。",
               "我想和同伴配合得更好，因为一起打的时候很开心。今天先练传接十次。"],
     "likes": ["跑到微微出汗就停下来，只为了舒服", "试一个新动作，不管做得好不好",
               "和一个同学随便打一会儿，不算输赢"]},
    {"id": "read", "name": "读一本课外书",
     "musts": ["我必须读完老师推荐的每一本", "我必须读得比同学多", "我必须记住书里的好词好句"],
     "wants": ["我想知道后面发生了什么，因为我喜欢合上书还在想它的那种感觉。今天先读一章，只为了看下去。",
               "我想把这本书讲给同桌听，因为我喜欢讲的时候他眼睛发亮的样子。先挑出我最想讲的那一段。",
               "我想看看这个作者还写过什么。今天先翻一翻开头三页。"],
     "likes": ["挑最喜欢的那一段再读一遍，只为了读", "把书里的一句话抄在本子上，因为喜欢它",
               "随便翻到一页读五分钟，不记笔记"]},
    {"id": "make", "name": "做一个手工或实验",
     "musts": ["我必须一次就做成", "我做的必须比别人的好看", "我必须拿得出手给家长看"],
     "wants": ["我想看看它到底能不能做出我想要的样子，因为我喜欢动手改来改去。今天先把第一步做完。",
               "我想弄明白上一次为什么没成功，因为我好奇里面的道理。今天先只改一个地方再试一次。",
               "我想把它做到自己看着舒服，因为我喜欢最后那一眼。今天先修一修最不满意的那个角。"],
     "likes": ["多做一个玩一玩，不是为了交作业", "把一个零件拆开看看里面是什么样",
               "做一件很小的东西，自己留着"]},
]

CUSTOM_JS = r"""
/* ============================================================
   psych-e-g5-self-accept 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 理由辨别员：理由在事情里面 / 在事情外面（八张卡片两栏分类）
   3) 「我必须」改写台：三种改写 → 实时更新「绷紧程度 / 手上能做的事」两根条 + 感受描述
   4) 综合任务：我的学习理由卡（选事 → 挑「我必须」 → 改成「我想要…因为…」 → 配一件小事）
   ============================================================ */
(function () {
  'use strict';

  /* ---------- 1. 选择题接线 ---------- */
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

  /* ---------- 2. 理由辨别员 ---------- */
  var MOTIVES = __MOTIVES_JSON__;
  var BINS = __BINS_JSON__;
  var bank = document.getElementById('motive-bank');
  if (bank && MOTIVES.length) {
    var placedM = {}, pickedM = null;
    var outM = document.getElementById('motive-out');
    var scoreM = document.getElementById('motive-score');

    function mById(id) {
      for (var i = 0; i < MOTIVES.length; i++) { if (MOTIVES[i].id === id) return MOTIVES[i]; }
      return null;
    }
    function binName(id) {
      for (var i = 0; i < BINS.length; i++) {
        if (BINS[i].id === id) return BINS[i].name.replace(/^[①②]\s*/, '');
      }
      return '';
    }
    MOTIVES.forEach(function (it) {
      var b = document.createElement('button');
      b.className = 'sort-item';
      b.dataset.mcard = it.id;
      b.textContent = it.t;
      b.addEventListener('click', function () {
        if (placedM[it.id]) return;
        pickedM = it.id;
        document.querySelectorAll('[data-mcard]').forEach(function (x) {
          x.classList.toggle('selected', x.dataset.mcard === pickedM);
        });
        outM.className = 'result warn';
        outM.innerHTML = '<strong>你选中了：</strong>' + it.t + '<br>它属于哪一栏？点一下上面两栏中的一个。';
      });
      bank.appendChild(b);
    });
    BINS.forEach(function (bn) {
      var box = document.getElementById('motive-bin-' + bn.id);
      if (!box) return;
      box.addEventListener('click', function () {
        if (!pickedM) {
          outM.className = 'result warn';
          outM.textContent = '先在左边点一句，再点这一栏。';
          return;
        }
        var it = mById(pickedM);
        if (!it || placedM[it.id]) return;
        if (it.bin !== bn.id) {
          outM.className = 'result warn';
          outM.innerHTML = '<strong>这一句再想一想。</strong>' + it.fb +
            '<br>它更合适放在「' + binName(it.bin) + '」那一栏，换一栏再点一次试试。';
          return;
        }
        placedM[it.id] = true;
        var card = document.querySelector('[data-mcard="' + it.id + '"]');
        if (card) { card.classList.add('done'); card.classList.remove('selected'); }
        var tag = document.createElement('span');
        tag.className = 'tag';
        tag.textContent = it.t;
        box.querySelector('.bin-list').appendChild(tag);
        box.classList.add('ok');
        pickedM = null;
        var n = Object.keys(placedM).length;
        scoreM.textContent = '已经分好 ' + n + ' / ' + MOTIVES.length + ' 句';
        outM.className = 'result';
        outM.innerHTML = '<strong>分对了。</strong>' + it.fb;
        if (n === MOTIVES.length) {
          outM.className = 'result';
          outM.innerHTML = '<strong>八句话都分好了。</strong>两种理由我们都会有，这很正常，不用把外面那一栏丢掉。' +
            '好用的办法是：<strong>在事情外面那个理由旁边，慢慢加上一个事情里面的理由</strong>。';
        }
      });
    });
    scoreM.textContent = '已经分好 0 / ' + MOTIVES.length + ' 句';
  }

  /* ---------- 3. 「我必须」改写台（实时感受变化） ---------- */
  var MUSTS = __MUSTS_JSON__;
  var stage = document.getElementById('must-stage');
  if (stage && MUSTS.length) {
    var curM = null, doneM = {};
    var outT = document.getElementById('must-out');
    var scoreT = document.getElementById('must-score');
    var tenseFill = document.getElementById('must-tense');
    var roomFill = document.getElementById('must-room');
    var tenseNum = document.getElementById('must-tense-num');
    var roomNum = document.getElementById('must-room-num');
    var feelBox = document.getElementById('must-feel');

    function mustById(id) {
      for (var i = 0; i < MUSTS.length; i++) { if (MUSTS[i].id === id) return MUSTS[i]; }
      return null;
    }
    function renderM() {
      document.querySelectorAll('[data-must]').forEach(function (b) {
        var k = b.dataset.must;
        b.classList.toggle('selected', k === curM);
        b.classList.toggle('done', !!doneM[k]);
      });
      scoreT.textContent = '已经改写 ' + Object.keys(doneM).length + ' / ' + MUSTS.length + ' 句';
    }
    function paintTense(tense, room, feel) {
      if (!tenseFill) return;
      tenseFill.style.width = (tense * 10) + '%';
      roomFill.style.width = (room * 10) + '%';
      tenseNum.textContent = tense + ' / 10';
      roomNum.textContent = room + ' / 10';
      if (feelBox) {
        feelBox.className = (tense >= 7 ? 'result warn' : 'result');
        feelBox.innerHTML = '<strong>这样说的感觉：</strong>' + feel;
      }
    }
    function paintM() {
      var box = document.getElementById('must-opts');
      box.innerHTML = '';
      if (!curM) return;
      var S = mustById(curM);
      if (!S) return;
      var head = document.createElement('p');
      head.style.cssText = 'margin:0 0 8px;color:var(--muted);font-size:14px';
      head.textContent = '心里那句话：「' + S.t + '」　下面有三种改写，选一个试试。';
      box.appendChild(head);
      S.opts.forEach(function (o) {
        var b = document.createElement('button');
        b.className = 'choice' + (doneM[curM] && o.ok ? ' correct' : '');
        b.style.textAlign = 'left';
        b.textContent = o.t;
        b.addEventListener('click', function () {
          paintTense(o.tense, o.room, o.feel);
          if (doneM[curM]) return;
          if (o.ok) {
            doneM[curM] = true;
            outT.className = 'result';
            outT.innerHTML = '<strong>这一句站得住。</strong>' + o.fb;
          } else {
            outT.className = 'result warn';
            outT.innerHTML = '<strong>这句话很多人心里都冒出来过，我们看看它会带来什么。</strong>' + o.fb;
          }
          renderM();
          paintM();
        });
        box.appendChild(b);
      });
    }
    document.querySelectorAll('[data-must]').forEach(function (b) {
      b.addEventListener('click', function () {
        curM = b.dataset.must;
        var S = mustById(curM);
        if (doneM[curM]) {
          outT.className = 'result';
          outT.innerHTML = '<strong>这一句已经改写过了。</strong>记住那个句式：我希望（什么），我更想（把哪件事弄懂），我先做（一个具体的小动作）。';
        } else {
          outT.className = 'result warn';
          outT.innerHTML = '<strong>心里冒出来的是：「' + S.t + '」</strong><br>下面有三种改写，选一个试试，看看两根条会怎么动。';
        }
        renderM();
        paintM();
      });
    });
    renderM();
  }

  /* ---------- 4. 综合任务：我的学习理由卡 ---------- */
  var SCEN = __SCEN_JSON__;
  var sWrap = document.getElementById('card-scen');
  if (sWrap && SCEN.length) {
    var curC = null, pickMust = '', pickWant = '', pickLike = '';
    var outC = document.getElementById('card-out');
    var cardBox = document.getElementById('card-result');
    var prev = document.getElementById('card-preview');

    function cById(id) {
      for (var i = 0; i < SCEN.length; i++) { if (SCEN[i].id === id) return SCEN[i]; }
      return null;
    }
    function cName(id) { var s = cById(id); return s ? s.name : ''; }

    function renderPreview() {
      if (!prev) return;
      if (!curC) { prev.innerHTML = '先在第一步选一件事。'; return; }
      var lines = ['<strong>这件事：</strong>' + cName(curC)];
      lines.push('<strong>原来的说法：</strong>' + (pickMust || '还没挑'));
      lines.push('<strong>改过来的说法：</strong>' + (pickWant || '还没挑'));
      lines.push('<strong>喜欢这件事本身的一件小事：</strong>' + (pickLike || '还没挑'));
      prev.className = 'result';
      prev.innerHTML = lines.join('<br>');
    }
    function renderChips() {
      var s = cById(curC);
      if (!s) return;
      [['card-musts', s.musts, 'pickMust'], ['card-wants', s.wants, 'pickWant'], ['card-likes', s.likes, 'pickLike']]
        .forEach(function (triple) {
          var box = document.getElementById(triple[0]);
          if (!box) return;
          box.innerHTML = '';
          triple[1].forEach(function (txt) {
            var b = document.createElement('button');
            var isSel = (triple[2] === 'pickMust' && pickMust === txt) ||
                        (triple[2] === 'pickWant' && pickWant === txt) ||
                        (triple[2] === 'pickLike' && pickLike === txt);
            b.className = 'choice' + (isSel ? ' selected' : '');
            b.style.cssText = 'text-align:left;font-size:14px;padding:10px 12px;margin:4px 0';
            b.textContent = txt;
            b.addEventListener('click', function () {
              if (triple[2] === 'pickMust') pickMust = txt;
              if (triple[2] === 'pickWant') pickWant = txt;
              if (triple[2] === 'pickLike') pickLike = txt;
              renderChips();
              renderPreview();
              if (cardBox) cardBox.innerHTML = '';
            });
            box.appendChild(b);
          });
        });
    }
    document.querySelectorAll('[data-cscen]').forEach(function (b) {
      b.addEventListener('click', function () {
        curC = b.dataset.cscen;
        pickMust = ''; pickWant = ''; pickLike = '';
        document.querySelectorAll('[data-cscen]').forEach(function (x) {
          x.classList.toggle('selected', x === b);
        });
        renderChips();
        renderPreview();
        if (cardBox) cardBox.innerHTML = '';
        outC.className = 'result warn';
        outC.innerHTML = '<strong>选好了：' + cName(curC) + '。</strong>接着挑一句你心里冒出来的「我必须」，再挑一句改过来的说法。';
      });
    });
    var genC = document.getElementById('card-gen');
    if (genC) {
      genC.addEventListener('click', function () {
        if (!curC) {
          outC.className = 'result warn';
          outC.textContent = '先在第一步选一件事。';
          return;
        }
        var like = document.getElementById('card-like-text');
        var a = document.getElementById('card-a');
        var b2 = document.getElementById('card-b');
        var c2 = document.getElementById('card-c');
        var likeTxt = (like && like.value.trim()) || '（还没写）';
        var aTxt = (a && a.value.trim()) || '（还没写）';
        var bTxt = (b2 && b2.value.trim()) || '（还没写）';
        var cTxt = (c2 && c2.value.trim()) || '（还没写）';
        var miss = [];
        if (!pickMust) miss.push('原来的说法');
        if (!pickWant) miss.push('改过来的说法');
        if (!pickLike) miss.push('喜欢这件事本身的小事');
        if (cardBox) {
          cardBox.className = 'result';
          cardBox.innerHTML =
            '<strong>我的学习理由卡 · ' + cName(curC) + '</strong><br>' +
            '① 原来的说法：' + (pickMust || '（还没挑）') + '<br>' +
            '② 改过来的说法：' + (pickWant || '（还没挑）') + '<br>' +
            '③ 喜欢这件事本身的一件小事：' + (pickLike || '（还没挑）') + '<br>' +
            '④ 我喜欢做的事：' + aTxt + '<br>' +
            '⑤ 我做起来有点吃力的事：' + bTxt + '<br>' +
            '⑥ 我想多试试的事：' + cTxt + '<br>' +
            '⑦ 我为自己留的一句话：' + likeTxt;
        }
        outC.className = miss.length ? 'result warn' : 'result';
        outC.innerHTML = miss.length
          ? '<strong>卡片生成了，还差几格：</strong>' + miss.join('、') + '。补上就是一张完整的卡。'
          : '<strong>卡片做好了。</strong>把它抄在纸上，贴在书桌前。最后那一句，是留给你自己的。';
      });
    }
    renderPreview();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__MOTIVES_JSON__', json.dumps(MOTIVES, ensure_ascii=False))
             .replace('__BINS_JSON__', json.dumps(MOTIVE_BINS, ensure_ascii=False))
             .replace('__MUSTS_JSON__', json.dumps(MUSTS, ensure_ascii=False))
             .replace('__SCEN_JSON__', json.dumps(CARD_SCENARIOS, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "下面哪个理由，更可能让你把一件事做很久？",
         "options": [("因为我很想知道后面怎么样了，读的时候会忘记时间", True),
                     ("因为做完才能换一个新玩具", False),
                     ("因为不做完就会被说", False)],
         "explain": "理由在事情里面的时候，做的时候就已经在享受了，不用别人来加油。"
                    "<strong>错因提醒：</strong>常见错误是误认为「为了得到什么才做就是不好的」——不是好不好的问题，是这份力气能撑多久的问题。"},
        {"q": "「我必须考第一」这句话，问题出在哪里？",
         "options": [("它把结果提前写死了，可结果并不完全由我决定", True),
                     ("它说明这个同学太不用功了", False),
                     ("它说明这个同学不想考好", False)],
         "explain": "名次要看好几个因素，把结果提前写死，等于把绳子套在自己身上。"
                    "<strong>错因提醒：</strong>最容易搞混的是「想考好」和「必须考第一」——前者留着空间，后者把结果钉死了。"},
        {"q": "下面哪一句，是把「我必须」改成了站得住的版本？",
         "options": [("我希望考得好，我更想弄懂这几道题。这周我先把错题整理一遍。", True),
                     ("算了吧，考第几都无所谓，随便考考。", False),
                     ("我必须考第一，考不到就完了。", False)],
         "explain": "站得住的说法里，希望还在、要求还在，只是把它放到了自己能做的那一部分上。"
                    "<strong>错因提醒：</strong>有人误认为「改说法就是降低要求」——把要求扔掉不是站得住，那是另一种停下。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "理由在事情里面，还是在事情外面", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道怎么把「我不会」改成「我还没学会」，也知道难受的时候先量一量温度（And）；可是很多同学做一件事的理由，是「不做会被说」「做完才有奖励」，这些理由能让今天动起来，却很难陪你走很久（But）；所以这节课先看清一件事——我做它，是因为喜欢它本身，还是为了得到什么（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">同一件事，可以有两个不一样的<strong>理由</strong>。理由在哪里，很大程度上决定这件事能走多远。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>① 理由在事情里面</strong></p>
            <p style="color:var(--muted)">因为喜欢它本身：想把这首曲子弹给奶奶听、一直好奇这道题为什么会这样。做的时候就已经在享受了。</p>
          </div>
          <div class="inner-card">
            <p><strong>② 理由在事情外面</strong></p>
            <p style="color:var(--muted)">为了得到什么才做：做完才有奖励、不做会被说。它能让人动起来，可奖励拿完、没人说了，力气就小了。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="同一件事两种理由对照示意图：理由在事情里面与理由在事情外面，附中文标注">
          <figcaption>示意图：同一件事的两种理由——理由在事情里面，还是理由在事情外面（教学示意图，中性简洁插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>两种理由都不用丢掉：</strong></p>
          <p style="color:var(--muted)">可以这样做——<strong>留着外面那个理由，同时加上一个里面的理由</strong>。比如「练够十次换新玩具」旁边，加一句「我想把最好听的那两小节弹顺」。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「为了奖励才做就是不对的，一定要喜欢才配做」。这里最容易<strong>搞混</strong>的是两件事：喜欢不喜欢，和这件事值不值得做，是两个问题。奖励本身没有错，它只是撑不了太久。<strong>要看的不是理由好不好，而是这份理由能陪你走多远。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "找一找：这件事里有没有一个瞬间，是你做的时候自己也挺喜欢的？那一瞬间，就是里面的理由。"},
    {"lens": "比较它", "text": "「做完才有奖励」和「我想把它弹顺」：前者停下来就没了，后者停下来还在心里。"},
    {"lens": "迁移它", "text": "写作业、练琴、跑步、做手工，都可以用一次：我现在的理由在事情里面，还是在外面？可以加上哪一句？"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>外面那个理由可以留着——<strong>再往里面添一句「我喜欢它的哪一点」。</strong></div></div>
    ''', tag="概念一"))

    motive_bins = "\n".join(
        f'''            <div class="sort-bin" id="motive-bin-{b["id"]}" role="button" tabindex="0">
              <h4>{b["name"]}</h4>
              <div class="bin-list"></div>
            </div>'''
        for b in MOTIVE_BINS
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：理由辨别员，这句话的理由在哪里", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">八句话都是我们做一件事时心里的理由。先在左边点一句，再点上面两栏中的一个。<strong>分得不太合适也不会说你错</strong>，我会告诉你这个理由能陪你走多久。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 八句话（点一句选中）</div>
          <div class="sort-bank" id="motive-bank"></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 这句话的理由在哪里</div>
          <div class="sort-bins">
{motive_bins}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">分类进度</span><span class="v" id="motive-score">已经分好 0 / 8 句</span></div>
          </div>
          <p class="result warn" id="motive-out" style="margin-top:12px">先在左边点一句。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>写一句你自己的：</strong></p>
          <p style="color:var(--muted)">挑一件你正在做的事，写下你现在的理由，再想一句可以加在里面的理由。</p>
          <textarea id="motive-answer" rows="2" placeholder="我做这件事，是因为……　我还想加上一句：我喜欢它的……" style="margin-top:8px"></textarea>
        </div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "把「我必须考第一」改一改，改成站得住的版本", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">像「我必须考第一」「我不能出一点错」这样的话，有一个共同点：<strong>它们把结果提前写死了</strong>，而结果并不完全由我决定。</p>
        <div class="grid grid-3">
          <div class="inner-card">
            <p><strong>「我必须考第一」</strong></p>
            <p style="color:var(--muted)">结果被提前钉死。心里像被一根绳子绷住，越想越紧，手反而抬不起来。</p>
          </div>
          <div class="inner-card">
            <p><strong>「随便吧，无所谓」</strong></p>
            <p style="color:var(--muted)">看着轻松，其实把要求整个扔掉了。不紧了，可手也停下来，这不是站得住。</p>
          </div>
          <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
            <p><strong>站得住的说法</strong></p>
            <p style="color:var(--muted)">「我希望考得好，我更想弄懂这几道题。这周我先把错题整理一遍。」要求还在，只是放在能做的事上。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="把「我必须考第一」改成站得住版本的图示，附中文标注">
          <figcaption>示意图：「我必须考第一」→「我希望考得好，我更想弄懂这几道题」——要求还在，位置换到了能做的事上（教学示意图，中性简洁插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>站得住的说法，长这个样子：</strong></p>
          <p style="color:var(--muted)"><strong>我希望</strong>（什么结果）<strong>＋ 我更想</strong>（把哪件事弄懂 / 做好）<strong>＋ 我先做</strong>（一个今天就能动的小动作）。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「把「我必须」改掉，就是把要求降低了，等于不努力了」。这里最容易<strong>搞混</strong>的是「放下要求」和「换个位置放要求」——站得住的说法里，希望还在、目标还在，只是从「一定要得到某个结果」换成了「我先做我能做的那一部分」。<strong>要求没变轻，是它终于落到了你手上。</strong></p>
        </div>
{insight_box([
    {"lens": "拆开它", "text": "一句话可以拆成两段：一段是想要的结果，一段是能做的动作。「我必须」只留了前一段，「我希望……我先做……」两段都有。"},
    {"lens": "解释它", "text": "为什么换一种说法，心里就松了？因为注意力从「结果会不会好」移到了「我现在做什么」——后者你能说了算。"},
    {"lens": "迁移它", "text": "比赛、演出、选班干部、和家长约定，凡是心里冒出「我必须」，都可以补上「更想弄懂什么」和「先做什么」。"},
])}
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🎵</span><div><strong>记一句口诀：</strong>我希望，我更想，我先做——<strong>把结果提前写死，不如把下一步写清。</strong></div></div>
    ''', tag="概念二"))

    must_btns = "\n".join(
        f'            <button class="choice" data-must="{s["id"]}" style="text-align:left">{s["t"]}</button>'
        for s in MUSTS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：「我必须」改写台，看看心里的变化", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">五句「我必须」在下面。点开一句，再从三种改写里选一个——<strong>选完之后两根条会马上动起来</strong>：上面那根是绷紧的程度，下面那根是手上能做的事。选得不太合适也不会批评你。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 心里冒出来的那一句</div>
          <div class="grid" id="must-stage">
{must_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 换一种说法试试</div>
          <div class="grid" id="must-opts">
            <span style="color:var(--muted);font-size:14px">先在上面点一句，这里就会出现三种改写。</span>
          </div>
          <div style="margin-top:16px;background:var(--bg-subtle);border:1px solid var(--line-subtle);border-radius:12px;padding:12px">
            <div style="font-size:13px;color:var(--muted);margin-bottom:6px">心里的变化（选一句改写，两根条会实时变化）</div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px">
              <span style="min-width:96px;font-size:13px;font-weight:700">绷紧的程度</span>
              <div style="flex:1;height:16px;border-radius:8px;background:rgb(var(--paper-rgb) / .18);overflow:hidden">
                <div id="must-tense" style="height:100%;width:0%;border-radius:8px;background:linear-gradient(90deg,var(--warm),var(--danger));transition:width .35s ease"></div>
              </div>
              <span id="must-tense-num" style="min-width:52px;text-align:right;font-weight:800;color:var(--muted)">0 / 10</span>
            </div>
            <div style="display:flex;align-items:center;gap:10px">
              <span style="min-width:96px;font-size:13px;font-weight:700">手上能做的事</span>
              <div style="flex:1;height:16px;border-radius:8px;background:rgb(var(--paper-rgb) / .18);overflow:hidden">
                <div id="must-room" style="height:100%;width:0%;border-radius:8px;background:linear-gradient(90deg,var(--brand-2),var(--brand));transition:width .35s ease"></div>
              </div>
              <span id="must-room-num" style="min-width:52px;text-align:right;font-weight:800;color:var(--muted)">0 / 10</span>
            </div>
          </div>
          <p class="result warn" id="must-feel" style="margin-top:12px">选一句改写，看看这样说的感觉。</p>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">改写进度</span><span class="v" id="must-score">已经改写 0 / 5 句</span></div>
          </div>
          <p class="result warn" id="must-out" style="margin-top:12px">先点一句你自己也说过的话。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💛</span><div><strong>两根条没有「对」的数字：</strong>它们只是让你看见，同一件事换一种说法，心里的感受真的会不一样。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小禾的第二次月考", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>第二次月考成绩出来了，小禾是班里第三名。她一整天都提不起劲，心里那句话是——我必须考第一，第三名就是没考好。请你陪她走四步。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看看这句「我必须」：</strong>它把名次提前写死了。可名次要看好几个因素，并不全由她决定——绳子是自己套上去的。</div></div>
          <div class="step"><span class="n">2</span><div><strong>把想法改一改：</strong>「我希望考得好，我更想弄懂这次错的三道题。」希望还在，位置换到了能做的事上。</div></div>
          <div class="step"><span class="n">3</span><div><strong>找一找喜欢这件事本身的地方：</strong>小禾最喜欢语文课上的那篇课文，读的时候会忘记时间。今天先把那一篇读第二遍，只为了读。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>看看自己的三个样子：</strong>喜欢做的事——读故事；有点吃力的事——列竖式容易漏掉进位；想多试试的事——在小组里讲一次自己读到的故事。三个都是她。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「悦纳自己，就是觉得自己什么都好」。这里最容易<strong>搞混</strong>的是「看见吃力的地方」和「不接纳自己」——悦纳不是假装没有吃力的地方，而是把喜欢的样子、有点吃力的样子、想多试试的样子<strong>放在一起看</strong>，不因为其中一个吃力，就否掉另外两个。</p>
        </div>
        <div class="inner-card">
          <p><strong>和同桌评价一下：</strong>小禾这四步里，哪一步你自己已经做到了？哪一步还想再练一练？你觉得哪一步对你更管用，为什么？</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于「理由在事情里面」和「理由在事情外面」，下面哪种理解更合适？",
         "options": [("两种理由我们都会有，可以留着外面的，再加上一个里面的", True),
                     ("为了得到奖励才做，说明这个同学品格有问题", False),
                     ("只要喜欢一件事本身，就一定能做好", False)],
         "explain": "奖励没有错，它只是撑不了太久；喜欢也不是万能的，它让你更愿意开始。"
                    "<strong>错因提醒：</strong>常见错误是误认为「喜欢就一定能做好」——喜欢让你愿意开始，做好还要靠方法和时间。"},
        {"q": "「把「我必须」改成站得住的版本」和「降低要求」，有什么不同？",
         "options": [("站得住的说法里希望还在，只是把要求放到了能做的事上", True),
                     ("两者完全一样，都是给自己找台阶", False),
                     ("站得住的说法就是把目标定低一点", False)],
         "explain": "要求没有变轻，是它终于落到了你手上：希望还在，多了一个今天能做的动作。"
                    "<strong>错因提醒：</strong>最容易搞混的是「放下要求」和「换个位置放要求」——「随便考考」是把要求扔了，那只是另一种停下。"},
        {"q": "下面哪一句，理由在事情外面？",
         "options": [("我练这首曲子，因为练够十次就能换一个新玩具", True),
                     ("我练这首曲子，因为我想弹给奶奶听", False),
                     ("我练这首曲子，因为我喜欢它安静下来的那一段", False)],
         "explain": "换玩具这个理由在事情外面，靠的是别人给的东西；另外两句的理由都在曲子本身。"
                    "<strong>错因提醒：</strong>有人误认为「说完奖励就一定要删掉」——不用删，再加一句里面的理由就好。"}
    ], tag="概念测试"))

    cscen_btns = "\n".join(
        f'            <button class="choice" data-cscen="{s["id"]}" style="text-align:center">{s["name"]}</button>'
        for s in CARD_SCENARIOS
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：做一张我的学习理由卡", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">选一件你正在做的事 → 挑一句你心里冒出来的「我必须」→ 改成「我想要……因为……」→ 配一件喜欢这件事本身的小事 → 写下你的三个样子。做完，归纳一下：这张卡里哪一句最像你自己。<strong>没挑完也不扣分</strong>，我会提示你还差哪几格。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 选一件你正在做的事</div>
          <div class="grid grid-2">
{cscen_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 挑一句你心里冒出来的「我必须」</div>
          <div class="grid" id="card-musts"><span style="color:var(--muted);font-size:14px">先在第一步选一件事。</span></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 改成「我想要……因为……」</div>
          <div class="grid" id="card-wants"><span style="color:var(--muted);font-size:14px">先在第一步选一件事。</span></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">④ 配一件「喜欢这件事本身」的小事</div>
          <div class="grid" id="card-likes"><span style="color:var(--muted);font-size:14px">先在第一步选一件事。</span></div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">⑤ 写下你的三个样子</div>
          <div class="grid grid-3">
            <label style="font-size:13px;color:var(--muted)">我喜欢做的事
              <textarea id="card-a" rows="2" placeholder="例如：读故事" style="margin-top:6px"></textarea>
            </label>
            <label style="font-size:13px;color:var(--muted)">我做起来有点吃力的事
              <textarea id="card-b" rows="2" placeholder="例如：列竖式容易漏进位" style="margin-top:6px"></textarea>
            </label>
            <label style="font-size:13px;color:var(--muted)">我想多试试的事
              <textarea id="card-c" rows="2" placeholder="例如：在小组里讲一次" style="margin-top:6px"></textarea>
            </label>
          </div>
          <label style="display:block;font-size:13px;color:var(--muted);margin-top:12px">我为自己留的一句话
            <input id="card-like-text" placeholder="例如：慢一点也没关系，我想把这一篇读完" style="margin-top:6px">
          </label>
          <div class="flex-row">
            <button class="choice" id="card-gen" style="text-align:center">⑥ 生成我的学习理由卡</button>
          </div>
          <p class="result warn" id="card-out" style="margin-top:12px">先在第一步选一件事。</p>
          <p id="card-preview" class="result" style="margin-top:10px">先在第一步选一件事。</p>
          <p id="card-result" style="margin-top:10px"></p>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换三个新情境，办法还在不在", TTS["posttest"], [
        {"q": "跳绳你练了三个月，这个月停下来了，也不太想再跳。下面哪个做法更可能让你重新跳起来？",
         "options": [("想一想当初喜欢跳的哪一点，今天只跳一分钟，就是为了跳", True),
                     ("告诉自己：必须每天跳一千个，跳不完就不许休息", False),
                     ("算了，练了也不一定能拿名次", False)],
         "explain": "回到那个里面的理由，再把门槛放低到一分钟，比给自己加一根绳子更容易重新开始。"
                    "<strong>错因提醒：</strong>常见错误是误认为「停下来了就是不自律」——有时候是理由用完了，需要往里面添一句。"},
        {"q": "「我必须每次都让老师满意」改成下面哪一句更站得住？",
         "options": [("我想把这篇作文写得让自己也想再读一遍。写完先自己读一次，改一处", True),
                     ("老师不满意就说明我特别差", False),
                     ("反正怎么都不满意，那我就不认真写了", False)],
         "explain": "标准回到自己能摸到的地方，还配了一个今天就能做的动作。"
                    "<strong>错因提醒：</strong>最容易搞混的是「看别人的评价」和「把别人的评价当成对自己的结论」——一句评语是关于一篇作文的，不是关于你这个人。"},
        {"q": "好朋友的画画得比你好，你有点不想画了。下面哪个做法更合适？",
         "options": [("先承认自己有点羡慕，再回到自己最喜欢画的那一种东西上，今天画一小张", True),
                     ("从此不画了，反正怎么画都比不上他", False),
                     ("每天逼自己画十张，一定要超过他", False)],
         "explain": "羡慕是很自然的心情；回到喜欢的那个点上，手上的笔才会自己动起来。"
                    "<strong>错因提醒：</strong>有人误认为「要比过别人才能喜欢自己」——喜欢画画这件事，从来不需要你先赢过谁。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，讲清悦纳自己和学习动机", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>看一看理由在哪里：</strong>理由在事情里面能走更久。外面那个理由可以留着，再往里面添一句「我喜欢它的哪一点」。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>把「我必须」改一改：</strong>我希望……我更想弄懂……我先做……——要求没变轻，是它落到了你手上。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>三个样子都是你：</strong>喜欢的样子、有点吃力的样子、想多试试的样子，放在一起看，不用改掉哪一个才值得被喜欢。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还要记牢一件事：</strong>有时候怎么都提不起劲，做什么都没意思，这不是一句「不努力」能解释的，也不是你一个人会遇到的。如果这种状态持续了一段时间，把它说给老师或者爸爸妈妈听，是很聪明的做法。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「里面的理由、我必须、三个样子」这三个词，说清楚你最近做一件事的经过。</p>
          <p style="color:var(--muted)">再动一动手：<strong>画出</strong>你的学习理由卡，左边写「我必须」的原话，右边写改过来的说法，下面留一行写你为自己留的那句话。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出三件你正在做的事，每件事写下你现在的理由，再说说这个理由在事情里面还是外面。",
            "说出「我必须考第一」和「我希望考得好，我更想弄懂这几道题」有什么不一样。",
            "说出「站得住的说法」和「随便考考」有什么不一样。",
        ],
        [
            "挑一句你心里说过的「我必须」，把它改写成「我希望……我更想……我先做……」的版本，再把心里的变化写两句。",
            "为一件你只为奖励才做的事，找出一个你喜欢的那个点，写下来。",
        ],
        [
            "这一周里，用设计一张学习理由卡的方式记录一件事：原来的说法、改过来的说法、喜欢它的哪一点、做完以后的感受。",
            "和同桌一起想一想：我们班里还有哪些说法，能把「我必须」改得站得住？写出两条。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "psych-e-g5-self-accept",
    "node_id": "psych-e-g5-self-accept",
    "subject": "psychology",
    "subject_cn": "心理健康",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "中小学心理健康教育指导纲要（2012年修订）/ 教育部相关要求 · 小学",
    "title": "悦纳自我与学习动机",
    "name_en": "Self-Acceptance and Learning Motivation",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "self-awareness",
    "domain_cn": "认识自我",
    "lesson_type": "workshop",
    "version": "1.0.0",
    "description": "面向小学五年级的认识自我课：先看清一件事的两种理由——「喜欢这件事本身」（理由在事情里面）和「为了得到什么才做」（理由在事情外面），再练习把「我必须考第一」这类想法改成站得住的版本（我希望……我更想弄懂……我先做……），并在改写的一瞬间实时看到「绷紧的程度」和「手上能做的事」两根条的变化；最后把喜欢的样子、有点吃力的样子、想多试试的样子放在一起看，在各种活动中悦纳自己。三个互动台子都能真的操作：理由辨别员（八句话分两栏，分错会说明这个理由能陪你走多久）、「我必须」改写台（五句各配三种改写，实时驱动感受条与感受描述），以及综合任务里从选事、改写、配小事到生成「我的学习理由卡」的完整模拟。全课语气温和、不评判、不贴标签，不使用任何临床诊断词汇，不涉及自伤自杀话题，插图一律为中性简洁的教学插画。",
    "tags": ["悦纳自我", "学习动机", "内在动机", "外在奖励", "五年级", "认识自我"],
    "standard_ref": "《中小学心理健康教育指导纲要（2012年修订）· 小学中高年级》认识自我——帮助学生正确认识自己的优缺点和兴趣爱好，在各种活动中悦纳自己；着力培养学生的学习兴趣和学习能力，端正学习动机，调整学习心态，正确对待成绩，体验学习成功的乐趣。",
    "hero_question": "心里那句「我必须考第一，考不到就完了」，一想起来就绷得紧紧的——同一件事，能不能换一个站得住的说法？",
    "hero_alt": "悦纳自我与学习动机知识结构图：理由在事情里面、把「我必须」改一改、三个样子都是你 三栏",
    "hero_caption": "悦纳自我与学习动机：看清理由在哪里 · 把「我必须」改一改 · 三个样子都是你",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "「喜欢这件事本身」和「为了奖励才做」，到底差在哪里？", "d": "两种感觉我都懂，可说不清哪一种更靠得住", "v": "喜欢这件事本身和为了奖励才做到底差在哪里"},
        {"t": "想把「我必须考第一」改一改，可不知道怎么改？", "d": "这句话一冒出来，人就绷住了", "v": "想把必须考第一改一改可不知道怎么改"},
        {"t": "改掉「我必须」，是不是就等于降低要求？", "d": "怕自己一放松就真的不努力了", "v": "改掉我必须是不是就等于降低要求"},
        {"t": "怎么才能真的喜欢上自己做的事？", "d": "想知道那个「里面的理由」从哪里找", "v": "怎么才能真的喜欢上自己做的事"},
    ],
    "objectives": [
        "能说出一件事的两种理由，知道理由在事情里面和在事情外面有什么不一样",
        "能把「我必须考第一」这类想法改成站得住的版本，并说出心里的感受有什么变化",
        "能说出「站得住的说法」和「降低要求」不是一回事",
        "能把自己的喜欢、有点吃力和想多试试的样子放在一起看一看，说出三个样子都是自己",
    ],
    "objectives_plain": [
        "能说出一件事的两种理由，知道理由在事情里面和在事情外面有什么不一样",
        "能把「我必须考第一」这类想法改成站得住的版本，并说出心里的感受有什么变化",
        "能说出「站得住的说法」和「降低要求」不是一回事",
        "能把自己的喜欢、有点吃力和想多试试的样子放在一起看一看，说出三个样子都是自己",
    ],
    "standards": [
        {"content": "帮助学生正确认识自己的优缺点和兴趣爱好，在各种活动中悦纳自己",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 认识自我"},
        {"content": "着力培养学生的学习兴趣和学习能力，端正学习动机，调整学习心态，正确对待成绩，体验学习成功的乐趣",
         "source": "《中小学心理健康教育指导纲要（2012年修订）》小学中高年级 · 认识自我"},
    ],
    "prereqs": ["psych-e-g4-study-motivation"],
    "prereqs_name": "学习自信与情绪表达",
    "prereqs_meta": "psych-e-g4-study-motivation",
    "leads_to": ["psych-e-g5-negative-emotion"],
    "next_meta": "psych-e-g5-negative-emotion",
    "section_images": ["assets/psych-e-g5-self-accept-fig1.webp",
                       "assets/psych-e-g5-self-accept-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "「我必须考第一」一冒出来人就绷住了——这节课教你把同一件事换一个站得住的说法，并看见心里的变化。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能改写自己的一句「我必须」，也能做出一张学习理由卡。",
        "objectives": "看清四件事：两种理由差在哪里、怎么改「我必须」、站得住和降低要求的区别、三个样子都是你。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "理由在事情里面能走更久；外面那个理由留着，再往里面添一句「我喜欢它的哪一点」。",
        "lab-1": "重点不是分得快，而是看看每一句的理由能陪你走多久。",
        "module-2": "「我必须」把结果提前写死；改成「我希望……我更想弄懂……我先做……」，要求还在，位置换了。",
        "lab-2": "选一句改写，看两根条怎么动——绷紧的程度降下来，手上能做的事升上去。",
        "worked-example": "小禾四步：看「我必须」、改说法、找喜欢的那一点、看自己的三个样子。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "选事 → 挑「我必须」 → 改写 → 配一件小事 → 写三个样子 → 生成理由卡。",
        "posttest": "出现了停下来的跳绳、希望老师满意的作文、朋友画得比你好，看看你能不能用上今天的办法。",
        "summary": "三句话：看清理由在哪里、把「我必须」改一改、三个样子都是你。",
        "homework": "三层小任务，先做前两层，第三层可以请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先帮你找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学心理健康「认识自我」在五年级的空缺，正对课标「帮助学生正确认识自己的优缺点和兴趣爱好，在各种活动中悦纳自己」「着力培养学生的学习兴趣和学习能力，端正学习动机，调整学习心态，正确对待成绩，体验学习成功的乐趣」。五年级学生的难点有两个：① 学习上的理由大多是外面的——不做会被说、做完才有奖励，这些理由能启动却撑不久，一停下来就不想再动，而学生说不清「喜欢这件事本身」长什么样；② 心里那根绳子是「我必须考第一」「我不能出一点错」这类把结果提前写死的句子，一冒出来人就绷住，可学生担心一改就等于不努力，于是只能在「绷住」和「随便」之间来回。所以全课围绕两件可操作的事：概念一给出两种理由的对照（理由在事情里面 / 在事情外面）并明确「不用丢掉外面的理由，可以再加上一个里面的理由」；概念二给出站得住说法的三件套（我希望…… ＋ 我更想弄懂…… ＋ 我先做……），并把它与「降低要求」明确区分开。三个台子都能真的操作：理由辨别员（八句话分两栏，选错不放行并说明这个理由能陪你走多久，另留一个自由文本框）、「我必须」改写台（五句各配三种改写，每选一句都会实时驱动「绷紧的程度」与「手上能做的事」两根条和一句感受描述，让同一件事换一种说法带来的感受变化直接看得见），以及综合任务里的完整模拟——选一件正在做的事 → 挑一句「我必须」→ 改成「我想要……因为……」→ 配一件喜欢这件事本身的小事 → 写下三个样子 → 生成「我的学习理由卡」。悦纳自我贯穿例题（小禾的三个样子）与综合任务；全课语气温和、不评判、不贴标签，不使用任何临床诊断词汇，不涉及自伤自杀话题；插图一律为中性简洁的教学插画，不使用真实儿童照片风格人像。",
    "plan_table": """| 1 | cover | 悦纳自我与学习动机 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 理由在事情里面，还是在事情外面 | 承·概念一（两种理由） |
| 6 | interactive | 动手一：理由辨别员，这句话的理由在哪里 | 承·分类器（八句话两栏） |
| 7 | concept | 把「我必须考第一」改一改，改成站得住的版本 | 承·概念二（改写句式） |
| 8 | interactive | 动手二：「我必须」改写台，看看心里的变化 | 承·改写练习（五句 × 三种改写 + 实时感受条） |
| 9 | concept | 例题示范：小禾的第二次月考 | 转·重难点突破（四步示范 + 悦纳三个样子） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：做一张我的学习理由卡 | 合·迁移应用（改写 + 配小事 + 生成卡片） |
| 12 | quiz | 后测：换三个新情境，办法还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，讲清悦纳自己和学习动机 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：理由在事情里面 / 把「我必须」改一改 / 三个样子都是你 三栏\n- P5 同一件事两种理由的对照图（已生成），附中文标注\n- P7 「我必须考第一」→ 站得住说法 的改写图（已生成），附中文标注\n- 三张图均为中性简洁教学插画，不使用任何真实儿童照片或可识别肖像\n- 若需补充：班级「学习理由卡」便签样例（需学校提供并授权后使用）",
}
