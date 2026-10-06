# -*- coding: utf-8 -*-
"""小学科学 · 光的反射与色散（G5）—— 补齐课标「物质的运动与相互作用·3.3 声音与光的传播」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-light-reflection-fig1.webp'
F2 = './assets/sci-e-light-reflection-fig2.webp'

TTS = {
    "hero": "先做一件好玩的事。拿一面小镜子放在桌上，用手电筒斜着照过去，天花板上马上会亮起一个光斑。光本来是往镜子那边走的，怎么突然拐个弯跑到天花板上去了？还有一件事更神奇：一束看上去没有颜色的白光，穿过一块三棱镜，墙上就出现了一条七彩光带。这节课我们就把这两件事弄明白。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道光为什么会拐弯，还是想知道七种颜色到底藏在哪里，又或者你想亲手在教室里做出一道彩虹。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出光遇到物体表面会发生反射，知道入射光和反射光分居法线两侧。第二，能说出反射角等于入射角。第三，知道白光是由多种色光组成的，三棱镜能把白光分解成七色光。第四，能解释镜子里的字为什么是反的，以及雨后为什么会出现彩虹。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好知道要重点听哪里。选完立刻会出现解释。",
    "module-1": "我们来仔细看一束光碰到镜面以后发生了什么。光照射到镜面的那一点，我们画一条垂直的虚线，叫做法线。射向镜面的那束光叫入射光，被弹回来的那束光叫反射光。你会发现两件事。第一，入射光和反射光分别待在法线的两边，一个在左一个在右。第二，入射光线和法线的夹角叫入射角，反射光线和法线的夹角叫反射角，这两个角永远一样大。入射角是三十度，反射角就是三十度。",
    "lab-1": "光说规律还不够，我们把它画出来看。下面这个反射台里，有一面镜子和一束光。拖动滑块改变入射角，光路图画会立刻跟着变，你一边拖一边看上面的两个读数，看看入射角和反射角是不是总是一样大。再点一下粗糙纸面，看看光打在上面会变成什么样。",
    "module-2": "再来看第二件事。把三棱镜放在阳光下，让一束白光斜着穿过它，另一边的白墙上就会出现一条彩色光带，从红、橙、黄、绿、蓝、靛一直到紫，一条都不少。这说明一件很重要的事：看上去没有颜色的白光，其实是由很多种色光混合而成的，三棱镜只是把它们分开，让它们按顺序排好了队。雨后天空出现彩虹，用的是同一个道理，空气中的小水滴就相当于无数个小三棱镜。",
    "lab-2": "现在你自己来做这道彩虹。点一下按钮，让白光穿过三棱镜，看看光带是怎么展开的。再看一看每种颜色的排列顺序，试着背下来。然后切换到雨后的情境，想想天空里没有三棱镜，那是什么东西在替我们分解阳光。",
    "worked-example": "我们一起分析一道题。一束光斜射到平面镜上，入射光线和镜面的夹角是六十度，反射角是多少度？第一步，先找法线，法线是垂直于镜面的那条虚线。第二步，把角度换算到法线上，入射光线和镜面夹角六十度，那么入射角和法线的夹角就是九十度减六十度，等于三十度。第三步，根据反射角等于入射角，所以反射角也是三十度。第四步，回头检查，如果你的答案是六十度，那说明你把光线和镜面的夹角当成入射角了，这是最常见的一个错误。",
    "conceptest-1": "接下来用三个容易弄混的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "学到这里，请你当一次光路设计师。任务是这样的：教室的墙上有一小块地方照不到太阳，请你用一面小镜子，把阳光引到那块地方去。先想一想镜子应该朝哪个方向放，再动手试一试，看看光斑到底落在了哪里，然后说清楚光走了怎样一条路。",
    "posttest": "最后一轮，用新的情境检验一下。这次会出现汽车后视镜、水面和彩虹，看看你能不能把学到的规律用上去。",
    "summary": "这节课我们弄明白了四件事。第一，光遇到物体表面会反射，入射光和反射光分居法线两侧。第二，反射角永远等于入射角，它们的角都是跟法线比的。第三，白光是由多种色光组成的，三棱镜能把白光分解成红橙黄绿蓝靛紫七种色光。第四，雨后彩虹就是空气中的小水滴把阳光分解了。回到开头那两个问题：光斑会跳到天花板上，是因为光被镜面反射了；白墙上出现彩带，是因为白光被三棱镜分解了。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：画出一束光射到平面镜上被反射的光路图，标出入射光线、反射光线和法线。第二层能力应用，动手做：拿一面小镜子和一只手电筒，把光斑打到墙上不同的位置，记录下你每次是怎么调整角度的。第三层迁移挑战，选做：用一杯水和一张白纸，在阳光下自己做一道彩虹，把七种颜色按顺序写出来。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 光会反射", "lab-1": "实验室一 镜面反射台", "module-2": "概念二 白光会分身",
    "lab-2": "实验室二 三棱镜色散", "worked-example": "例题讲解 算反射角", "conceptest-1": "概念测试",
    "synthesis": "综合任务 光路设计师", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

CUSTOM_JS = r"""
/* ============================================================
   sci-e-light-reflection 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 镜面反射台：滑块改入射角 → Canvas 实时画光路
   3) 三棱镜色散台：白光穿过棱镜展开七色光带 / 雨后彩虹情境
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

  /* ---------- 2. 镜面反射台 ---------- */
  var cv = document.getElementById('mirror-canvas');
  if (cv) {
    var ctx = cv.getContext('2d');
    var range = document.getElementById('angle-range');
    var angleVal = document.getElementById('angle-val');
    var rInc = document.getElementById('r-inc');
    var rRef = document.getElementById('r-ref');
    var rRel = document.getElementById('r-rel');
    var out = document.getElementById('mirror-out');
    var surface = 'smooth';

    function draw() {
      var W = cv.width, H = cv.height;
      var deg = Number(range.value);
      var rad = deg * Math.PI / 180;
      var O = { x: W / 2, y: H * 0.78 };   // 入射点
      var L = H * 0.52;                    // 光线长度

      ctx.clearRect(0, 0, W, H);

      // 镜面
      if (surface === 'smooth') {
        ctx.fillStyle = '#cfe3f5';
        ctx.fillRect(40, O.y, W - 80, 16);
        ctx.strokeStyle = '#8fb6d8';
        ctx.lineWidth = 2;
        ctx.strokeRect(40, O.y, W - 80, 16);
      } else {
        ctx.fillStyle = '#efe3cc';
        ctx.fillRect(40, O.y, W - 80, 16);
        ctx.strokeStyle = '#c8b48c';
        ctx.lineWidth = 2;
        ctx.strokeRect(40, O.y, W - 80, 16);
        ctx.strokeStyle = 'rgba(200,180,140,.65)';
        ctx.lineWidth = 1;
        for (var t = 0; t < 26; t++) {
          var px = 46 + t * (W - 92) / 26;
          ctx.beginPath();
          ctx.arc(px, O.y + 8, 3.5, Math.PI, 0);
          ctx.stroke();
        }
      }

      // 法线
      ctx.save();
      ctx.setLineDash([9, 7]);
      ctx.strokeStyle = '#7a8aa0';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(O.x, O.y);
      ctx.lineTo(O.x, O.y - L * 1.12);
      ctx.stroke();
      ctx.restore();
      ctx.fillStyle = '#5c6b80';
      ctx.font = 'bold 16px sans-serif';
      ctx.fillText('法线', O.x + 10, O.y - L * 1.12 + 6);

      // 入射光线
      var ix = O.x - Math.sin(rad) * L;
      var iy = O.y - Math.cos(rad) * L;
      ctx.strokeStyle = '#ff6b6b';
      ctx.lineWidth = 4;
      ctx.beginPath();
      ctx.moveTo(ix, iy);
      ctx.lineTo(O.x, O.y);
      ctx.stroke();
      arrow(ctx, ix, iy, O.x, O.y, '#ff6b6b');
      ctx.fillStyle = '#d94b4b';
      ctx.fillText('入射光线', Math.max(8, ix - 96), iy + 6);

      if (surface === 'smooth') {
        // 反射光线：与法线夹角相同，位于另一侧
        var rx = O.x + Math.sin(rad) * L;
        var ry = O.y - Math.cos(rad) * L;
        ctx.strokeStyle = '#14897f';
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(O.x, O.y);
        ctx.lineTo(rx, ry);
        ctx.stroke();
        arrow(ctx, O.x, O.y, rx, ry, '#14897f');
        ctx.fillStyle = '#0f6f68';
        ctx.fillText('反射光线', Math.min(W - 90, rx + 12), ry + 6);

        // 角度弧
        arc(ctx, O, 62, -Math.PI / 2, -Math.PI / 2 - rad, '#d94b4b', deg + '°', -1);
        arc(ctx, O, 62, -Math.PI / 2, -Math.PI / 2 + rad, '#0f6f68', deg + '°', 1);
      } else {
        // 粗糙表面：漫反射，多束反射光射向不同方向
        for (var k = 0; k < 7; k++) {
          var a = (-70 + k * 24) * Math.PI / 180;
          var sx = O.x + Math.sin(a) * L * 0.86;
          var sy = O.y - Math.cos(a) * L * 0.86;
          ctx.strokeStyle = 'rgba(20,137,127,.62)';
          ctx.lineWidth = 3;
          ctx.beginPath();
          ctx.moveTo(O.x, O.y);
          ctx.lineTo(sx, sy);
          ctx.stroke();
        }
        ctx.fillStyle = '#0f6f68';
        ctx.font = 'bold 16px sans-serif';
        ctx.fillText('光射向各个方向', O.x + 30, O.y - L * 0.95);
      }

      // 入射点
      ctx.fillStyle = '#3a3126';
      ctx.beginPath();
      ctx.arc(O.x, O.y, 5, 0, Math.PI * 2);
      ctx.fill();
      ctx.font = 'bold 15px sans-serif';
      ctx.fillText('入射点', O.x + 10, O.y + 30);
    }

    function arrow(c, x1, y1, x2, y2, color) {
      var ang = Math.atan2(y2 - y1, x2 - x1);
      c.fillStyle = color;
      c.beginPath();
      c.moveTo(x2, y2);
      c.lineTo(x2 - 14 * Math.cos(ang - 0.4), y2 - 14 * Math.sin(ang - 0.4));
      c.lineTo(x2 - 14 * Math.cos(ang + 0.4), y2 - 14 * Math.sin(ang + 0.4));
      c.closePath();
      c.fill();
    }

    function arc(c, O, r, a1, a2, color, label, side) {
      c.save();
      c.strokeStyle = color;
      c.lineWidth = 3;
      c.beginPath();
      c.arc(O.x, O.y, r, Math.min(a1, a2), Math.max(a1, a2));
      c.stroke();
      c.restore();
      var mid = (a1 + a2) / 2;
      c.fillStyle = color;
      c.font = 'bold 17px sans-serif';
      c.fillText(label, O.x + Math.cos(mid) * (r + 10) + (side > 0 ? 4 : -46), O.y + Math.sin(mid) * (r + 10) + 6);
    }

    function update() {
      var deg = Number(range.value);
      angleVal.textContent = deg + '°';
      rInc.textContent = deg + '°';
      rRef.textContent = deg + '°';
      if (surface === 'smooth') {
        rRel.textContent = '分居法线两侧';
        rRel.className = 'v green';
        out.className = 'result';
        out.innerHTML = '<strong>入射角 ' + deg + '°，反射角也是 ' + deg + '°。</strong>' +
          '不管你把入射角调到多大，反射角永远跟它一样大——这就是光的反射规律。' +
          (deg === 0 ? ' 现在光正好沿着法线射下来，它原路返回。' : ' 注意：这两个角都是跟<strong>法线</strong>比的，不是跟镜面比的。');
      } else {
        rRel.textContent = '射向各个方向';
        rRel.className = 'v';
        out.className = 'result warn';
        out.innerHTML = '<strong>粗糙纸面：光被弹向四面八方。</strong>' +
          '纸面上有很多微小的凹凸，每一小块都遵守反射规律，但方向各不相同，合起来就成了漫反射。' +
          '正因为有漫反射，我们才能从各个角度看见不发光的物体——比如现在你手里的这张纸。';
      }
      draw();
    }

    range.addEventListener('input', update);
    document.getElementById('mirror-smooth').addEventListener('click', function () {
      surface = 'smooth';
      document.getElementById('mirror-smooth').classList.add('selected');
      document.getElementById('mirror-rough').classList.remove('selected');
      update();
    });
    document.getElementById('mirror-rough').addEventListener('click', function () {
      surface = 'rough';
      document.getElementById('mirror-rough').classList.add('selected');
      document.getElementById('mirror-smooth').classList.remove('selected');
      update();
    });
    document.getElementById('mirror-reset').addEventListener('click', function () {
      range.value = '45';
      surface = 'smooth';
      document.getElementById('mirror-smooth').classList.add('selected');
      document.getElementById('mirror-rough').classList.remove('selected');
      update();
    });
    document.getElementById('mirror-smooth').classList.add('selected');
    update();
  }

  /* ---------- 3. 三棱镜色散台 ---------- */
  var prism = document.getElementById('prism-stage');
  if (prism) {
    var COLORS = [
      ['红', '#e63946'], ['橙', '#f77f00'], ['黄', '#fcbf49'], ['绿', '#2a9d8f'],
      ['蓝', '#118ab2'], ['靛', '#3d5a80'], ['紫', '#7b2cbf']
    ];
    var band = document.getElementById('prism-band');
    var out2 = document.getElementById('prism-out');
    var rainStage = 'prism';

    function renderBand() {
      band.innerHTML = '';
      COLORS.forEach(function (c) {
        var b = document.createElement('span');
        b.style.cssText = 'flex:1;height:100%;background:' + c[1] +
          ';display:grid;place-items:center;color:#fff;font-weight:800;font-size:15px;border-radius:4px';
        b.textContent = c[0];
        band.appendChild(b);
      });
    }

    function shine() {
      band.style.display = 'flex';
      document.getElementById('prism-in').style.opacity = '1';
      out2.className = 'result';
      out2.innerHTML = '<strong>白光穿过三棱镜，被分解成七种色光。</strong>' +
        '它们按顺序排好队：红、橙、黄、绿、蓝、靛、紫。' +
        '请记住：白光本来就有这些颜色，三棱镜只是把它们<strong>分开</strong>，并没有把白光染色。' +
        '<br><strong>错因提醒：</strong>常见错误是误认为三棱镜给光染上了颜色。三棱镜是无色的，它做的是分光。';
    }

    function reset() {
      band.style.display = 'none';
      document.getElementById('prism-in').style.opacity = '.25';
      out2.className = 'result warn';
      out2.textContent = '现在只有一束白光。点下面的按钮，让它穿过三棱镜。';
    }

    function rain() {
      if (rainStage === 'prism') {
        rainStage = 'rain';
        document.getElementById('prism-scene').textContent = '雨后的天空';
        document.getElementById('prism-prop').textContent = '小水滴';
        band.style.display = 'flex';
        out2.className = 'result';
        out2.innerHTML = '<strong>雨后彩虹：空气里的小水滴就是无数个小三棱镜。</strong>' +
          '雨刚停时，天空还飘着很多小水滴。阳光斜射进水滴，先折射、再反射、最后又折射出来，' +
          '就被分解成了七色光，于是天上出现一道彩虹。彩虹总是出现在太阳的<strong>对面方向</strong>。';
        document.getElementById('rain-btn').textContent = '切换回三棱镜实验';
      } else {
        rainStage = 'prism';
        document.getElementById('prism-scene').textContent = '实验室桌面';
        document.getElementById('prism-prop').textContent = '三棱镜';
        reset();
        document.getElementById('rain-btn').textContent = '切换：彩虹为什么出现在雨后';
      }
    }

    renderBand();
    document.getElementById('prism-go').addEventListener('click', shine);
    document.getElementById('prism-reset').addEventListener('click', reset);
    document.getElementById('rain-btn').addEventListener('click', rain);
    reset();
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：光遇到镜子会怎样？", TTS["pretest"], [
        {"q": "用手电筒斜着照一面镜子，天花板上出现了光斑。这个光斑是怎么来的？",
         "options": [("光被镜面反射，改变了方向射到天花板上", True),
                     ("光自己会拐弯，跟镜子没关系", False),
                     ("镜子里本来藏着一小团光", False)],
         "explain": "光遇到镜面会被反射，方向改变后射到天花板上，就形成了光斑。<strong>错因提醒：</strong>常见错误是误认为光会自己拐弯。光在同一物质中总是沿直线传播的，是<strong>镜面</strong>让它的方向变了。"},
        {"q": "一束白光穿过三棱镜以后，在墙上出现了一条彩色光带。这说明：",
         "options": [("白光是由多种色光组成的", True),
                     ("三棱镜本身有颜色，把光染了", False),
                     ("是墙壁把白光变成了彩色", False)],
         "explain": "白光里本来就藏着多种色光，三棱镜把它们分开排好队。<strong>错因提醒：</strong>不要误认为三棱镜给光染了色。三棱镜是无色透明的，它只是分光，不产生颜色。"},
        {"q": "你做实验时用手电筒照到了同桌的眼睛，应该怎么做？",
         "options": [("马上移开，并提醒大家不要用强光直射别人眼睛", True),
                     ("没关系，手电筒的光很弱", False),
                     ("继续照，看看他会不会眨眼睛", False)],
         "explain": "强光直射眼睛会让人很不舒服，甚至受伤。<strong>错因提醒：</strong>很多同学觉得实验中的光不亮、无所谓，这是很危险的搞混——玩激光笔、直视太阳或强光源，都可能伤害眼睛。做光的实验时，光只照物体，不照人眼。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "光遇到物体表面会反射，反射光与入射光分居法线两侧", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">光照到镜子上，会被<strong>弹回来</strong>，这就是<strong>光的反射</strong>。要看懂反射，先认识三个名字：<strong>入射光线</strong>、<strong>反射光线</strong>、还有那条垂直于镜面的虚线——<strong>法线</strong>。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>谁在法线两侧</strong></p>
            <p style="color:var(--muted)">入射光线在左边，反射光线就在右边，两者<strong>分居法线两侧</strong>。</p>
          </div>
          <div class="inner-card">
            <p><strong>两个角谁大</strong></p>
            <p style="color:var(--muted)">反射角 <strong>永远等于</strong> 入射角。角都是跟<strong>法线</strong>比的，不是跟镜面比。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="光的反射光路图：入射光线、反射光线、法线、入射角与反射角">
          <figcaption>入射光线射到镜面后沿反射光线弹出，两条光线分居法线两侧，入射角 <strong>等于</strong> 反射角</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🎯</span><div><strong>一句口诀记住它：</strong>三线共面、两线分居、两角相等。三条线在同一个平面上，入射光和反射光分居法线两侧，两个角一样大。</div></div>
{insight_box([
    {"lens": "看见它", "text": "白天你能看见课桌、看见同学，是因为太阳光照到他们身上又被反射进你的眼睛。不发光的物体能被看见，全靠反射。"},
    {"lens": "解释它", "text": "为什么镜子里的字是反的？因为镜子把光左右颠倒地反射回来，你看到的其实是文字的镜像，所以左右正好对调。"},
    {"lens": "迁移它", "text": "自行车尾灯、路口的反光标志，里面都装着小棱镜或反光膜，把汽车的光原路反射回去，让司机远远就能看见。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "镜面反射台：拖一拖，看两个角是不是一样大", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">拖动下面的滑块改变入射角，光路图和两个读数会立刻更新。先调到 30°，再调到 60°，对比一下。</p>
        <div class="lab-panel">
          <canvas id="mirror-canvas" width="720" height="380" aria-label="镜面反射光路互动画布"
                  style="width:100%;display:block;border-radius:14px;border:1px solid var(--line-subtle);background:#f7fbff"></canvas>
          <div class="slider-row">
            <label for="angle-range">入射角</label>
            <input type="range" id="angle-range" min="0" max="80" step="5" value="45" style="flex:1;min-width:160px">
            <span id="angle-val" style="font-weight:800;color:#e05555">45°</span>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">入射角（与法线）</span><span class="v" id="r-inc">45°</span></div>
            <div class="readout-cell"><span class="k">反射角（与法线）</span><span class="v green" id="r-ref">45°</span></div>
            <div class="readout-cell"><span class="k">两条光线的位置</span><span class="v" id="r-rel" style="font-size:15px">分居法线两侧</span></div>
          </div>
          <div class="flex-row">
            <button class="choice selected" id="mirror-smooth" style="text-align:center">光滑镜面</button>
            <button class="choice" id="mirror-rough" style="text-align:center">粗糙纸面</button>
            <button class="choice" id="mirror-reset" style="text-align:center">回到 45°</button>
          </div>
          <p class="result warn" id="mirror-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">💡</span><div><strong>注意一个陷阱：</strong>入射角是光线和<strong>法线</strong>的夹角。如果题目说光线和<strong>镜面</strong>成 60°，那入射角其实是 90° 减 60°，等于 30°。这里最容易搞混。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "白光由多种色光组成，三棱镜能把白光分解成七色光", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">看起来没有颜色的白光，其实是个<strong>颜色大集合</strong>。让白光穿过三棱镜，它就会按红、橙、黄、绿、蓝、靛、紫的顺序散开——这叫<strong>光的色散</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div>白光斜着射进三棱镜，进入时先发生一次<strong>折射</strong>。</div></div>
          <div class="step"><span class="n">2</span><div>不同颜色的光偏折的程度不一样，紫光偏得最多，红光偏得最少。</div></div>
          <div class="step"><span class="n green">3</span><div>从三棱镜射出来时，各种色光已经分开，在白墙上排成一条<strong>七色光带</strong>。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="白光通过三棱镜后分解成红橙黄绿蓝靛紫七色光带">
          <figcaption>白光 → 三棱镜 → 七色光带：红、橙、黄、绿、蓝、靛、紫，顺序永远不变</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🌈</span><div><strong>想想彩虹：</strong>雨后天空飘着许多小水滴，每一颗都像一个小小的三棱镜。阳光射进水滴再射出来，就被分解成七色光——天上就出现了一道彩虹。要看得见彩虹，你得背对太阳站着。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "三棱镜色散台：亲手把白光分成七色", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点按钮让白光穿过三棱镜，看清楚七种颜色是怎么排队的；再切换到雨后情境，想一想天空里是什么在替我们分光。</p>
        <div class="lab-panel">
          <div class="lab-stage" id="prism-stage" style="height:250px;background:linear-gradient(180deg,#f2f7ff 0%,#e6f0ff 100%)">
            <div style="position:absolute;left:14px;top:12px;font-size:13px;color:#94866c">场景：<strong id="prism-scene">实验室桌面</strong></div>
            <div style="position:absolute;left:8%;top:50%;transform:translateY(-50%);font-size:14px;font-weight:800;color:#3a3126">白光</div>
            <div id="prism-in" style="position:absolute;left:19%;top:50%;transform:translateY(-50%);width:26%;height:6px;border-radius:3px;background:linear-gradient(90deg,rgba(255,255,255,.9),#ffffff);border:1px solid #cfd8e3;transition:opacity .4s"></div>
            <div style="position:absolute;left:46%;top:50%;transform:translateY(-50%);width:0;height:0;border-left:26px solid transparent;border-right:26px solid transparent;border-bottom:74px solid rgba(180,215,255,.85);filter:drop-shadow(0 2px 4px rgba(0,0,0,.12))"></div>
            <div style="position:absolute;left:45.2%;top:calc(50% + 46px);font-size:13px;font-weight:700;color:#3f6ea8" id="prism-prop">三棱镜</div>
            <div id="prism-band" style="display:none;position:absolute;left:62%;right:5%;top:34%;height:132px;gap:4px"></div>
            <div style="position:absolute;right:8%;top:calc(34% - 24px);font-size:13px;color:#94866c">白墙上的七色光带</div>
          </div>
          <div class="flex-row">
            <button class="choice" id="prism-go" style="text-align:center">让白光穿过三棱镜</button>
            <button class="choice" id="prism-reset" style="text-align:center">收起光带</button>
            <button class="choice" id="rain-btn" style="text-align:center">切换：彩虹为什么出现在雨后</button>
          </div>
          <p class="result warn" id="prism-out" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧠</span><div><strong>动脑想一想：</strong>把七色光带里的颜色重新混在一起，会变回什么颜色？答案是白色。所以三棱镜并没有创造颜色，它只是把本来就有的颜色<strong>分开</strong>了。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：入射光线和镜面成 60°，反射角是多少？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>一束光斜射到平面镜上，入射光线与镜面的夹角是 60°。请算出反射角，并说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先找法线：</strong>法线是过入射点、垂直于镜面的那条虚线。所以法线和镜面成 90°。</div></div>
          <div class="step"><span class="n">2</span><div><strong>换算成入射角：</strong>入射角是光线与<strong>法线</strong>的夹角，90° − 60° = <strong>30°</strong>。</div></div>
          <div class="step"><span class="n">3</span><div><strong>用规律作答：</strong>反射角等于入射角，所以反射角也是 <strong>30°</strong>。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>回头检查：</strong>反射光线与镜面的夹角应该是 90° − 30° = 60°，和入射光线与镜面的夹角一样，答案合理。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">直接写 60° 是最常见的错误，原因是把<strong>光线和镜面的夹角</strong>当成了入射角。请记住：入射角、反射角都是跟<strong>法线</strong>比的。以后再遇到这种题，第一步永远是先画法线。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("反射角永远等于入射角，两个角都是与法线的夹角", True),
                     ("入射角越大，反射角越小", False),
                     ("光线与镜面的夹角就是入射角", False)],
         "explain": "反射角始终等于入射角，而且两个角都从法线量起。<strong>错因提醒：</strong>把光线与镜面的夹角当成入射角，是这一课最高频的常见错误——两者相加才是 90°。"},
        {"q": "教室里各个位置的同学都能看见黑板上的字，这是因为：",
         "options": [("黑板表面发生漫反射，把光射向各个方向", True),
                     ("黑板像镜子一样把光集中反射到一个方向", False),
                     ("黑板自己会发光", False)],
         "explain": "黑板表面比较粗糙，光被弹向四面八方，所以每个位置都能看到。<strong>错因提醒：</strong>有同学误认为漫反射不遵守反射规律，其实每一小块都严格遵守，只是方向各不相同。"},
        {"q": "关于彩虹，下面说法正确的是：",
         "options": [("空气中的小水滴把阳光分解成了七色光", True),
                     ("彩虹是天空自己长出来的颜色", False),
                     ("要面对太阳才能看见彩虹", False)],
         "explain": "小水滴相当于无数个小三棱镜，把阳光分解成七色光。<strong>错因提醒：</strong>很多同学把方向搞混了——看彩虹要<strong>背对太阳</strong>，因为光是从你身后射进水滴再反射回你眼里的。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：当一次光路设计师", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">教室墙上有一小块地方照不到太阳，请你用一面小镜子，把阳光引到那块地方去。先想清楚再动手。</p>
        <div class="inner-card">
          <p><strong>第一步：先预测</strong></p>
          <p style="color:var(--muted)">把镜子放在窗台上，光斑会落在墙上高一点的地方，还是低一点的地方？先写下你的猜测，再去试。</p>
        </div>
        <div class="inner-card">
          <p><strong>第二步：动手调，记录变化</strong></p>
          <p style="color:var(--muted)">慢慢转动镜子，光斑会往哪边跑？把三次不同的角度和光斑位置记在下面的表格里。</p>
          <textarea id="syn-table" rows="3" placeholder="第 1 次：镜子角度……光斑落在……&#10;第 2 次：镜子角度……光斑落在……&#10;第 3 次：镜子角度……光斑落在……"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>第三步：说清道理</strong></p>
          <p style="color:var(--muted)">用「入射光线、法线、反射光线、反射角等于入射角」这几个词，把光走的路讲给同桌听。</p>
          <textarea id="syn-explain" rows="3" placeholder="阳光射到镜面上，发生了什么……镜子的角度一改变，反射光线就……"></textarea>
        </div>
        <div class="kid-note"><span class="emoji">⚠️</span><div><strong>安全提示：</strong>用镜子反射阳光时，千万不要让光斑照到同学的眼睛。做光的实验，光只照物体、不照人眼。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "汽车的两侧后视镜能把车后的情况反射给司机。司机从后视镜里看到的景物：",
         "options": [("是景物反射的光经镜面反射后进入司机的眼睛", True),
                     ("是镜子里本来就存在的一个小画面", False),
                     ("是景物自己跑到镜子里去了", False)],
         "explain": "后视镜不能自己发光，它只是把景物射来的光反射进司机眼里。<strong>错因提醒：</strong>常见错误是误认为镜子里有个小世界。其实镜中的像就是光被你看见的结果。"},
        {"q": "平静的水面能像镜子一样映出岸边的树，这是因为：",
         "options": [("平静水面很光滑，光在水面上发生了镜面反射", True),
                     ("水面把树吸了进去", False),
                     ("水会发光，把树照亮了", False)],
         "explain": "水面平静时光滑，能像镜子一样反射。<strong>错因提醒：</strong>一旦有风把水面吹皱，反射就变成漫反射，树影也就看不清楚了——这一点常常被忽略。"},
        {"q": "一束紫光和一束红光一起斜射进三棱镜，出来以后：",
         "options": [("两种光分开的角度不一样，紫光偏折得更厉害", True),
                     ("两种光完全重合在一起，分不开", False),
                     ("红光偏折得更厉害", False)],
         "explain": "不同色光偏折程度不同，紫光偏得最多，红光偏得最少，这正是色散能发生的原因。<strong>错因提醒：</strong>容易搞混的是谁偏得多——记住口诀「紫偏多、红偏少」，白光才会被拆开。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：四句话，把光和颜色讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>反射</strong>：光遇到物体表面会弹回来，入射光和反射光<strong>分居法线两侧</strong>。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>两个角</strong>：反射角<strong>永远等于</strong>入射角，都是从<strong>法线</strong>量起的角。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>白光</strong>：白光是由多种色光组成的，三棱镜能把它们分开。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>七色顺序</strong>：红、橙、黄、绿、蓝、靛、紫，顺序永远不变。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那两个问题：</strong>天花板上的光斑，是手电筒的光被镜面反射后改变了方向；白墙上的彩带，是白光被三棱镜分解成了七色光。一个讲的是光<strong>往哪走</strong>，一个讲的是光<strong>有哪些颜色</strong>。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「反射、法线、入射角、色散」这四个词，说清楚为什么镜子里的字是左右反的。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "画出一束光射到平面镜上被反射的光路图，标出入射光线、反射光线、法线和入射点。",
            "说出反射角与入射角的大小关系，并说明这两个角是跟哪条线比的。",
        ],
        [
            "拿一面小镜子和一只手电筒，把光斑打到墙上不同的位置，记录三次镜子的角度和光斑位置，说说光路是怎么变的。",
            "把七种色光按顺序写出来，并解释雨后彩虹是怎么形成的。",
        ],
        [
            "用一杯清水、一张白纸和阳光，自己做出一道彩虹，把做法和看到的颜色顺序写下来。",
            "在生活里找出三种利用光的反射的物品（例如自行车尾灯、反光衣、潜望镜），说明它们各自解决了什么问题。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-light-reflection",
    "node_id": "sci-e-light-reflection",
    "title": "光的反射与色散：光会拐弯，还会分身",
    "name_en": "Reflection and Dispersion of Light",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "matter-science",
    "domain_cn": "物质科学 · 声音与光",
    "lesson_type": "experiment-inquiry",
    "version": "1.0.0",
    "description": "通过镜面反射台与三棱镜色散两个动手实验，认识光的反射规律（反射光与入射光分居法线两侧、反射角等于入射角），知道白光由多种色光组成、三棱镜能把白光分解成七色光，并用它解释镜子成像与雨后彩虹。",
    "tags": ["光的反射", "法线", "入射角", "反射角", "色散", "三棱镜", "彩虹"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3「物质的运动与相互作用」学习内容3.3 声音与光的传播——1～6年级认识光沿直线传播与光的反射现象；5～6年级用三棱镜使太阳光发生色散。",
    "hero_question": "光本来是直着走的，为什么照到镜子上会拐弯，穿过三棱镜又会分身？",
    "hero_alt": "光的反射与色散知识结构图：反射规律、白光组成、七色顺序",
    "hero_caption": "反射：分居法线两侧 · 反射角等于入射角 ｜ 色散：白光由多种色光组成 · 三棱镜分出红橙黄绿蓝靛紫",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的实验都会围着它转。",
    "anchor_choices": [
        {"t": "光为什么会拐弯？", "d": "想知道镜子把光弹回来的规律", "v": "光为什么会拐弯"},
        {"t": "七种颜色藏在哪里？", "d": "想知道白光里的颜色是怎么被找出来的", "v": "七种颜色藏在哪里"},
        {"t": "镜子里的字为什么是反的？", "d": "想弄懂照镜子时看到的是什么", "v": "镜子里的字为什么是反的"},
        {"t": "彩虹是怎么出现的？", "d": "想在雨后看懂天边那道桥", "v": "彩虹是怎么出现的"},
    ],
    "objectives": [
        "能说出光遇到物体表面会发生反射，知道反射光与入射光分居法线两侧",
        "能说出反射角等于入射角，并会用先画法线的方法算出反射角",
        "知道白光由多种色光组成，三棱镜能把白光分解成七色光",
        "能解释镜子里的字为什么是反的，以及雨后彩虹是怎么形成的",
    ],
    "objectives_plain": [
        "能说出光遇到物体表面会发生反射，知道反射光与入射光分居法线两侧",
        "能说出反射角等于入射角，并会用先画法线的方法算出反射角",
        "知道白光由多种色光组成，三棱镜能把白光分解成七色光",
        "能解释镜子里的字为什么是反的，以及雨后彩虹是怎么形成的",
    ],
    "standards": [
        {"content": "认识光沿直线传播，认识光的反射现象，能举例说明光遇到物体会改变传播方向",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3 物质的运动与相互作用·3.3 声音与光的传播（1～6年级）"},
        {"content": "知道白光由多种色光组成，能用三棱镜使太阳光发生色散，并解释彩虹的成因",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念3 物质的运动与相互作用·3.3 声音与光的传播（5～6年级）"},
    ],
    "prereqs": ["sci-e-light"],
    "prereqs_name": "光的传播与影子",
    "prereqs_meta": "sci-e-light",
    "leads_to": ["sci-e-heat-transfer"],
    "next_meta": "sci-e-heat-transfer",
    "section_images": ["assets/sci-e-light-reflection-fig1.webp", "assets/sci-e-light-reflection-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "光会拐弯，还会分身——两个奇怪的现象，今天都用实验解开。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己算出反射角，还能说清彩虹的来历。",
        "objectives": "看清四件事：反射与法线、反射角等于入射角、白光的组成、解释镜中像与彩虹。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "记住三个名字：入射光线、反射光线、法线。两线分居，两角相等。",
        "lab-1": "拖滑块，把入射角从 0° 调到 80°，盯着两个读数看它们是不是总一样。",
        "module-2": "白光不是没有颜色，而是颜色太多混在一起。三棱镜只是把它们分开。",
        "lab-2": "先让白光穿过三棱镜，再切到雨后情境，想想是谁在替天空分光。",
        "worked-example": "四步走：找法线、换算入射角、用规律作答、回头检查。",
        "conceptest-1": "干扰项里藏着最常见的那几个错误想法，选完看清每一个解释。",
        "synthesis": "转动镜子，光斑就往另一个方向跑——你能不能让光刚好落在暗处？",
        "posttest": "换了后视镜、水面和紫光的新情境，看看你还能不能用上同一条规律。",
        "summary": "回到开头那两个现象：一个讲光往哪走，一个讲光有哪些颜色。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「声音与光的传播」在小学段长期空缺的一课：知识树原有光的传播与影子，缺光的反射与色散。设计上把反射收敛为一条学生能自己验证的规律——反射角等于入射角，并用可拖动的反射台让规律被亲眼看见；再用三棱镜色散把白光的组成讲透，最后落到镜子成像与雨后彩虹两个真实情境收束。",
    "plan_table": """| 1 | cover | 光的反射与色散：光会拐弯，还会分身 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：光遇到镜子会怎样？ | 起·前测（暴露直觉） |
| 5 | concept | 光遇到物体表面会反射，反射光与入射光分居法线两侧 | 承·概念一 |
| 6 | interactive | 镜面反射台：拖一拖，看两个角是不是一样大 | 承·实验室一（滑块 + Canvas 光路） |
| 7 | concept | 白光由多种色光组成，三棱镜能把白光分解成七色光 | 承·概念二 |
| 8 | interactive | 三棱镜色散台：亲手把白光分成七色 | 承·实验室二（色散 + 彩虹情境） |
| 9 | concept | 例题示范：入射光线和镜面成 60°，反射角是多少？ | 转·重难点突破（先画法线 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：当一次光路设计师 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：四句话，把光和颜色讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：反射规律、白光组成、七色顺序三栏标注\n- P5 光的反射光路图（已生成）：入射光线、反射光线、法线、入射角与反射角中文标注\n- P7 三棱镜色散图（已生成）：白光分解成红橙黄绿蓝靛紫七色光带\n- 若需补充：镜子光斑的实拍照片、雨后彩虹的实景照片",
}
