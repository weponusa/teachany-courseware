# -*- coding: utf-8 -*-
"""小学科学 · 微生物：小到看不见的居民（G5）—— 补齐课标「生命系统的构成层次·5.2 不同类型的生物」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-microorganisms-fig1.webp'
F2 = './assets/sci-e-microorganisms-fig2.webp'

TTS = {
    "hero": "先来看一样东西。你的手上、空气里，还有一块放了几天的馒头上，住着一群小到看不见的居民。用眼睛根本看不见它们，可它们真实存在着，数量比地球上的人还要多得多。它们是谁？对我们到底是好还是坏？这节课我们就去认识这些看不见的邻居。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道这些小家伙到底有多小，还是想知道它们长什么样、分成哪几类，又或者你想弄清楚它们对我们的身体和生活有什么用。选好之后，带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出微生物是一类个体微小、要借助显微镜才能看清的生物。第二，能说出细菌、真菌、病毒是常见的三类微生物。第三，能举例说明有的微生物对人有害，有的对人有益。第四，能说出有益的微生物在做饭、分解垃圾这些事里的作用。",
    "pretest": "先做三道小题，用你现在的想法选就好，选完马上能看到解释。选错了也没关系，正好知道要重点听哪里。",
    "module-1": "我们先把微生物的样子看清楚。它最大的特点就是小。小到什么程度呢？一滴水里可以住着几百万个细菌，用眼睛、用放大镜都看不清，必须借助显微镜。第二个特点是多，它们几乎无处不在：土壤里、水里、空气里、还有我们的皮肤上，都有它们。常见的微生物主要有三类：细菌、真菌和病毒。霉菌和酵母菌属于真菌，感冒病毒属于病毒。",
    "lab-1": "现在请你转动放大倍数，自己看一看。先从肉眼看起，再换成放大镜，最后换成显微镜。每调一次，画面里的东西都会变多、变清楚。看完你就明白，为什么科学家一定要用显微镜才能研究微生物。",
    "module-2": "微生物不都是坏家伙。我们身边很多好吃的东西，都离不开它们。发面做馒头、烤面包要用酵母菌，它让面团里充满小气泡；做酸奶、泡菜要用乳酸菌；土壤里的细菌会把落叶和垃圾分解成肥料，帮植物长大，也能帮污水厂把水变干净。当然，也有会捣乱的微生物：食物上长的霉菌让食物变质不能吃，致病的大肠杆菌和感冒病毒会让人生病。所以对微生物，不能一句好或一句坏就说完了，要看是哪一种、在什么地方。",
    "lab-2": "下面请你当一次分类员。这里有几个常见微生物的名字，请你把它们放进两个筐：对我们有益的，和对我们有害的。放之前先想一想，它出现在哪里，它做过什么。放错了会告诉你原因。",
    "worked-example": "我们一起分析一个问题：馒头为什么能变得又软又大？第一步，先找出是谁在帮忙，是酵母菌。第二步，看它属于哪一类，酵母菌是一种真菌，属于微生物。第三步，说清它做了什么，酵母菌在面团里生长繁殖，产生了很多小气泡，把面团撑了起来。第四步，得出结论，馒头变大是酵母菌帮的忙，所以微生物也能为人服务。",
    "conceptest-1": "下面有三道容易弄错的说法，请你仔细读每一个选项，选完再看解释，看看自己有没有掉进那几个常见的坑里。",
    "synthesis": "最后一件事交给你。如果给你一小杯酸奶，和一块放了几天、长了绿毛的面包，你会怎么比较它们？先说哪一样还能吃、哪一样不能吃，再说出你的理由，最后说说你从中学到了什么。",
    "posttest": "最后一轮，用新的情境检验一下。这里面有手上的细菌、有疫苗、有做面包，看看你能不能把学到的知识用上去。",
    "summary": "这节课我们认识了一群看不见的邻居。微生物个体微小，要借助显微镜才能看清；常见的有细菌、真菌和病毒三类。它们有的对我们有益，比如酵母菌帮我们发面、乳酸菌帮我们做酸奶、土壤里的细菌分解垃圾；也有的对我们有害，比如让食物发霉的霉菌、致病的大肠杆菌和感冒病毒。回到开头那块馒头上的小居民，它们不全是坏蛋，也不全是好人，关键要看是哪一种，还要看它在做什么。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出微生物的两个特点，并说出常见微生物的三类名字。第二层能力应用，动手做：调查家里三样和微生物有关的东西，写清楚各用到了哪一种微生物。第三层迁移挑战，选做：设计一个小实验，观察两块面包在潮湿和干燥的环境里哪一块先长出霉斑，把每天看到的变化记下来。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 微生物有多小", "lab-1": "实验室一 显微镜观察台", "module-2": "概念二 有益的与有害的",
    "lab-2": "实验室二 益害分类筐", "worked-example": "例题讲解 馒头为什么变大", "conceptest-1": "概念测试",
    "synthesis": "综合任务 酸奶与发霉面包", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

SORT_ITEMS = [
    {"id": "yeast", "t": "酵母菌", "kind": "good",
     "why": "发面做馒头、烤面包都靠它。酵母菌在面团里生长，放出小气泡，把面团撑得又软又大。"},
    {"id": "lactic", "t": "乳酸菌", "kind": "good",
     "why": "做酸奶和泡菜离不开它，它还能帮我们的肠道更好地工作。"},
    {"id": "decompose", "t": "分解垃圾的细菌", "kind": "good",
     "why": "它们把落叶和厨余垃圾分解成肥料，还能在污水厂里帮忙把水变干净。"},
    {"id": "ecoli", "t": "致病的大肠杆菌", "kind": "bad",
     "why": "不干净的水和没洗净的蔬菜上可能带着它，吃进肚子里会让人拉肚子。要注意，肠道里也有帮我们的细菌，不能一见到细菌就说它坏。"},
    {"id": "mold", "t": "霉菌", "kind": "bad",
     "why": "面包和水果上长出的绿毛就是霉菌，食物一旦发霉就不能再吃了。"},
    {"id": "virus", "t": "感冒病毒", "kind": "bad",
     "why": "感冒病毒钻进我们的身体里，会让人发烧、咳嗽、打喷嚏。"},
]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-microorganisms 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 显微镜观察台：放大倍数滑块 → 肉眼 / 放大镜 / 显微镜三级视场
   3) 益害分类筐：六种微生物 → 有益 / 有害
   4) 综合任务勾选：哪些事情离不开微生物
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

  /* ---------- 2. 显微镜观察台 ---------- */
  var mic = document.getElementById('mic-canvas');
  if (mic) {
    var mctx = mic.getContext('2d');
    var zoomEl = document.getElementById('mic-zoom');
    var toolEl = document.getElementById('mic-tool');
    var timesEl = document.getElementById('mic-times');
    var countEl = document.getElementById('mic-count');
    var outEl = document.getElementById('mic-out');
    var canBlur = ('filter' in mctx);

    function setBlur(px) {
      if (canBlur) mctx.filter = px > 0.05 ? 'blur(' + px.toFixed(2) + 'px)' : 'none';
    }
    function text(str, x, y, size, color, align) {
      mctx.fillStyle = color || '#3a3126';
      mctx.font = '700 ' + (size || 17) + 'px "PingFang SC", "Microsoft YaHei", sans-serif';
      mctx.textAlign = align || 'left';
      mctx.fillText(str, x, y);
      mctx.textAlign = 'left';
    }
    function circle(x, y, r) { mctx.beginPath(); mctx.arc(x, y, r, 0, Math.PI * 2); }

    function drawField() {
      var W = mic.width, H = mic.height;
      mctx.setTransform(1, 0, 0, 1, 0, 0);
      mctx.filter = 'none';
      mctx.clearRect(0, 0, W, H);
      var g = mctx.createRadialGradient(W / 2, H / 2, 12, W / 2, H / 2, Math.max(W, H) / 1.35);
      g.addColorStop(0, '#fdfefe');
      g.addColorStop(1, '#d8e8f4');
      mctx.fillStyle = g;
      mctx.fillRect(0, 0, W, H);
      mctx.strokeStyle = 'rgba(120,160,190,.35)';
      mctx.lineWidth = 2;
      mctx.beginPath();
      mctx.moveTo(W / 2, 18); mctx.lineTo(W / 2, H - 18);
      mctx.moveTo(18, H / 2); mctx.lineTo(W - 18, H / 2);
      mctx.stroke();
    }

    function stageOf(v) { return v < 34 ? 0 : (v < 67 ? 1 : 2); }

    function drawNaked() {
      setBlur(7);
      mctx.fillStyle = '#e8d3a8';
      mctx.beginPath();
      mctx.moveTo(150, 300); mctx.lineTo(210, 110); mctx.lineTo(520, 110); mctx.lineTo(580, 300);
      mctx.closePath();
      mctx.fill();
      setBlur(9);
      mctx.fillStyle = 'rgba(120,150,110,.75)';
      circle(360, 190, 46); mctx.fill();
      setBlur(0);
      text('肉眼看到的样子：只有一小片模模糊糊的痕迹', 360, 350, 18, '#5c5142', 'center');
    }

    function drawMag() {
      setBlur(1.4);
      mctx.strokeStyle = 'rgba(96,140,96,.85)';
      mctx.lineWidth = 3;
      for (var i = 0; i < 26; i++) {
        mctx.beginPath();
        mctx.moveTo(360, 200);
        var a = (Math.PI * 2 / 26) * i + 0.2;
        mctx.quadraticCurveTo(360 + Math.cos(a) * 70, 200 + Math.sin(a) * 70,
                              360 + Math.cos(a + 0.25) * 135, 200 + Math.sin(a + 0.25) * 135);
        mctx.stroke();
      }
      setBlur(0);
      text('放大镜（约 10 倍）：看清霉菌一丝一丝的菌丝', 360, 350, 18, '#37603a', 'center');
    }

    function drawScope() {
      // 球菌
      var pts = [[130, 110], [166, 96], [186, 132], [150, 150], [118, 142]];
      mctx.fillStyle = '#ff8f8f';
      pts.forEach(function (p) { circle(p[0], p[1], 19); mctx.fill(); });
      mctx.strokeStyle = 'rgba(200,60,60,.55)'; mctx.lineWidth = 2;
      pts.forEach(function (p) { circle(p[0], p[1], 19); mctx.stroke(); });
      text('球菌', 150, 192, 17, '#b03a3a', 'center');

      // 杆菌
      mctx.fillStyle = '#7fc8f8';
      [[380, 90, 74, 26], [470, 132, 62, 24], [340, 152, 56, 22]].forEach(function (r) {
        mctx.beginPath();
        mctx.roundRect ? mctx.roundRect(r[0], r[1], r[2], r[3], 12)
                       : mctx.rect(r[0], r[1], r[2], r[3]);
        mctx.fill();
      });
      text('杆菌', 420, 200, 17, '#2b6f9e', 'center');

      // 螺旋菌
      mctx.strokeStyle = '#b07d12';
      mctx.lineWidth = 7;
      mctx.beginPath();
      for (var t = 0; t <= 40; t++) {
        var x = 600 + Math.sin(t / 3) * 16;
        var y = 80 + t * 2.2;
        if (t === 0) mctx.moveTo(x, y); else mctx.lineTo(x, y);
      }
      mctx.stroke();
      text('螺旋菌', 610, 200, 17, '#8a6410', 'center');

      // 酵母菌
      mctx.fillStyle = '#ffd166';
      circle(170, 290, 40); mctx.fill();
      mctx.strokeStyle = 'rgba(190,140,20,.7)'; mctx.lineWidth = 2;
      circle(170, 290, 40); mctx.stroke();
      circle(214, 262, 20); mctx.fill(); circle(214, 262, 20); mctx.stroke();
      text('酵母菌', 175, 348, 17, '#8a6410', 'center');

      // 霉菌孢子
      mctx.fillStyle = '#9ad3a0';
      for (var k = 0; k < 6; k++) { circle(500 + k * 26, 290 + (k % 2) * 14, 13); mctx.fill(); }
      text('霉菌的孢子', 560, 348, 17, '#37603a', 'center');
    }

    function renderMic() {
      var v = parseInt(zoomEl.value, 10) || 0;
      var st = stageOf(v);
      drawField();
      if (st === 0) {
        drawNaked();
        toolEl.textContent = '肉眼';
        timesEl.textContent = '1 倍';
        countEl.textContent = '0 种';
        outEl.className = 'result warn';
        outEl.innerHTML = '<strong>肉眼看不到微生物。</strong>你只能看到一小片模糊的痕迹。想知道它到底是什么，就要换工具了——把倍数调大试试。';
      } else if (st === 1) {
        drawMag();
        toolEl.textContent = '放大镜';
        timesEl.textContent = '10 倍';
        countEl.textContent = '1 种';
        outEl.className = 'result warn';
        outEl.innerHTML = '<strong>用放大镜，能看见霉菌一丝一丝的菌丝了。</strong>可再小的细菌，放大镜还是看不清，还得把倍数继续调大。';
      } else {
        drawScope();
        toolEl.textContent = '显微镜';
        timesEl.textContent = '400 倍';
        countEl.textContent = '5 种';
        outEl.className = 'result';
        outEl.innerHTML = '<strong>换成显微镜，球菌、杆菌、螺旋菌、酵母菌、霉菌的孢子都出现了。</strong>微生物个体微小，必须借助显微镜才能看清它们的模样。';
      }
    }
    zoomEl.addEventListener('input', renderMic);
    renderMic();
  }

  /* ---------- 3. 益害分类筐 ---------- */
  var bank = document.getElementById('sort-bank');
  if (bank) {
    var picked = null;
    var done = 0, wrongCount = 0;
    var msg = document.getElementById('sort-msg');
    var total = bank.querySelectorAll('.sort-item').length;

    bank.querySelectorAll('.sort-item').forEach(function (card) {
      card.addEventListener('click', function () {
        if (card.classList.contains('done')) return;
        bank.querySelectorAll('.sort-item').forEach(function (c) { c.style.outline = 'none'; });
        card.style.outline = '3px solid var(--brand)';
        picked = card;
        msg.className = 'result warn';
        msg.textContent = '已选中「' + card.textContent.trim() + '」，现在点左边或右边的筐把它归类。';
      });
    });

    document.querySelectorAll('[data-sort-bin]').forEach(function (bin) {
      bin.addEventListener('click', function () {
        if (!picked) { msg.className = 'result warn'; msg.textContent = '先点一张微生物卡片，再点筐。'; return; }
        var want = picked.dataset.kind, got = bin.dataset.sortBin;
        var name = picked.textContent.trim();
        picked.style.outline = 'none';
        if (want === got) {
          var tag = document.createElement('span');
          tag.className = 'tag';
          tag.textContent = name + ' ✓';
          tag.style.borderColor = 'rgba(78,205,196,.8)';
          tag.style.background = 'rgba(78,205,196,.14)';
          bin.querySelector('.bin-body').appendChild(tag);
          picked.classList.add('done');
          done++;
          msg.className = 'result';
          msg.innerHTML = '<strong>放对了！</strong>' + picked.dataset.why;
          picked = null;
          if (done === total) {
            msg.className = 'result';
            msg.innerHTML = '<strong>六张卡片全部分类完成，错误 ' + wrongCount + ' 次。</strong>你会发现，微生物里既有帮我们的，也有害我们的，不能一句话说死。';
          }
        } else {
          wrongCount++;
          msg.className = 'result error';
          msg.innerHTML = '<strong>再想一下：</strong>' + name + ' 出现在哪里？它做的事情是帮了我们，还是给我们添了麻烦？';
          picked.style.outline = '3px dashed rgba(239,68,68,.7)';
        }
      });
    });
  }

  /* ---------- 4. 综合任务勾选 ---------- */
  var pickList = document.getElementById('syn-picks');
  if (pickList) {
    var out = document.getElementById('syn-out');
    var RIGHT = ['面包', '酸奶', '落叶变成肥料'];
    pickList.querySelectorAll('[data-syn-pick]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        btn.classList.toggle('selected');
        var chosen = [];
        pickList.querySelectorAll('[data-syn-pick]').forEach(function (b) {
          if (b.classList.contains('selected')) chosen.push(b.dataset.synPick);
        });
        var hits = chosen.filter(function (c) { return RIGHT.indexOf(c) >= 0; });
        var allRight = chosen.length === RIGHT.length && hits.length === RIGHT.length;
        out.className = 'result ' + (allRight ? '' : 'warn');
        if (allRight) {
          out.innerHTML = '<strong>全对！</strong>面包要发酵、酸奶要乳酸菌、落叶变成肥料要靠分解者，这三件事都离不开微生物。剩下两件（把水烧开、把水果放进冰箱）靠的是高温和低温，和微生物本身没有关系。';
        } else {
          out.innerHTML = '你选了 <strong>' + chosen.length + '</strong> 件事，其中 <strong>' + hits.length + '</strong> 件确实离不开微生物。再想一想：烧开水和放进冰箱，是用温度和低温让食物不容易坏，它们本身用到微生物了吗？';
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你见过看不见的邻居吗？", TTS["pretest"], [
        {"q": "想看清一个细菌的模样，最合适的工具是：",
         "options": [("显微镜", True), ("放大镜", False), ("望远镜", False)],
         "explain": "细菌太小了，放大镜也看不清，要用显微镜。<strong>错因提醒：</strong>把放大镜和显微镜搞混是这一课最常见的错误——放大镜只能看到霉菌菌丝这个级别。"},
        {"q": "下面哪一组全都是微生物？",
         "options": [("细菌、真菌、病毒", True), ("蚂蚁、蝴蝶、蜘蛛", False), ("石头、水、空气", False)],
         "explain": "细菌、真菌、病毒是常见的三类微生物。<strong>错因提醒：</strong>常见错误是把昆虫当成微生物，因为昆虫也很小——但用眼睛就能看见的，不是微生物。"},
        {"q": "馒头蒸熟后变得又软又大，主要靠的是：",
         "options": [("酵母菌在面团里放出小气泡", True), ("面粉自己会膨胀", False), ("蒸的时候水变成了气", False)],
         "explain": "发面靠的是酵母菌，它是真菌，属于微生物。这一题先记在心里，等下我们还会讲一遍。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "微生物小到看不见，必须用显微镜才能看清", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">你已经知道生活中有花草树木、有猫狗昆虫，它们都能用眼睛看见。<strong>但</strong>还有一整群生物，小到肉眼根本看不见，它们就是<strong>微生物</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>特点一：小</strong></p>
            <p style="color:var(--muted)">一滴水里可以住着几百万个细菌，要用显微镜放大几百倍才看得清。</p>
          </div>
          <div class="inner-card">
            <p><strong>特点二：多</strong></p>
            <p style="color:var(--muted)">土壤、水、空气、皮肤上都有它们，几乎无处不在。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="微生物的大小对比与三类微生物示意图">
          <figcaption>肉眼、放大镜、显微镜看到的差别：微生物的个体太小，只有显微镜才能看清它们的形态</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔬</span><div><strong>记住三类名字：</strong>细菌、真菌、病毒。霉菌和酵母菌是<strong>真菌</strong>，感冒病毒是<strong>病毒</strong>，我们手上最多的是<strong>细菌</strong>。</div></div>
{insight_box([
    {"lens": "解释它", "text": "为什么看不见？因为它们的个体只有几微米，比我们的头发丝还细得多，光线照上去也分辨不出来。"},
    {"lens": "比较它", "text": "霉菌长在馒头上的绿毛，肉眼刚好能看到一点，那是很多菌丝聚在一起；单个细菌比它小上千倍。"},
    {"lens": "迁移它", "text": "所以医院做检查、厨房检验食物，都要采样送到显微镜下看——看不见的东西，要靠工具把它放大。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "显微镜观察台：把倍数一点点调大", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">拖动下面的滑块，从肉眼换到放大镜，再换到显微镜，看看画面里的微生物有什么变化。</p>
        <div class="lab-panel">
          <div class="canvas-wrap" style="padding:10px">
            <canvas id="mic-canvas" width="720" height="380" style="width:100%;display:block;border-radius:14px"></canvas>
          </div>
          <div class="slider-row">
            <label for="mic-zoom">放大倍数</label>
            <input type="range" id="mic-zoom" min="0" max="100" value="0" step="1">
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">现在用什么看</span><span class="v" id="mic-tool">肉眼</span></div>
            <div class="readout-cell"><span class="k">放大倍数</span><span class="v" id="mic-times">1 倍</span></div>
            <div class="readout-cell"><span class="k">能看清的微生物</span><span class="v green" id="mic-count">0 种</span></div>
          </div>
          <p class="result warn" id="mic-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧫</span><div><strong>动手之后再想一句：</strong>如果一开始就用肉眼看，你能发现馒头上的细菌吗？这就是科学家一定要用显微镜的原因。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "微生物有的帮我们，有的害我们，不能一句说死", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">说到微生物，很多同学第一反应是"脏"和"生病"。<strong>但</strong>我们每天吃的馒头、酸奶，都离不开它们。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>👍 帮我们的</strong></p>
            <p style="color:var(--muted)">酵母菌发面、乳酸菌做酸奶和泡菜、土壤里的细菌分解落叶和垃圾，还能净化污水。</p>
          </div>
          <div class="inner-card">
            <p><strong>⚠️ 添麻烦的</strong></p>
            <p style="color:var(--muted)">霉菌让食物发霉变质，致病的大肠杆菌和感冒病毒会让人生病。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="有益微生物与有害微生物的用途对比示意图">
          <figcaption>同样的微生物世界，一边在帮我们做食物、分解垃圾，一边在让食物变质、让人生病</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不能<strong>误认为</strong>细菌全都是坏的。我们的肠道里就住着大量帮我们消化食物的细菌；也不能<strong>误认为</strong>食物只要放进冰箱就永远安全——低温只是让微生物长得慢，不是把它们全部消灭。</p>
        </div>
    ''', tag="概念二"))

    items_html = "\n".join(
        f'          <button class="sort-item" data-kind="{it["kind"]}" data-why="{it["why"]}">{it["t"]}</button>'
        for it in SORT_ITEMS
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "益害分类筐：六种微生物，放进两个筐", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点一张卡片，再点你认为正确的筐。每放一次都会立刻告诉你理由。</p>
        <div class="lab-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">待分类的微生物</div>
          <div class="sort-bank" id="sort-bank">
{items_html}
          </div>
          <div class="sort-bins">
            <div class="sort-bin" data-sort-bin="good">
              <h4>👍 对我们有益</h4>
              <div class="bin-body"></div>
            </div>
            <div class="sort-bin" data-sort-bin="bad">
              <h4>⚠️ 对我们有害</h4>
              <div class="bin-body"></div>
            </div>
          </div>
          <p class="result warn" id="sort-msg" style="margin-top:12px">点一张卡片开始分类。</p>
        </div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：馒头为什么能变得又软又大", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>妈妈和面时往面粉里加了一小包酵母。几个小时后，面团鼓成了两倍大，蒸出来的馒头又软又香。这是谁在帮忙？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>找出帮忙的"人"：</strong>是酵母，也就是酵母菌。</div></div>
          <div class="step"><span class="n">2</span><div><strong>判断它属于哪一类：</strong>酵母菌是真菌，属于微生物这一大类。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说清它做了什么：</strong>它在面团里生长繁殖，放出许多小气泡，把面团一点点撑大。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>得出结论：</strong>馒头变大是酵母菌这种微生物帮的忙，微生物对人也有用处。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🍞</span><div><strong>换个问法也一样：</strong>把"馒头"换成"酸奶""泡菜""面包"，答案里的主角换成乳酸菌，道理完全一样。</div></div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：这三个说法错在哪里", TTS["conceptest-1"], [
        {"q": "下面哪个说法是正确的？",
         "options": [("有的微生物对我们有益，有的对我们有害", True),
                     ("微生物全都是坏东西", False),
                     ("肉眼看不见的东西都不算生物", False)],
         "explain": "酵母菌、乳酸菌帮我们做食物，霉菌、致病菌让人生病。<strong>错因提醒：</strong>最常见错误是误认为微生物都是坏的，其实是把看不见和有害这两件事搞混了。"},
        {"q": "食物放进冰箱不容易坏，主要是因为：",
         "options": [("低温让微生物长得慢，食物保存得更久", True),
                     ("冰箱把微生物全部杀死了", False),
                     ("冰箱里没有空气，微生物活不了", False)],
         "explain": "低温只是减慢微生物的繁殖速度，并没有把它们全部消灭。<strong>错因提醒：</strong>误认为冰箱能杀菌是高频错误，所以冰箱里的食物放久了照样会坏。"},
        {"q": "关于细菌，下面哪句话最准确？",
         "options": [("细菌既可能让我们生病，也可能帮我们消化食物", True),
                     ("细菌会让所有食物变质", False),
                     ("细菌比霉菌大很多，肉眼能看到", False)],
         "explain": "细菌的种类很多，作用也不一样。<strong>错因提醒：</strong>把细菌和霉菌搞混、以为细菌肉眼能看见，也是常见的错误——它们都要用显微镜才能看清。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：酸奶能喝，长绿毛的面包不能吃", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面五件事，哪些真的离不开微生物？点一点，选出来，再写出你的比较理由。</p>
        <div class="lab-panel">
          <div id="syn-picks" class="sort-bank">
            <button class="sort-item" data-syn-pick="面包">🍞 面包能发起来</button>
            <button class="sort-item" data-syn-pick="酸奶">🥛 牛奶变成酸奶</button>
            <button class="sort-item" data-syn-pick="落叶变成肥料">🍂 落叶变成肥料</button>
            <button class="sort-item" data-syn-pick="把水烧开">💧 把水烧开</button>
            <button class="sort-item" data-syn-pick="放进冰箱">🧊 把水果放进冰箱</button>
          </div>
          <p class="result warn" id="syn-out" style="margin-top:12px">先把你认为"离不开微生物"的事情都点出来。</p>
        </div>
        <div class="inner-card">
          <p><strong>比一比，再写下来：</strong></p>
          <p style="color:var(--muted)">同样放在桌上，酸奶为什么能喝，长了绿毛的面包为什么不能吃？请用"微生物、有益、有害"这三个词说清楚。</p>
          <textarea id="syn-answer" rows="3" placeholder="酸奶里的微生物……面包上的绿毛是……所以……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，你还能判断吗", TTS["posttest"], [
        {"q": "饭前要用肥皂认真洗手，主要原因是：",
         "options": [("手上带着肉眼看不见的细菌和病毒，洗掉它们不容易生病", True),
                     ("洗完手心情更好", False),
                     ("肥皂能把手上的脏东西变成新物质", False)],
         "explain": "病原微生物个体微小、肉眼看不见，洗手能把它们随水流冲走，是最简单的防病办法。"},
        {"q": "做酸奶需要往牛奶里加入：",
         "options": [("乳酸菌", True), ("感冒病毒", False), ("霉菌的孢子", False)],
         "explain": "乳酸菌在牛奶里生长，把牛奶变成酸奶，这是有益微生物的典型用途。"},
        {"q": "小明的妈妈说，打了疫苗就不容易得某些传染病。疫苗起作用时用到的道理是：",
         "options": [("让身体提前认识病原体，学会防备它", True),
                     ("把身体里所有微生物都消灭", False),
                     ("让人从此不再接触任何病毒", False)],
         "explain": "疫苗帮身体提前做好防备，而不是消灭身体里所有微生物——我们身体里本来就住着许多有益的微生物。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话记住看不见的邻居", TTS["summary"], f'''
        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>样子</strong>：微生物个体微小，要借助显微镜才能看清；常见的有细菌、真菌、病毒三类。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>住处</strong>：它们几乎无处不在，土壤、水、空气和我们身上都有。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>作用</strong>：有益的在帮我们发面、做酸奶、分解垃圾；有害的会让食物变质、让人生病。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那块馒头：</strong>发面时，酵母菌是我们请来的帮手；放久了长出的绿毛，是霉菌这个不请自来的客人。同样是小到看不见的居民，做的事情却完全不同——所以要看是哪一种，还要看它在做什么。</p>
        </div>
        <div class="inner-card">
          <p><strong>讲给同桌听：</strong>请用"微生物、显微镜、有益、有害"这四个词，说说为什么我们既怕细菌，又离不开细菌。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出微生物的两个特点，并说出常见微生物的三类名字。",
            "举出一个对我们有益的微生物和一个对我们有害的微生物，各写一句理由。",
        ],
        [
            "在家里找出三样和微生物有关的东西（例如酸奶、馒头、消毒湿巾），写清楚各用到了哪一种微生物，或者是在防备哪一类微生物。",
            "用一句话向家里人解释：为什么食物放进冰箱还是会坏？",
        ],
        [
            "设计一个小实验：把两块一样的面包分别放在潮湿和干燥的地方，每天记录一次变化，看看哪一块先长出霉斑，并说明为什么。",
            "查一查疫苗的作用，用三句话说明它和微生物之间的关系。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-microorganisms",
    "node_id": "sci-e-microorganisms",
    "title": "微生物：小到看不见的居民",
    "name_en": "Microorganisms: the invisible neighbours",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "life-science",
    "domain_cn": "生命科学 · 生物多样性",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "从肉眼、放大镜、显微镜三级视场出发认识微生物的微小特征，知道细菌、真菌、病毒是常见的三类微生物，并通过益害分类理解微生物对人类生活既可能有害也可能有益。",
    "tags": ["微生物", "细菌", "真菌", "病毒", "显微镜", "有益与有害"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念5「生命系统的构成层次」学习内容5.2 地球上存在动物、植物、微生物等不同类型的生物——知道地球上存在不同类群的生物，能举例说出微生物的存在与特征。",
    "hero_question": "它们小到看不见，却住在你的手上、空气里和馒头上——它们是谁？",
    "hero_alt": "微生物知识结构图：微生物有多小、常见的三类、有益的与有害的",
    "hero_caption": "微生物 · 个体微小要用显微镜 · 常见三类：细菌、真菌、病毒 · 有的有益有的有害",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的观察和分类都会围着它转。",
    "anchor_choices": [
        {"t": "微生物到底有多小？", "d": "想知道它和蚂蚁、灰尘比谁更小", "v": "微生物到底有多小"},
        {"t": "微生物长什么样，有哪几类？", "d": "想知道细菌、真菌、病毒的区别", "v": "微生物长什么样有哪几类"},
        {"t": "它们对我们到底有什么用？", "d": "想知道微生物是帮助我们还是害我们", "v": "微生物对我们到底有什么用"},
        {"t": "为什么食物会发霉、会变酸？", "d": "从厨房里的现象开始问", "v": "为什么食物会发霉会变酸"},
    ],
    "objectives": [
        "能说出微生物个体微小，需要借助显微镜才能看清",
        "能说出细菌、真菌、病毒是常见的三类微生物，并各举一例",
        "能举例说明有的微生物对人有益、有的对人有害",
        "能说出有益微生物在发面、做酸奶、分解垃圾等活动中的作用",
    ],
    "objectives_plain": [
        "能说出微生物个体微小，需要借助显微镜才能看清",
        "能说出细菌、真菌、病毒是常见的三类微生物，并各举一例",
        "能举例说明有的微生物对人有益、有的对人有害",
        "能说出有益微生物在发面、做酸奶、分解垃圾等活动中的作用",
    ],
    "standards": [
        {"content": "知道地球上存在动物、植物、微生物等不同类型的生物，能举例说出微生物的存在",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念5 生命系统的构成层次·学习内容5.2"},
        {"content": "能借助工具进行观察，用观察到的现象描述生物的特征",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》科学探究·观察与描述（3～4年级、5～6年级）"},
    ],
    "prereqs": ["sci-e-classification"],
    "prereqs_name": "生物的分类",
    "prereqs_meta": "sci-e-classification",
    "leads_to": ["sci-e-cell-unit"],
    "next_meta": "sci-e-cell-unit",
    "section_images": ["assets/sci-e-microorganisms-fig1.webp", "assets/sci-e-microorganisms-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "看不见的居民就住在你身上，先带着好奇开始这节课。",
        "problem-anchor": "先定一个小目标：这节课结束时，你要能说出微生物是多小、分几类、有什么用。",
        "objectives": "看清四件事：微生物有多小、有哪三类、有没有害、在生活里做什么。",
        "pretest": "凭直觉选就好，错了不扣分——前测帮你先看清自己现在站在哪里。",
        "module-1": "小和多，是微生物最要紧的两个特点；记住细菌、真菌、病毒三个名字。",
        "lab-1": "从肉眼到放大镜再到显微镜，每调大一档，画面就多出一些东西。",
        "module-2": "别急着说微生物都是坏的，做馒头、做酸奶、分解垃圾都要靠它们。",
        "lab-2": "放之前先想一句话：它出现在哪里，它做了什么？",
        "worked-example": "四步走：找出帮忙的、判断属于哪类、说清它做了什么、得出结论。",
        "conceptest-1": "这三道题都埋了高频错误，选完看清每一个解释。",
        "synthesis": "同样放在桌上，一个能喝一个不能吃，差别就在微生物做的事情上。",
        "posttest": "换了洗手、酸奶和疫苗的新情境，看看你还能不能判断准确。",
        "summary": "回到开头那块馒头：发起来靠酵母菌，长绿毛是霉菌，同样是微生物，做的事不一样。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「生命系统的构成层次」中长期空缺的一课。知识树原有生物分类、动植物特征，但没有任何一课处理课标明确要求学习的微生物。设计上把「小到看不见」变成可以亲手操作的体验——滑块从肉眼调到显微镜，画面里的微生物一级一级多起来；再把「微生物是好是坏」这个孩子最常见的二元判断，通过六张分类卡和馒头发面的例题，落成一句能带走的话：要看是哪一种，还要看它在做什么。",
    "plan_table": """| 1 | cover | 微生物：小到看不见的居民 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你见过看不见的邻居吗？ | 起·前测（暴露直觉） |
| 5 | concept | 微生物小到看不见，必须用显微镜才能看清 | 承·概念一（微小与三类） |
| 6 | interactive | 显微镜观察台：把倍数一点点调大 | 承·实验室一（三级视场） |
| 7 | concept | 微生物有的帮我们，有的害我们，不能一句说死 | 承·概念二（益与害） |
| 8 | interactive | 益害分类筐：六种微生物，放进两个筐 | 承·实验室二（即时反馈） |
| 9 | concept | 例题示范：馒头为什么能变得又软又大 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：这三个说法错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：酸奶能喝，长绿毛的面包不能吃 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，你还能判断吗 | 合·后测 |
| 13 | summary | 小结：三句话记住看不见的邻居 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：微生物有多小 / 常见三类 / 有益与有害 三栏标注\n- P5 大小与三类对比图（已生成）：肉眼—放大镜—显微镜的观察差别\n- P7 益害对比图（已生成）：酵母菌、乳酸菌、分解者 vs 霉菌、致病菌、病毒\n- 若需补充：霉菌菌落实拍照片、显微镜下细菌形态照片",
}
