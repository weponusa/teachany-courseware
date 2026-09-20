# -*- coding: utf-8 -*-
"""小学信息科技 · 互联网服务与应用（G5）—— 补齐知识树「互联网与人工智能」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课不背服务名称，只做三件真能上手的事：
  ① 需求匹配器：给一个生活需求 → 从四类互联网服务里挑出合适的那一类
  ② 同一需求两个办法：A / B 两个候选服务，学生判断哪个更合适、另一个为什么不合适
  ③ 读书节服务单：六张需求卡片分进四个筐（含一个「这件事不该放到网上」的筐）
最后收口到一句可带走的判断口诀：
  先问给谁看，再问改不改，最后想想该不该。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-internet-services-fig1.webp'
F2 = './assets/it-e-internet-services-fig2.webp'

TTS = {
    "hero": "先想一件事。你要把班级活动的合影发给远在外地的奶奶，你会怎么发？如果你要在网上查一查大熊猫吃什么，你又会怎么做？同样是上网，用的却不是同一种服务。互联网就像一个大工具箱，里面有专门传消息的、专门查资料的、专门几个人一起改东西的，还有专门预约办事的。今天这节课，我们不背服务的名字，只学一件事：拿到一个需求，怎样挑出最合适的那一样。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道互联网上到底有哪些服务，还是想知道面对一件事该怎么挑服务，又或者你更关心用这些服务时不能碰的几条线，再或者你想弄明白，为什么同一件事别人选的服务和你不一样。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出几种常见的互联网服务，知道它们各自擅长做什么。第二，拿到一个真实需求时，能挑出比较合适的那一类服务，并说出为什么。第三，能比较同一件事的两种做法，说清楚另一种为什么不合适。第四，能说出使用互联网服务时的几条规矩，比如别人的个人信息不能随便公开，看到没核实的消息不急着转发。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先认一认工具箱里有什么。互联网服务，就是别人做好、放在网上给我们用的功能。常用的可以分成四类。第一类是通信交流，把消息、照片、语音单独发给某个人或者一个小群。第二类是信息获取，你用关键词去查，它把资料找出来给你。第三类是协作共创，几个人可以同时改同一份文档，改动的永远是同一份。第四类是预约办事，像预约图书馆座位、报名参加活动，在网上把名额定下来。记住一件事：它们没有谁高级谁低级，只是各自擅长的事不一样。",
    "lab-1": "现在请你当一次接线员。上面会出现一个生活里的需求，下面摆着四种服务，请你点出你认为最合适的那一种。点对了会告诉你理由，点错了会提示你回头看看这个需求到底要解决什么。一共四道，慢慢来。",
    "module-2": "第二个问题：怎么挑才算挑对了？给你三道门，一个一个走过去。第一道门问范围：这件事是给一个人、几个人看，还是给所有人看？第二道门问协作：这件事要不要几个人一起改，要不要始终保留最新的那一版？第三道门问安全：这件事会不会碰到别人的信息，会不会麻烦到别人？三道门问完，合适的服务基本就浮出来了。要提醒的是，选服务不是哪个用起来最方便就用哪个，而是哪个合适才用哪个。",
    "lab-2": "接下来做一组对比。同一件事，往往有好几种做法，看起来都能办成，可是合不合适差得远。下面有三组题，每一组给你一件事和两个办法，请你点出更合适的那个，再看看另一个为什么不合适。做完之后你会发现，判断的依据一直是那三道门。",
    "worked-example": "我们一起把一道题想完整。任务是这样的：班级要办春游，需要一张报名表，让三十个同学自己填，而且随时能看到最新的人数。第一步，先问范围：这只是给本班同学看的，不用给所有人看。第二步，再问协作：三十个人都要填，而且填完还要能随时改，一定得是同一份，不能出现三十个版本。第三步，再问安全：表里只填姓名和是否参加就够了，不要顺手把电话和住址也加上，用过之后要收好。第四步，得出结论：用在线文档协作服务最合适，因为大家改的是同一份，人数一多也不乱。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。学校要办读书节，班上接到了六个小任务，有的适合放到网上做，有的压根就不该放到网上。请你把六张卡片放进下面四个筐里：通信交流、协作共创、预约办事，还有一个特别的筐，叫这件事不该放到网上。放对了会告诉你理由，放错了可以再试一次。",
    "posttest": "最后一轮，换几个新的小情境来考考你。这次会出现一个要很多信息的服务、一次网上预约，还有一张合影，看看你能不能把三道门和那几条规矩都用上去。",
    "summary": "这节课我们记住了三句话。第一句，互联网服务像一个工具箱，常用的有通信交流、信息获取、协作共创、预约办事这几类，它们没有高下之分，只是擅长的事不同。第二句，挑服务要走三道门：先问给谁看，再问改不改，最后想想该不该。第三句，用网络有几条底线不能碰：别人的个人信息不随便公开，没有核实的消息不急着转发，发照片之前先问问照片里的人。回到开头那个问题，奶奶要看照片，就单独发给她——合适，比方便更重要。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：说出四种常见的互联网服务，每种各举一个你家里用过的例子。第二层能力应用，动手做：挑一件你家里常在网上办的事，写出你们家用的是哪一类服务，为什么合适。第三层迁移挑战，选做：给班级读书节设计一份网上服务清单，把每件事该用哪类服务、要注意什么写清楚，特别标明哪些事情不该放到网上。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 工具箱里有什么", "lab-1": "动手一 需求匹配器", "module-2": "概念二 挑服务走三道门",
    "lab-2": "动手二 同一件事两个办法", "worked-example": "例题讲解 春游报名表", "conceptest-1": "概念测试",
    "synthesis": "综合任务 读书节服务单", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 四类常见互联网服务
SERVICES = [
    ("im", "通信交流服务", "把消息、照片单独发给某个人或一个小群"),
    ("search", "信息获取服务", "用关键词去查，把资料找出来"),
    ("doc", "协作共创服务", "几个人同时改同一份文档，只有一份最新版"),
    ("book", "预约办事服务", "在网上把时间、名额定下来"),
]

# 动手一：需求匹配器
NEEDS = {
    "n1": {"t": "把班级活动的合影，单独发给远方的奶奶", "ans": "im",
           "why": "这件事是给<strong>一个人</strong>看的，而且照片里有同学的脸，只发给该看的人最稳妥——通信交流服务正合适。"},
    "n2": {"t": "查一查大熊猫主要吃什么", "ans": "search",
           "why": "你要的是<strong>已经有人写好的资料</strong>，用关键词去查最直接——信息获取服务正合适。"},
    "n3": {"t": "小组四个人要同时改一份班级公约", "ans": "doc",
           "why": "四个人都要动手改，还要始终只有<strong>一份最新版</strong>——协作共创服务正合适。"},
    "n4": {"t": "预约周末去图书馆的座位", "ans": "book",
           "why": "这件事要<strong>把一个名额定下来</strong>，定完还得算数——预约办事服务正合适。"},
}

# 动手二：同一件事，两个办法（A / B 判断，逻辑写在 CUSTOM_JS 的 PAIRS 里）

# 综合任务：六张卡片分进四个筐
CARD_POOL = [
    ("c1", "把班级合影单独发给奶奶", "im", "这是发给一个人的消息，住通信交流筐。"),
    ("c2", "小组四人同时改一份班级公约", "doc", "几个人改同一份，是协作共创。"),
    ("c3", "预约周末图书馆的座位", "book", "把名额定下来，属于预约办事。"),
    ("c4", "报名参加读书节的朗读活动", "book", "报名也是把名额定下来，同样是预约办事。"),
    ("c5", "把同学的身份证号发到公开的地方，让大家都来核对", "never",
     "同学身份证号是最要紧的个人信息，不管出于什么理由，都不该发到公开的地方——这件事不该放到网上。"),
    ("c6", "把网上看到、还没核实的「紧急通知」转发到公开的地方", "never",
     "自己都没核实过就转发，等于帮别人传了没影的话——这件事不该放到网上。"),
]

BINS = [
    ("im", "通信交流"),
    ("doc", "协作共创"),
    ("book", "预约办事"),
    ("never", "⚠️ 这件事不该放到网上"),
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-internet-services 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：需求匹配器（给需求 → 从四类服务里挑一类）
   3) 动手二：同一件事两个办法（A / B 判断更合适的那个）
   4) 综合任务：六张卡片分进四个筐
   ============================================================ */
(function () {
  'use strict';

  var st = document.createElement('style');
  st.textContent =
    '.svc-need{display:flex;gap:10px;align-items:flex-start;padding:14px 16px;border-radius:14px;' +
    'background:var(--warm-soft);border:1px dashed var(--warm);font-size:16px;font-weight:700;}' +
    '.svc-need .emoji{font-size:20px;line-height:1.3;}' +
    '.pair-card{border:2px solid var(--line-subtle);border-radius:14px;padding:14px 16px;background:var(--bg-subtle);' +
    'cursor:pointer;transition:border-color .25s ease,background .25s ease;margin:0;}' +
    '.pair-card:hover{border-color:var(--brand);}' +
    '.pair-card.picked-right{border-color:var(--ok);background:rgba(34,197,94,.10);}' +
    '.pair-card.picked-wrong{border-color:var(--danger);background:rgba(239,68,68,.09);}';
  document.head.appendChild(st);

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

  /* ---------- 2. 动手一：需求匹配器 ---------- */
  var matcher = document.getElementById('svc-matcher');
  if (matcher) {
    var NEED = {
      n1: { t: '把班级活动的合影，单独发给远方的奶奶', ans: 'im',
            why: '这件事是给<strong>一个人</strong>看的，而且照片里有同学的脸，只发给该看的人最稳妥——通信交流服务正合适。' },
      n2: { t: '查一查大熊猫主要吃什么', ans: 'search',
            why: '你要的是<strong>已经有人写好的资料</strong>，用关键词去查最直接——信息获取服务正合适。' },
      n3: { t: '小组四个人要同时改一份班级公约', ans: 'doc',
            why: '四个人都要动手改，还要始终只有<strong>一份最新版</strong>——协作共创服务正合适。' },
      n4: { t: '预约周末去图书馆的座位', ans: 'book',
            why: '这件事要<strong>把一个名额定下来</strong>，定完还得算数——预约办事服务正合适。' }
    };
    var NAME = { im: '通信交流服务', search: '信息获取服务', doc: '协作共创服务', book: '预约办事服务' };
    var solved = {}, cur = 'n1';
    var needBox = document.getElementById('svc-need-text');
    var out1 = document.getElementById('svc-verdict');

    function paint1() {
      var left = 0;
      Object.keys(NEED).forEach(function (k) { if (!solved[k]) left++; });
      needBox.textContent = NEED[cur].t;
      matcher.querySelectorAll('[data-need]').forEach(function (b) {
        b.classList.toggle('done', !!solved[b.dataset.need]);
        b.classList.toggle('selected', b.dataset.need === cur && !solved[b.dataset.need]);
        b.disabled = !!solved[b.dataset.need];
      });
      document.getElementById('svc-progress').textContent = (4 - left) + ' / 4 个需求已解决';
      if (left === 0) {
        out1.className = 'result';
        out1.innerHTML = '<strong>四个需求全部接对了！</strong>回头看看你刚才的判断：每一个都问过同一件事——' +
          '这个需求到底要解决什么？是发给一个人、是要一份资料、是几个人一起改，还是要把一个名额定下来。';
      }
    }

    matcher.querySelectorAll('[data-need]').forEach(function (b) {
      b.addEventListener('click', function () {
        if (solved[b.dataset.need]) return;
        cur = b.dataset.need;
        paint1();
        out1.className = 'result warn';
        out1.textContent = '当前需求：' + NEED[cur].t + '。请从下面四种服务里点出最合适的一种。';
      });
    });

    matcher.querySelectorAll('[data-svc]').forEach(function (b) {
      b.addEventListener('click', function () {
        var k = b.dataset.svc;
        if (solved[cur]) return;
        if (NEED[cur].ans === k) {
          solved[cur] = true;
          out1.className = 'result';
          out1.innerHTML = '<strong>接对了：' + NAME[k] + '。</strong>' + NEED[cur].why;
          b.classList.add('correct');
          setTimeout(function () { b.classList.remove('correct'); }, 1600);
          var next = null;
          Object.keys(NEED).forEach(function (n) { if (!solved[n] && !next) next = n; });
          if (next) cur = next;
          paint1();
        } else {
          out1.className = 'result error';
          out1.innerHTML = '<strong>再想一想：' + NAME[k] + '不适合这件事。</strong>' + NAME[k] + '擅长的是' +
            (k === 'im' ? '把消息单独发给某个人或一个小群。'
              : k === 'search' ? '用关键词把别人写好的资料找出来。'
              : k === 'doc' ? '几个人同时改同一份文档。'
              : '把时间或名额在网上定下来。') +
            '<br><span style="color:var(--muted)">常见错误：只看「能不能办成」，不看「合不合适」。' +
            '很多服务都能把一件事勉强办完，但范围、版本、安全这几件事对不上，就会出问题。</span>';
        }
      });
    });
    paint1();
  }

  /* ---------- 3. 动手二：同一件事两个办法 ---------- */
  var pairPanel = document.getElementById('pair-panel');
  if (pairPanel) {
    var PAIRS = {
      0: { need: '把班级活动的合影，发给远方的奶奶',
           a: '用通信交流服务，只发给奶奶一个人',
           b: '发在所有人都能看到的地方，让奶奶自己去找',
           good: 'a',
           whyGood: '照片里有同学的脸，只发给该看的人，范围最小、最稳妥。',
           whyBad: '发到所有人都能看到的地方，等于把全班同学的样子公开了出去——既没问过大家，也没必要。' },
      1: { need: '想知道下一班公交车还有几站到',
           a: '用实时信息查询服务，看这趟车现在到哪儿了',
           b: '用信息获取服务，搜「公交车」三个字',
           good: 'a',
           whyGood: '你要的是「此刻」的情况，只有实时信息查询这一类服务会不断更新。',
           whyBad: '搜出来的是别人以前写好的文章，讲的是公交车怎么回事，回答不了「下一班还有几站」这个当下问题。' },
      2: { need: '小组四个人要同时改一份班级公约',
           a: '每人改一份，改完互相发来发去',
           b: '用协作共创服务，四个人改的就是同一份',
           good: 'b',
           whyGood: '大家改的是同一份，谁改了什么一眼看得见，不会出现「哪句才是最新的」这种麻烦。',
           whyBad: '四个人各改一份，最后会有四份不一样的文件，谁的才是最新的根本说不清。' }
    };
    var round = 0, answered = false;
    var needEl = document.getElementById('pair-need');
    var aEl = document.getElementById('pair-a');
    var bEl = document.getElementById('pair-b');
    var out2 = document.getElementById('pair-verdict');

    function loadRound() {
      var p = PAIRS[round];
      answered = false;
      needEl.textContent = '第 ' + (round + 1) + ' 组　需求：' + p.need;
      aEl.querySelector('.pair-text').textContent = '办法 A：' + p.a;
      bEl.querySelector('.pair-text').textContent = '办法 B：' + p.b;
      aEl.className = 'pair-card';
      bEl.className = 'pair-card';
      document.getElementById('pair-progress').textContent = '第 ' + (round + 1) + ' / 3 组';
      out2.className = 'result warn';
      out2.textContent = '读一读这件事，点出你认为更合适的那个办法。';
      document.getElementById('pair-next').disabled = true;
    }

    function choose(which) {
      if (answered) return;
      answered = true;
      var p = PAIRS[round];
      var picked = which === 'a' ? aEl : bEl;
      var other = which === 'a' ? bEl : aEl;
      picked.classList.add(which === p.good ? 'picked-right' : 'picked-wrong');
      other.classList.add(which === p.good ? 'picked-wrong' : 'picked-right');
      if (which === p.good) {
        out2.className = 'result';
        out2.innerHTML = '<strong>选得好。</strong>' + p.whyGood + '<br>另一个办法的问题在于：' + p.whyBad;
      } else {
        out2.className = 'result error';
        out2.innerHTML = '<strong>再看看。</strong>另一个办法更合适，因为' + p.whyGood +
          '<br>你刚选的这个，问题在于：' + p.whyBad +
          '<br><span style="color:var(--muted)">常见错误：以为「反正都能办成，选哪个都一样」——' +
          '范围、版本和安全这三样对不上，办事的过程中就会出麻烦。</span>';
      }
      var nb = document.getElementById('pair-next');
      if (round < 2) {
        nb.disabled = false;
        nb.textContent = '下一组 →';
      } else {
        nb.disabled = true;
        nb.textContent = '已经到最后一组了';
      }
    }

    aEl.addEventListener('click', function () { choose('a'); });
    bEl.addEventListener('click', function () { choose('b'); });
    document.getElementById('pair-next').addEventListener('click', function () {
      if (round < 2) { round++; loadRound(); }
    });
    loadRound();
  }

  /* ---------- 4. 综合任务：分进四个筐 ---------- */
  var bank4 = document.getElementById('card-pool');
  if (bank4) {
    var picked4 = null, done4 = 0;
    var out4 = document.getElementById('card-verdict');

    bank4.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        bank4.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked4 = card;
        out4.className = 'result warn';
        out4.textContent = '已选中「' + card.textContent.trim() + '」，现在点下面你认为对的那个筐。';
      });
    });

    document.querySelectorAll('[data-card-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked4) {
          out4.className = 'result warn';
          out4.textContent = '先点上面的一张卡片，再点筐。';
          return;
        }
        var want = picked4.dataset.kind, got = bin.dataset.cardBin;
        picked4.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = picked4.textContent.trim() + ' ✓';
          bin.querySelector('.bin-body').appendChild(tag);
          picked4.classList.add('done');
          picked4.disabled = true;
          done4++;
          out4.className = 'result';
          out4.innerHTML = '<strong>放对了！</strong>' + picked4.dataset.why;
          bin.classList.add('ok');
          picked4 = null;
          if (done4 === 6) {
            out4.className = 'result';
            out4.innerHTML = '<strong>六张卡片全部归位。</strong>最后再记住那道最关键的判断：' +
              '一件事能不能放到网上做，先看它会不会碰到<strong>别人的信息</strong>，' +
              '再看自己有没有<strong>核实过</strong>。这两条过不去，再方便也不做。';
          }
        } else {
          out4.className = 'result error';
          out4.innerHTML = '<strong>再想一下：「' + picked4.textContent.trim() + '」</strong>' +
            '先问自己三句话：这件事是发给人的，还是几个人一起改的，还是把名额定下来？' +
            '再补一句：它会不会碰到别人的信息？<br>' +
            '<span style="color:var(--muted)">常见错误：只按「办什么事」分，忘了看「会不会伤到别人」。' +
            '有两张卡片，不管办得成办不成，都不该放到网上。</span>';
          picked4.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
      });
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：同一件事，你会挑哪种服务？", TTS["pretest"], [
        {"q": "下面哪件事，适合用「只把消息发给一个人」这类服务？",
         "options": [("把班级活动的合影发给远方的奶奶", True),
                     ("把活动通知告诉全校同学", False),
                     ("查一查大熊猫主要吃什么", False)],
         "explain": "发给一个人、一个小群，用通信交流类的服务。通知全校要发给很多人，查资料又是另一回事。"
                    "<strong>错因提醒：</strong>常见错误是把「发给谁」和「发什么」搞混——"
                    "先看要给几个人看，服务的类型基本就定了。"},
        {"q": "想知道下一班公交车还有几站到，哪种做法最直接？",
         "options": [("用会不断更新的实时信息查询服务", True),
                     ("用信息获取服务搜「公交车」三个字", False),
                     ("在公开的地方发一句「有人知道吗」", False)],
         "explain": "「现在到哪儿了」这种随时在变的信息，只有实时查询类服务答得上来。"
                    "<strong>错因提醒：</strong>容易误认为「上网查一查都一样」。"
                    "搜出来的是别人以前写好的文章，回答不了此刻的问题。"},
        {"q": "有同学把班里另一位同学的手机号，发到了所有人都能看到的地方。这样做最主要的问题是什么？",
         "options": [("没经过同意，就把别人的个人信息公开了出去", True),
                     ("手机号可能写错了一位数字", False),
                     ("发的时间太晚，大家看不到", False)],
         "explain": "手机号是别人的个人信息。要不要公开、给谁看，得由他自己说了算。"
                    "<strong>错因提醒：</strong>「反正大家都是同学」是最常见的错误想法——"
                    "信息一旦公开出去，就收不回来了。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "互联网服务就像一个工具箱，各有各的擅长", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们天天在网上传消息、查资料，其实已经在用互联网服务了（And）；可同一件事换一种服务做，效果会差很远，用错了还可能伤到别人（But）；所以我们要认出工具箱里有哪几样，并且学会挑最合适的那一样（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>互联网服务</strong>，简单说就是别人做好、放在网上给我们用的功能。常用的可以分成四大类。</p>
        <div class="grid grid-2">
          <div class="inner-card"><p><strong>💬 通信交流</strong></p><p style="color:var(--muted)">把消息、照片、语音，单独发给某个人或一个小群。</p></div>
          <div class="inner-card"><p><strong>🔎 信息获取</strong></p><p style="color:var(--muted)">用关键词去查，把已经有人写好的资料找出来。</p></div>
          <div class="inner-card"><p><strong>📄 协作共创</strong></p><p style="color:var(--muted)">几个人同时改同一份文档，始终只有一份最新版。</p></div>
          <div class="inner-card"><p><strong>📅 预约办事</strong></p><p style="color:var(--muted)">在网上把时间、名额定下来，定完就算数。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="四类常见互联网服务与对应生活场景示意图：通信交流、信息获取、协作共创、预约办事">
          <figcaption>同一个工具箱里的四类服务，各自对应不同的生活场景——没有谁更高级，只是擅长的事不同</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🧰</span><div><strong>打一个比方：</strong>互联网服务就像家里那个工具箱。工具箱里有锤子、有螺丝刀，也有尺子。锤子再好，也不能拿来拧螺丝——<strong>合不合适，比好不好更重要</strong>。</div></div>
{insight_box([
    {"lens": "看见它", "text": "打开家里的手机看看：你家的每一件线上小事，背后都属于这四类里的某一类。"},
    {"lens": "比较它", "text": "同一件事往往能被好几类服务勉强办成——区别不在「能不能」，而在「合不合适」。"},
    {"lens": "迁移它", "text": "以后遇到一个新需求，先别急着打开某个应用，先判断它属于哪一类，再去找对应那一类里的服务。"},
])}
    ''', tag="概念一"))

    need_btns = "\n".join(
        f'            <button class="sort-item" data-need="{k}">{v["t"]}</button>'
        for k, v in NEEDS.items()
    )
    svc_btns = "\n".join(
        f'            <button class="choice" data-svc="{k}" style="text-align:center">{cn}<br><span style="color:var(--muted);font-size:13px">{d}</span></button>'
        for k, cn, d in SERVICES
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：需求匹配器", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点上面任意一个需求，再从下面四种服务里点出最合适的那一种。四道都接对，就通关了。</p>
        <div class="lab-panel" id="svc-matcher">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 四个生活需求（点它，开始处理）</div>
          <div class="sort-bank">
{need_btns}
          </div>
          <div class="svc-need" style="margin-top:14px"><span class="emoji">📌</span><span id="svc-need-text">先选一个需求</span></div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">② 四种服务，选一种接上去</div>
          <div class="grid grid-2">
{svc_btns}
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">进度</span><span class="v" id="svc-progress">0 / 4 个需求已解决</span></div>
          </div>
          <p class="result warn" id="svc-verdict" style="margin-top:12px">先选一个需求。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>发现了吗：</strong>决定选哪一类的，从来不是「哪个应用你最熟」，而是这件事本身<strong>要给谁看、要几个人一起做、要不要把名额定下来</strong>。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "挑服务走三道门：给谁看、改不改、该不该", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">服务那么多，怎么挑才不会挑错？给你<strong>三道门</strong>，一个一个走过去。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>第一道门·给谁看：</strong>这件事是给一个人、少数几个人看，还是给所有人看？范围越小的服务，越不容易出问题。</div></div>
          <div class="step"><span class="n">2</span><div><strong>第二道门·改不改：</strong>这件事要不要几个人一起动手改？要不要始终保留最新的那一版？要，就找能一起改的。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>第三道门·该不该：</strong>会不会碰到别人的信息？自己有没有核实过？这一道门过不去，前面两道门就别再走了。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="挑选互联网服务的三道门示意图：给谁看、改不改、该不该，逐道通过后得到合适的服务">
          <figcaption>三道门：先问给谁看，再问改不改，最后想想该不该——三道都过了，才轮到「用起来方不方便」</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">只按「哪个用起来最方便」来挑。方便是好事，但<strong>方便排在三道门后面</strong>。一个用起来很方便的服务，如果把范围放得太开、或者碰到别人的信息，那它就不合适。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🔐</span><div><strong>记一句口诀：</strong>先问给谁看，再问改不改，最后想想该不该。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：同一件事，两个办法，哪个更合适？", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">每一组都有两个办法，看起来都能把事办成。请点出你认为更合适的那个，再看解释。</p>
        <div class="lab-panel" id="pair-panel">
          <div class="svc-need"><span class="emoji">📌</span><span id="pair-need">第 1 组</span></div>
          <div class="grid grid-2" style="margin-top:14px">
            <div class="pair-card" id="pair-a"><p><strong>办法 A</strong></p><p class="pair-text" style="color:var(--muted);font-size:14px;margin:0">—</p></div>
            <div class="pair-card" id="pair-b"><p><strong>办法 B</strong></p><p class="pair-text" style="color:var(--muted);font-size:14px;margin:0">—</p></div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">当前进度</span><span class="v" id="pair-progress">第 1 / 3 组</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="pair-next" style="text-align:center" disabled>下一组 →</button>
          </div>
          <p class="result warn" id="pair-verdict" style="margin-top:12px">读一读这件事，点出你认为更合适的那个办法。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>做完三组，回头看：</strong>每一组你判断的依据，其实都是同一件事——<strong>范围、版本、安全</strong>。把这三样想清楚了，服务就挑对了。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：给春游报名表挑一个服务", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>班级要办春游，需要一张报名表，让三十个同学自己填，还要能随时看到最新的人数。该用哪一类互联网服务？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先问给谁看：</strong>这张表只给本班同学填，不用给所有人看——所以范围要收在本班以内。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再问改不改：</strong>三十个人都要填，填完还可能要改。一定得是<strong>同一份</strong>，不能出现三十个版本。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>最后想想该不该：</strong>表里只留姓名和「参加 / 不参加」就够了，不要顺手把电话、住址也加上；用完之后要把表收起来。</div></div>
          <div class="step"><span class="n">4</span><div><strong>得出结论：</strong>用<strong>协作共创服务</strong>最合适——大家改的是同一份，人数一多也不会乱，还能随时看到最新结果。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学提议「一人填一份，填完都发到群里」。这样确实每个人都能填，可最后会出现三十份不一样的文件，<strong>哪一份才是最新的，谁也说不清</strong>。办事的过程一乱，结果就容易出错。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "挑互联网服务的时候，最重要的判断标准是什么？",
         "options": [("这个服务适合这件事，也不越界", True),
                     ("哪个用起来最方便就用哪个", False),
                     ("哪个看起来最热闹用哪个", False)],
         "explain": "方便只是最后才考虑的一条。先要看范围、版本和安全这三道门过得去不过去。"
                    "<strong>错因提醒：</strong>最常见的是「方便优先」，觉得能省事就好——"
                    "方便的服务如果范围放得太开，反而容易出问题。"},
        {"q": "小组四个人要同时改一份班级公约，哪种做法最合适？",
         "options": [("用协作共创服务，四个人改的就是同一份", True),
                     ("每人改一份，改完互相发来发去", False),
                     ("各自把改动记在心里，见面再说", False)],
         "explain": "大家改同一份，谁改了什么一眼看得见，永远只有一份最新版。"
                    "<strong>错因提醒：</strong>容易误认为「反正最后合在一起就行」。"
                    "四个版本混在一起的时候，最要紧的那句到底是谁改的，就说不清了。"},
        {"q": "在网上看到一条标题很吓人的「紧急通知」，最稳妥的做法是什么？",
         "options": [("先找一找有没有可靠来源，没核实之前不转发", True),
                     ("赶紧转发到各个群里，让大家早点知道", False),
                     ("换个更醒目的标题再发一次", False)],
         "explain": "没核实就转发，等于帮别人把没影的话传得更远。想帮大家，先核实。"
                    "<strong>错因提醒：</strong>这里最常见的错误想法是「我是在做好事」——"
                    "好意不等于准确，转发的人也要为传出去的话负责。"}
    ], tag="概念测试"))

    card_btns = "\n".join(
        f'          <button class="sort-item" data-kind="{kind}" data-why="{why}">{t}</button>'
        for _k, t, kind, why in CARD_POOL
    )
    bin_html = "\n".join(f'''            <div class="sort-bin" data-card-bin="{k}">
              <h4>{label}</h4>
              <div class="bin-body"></div>
            </div>''' for k, label in BINS)
    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：读书节服务单", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张卡片，再点你认为对的那个筐。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待归位的六张卡片</div>
          <div class="sort-bank" id="card-pool">
{card_btns}
          </div>
          <div class="sort-bins" style="grid-template-columns:repeat(2,1fr)">
{bin_html}
          </div>
          <p class="result warn" id="card-verdict" style="margin-top:12px">点一张卡片开始归位。</p>
        </div>
        <div class="inner-card">
          <p><strong>放完以后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">两个「不该放到网上」的筐里，装的是两件不一样的事：一件碰到了别人的个人信息，一件是自己没核实过。你还能各举一个身边的例子吗？</p>
          <textarea id="syn-answer" rows="3" placeholder="碰到别人信息的例子是……没核实过的例子是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，三道门还在不在", TTS["posttest"], [
        {"q": "有个人只想查一下公交到站，那个服务却要他填手机号、家庭住址，还要开摄像头。你会怎么办？",
         "options": [("换一个只要必要信息的服务，或者只填真正用得上的那一项", True),
                     ("反正要用，全填了省事", False),
                     ("先填一个假的，用完再改回来", False)],
         "explain": "办一件小事却要走这么多信息，说明这个服务要的东西超出了它该要的范围。"
                    "<strong>错因提醒：</strong>常见错误是「反正要用就全填了」。"
                    "信息给得越多，将来收不回来的也越多。"},
        {"q": "妈妈想在手机上预约一次体检，这属于哪一类互联网服务？",
         "options": [("预约办事类", True), ("信息获取类", False), ("协作共创类", False)],
         "explain": "预约的本质是把一个时间或名额在网上定下来，定完就算数——这是预约办事类服务。"
                    "<strong>错因提醒：</strong>容易和「信息获取」搞混。查资料只是看一看，预约是<strong>真的占掉一个名额</strong>，办完不能当没发生。"},
        {"q": "班级合影里有同学的脸，要把它发给别人看，最稳妥的第一步是什么？",
         "options": [("先问问照片里的同学同不同意，再决定发给谁、发到哪儿", True),
                     ("直接发到所有人都能看到的地方，热闹一点", False),
                     ("先发出去，有人反对再删掉", False)],
         "explain": "照片里是别人的样子，发到哪儿、给谁看，得先问过他们。"
                    "<strong>错因提醒：</strong>「先发出去，有人反对再删」是很常见的想法——"
                    "可是看到的人可能已经存下来了，删掉也追不回来。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把挑服务这件事讲清楚", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>工具箱里有什么：</strong>通信交流、信息获取、协作共创、预约办事四类，没有高下之分，只是擅长的事不同。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>怎么挑：</strong>先问给谁看，再问改不改，最后想想该不该——三道门都过了，才轮到「方不方便」。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>底线在哪：</strong>别人的个人信息不随便公开；没核实过的消息不急着转发；发照片之前先问问照片里的人。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>还有一条容易被忽略的：</strong>服务再方便，也要有停下来的时间。给自己定一个用网的时间边界，什么时候用、用多久，由你来定，不是由手机来定。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「给谁看、改不改、该不该」这三句话，说清楚为什么把合影单独发给奶奶更稳妥。</p>
          <p style="color:var(--muted)">再动一动手：<strong>列出来</strong>——把家里人在网上办的三件事写下来，各标出它属于哪一类服务。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "说出四种常见的互联网服务，每种再举一个你家里用过的例子。",
            "背一背挑服务的口诀：先问给谁看，再问改不改，最后想想该不该。",
        ],
        [
            "挑一件你家里常在网上办的事，写出你们家用的是哪一类服务，并说说为什么合适。",
            "找出一件「本来可以用另一类服务办得更好」的事，说说换成哪一类会更好，为什么。",
        ],
        [
            "给班级读书节设计一份网上服务清单：每件事该用哪一类服务、要注意什么，都写清楚。",
            "在那份清单里特别标出「哪些事情不该放到网上」，并写明理由。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-internet-services",
    "node_id": "it-e-internet-services",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "互联网服务与应用",
    "name_en": "Internet Services: Choosing the Right Tool",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "internet-ai",
    "domain_cn": "互联网与人工智能",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学五年级：认识通信交流、信息获取、协作共创、预约办事四类常见互联网服务，能用「给谁看、改不改、该不该」三道门为真实需求挑出合适的服务，并知道个人信息保护与不传未核实信息这两条底线。",
    "tags": ["互联网服务", "选择服务", "协作", "个人信息", "信息社会责任"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「互联网与人工智能」——了解常见互联网服务，安全、负责任地使用网络。",
    "hero_question": "同样是上网，为什么发给奶奶的照片要用一种服务，查资料又要用另一种？",
    "hero_alt": "互联网服务与应用知识结构图：四类常见服务、挑服务的三道门、使用网络的三条底线",
    "hero_caption": "四类服务：通信交流 · 信息获取 · 协作共创 · 预约办事　|　三道门：给谁看 · 改不改 · 该不该",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "互联网上到底有哪些服务？", "d": "想把工具箱里的东西认全", "v": "互联网上到底有哪些服务"},
        {"t": "面对一件事，怎么挑出合适的服务？", "d": "想让自己的选择有个依据", "v": "面对一件事怎么挑出合适的服务"},
        {"t": "用这些服务时，有哪些线不能碰？", "d": "想知道怎么做才不出事", "v": "用这些服务时有哪些线不能碰"},
        {"t": "为什么同一件事，别人选的服务和我不一样？", "d": "想弄明白判断的标准是什么", "v": "为什么同一件事别人选的服务和我不一样"},
    ],
    "objectives": [
        "能说出几种常见的互联网服务，知道它们各自擅长做什么",
        "拿到一个真实需求时，能挑出比较合适的那一类服务，并说出为什么",
        "能比较同一件事的两种做法，说清楚另一种为什么不合适",
        "能说出使用互联网服务时的几条规矩，例如不公开别人的个人信息、不转发没核实的消息",
    ],
    "objectives_plain": [
        "能说出几种常见的互联网服务，知道它们各自擅长做什么",
        "拿到一个真实需求时，能挑出比较合适的那一类服务，并说出为什么",
        "能比较同一件事的两种做法，说清楚另一种为什么不合适",
        "能说出使用互联网服务时的几条规矩，例如不公开别人的个人信息、不转发没核实的消息",
    ],
    "standards": [
        {"content": "了解常见互联网服务，安全、负责任地使用网络",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能"},
        {"content": "在真实需求中比较不同服务的适用性，初步形成「选择合适服务」的判断习惯和保护个人信息、不传播未核实信息的责任感",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能 / 信息社会责任"},
    ],
    "prereqs": [],
    "prereqs_name": "本课是信息科技小学段「互联网与人工智能」的起始课，不需要先修节点",
    "prereqs_meta": "",
    "leads_to": ["it-e-network-security-basic"],
    "next_meta": "it-e-network-security-basic",
    "section_images": ["assets/it-e-internet-services-fig1.webp", "assets/it-e-internet-services-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "同样是在网上做事，为什么有的用这个、有的用那个？说说你的想法。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能给一件事挑出合适的服务，并说出理由。",
        "objectives": "看清四件事：有哪些服务、怎么挑、怎么比较两个办法、哪些线不能碰。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "互联网服务像工具箱：传消息的、查资料的、一起改东西的、预约办事的，各有各的擅长。",
        "lab-1": "先点需求，再点服务。判断的依据不是「哪个你最熟」，而是这件事要找谁、要几个人做。",
        "module-2": "三道门：给谁看、改不改、该不该。三道都过了，才轮到「方不方便」。",
        "lab-2": "每一组两个办法都能办成事，区别在于范围、版本和安全。",
        "worked-example": "四步走：先问给谁看、再问改不改、最后想想该不该，然后才得出结论。",
        "conceptest-1": "三个说法里都藏着高频错误，选完把解释读一遍。",
        "synthesis": "有两个筐装的是「不该放到网上」的事：一件碰到别人的信息，一件自己没核实过。",
        "posttest": "要很多信息的服务、一次网上预约、还有一张合影，看看三道门管不管用。",
        "summary": "三句话：工具箱里有什么、怎么挑、底线在哪。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「互联网与人工智能」的起始一课。五年级学生的常见问题是「哪个用起来最方便就用哪个」，以及把服务名称背下来却不会挑。所以全课不背名称，只做三件真能上手的事：先用一个需求匹配器，让学生把四个生活需求分别接上四类服务（点错会指出这一类服务真正擅长什么）；再用「同一件事两个办法」做三轮 A/B 判断，让「范围、版本、安全」这三条依据在对比中被看得清清楚楚；最后用读书节服务单把六张卡片分进四个筐——其中特意留了一个「这件事不该放到网上」的筐，装两件性质不同的事（碰到别人的个人信息、没核实过就转发），把信息社会责任落在具体的判断上。概念页把挑服务的依据收成一句口诀（先问给谁看，再问改不改，最后想想该不该），并强调方便排在三道门之后。全课不出现任何真实平台品牌，只讲服务类型。",
    "plan_table": """| 1 | cover | 互联网服务与应用 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：同一件事，你会挑哪种服务？ | 起·前测（暴露直觉） |
| 5 | concept | 互联网服务就像一个工具箱，各有各的擅长 | 承·概念一（四类服务 + 类比 + 生活场景） |
| 6 | interactive | 动手一：需求匹配器 | 承·动手模拟（四个需求 × 四类服务，逐题即时反馈） |
| 7 | concept | 挑服务走三道门：给谁看、改不改、该不该 | 承·概念二（三道门 + 口诀 + 常见错误） |
| 8 | interactive | 动手二：同一件事，两个办法，哪个更合适？ | 承·对比判断（三轮 A/B，含未核实转发陷阱） |
| 9 | concept | 例题示范：给春游报名表挑一个服务 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：读书节服务单 | 合·迁移应用（六张卡片分四筐，含「不该放到网上」） |
| 12 | quiz | 后测：换几个情境，三道门还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把挑服务这件事讲清楚 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：四类常见服务 / 挑服务三道门 / 使用网络三条底线 三栏\n- P5 四类服务与生活场景示意图（已生成）：通信交流、信息获取、协作共创、预约办事\n- P7 挑服务三道门示意图（已生成）：给谁看 → 改不改 → 该不该\n- 三张图均为教学示意图，画面中不出现任何真实平台品牌、界面或商标\n- 若需补充：家庭上网场景照片（需获得授权后使用）",
}
