# -*- coding: utf-8 -*-
"""小学道德与法治 · 让生活多一些绿色（四年级）—— 补齐知识树「法治启蒙」空缺

学科语气（道德与法治）：情境案例驱动，情感共鸣 + 价值判断，从学生每天都会碰到的生活小事讲起；
结论落在「应该怎么做、为什么」，不做道德说教，不堆口号，也不用「要保护环境」这类空话收尾。

内容落点（对应统编四上「让生活多一些绿色」三课）：
  ① 我们所了解的环境污染：垃圾从哪里来、到哪里去；垃圾分类是指按一定的标准把垃圾分成几类，
     分别投放。四类桶分别是可回收物、厨余垃圾、有害垃圾、其他垃圾。
     两个高频易错项讲透——用过的餐巾纸属于其他垃圾（脏了的纸不能再回收），大骨头属于其他垃圾
     （太硬，小骨头和鱼刺才是厨余垃圾）。拿不准的时候，看一看桶边的提示最稳妥。
  ② 变废为宝有妙招：扔之前先想一想它还能做什么。空瓶、旧衣服、纸箱、玻璃罐、旧报纸都有第二次用处。
  ③ 低碳生活每一天：随手关灯、洗菜水浇花、少用一次性餐具、自带水杯和购物袋、近路走一走。
     一个人的一小步，一个班就是一大步。

三个互动台子都能真操作：
  动手一 = 垃圾分类投放台（12 件垃圾 → 四类桶，可点选也可拖放，含易错项反馈）；
  动手二 = 绿色生活计划（三组勾选 → 生成我的绿色一周计划）；
  综合任务 = 变废为宝配对台（六件废旧物品 × 它的新用法）。
插图一律中性简洁扁平插画，不使用真人照片风格。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g4-u4"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "我们的生活里会用到很多东西：书包里的本子、喝水用的瓶子、吃饭用的餐具。用完之后，它们就成了垃圾。垃圾多不多、分得对不对，不只是别人的事，也和我们每天的一个个小动作有关。这节课我们做三件事。第一件，弄清楚四类桶分别装什么。第二件，站到投放台前，把一件一件垃圾投到对的地方。第三件，给自己做一份绿色生活计划，从身边的小事开始。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你最想弄清楚的问题。是想知道每一件垃圾到底投进哪个桶，还是想知道那些用过的旧东西还能变成什么；是想知道一天里能做哪些省电省水的小事，还是想知道为什么少用一次性餐具也算一份力。选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出四类垃圾桶分别装什么：可回收物、厨余垃圾、有害垃圾、其他垃圾，并能把常见垃圾投对地方。第二，能说清两个容易投错的例子：用过的餐巾纸属于其他垃圾，大骨头也属于其他垃圾；拿不准的时候，看看桶边的提示。第三，能说出至少三种变废为宝的办法，扔之前先想一想它还能做什么。第四，能说出至少四件随手就能做到的低碳小事，比如随手关灯、洗菜水浇花、少用一次性餐具、近路走一走，并给自己定一份可以做到的计划。",
    "pretest": "先做三道小题，用你现在想到的选就行。选完马上能看到解释，选得不太合适也没关系，正好知道要重点听哪里。",
    "module-1": "先说一件每天都在发生的事：我们把东西用完，它就成了垃圾。垃圾分类是指按照一定的标准，把垃圾分成几类，分别投放到不同的桶里。为什么要分？因为分好以后，能再利用的就不会被埋在土里，需要专门处理的不至于混在普通垃圾里。四类桶是这样的。第一类，可回收物：干净的纸、塑料瓶、易拉罐、旧衣服、纸箱，它们还能变成新东西。第二类，厨余垃圾：剩饭剩菜、果皮、菜叶、茶叶渣，这些是厨房里来的，容易腐坏，可以专门处理。第三类，有害垃圾：废电池、过期药品、坏掉的荧光灯管，这些东西里有需要专门处理的部分，绝不能随手扔进普通垃圾桶。第四类，其他垃圾：用过的餐巾纸、大骨头、摔碎的陶瓷碗、扫地的灰尘，它们既不能再回收，也不好当厨余处理。这里有两个最容易投错的地方，一定要记住。第一个，用过的餐巾纸属于其他垃圾。很多同学误认为纸都可以回收，可餐巾纸沾了水和油，脏了的纸不能回收，把它投进可回收物，会让一整袋干净的东西都被弄脏。第二个，大骨头属于其他垃圾。很多人以为带骨头都是厨余垃圾，可大骨头太硬，处理设备容易被卡住；小骨头和鱼刺才是厨余垃圾。一句话记住：干净能回收，脏了就归其他；拿不准的时候，看一看桶边贴的提示，或者问一句。",
    "lab-1": "现在请你站到投放台前，当一次分类投放员。这里有十二件垃圾和四个桶。你可以先点一件垃圾，再点一个桶；也可以直接把垃圾拖进桶里。投得对会告诉你为什么，投错了会告诉你这样可能会有什么麻烦，还会告诉你还可以试试什么。",
    "module-2": "分完垃圾，再说说扔出去以前可以做的事。第一件事是变废为宝：扔之前先想一想，它还能做什么。喝完的塑料瓶剪开可以做笔筒，也能做浇花的小水壶；旧衣服剪成抹布，或者拼成小坐垫；纸箱折一折就是收纳盒；洗干净的玻璃罐可以装豆子；旧报纸擦玻璃特别亮，也能用来包东西。第二件事是低碳生活每一天，它其实就在手边。随手关灯，出门前把不用的电器关掉；洗菜的水接起来浇花；少用一次性餐具，带上自己的筷子和水杯；买东西带上购物袋；近的地方走路或者骑车去。这些事一件看起来很小，可是一个班四十个人一起做，就是一大步。这里有一个常见错误要提醒：有的同学误认为只有做大事才算为环境出力，自己少用一双一次性筷子没什么用。可是垃圾是一点一点多起来的，也可以一点一点少下去。从今天起，先把一件小事做到底，比喊十句口号都管用。",
    "lab-2": "接下来请你给自己做一份绿色生活计划。这里有家里、学校、出门三个场景的小事，你挑一挑自己愿意做、也做得到的，打上勾，然后点一下生成我的计划。计划里会有你选的事，也会数一数你一共选了几件。选多做不完没关系，选一件能坚持下来的，才最有用。",
    "worked-example": "我们一起来看小禾家的一天。第一步，先看清楚手里拿的是什么。早上，小禾喝完了一瓶牛奶，又用纸巾擦了擦嘴。他先把牛奶盒倒空、用水冲了冲、压扁，投进了可回收物。第二步，遇到拿不准的那一件。那张用过的餐巾纸，他本来想跟纸盒一起投进可回收物，可桶边贴着一张提示，写着用过的餐巾纸属于其他垃圾。他想了想，把它投进了其他垃圾。第三步，把理由说出来。他跟弟弟说：纸盒是干净的，洗干净就能再做成纸；餐巾纸沾了水和油，脏了的纸不能再回收，投进去会让一整桶都变脏。第四步，把家里的一件旧东西用起来。中午，妈妈要把一个空玻璃罐扔掉，小禾把它洗干净，装上了豆子，放在厨房柜子里。第五步，把小事变成习惯。晚上离开房间，他把灯关了；写作业时，草稿本用的是上学期没用完的本子背面。这一天没有发生什么大事，可小禾家里的垃圾少了一点，能再用起来的东西多了一点。这里有一个常见错误要提醒：有的同学误认为纸就是可回收物，看到纸就往可回收桶里放。可关键是干净还是脏了——干净能回收，脏了就归其他。",
    "conceptest-1": "接下来用三个说法考考你，每个说法里都藏着一个小陷阱。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你。下面左边是六件废旧物品，右边是它们可能的第二种用法。请你把物品和它的新用法配起来，配好以后读一读为什么。",
    "posttest": "最后一轮，换几件新的东西来考考你。这次会遇到大骨头、废电池和旧衣服，还有出门买东西的时候，看看你能不能用上今天的办法。",
    "summary": "这节课我们记住四句话。第一句，垃圾分类是指按一定的标准把垃圾分成几类，分别投放：可回收物、厨余垃圾、有害垃圾、其他垃圾。第二句，两个最容易投错的地方：用过的餐巾纸属于其他垃圾，大骨头也属于其他垃圾；记住干净能回收，脏了就归其他，拿不准就看看桶边的提示。第三句，扔之前先想一想它还能做什么——空瓶、旧衣服、纸箱、玻璃罐、旧报纸都能再用一次。第四句，低碳生活就在手边：随手关灯、洗菜水浇花、少用一次性餐具、自带水杯和购物袋、近路走一走；一个人的一小步，一个班就是一大步。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出四类垃圾桶分别装什么，各举两个例子；再写出用过的餐巾纸和大骨头分别属于哪一类，并说说为什么。第二层能力应用，动手做：这一周在家里认领一个桶，记录一天里投进去的东西，看看有没有投错，再把结果写成三句话。第三层迁移挑战，选做：用三件废旧物品做一件能用的东西，把材料和做法写下来，再用一句话说说你最近做的一件低碳小事坚持了几天。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 四类桶怎么分", "lab-1": "动手一 垃圾分类投放台",
    "module-2": "概念二 变废为宝与低碳生活", "lab-2": "动手二 绿色生活计划",
    "worked-example": "例题示范 小禾家的一天", "conceptest-1": "概念测试",
    "synthesis": "综合任务 变废为宝配对台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：垃圾分类投放台（十二件垃圾 × 四类桶） ──
BINS4 = [
    {"k": "recycle", "n": "可回收物"},
    {"k": "kitchen", "n": "厨余垃圾"},
    {"k": "harmful", "n": "有害垃圾"},
    {"k": "other", "n": "其他垃圾"},
]
GARBAGE = [
    {"id": "g1", "t": "旧报纸", "bin": "recycle",
     "why": "旧报纸是干净的纸，回收以后可以再做成纸，投进可回收物，它就还有下一次。"},
    {"id": "g2", "t": "喝完的塑料饮料瓶", "bin": "recycle",
     "why": "塑料瓶倒空、冲一冲、压扁，投进可回收物；瓶里还剩饮料的话，先把水倒掉再投。"},
    {"id": "g3", "t": "易拉罐", "bin": "recycle",
     "why": "易拉罐是金属，投进可回收物最好；罐子还烫的时候先放凉，别烫到自己。"},
    {"id": "g4", "t": "剩饭剩菜", "bin": "kitchen",
     "why": "剩饭剩菜先把汤水沥一沥，投进厨余垃圾。"},
    {"id": "g5", "t": "苹果皮和菜叶", "bin": "kitchen",
     "why": "果皮、菜叶都是从厨房里来的，投进厨余垃圾。"},
    {"id": "g6", "t": "泡过的茶叶渣", "bin": "kitchen",
     "why": "茶叶渣也算厨余垃圾，投之前把水沥一沥，桶里就不会又湿又重。"},
    {"id": "g7", "t": "废电池（纽扣电池、充电电池）", "bin": "harmful",
     "why": "电池里有需要专门处理的东西，投进有害垃圾，别随手扔进普通垃圾桶。"},
    {"id": "g8", "t": "过期的药品", "bin": "harmful",
     "why": "过期药品连同包装投进有害垃圾；别自己乱吃，也别冲进下水道。"},
    {"id": "g9", "t": "坏掉的荧光灯管", "bin": "harmful",
     "why": "灯管里有需要专门处理的东西，投进有害垃圾；灯管容易碎，先用厚纸包一包再放。"},
    {"id": "g10", "t": "用过的餐巾纸", "bin": "other",
     "why": "这是最容易投错的一件。餐巾纸沾了水和油，脏了的纸不能再回收——"
            "投进可回收物，会让一整袋干净的东西都被弄脏。它属于其他垃圾。"},
    {"id": "g11", "t": "大骨头", "bin": "other",
     "why": "这也是最容易投错的一件。大骨头太硬，厨余垃圾的处理设备容易被卡住，所以它属于其他垃圾；"
            "小骨头和鱼刺才是厨余垃圾。"},
    {"id": "g12", "t": "摔碎的陶瓷碗", "bin": "other",
     "why": "摔碎的陶瓷碗不能回收，属于其他垃圾；碎片锋利，先用厚纸包好再投，别扎到手。"},
]

# ── 动手二：绿色生活计划（三组勾选 → 生成我的计划） ──
PLAN_GROUPS = [
    {"k": "home", "n": "在家里", "items": [
        "离开房间随手关灯，出门前把不用的电器关掉",
        "洗菜、洗米的水接起来浇花",
        "吃饭少用一次性餐具，用自己的筷子和小碗",
        "东西扔之前先想一想，它还能不能再用一次",
        "把家里的垃圾分类投进对应的桶",
    ]},
    {"k": "school", "n": "在学校", "items": [
        "用完的作业本，背面接着写草稿",
        "离开教室时，看看灯和风扇关了没有",
        "自带水杯，少买瓶装水",
    ]},
    {"k": "out", "n": "出门时", "items": [
        "近的地方走路或者骑车去",
        "带上自己的水杯和购物袋",
        "少买包装一层又一层的东西",
    ]},
]

# ── 综合任务：变废为宝配对台（六件废旧物品 × 它的新用法） ──
REUSE = [
    {"id": "r1", "t": "喝完的塑料瓶", "u": "剪开做笔筒，或者做浇花的小水壶",
     "why": "塑料瓶剪一刀、修一修边，就是一个笔筒；瓶盖上扎几个小孔，就是浇花的小水壶。"},
    {"id": "r2", "t": "穿不下的旧衣服", "u": "剪成抹布，或者拼成小坐垫",
     "why": "棉布吸水，剪成方块就是抹布；几块拼在一起缝一缝，就是小坐垫。"},
    {"id": "r3", "t": "拆开的纸箱", "u": "折成收纳盒，或者做手工模型",
     "why": "纸箱折一折、贴上纸，就是收纳盒；也可以做手工模型，做完还能再回收。"},
    {"id": "r4", "t": "洗干净的玻璃罐", "u": "装豆子、装小东西，或者做笔筒",
     "why": "玻璃罐洗净晾干，能装豆子、装小零件；罐口不锋利的话，也能当笔筒。"},
    {"id": "r5", "t": "旧报纸", "u": "擦玻璃，或者用来包东西",
     "why": "旧报纸擦玻璃又亮又不留水痕，也能用来包易碎的东西。"},
    {"id": "r6", "t": "写完的作业本纸", "u": "订起来当草稿本",
     "why": "背面还空着的纸订在一起，就是一本草稿本；实在用完了，再投进可回收物。"},
]

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g4-u4 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 垃圾分类投放台：点垃圾 + 点桶，或直接拖进桶（四类桶，含易错项反馈）
   3) 绿色生活计划：三组勾选 → 生成我的绿色一周计划
   4) 变废为宝配对台：六件废旧物品 × 它的新用法
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

  /* ---------- 2. 垃圾分类投放台 ---------- */
  var GARBAGE = __GARBAGE_JSON__;
  var BINS4 = __BINS4_JSON__;
  function garbageById(id) {
    for (var i = 0; i < GARBAGE.length; i++) { if (GARBAGE[i].id === id) return GARBAGE[i]; }
    return null;
  }
  function binName(k) {
    for (var i = 0; i < BINS4.length; i++) { if (BINS4[i].k === k) return BINS4[i].n; }
    return k;
  }
  var stage1 = document.getElementById('g-stage');
  if (stage1) {
    var pickG = null, placedG = {};
    var out1 = document.getElementById('g-out');
    function render1() {
      document.querySelectorAll('[data-g-item]').forEach(function (b) {
        var k = b.dataset.gItem;
        b.classList.toggle('selected', k === pickG);
        b.classList.toggle('done', !!placedG[k]);
        b.draggable = !placedG[k];
      });
      var done = Object.keys(placedG).length;
      document.getElementById('g-score').textContent = '已经投对 ' + done + ' / ' + GARBAGE.length + ' 件';
      BINS4.forEach(function (B) {
        var box = document.getElementById('g-box-' + B.k);
        if (!box) return;
        box.innerHTML = '';
        var h = document.createElement('h4');
        h.textContent = B.n;
        box.appendChild(h);
        var n = 0;
        GARBAGE.forEach(function (G) {
          if (!placedG[G.id] || G.bin !== B.k) return;
          var s = document.createElement('div');
          s.className = 'tag';
          s.textContent = G.t;
          box.appendChild(s);
          n++;
        });
        if (!n) {
          var e = document.createElement('span');
          e.style.color = 'var(--muted)';
          e.style.fontSize = '13px';
          e.textContent = '还没有放进来。';
          box.appendChild(e);
        }
      });
    }
    function place(bin) {
      if (!pickG) {
        out1.className = 'result warn';
        out1.textContent = '先点一件垃圾，或者直接把垃圾拖进桶里。';
        return;
      }
      var G = garbageById(pickG);
      if (G.bin === bin) {
        placedG[G.id] = true;
        out1.className = 'result';
        out1.innerHTML = '<strong>' + G.t + '：投对了，它属于「' + binName(bin) + '」。</strong>' + G.why;
        pickG = null;
        if (Object.keys(placedG).length === GARBAGE.length) {
          out1.className = 'result';
          out1.innerHTML = '<strong>十二件全投对了！</strong>记住这句口诀：<strong>干净能回收，脏了归其他；' +
            '电池药灯管，专门一类放。</strong>拿不准的时候，看看桶边贴的提示最稳妥。';
        }
      } else {
        out1.className = 'result warn';
        out1.innerHTML = '<strong>' + G.t + '：这样可能会投错地方。</strong>' + G.why +
          '<br><span style="color:var(--muted)">还可以试试这样想：它还是干净的吗？它是厨房里来的吗？' +
          '里面有没有需要专门处理的东西？想清楚了再投。</span>';
      }
      render1();
    }
    document.querySelectorAll('[data-g-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (placedG[b.dataset.gItem]) return;
        pickG = b.dataset.gItem;
        out1.className = 'result warn';
        out1.innerHTML = '<strong>你手里拿的是：' + b.textContent + '</strong><br>想一想它该进哪个桶，再点一下桶。';
        render1();
      });
      b.addEventListener('dragstart', function (ev) {
        if (placedG[b.dataset.gItem]) { ev.preventDefault(); return; }
        pickG = b.dataset.gItem;
        if (ev.dataTransfer) ev.dataTransfer.setData('text/plain', b.dataset.gItem);
        render1();
      });
    });
    document.querySelectorAll('[data-g-bin]').forEach(function (b) {
      b.addEventListener('click', function () { place(b.dataset.gBin); });
      b.addEventListener('dragover', function (ev) { ev.preventDefault(); });
      b.addEventListener('drop', function (ev) {
        ev.preventDefault();
        var id = id_from_ev(ev);
        if (id) pickG = id;
        place(b.dataset.gBin);
      });
    });
    function id_from_ev(ev) {
      if (ev.dataTransfer && ev.dataTransfer.getData) {
        var v = ev.dataTransfer.getData('text/plain');
        if (v) return v;
      }
      return null;
    }
    render1();
  }

  /* ---------- 3. 绿色生活计划 ---------- */
  var planBtn = document.getElementById('plan-go');
  if (planBtn) {
    planBtn.addEventListener('click', function () {
      var out = document.getElementById('plan-out');
      var box = document.getElementById('plan-result');
      var boxes = document.querySelectorAll('[data-plan-item]');
      var picked = [];
      boxes.forEach(function (c) { if (c.checked) picked.push(c.dataset.planItem); });
      box.innerHTML = '';
      if (!picked.length) {
        out.className = 'result warn';
        out.innerHTML = '<strong>还没有挑。可以先选一件最容易做到的</strong>，比如离开房间随手关灯。' +
          '还可以试试：先选三件事，做一周，下周再换三件。';
        return;
      }
      out.className = 'result';
      out.innerHTML = '<strong>你的绿色生活计划做好了，一共 ' + picked.length + ' 件。</strong>' +
        '先说给家里人听，请一个人帮你记着；一周以后回来看看，做到了几件。';
      picked.forEach(function (t) {
        var d = document.createElement('div');
        d.className = 'tag';
        d.textContent = t;
        box.appendChild(d);
      });
      document.getElementById('plan-score').textContent = '已选 ' + picked.length + ' 件';
    });
    document.querySelectorAll('[data-plan-item]').forEach(function (c) {
      c.addEventListener('change', function () {
        var n = document.querySelectorAll('[data-plan-item]:checked').length;
        document.getElementById('plan-score').textContent = '已选 ' + n + ' 件';
      });
    });
  }

  /* ---------- 4. 变废为宝配对台 ---------- */
  var REUSE = __REUSE_JSON__;
  var stage3 = document.getElementById('re-stage');
  if (stage3) {
    var pickR = null, matchedR = {};
    var out3 = document.getElementById('re-out');
    function reuseById(id) {
      for (var i = 0; i < REUSE.length; i++) { if (REUSE[i].id === id) return REUSE[i]; }
      return null;
    }
    function render3() {
      document.querySelectorAll('[data-re-item]').forEach(function (b) {
        var k = b.dataset.reItem;
        b.classList.toggle('selected', k === pickR);
        b.classList.toggle('done', !!matchedR[k]);
        b.disabled = !!matchedR[k];
      });
      document.querySelectorAll('[data-re-use]').forEach(function (b) {
        var k = b.dataset.reUse;
        b.classList.toggle('done', !!matchedR[k]);
        b.disabled = !!matchedR[k];
      });
      var box = document.getElementById('re-done');
      box.innerHTML = '';
      var n = 0;
      REUSE.forEach(function (R) {
        if (!matchedR[R.id]) return;
        var d = document.createElement('div');
        d.className = 'tag';
        d.textContent = R.t + ' → ' + R.u;
        box.appendChild(d);
        n++;
      });
      if (!n) box.innerHTML = '<span style="color:var(--muted);font-size:14px">还没有配好的。</span>';
      document.getElementById('re-score').textContent = '已经配好 ' + n + ' / ' + REUSE.length + ' 对';
    }
    document.querySelectorAll('[data-re-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (matchedR[b.dataset.reItem]) return;
        pickR = b.dataset.reItem;
        out3.className = 'result warn';
        out3.innerHTML = '<strong>你拿起的是：' + b.textContent + '</strong><br>它的第二种用法是什么？在右边选一个。';
        render3();
      });
    });
    document.querySelectorAll('[data-re-use]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (!pickR) {
          out3.className = 'result warn';
          out3.textContent = '先在左边点一件废旧物品，再在右边选它的用法。';
          return;
        }
        var R = reuseById(pickR);
        if (b.dataset.reUse === R.id) {
          matchedR[R.id] = true;
          out3.className = 'result';
          out3.innerHTML = '<strong>配好了：' + R.t + '可以' + R.u + '。</strong>' + R.why;
          pickR = null;
          if (Object.keys(matchedR).length === REUSE.length) {
            out3.className = 'result';
            out3.innerHTML = '<strong>六对全配好了！</strong>记住这句话：<strong>扔之前先想一想，它还能做什么。</strong>';
          }
        } else {
          out3.className = 'result warn';
          out3.innerHTML = '<strong>再想一想这一件。</strong>它本来的材料决定了它能变成什么——' +
            '是纸、是布、是塑料、还是玻璃？还可以试试：先看看它的材料，再挑用途。';
        }
        render3();
      });
    });
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__GARBAGE_JSON__', json.dumps(GARBAGE, ensure_ascii=False))
             .replace('__BINS4_JSON__', json.dumps(BINS4, ensure_ascii=False))
             .replace('__REUSE_JSON__', json.dumps(REUSE, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：三道小选择题", TTS["pretest"], [
        {"q": "用过的餐巾纸，应该投进哪一个桶？",
         "options": [("其他垃圾", True),
                     ("可回收物", False),
                     ("厨余垃圾", False)],
         "explain": "餐巾纸沾了水和油，脏了的纸不能再回收，所以属于其他垃圾。"
                    "<strong>错因提醒：</strong>常见错误是误认为「纸都可以回收」——"
                    "能不能回收，看的是干净还是脏了。"},
        {"q": "下面哪一件是随手就能做到的省电小事？",
         "options": [("离开房间的时候顺手把灯关掉", True),
                     ("把灯一直开着，反正一会儿还要回来", False),
                     ("白天把窗帘拉上，开着灯看书", False)],
         "explain": "随手关灯不用准备什么工具，也不用多花时间，是门槛最低的一件小事。"
                    "<strong>错因提醒：</strong>有的同学把「一会儿还要回来」搞混成「不用关」——"
                    "走出去就关，回来再开，一共只有两下。"},
        {"q": "关于少用一次性餐具，下面哪种说法说得对？",
         "options": [("自己带筷子和水杯，用一次就少产生一件垃圾", True),
                     ("一个人少用一双筷子，对环境影响不大，做不做都一样", False),
                     ("用一次性餐具更方便，方便就够了", False)],
         "explain": "垃圾是一点一点多起来的，也可以一点一点少下去；一个班一起做，就是一大步。"
                    "<strong>错因提醒：</strong>容易把「一个人做不了什么」误认为「做了也没用」——"
                    "教室里四十个人一起做，一学期就是很多件。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "四类桶怎么分：干净能回收，脏了就归其他", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在扔垃圾，也大概知道要分类（And）；可真正站在桶前面的时候，用过的餐巾纸、大骨头这些就拿不准了（But）；所以这节课先把四类桶分清楚，再站到投放台前一件一件投对（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>垃圾分类</strong>是指按照一定的标准，把垃圾分成几类，分别投放到不同的桶里。分好以后，能再利用的就不会被埋在土里。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>可回收物</strong></p>
            <p style="color:var(--muted)">干净的纸、塑料瓶、易拉罐、旧衣服、纸箱。它们还能变成新东西。</p>
          </div>
          <div class="inner-card">
            <p><strong>厨余垃圾</strong></p>
            <p style="color:var(--muted)">剩饭剩菜、果皮、菜叶、茶叶渣。厨房里来的，容易腐坏，专门处理。</p>
          </div>
          <div class="inner-card">
            <p><strong>有害垃圾</strong></p>
            <p style="color:var(--muted)">废电池、过期药品、坏掉的荧光灯管。里面有需要专门处理的部分。</p>
          </div>
          <div class="inner-card">
            <p><strong>其他垃圾</strong></p>
            <p style="color:var(--muted)">用过的餐巾纸、大骨头、摔碎的陶瓷碗。既不能再回收，也不好当厨余。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="四类垃圾桶与常见垃圾对照图：可回收物、厨余垃圾、有害垃圾、其他垃圾，附中文标注">
          <figcaption>概念图：四类桶分别装什么 · 干净能回收，脏了就归其他（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--accent-soft);border-color:rgba(78,205,196,.45)">
          <p><strong>两个最容易投错的例子</strong></p>
          <p style="color:var(--muted)">用过的餐巾纸属于其他垃圾——脏了的纸不能再回收，投进可回收物会把一整袋干净的东西弄脏。大骨头也属于其他垃圾——太硬，处理设备会被卡住；小骨头和鱼刺才是厨余垃圾。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「只要带个纸字就是可回收物」。其实关键是干净还是脏了：<strong>干净能回收，脏了就归其他。拿不准的时候，看一看桶边贴的提示。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样是一张纸，干净的纸盒是资源，沾了油的餐巾纸是其他垃圾。差别不在材料，在它现在的样子。"},
    {"lens": "解释它", "text": "为什么要分得这么细？因为混在一起，能用的和需要专门处理的都会互相拖累——分开以后，才各归各位。"},
    {"lens": "迁移它", "text": "这套判断在家里、在学校、在小区都用得上：先看干净不干净，再看是哪里来的，最后看有没有需要专门处理的东西。"},
])}
    ''', tag="概念一"))

    g_btns = "\n".join(
        f'            <button class="sort-item" draggable="true" data-g-item="{g["id"]}">{g["t"]}</button>'
        for g in GARBAGE
    )
    bin_btns = "\n".join(
        f'            <button class="choice" data-g-bin="{b["k"]}" style="text-align:center">{b["n"]}</button>'
        for b in BINS4
    )
    bin_boxes = "\n".join(
        f'            <div class="sort-bin" id="g-box-{b["k"]}"><h4>{b["n"]}</h4></div>'
        for b in BINS4
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：垃圾分类投放台，这件垃圾该进哪个桶？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">你现在是分类投放员。<strong>先点一件垃圾，再点一个桶；也可以直接把垃圾拖进桶里。</strong>拿不准的那两件，投完记得读一读为什么。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 手里要投的垃圾</div>
          <div class="sort-bank" id="g-stage">
{g_btns}
          </div>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">② 四个桶（点一下，或者把垃圾拖进来）</div>
          <div class="grid grid-2">
{bin_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">投放进度</span><span class="v" id="g-score">已经投对 0 / 12 件</span></div>
          </div>
          <p class="result warn" id="g-out" style="margin-top:12px">先点一件垃圾。</p>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 四个桶里现在有什么</div>
          <div class="sort-bins">
{bin_boxes}
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">♻️</span><div><strong>说给你听：</strong>各地垃圾桶的样子和名字不完全一样，有的地方分得更细。拿不准的时候，看一看桶边贴的提示，或者问一句，比凭印象投更稳妥。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "变废为宝与低碳生活：扔之前先想一想，它还能做什么", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">分完垃圾，还有一件更早可以做的事：<strong>扔之前先想一想，它还能做什么。</strong></p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>变废为宝有妙招</strong></p>
            <p style="color:var(--muted)">塑料瓶剪开做笔筒；旧衣服剪成抹布；纸箱折成收纳盒；玻璃罐装豆子；旧报纸擦玻璃。</p>
          </div>
          <div class="inner-card">
            <p><strong>低碳生活每一天</strong></p>
            <p style="color:var(--muted)">随手关灯；洗菜水浇花；少用一次性餐具；自带水杯和购物袋；近的地方走路或者骑车。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="变废为宝与低碳生活概念图：旧物再用、随手关灯、少用一次性餐具、自带水杯，附中文标注">
          <figcaption>概念图：变废为宝的几件常用办法 · 一天里能做的低碳小事（教学示意图，中性简洁扁平插画）</figcaption>
        </figure>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么这些小事值得做</strong></p>
          <p style="color:var(--muted)">一件看起来很小，可是一个班四十个人一起做，就是一大步。垃圾是一点一点多起来的，也可以一点一点少下去。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>只有做大事才算为环境出力，自己少用一双一次性筷子没什么用。<strong>先把一件小事做到底，比喊十句口号都管用。</strong></p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一个空瓶子，扔进可回收桶是一次回收，做成笔筒是又一次使用——它被用了几次，取决于我先想了哪一步。"},
    {"lens": "比较它", "text": "同样是喝水：买一瓶瓶装水，是喝一次、多一个瓶子；带自己的水杯，是喝很多次、不多一个瓶子。"},
    {"lens": "迁移它", "text": "这套办法在家里和在学校都一样：先问还能不能用，再问该投哪个桶，最后才说扔。"},
])}
    ''', tag="概念二"))

    groups_html = []
    for G in PLAN_GROUPS:
        rows = "\n".join(
            f'              <label style="display:block;padding:7px 0;cursor:pointer"><input type="checkbox" data-plan-item="{it}" style="margin-right:8px;vertical-align:-2px"><span>{it}</span></label>'
            for it in G["items"]
        )
        groups_html.append(f'''          <div class="inner-card">
            <p><strong>{G["n"]}</strong></p>
{rows}
          </div>''')
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：绿色生活计划，挑出你能坚持的那几件", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">给自己做一份计划：在下面三个场景里，勾出你愿意做、也做得到的小事，然后点一下按钮生成计划。</p>
        <div class="lab-panel">
          <div class="grid">
{chr(10).join(groups_html)}
          </div>
          <div style="margin-top:16px">
            <button class="choice" id="plan-go" style="text-align:center;font-weight:700">生成我的绿色一周计划</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">已选几件</span><span class="v" id="plan-score">已选 0 件</span></div>
          </div>
          <p class="result warn" id="plan-out" style="margin-top:12px">先勾一勾，再点生成。</p>
          <div class="sort-bank" id="plan-result"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🌱</span><div><strong>想一想：</strong>计划不是越长越好。挑一件最容易做到的，做满一周，比一下子勾十件、第二天就忘了更算数。勾完以后回头看一看：这几件事里，哪一个更像是我自己能做到的？</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：小禾家的一天", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>早上小禾喝完一瓶牛奶、用纸巾擦了擦嘴；中午妈妈要把一个空玻璃罐扔掉；晚上他回房间写作业。这一天里，藏着好几件和绿色有关的小事。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看清楚手里拿的是什么：</strong>牛奶盒倒空、冲一冲、压扁，投进可回收物。</div></div>
          <div class="step"><span class="n">2</span><div><strong>遇到拿不准的那一件：</strong>用过的餐巾纸本来想跟纸盒一起放，可桶边提示写着它属于其他垃圾，就投进了其他垃圾。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>把理由说出来：</strong>纸盒是干净的，能再做成纸；餐巾纸脏了，不能再回收，混进去会让一整桶都变脏。</div></div>
          <div class="step"><span class="n">4</span><div><strong>让旧东西再用一次：</strong>空玻璃罐洗干净，装上豆子放进柜子。</div></div>
        </div>
        <div class="inner-card">
          <p><strong>第五步：把小事变成习惯</strong></p>
          <p style="color:var(--muted)">晚上离开房间把灯关了；写作业时，草稿用的是上学期没用完的本子背面。这一天没发生什么大事，可家里的垃圾少了一点，能再用起来的东西多了一点。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>「纸就是可回收物，看到纸就往可回收桶里放」。可关键是干净还是脏了——<strong>干净能回收，脏了就归其他。</strong></p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，藏着小陷阱", TTS["conceptest-1"], [
        {"q": "关于垃圾分类，下面哪句话说得对？",
         "options": [("干净能回收，脏了就归其他；拿不准就看看桶边的提示", True),
                     ("只要带个纸字，就都属于可回收物", False),
                     ("分不分都一样，反正最后都装车运走", False)],
         "explain": "能不能回收，看的是干净还是脏了；分开以后，能用的和需要专门处理的才各归各位。"
                    "<strong>错因提醒：</strong>常见错误是误认为「纸都可以回收」——"
                    "一张沾了油的餐巾纸混进可回收物，会把一整袋都弄脏。"},
        {"q": "大骨头应该投进哪一个桶？",
         "options": [("其他垃圾", True),
                     ("厨余垃圾", False),
                     ("可回收物", False)],
         "explain": "大骨头太硬，厨余垃圾的处理设备容易被卡住，所以它属于其他垃圾；小骨头和鱼刺才是厨余垃圾。"
                    "<strong>错因提醒：</strong>有的同学把「带骨头就是厨房里的东西」搞混成「都算厨余垃圾」——"
                    "硬不硬，也是判断的一条。"},
        {"q": "喝完的塑料瓶，下面哪种做法更好？",
         "options": [("倒空、冲一冲、压扁，投进可回收物；如果还需要，就先做成笔筒", True),
                     ("里面还剩半瓶饮料，直接扔进可回收物", False),
                     ("跟剩饭剩菜一起扔进厨余垃圾", False)],
         "explain": "干净、压扁再投，回收起来更方便；还能用的话，先用一次再回收。"
                    "<strong>错因提醒：</strong>容易把「它是塑料就能回收」误认为「不用洗也能投」——"
                    "没倒干净的瓶子会把整袋可回收物弄脏。"}
    ], tag="概念测试"))

    re_items = "\n".join(
        f'            <button class="sort-item" data-re-item="{r["id"]}">{r["t"]}</button>' for r in REUSE
    )
    re_uses = "\n".join(
        f'            <button class="sort-item" data-re-use="{r["id"]}">{r["u"]}</button>' for r in REUSE
    )
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：变废为宝配对台，它能变成什么？", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先在左边点一件废旧物品，再在右边点它的第二种用法。两边对上了，就会记进下面的清单里。</p>
        <div class="lab-panel">
          <div class="grid grid-2">
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 废旧物品</div>
              <div class="sort-bank" id="re-stage">
{re_items}
              </div>
            </div>
            <div>
              <div style="font-weight:700;font-size:14px;margin-bottom:6px">② 它的第二种用法</div>
              <div class="sort-bank">
{re_uses}
              </div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">配对进度</span><span class="v" id="re-score">已经配好 0 / 6 对</span></div>
          </div>
          <p class="result warn" id="re-out" style="margin-top:12px">先在左边点一件废旧物品。</p>
          <div style="font-weight:700;font-size:14px;margin:16px 0 6px">③ 配好的清单</div>
          <div class="sort-bank" id="re-done"></div>
        </div>
        <div class="inner-card">
          <p><strong>配完之后，想一想：</strong></p>
          <p style="color:var(--muted)">家里有什么东西，你原来打算扔掉，现在想留下来再用一次？写下来。</p>
          <textarea id="syn-answer" rows="3" placeholder="我家里有……，我想把它……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几件新东西，办法还在不在", TTS["posttest"], [
        {"q": "一块废电池（纽扣电池）应该投进哪一个桶？",
         "options": [("有害垃圾", True),
                     ("其他垃圾", False),
                     ("可回收物", False)],
         "explain": "电池里有需要专门处理的部分，投进有害垃圾，别随手扔进普通垃圾桶。"
                    "<strong>错因提醒：</strong>常见错误是误认为「小东西无所谓，扔进哪个桶都行」——"
                    "越是有需要专门处理的部分，越不能混进去。"},
        {"q": "穿不下的旧衣服，下面哪种做法更好？",
         "options": [("看看还能不能穿给别人，或者剪成抹布、拼成小坐垫", True),
                     ("跟其他垃圾一起扔掉", False),
                     ("放在楼道里，等人来收", False)],
         "explain": "先想它还能做什么，再决定扔不扔；旧衣服干净还能穿的话，可以送出去继续用。"
                    "<strong>错因提醒：</strong>容易把「我不穿了」误认为「它没用了」——"
                    "对我没用的东西，可能对别人还有用。"},
        {"q": "和妈妈一起去超市买东西，下面哪种做法更好？",
         "options": [("带上自己的购物袋和水杯，尽量不买包装很多层的东西", True),
                     ("袋子要花钱，那就多拿几个塑料袋分着装", False),
                     ("方便最重要，包装多不多不管", False)],
         "explain": "带一个购物袋、少一层包装，都是出门前就能准备好的小事。"
                    "<strong>错因提醒：</strong>有的同学把「单独看这一件没什么」搞混成「做了也没用」——"
                    "一周买三次，一个学期就是很多个袋子。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，讲清绿色生活怎么做", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>四类桶怎么分：</strong>可回收物、厨余垃圾、有害垃圾、其他垃圾，分别装在四个桶里。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>两个最容易错的：</strong>用过的餐巾纸属于其他垃圾，大骨头也属于其他垃圾；干净能回收，脏了就归其他。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>扔之前先想一想：</strong>空瓶、旧衣服、纸箱、玻璃罐、旧报纸都能再用一次。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>低碳就在手边：</strong>随手关灯、洗菜水浇花、少用一次性餐具、自带水杯和购物袋、近路走一走。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>干净能回收，脏了归其他；电池药灯管，专门一类放。扔之前先想一想，它还能做什么。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「四类桶」「干净能回收」这两个说法，给家里人讲一件今天投对过的垃圾。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>你打算从今天起先做的那一件小事，写清楚做什么、什么时候做、请谁帮你记着。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出四类垃圾桶分别装什么，各举两个例子；再把这四个桶的样子画出来，标上名字。",
            "写出用过的餐巾纸和大骨头分别属于哪一类，并说说为什么。",
            "写出三件变废为宝的办法。",
        ],
        [
            "这一周在家里认领一个桶，记录一天里投进去的东西，看看有没有投错，再把结果写成三句话。",
            "和家里人一起做一份绿色生活计划，每人挑两件小事，一周以后一起看看做到了几件。",
        ],
        [
            "用三件废旧物品做一件能用的东西，把材料和做法写下来，再说说它解决了什么小问题。",
            "选一件低碳小事坚持一周，每天记一次，最后写一句话说说最难度过的是哪一天、你是怎么坚持下来的。",
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
    "title": "让生活多一些绿色",
    "name_en": "Make Life a Little Greener",
    "grade": 4,
    "grade_cn": "四年级",
    "domain": "rule-of-law",
    "domain_cn": "法治启蒙",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学四年级的道德与法治课：从学生每天都在做的事讲起，落到三个可以立刻行动的层面。一是「垃圾怎么分类」——垃圾分类是指按照一定的标准把垃圾分成几类、分别投放，四类桶分别是可回收物、厨余垃圾、有害垃圾、其他垃圾，并把两个高频易错项讲透：用过的餐巾纸属于其他垃圾（脏了的纸不能再回收），大骨头属于其他垃圾（太硬，小骨头和鱼刺才是厨余），记住一句干净能回收、脏了就归其他，拿不准就看桶边的提示。二是「变废为宝有妙招」——扔之前先想一想它还能做什么，空瓶、旧衣服、纸箱、玻璃罐、旧报纸都有第二次用处。三是「低碳生活每一天」——随手关灯、洗菜水浇花、少用一次性餐具、自带水杯和购物袋、近路走一走，一个人的一小步，一个班就是一大步。全课不喊口号、不说教，用真实家庭与校园情境推进，并处理一个常见误解：只有做大事才算为环境出力。三个互动台子都能真操作：动手一是垃圾分类投放台（十二件垃圾点选或拖放进四类桶，含易错项反馈）、动手二是绿色生活计划（家里/学校/出门三组勾选 → 生成我的绿色一周计划）、综合任务是变废为宝配对台（六件废旧物品 × 它的新用法）。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "tags": ["让生活多一些绿色", "我们所了解的环境污染", "变废为宝有妙招", "低碳生活每一天", "垃圾分类", "四类垃圾桶", "变废为宝", "四年级", "法治启蒙"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「法治启蒙」——遵守公共秩序，爱护公共设施，参与力所能及的公益活动，在公共生活中承担自己的一份责任；对应统编《道德与法治》四年级上册「让生活多一些绿色」：我们所了解的环境污染、变废为宝有妙招、低碳生活每一天。",
    "hero_question": "一件用完的东西，怎样才能让它再有用一次？",
    "hero_alt": "让生活多一些绿色知识结构图：四类桶怎么分、变废为宝有妙招、低碳生活每一天 三栏",
    "hero_caption": "让生活多一些绿色：四类桶怎么分 · 变废为宝有妙招 · 低碳生活每一天（干净能回收，脏了就归其他）",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "每一件垃圾到底投进哪个桶？", "d": "可回收物、厨余垃圾、有害垃圾、其他垃圾", "v": "每一件垃圾到底投进哪个桶"},
        {"t": "用过的旧东西还能变成什么？", "d": "空瓶、旧衣服、纸箱、玻璃罐、旧报纸", "v": "用过的旧东西还能变成什么"},
        {"t": "一天里我能做哪些省电省水的小事？", "d": "随手关灯、洗菜水浇花、少用一次性餐具", "v": "一天里我能做哪些省电省水的小事"},
        {"t": "为什么少用一次性餐具也算一份力？", "d": "一个人的一小步，一个班就是一大步", "v": "为什么少用一次性餐具也算一份力"},
    ],
    "objectives": [
        "能说出四类垃圾桶分别装什么（可回收物、厨余垃圾、有害垃圾、其他垃圾），并能把常见垃圾投对地方",
        "能说清两个容易投错的例子：用过的餐巾纸属于其他垃圾，大骨头也属于其他垃圾；拿不准就看桶边的提示",
        "能说出至少三种变废为宝的办法，知道扔之前先想一想它还能做什么",
        "能说出至少四件随手就能做到的低碳小事，并给自己定一份做得到的计划",
    ],
    "objectives_plain": [
        "能说出四类桶分别装什么，把常见垃圾投对地方",
        "知道用过的餐巾纸和大骨头属于其他垃圾，拿不准就看桶边提示",
        "能说出三种变废为宝的办法，扔之前先想一想",
        "能说出四件低碳小事，并挑出自己能坚持的那几件",
    ],
    "standards": [
        {"content": "遵守公共秩序，爱护公共设施，参与力所能及的公益活动。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 法治启蒙"},
        {"content": "我们所了解的环境污染；变废为宝有妙招；低碳生活每一天",
         "source": "统编《道德与法治》四年级上册「让生活多一些绿色」"},
    ],
    "prereqs": ["pol-e-g4-u3"],
    "prereqs_name": "信息万花筒",
    "prereqs_meta": "pol-e-g4-u3",
    "leads_to": ["pol-e-g5-u1"],
    "next_meta": "pol-e-g5-u1",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "一件东西用完，故事还没结束。这节课弄清楚：怎么分、还能变成什么、一天能做哪几件小事。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能站到桶前面把手里这件垃圾投对。",
        "objectives": "看清四件事：四类桶分别装什么、两个最容易投错的例子、变废为宝、低碳小事。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "四类桶：可回收物、厨余垃圾、有害垃圾、其他垃圾。干净能回收，脏了就归其他。",
        "lab-1": "十二件垃圾、四个桶。点一件垃圾再点桶，也可以直接拖进去；投错了会告诉你为什么。",
        "module-2": "扔之前先想一想它还能做什么；随手关灯、少用一次性餐具都是在做同一件事。",
        "lab-2": "勾出你愿意做也做得到的几件小事，点一下就能生成你的绿色一周计划。",
        "worked-example": "小禾家的一天五步：先看清楚、遇到拿不准的看提示、把理由说出来、旧东西再用、把小事变习惯。",
        "conceptest-1": "三个说法里都藏着一个小陷阱，选完把解释读一遍。",
        "synthesis": "把六件废旧物品和它的第二种用法配起来，配完读一读为什么。",
        "posttest": "出现了废电池、旧衣服和去超市买东西，看看办法还在不在。",
        "summary": "四句话：四类桶怎么分、两个最容易错的、扔之前先想一想、低碳就在手边。",
        "homework": "三层小任务，先做前两层；第二层要请家里人一起完成。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「法治启蒙」板块在四年级的空缺，正对统编教材四年级上册「让生活多一些绿色」（我们所了解的环境污染、变废为宝有妙招、低碳生活每一天）。四年级学生已经知道「要垃圾分类」，但真正站在桶前面时常常拿不准：用过的餐巾纸算不算纸、大骨头算不算厨余，都很容易投错；同时很容易觉得「我一个人做什么都没用」，把环保当成一句口号。所以全课不喊口号，把口号换成一连串能立刻做出来的动作。第一层是「垃圾怎么分」：先给出垃圾分类的规范表述——按照一定的标准把垃圾分成几类、分别投放，再把四类桶一一说清楚，并把两个高频易错项讲透：用过的餐巾纸属于其他垃圾（脏了的纸不能再回收，混进去会把整袋干净的东西弄脏）、大骨头属于其他垃圾（太硬，小骨头和鱼刺才是厨余），最后收在一句可随身带的判断上——干净能回收，脏了就归其他，拿不准就看桶边的提示。第二层是「变废为宝有妙招」：把「扔」这一步往后推一格，先问它还能做什么，空瓶、旧衣服、纸箱、玻璃罐、旧报纸各有第二次用处。第三层是「低碳生活每一天」：随手关灯、洗菜水浇花、少用一次性餐具、自带水杯和购物袋、近路走一走，并正面回应「一个人做不了什么」这个常见误解——垃圾是一点一点多起来的，也可以一点一点少下去，一个班四十个人一起做就是一大步。三个互动台子都能真操作：动手一是垃圾分类投放台，十二件垃圾既可以点选也可以直接拖进四个桶，投对讲清为什么、投错说明这样可能会有什么麻烦，反馈一律写成「这样可能会……，还可以试试……」；动手二是绿色生活计划，在家里、在学校、出门三个场景里勾选，点按钮即时生成自己的绿色一周计划；综合任务是变废为宝配对台，把六件废旧物品和它们的第二种用法配起来。插图一律为中性简洁扁平插画，不使用真人照片风格。",
    "plan_table": """| 1 | cover | 让生活多一些绿色 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：三道小选择题 | 起·前测（暴露已有经验） |
| 5 | concept | 四类桶怎么分：干净能回收，脏了就归其他 | 承·概念一（垃圾分类 + 两个易错项） |
| 6 | interactive | 动手一：垃圾分类投放台，这件垃圾该进哪个桶？ | 承·核心模拟（点选/拖放进四类桶） |
| 7 | concept | 变废为宝与低碳生活：扔之前先想一想，它还能做什么 | 承·概念二（旧物再用 + 低碳小事） |
| 8 | interactive | 动手二：绿色生活计划，挑出你能坚持的那几件 | 承·计划生成（三组勾选 → 一键生成） |
| 9 | concept | 例题示范：小禾家的一天 | 转·重难点突破（五步示范 + 易错点） |
| 10 | quiz | 概念测试：三个说法，藏着小陷阱 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：变废为宝配对台，它能变成什么？ | 合·迁移应用（配对判断） |
| 12 | quiz | 后测：换几件新东西，办法还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，讲清绿色生活怎么做 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：四类桶怎么分 / 变废为宝有妙招 / 低碳生活每一天 三栏\n- P5 四类桶与常见垃圾对照图（已生成）：附中文标注，含用过的餐巾纸与大骨头两个易错项\n- P7 变废为宝与低碳生活概念图（已生成）：附中文标注\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物\n- 课件不出现真实垃圾处理场照片，不呈现脏乱或不适画面；垃圾分类示例以通用常见物品为主\n- 各地分类标准存在差异，课件已提示以当地桶边提示与实际要求为准\n- 若需补充：本班一周垃圾产生量的统计表（由学生自己记录），不在课件中呈现任何个人或家庭信息",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
