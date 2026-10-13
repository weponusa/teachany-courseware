# -*- coding: utf-8 -*-
"""小学科学 · 细胞：生物体最小的生命单位（G6）—— 补齐课标「生命系统的构成层次·5.3 细胞」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-cell-unit-fig1.webp'
F2 = './assets/sci-e-cell-unit-fig2.webp'

TTS = {
    "hero": "我们一起看两样东西。一小片洋葱，薄得几乎透明；一只草履虫，小到只有一个点。它们看上去完全不一样，可它们身体里都藏着一个共同的秘密。如果把它们放在显微镜下，你会看到一个个小小的格子——那就是细胞。这节课我们就来认识它。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道我身上到底有多少个细胞，还是想知道一个细胞能不能自己活着，又或者你想弄清楚洋葱那么大，为什么也是细胞组成的。选好之后，带着问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出除病毒外，生物体都是由细胞构成的。第二，能说出细胞是生物体结构和生命活动的基本单位。第三，能在显微镜下认出细胞，并指认细胞壁、细胞膜和细胞核。第四，能比较单细胞生物和多细胞生物，说出细胞、组织、器官之间的层次关系。",
    "pretest": "先做三道小题，用你现在的想法选就好。选完马上能看到解释，选错了也没关系，正好知道要重点听哪里。",
    "module-1": "我们已经认识了动物、植物和微生物，它们的样子差别很大。可是科学家发现，它们有一个共同的秘密：除了病毒以外，所有生物的身体，都是由细胞构成的。细胞非常小，要用显微镜才能看清。它外面包着一层细胞膜，里面有细胞质，中间还有一个细胞核。植物细胞在细胞膜外面，还多了一层比较硬的细胞壁。细胞是生物体结构的基本单位，也是生命活动的基本单位。",
    "lab-1": "现在请你亲手调一次显微镜的焦距。画面一开始是模糊的，你要慢慢转动滑块，让细胞的轮廓一点点变清楚。调到最清楚的时候，你会看到一个个长方形的格子紧紧排在一起，每个格子里都有一个细胞核。",
    "module-2": "生物可以分成两类。有的生物全身只有一个细胞，比如草履虫、变形虫和酵母菌，就叫单细胞生物。别看它只有一个细胞，运动、吃东西、呼吸、繁殖，全由这一个细胞包办。还有的生物由许许多多细胞组成，比如人、大树和猫，叫多细胞生物。多细胞生物的细胞会分工合作，先形成组织，再形成器官，人和动物还会形成系统，最后才是一个完整的个体。",
    "lab-2": "下面我们来比一比单细胞生物和多细胞生物。点一点按钮，看看草履虫和人的身体，在细胞数目和结构层次上有什么不一样。",
    "worked-example": "我们一起分析一道题：洋葱和草履虫都是生物，它们的身体在细胞上有什么相同和不同？第一步，看清条件，洋葱由许多细胞组成，草履虫只有一整个细胞。第二步，找出共同点，它们都由细胞构成，都有细胞膜、细胞质和细胞核。第三步，找出不同点，草履虫的一个细胞就要完成全部生命活动，洋葱的许多细胞会分工，形成组织，再形成器官。第四步，得出结论，细胞是生物体结构和生命活动的基本单位，细胞数目不一样，基本单位却是同一个。",
    "conceptest-1": "下面有三道容易弄错的说法，请你仔细读每一个选项，选完再看解释，看看自己有没有掉进那几个常见的坑里。",
    "synthesis": "最后一件事交给你。请你给草履虫、洋葱和人各填一张细胞身份证：它到底是一个细胞，还是许多细胞？填完以后，再用三句话写下你在显微镜下看到的洋葱表皮细胞是什么样子的。",
    "posttest": "最后一轮，用新的情境检验一下。这里有伤口愈合、大树长高和病毒，看看你能不能把学到的知识用上去。",
    "summary": "这节课我们找到了生物身上共同的秘密。除病毒外，生物体都是由细胞构成的；细胞是生物体结构和生命活动的基本单位。细胞很小，要用显微镜才能看清，它外面是细胞膜，里面有细胞质和细胞核，植物细胞外面还有一层细胞壁。有的生物只有一个细胞，叫做单细胞生物；有的生物由许多细胞组成，细胞分工以后形成组织、器官，甚至形成系统。回到开头那片薄薄的洋葱，它看起来和草履虫完全不同，可它们都是由细胞一个个搭起来的。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出细胞是生物体什么的基本单位，并说出细胞膜、细胞质、细胞核这三个结构。第二层能力应用，动手做：用橡皮泥或者彩纸做一个细胞模型，把细胞膜、细胞质、细胞核标出来，再讲给家里人听。第三层迁移挑战，选做：找一段洋葱表皮或者一片叶子，画出你看到的细胞排列，并说明它们为什么要紧紧排在一起。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 生物体都由细胞构成", "lab-1": "实验室一 洋葱表皮细胞", "module-2": "概念二 单细胞与多细胞",
    "lab-2": "实验室二 草履虫与人", "worked-example": "例题讲解 洋葱和草履虫", "conceptest-1": "概念测试",
    "synthesis": "综合任务 细胞身份证", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

ID_CARDS = [
    {"key": "paramecium", "name": "草履虫", "correct": "single",
     "why": "草履虫全身只有一个细胞，运动、吃东西、呼吸都靠这一个细胞完成，是单细胞生物。"},
    {"key": "yeast", "name": "酵母菌", "correct": "single",
     "why": "酵母菌也是单细胞生物。上节课做馒头用到的酵母菌，就是一个一个独立的细胞。"},
    {"key": "onion", "name": "洋葱", "correct": "multi",
     "why": "洋葱的细胞会分工，形成组织，再形成器官，是一株多细胞生物。"},
    {"key": "human", "name": "人", "correct": "multi",
     "why": "人体由几十万亿个细胞组成，细胞分工后形成组织、器官和系统，是多细胞生物。"},
]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-cell-unit 互动逻辑
   1) 选择题接线
   2) 洋葱表皮细胞：调焦滑块 → 模糊到清晰（清晰后显示结构图例）
   3) 单细胞 vs 多细胞：草履虫 / 人 切换对比
   4) 细胞身份证：四个生物判定单细胞 / 多细胞
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

  /* ---------- 2. 洋葱表皮细胞调焦 ---------- */
  var oc = document.getElementById('cell-canvas');
  if (oc) {
    var cctx = oc.getContext('2d');
    var focusEl = document.getElementById('cell-focus');
    var clarEl = document.getElementById('cell-clarity');
    var outEl = document.getElementById('cell-out');
    var canBlur = ('filter' in cctx);
    var IDEAL = 70;
    var CELLS = [];
    (function () {
      var ys = [30, 138, 246], xs = [40, 205, 370, 535];
      ys.forEach(function (y, r) {
        xs.forEach(function (x, c) {
          CELLS.push([x, y, 150, 88, r, c]);
        });
      });
    })();

    function blurOf(v) { return Math.abs(v - IDEAL) / 9; }

    function drawCells(blur, clarity) {
      var W = oc.width, H = oc.height;
      cctx.setTransform(1, 0, 0, 1, 0, 0);
      cctx.filter = 'none';
      cctx.clearRect(0, 0, W, H);
      cctx.fillStyle = '#eef7ff';
      cctx.fillRect(0, 0, W, H);
      if (canBlur) cctx.filter = blur > 0.06 ? 'blur(' + blur.toFixed(2) + 'px)' : 'none';

      CELLS.forEach(function (c) {
        var x = c[0], y = c[1], w = c[2], h = c[3];
        cctx.fillStyle = '#f6fdf2';
        cctx.beginPath();
        cctx.rect(x, y, w, h);
        cctx.fill();
        cctx.strokeStyle = '#8fbf72';
        cctx.lineWidth = 6;
        cctx.stroke();
        cctx.strokeStyle = 'rgba(110,170,200,.75)';
        cctx.lineWidth = 1.6;
        cctx.strokeRect(x + 6, y + 6, w - 12, h - 12);
        cctx.fillStyle = 'rgba(160,205,240,.45)';
        cctx.beginPath();
        cctx.ellipse(x + w * 0.68, y + h * 0.62, w * 0.2, h * 0.26, 0, 0, Math.PI * 2);
        cctx.fill();
        cctx.fillStyle = '#b98fd6';
        cctx.beginPath();
        cctx.ellipse(x + w * 0.36, y + h * 0.42, 18, 14, 0, 0, Math.PI * 2);
        cctx.fill();
      });

      cctx.filter = 'none';
      if (clarity >= 88) {
        cctx.fillStyle = 'rgba(255,255,255,.94)';
        cctx.fillRect(16, 344, W - 32, 62);
        cctx.strokeStyle = 'rgba(143,191,114,.9)';
        cctx.lineWidth = 1.5;
        cctx.strokeRect(16, 344, W - 32, 62);
        cctx.font = '700 16px "PingFang SC", "Microsoft YaHei", sans-serif';
        cctx.fillStyle = '#3a3126';
        cctx.fillText('● 细胞壁：最外圈的粗厚边缘　● 细胞膜：紧贴在壁内侧的细线', 32, 370);
        cctx.fillText('● 细胞核：每个细胞中间深紫色的椭圆　● 细胞质：细胞里浅色的部分', 32, 394);
      } else {
        cctx.font = '700 18px "PingFang SC", "Microsoft YaHei", sans-serif';
        cctx.fillStyle = 'rgba(90,110,130,.85)';
        cctx.fillText('画面还看不清，继续慢慢转动焦距', 360, 392);
        cctx.textAlign = 'center';
        cctx.fillText('画面还看不清，继续慢慢转动焦距', 360, 392);
        cctx.textAlign = 'left';
      }
    }

    function renderCell() {
      var v = parseInt(focusEl.value, 10) || 0;
      var blur = blurOf(v);
      var clarity = Math.max(0, Math.round(100 - blur * 13));
      drawCells(blur, clarity);
      clarEl.textContent = clarity + ' %';
      if (clarity >= 88) {
        outEl.className = 'result';
        outEl.innerHTML = '<strong>看得清楚了！</strong>洋葱表皮细胞是一个个长方形的格子，紧紧地排在一起，每个格子里都有一个细胞核。外面的粗边是细胞壁，紧贴着它内侧的细线是细胞膜。';
      } else if (clarity >= 60) {
        outEl.className = 'result warn';
        outEl.innerHTML = '<strong>有点清楚了，再微调一点点。</strong>显微镜调焦要慢慢来，转到刚刚好的位置，轮廓才会最清楚。';
      } else {
        outEl.className = 'result warn';
        outEl.innerHTML = '<strong>还是很模糊。</strong>现在只看得到一团颜色，还分不出细胞的边界。把滑块继续往合适的位置转。';
      }
    }
    focusEl.addEventListener('input', renderCell);
    renderCell();
  }

  /* ---------- 3. 草履虫 vs 人 ---------- */
  var cmp = document.getElementById('cmp-canvas');
  if (cmp) {
    var xctx = cmp.getContext('2d');
    var CMP = {
      paramecium: {
        cells: '只有 1 个', level: '细胞（没有组织、器官）', type: '单细胞生物',
        msg: '草履虫全身就只有一个细胞，可它照样能游动、吃东西、呼吸、繁殖——一个细胞就包办了全部生命活动。眼虫、变形虫、酵母菌也是单细胞生物。'
      },
      human: {
        cells: '大约几十万亿个', level: '细胞 → 组织 → 器官 → 系统 → 人体', type: '多细胞生物',
        msg: '人体由许多细胞组成，细胞还会分工：肌肉细胞管运动，神经细胞传递信号，红细胞运送氧气。细胞分工以后形成组织、器官和系统，才能完成复杂的生命活动。'
      }
    };
    var cur = 'paramecium';
    var cellsEl = document.getElementById('cmp-cells');
    var levelEl = document.getElementById('cmp-level');
    var typeEl = document.getElementById('cmp-type');
    var cout = document.getElementById('cmp-out');

    function label(str, x, y, size, color, align) {
      xctx.fillStyle = color || '#3a3126';
      xctx.font = '700 ' + (size || 16) + 'px "PingFang SC", "Microsoft YaHei", sans-serif';
      xctx.textAlign = align || 'center';
      xctx.fillText(str, x, y);
      xctx.textAlign = 'left';
    }

    function drawParamecium() {
      var W = cmp.width, H = cmp.height;
      xctx.setTransform(1, 0, 0, 1, 0, 0);
      xctx.clearRect(0, 0, W, H);
      xctx.fillStyle = '#f7fbff';
      xctx.fillRect(0, 0, W, H);
      xctx.beginPath();
      xctx.ellipse(300, 150, 140, 72, -0.18, 0, Math.PI * 2);
      xctx.fillStyle = '#cdeab7';
      xctx.fill();
      xctx.strokeStyle = '#6fa64d';
      xctx.lineWidth = 3;
      xctx.stroke();
      xctx.strokeStyle = '#6fa64d';
      xctx.lineWidth = 1.6;
      for (var i = 0; i < 46; i++) {
        var a = (Math.PI * 2 / 46) * i;
        var bx = 300 + Math.cos(a) * 140, by = 150 + Math.sin(a) * 72;
        xctx.beginPath();
        xctx.moveTo(bx, by);
        xctx.lineTo(bx + Math.cos(a) * 12, by + Math.sin(a) * 10);
        xctx.stroke();
      }
      xctx.fillStyle = '#b98fd6';
      xctx.beginPath();
      xctx.ellipse(300, 150, 26, 20, 0, 0, Math.PI * 2);
      xctx.fill();
      xctx.fillStyle = 'rgba(160,205,240,.6)';
      xctx.beginPath();
      xctx.ellipse(255, 132, 22, 14, 0, 0, Math.PI * 2);
      xctx.fill();
      label('草履虫', 300, 262, 18, '#3a3126');
      label('整个身体 = 1 个细胞（细胞核·细胞质·细胞膜）', 300, 292, 15, '#5c5142');
      label('靠身上的纤毛摆动前进', 300, 60, 15, '#5c5142');
    }

    function drawHuman() {
      var W = cmp.width, H = cmp.height;
      xctx.setTransform(1, 0, 0, 1, 0, 0);
      xctx.clearRect(0, 0, W, H);
      xctx.fillStyle = '#f7fbff';
      xctx.fillRect(0, 0, W, H);
      // 中性简笔人形
      xctx.strokeStyle = '#7fa8c9';
      xctx.lineWidth = 4;
      xctx.beginPath(); xctx.arc(120, 74, 26, 0, Math.PI * 2); xctx.stroke();
      xctx.beginPath();
      xctx.moveTo(120, 100); xctx.lineTo(120, 208);
      xctx.moveTo(120, 128); xctx.lineTo(76, 168);
      xctx.moveTo(120, 128); xctx.lineTo(164, 168);
      xctx.moveTo(120, 208); xctx.lineTo(92, 262);
      xctx.moveTo(120, 208); xctx.lineTo(148, 262);
      xctx.stroke();
      label('一个完整的人体', 120, 296, 15, '#5c5142');
      // 层次链
      var items = ['细胞', '组织', '器官', '系统', '人体'];
      var x0 = 260, gap = 88;
      items.forEach(function (t, i) {
        var x = x0 + i * gap;
        xctx.fillStyle = i === 4 ? '#ffd166' : '#ffffff';
        xctx.strokeStyle = i === 4 ? '#d9a41f' : '#b9d3e6';
        xctx.lineWidth = 2.5;
        xctx.beginPath();
        xctx.roundRect ? xctx.roundRect(x, 120, 74, 52, 12) : xctx.rect(x, 120, 74, 52);
        xctx.fill();
        xctx.stroke();
        label(t, x + 37, 152, 16, '#3a3126');
        if (i < 4) {
          xctx.strokeStyle = '#b9d3e6';
          xctx.lineWidth = 3;
          xctx.beginPath();
          xctx.moveTo(x + 76, 146); xctx.lineTo(x + gap - 4, 146);
          xctx.stroke();
          xctx.beginPath();
          xctx.moveTo(x + gap - 12, 139); xctx.lineTo(x + gap - 2, 146); xctx.lineTo(x + gap - 12, 153);
          xctx.stroke();
        }
      });
      label('细胞一点点分工，最后组成一个完整的人', 480, 216, 16, '#5c5142');
      label('人体里有几十万亿个细胞', 480, 250, 16, '#5c5142');
    }

    function drawCmp() {
      if (cur === 'paramecium') drawParamecium(); else drawHuman();
      var d = CMP[cur];
      cellsEl.textContent = d.cells;
      levelEl.textContent = d.level;
      typeEl.textContent = d.type;
      cout.className = 'result';
      cout.innerHTML = '<strong>' + d.type + '</strong>：' + d.msg;
      document.querySelectorAll('[data-cmp]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.cmp === cur);
      });
    }
    document.querySelectorAll('[data-cmp]').forEach(function (b) {
      b.addEventListener('click', function () { cur = b.dataset.cmp; drawCmp(); });
    });
    drawCmp();
  }

  /* ---------- 4. 细胞身份证 ---------- */
  var idWrap = document.getElementById('id-cards');
  if (idWrap) {
    idWrap.querySelectorAll('[data-idrow]').forEach(function (row) {
      var out = row.querySelector('[data-idout]');
      row.querySelectorAll('[data-idpick]').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (row.dataset.done === '1') return;
          row.dataset.done = '1';
          var ok = btn.dataset.idpick === row.dataset.correct;
          btn.classList.add(ok ? 'correct' : 'wrong');
          row.querySelectorAll('[data-idpick]').forEach(function (b) {
            if (b.dataset.idpick === row.dataset.correct) b.classList.add('correct');
            b.disabled = true;
          });
          out.style.display = 'block';
          out.className = 'result' + (ok ? '' : ' warn');
          out.innerHTML = (ok ? '<strong>填对了！</strong>' : '<strong>再想一下：</strong>这一个生物的身体，是由一个细胞构成的，还是由许多细胞构成的？<br>')
            + row.dataset.why;
        });
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

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：你身体里有什么？", TTS["pretest"], [
        {"q": "一片薄薄的洋葱表皮，放在显微镜下会看到什么？",
         "options": [("一个个小格子紧紧排在一起", True), ("一团均匀的颜色", False), ("一些细小的虫子", False)],
         "explain": "那些小格子就是细胞。洋葱表皮由许多个细胞拼成，所以看起来像一格一格的。<strong>错因提醒：</strong>常见错误是误认为生物内部是均匀的一整块，其实它们都是一个个细胞搭起来的。"},
        {"q": "关于细胞，下面哪句话是对的？",
         "options": [("细胞是生物体结构和生命活动的基本单位", True),
                     ("细胞只在动物身体里才有", False),
                     ("细胞用肉眼就能看得很清楚", False)],
         "explain": "除病毒外，生物体都由细胞构成，细胞是生物体结构和生命活动的基本单位。<strong>错因提醒：</strong>把细胞和病毒搞混、以为细胞肉眼可见，是这一课的高频错误。"},
        {"q": "草履虫和猫相比，最大的不同是：",
         "options": [("草履虫只有一个细胞，猫由许多细胞组成", True),
                     ("草履虫不是生物", False),
                     ("猫的身体里没有细胞", False)],
         "explain": "草履虫是单细胞生物，一个细胞就完成全部生命活动；猫是多细胞生物，细胞还会分工。这一题先记在心里。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "除病毒外，生物体都是由细胞构成的", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">你已经知道，动物、植物和微生物的样子差别很大。<strong>但</strong>科学家发现，它们身上藏着一个共同的秘密：身体都是由<strong>细胞</strong>搭起来的。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>细胞很小</strong></p>
            <p style="color:var(--muted)">必须用显微镜才能看清，一个细胞就是一块小小的空间。</p>
          </div>
          <div class="inner-card">
            <p><strong>细胞里有分工</strong></p>
            <p style="color:var(--muted)">外面一层是细胞膜，里面有细胞质，中间是细胞核；植物细胞外面还有一层细胞壁。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="细胞结构示意图，标注细胞壁、细胞膜、细胞质、细胞核">
          <figcaption>植物细胞的结构：最外面是细胞壁，往里是细胞膜，中间有细胞核，其余部分是细胞质</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔬</span><div><strong>一句话记住：</strong>细胞是生物体结构的基本单位，也是生命活动的基本单位。除病毒以外，所有生物的身体都是它搭起来的。</div></div>
{insight_box([
    {"lens": "解释它", "text": "为什么说细胞是基本单位？因为呼吸、吃东西、生长这些生命活动，都是在细胞里发生的。"},
    {"lens": "比较它", "text": "动物细胞没有细胞壁，所以形状常常是圆的；植物细胞有细胞壁，所以能排成长方形，像一格一格的砖。"},
    {"lens": "迁移它", "text": "医生检查身体时会取一点点组织看细胞，正是因为身体出了问题，常在细胞这一层先露出痕迹。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "显微镜实验室：把洋葱表皮细胞调清楚", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">拖动滑块调节焦距。调到刚好的位置，细胞的轮廓会最清楚，结构名称也会一起出现。</p>
        <div class="lab-panel">
          <div class="canvas-wrap" style="padding:10px">
            <canvas id="cell-canvas" width="720" height="420" style="width:100%;display:block;border-radius:14px"></canvas>
          </div>
          <div class="slider-row">
            <label for="cell-focus">调节焦距</label>
            <input type="range" id="cell-focus" min="0" max="100" value="18" step="1">
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">画面清晰度</span><span class="v" id="cell-clarity">0 %</span></div>
            <div class="readout-cell"><span class="k">观察对象</span><span class="v green">洋葱表皮</span></div>
          </div>
          <p class="result warn" id="cell-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧅</span><div><strong>别忘了记录：</strong>洋葱表皮细胞都是长方形的，一个个像砖块一样紧紧排在一起，中间几乎不留空隙。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "一个细胞能自己活，许多细胞会分工合作", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">生物可以分成两类：有的全身只有<strong>一个细胞</strong>，有的由<strong>许多细胞</strong>组成，细胞之间还会分工。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>单细胞生物</strong></p>
            <p style="color:var(--muted)">草履虫、变形虫、酵母菌。一个细胞就完成了运动、吃东西、呼吸和繁殖。</p>
          </div>
          <div class="inner-card">
            <p><strong>多细胞生物</strong></p>
            <p style="color:var(--muted)">人、大树、猫。细胞分工以后形成组织、器官，人和动物还会形成系统。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="单细胞生物与多细胞生物的结构层次对比示意图">
          <figcaption>左边一个细胞包办全部生命活动，右边许多细胞分工合作，一层一层组成完整的个体</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">不要<strong>误认为</strong>细胞只有多细胞生物才有。草履虫只有一个细胞，照样是完整的生物；也不要<strong>误认为</strong>组织、器官是细胞以外的东西，它们本身就是许多细胞组织起来的结果。</p>
        </div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "对比实验室：草履虫和人的身体有什么不一样", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一点按钮，切换草履虫和人，观察它们在细胞数目和结构层次上的差别。</p>
        <div class="lab-panel">
          <div class="canvas-wrap" style="padding:10px">
            <canvas id="cmp-canvas" width="720" height="320" style="width:100%;display:block;border-radius:14px"></canvas>
          </div>
          <div class="flex-row" style="margin-top:12px">
            <button class="choice" data-cmp="paramecium" style="text-align:center">草履虫</button>
            <button class="choice" data-cmp="human" style="text-align:center">人</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">细胞数目</span><span class="v" id="cmp-cells">只有 1 个</span></div>
            <div class="readout-cell"><span class="k">结构层次</span><span class="v green" id="cmp-level">细胞</span></div>
            <div class="readout-cell"><span class="k">属于</span><span class="v" id="cmp-type">单细胞生物</span></div>
          </div>
          <p class="result" id="cmp-out" style="margin-top:12px"></p>
        </div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：洋葱和草履虫，细胞上有什么一样和不一样", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>洋葱和草履虫都是生物。请比较它们的身体在细胞上有什么相同点和不同点。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>洋葱是一株植物，由许多细胞组成；草履虫只有一个细胞。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找出共同点：</strong>它们都由细胞构成，都有细胞膜、细胞质和细胞核。</div></div>
          <div class="step"><span class="n">3</span><div><strong>找出不同点：</strong>草履虫的一个细胞要完成全部生命活动；洋葱的许多细胞会分工，形成组织和器官。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>得出结论：</strong>细胞是生物体结构和生命活动的基本单位，细胞数目不同，基本单位却是同一个。</div></div>
        </div>
        <div class="kid-note"><span class="emoji">🧱</span><div><strong>打个比方：</strong>细胞就像砖块。草履虫是一间只用一块砖搭成的小屋，虽然只有一块，也能住人；洋葱是用许多块砖砌成的大楼，砖还要按位置分工摆放。</div></div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：这三个说法错在哪里", TTS["conceptest-1"], [
        {"q": "下面哪个说法是正确的？",
         "options": [("除病毒外，生物体都是由细胞构成的", True),
                     ("只有动物才有细胞，植物是例外", False),
                     ("只有多细胞生物才有细胞", False)],
         "explain": "植物、动物、微生物的身体都由细胞构成，只有病毒例外。<strong>错因提醒：</strong>最常见错误是误认为植物没有细胞，或者把细胞当成多细胞生物独有的东西。"},
        {"q": "草履虫全身只有一个细胞，它为什么仍然是完整的生物？",
         "options": [("这一个细胞就能完成运动、吃东西、呼吸等全部生命活动", True),
                     ("因为它其实是由很多小细胞拼成的", False),
                     ("因为它会分裂成许多细胞", False)],
         "explain": "单细胞生物虽然只有一个细胞，但生命活动一样不缺。<strong>错因提醒：</strong>常见错误是把细胞数目少误认为不算完整的生物，把数目多当成生命的必要条件。"},
        {"q": "人体里肌肉、神经这些不同的细胞能一起工作，是因为：",
         "options": [("细胞分工以后形成了组织、器官和系统", True),
                     ("所有细胞的形状和功能都一样", False),
                     ("细胞长大以后直接变成了器官", False)],
         "explain": "多细胞生物的细胞会分工，先形成组织，再形成器官和系统。<strong>错因提醒：</strong>误认为细胞是孤立的，或者把组织、器官和细胞搞混，都是本课的高频错误。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：给四种生物发一张细胞身份证", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面四个生物，请你判断它的身体是一个细胞，还是许多细胞，然后写出你的观察记录。</p>
        <div id="id-cards" class="grid grid-2">
''' + "\n".join(f'''          <div class="inner-card" data-idrow="{c["key"]}" data-correct="{c["correct"]}" data-why="{c["why"]}">
            <p><strong>{c["name"]}</strong>：它的身体是</p>
            <div class="flex-row" style="margin-top:8px">
              <button class="choice" data-idpick="single" style="text-align:center">单细胞生物</button>
              <button class="choice" data-idpick="multi" style="text-align:center">多细胞生物</button>
            </div>
            <p class="result warn" data-idout style="display:none;margin-top:8px"></p>
          </div>''' for c in ID_CARDS) + f'''
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>写出你的观察记录：</strong></p>
          <p style="color:var(--muted)">你在显微镜下看到的洋葱表皮细胞是什么形状？它们是紧紧挨在一起，还是中间有空隙？每个细胞里都看到了什么？</p>
          <textarea id="syn-answer" rows="3" placeholder="我看到的细胞是……它们……每个细胞里有……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，你还能判断吗", TTS["posttest"], [
        {"q": "手指划破一个小口子，过几天就长好了。这个过程中主要在发生什么？",
         "options": [("皮肤细胞不断分裂，长出新的细胞把伤口补上", True),
                     ("伤口处凭空长出了新皮肤", False),
                     ("身体里的细胞总数一直没有变化", False)],
         "explain": "伤口的愈合靠的是细胞分裂，新细胞把缺口补起来。这正是细胞是生命活动基本单位的证据。"},
        {"q": "一棵大树能从一粒种子长到几米高，根本原因是：",
         "options": [("细胞数目增多、体积增大", True), ("细胞被水泡大了", False), ("树干里填进了泥土", False)],
         "explain": "生物由小长大，靠的是细胞分裂让数目变多，以及细胞生长让体积变大。"},
        {"q": "下面关于病毒的说法，哪一句是正确的？",
         "options": [("病毒没有细胞结构，是生物界里的例外", True),
                     ("病毒也是由一个细胞构成的", False),
                     ("病毒有细胞壁，所以很难消灭", False)],
         "explain": "除病毒外，生物体都由细胞构成，病毒正是那个例外。它也是上节课我们认识的微生物之一。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话记住最小的生命单位", TTS["summary"], f'''
        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>基本单位</strong>：除病毒外，生物体都是由细胞构成的；细胞是结构和生命活动的基本单位。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>结构</strong>：细胞膜、细胞质、细胞核；植物细胞外面还多一层细胞壁。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>两类生物</strong>：单细胞生物一个细胞包办全部生命活动；多细胞生物的细胞分工形成组织、器官甚至系统。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那片洋葱：</strong>它薄得几乎透明，可放到显微镜下，里面是一格一格排列整齐的细胞；草履虫只有一个细胞，也在认真地活着。样子差得远，构成生命的基本单位却是同一个。</p>
        </div>
        <div class="inner-card">
          <p><strong>讲给同桌听：</strong>请用"细胞、单细胞、多细胞、组织、器官"这五个词，说说为什么大树和一株草履虫都属于生物。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出细胞是生物体什么的基本单位，并说出细胞膜、细胞质、细胞核三个结构。",
            "在草履虫、洋葱、人中，选出单细胞生物和多细胞生物各一个，并说明理由。",
        ],
        [
            "用橡皮泥或者彩纸做一个细胞模型，把细胞膜、细胞质、细胞核标出来，拍照或带到课堂上讲给同学听。",
            "把洋葱表皮细胞的观察画下来，标出细胞壁、细胞膜和细胞核。",
        ],
        [
            "找一株植物的叶或者茎，画出你看到的细胞排列方式，并说明它们为什么紧紧挤在一起，中间几乎不留空隙。",
            "查阅资料，说说为什么医生做检查时常要取一点点组织看细胞，用三句话写下来。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-cell-unit",
    "node_id": "sci-e-cell-unit",
    "title": "细胞：生物体最小的生命单位",
    "name_en": "The Cell: the smallest unit of life",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "life-science",
    "domain_cn": "生命科学 · 生命的构成",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "借助洋葱表皮细胞的调焦观察认识细胞的基本结构，理解除病毒外生物体都由细胞构成、细胞是结构和生命活动的基本单位，并能比较单细胞生物与多细胞生物的结构层次。",
    "tags": ["细胞", "细胞壁", "细胞核", "单细胞生物", "多细胞生物", "组织与器官"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念5「生命系统的构成层次」学习内容5.3 细胞是生物体结构与生命活动的基本单位——5～6年级认识细胞是生物体结构的基本单位。",
    "hero_question": "一片薄薄的洋葱和一只小小的草履虫，身体里藏着同一个秘密——是什么？",
    "hero_alt": "细胞知识结构图：细胞是基本单位、细胞的结构、单细胞与多细胞",
    "hero_caption": "细胞 · 除病毒外生物体都由细胞构成 · 细胞膜·细胞质·细胞核（植物还有细胞壁） · 一个细胞也能活",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的观察和对比都会围着它转。",
    "anchor_choices": [
        {"t": "我身上到底有多少个细胞？", "d": "想知道身体里细胞的数目和大小", "v": "我身上到底有多少个细胞"},
        {"t": "一个细胞能自己活着吗？", "d": "想知道草履虫这样的生物怎么活", "v": "一个细胞能自己活着吗"},
        {"t": "洋葱那么大，也是细胞组成的吗？", "d": "想亲眼看看植物身体里的细胞", "v": "洋葱那么大也是细胞组成的吗"},
        {"t": "细胞里面到底有什么？", "d": "想知道细胞的结构长什么样", "v": "细胞里面到底有什么"},
    ],
    "objectives": [
        "能说出除病毒外生物体都是由细胞构成的，细胞是生物体结构和生命活动的基本单位",
        "能在显微镜视野中认出细胞，并指认细胞壁、细胞膜和细胞核",
        "能比较单细胞生物与多细胞生物，说出各自的代表生物",
        "能说出细胞、组织、器官之间的层次关系，并举例说明细胞分工",
    ],
    "objectives_plain": [
        "能说出除病毒外生物体都是由细胞构成的，细胞是生物体结构和生命活动的基本单位",
        "能在显微镜视野中认出细胞，并指认细胞壁、细胞膜和细胞核",
        "能比较单细胞生物与多细胞生物，说出各自的代表生物",
        "能说出细胞、组织、器官之间的层次关系，并举例说明细胞分工",
    ],
    "standards": [
        {"content": "认识细胞是生物体结构的基本单位，能说出细胞的基本结构",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念5 生命系统的构成层次·学习内容5.3（5～6年级）"},
        {"content": "能使用显微镜等工具观察生物体的细微结构并描述观察结果",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》科学探究·工具与技术（5～6年级）"},
    ],
    "prereqs": ["sci-e-microorganisms"],
    "prereqs_name": "微生物：小到看不见的居民",
    "prereqs_meta": "sci-e-microorganisms",
    "leads_to": ["sci-e-human-life-origin"],
    "next_meta": "sci-e-human-life-origin",
    "section_images": ["assets/sci-e-cell-unit-fig1.webp", "assets/sci-e-cell-unit-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "洋葱和草履虫差别那么大，身体里却藏着同一个秘密，先猜一猜是什么。",
        "problem-anchor": "先定一个小目标：这节课结束时，你要能说出细胞是什么、里面有什么。",
        "objectives": "看清四件事：细胞是基本单位、细胞的结构、单细胞与多细胞、细胞怎样分工。",
        "pretest": "凭直觉选就好，错了不扣分——前测帮你先看清自己现在站在哪里。",
        "module-1": "除病毒外，所有生物的身体都是细胞搭起来的，记住细胞膜、细胞质、细胞核。",
        "lab-1": "慢慢转滑块，调到最清楚的位置，细胞的轮廓和结构名称才会一起出来。",
        "module-2": "一个细胞能包办全部生命活动，许多细胞则会分工，形成组织、器官、系统。",
        "lab-2": "切过去切回来，比一比细胞数目和结构层次各有什么不同。",
        "worked-example": "四步走：看清条件、找共同点、找不同点、得出结论。",
        "conceptest-1": "这三道题都埋了高频错误，选完看清每一个解释。",
        "synthesis": "四个生物各填一张身份证，别忘了写下你看到的洋葱细胞。",
        "posttest": "换了伤口愈合、大树长高和病毒的新情境，看看你还能不能判断准确。",
        "summary": "回到开头那片洋葱：它和草履虫差得那么远，为什么都是细胞搭起来的？",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「生命系统的构成层次」中段的空缺：知识树原有生物分类与微生物，缺少细胞这一层，学生会在没有细胞概念的情况下直接跳到人的生命起点。设计上用一次真实的调焦体验把细胞看得见——滑块从模糊调到清晰，细胞壁、细胞核随清晰度出现；再用草履虫与人的对比把单细胞、多细胞的层次差别摆出来，最后用细胞身份证收束到一句可带走的话：除病毒外，生物体都由细胞构成，细胞是生命活动的基本单位。",
    "plan_table": """| 1 | cover | 细胞：生物体最小的生命单位 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：你身体里有什么？ | 起·前测（暴露直觉） |
| 5 | concept | 除病毒外，生物体都是由细胞构成的 | 承·概念一（基本单位与结构） |
| 6 | interactive | 显微镜实验室：把洋葱表皮细胞调清楚 | 承·实验室一（调焦观察） |
| 7 | concept | 一个细胞能自己活，许多细胞会分工合作 | 承·概念二（单细胞与多细胞） |
| 8 | interactive | 对比实验室：草履虫和人的身体有什么不一样 | 承·实验室二（对比切换） |
| 9 | concept | 例题示范：洋葱和草履虫，细胞上有什么一样和不一样 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：这三个说法错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：给四种生物发一张细胞身份证 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，你还能判断吗 | 合·后测 |
| 13 | summary | 小结：三句话记住最小的生命单位 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：细胞是基本单位 / 细胞的结构 / 单细胞与多细胞 三栏标注\n- P5 细胞结构图（已生成）：细胞壁、细胞膜、细胞质、细胞核标注\n- P7 层次对比图（已生成）：单细胞生物与多细胞生物的细胞→组织→器官→系统\n- 若需补充：洋葱表皮细胞显微镜实拍照片、细胞模型照片",
}
