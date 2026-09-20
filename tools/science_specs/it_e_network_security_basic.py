# -*- coding: utf-8 -*-
"""小学信息科技 · 网络安全与信息保护（G5）—— 补齐知识树「互联网与人工智能」空缺

学科语气：信息科技 = 概念 + 动手并重。
本课不背安全口号，只做三件真能上手的事：
  ① 密码强度体检：真的敲一个密码进去 → 强度环实时变化 → 逐条告诉你弱在哪里
  ② 可疑消息鉴别：逐条点开细节 → 判断"正常还是可疑" → 里面故意留了一条「看不出问题」的消息
  ③ 保护清单：12 条候选里勾出该写进清单的，检查后得到属于自己的那份清单
最后收口到一句能带走的判断方法：
  催得急、要信息、点链接、要转钱——中一个就停下来核实。
"""

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

F1 = './assets/it-e-network-security-basic-fig1.webp'
F2 = './assets/it-e-network-security-basic-fig2.webp'

TTS = {
    "hero": "先看一条消息。上面写着：学校要核对学籍，请在今晚之前点开链接，填写学生姓名、班级和家长手机号。头像和名字看着就是你们班主任。这条消息很正常吧？可是发消息的那个号，是刚注册的，根本不是老师本人的号。今天这节课，我们只学两件事：第一件，给自己的账号上一把结实的锁；第二件，学会一眼看出一条消息哪里不对劲。学完之后，你会得到一份属于自己的保护清单。",
    "problem-anchor": "开始之前，先选一个你最想弄明白的问题。是想知道密码到底怎么设才算安全，还是想知道怎么分辨一条消息是不是骗人的，又或者你想搞清楚哪些信息属于绝对不能告诉别人的那一档，再或者你只是想给自己写一份照着就能做的保护清单。选好了，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能把个人信息分成三档，知道哪一档绝对不能给出去。第二，能说出密码的强度是由什么决定的，并且能亲手把一个弱密码改成强密码。第三，能用四个破绽去检查一条消息或者一个网址，把它不对劲的地方指出来。第四，能写出一份自己照着做得到的上网保护清单。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选错了也没关系，正好知道该重点听哪里。",
    "module-1": "先说清楚什么是个人信息。凡是能认出你、找到你、冒充你的信息，都算个人信息。它们并不是一样重要的，可以分成三档。第一档是可以公开的，比如你喜欢的颜色、你爱看的书，别人知道了没什么关系。第二档是只给熟人的，比如你是哪个班的、每天走哪条路上学，家里人知道就够了。第三档是绝不外传的，比如密码、验证码、身份证号、家庭住址、家长的银行卡号。这一档里最要紧的是验证码，它就像一把一次性钥匙，谁拿到谁就能进你的账号，所以不管谁问，都不能给。",
    "lab-1": "现在我们给密码做一次体检。下面有一个输入框，你可以随便敲一个密码进去，也可以点旁边的例子直接试试看。右边那根强度环会一边敲一边变。下面还会一条一条告诉你，这个密码到底弱在哪里：是太短了，还是只有数字，还是里面藏了名字和生日这种一眼就能猜到的信息。试够五个，你就明白一个结实的密码长什么样了。",
    "module-2": "再说怎么识破骗人的消息。不管它伪装成什么样，一般逃不过四个破绽。第一个破绽是催得急，它总说只剩几分钟、不办就晚了，因为人一急就来不及想。第二个破绽是要信息，密码、验证码、身份证号，正常办事不会这样跟你要。第三个破绽是让你点链接，那个网址和它嘴上说的对不上。第四个破绽是要你转钱或者扫码，凡是让你先付钱、先充值的，都要立刻停下来问问大人。记住，这四个破绽不用全中，中一个就值得停下来核实。",
    "lab-2": "接下来请你当一次鉴别员。上面会出现一条消息，下面列出它的几个细节，请你一个细节一个细节地点开，判断这一条属于正常还是可疑。要提前提醒你一句：这里面有一条消息，从头发到尾都看不出问题。因为骗子发来的消息，常常就长得很正常。把两轮都判完，你会看到最后的结论。",
    "worked-example": "我们一起把一道题想完整。小明收到三条消息，我们一条一条来判。第一条：同学说，明天考试范围变了，我把资料发你，点这个链接下载。怎么想？先看它要什么，它只要我点链接，没要密码；再看它急不急，明天就考试了，确实有点急；最后看网址，和这个同学平时发的完全不是一个样子。判断出来了：先不点，直接打个电话问问这个同学本人，是不是他发的。这就叫先核实，再动作。",
    "conceptest-1": "接下来用三个容易弄错的说法考考你。请仔细读每一个选项，选完再看解释。",
    "synthesis": "最后一件事交给你。下面有十二条候选说法，请你把该写进保护清单的那些勾出来。勾完点一下检查，每一条都会告诉你为什么该选或者不该选。做完之后，你手上就有一份属于自己的保护清单了。",
    "posttest": "最后一轮，换几个新的情境来考考你。这次会出现一个免费领礼物的网站、一条要验证码的消息，还有一次在公共电脑上的登录。看看你能不能把四个破绽和三个信息档次都用上去。",
    "summary": "这节课我们记住三件事。第一件，个人信息分三档：可以公开的、只给熟人的、绝不外传的。密码和验证码属于最要紧的那一档。第二件，密码要够长、够杂、每个账号都不一样，别拿名字和生日当密码。第三件，识破可疑消息看四个破绽：催得急、要信息、点链接、要转钱。中一个，就先停下来核实。回到开头那条消息——头像像老师，不代表就是老师。先打个电话问一句，比什么都管用。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：把个人信息按三个档次各写两个例子，并说出验证码为什么绝对不能告诉别人。第二层能力应用，动手做：把家里一个账号的弱密码改成强密码，把改之前和改之后的样子记下来，注意不要把真正的密码写在纸上。第三层迁移挑战，选做：和家长一起看一条手机上收到的可疑消息，用四个破绽逐条分析，写成一小段判断，再给家里写一条防骗提醒。",
    "knowledge-graph": "这张图展示了这节课在信息科技知识网络里的位置。左边是学它之前要先会的，右边是学会之后可以接着探索的，下面是同一个领域的伙伴知识。可以点一点，看看还有哪些值得继续学的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 个人信息分三档", "lab-1": "动手一 密码强度体检", "module-2": "概念二 可疑消息四个破绽",
    "lab-2": "动手二 鉴别两条消息", "worked-example": "例题讲解 同学发来的链接", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的保护清单", "posttest": "后测", "summary": "课堂小结", "homework": "作业分层",
    "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# 综合任务：12 条候选说法（good=1 该写进清单 / 0 不该写）
LIST_ITEMS = [
    ("p1", "密码至少 12 位，里面有字母、数字和符号，而且每个账号都不一样", 1,
     "长度和字符种类是密码强度的两条腿，每个账号用不同的密码，一处泄露不会连累其他账号。"),
    ("p2", "验证码只留在自己手机上，不管谁问都不给", 1,
     "验证码是一次性钥匙。客服、老师、同学，谁都不需要你的验证码，开口要的都是骗子。"),
    ("p3", "陌生链接先不点，把网址看一遍再说", 1,
     "网址是骗子最难伪装的地方。多看一遍，很多明显不对劲的地方就露出来了。"),
    ("p4", "说自己中奖了、免费送礼物的消息，直接不理", 1,
     "「免费」和「中奖」是钓人上钩最常用的饵，正规活动不会用陌生消息通知你先交钱。"),
    ("p5", "网上认识的人约见面，一定先告诉家里人", 1,
     "网上认识的人，身份是没法核实的。要见面，必须让家里大人知道并且在旁边。"),
    ("p6", "在公共电脑上登录过账号，走之前一定要退出", 1,
     "不退出，下一个用这台电脑的人打开就是你的账号，等于把账号交给了陌生人。"),
    ("p7", "收到「老师」要资料的消息，先打电话跟老师本人核实", 1,
     "头像和名字都能照抄，唯一靠得住的是你平时就知道的那个电话。"),
    ("p8", "手机和电脑提示更新系统、更新软件，就更新", 1,
     "更新里常常包含安全漏洞的修补。拖着不更新，等于把门留着不关。"),
    ("q1", "把同一个密码用在所有账号上，这样好记", 0,
     "只要有一个网站出了问题，你所有账号就一起被人打开了。好记不能拿这个换。"),
    ("q2", "把密码写在手机备忘录里，顺便写上账号，怕忘", 0,
     "这等于把家里的钥匙和门牌号写在一起。实在记不住，可以用只有自己看得懂的提示词代替。"),
    ("q3", "只要消息是「官方」发来的，就照着做", 0,
     "「官方」两个字谁都能写。要看的不是它自称什么，而是号码、网址这些能核实的东西。"),
    ("q4", "为了不被骗，以后干脆不上网", 0,
     "因噎废食。要学会的是怎么用得更安全，不是把工具扔掉。"),
]

# 动手二：两条消息的细节清单
ROUNDS = [
    {
        "head": "第 1 条消息",
        "from": "发信号码：1069 开头的陌生号码（不是你班主任平时用的号）",
        "text": "【学籍资料核对】家长您好，本学期学籍信息需要核对。请在今晚 22:00 前点击下方链接，填写学生姓名、班级与家长手机号。逾期将影响期末成绩单发放。网址：xx-school-check.top/info",
        "clues": [
            ("发信号码", "是你从没见过的号码，也不知道这个号是谁在用。", "risk",
             "班主任平时用的是固定的那个号。号码对不上，就说明发消息的人至少不是你熟悉的那个。"),
            ("催得急不急", "「今晚 22:00 前」「逾期影响成绩单」，把时间卡得很死。", "risk",
             "真正要紧的事情，学校会提前通知，不会只留几个小时。把人催急，是让人来不及想。"),
            ("要什么信息", "只要姓名、班级、家长手机号，没要密码也没要验证码。", "risk",
             "姓名加手机号，是骗子最想先拿到的东西。靠着这两样，他才好发第二条更逼真的消息。"),
            ("网址对不对", "结尾是 .top，中间还带着 -check 这种词。", "risk",
             "学校的官方网站不会用这种便宜的域名后缀。网址是骗子最难伪装的地方，值得多看两眼。"),
            ("看起来正不正常", "整条消息没有一个错别字，语气很正式，落款还像模像样。", "risk",
             "这一条最容易骗人：没有错别字、语气正式、落款像真的，都是骗子可以刻意做到的。判断可不可信，要看号码和网址，不是看写得像不像。"),
        ],
        "verdict": "这条消息是<strong>可疑的</strong>。它中了四个破绽里的三个——催得急、要信息、给链接。最容易骗过人的地方是：它读起来很正常。安全不安全，不看它写得好不好。",
    },
    {
        "head": "第 2 条消息",
        "from": "发送人：班主任王老师，用的就是平时那个号，消息发在班级群里",
        "text": "明天上午体检，记得空腹来学校。体检表在教室后面自己拿，不用在网上填任何东西，也不用回复任何数字。",
        "clues": [
            ("发送的人", "是班主任平时用的那个号，而且发在大家都熟悉的班级群里。", "safe",
             "号码和群都对得上，这是可以核实的东西，比头像和名字可靠得多。"),
            ("催得急不急", "只说要空腹，没有卡一个很急的时间点。", "safe",
             "通知一件明天的事，用的是正常提前量，没有制造紧张。"),
            ("要什么信息", "什么都没要，还特意说「不用在网上填任何东西」。", "safe",
             "正常通知不会向你索取账号信息。主动说「什么都不用填」，反而是负责的做法。"),
            ("有没有链接", "整条消息一个链接也没有。", "safe",
             "不需要你点任何地方，也就没有把你带到假网站的机会。"),
            ("要做什么", "只让你明天去学校拿体检表，没有任何转钱、扫码、回复数字的要求。", "safe",
             "交代一件事，不涉及钱，也不涉及账号——这两样一出现，就要立刻警惕。"),
        ],
        "verdict": "这条消息是<strong>正常的</strong>。它一个破绽都没中：人是对的、不催、不要信息、没有链接、不涉及钱。<br><span style=\"color:var(--muted)\">和上一条对照着看：不是所有消息都可疑，关键是有没有中那四个破绽。</span>",
    },
]

CUSTOM_JS = r"""
/* ============================================================
   it-e-network-security-basic 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 动手一：密码强度体检（Canvas 强度环 + 逐条弱因诊断）
   3) 动手二：鉴别两条消息（逐条点开细节 → 正常 / 可疑）
   4) 综合任务：我的保护清单（12 条候选勾选 → 检查）
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

  /* ---------- 2. 密码强度体检 ---------- */
  var pwInput = document.getElementById('pw-input');
  if (pwInput) {
    var cv = document.getElementById('pw-gauge');
    var ctx = cv ? cv.getContext('2d') : null;
    var levelEl = document.getElementById('pw-level');
    var scoreEl = document.getElementById('pw-score');
    var lenEl = document.getElementById('pw-len');
    var kindEl = document.getElementById('pw-kind');
    var tipsEl = document.getElementById('pw-tips');

    var WEAK = ['123456', '12345678', '123456789', '111111', '000000', '888888', '666666',
                'abc123', 'qwerty', 'password', 'admin', 'woaini', 'iloveyou', '5201314',
                '123123', 'a123456', 'woaini520', 'abcd1234'];

    function drawGauge(score) {
      if (!ctx) return;
      var w = cv.width, h = cv.height;
      ctx.clearRect(0, 0, w, h);
      var cx = w / 2, cy = 100, r = 58;
      var start = Math.PI * 0.75, sweep = Math.PI * 1.5;
      ctx.lineWidth = 16;
      ctx.lineCap = 'round';
      ctx.strokeStyle = 'rgba(150,140,120,.22)';
      ctx.beginPath(); ctx.arc(cx, cy, r, start, start + sweep); ctx.stroke();
      var p = Math.max(0, Math.min(1, score / 5));
      if (p > 0.001) {
        ctx.strokeStyle = score <= 1 ? '#ef4444' : (score <= 3 ? '#f59e0b' : '#22c55e');
        ctx.beginPath(); ctx.arc(cx, cy, r, start, start + sweep * p); ctx.stroke();
      }
      ctx.fillStyle = 'rgba(150,140,120,.9)';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('弱', cx - r + 4, cy + 34);
      ctx.fillText('强', cx + r - 4, cy + 34);
    }

    function evaluate(pw) {
      if (!pw) {
        return { score: 0, level: '—', kinds: 0, tips: ['还没有输入。在框里敲一个密码，或者点下面的例子试试看。'] };
      }
      var score = 0;
      var tips = [];
      var n = pw.length;

      if (n < 8) {
        tips.push('<strong>太短了。</strong>只有 ' + n + ' 位。长度是密码最有用的一条——每多一位，别人要试的次数就会翻好几倍。至少 12 位才比较稳。');
      } else if (n < 12) {
        score += 1;
        tips.push('<strong>长度还行。</strong>' + n + ' 位，再长一点会更结实。');
      } else {
        score += 2;
        tips.push('<strong>长度很好。</strong>' + n + ' 位，这一条你已经拿到了。');
      }

      var kinds = 0;
      if (/[a-z]/.test(pw)) kinds++;
      if (/[A-Z]/.test(pw)) kinds++;
      if (/[0-9]/.test(pw)) kinds++;
      if (/[^A-Za-z0-9]/.test(pw)) kinds++;
      if (kinds >= 3) {
        score += 2;
        tips.push('<strong>字符种类够杂。</strong>字母、数字、符号混着用，一共用了 ' + kinds + ' 类，别人更难猜。');
      } else if (kinds === 2) {
        score += 1;
        tips.push('<strong>种类还差一点。</strong>只用了 ' + kinds + ' 类字符。再加一类符号，强度会明显往上走。');
      } else {
        tips.push('<strong>种类太单一。</strong>全是数字或者全是字母，是最容易被机器一批一批试出来的。');
      }

      if (WEAK.indexOf(pw.toLowerCase()) >= 0) {
        score -= 3;
        tips.push('<strong>这是网上最常见的密码之一。</strong>别人拿一份「最常见密码表」一开头就会试到它，不管多长都没用。');
      }
      if (/(19|20)\d{2}/.test(pw) || /\d{6,}/.test(pw)) {
        score -= 1;
        tips.push('<strong>里面有生日或者一长串数字。</strong>年份、生日、学号、手机号，认识你的人第一反应就是拿这些去试。');
      }
      if (/(.)\1{2,}/.test(pw)) {
        score -= 1;
        tips.push('<strong>有连着重复的字符。</strong>aaaa 这种样子，机器试起来特别快。');
      }
      if (/qwert|asdf|zxcv|1234|abcd|0000/i.test(pw)) {
        score -= 1;
        tips.push('<strong>里面有按顺序或者挨着的一串。</strong>1234、abcd 看着乱，其实第一批就会被试到。');
      }

      score = Math.max(0, Math.min(5, score + (n >= 12 && kinds >= 3 ? 1 : 0)));
      var level = score <= 1 ? '弱' : (score <= 3 ? '中' : '强');
      return { score: score, level: level, kinds: kinds, tips: tips };
    }

    function paintPw() {
      var pw = pwInput.value;
      var r = evaluate(pw);
      drawGauge(r.score);
      levelEl.textContent = r.level;
      levelEl.style.color = r.score <= 1 ? 'var(--danger)' : (r.score <= 3 ? 'var(--warn)' : '#22c55e');
      scoreEl.textContent = r.score + ' / 5 分';
      lenEl.textContent = pw.length + ' 位';
      kindEl.textContent = r.kinds + ' 类';
      tipsEl.className = 'result ' + (r.score <= 1 ? 'error' : (r.score <= 3 ? 'warn' : ''));
      tipsEl.innerHTML = r.tips.map(function (t) { return '· ' + t; }).join('<br>');
    }

    pwInput.addEventListener('input', paintPw);
    document.querySelectorAll('[data-pw]').forEach(function (b) {
      b.addEventListener('click', function () {
        pwInput.value = b.getAttribute('data-pw');
        paintPw();
      });
    });
    paintPw();
  }

  /* ---------- 3. 鉴别两条消息 ---------- */
  var insPanel = document.getElementById('inspect-panel');
  if (insPanel) {
    var ROUNDS = [
      {
        head: '第 1 条消息',
        from: '发信号码：1069 开头的陌生号码（不是你班主任平时用的号）',
        text: '【学籍资料核对】家长您好，本学期学籍信息需要核对。请在今晚 22:00 前点击下方链接，填写学生姓名、班级与家长手机号。逾期将影响期末成绩单发放。网址：xx-school-check.top/info',
        clues: [
          ['发信号码', '是你从没见过的号码，也不知道这个号是谁在用。',
           '班主任平时用的是固定的那个号。号码对不上，就说明发消息的人至少不是你熟悉的那个。'],
          ['催得急不急', '「今晚 22:00 前」「逾期影响成绩单」，把时间卡得很死。',
           '真正要紧的事情，学校会提前通知，不会只留几个小时。把人催急，就是让人来不及想。'],
          ['要什么信息', '只要姓名、班级、家长手机号，没要密码也没要验证码。',
           '姓名加手机号，是骗子最想先拿到的东西。靠着这两样，他才好发第二条更像真的消息。'],
          ['网址对不对', '结尾是 .top，中间还带着 -check 这种词。',
           '学校的官方网站不会用这种便宜的域名后缀。网址是骗子最难伪装的地方，值得多看两眼。'],
          ['看起来正不正常', '整条消息没有一个错别字，语气很正式，落款也像模像样。',
           '这一条最容易骗人：没有错别字、语气正式、落款像真的，都是骗子可以刻意做到的。判断可不可信，要看号码和网址，不是看它写得像不像。']
        ],
        verdict: '这条消息<strong>可疑</strong>。它中了四个破绽里的三个——催得急、要信息、给链接。最容易骗过人的地方是：它读起来很正常。<br><span style="color:var(--muted)">安全不安全，不看它写得好不好。</span>'
      },
      {
        head: '第 2 条消息',
        from: '发送人：班主任王老师，用的就是平时那个号，消息发在班级群里',
        text: '明天上午体检，记得空腹来学校。体检表在教室后面自己拿，不用在网上填任何东西，也不用回复任何数字。',
        clues: [
          ['发送的人', '是班主任平时用的那个号，而且发在大家都熟悉的班级群里。',
           '号码和群都对得上，这是可以核实的东西，比头像和名字可靠得多。'],
          ['催得急不急', '只说要空腹，没有卡一个很急的时间点。',
           '通知一件明天的事，用的是正常提前量，没有制造紧张。'],
          ['要什么信息', '什么都没要，还特意说「不用在网上填任何东西」。',
           '正常的通知不会向你索取账号信息。主动说「什么都不用填」，反而是负责的做法。'],
          ['有没有链接', '整条消息一个链接也没有。',
           '不需要你点任何地方，也就没有把你带到假网站的机会。'],
          ['要不要花钱', '只让你明天去学校拿体检表，没有任何转钱、扫码、回复数字的要求。',
           '交代一件事，不涉及钱，也不涉及账号——这两样一出现，就要立刻警惕。']
        ],
        verdict: '这条消息<strong>正常</strong>。它一个破绽都没中：人是对的、不催、不要信息、没有链接、不涉及钱。<br><span style="color:var(--muted)">和上一条对照着看：不是所有消息都可疑，关键是有没有中那四个破绽。</span>'
      }
    ];
    var rd = 0, opened = {}, out3;
    var headEl = document.getElementById('ins-head');
    var fromEl = document.getElementById('ins-from');
    var textEl = document.getElementById('ins-text');
    var listEl = document.getElementById('ins-clues');
    out3 = document.getElementById('ins-verdict');

    function paint3() {
      var r = ROUNDS[rd];
      var keys = Object.keys(opened);
      var total = r.clues.length;
      headEl.textContent = r.head;
      fromEl.textContent = r.from;
      textEl.textContent = r.text;
      listEl.innerHTML = '';
      r.clues.forEach(function (c, i) {
        var b = document.createElement('button');
        b.className = 'choice';
        b.style.textAlign = 'left';
        b.textContent = (opened[i] ? '✓ ' : '○ ') + c[0] + '：' + c[1];
        if (opened[i]) {
          b.classList.add('correct');
        }
        b.addEventListener('click', function () {
          opened[i] = true;
          paint3();
          out3.className = 'result warn';
          out3.innerHTML = '<strong>' + c[0] + ' —— 怎么看：</strong>' + c[2];
        });
        listEl.appendChild(b);
      });
      document.getElementById('ins-progress').textContent = keys.length + ' / ' + total + ' 个细节已看过';
      document.getElementById('ins-target').textContent = r.head;
      if (keys.length === total) {
        out3.className = 'result';
        out3.innerHTML = r.verdict;
        document.getElementById('ins-next').disabled = rd >= ROUNDS.length - 1;
        if (rd >= ROUNDS.length - 1) {
          out3.innerHTML += '<br><br><strong>两轮小结：</strong>判断一条消息，不看它写得多正式，只看有没有中这四个破绽——催得急、要信息、点链接、要转钱。';
        }
      } else {
        out3.className = 'result warn';
        out3.textContent = '还有 ' + (total - keys.length) + ' 个细节没看。逐条点开，看完再下结论。';
      }
    }
    document.getElementById('ins-next').addEventListener('click', function () {
      if (rd < ROUNDS.length - 1) { rd++; opened = {}; paint3(); }
    });
    document.getElementById('ins-reset').addEventListener('click', function () {
      rd = 0; opened = {}; paint3();
    });
    paint3();
  }

  /* ---------- 4. 我的保护清单 ---------- */
  var listPool = document.getElementById('list-pool');
  if (listPool) {
    var ITEMS = [
      ['p1', '密码至少 12 位，里面有字母、数字和符号，而且每个账号都不一样',
        '长度和字符种类是密码强度的两条腿。每个账号用不同的密码，一处泄露才不会连累其他账号。'],
      ['p2', '验证码只留在自己手机上，不管谁问都不给',
        '验证码是一次性钥匙。客服、老师、同学，谁都不需要你的验证码，开口要的都是骗子。'],
      ['p3', '陌生链接先不点，把网址看一遍再说',
        '网址是骗子最难伪装的地方。多看一遍，很多明显不对劲的地方就露出来了。'],
      ['p4', '说自己中奖了、免费送礼物的消息，直接不理',
        '「免费」和「中奖」是钓人上钩最常用的饵。正规活动不会用陌生消息通知你先交钱。'],
      ['p5', '网上认识的人约见面，一定先告诉家里人',
        '网上认识的人，身份是没法核实的。要见面，必须让家里大人知道，而且在旁边。'],
      ['p6', '在公共电脑上登录过账号，走之前一定要退出',
        '不退出，下一个用这台电脑的人打开就是你的账号，等于把账号交给了陌生人。'],
      ['p7', '收到「老师」要资料的消息，先打电话跟老师本人核实',
        '头像和名字都能照抄，唯一靠得住的是你平时就知道的那个电话。'],
      ['p8', '手机和电脑提示更新系统、更新软件，就更新',
        '更新里常常包含安全漏洞的修补。拖着不更新，等于把门留着不关。'],
      ['q1', '把同一个密码用在所有账号上，这样好记',
        '只要有一个网站出了问题，你所有账号就一起被人打开了。好记不能拿这个换。'],
      ['q2', '把密码写在手机备忘录里，顺便写上账号，怕忘',
        '这等于把家里的钥匙和门牌号写在一起。实在记不住，可以用只有自己看得懂的提示词代替。'],
      ['q3', '只要消息是「官方」发来的，就照着做',
        '「官方」两个字谁都能写。要看的不是它自称什么，而是号码、网址这些能核实的东西。'],
      ['q4', '为了不被骗，以后干脆不上网',
        '因噎废食。要学会的是怎么用得更安全，不是把工具扔掉。']
    ];
    var GOOD = { p1: 1, p2: 1, p3: 1, p4: 1, p5: 1, p6: 1, p7: 1, p8: 1 };
    var picked = {}, locked = false;
    var out4 = document.getElementById('list-verdict');
    var cards = [];

    ITEMS.forEach(function (it) {
      var b = document.createElement('button');
      b.className = 'sort-item';
      b.textContent = it[1];
      b.addEventListener('click', function () {
        if (locked) return;
        if (picked[it[0]]) { delete picked[it[0]]; b.classList.remove('selected'); }
        else { picked[it[0]] = 1; b.classList.add('selected'); }
        document.getElementById('list-count').textContent = Object.keys(picked).length + ' 条';
        out4.className = 'result warn';
        out4.textContent = '已经选了 ' + Object.keys(picked).length + ' 条。选完点「检查我的清单」。';
      });
      listPool.appendChild(b);
      cards.push({ id: it[0], el: b });
    });

    document.getElementById('list-check').addEventListener('click', function () {
      locked = true;
      var right = 0, wrong = [];
      cards.forEach(function (c) {
        var should = !!GOOD[c.id];
        var did = !!picked[c.id];
        c.el.style.outline = 'none';
        c.el.classList.remove('selected');
        if (should === did) {
          c.el.classList.add('correct');
          right++;
        } else {
          c.el.classList.add('wrong');
          wrong.push(c.id);
        }
      });
      var why = wrong.map(function (id) {
        var it = ITEMS.filter(function (x) { return x[0] === id; })[0];
        var should = !!GOOD[id];
        return '<br>· 「' + it[1] + '」——' + (should ? '这一条<strong>该</strong>写进清单，但你没选：' : '这一条<strong>不该</strong>写进清单，但你选了：') + it[2];
      }).join('');
      out4.className = 'result' + (wrong.length ? ' warn' : '');
      out4.innerHTML = '<strong>对 ' + right + ' 条，需要再想想 ' + wrong.length + ' 条。</strong>' +
        (wrong.length ? why : '<br>全对了。把这八条连起来读一遍，它就是你的保护清单。') +
        '<br><br><span style="color:var(--muted)">常见错误：把「小心一点」和「干脆不用」当成一回事。清单是让你用得更放心，不是让你不用。</span>';
    });

    document.getElementById('list-reset').addEventListener('click', function () {
      locked = false;
      picked = {};
      cards.forEach(function (c) { c.el.className = 'sort-item'; c.el.style.outline = 'none'; });
      document.getElementById('list-count').textContent = '0 条';
      out4.className = 'result warn';
      out4.textContent = '先点卡片，把你认为该写进清单的条目选出来。';
    });
  }
})();
"""


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：这三件事，你会怎么做？", TTS["pretest"], [
        {"q": "手机上收到一条短信，说你的快递出了问题，点链接填写姓名和手机号就能重新派送。最稳妥的做法是：",
         "options": [("不点链接，去官方应用里自己查一查物流", True),
                     ("点开看看，反正只是填姓名和手机号", False),
                     ("先转发给同学，问问他们收到没有", False)],
         "explain": "要你先点链接、再填信息的陌生消息，是典型的可疑消息。自己从正规入口去查，才靠得住。"
                    "<strong>错因提醒：</strong>常见错误是误认为「只是姓名和手机号，没什么大不了」。"
                    "这两样正好是骗子最想先拿到的东西，靠它才能发第二条更像真的消息。"},
        {"q": "下面哪一个，是绝对不能告诉别人的？",
         "options": [("手机收到的那串验证码", True),
                     ("你最喜欢的颜色", False),
                     ("你喜欢的运动项目", False)],
         "explain": "验证码是一次性钥匙，谁拿到谁就能进你的账号。喜欢什么颜色、什么运动，属于可以公开的那一档。"
                    "<strong>错因提醒：</strong>容易把「熟人问的」和「可以给的」搞混。"
                    "验证码不管谁问都不能给——包括自称客服、自称老师的人。"},
        {"q": "关于密码，下面哪个说法是对的？",
         "options": [("长一点、种类杂一点、每个账号不一样，才算结实", True),
                     ("用自己的生日当密码，最好记也最安全", False),
                     ("所有账号用同一个密码，只要够长就没问题", False)],
         "explain": "密码的强度主要看长度和字符种类，再加上「不重复使用」。生日是认识你的人第一批会试的内容。"
                    "<strong>错因提醒：</strong>最常见的错误想法是「够长就行」。"
                    "只要所有账号共用一个密码，其中任何一个网站出问题，其他账号会一起被打开。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "个人信息分三档：可以公开的、只给熟人的、绝不外传的", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在网上发消息、填表格、注册账号，其实一直在交出信息（And）；可这些信息并不是一样重要的，一股脑给出去，会被人拿去冒充你、骗家里人（But）；所以要把它们分成三档，先学会哪一档绝对不能给（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px">凡是能<strong>认出你、找到你、冒充你</strong>的信息，都算个人信息。它们可以分成三档。</p>
        <div class="grid grid-3">
          <div class="inner-card"><p><strong>🟢 第一档 · 可以公开</strong></p><p style="color:var(--muted)">喜欢的颜色、爱看的书、擅长的运动。别人知道了没关系。</p></div>
          <div class="inner-card"><p><strong>🟡 第二档 · 只给熟人</strong></p><p style="color:var(--muted)">哪个班的、走哪条路上学、周末常去哪儿。家里人知道就够了。</p></div>
          <div class="inner-card"><p><strong>🔴 第三档 · 绝不外传</strong></p><p style="color:var(--muted)">密码、验证码、身份证号、家庭住址、家长的银行卡号。</p></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="个人信息三档示意图：可以公开、只给熟人、绝不外传，第三档列举密码、验证码、身份证号、家庭住址、银行卡号">
          <figcaption>个人信息不是一样重要的三档里，越往下越要收好；最要紧的是验证码——它是一次性钥匙</figcaption>
        </figure>
        <div class="kid-note"><span class="emoji">🔑</span><div><strong>为什么验证码最要紧：</strong>密码忘了还能改，验证码<strong>用过就作废</strong>。所以骗子会想尽办法让你在几分钟内把它念出来。记住一句：验证码不管谁问，都不能给。</div></div>
{insight_box([
    {"lens": "看见它", "text": "打开你的手机想一想：最近一周你在哪些地方填过信息？填的时候，有没有停下来想过它属于哪一档？"},
    {"lens": "比较它", "text": "「我是哪个班的」和「我的身份证号」，差的不只是字面。前者最多让人知道你在这个集体里，后者可以让人拿着去冒充你。"},
    {"lens": "迁移它", "text": "第三档的信息有个共同点：拿去就能当钥匙用。以后遇到要填这一类信息的地方，先问一句——它真的需要吗？"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：给密码做一次体检", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">在下面敲一个密码，强度环会实时变化，体检报告会一条一条告诉你它弱在哪里。也可以点例子直接试。</p>
        <div class="lab-panel">
          <div class="lab-stage" style="height:auto;min-height:auto;background:var(--bg-subtle);padding:14px;display:flex;gap:16px;flex-wrap:wrap;align-items:center;justify-content:center">
            <canvas id="pw-gauge" width="220" height="150" style="width:220px;max-width:100%;height:150px"></canvas>
            <div style="flex:1;min-width:180px;text-align:center">
              <div style="font-size:13px;color:var(--muted)">当前强度</div>
              <div id="pw-level" style="font-size:34px;font-weight:900;line-height:1.2;color:var(--brand)">—</div>
              <div id="pw-score" style="font-size:13px;color:var(--muted)">0 / 5 分</div>
            </div>
          </div>
          <div class="slider-row" style="display:block;margin-top:14px">
            <label for="pw-input" style="display:block;margin-bottom:6px">试一试这个密码：</label>
            <input id="pw-input" type="text" autocomplete="off" placeholder="在这里敲一个密码，边敲边看强度环">
          </div>
          <div class="flex-row" style="margin-top:10px">
            <button class="choice" data-pw="123456" style="text-align:center">123456</button>
            <button class="choice" data-pw="woaini520" style="text-align:center">woaini520</button>
            <button class="choice" data-pw="xiaoming2013" style="text-align:center">xiaoming2013</button>
            <button class="choice" data-pw="Tk7#pQ2mZ9@vL" style="text-align:center">Tk7#pQ2mZ9@vL</button>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">长度</span><span class="v" id="pw-len">0 位</span></div>
            <div class="readout-cell"><span class="k">字符种类</span><span class="v green" id="pw-kind">0 类</span></div>
          </div>
          <p class="result warn" id="pw-tips" style="margin-top:12px">还没有输入。在框里敲一个密码，或者点下面的例子试试看。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🧪</span><div><strong>试出来了吗：</strong>把 123456 改长、改杂之后，强度环会明显往右走；而 <em>xiaoming2013</em> 又长又有数字，看起来挺结实，却因为里面藏着名字和年份，只要认识你的人就能猜中。长度、种类、有没有规律——三条一起看，才叫结实。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "可疑消息的四个破绽：催得急、要信息、点链接、要转钱", TTS["module-2"], f'''
        <p style="font-size:17px;margin:0 0 12px">骗人的消息不管伪装成什么样，一般都逃不过下面<strong>四个破绽</strong>。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>催得急：</strong>「只剩 10 分钟」「不办就晚了」。一急，你就来不及想。</div></div>
          <div class="step"><span class="n">2</span><div><strong>要信息：</strong>要密码、要验证码、要身份证号。正常办事不会这样跟你要。</div></div>
          <div class="step"><span class="n">3</span><div><strong>点链接：</strong>让你点一个网址。网址和它嘴上说的对不上，是最大的破绽。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>要转钱：</strong>让你先付钱、先充值、扫码。凡是先要钱的，立刻停下来问大人。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="可疑消息的四个破绽示意图：一张消息气泡被放大镜逐条标出催得急、要信息、点链接、要转钱">
          <figcaption>四个破绽不用全中，中一个就值得停下来核实——尤其是「要钱」和「要验证码」</figcaption>
        </figure>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学认为「只要没有错别字、语气够正式、落款像官方的，就说明是真的」。恰恰相反：<strong>错别字少、语气正式、头像像老师，这些都是骗子可以刻意做出来的</strong>。真正能核实的是号码、网址这些你本来就熟悉的东西。</p>
        </div>
        <div class="kid-note" style="margin-top:12px"><span class="emoji">🛑</span><div><strong>记一句口诀：</strong>催得急、要信息、点链接、要转钱——中一个，先停下来核实。</div></div>
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "动手二：当一次鉴别员，逐条看这两条消息", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">上面是一条消息，下面列出它的几个细节。一个细节一个细节地点开看，看完再下结论。</p>
        <div class="lab-panel" id="inspect-panel">
          <div class="inner-card" style="background:var(--card);border:2px solid var(--brand)">
            <p><strong id="ins-head">第 1 条消息</strong></p>
            <p style="color:var(--muted);font-size:13px;margin:0 0 6px" id="ins-from">—</p>
            <p style="margin:0;font-size:15px" id="ins-text">—</p>
          </div>
          <div style="font-weight:700;font-size:14px;margin:14px 0 6px">逐条点开这些细节，看看能不能看出问题</div>
          <div class="grid" id="ins-clues"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">正在鉴别</span><span class="v" id="ins-target">第 1 条消息</span></div>
            <div class="readout-cell"><span class="k">进度</span><span class="v green" id="ins-progress">0 / 5 个细节已看过</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="ins-next" style="text-align:center" disabled>看第 2 条消息 →</button>
            <button class="choice" id="ins-reset" style="text-align:center">从头再来</button>
          </div>
          <p class="result warn" id="ins-verdict" style="margin-top:12px">逐条点开细节，看完再下结论。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🔍</span><div><strong>做完两轮，回头看：</strong>第 1 条里最难发现的不是网址，而是它「读起来很正常」；第 2 条里最让人放心的也不是语气，而是「人是对的、什么都没要」。判断可不可信，要看能核实的东西。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：同学发来的那条链接，点还是不点？", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>题目：</strong>小明收到三条消息：①同学说「明天考试范围变了，资料点这个链接下载」；②「你的账号异常，回复短信里的数字就能解锁」；③「恭喜你中了一台平板，先付 20 元运费」。请逐条判断该怎么办，并说明理由。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先看它要什么：</strong>第①条只要点链接，第②条要短信里的数字（那多半是验证码），第③条要你先付钱。</div></div>
          <div class="step"><span class="n">2</span><div><strong>再看它急不急：</strong>①说明天就考，②说账号异常，③说中奖有时限——三条都在制造着急。</div></div>
          <div class="step"><span class="n">3</span><div><strong>最后看能不能核实：</strong>①的网址和同学平时发的不一样；②根本没有任何正规入口让你去查；③正规抽奖不会让中奖的人先付钱。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>给出做法：</strong>①先不点，直接打电话问那个同学本人；②不回复、不念数字，自己打开官方应用看看账号是否正常；③不理它，直接删掉。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有同学会想：「第①条是我同学发的，肯定没问题。」可是<strong>账号是可以被冒用的</strong>——别人登上了他的号，发出来的消息看起来就是同学发的。所以第一步不是判断「像不像同学」，而是用一个<strong>另外的渠道</strong>去核实：打个电话、当面问一句。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三个说法，错在哪里", TTS["conceptest-1"], [
        {"q": "有同学说：「这条消息从头到尾没有错别字，语气也很正式，那应该是真的。」这个想法的问题在哪？",
         "options": [("错别字和语气都是可以刻意做出来的，能核实的是号码和网址", True),
                     ("没有错别字就说明确实是真的", False),
                     ("语气正式的消息一定是骗子发的", False)],
         "explain": "骗子完全可以把消息写得干净、正式、落款像官方。真正能核实的是发信号码和网址这些你本来就熟悉的东西。"
                    "<strong>错因提醒：</strong>最常见的错误是误认为「写得像真的＝真的」。"
                    "判断的依据要放在可核实的信息上，不是放在感觉上。"},
        {"q": "「给账号充一次值就能解锁，快点，十分钟后就失效了」——这条消息中的破绽是什么？",
         "options": [("同时中了两个：催得急、要转钱", True),
                     ("只有一个破绽：它写得太短", False),
                     ("没有破绽，因为它是系统自动发的", False)],
         "explain": "限时十分钟是在制造着急，要求先充值是在要钱。两个破绽同时出现，几乎可以确定有问题。"
                    "<strong>错因提醒：</strong>容易把「系统自动发的」当成可信的理由。"
                    "自称是谁不重要，重要的是它要你做什么。"},
        {"q": "关于验证码，下面哪句话对？",
         "options": [("验证码是一次性钥匙，不管谁问都不能给", True),
                     ("只要对方能说出我的名字，就可以给他", False),
                     ("验证码用过了还能再用，所以给一次没关系", False)],
         "explain": "验证码用过就作废，正是这一点让它格外要紧——给出去了，账号的门就开了。"
                    "<strong>错因提醒：</strong>这里最容易搞混的是「他认识我」和「他可信」。"
                    "能叫出你名字、能报出你班级的人，恰恰是最需要警惕的，因为这些信息本来就容易被打听到。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：做一份属于你自己的保护清单", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">下面有十二条候选说法。点一下卡片就可以选上或者取消，把你认为该写进保护清单的挑出来，再点「检查我的清单」。</p>
        <div class="lab-panel" id="list-panel">
          <div style="font-weight:700;font-size:14px;margin-bottom:6px">十二条候选说法</div>
          <div class="sort-bank" id="list-pool"></div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">已选</span><span class="v" id="list-count">0 条</span></div>
          </div>
          <div class="flex-row">
            <button class="choice" id="list-check" style="text-align:center">检查我的清单</button>
            <button class="choice" id="list-reset" style="text-align:center">重新来</button>
          </div>
          <p class="result warn" id="list-verdict" style="margin-top:12px">先点卡片，把你认为该写进清单的条目选出来。</p>
        </div>
        <div class="inner-card">
          <p><strong>检查完以后想一想，说给同桌听：</strong></p>
          <p style="color:var(--muted)">十二条里有四条是<strong>不该</strong>写进清单的。它们看着像在保护你，其实会给你添麻烦。你能说清楚每一条的问题在哪里吗？</p>
          <textarea id="syn-answer" rows="3" placeholder="不该选的第一条是……因为……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个情境，四个破绽还在不在", TTS["posttest"], [
        {"q": "你看到一个网站写着「免费领取学习礼包，只需填写姓名、学校和家长手机号」。最稳妥的做法是：",
         "options": [("不填，先弄清楚这是谁办的、要这些信息做什么", True),
                     ("反正是免费的，填了再说", False),
                     ("先填个假名字，其他信息填真的", False)],
         "explain": "「免费」是最常见的诱饵，而要的又正好是能定位到你和你家长的信息。先弄清楚是谁办的，再决定填不填。"
                    "<strong>错因提醒：</strong>这里最容易出错的是「填一部分真的没关系」。"
                    "姓名加手机号已经足够让人找到你，真真假假混着填反而更乱。"},
        {"q": "有人在聊天里说：「我是客服，你把收到的验证码报给我，我帮你把误扣的钱退回来。」正确做法是：",
         "options": [("不报验证码，自己打开官方应用查这笔钱", True),
                     ("把验证码报给他，反正是要退钱给我", False),
                     ("先把验证码报一半，看他反应再说", False)],
         "explain": "验证码不能给任何人。自己从正规入口去查，才能真正知道钱有没有被扣。"
                    "<strong>错因提醒：</strong>常见错误是被「退钱」两个字吸引住了。"
                    "对方越是给你好处，越要想一想：他为什么需要我的验证码？"},
        {"q": "在图书馆的公共电脑上登录了自己的账号，离开前最重要的一件事是：",
         "options": [("退出账号，并关掉浏览器", True),
                     ("把自己的东西带走就行", False),
                     ("清空浏览器的历史记录就够了", False)],
         "explain": "不退出账号，下一个用这台电脑的人打开就是你的账号。清历史记录不等于退出登录。"
                    "<strong>错因提醒：</strong>容易把「清理痕迹」和「退出登录」搞混。"
                    "痕迹清掉只是别人看不到你去过哪儿，账号还开着，门就还开着。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三句话，把上网这件事护住", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>信息分三档：</strong>可以公开的、只给熟人的、绝不外传的。密码和验证码在最要紧的那一档。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>密码要三看：</strong>够长、够杂、每个账号都不一样。名字和生日不能当密码。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>消息看四破绽：</strong>催得急、要信息、点链接、要转钱。中一个就先停下来核实。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>回到开头那条消息：</strong>头像像老师，不代表就是老师；没有错别字，也不代表就是真的。唯一靠得住的办法，是用<strong>另外一个渠道</strong>去核实——打个电话，或者当面问一句。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「三个档次、四个破绽」这两组词，说清楚那条消息到底哪里不对劲。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写下来</strong>——你今天在综合任务里选中的那八条，按你最容易忘的顺序重新排一遍。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "把个人信息按三个档次各写两个例子，并说出验证码为什么绝对不能告诉别人。",
            "背一背识破可疑消息的口诀：催得急、要信息、点链接、要转钱。",
        ],
        [
            "把家里一个账号的弱密码改成强密码，把改之前和改之后的样子记下来（不要写真正的密码）。",
            "找一条你或家里人收到过的可疑消息，用四个破绽逐条分析，写出你的判断。",
        ],
        [
            "和家长一起，给家里写一份一页纸的防骗提醒，写清楚遇到哪几种情况要先打电话核实。",
            "想一想：如果家里的老人收到「孙子在学校出事要交钱」的消息，你会教他们怎么做？把你的办法写下来。",
        ],
    ]))

    pages.append(p_kg(SPEC, 14))
    pages.append(p_tutor(SPEC, 15))
    return pages


SPEC = {
    "id": "it-e-network-security-basic",
    "node_id": "it-e-network-security-basic",
    "subject": "info-tech",
    "subject_cn": "信息科技",
    "stage": "elementary",
    "stage_cn": "小学",
    "curriculum": "义务教育信息科技课程标准（2022年版2025年修订）· 小学",
    "title": "网络安全与信息保护",
    "name_en": "Network Safety and Protecting Your Information",
    "grade": 5,
    "grade_cn": "五年级",
    "domain": "internet-ai",
    "domain_cn": "互联网与人工智能",
    "lesson_type": "concept-practice",
    "version": "1.0.0",
    "description": "面向小学五年级：把个人信息分成可以公开、只给熟人、绝不外传三档，理解密码强度由长度与字符种类决定，掌握识别可疑消息与链接的四个破绽（催得急、要信息、点链接、要转钱），并产出一份自己照着做得到的上网保护清单。",
    "tags": ["网络安全", "个人信息保护", "密码强度", "可疑链接", "信息社会责任"],
    "standard_ref": "《义务教育信息科技课程标准（2022年版2025年修订）》小学「互联网与人工智能」——知道个人信息保护要求，识别常见网络安全风险。",
    "hero_question": "一条看起来很正常、一个错别字都没有的消息，为什么可能是在骗你？",
    "hero_alt": "网络安全与信息保护知识结构图：个人信息三档、密码强度三看、可疑消息四个破绽",
    "hero_caption": "信息分三档：可以公开 · 只给熟人 · 绝不外传　|　密码三看：够长 · 够杂 · 不重复　|　破绽四个：催得急 · 要信息 · 点链接 · 要转钱",
    "anchor_title": "今天最想弄明白哪一件事？",
    "anchor_intro": "选一个你真正好奇的问题，后面的动手活动都会围着它转。",
    "anchor_choices": [
        {"t": "密码到底怎么设才算安全？", "d": "想知道一个结实的密码长什么样", "v": "密码到底怎么设才算安全"},
        {"t": "怎么看出一条消息是骗人的？", "d": "想知道该盯住哪几个地方", "v": "怎么看出一条消息是骗人的"},
        {"t": "哪些信息绝对不能给别人？", "d": "想弄清楚三档信息的分界在哪里", "v": "哪些信息绝对不能给别人"},
        {"t": "能不能给我一份照着做的保护清单？", "d": "想要一份能贴在书桌前的清单", "v": "能不能给我一份照着做的保护清单"},
    ],
    "objectives": [
        "能把个人信息分成可以公开、只给熟人、绝不外传三档，并说出哪一档绝对不能给出去",
        "能说出密码强度由长度和字符种类决定，并亲手把一个弱密码改成强密码",
        "能用催得急、要信息、点链接、要转钱这四个破绽检查一条消息或一个网址",
        "能写出一份自己照着做得到的上网保护清单，并说明其中每一条的理由",
    ],
    "objectives_plain": [
        "能把个人信息分成可以公开、只给熟人、绝不外传三档，并说出哪一档绝对不能给出去",
        "能说出密码强度由长度和字符种类决定，并亲手把一个弱密码改成强密码",
        "能用催得急、要信息、点链接、要转钱这四个破绽检查一条消息或一个网址",
        "能写出一份自己照着做得到的上网保护清单，并说明其中每一条的理由",
    ],
    "standards": [
        {"content": "知道个人信息保护要求，识别常见网络安全风险",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能"},
        {"content": "在真实情境中分辨信息的可信度，形成保护自己与家人的信息、不轻易转发与不轻信陌生链接的责任意识",
         "source": "《义务教育信息科技课程标准（2022年版2025年修订）》小学 互联网与人工智能 / 信息社会责任"},
    ],
    "prereqs": ["it-e-internet-services"],
    "prereqs_name": "互联网服务与应用",
    "prereqs_meta": "it-e-internet-services",
    "leads_to": ["it-m-cybersecurity"],
    "next_meta": "it-m-cybersecurity",
    "section_images": ["assets/it-e-network-security-basic-fig1.webp", "assets/it-e-network-security-basic-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "没有错别字、头像像老师，也算可疑吗？带着这个疑问开始。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能自己看出一条消息哪里不对劲。",
        "objectives": "看清四件事：信息分三档、密码怎么算结实、消息的四个破绽、写一份保护清单。",
        "pretest": "凭现在的想法选就好，错了不扣分——前测是帮你看清自己站在哪里。",
        "module-1": "个人信息分三档，越往下越要收好；验证码是一次性钥匙，谁问都不能给。",
        "lab-1": "真的敲一个密码进去，看强度环怎么变。长度、种类、有没有规律，三条一起看。",
        "module-2": "四个破绽：催得急、要信息、点链接、要转钱。中一个就要停下来核实。",
        "lab-2": "逐条点开细节再下结论。有一条消息从头到尾都看不出问题，仔细找找是哪一条。",
        "worked-example": "四步走：先看要什么、再看急不急、再看能不能核实、最后给出做法。",
        "conceptest-1": "三个说法里藏着高频错误，选完把解释读一遍。",
        "synthesis": "十二条候选里有四条是「看着像保护你，其实给你添麻烦」的，别被它们骗过去。",
        "posttest": "免费礼物、客服要验证码、公共电脑登录——四个破绽还管用吗？",
        "summary": "三句话：信息分三档、密码要三看、消息看四破绽。",
        "homework": "三层小任务，先做前两层，第三层留给愿意继续探索的你。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学信息科技「互联网与人工智能」在网络安全板块的空缺。五年级学生真正的困难不是不知道「要注意安全」，而是没法判断一条具体消息要不要相信，也分不清哪些信息属于「绝对不能说」。所以全课不做口号宣讲，只做三件真能上手的事：先用一个密码强度体检器，让学生在输入框里真的敲密码，看着强度环随长度、字符种类、有没有藏名字生日而变化，把「密码强度」变成能看见的东西；再用「鉴别两条消息」逐条点开细节——第 1 条是可疑消息，故意留了一条「读起来很正常、没有错别字」的陷阱细节，第 2 条是正常消息，两轮对照让学生明白判断依据在号码和网址这类可核实的信息上，而不是在感觉上；最后用十二条候选说法勾出保护清单，其中有四条是「看着像保护你、其实给你添麻烦」的过度反应与错误做法，把信息社会责任落在具体的选择上。概念页把识别方法收成一句口诀（催得急、要信息、点链接、要转钱），并强调四个破绽中一个就值得停下来核实。全课不出现任何真实平台、应用或机构品牌。",
    "plan_table": """| 1 | cover | 网络安全与信息保护 | 定向 |
| 2 | interactive | 今天最想弄明白哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：这三件事，你会怎么做？ | 起·前测（暴露直觉） |
| 5 | concept | 个人信息分三档：可以公开的、只给熟人的、绝不外传的 | 承·概念一（三档 + 验证码 + 生活场景） |
| 6 | interactive | 动手一：给密码做一次体检 | 承·动手模拟（强度环实时评估 + 逐条弱因诊断） |
| 7 | concept | 可疑消息的四个破绽：催得急、要信息、点链接、要转钱 | 承·概念二（四破绽 + 口诀 + 常见错误） |
| 8 | interactive | 动手二：当一次鉴别员，逐条看这两条消息 | 承·判定练习（两条消息 × 5 个细节，含「看起来很正常」陷阱） |
| 9 | concept | 例题示范：同学发来的那条链接，点还是不点？ | 转·重难点突破（四步示范 + 纠错） |
| 10 | quiz | 概念测试：三个说法，错在哪里 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：做一份属于你自己的保护清单 | 合·迁移应用（12 条候选勾选，含 4 条「看着像保护」的错误做法） |
| 12 | quiz | 后测：换几个情境，四个破绽还在不在 | 合·后测 |
| 13 | summary | 小结：三句话，把上网这件事护住 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：个人信息三档 / 密码强度三看 / 可疑消息四个破绽 三栏\n- P5 个人信息三档示意图（已生成）：可以公开 → 只给熟人 → 绝不外传\n- P7 可疑消息四个破绽示意图（已生成）：一张消息气泡 + 四个放大镜标注\n- 三张图均为教学示意图，画面中不出现任何真实平台、应用、机构品牌或界面截图\n- 若需补充：家庭上网场景照片（需获得授权后使用）",
}
