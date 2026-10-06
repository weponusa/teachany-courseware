# -*- coding: utf-8 -*-
"""小学科学 · 自然灾害与防灾减灾：遇到危险怎么办（G5）—— 补齐课标「人类活动与环境·11.2 自然灾害」空缺"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/sci-e-natural-disasters-fig1.webp'
F2 = './assets/sci-e-natural-disasters-fig2.webp'

TTS = {
    "hero": "这节课我们要学一件很有用的本事。地震、洪水、台风、滑坡，这些自然灾害在新闻里出现过。它们来的时候力量很大，可是如果我们认识它的前兆、看得懂预警、做对了动作，受到的伤害就能大大减少。今天我们不吓自己，也不看可怕的东西，只做三件实在的事：认识它、预防它、用正确的方法应对它。",
    "problem-anchor": "在开始之前，先选出你最想弄明白的那个问题。是想知道我们国家哪些地方容易发生哪几种灾害，还是想知道灾害来之前有什么前兆，又或者你想学会几个关键时刻能保护自己的动作。选好之后，就带着这个问题往下看。",
    "objectives": "这节课有四个目标。第一，能说出地震、洪水、台风、滑坡四种常见的自然灾害，并各举一个例子。第二，能说出我国不同地区多发的灾害不一样。第三，能说出几种灾害前兆，并看懂预警信息的等级。第四，能说出并做出几种正确的避险动作，知道在什么情况下该怎么做。",
    "pretest": "先做三道小题，凭你现在的想法选就行，选错了也没关系，正好能看出哪里需要重点听。选完会立刻出现解释。",
    "module-1": "先说什么是自然灾害。自然灾害是指由自然原因引起、并对人的生命和财产造成危害的现象。小学阶段我们要重点认识四种。第一种是地震，大地突然震动，房屋可能开裂甚至倒塌，它常常发生在板块交界的地方。第二种是洪水，暴雨或者连续降雨让河水猛涨，淹掉低洼的地方。第三种是台风，从海上来的强烈风暴，带着狂风和暴雨，主要影响我国东南沿海。第四种是滑坡和泥石流，山坡上大量的泥土石头突然滑下来，常常出现在山区连下暴雨的时候。我们国家很大，各地多发的灾害并不一样。东南沿海最容易遇到台风，长江中下游一带容易发生洪水，西南山区地形陡、雨水多，滑坡和泥石流比较常见，而我国不少地区都处在地震带上，需要防震。",
    "lab-1": "现在我们来做一次情境判断。下面有五个真实会遇到的情境，每一个都给你三个做法。请你选出你认为最正确的那一个。选对了会告诉你为什么对，选错了会告诉你错在哪里，还会说清正确做法是什么。做完五个情境，你就抓住避险的要点。",
    "module-2": "接下来我们学防灾减灾的三件实事。第一件是认识前兆。灾害来之前常常有一些信号：暴雨后山路上出现新的裂缝、泉水突然变浑浊、小石块不断掉落，这些都是滑坡或者泥石流的前兆；井水突然变浑、动物反常地惊慌，也可能是地震前的异常，发现以后要马上告诉大人。第二件是看懂预警。气象和水利部门会用颜色来表示危险程度，从低到高是蓝色、黄色、橙色、红色，红色最危险。收到预警不是看热闹，而是要按照提示行动。第三件是做对动作。地震时记住一个口诀：趴下、遮挡、手抓牢。台风时关紧门窗、远离窗户。洪水来了就往高处转移，不要涉水过河。滑坡和泥石流来了，要往垂直于沟谷方向的两侧高处跑，千万不要顺着沟往下跑。这三件事都做到了，伤害就能明显减少。",
    "lab-2": "光记住还不够，身体也要学会。下面有五个场景，点一点，就能看到每个场景里正确的姿势示意图和三条要点。请你跟着图做一遍动作，同桌互相检查一下，看看哪里还不到位。",
    "worked-example": "我们一起来分析一道题。暑假里，几个同学在山里玩。突然下起大暴雨，他们躲进一条山谷里的小亭子。雨停后，他们发现山路出现了一条新的裂缝，旁边的小水沟里水变得很浑，还有小石块往下掉。这时候应该怎么做？第一步，看清条件：有三个线索，刚下过大暴雨、山路上有新裂缝、水变浑还掉小石块。第二步，判断这些线索意味着什么：这三点正是滑坡或者泥石流的前兆，山谷又在沟谷里，正是泥石流会经过的路线。第三步，做出选择：马上离开山谷，向垂直于沟谷方向的两侧高处转移，并且大声告诉大人。第四步，说清道理：泥石流会顺着沟谷往下冲，躲在谷里和顺着沟往下跑都很危险；向两侧高处走，才是离开它行进路线的最快办法。",
    "conceptest-1": "现在用三个容易弄错的说法考考你。请仔细读每一个选项，选出你认为正确的那个，然后看解释。",
    "synthesis": "学到这里，请你为班级做一张防灾小卡片。卡片要写清楚三样东西：一种灾害的前兆、对应的预警颜色、以及两到三个正确动作。写完后和同桌交换，互相补充对方漏掉的地方。",
    "posttest": "最后用新的情境检验一下。这次的问题里出现了操场、结冰的河面和楼道，看看你能不能把正确的做法用上去。",
    "summary": "这节课我们弄明白了三件事。第一，地震、洪水、台风、滑坡和泥石流是常见的自然灾害，我国不同地区多发的灾害不一样。第二，灾害来之前常常有前兆，气象和水利用蓝色、黄色、橙色、红色四级预警表示危险程度，红色最高。第三，做对动作能明显减少伤害：地震记住趴下、遮挡、手抓牢；台风关紧门窗、远离窗户；洪水往高处转移、不涉水；滑坡和泥石流往垂直于沟谷的两侧高处跑。回到开头的问题，遇到危险，最重要的不是害怕，而是认得出、躲得对。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出四种常见的自然灾害，并各写一句它们的成因。第二层能力应用，动手做：和家人一起画出家里的避险路线图，标出地震时躲在哪里、火灾时从哪里下楼。第三层迁移挑战，选做：查一查你家乡最常见的自然灾害是哪一种，写出一份三条措施的防灾小方案。",
    "knowledge-graph": "这张图展示了这节课在科学知识网络里的位置。左边是先要学会的知识，右边是可以接着探索的内容，下面是同一领域的伙伴知识。可以点一点，看看还有哪些值得继续研究的问题。",
    "ai-tutor": "如果还有没弄明白的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 四种常见的自然灾害", "lab-1": "实验室一 灾害判断与应对", "module-2": "概念二 防灾减灾的三件实事",
    "lab-2": "实验室二 避险动作演练", "worked-example": "例题讲解 山谷里的选择", "conceptest-1": "概念测试",
    "synthesis": "综合任务 防灾小卡片", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 五个情境判断（每个情境三个做法，只有一个是正确的）
DCASES = [
    {
        "q": "课堂上，教室突然摇晃起来，头顶的电灯也在晃。",
        "opts": [
            ("蹲下，躲到课桌下面，用手护住头和脖子，等震动停下再听老师指挥撤离", True,
             "做对了。先就近躲到结实的课桌下，护住头颈，等震动停下来再有序撤离，这是教室里最稳妥的做法。"),
            ("马上冲出教室，从楼梯跑下楼", False,
             "错因提醒：震动最厉害的时候冲楼梯、挤楼道最危险，容易被掉落的东西砸到，也容易摔倒。正确做法是先就近躲避，震动停下来以后再有序撤离。"),
            ("从窗户跳下去，越快越好", False,
             "错因提醒：不要把跳窗当成更快的办法。玻璃可能正在碎裂，跳下去极易受伤。正确做法是远离窗户，躲到结实的课桌下面。"),
        ],
    },
    {
        "q": "暴雨过后，山路上出现了一条新裂缝，路边泉水变浑浊，还有小石块往下掉。",
        "opts": [
            ("立刻离开沟谷和陡坡，向垂直于沟谷的两侧高处转移，并马上告诉大人", True,
             "做对了。裂缝、浑水、掉石块都是滑坡或泥石流的前兆，向两侧高处走，能最快离开它的行进路线。"),
            ("站在原地拍照，记录下这个现象再说", False,
             "错因提醒：这些现象正是滑坡或泥石流的前兆，停留观察等于把自己留在危险区。正确做法是马上离开沟谷，向两侧高处转移并报告大人。"),
            ("顺着山谷往下跑，快点离开这里", False,
             "错因提醒：误认为往下跑能更快脱离。滑坡和泥石流正是顺着沟谷往下冲的，顺沟跑反而走进它的路线。正确做法是向垂直于沟谷方向的两侧高处跑。"),
        ],
    },
    {
        "q": "台风登陆，家里的窗户被风吹得哐哐响。",
        "opts": [
            ("关紧门窗，远离窗户，待在屋里最里面、结构最结实的房间", True,
             "做对了。关紧门窗能挡住风雨，远离窗户能避开破碎的玻璃，待在里面的房间更安全。"),
            ("打开窗户让风对流，减小风力", False,
             "错因提醒：不要把开窗当成泄压的办法。强风灌进屋里，玻璃和屋内的物品更容易被吹坏伤人。正确做法是关紧门窗，远离窗户。"),
            ("出门看看风雨到底有多大", False,
             "错因提醒：台风期间室外最危险，被吹落的广告牌、树枝和飞来的杂物都可能伤人。正确做法是留在室内，等预警解除再外出。"),
        ],
    },
    {
        "q": "洪水已经漫到小腿，水流有点急，你要去对面的高处。",
        "opts": [
            ("先就近往地势高的地方转移，走稳、结伴，绕开河道和低洼地", True,
             "做对了。往高处走、绕开河道和低洼地，是最安全的路线；结伴同行还能互相照应。"),
            ("直接涉水走过去，水看起来很浅", False,
             "错因提醒：不要以为水浅就没关系。水到膝盖就可能把人冲倒，水下还可能藏着坑和没有盖子的井。正确做法是绕开水流，往高处转移。"),
            ("躲进地下室，等水退下去", False,
             "错因提醒：地下室是最容易被灌水的地方，躲进去等于把自己关在最低处。正确做法是往楼上或者地势高的地方去。"),
        ],
    },
    {
        "q": "手机收到暴雨红色预警，外面的雨非常大。",
        "opts": [
            ("留在安全的室内，暂缓外出，先联系家长，等学校通知", True,
             "做对了。红色预警是最高级别，留在安全的室内、先联系家长，是这个时候最稳妥的选择。"),
            ("照常出门上学，不能迟到", False,
             "错因提醒：红色预警不是普通提醒，它说明危险已经迫近，路上可能积水或者有落石。正确做法是留在室内等通知，不要冒险出门。"),
            ("约同学一起去河边看看水有多大", False,
             "错因提醒：把预警当成看热闹的机会很危险，河边和桥上是洪水最要命的地方。正确做法是远离河道和低洼地带。"),
        ],
    },
]

# 避险动作演练场景（内联 SVG 示意图 + 要点）
SCENES = [
    {
        "t": "教室里遇到地震",
        "svg": '''<svg viewBox="0 0 320 150" role="img" aria-label="教室里蹲在课桌下护住头颈的示意图" style="width:100%;height:auto;display:block">
  <rect x="0" y="0" width="320" height="150" fill="#fdf8ec"/>
  <line x1="0" y1="128" x2="320" y2="128" stroke="#c9a46a" stroke-width="3"/>
  <rect x="78" y="58" width="164" height="9" rx="4" fill="#8d6a3f"/>
  <rect x="86" y="67" width="9" height="61" fill="#8d6a3f"/>
  <rect x="225" y="67" width="9" height="61" fill="#8d6a3f"/>
  <circle cx="160" cy="90" r="13" fill="#ffd166" stroke="#b07d12" stroke-width="2"/>
  <path d="M152 120 Q160 100 168 120 Z" fill="#4ecdc4" stroke="#14897f" stroke-width="2"/>
  <path d="M148 96 Q160 80 172 96" fill="none" stroke="#e05555" stroke-width="4" stroke-linecap="round"/>
  <text x="160" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#e05555">蹲下 · 遮挡 · 手抓牢</text>
  <text x="160" y="145" text-anchor="middle" font-size="13" fill="#94866c">躲在结实的课桌下，护住头和脖子</text>
</svg>''',
        "pts": ["趴下：蹲低身体，降低重心，别站着。",
                "遮挡：躲到结实的课桌下，用手或书包护住头和脖子。",
                "手抓牢：抓住桌腿，别让桌子晃走；震动停下再听老师指挥有序撤离。"],
    },
    {
        "t": "室外遇到地震",
        "svg": '''<svg viewBox="0 0 320 150" role="img" aria-label="在室外空旷地蹲下抱头的示意图" style="width:100%;height:auto;display:block">
  <rect x="0" y="0" width="320" height="150" fill="#fdf8ec"/>
  <line x1="0" y1="128" x2="320" y2="128" stroke="#c9a46a" stroke-width="3"/>
  <rect x="236" y="52" width="60" height="76" fill="#d8d2c4" stroke="#94866c" stroke-width="2"/>
  <line x1="240" y1="56" x2="292" y2="124" stroke="#e05555" stroke-width="3"/>
  <line x1="292" y1="56" x2="240" y2="124" stroke="#e05555" stroke-width="3"/>
  <circle cx="112" cy="88" r="13" fill="#ffd166" stroke="#b07d12" stroke-width="2"/>
  <path d="M104 120 Q112 98 120 120 Z" fill="#4ecdc4" stroke="#14897f" stroke-width="2"/>
  <path d="M100 94 Q112 78 124 94" fill="none" stroke="#e05555" stroke-width="4" stroke-linecap="round"/>
  <text x="150" y="30" text-anchor="middle" font-size="17" font-weight="700" fill="#e05555">跑到空旷地，蹲下抱头</text>
  <text x="150" y="145" text-anchor="middle" font-size="13" fill="#94866c">远离楼房、大树和电线杆</text>
</svg>''',
        "pts": ["马上跑到空旷的地方，远离楼房、大树、广告牌和电线杆。",
                "蹲下身体，双手护住头和脖子，不要乱跑。",
                "不要在狭窄的巷子里停留，也不要靠近玻璃幕墙。"],
    },
    {
        "t": "家里遇到台风",
        "svg": '''<svg viewBox="0 0 320 150" role="img" aria-label="台风天关紧门窗远离窗户的示意图" style="width:100%;height:auto;display:block">
  <rect x="0" y="0" width="320" height="150" fill="#fdf8ec"/>
  <line x1="0" y1="128" x2="320" y2="128" stroke="#c9a46a" stroke-width="3"/>
  <rect x="196" y="30" width="98" height="72" fill="#dceaf7" stroke="#7fa8c9" stroke-width="3"/>
  <line x1="196" y1="30" x2="294" y2="102" stroke="#7fa8c9" stroke-width="2"/>
  <line x1="294" y1="30" x2="196" y2="102" stroke="#7fa8c9" stroke-width="2"/>
  <line x1="245" y1="30" x2="245" y2="102" stroke="#7fa8c9" stroke-width="2"/>
  <line x1="196" y1="66" x2="294" y2="66" stroke="#7fa8c9" stroke-width="2"/>
  <circle cx="88" cy="86" r="13" fill="#ffd166" stroke="#b07d12" stroke-width="2"/>
  <path d="M78 124 Q88 94 98 124 Z" fill="#4ecdc4" stroke="#14897f" stroke-width="2"/>
  <text x="92" y="34" text-anchor="middle" font-size="17" font-weight="700" fill="#e05555">关紧门窗，远离窗户</text>
  <text x="160" y="145" text-anchor="middle" font-size="13" fill="#94866c">待在屋里最里面的房间，等预警解除</text>
</svg>''',
        "pts": ["提前关紧门窗，把阳台上的花盆等物品收进屋里。",
                "台风期间远离窗户和玻璃门，待在屋里最里面、结构结实的房间。",
                "不要出门看风雨，等预警解除以后再外出。"],
    },
    {
        "t": "山区遇到滑坡、泥石流",
        "svg": '''<svg viewBox="0 0 320 150" role="img" aria-label="向垂直于沟谷方向的两侧高处转移的示意图" style="width:100%;height:auto;display:block">
  <rect x="0" y="0" width="320" height="150" fill="#fdf8ec"/>
  <path d="M0 128 L110 44 L160 128 L210 44 L320 128 Z" fill="#e6dcc4" stroke="#b09060" stroke-width="2"/>
  <line x1="160" y1="128" x2="160" y2="60" stroke="#7fa8c9" stroke-width="6" stroke-dasharray="10 7"/>
  <path d="M118 96 L84 66" stroke="#22c55e" stroke-width="5" stroke-linecap="round"/>
  <path d="M84 66 l14 2 l-4 -14 z" fill="#22c55e"/>
  <path d="M202 96 L236 66" stroke="#22c55e" stroke-width="5" stroke-linecap="round"/>
  <path d="M236 66 l-14 2 l4 -14 z" fill="#22c55e"/>
  <circle cx="160" cy="112" r="11" fill="#ffd166" stroke="#b07d12" stroke-width="2"/>
  <text x="160" y="24" text-anchor="middle" font-size="17" font-weight="700" fill="#e05555">向两侧高处跑，别顺沟跑</text>
  <text x="160" y="145" text-anchor="middle" font-size="13" fill="#94866c">绿色箭头是安全方向，蓝色虚线是泥石流的路线</text>
</svg>''',
        "pts": ["发现裂缝、浑水、掉石块，马上离开沟谷和陡坡，并大声告诉大人。",
                "往垂直于沟谷方向的两侧高处跑，不要顺着沟往下跑。",
                "不要躲在沟里的大石头后面，也不要停留在桥洞、涵洞里。"],
    },
    {
        "t": "遇到洪水",
        "svg": '''<svg viewBox="0 0 320 150" role="img" aria-label="洪水时向楼上高处转移的示意图" style="width:100%;height:auto;display:block">
  <rect x="0" y="0" width="320" height="150" fill="#fdf8ec"/>
  <rect x="182" y="42" width="118" height="86" fill="#f3ece0" stroke="#b09060" stroke-width="2"/>
  <rect x="196" y="58" width="34" height="24" fill="#dceaf7" stroke="#7fa8c9" stroke-width="2"/>
  <rect x="252" y="58" width="34" height="24" fill="#dceaf7" stroke="#7fa8c9" stroke-width="2"/>
  <rect x="196" y="94" width="34" height="24" fill="#dceaf7" stroke="#7fa8c9" stroke-width="2"/>
  <rect x="252" y="94" width="34" height="24" fill="#dceaf7" stroke="#7fa8c9" stroke-width="2"/>
  <path d="M0 112 Q40 100 80 112 T160 112 L160 150 L0 150 Z" fill="#9fd0ea" opacity=".85"/>
  <circle cx="96" cy="72" r="12" fill="#ffd166" stroke="#b07d12" stroke-width="2"/>
  <path d="M86 110 Q96 84 106 110 Z" fill="#4ecdc4" stroke="#14897f" stroke-width="2"/>
  <path d="M108 96 L172 62" stroke="#22c55e" stroke-width="5" stroke-linecap="round"/>
  <path d="M172 62 l-15 2 l5 -14 z" fill="#22c55e"/>
  <text x="150" y="26" text-anchor="middle" font-size="17" font-weight="700" fill="#e05555">往高处转移，不涉水</text>
  <text x="160" y="145" text-anchor="middle" font-size="13" fill="#94866c">水到膝盖就能把人冲倒，绕开水流走高处</text>
</svg>''',
        "pts": ["就近向楼上或者地势高的地方转移，走稳、结伴。",
                "不要涉水过河、不要在积水的路上走，水下可能有坑或者没有盖子的井。",
                "不要躲进地下室，洪水会往低处灌；远离河道和桥洞。"],
    },
]

CUSTOM_JS = r"""
/* ============================================================
   sci-e-natural-disasters 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 灾害判断与应对：五个情境，逐题作答并给出错因与正确做法
   3) 避险动作演练：切换场景，查看示意图与要点
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

  /* ---------- 2. 灾害判断与应对 ---------- */
  var wrap = document.getElementById('dcase-wrap');
  if (wrap) {
    var blocks = Array.prototype.slice.call(wrap.querySelectorAll('[data-dcase]'));
    var cur = 0;
    var progress = document.getElementById('dcase-progress');
    var prev = document.getElementById('dcase-prev');
    var next = document.getElementById('dcase-next');

    function showCase(i) {
      cur = Math.max(0, Math.min(blocks.length - 1, i));
      blocks.forEach(function (b, k) { b.style.display = (k === cur) ? 'block' : 'none'; });
      progress.className = 'result warn';
      progress.textContent = '情境 ' + (cur + 1) + ' / ' + blocks.length +
        '　先选出你的做法，再点「下一个情境」。';
      prev.disabled = (cur === 0);
      next.disabled = (cur === blocks.length - 1);
    }

    blocks.forEach(function (block) {
      var out = block.querySelector('[data-dout]');
      var picked = false;
      block.querySelectorAll('.choice').forEach(function (btn) {
        btn.addEventListener('click', function () {
          if (picked) return;
          picked = true;
          var ok = btn.dataset.ok === '1';
          btn.classList.add(ok ? 'correct' : 'wrong');
          block.querySelectorAll('.choice').forEach(function (b) {
            if (b.dataset.ok === '1') b.classList.add('correct');
            b.disabled = true;
          });
          out.style.display = 'block';
          out.className = 'result' + (ok ? '' : ' error');
          out.innerHTML = btn.dataset.fb;
        });
      });
    });

    prev.addEventListener('click', function () { showCase(cur - 1); });
    next.addEventListener('click', function () { showCase(cur + 1); });
    showCase(0);
  }

  /* ---------- 3. 避险动作演练 ---------- */
  var drillWrap = document.getElementById('drill-wrap');
  if (drillWrap) {
    var panels = Array.prototype.slice.call(drillWrap.querySelectorAll('[data-drill]'));
    function showDrill(key) {
      panels.forEach(function (p) { p.style.display = (p.dataset.drill === key) ? 'block' : 'none'; });
      document.querySelectorAll('[data-scene]').forEach(function (b) {
        b.classList.toggle('selected', b.dataset.scene === key);
      });
    }
    document.querySelectorAll('[data-scene]').forEach(function (b) {
      b.addEventListener('click', function () { showDrill(b.dataset.scene); });
    });
    showDrill(panels[0].dataset.drill);
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：危险来了，你会怎么做？", TTS["pretest"], [
        {"q": "下面哪一组都属于自然灾害？",
         "options": [("地震、洪水、台风、滑坡", True),
                     ("乱扔垃圾、噪音、堵车", False),
                     ("停电、漏水、摔跤", False)],
         "explain": "自然灾害是由自然原因引起、并对人的生命财产造成危害的现象。<strong>错因提醒：</strong>不要把人为原因造成的事故和自然灾害搞混。"},
        {"q": "课堂上突然发生地震，最正确的第一反应是：",
         "options": [("蹲下、躲到课桌下、用手护住头和脖子", True),
                     ("马上冲出教室跑下楼", False),
                     ("站在窗边看看外面怎么了", False)],
         "explain": "震动最厉害的时候，先就近躲避、护住头颈最安全。<strong>错因提醒：</strong>常见错误是误认为跑得越快越好，其实这时冲楼梯、挤楼道和靠近窗户都更危险。"},
        {"q": "气象台发布暴雨红色预警，这个颜色表示：",
         "options": [("危险程度最高，要马上按提示行动", True),
                     ("只表示雨会下得比较久", False),
                     ("是所有预警里最轻的一级", False)],
         "explain": "预警颜色从低到高是蓝色、黄色、橙色、红色，红色代表危险程度最高。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "地震、洪水、台风、滑坡是常见的四种自然灾害", TTS["module-1"], f'''
        <p style="font-size:17px;margin:0 0 12px">自然灾害是指由自然原因引起、并对人的生命和财产造成危害的现象。小学阶段我们重点认识下面四种。</p>
        <div class="grid grid-2">
          <div class="inner-card">
            <p><strong>🌐 地震</strong></p>
            <p style="color:var(--muted)">大地突然震动，房屋可能开裂甚至倒塌，多发生在板块交界的地方。</p>
          </div>
          <div class="inner-card">
            <p><strong>🌊 洪水</strong></p>
            <p style="color:var(--muted)">暴雨或者连续降雨让河水猛涨，淹掉地势低洼的地方。</p>
          </div>
          <div class="inner-card">
            <p><strong>🌀 台风</strong></p>
            <p style="color:var(--muted)">从海上来的强烈风暴，带着狂风和暴雨，主要影响我国东南沿海。</p>
          </div>
          <div class="inner-card">
            <p><strong>⛰️ 滑坡、泥石流</strong></p>
            <p style="color:var(--muted)">山坡上大量泥土和石头突然滑下来，常出现在山区连下暴雨的时候。</p>
          </div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="我国常见自然灾害分类与多发地区示意图，标注地震、洪水、台风、滑坡泥石流">
          <figcaption>我国不同地区多发的灾害不一样：东南沿海多台风，长江中下游多洪水，西南山区多滑坡泥石流</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🗺️</span><div><strong>记住一句话：</strong>灾害有它的「脾气」和「地盘」——知道家乡容易发生哪一种，就能提前做哪一种准备。</div></div>
        <div class="kid-note"><span class="emoji">🤔</span><div><strong>为什么要学这一课？</strong>灾害的力量我们改变不了，但认得出、躲得对，能实实在在减少伤害。这就是我们要学它的理由。</div></div>
{insight_box([
    {"lens": "看见它", "text": "四种灾害看起来不一样，但有一点相同：它们的力量都远远超过一个人，所以我们不跟它硬碰，而是躲开它。"},
    {"lens": "解释它", "text": "为什么东南沿海多台风、西南山区多滑坡？因为灾害和当地的地形、气候直接相关，这也是不同地区多发灾害不同的原因。"},
    {"lens": "比较它", "text": "台风和洪水都和水有关，但台风从海上来、带着狂风，洪水多由河水上涨造成，应对方法也不一样。"},
])}
    ''', tag="概念一"))

    blocks_html = []
    for i, c in enumerate(DCASES):
        opts = "\n".join(
            f'''              <button class="choice" data-ok="{"1" if ok else "0"}" data-fb="{fb}">{txt}</button>'''
            for (txt, ok, fb) in c["opts"]
        )
        blocks_html.append(f'''          <div class="inner-card" data-dcase="{i}" style="display:{"block" if i == 0 else "none"}">
            <p><strong>情境 {i + 1}：{c["q"]}</strong></p>
            <div class="grid" style="margin-top:10px">
{opts}
            </div>
            <p class="result warn" data-dout="{i}" style="display:none;margin-top:10px"></p>
          </div>''')
    cases_html = "\n".join(blocks_html)
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "灾害判断与应对：五道情境题，选一个做法", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">每题只选一个做法。选完会立刻告诉你哪里对、哪里错，还会说清正确做法。</p>
        <div class="lab-panel">
          <div id="dcase-wrap">
{cases_html}
          </div>
          <div class="flex-row">
            <button class="choice" id="dcase-prev" style="text-align:center">上一个情境</button>
            <button class="choice" id="dcase-next" style="text-align:center">下一个情境</button>
          </div>
          <p class="result warn" id="dcase-progress" style="margin-top:12px"></p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">✅</span><div><strong>做完五题，你会发现一条共同规律：</strong>先躲开危险，再找安全的地方，最后才考虑往外走。慌乱中做反了顺序，才是最危险的。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "认识前兆、看懂预警、做对动作，伤害就能减少", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">防灾减灾就三件实事：<strong>认识前兆</strong>、<strong>看懂预警</strong>、<strong>做对动作</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>认识前兆：</strong>暴雨后山路出现新裂缝、泉水突然变浑、小石块不断掉落，都是滑坡和泥石流的前兆。</div></div>
          <div class="step"><span class="n">2</span><div><strong>看懂预警：</strong>颜色由低到高是蓝、黄、橙、红，红色最危险。收到预警要按提示行动，不是看热闹。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>做对动作：</strong>地震记口诀「趴下、遮挡、手抓牢」；台风关紧门窗远离窗户；洪水往高处走、不涉水；滑坡向两侧高处跑。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="不同场景下正确避险动作示意图，标注蹲下护头、往高处转移、远离窗户">
          <figcaption>四个关键动作：蹲下护头颈、往高处转移、远离窗户、向垂直于沟谷的两侧跑</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">误认为遇到灾害「跑得越快越好」。地震时第一时间冲楼梯、洪水时涉水抄近路、滑坡时顺着沟往下跑，都是把危险放大的常见错误。正确顺序是：<strong>先躲开、再找安全处、最后才往外走</strong>。</p>
        </div>
    ''', tag="概念二"))

    scene_btns = "\n".join(
        f'''            <button class="choice{ " selected" if i == 0 else ""}" data-scene="{i}" style="text-align:center;font-size:14px">{s["t"]}</button>'''
        for i, s in enumerate(SCENES)
    )
    drill_panels = []
    for i, s in enumerate(SCENES):
        pts = "\n".join(f'              <li>{p}</li>' for p in s["pts"])
        drill_panels.append(f'''          <div data-drill="{i}" style="display:{"block" if i == 0 else "none"}">
            <div style="border:1px solid var(--line-subtle);border-radius:14px;overflow:hidden">{s["svg"]}</div>
            <ul class="objectives" style="margin-top:10px">
{pts}
            </ul>
          </div>''')
    drill_html = "\n".join(drill_panels)
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "避险动作演练：跟着图把姿势做一遍", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">点一个场景，看正确的姿势示意图和三条要点，然后自己跟着做一遍。</p>
        <div class="lab-panel">
          <div class="grid grid-2" style="margin-bottom:12px">
{scene_btns}
          </div>
          <div id="drill-wrap">
{drill_html}
          </div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🤝</span><div><strong>互相检查：</strong>两人一组，一人做动作，一人对照要点打分。动作做对了，关键时刻才用得上。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：山谷里遇到暴雨，先做什么", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>暑假里几个同学在山里玩，下了一场大暴雨，他们躲进山谷里的小亭子。雨停后，山路出现一条新裂缝，旁边水沟里水很浑，还有小石块往下掉。这时应该怎么做？请说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>看清条件：</strong>刚下过大暴雨；山路有新裂缝；水变浑，还掉小石块。</div></div>
          <div class="step"><span class="n">2</span><div><strong>读出线索的意思：</strong>这三点正是滑坡或泥石流的前兆，而山谷恰好在泥石流会经过的路线上。</div></div>
          <div class="step"><span class="n">3</span><div><strong>做出选择：</strong>马上离开山谷，向垂直于沟谷方向的两侧高处转移，并大声告诉大人。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>说清道理：</strong>泥石流顺着沟谷往下冲，留在谷里或者顺沟往下跑都很危险；向两侧高处走，能最快离开它的路线。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错法</span>
          <p style="margin:6px 0 0">一看到下雨就往谷里的亭子躲，或者想着「顺着沟快点跑出去」，是这道题最常见的错误。请记住这句口诀：<strong>不顺着沟跑，往两侧高处跑</strong>。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：找出藏在说法里的错误", TTS["conceptest-1"], [
        {"q": "下面哪句话是正确的？",
         "options": [("我国不同地区多发的灾害不一样，东南沿海多台风", True),
                     ("全国每个地方都同样容易发生台风", False),
                     ("山区不会发生洪水", False)],
         "explain": "灾害和当地的地形、气候有关，所以不同地区多发的灾害不同。<strong>错因提醒：</strong>常见错误是把某一种灾害当成全国到处都一样，忽略了地区差异。"},
        {"q": "关于预警颜色，下面说法正确的是：",
         "options": [("蓝、黄、橙、红四级，红色代表危险程度最高", True),
                     ("红色是最轻的一级", False),
                     ("颜色只是好看，和危险程度无关", False)],
         "explain": "颜色从低到高是蓝、黄、橙、红。<strong>错因提醒：</strong>容易误认为预警只是普通提醒，其实颜色越深，越需要马上按提示行动。"},
        {"q": "滑坡、泥石流来了，应该往哪个方向跑？",
         "options": [("垂直于沟谷方向的两侧高处", True),
                     ("顺着沟谷往下跑", False),
                     ("躲到沟里的大石头后面", False)],
         "explain": "泥石流顺着沟谷往下冲，向两侧高处跑能最快离开它的路线。<strong>错因提醒：</strong>把「顺着沟跑得快」当成好办法，是这一课最危险的常见错误。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：做一张班级防灾小卡片", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">选一种你最想弄清楚的灾害，为班级做一张防灾小卡片。</p>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>卡片必须写清三样：</strong>这种灾害的前兆 · 对应的预警颜色 · 两到三个正确动作</p>
        </div>
        <div class="inner-card">
          <p><strong>我选的灾害是：</strong></p>
          <textarea id="syn-type" rows="2" placeholder="例如：山区暴雨后的滑坡和泥石流"></textarea>
        </div>
        <div class="inner-card">
          <p><strong>卡片内容（前兆 / 预警 / 动作）</strong></p>
          <textarea id="syn-answer" rows="5" placeholder="前兆：……　预警：……　正确动作：……"></textarea>
        </div>
        <div class="kid-note"><span class="emoji">🔁</span><div>写完后和同桌交换卡片，互相补充对方漏掉的地方，再把补充后的版本读一遍。</div></div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换个情境，规律还在不在", TTS["posttest"], [
        {"q": "在操场上上课时突然发生地震，最正确的做法是：",
         "options": [("跑到空旷处蹲下，护住头颈，远离楼房和电线杆", True),
                     ("马上跑回教学楼里躲到桌子下面", False),
                     ("站在原地不动，等老师安排", False)],
         "explain": "操场上空间开阔，就近跑到空旷处蹲下护头最安全。<strong>错因提醒：</strong>不要误认为楼里更安全，这时往楼里跑，反而会靠近可能掉落的东西。"},
        {"q": "冬天湖面结了冰，有同学想去冰上走一走。最合理的做法是：",
         "options": [("不去，冰层厚薄不均，掉进冰水里非常危险", True),
                     ("先踩一只脚试试，不裂就继续走", False),
                     ("叫上几个人一起去，人多更安全", False)],
         "explain": "冰面情况看不出来，人多反而增加压塌的风险。远离危险区域是防灾的第一步。"},
        {"q": "教学楼里突然闻到焦味，走廊有烟。最正确的做法是：",
         "options": [("弯腰低姿、用湿毛巾捂住口鼻，按疏散路线有序下楼到操场", True),
                     ("坐电梯快点下楼", False),
                     ("躲进教室角落等别人来", False)],
         "explain": "火灾时应走疏散楼梯，弯腰低姿减少吸入烟雾。<strong>错因提醒：</strong>不要误认为电梯更快，着火时电梯可能停运或者断电。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把自己讲明白", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>认识它</strong>：地震、洪水、台风、滑坡和泥石流是常见的自然灾害，不同地区多发的不一样。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>预防它</strong>：记住前兆（裂缝、浑水、掉石块），看懂预警（蓝黄橙红，红色最高），提前做家庭避险路线图。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>应对它</strong>：地震「趴下、遮挡、手抓牢」；台风远离窗户；洪水往高处走、不涉水；滑坡向两侧高处跑。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头的问题：</strong>遇到危险，最重要的不是害怕，而是认得出、躲得对。灾害的力量我们改变不了，但正确的知识和动作，能实实在在减少伤害。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「前兆、预警、动作」这三个词，把一种灾害的防灾办法讲给家人听。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层练习，按自己的节奏来", TTS["homework"], [
        [
            "写出地震、洪水、台风、滑坡四种常见自然灾害，并各写一句它们的成因。",
            "写出预警颜色的四个等级，并说清哪一种最危险。",
            "判断对错并说明理由：滑坡、泥石流来了，应该顺着沟谷往下跑。",
        ],
        [
            "和家人一起画出家里的避险路线图：标出地震时躲在哪里、着火时从哪里下楼、在哪里集合，贴在家里显眼的地方。",
            "把课件里的五个情境讲给家人听，请他们各选一个做法，再一起对答案。",
        ],
        [
            "查一查你家乡最常见的自然灾害是哪一种，写出一份三条措施的防灾小方案，并说明每条措施挡住的危险是什么。",
            "为低年级同学设计一张防灾提示卡：只用图和不超过十个字，让他们一眼就看懂该怎么做。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "sci-e-natural-disasters",
    "node_id": "sci-e-natural-disasters",
    "title": "自然灾害与防灾减灾：遇到危险怎么办",
    "name_en": "Natural Disasters: What should we do when danger comes?",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "earth-space-science",
    "domain_cn": "地球与宇宙科学 · 人类活动与环境",
    "lesson_type": "concept-inquiry",
    "version": "1.0.0",
    "description": "以认识它、预防它、应对它为主线，认识四种常见自然灾害与我国区域差异，通过五道情境判断题和五个避险动作演练，把前兆识别、预警认读与正确动作变成学生能真正做出来的能力。",
    "tags": ["自然灾害", "防灾减灾", "地震避险", "洪水", "台风", "滑坡泥石流", "预警信号"],
    "standard_ref": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念11「人类活动与环境」学习内容11.2 自然灾害——5～6年级知道自然灾害对人类的影响和防灾减灾常识。",
    "hero_question": "地震、洪水、台风来的时候，我们第一时间该做什么？",
    "hero_alt": "自然灾害与防灾减灾知识结构图：认识灾害、看懂预警、做对动作",
    "hero_caption": "认识它：四种常见自然灾害 · 预防它：前兆与预警 · 应对它：正确避险动作",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正关心的问题，后面的判断和演练都会围着它转。",
    "anchor_choices": [
        {"t": "我们国家哪些地方容易发生哪几种灾害？", "d": "想知道家乡要重点防什么", "v": "我们国家哪些地方容易发生哪几种灾害"},
        {"t": "灾害来之前有什么前兆？", "d": "想早点发现危险的信号", "v": "灾害来之前有什么前兆"},
        {"t": "预警信息的颜色是什么意思？", "d": "想看懂蓝黄橙红分别代表什么", "v": "预警信息的颜色是什么意思"},
        {"t": "关键时刻该做什么动作？", "d": "想学会几个能保护自己的姿势", "v": "关键时刻该做什么动作"},
    ],
    "objectives": [
        "能说出地震、洪水、台风、滑坡和泥石流四种常见自然灾害，并各举一个例子",
        "能说出我国不同地区多发的灾害不一样，并举例说明",
        "能说出几种灾害前兆，知道预警信息分红、橙、黄、蓝四级且红色最高",
        "能说出并做出几种正确的避险动作，知道在什么情况下该怎么做",
    ],
    "objectives_plain": [
        "能说出地震、洪水、台风、滑坡和泥石流四种常见自然灾害，并各举一个例子",
        "能说出我国不同地区多发的灾害不一样，并举例说明",
        "能说出几种灾害前兆，知道预警信息分红、橙、黄、蓝四级且红色最高",
        "能说出并做出几种正确的避险动作，知道在什么情况下该怎么做",
    ],
    "standards": [
        {"content": "知道自然灾害对人类的影响，知道常见的自然灾害类型及其成因",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学科核心概念11 人类活动与环境（5～6年级）"},
        {"content": "知道防灾减灾常识，能说出并做出正确的避险动作，会看预警信息",
         "source": "《义务教育科学课程标准（2022年版2025年修订）》学习内容11.2 自然灾害（5～6年级）"},
    ],
    "prereqs": ["sci-e-earth-surface-change"],
    "prereqs_name": "地球表面的变化",
    "prereqs_meta": "sci-e-earth-surface-change",
    "leads_to": ["sci-e-environment-protection"],
    "next_meta": "sci-e-environment-protection",
    "section_images": ["assets/sci-e-natural-disasters-fig1.webp", "assets/sci-e-natural-disasters-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "遇到灾害，最重要的不是害怕，而是认得出、躲得对。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己判断危险来了该怎么做。",
        "objectives": "看清四件事：说出四种灾害、说出地区差异、认识前兆与预警、做出正确动作。",
        "pretest": "凭直觉选就好，错了不扣分——前测是帮你看清自己现在站在哪里。",
        "module-1": "地震、洪水、台风、滑坡各有各的脾气，也各有各的地盘。",
        "lab-1": "五个情境只选一个做法，选完立刻看清错在哪里、正确做法是什么。",
        "module-2": "认识前兆、看懂预警、做对动作——防灾减灾就这三件实事。",
        "lab-2": "点场景，看示意图，然后自己跟着把姿势做一遍。",
        "worked-example": "四步走：看清条件、读出线索、做出选择、说清道理。",
        "conceptest-1": "干扰项里藏着最危险的那几个错误想法，选完看清每一个解释。",
        "synthesis": "卡片要写清前兆、预警和动作三样，才叫能用的防灾卡。",
        "posttest": "换了操场、冰面和楼道的新情境，看看你还能不能判断准确。",
        "summary": "用「认识它、预防它、应对它」三句话，把防灾办法讲清楚。",
        "homework": "三层练习，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先诊断你的卡点，再给最小提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是「人类活动与环境」在学习内容11.2 自然灾害上的空缺。这类内容容易滑向渲染灾难、制造恐慌，设计上明确采用「以文字和示意图呈现事实、不呈现伤亡影像」的处理方式，把落点放在认识—预防—正确应对三件事上：用五道情境判断题把常见的错误做法（往楼上冲、顺沟跑、涉水抄近路）逐一纠正，用五个避险动作演练把知识变成身体记忆，最后落到家庭避险路线图与家乡防灾小方案。",
    "plan_table": """| 1 | cover | 自然灾害与防灾减灾：遇到危险怎么办 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：危险来了，你会怎么做？ | 起·前测（暴露直觉） |
| 5 | concept | 地震、洪水、台风、滑坡是常见的四种自然灾害 | 承·概念一（类型与地区差异） |
| 6 | interactive | 灾害判断与应对：五道情境题，选一个做法 | 承·实验室一（情境判断） |
| 7 | concept | 认识前兆、看懂预警、做对动作，伤害就能减少 | 承·概念二（防灾三件实事） |
| 8 | interactive | 避险动作演练：跟着图把姿势做一遍 | 承·实验室二（动作演练） |
| 9 | concept | 例题示范：山谷里遇到暴雨，先做什么 | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：找出藏在说法里的错误 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：做一张班级防灾小卡片 | 合·迁移应用 |
| 12 | quiz | 后测：换个情境，规律还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把自己讲明白 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层练习，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：认识灾害 / 看懂预警 / 做对动作 三栏标注\n- P5 四种常见自然灾害与多发地区示意图（已生成）：地震、洪水、台风、滑坡泥石流中文标注\n- P7 正确避险动作示意图（已生成）：蹲下护头、往高处转移、远离窗户、向两侧跑\n- 若需补充：中国气象局预警信号颜色对照图、本地应急避难场所位置图",
}
