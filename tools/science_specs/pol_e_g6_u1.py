# -*- coding: utf-8 -*-
"""小学道德与法治 · 我们的守护者（六年级上·第1单元）—— 补齐知识树「道德修养」空缺

学科语气（道德与法治）：从学生每天上下学的路口、教室里的座位、手机里的消息讲起，
情感共鸣 + 价值判断；结论落在「遇到事情该找谁、为什么这样找」，不做口号式抒情、不背条文。

★ 表述红线（最高优先级，全课统一口径，任何地方不得含糊）：
  · 法律名称一律写全称、写准确：《中华人民共和国宪法》《中华人民共和国未成年人保护法》。
  · 一律不出现任何法律条文编号（不写「第几条」，只说「宪法规定」「法律规定」）。
  · 不臆造案例细节，不编造机关名称、电话号码与办理流程；求助渠道只用常识层面、
    社会公认的公开渠道（告诉父母、报告老师、请学校或社区帮助、110、12345、12355）。
  · 宪法只讲定位与效力，不引原文条款：宪法是国家的根本法，是治国安邦的总章程，
    具有最高的法律效力，一切法律、行政法规和地方性法规都不得同宪法相抵触。

内容落点（对应统编六上第 1 单元「我们的守护者」）：
  ① 感受生活中的法律：法律是由国家制定或认可、靠国家强制力保证实施、对全体社会成员
     具有普遍约束力的行为规范；生活处处有法律，法律就在我们身边。
  ② 宪法是根本法：宪法规定国家生活中最根本、最重要的问题；具有最高的法律效力；
     一切组织和个人都必须以宪法为根本的活动准则；12 月 4 日是国家宪法日。
  ③ 国家为我们撑起的保护伞：《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，
     确立了家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护，
     保护未成年人是全社会的共同责任，坚持最有利于未成年人的原则。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = 「法律就在身边」情境配对台（5 个生活情境 × 5 部管这件事的法律）；
  动手二 = ★核心模拟「遇到困难该找谁」对照台（6 个真实情境 × 6 类保护力量，配出求助渠道）；
  综合任务 = 「我的守护锦囊」生成台（选情境 → 选第一个该找的人 → 选一句说清楚的话 → 合成锦囊卡）。
插图一律中性简洁扁平插画，不使用真人照片风格，不绘制国旗、国徽、宪法文本封面等图形，
涉及国家与法律改用立柱、拱门、盾牌、天平、书页线条等抽象符号与地标性建筑抽象剪影。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g6-u1"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "先想一件事：今天早上你出门上学，路上看了信号灯，进了校门，坐在自己的座位上，课间还和同桌分享了一包饼干。这些看起来很平常的事，背后都有一样东西在悄悄守护着我们，那就是法律。这节课我们弄清楚三件事：法律到底和我们有什么关系，为什么说宪法是国家的根本法，以及当我们遇到困难时可以找谁帮忙。带着这三个问题，我们开始。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题：法律离我们到底有多近？为什么说宪法是国家的根本法？遇到困难的时候，我们该找谁？还是那部专门保护我们的法律都保护了什么？选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出法律是什么，知道法律就在我们身边。第二，能说出宪法是国家的根本法、具有最高的法律效力，知道十二月四日是国家宪法日。第三，能说出《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，并把家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护说出来。第四，遇到困难时能找到合适的人和渠道求助，知道说清楚时间、地点和经过。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "第一件事，法律就在我们身边。什么是法律？法律是由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力的行为规范。它有三个方面最要紧：一是由国家制定或认可，不是谁想定就能定；二是靠国家强制力保证实施，这一点把法律和道德、纪律区分开来；三是对全体社会成员都有约束力，法律面前人人平等，没有人可以例外。生活里到处都是法律的守护：我们每天到学校上课，有《中华人民共和国义务教育法》；过马路看信号灯，有《中华人民共和国道路交通安全法》；买到过期食品可以要求商家处理，有《中华人民共和国消费者权益保护法》；工厂不能往河里排污，有《中华人民共和国环境保护法》。这里有两个容易想歪的地方：有的同学误认为法律离我们很远，只有犯法的人才跟法律打交道；也有的同学把道德和法律搞混，觉得违反了道德就等于违法。其实法律是底线，道德是更高的要求，两者都在守护我们，但不是一回事。",
    "lab-1": "现在请你玩一次配对。左边是五个生活情境，右边是五部管这件事的法律，顺序被打乱了。先点一个情境，再点你认为对应的那部法律。配对了，两边会连起来；配错了，我会告诉你这样可能会错在哪里，还可以怎么想。",
    "module-2": "第二件事，宪法是国家的根本法。为什么这么多法律里，还要单独记住宪法？因为宪法是国家的根本法，是治国安邦的总章程，它规定的是国家生活中最根本、最重要的问题，比如国家的性质、根本制度、根本任务、公民的基本权利和义务、国家机构的组织及其职权。宪法具有最高的法律效力：一切法律、行政法规和地方性法规都不得同宪法相抵触；任何组织或者个人都不得有超越宪法和法律的特权。宪法的制定和修改程序也比其他法律更加严格，它的修改要由全国人民代表大会以全体代表的三分之二以上的多数通过。全国各族人民、一切国家机关和武装力量、各政党和各社会团体、各企业事业组织，都必须以宪法为根本的活动准则。我国还把十二月四日设立为国家宪法日，为的是让全社会都增强宪法意识。这里有两个容易搞混的地方：有的同学误认为宪法也是一部只管某一件小事的具体法律；也有的同学觉得宪法很高很远，跟小学生没关系。其实我们上学、被保护、被尊重，都离不开宪法确立的保障。",
    "lab-2": "接下来是这个单元最重要的一个台子：遇到困难该找谁。左边是六个真实的困难情境，右边是六类保护力量。先点一个情境，再点你认为最该找的那一类保护。配对了，我会告诉你该找谁、可以怎么做；配错了，我会告诉你这样可能会耽误事，还可以试试别的方向。记住一件事：遇到困难不是丢人的事，及时说出去，才是对自己最好的保护。",
    "worked-example": "我们一起来看一次求助方案的校对。班里要为同学们做一份求助指引，几位同学写了四条方案，请你当一次校对员。方案一，遇到困难先自己扛着，别告诉任何人，免得被笑话。这一条不妥。这样可能会：让事情拖得更久、变得更严重。还可以试试：把心里的事告诉父母、老师或者其他你信任的大人。方案二，把事情告诉父母和老师，说清楚时间、地点和事情的经过。这一条可行，说清楚细节，大人才好帮你。方案三，拨打报警电话一百一十，或者拨打一二三四五政务服务便民热线、一二三五五青少年服务台寻求帮助。这一条也可行，这些都是可以公开求助的渠道。方案四，自己去找对方算账，把气出回来。这一条不行。这样可能会：既伤了别人，也伤了自己，还可能让自己从被欺负的一方变成做错事的一方。再看一遍这四条，你会发现问题不在胆量，而在方法。这里还有一个常见错误要提醒：有的同学把《中华人民共和国未成年人保护法》和《中华人民共和国宪法》搞混了。宪法是国家的根本法，未成年人保护法是专门保护未满十八周岁公民的一部法律，它规定的家庭保护、学校保护、社会保护、网络保护、政府保护和司法保护，是把宪法的精神落到了我们的日常生活里。",
    "conceptest-1": "接下来用三道题考考你，每道题里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你：为自己做一份守护锦囊。下面分三步：先选一个你想过办法去应对的情境，再选你第一个会告诉的人或者会找的力量，最后选一句你打算怎么说清楚的话。三步选完，我会把它们拼成一张锦囊卡，你可以抄进自己的小本子里。",
    "posttest": "最后一轮，换几个新情境来考考你。这次会遇到放学路上的事、家里的事和网上的事，看看今天学的方法还用不用得上。",
    "summary": "这节课我们弄清楚三件事。第一，法律就在我们身边：法律是由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力的行为规范，生活处处有法律。第二，宪法是国家的根本法，具有最高的法律效力，一切法律、行政法规和地方性法规都不得同宪法相抵触，十二月四日是国家宪法日。第三，《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，确立了家庭保护、学校保护、社会保护、网络保护、政府保护和司法保护六大保护；保护未成年人是全社会的共同责任。最后记住一句最实用的话：遇到困难及时说出来，找对人、说清楚，就是对自己最好的保护。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出法律区别于道德和纪律的最主要特征，再写出宪法在国家法律体系中的地位和效力。第二层能力应用，动手做：把《中华人民共和国未成年人保护法》确立的六类保护各举一个身边的例子，写成六行小清单。第三层迁移挑战，选做：为自己做一份守护锦囊，写清楚三个情境、第一个该告诉的人、以及打算怎么说清楚，做完在班里和同学交流一遍。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域里的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 感受生活中的法律", "lab-1": "动手一 法律就在身边情境配对台",
    "module-2": "概念二 宪法是国家的根本法", "lab-2": "动手二 遇到困难该找谁对照台",
    "worked-example": "例题示范 求助方案校对与未成年人保护法", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的守护锦囊生成台", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一：法律就在身边情境配对台（5 情境 × 5 部法律） ──
LAWS = [
    {"k": "l1", "n": "《中华人民共和国义务教育法》",
     "what": "保障适龄儿童、少年接受义务教育的权利。",
     "f": "我们每天到学校上课，学校不能随意让我们停学。",
     "why": "上学不只是家里的事，也是国家的事：法律保障每个适龄儿童、少年都能接受义务教育，学校和我们都要认真对待这件事。",
     "tip": "还可以试试：想一想「上学」为什么既是我们的权利，也是我们要完成的义务。"},
    {"k": "l2", "n": "《中华人民共和国道路交通安全法》",
     "what": "规范道路交通秩序，保护人身安全。",
     "f": "过马路要看交通信号灯，走斑马线，不闯红灯。",
     "why": "信号灯、斑马线、安全带这些规定，目的都是让每个人的出行更安全，其中也特别照顾行人和未成年人。",
     "tip": "还可以试试：把「遵守规则」和「保护自己」连起来想一想，它们其实是一件事。"},
    {"k": "l3", "n": "《中华人民共和国消费者权益保护法》",
     "what": "保护消费者在购买、使用商品和接受服务时的合法权益。",
     "f": "买到过期食品，可以要求商家处理。",
     "why": "买东西时我们是消费者，法律保护我们不受欺骗，也要求商家诚信经营。",
     "tip": "还可以试试：保留好小票或付款记录，这样说明情况时更有依据。"},
    {"k": "l4", "n": "《中华人民共和国环境保护法》",
     "what": "保护和改善环境，防治污染和其他公害。",
     "f": "工厂不能往河里排污，垃圾分类人人有责。",
     "why": "清水、蓝天、干净的土壤，都是法律在守护的公共利益，我们每个人也是参与者。",
     "tip": "还可以试试：想一想，自己每天能做的一件环保小事是什么。"},
    {"k": "l5", "n": "《中华人民共和国民法典》",
     "what": "调整平等主体之间的人身关系和财产关系，被称为社会生活的百科全书。",
     "f": "捡到别人丢的东西，应当归还。",
     "why": "拾得遗失物应当返还权利人，这是民法典处理日常生活纠纷的基本态度：讲诚信、守规矩。",
     "tip": "还可以试试：先想「这样对别人公不公平」，再看法律是怎么规定的。"},
]

# ── 动手二（★核心模拟）：遇到困难该找谁对照台（6 情境 × 6 类保护力量） ──
SEEK = [
    {"k": "s1", "n": "在家里遇到困难",
     "case": "爸爸妈妈因为生气，不让我去上学，也不听我解释。",
     "who": "家庭保护",
     "how": "家庭保护说的是父母或者其他监护人应当保护未成年人，也要保障我们受教育的权利。遇到这种情况，先好好说明自己的想法；如果说不通，就告诉老师或者请学校、社区帮助沟通。",
     "tip": "还可以试试：把事情说具体一点——从什么时候开始、发生了什么、你希望怎样，大人更容易听懂。"},
    {"k": "s2", "n": "在学校遇到困难",
     "case": "有同学反复给我起侮辱性的外号，我很难受。",
     "who": "学校保护",
     "how": "学校保护说的是学校应当关心、爱护学生，制止欺负同学的行为。可以先告诉班主任或者你信任的老师，请老师出面处理；也可以回家告诉父母。",
     "tip": "还可以试试：把发生的时间、地点和当时的原话说清楚，不要说「反正就是欺负我」，这样老师才好帮你。"},
    {"k": "s3", "n": "在校外遇到危险",
     "case": "放学路上，有陌生人一路跟着我，还说要我跟他走。",
     "who": "社会保护",
     "how": "社会保护说的是全社会都要为未成年人营造安全的环境。这时要坚决拒绝，马上走向人多、明亮的地方，找附近可靠的成年人帮忙，并及时告诉父母和老师；情况紧急可以拨打报警电话一百一十。",
     "tip": "还可以试试：平时就和父母约好一条安全的路线和一个可以求助的地点。"},
    {"k": "s4", "n": "在网上遇到麻烦",
     "case": "网上有人不停骂我，还要我把家里的地址和照片发给他。",
     "who": "网络保护",
     "how": "网络保护说的是要为我们营造健康的网络环境，保护我们不受网络侵害。不要回复、不要发送任何信息，保存好截图，告诉父母或者老师；情况严重时可以拨打报警电话一百一十。",
     "tip": "还可以试试：把对方说的话截图保存下来，证据比你记住的细节更靠得住。"},
    {"k": "s5", "n": "事情一直没人管",
     "case": "我把困难反映上去了，可是过了很久还是没有解决。",
     "who": "政府保护",
     "how": "政府保护说的是有关部门依法履行职责，保护未成年人的合法权益。可以请父母或老师拨打一二三四五政务服务便民热线反映情况，也可以向当地的未成年人保护机构求助。",
     "tip": "还可以试试：再往上反映一次，并把之前反映的时间和结果一起说清楚。"},
    {"k": "s6", "n": "需要法律来保护",
     "case": "有人伤害了我，我希望能得到法律的保护和公正的处理。",
     "who": "司法保护",
     "how": "司法保护说的是公安机关、人民检察院、人民法院等依法履行职责，保护未成年人。在父母和其他人陪同下，可以向公安机关报案，也可以向人民法院请求保护，法律会站在我们这一边。",
     "tip": "还可以试试：遇到要打官司这样的大事，一定要有大人陪着一起，不要自己单独去。"},
]

# ── 综合任务：我的守护锦囊生成台 ──
KIT = {
    "cases": [
        {"k": "c1", "n": "放学路上被陌生人跟着"},
        {"k": "c2", "n": "同学反复给我起侮辱性外号"},
        {"k": "c3", "n": "网上有人要我发照片和家庭住址"},
        {"k": "c4", "n": "买到过期食品，商家不肯处理"},
    ],
    "persons": [
        {"t": "第一个告诉我信任的大人：父母或者老师", "ok": True,
         "why": "这是最稳妥的第一步。父母和老师离我们最近，也最方便帮我们想办法，还能陪你一起去反映。"},
        {"t": "谁也不说，自己想办法解决", "ok": False,
         "why": "这样可能会：事情越拖越难处理，自己还一直担着。还可以试试：哪怕只说出一句「我遇到麻烦了」，也是在保护自己。"},
        {"t": "先在网上把这件事公开，让大家来评理", "ok": False,
         "why": "这样可能会：把对方的个人信息说出去，反而让自己也可能做错事。还可以试试：先把情况告诉大人，再决定怎么处理。"},
    ],
    "words": [
        {"t": "说清楚时间、地点、发生了什么，还有我现在的感受。", "ok": True,
         "why": "一句话里有事实也有感受，大人马上就能听懂，也更容易帮你。"},
        {"t": "只说「反正就是他们欺负我」，其他的都说不清。", "ok": False,
         "why": "这样可能会：对方不知道从哪一步帮你，你还得从头再说一遍。还可以试试：把时间、地点、经过按顺序讲一遍。"},
        {"t": "怕被笑话，故意把最要紧的那一段省略掉。", "ok": False,
         "why": "这样可能会：大人判断偏了，帮不到你真正需要的地方。还可以试试：可以先说明「有一件事我有点不好意思讲」，再慢慢讲出来。"},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g6-u1 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) 「法律就在身边」情境配对台：5 个生活情境 × 5 部法律
   3) ★「遇到困难该找谁」对照台：6 个情境 × 6 类保护力量 → 配出求助渠道
   4) 「我的守护锦囊」生成台：情境 → 该找的人 → 怎么说清楚 → 合成锦囊卡
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

  /* ---------- 2. 「法律就在身边」情境配对台 ---------- */
  var LAWS = __LAWS_JSON__;
  var CASES = __CASES_JSON__;
  var stage1 = document.getElementById('lp-stage');
  if (stage1) {
    var selL = null;
    var matched = {};
    var out1 = document.getElementById('lp-out');
    var left = document.getElementById('lp-left');
    var right = document.getElementById('lp-right');
    var board = document.getElementById('lp-board');
    function lawByKey(k) {
      for (var i = 0; i < LAWS.length; i++) { if (LAWS[i].k === k) return LAWS[i]; }
      return null;
    }
    function render1() {
      left.innerHTML = '';
      CASES.forEach(function (C) {
        var b = document.createElement('button');
        b.className = 'choice' + (matched[C.k] ? ' correct' : (selL === C.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = C.t + (matched[C.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已配对 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[C.k]) return;
          selL = C.k;
          out1.className = 'result warn';
          out1.innerHTML = '<strong>你选了「' + C.t + '」。</strong>现在到右边点一部你认为管这件事的法律。';
          render1();
        });
        left.appendChild(b);
      });
      right.innerHTML = '';
      LAWS.forEach(function (L) {
        var b = document.createElement('button');
        b.className = 'choice' + (matched[L.k] ? ' correct' : '');
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + L.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + L.what + '</span>' +
          (matched[L.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">配对成功 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (matched[L.k]) return;
          if (!selL) {
            out1.className = 'result warn';
            out1.innerHTML = '先到左边点一个情境，再回到右边点法律。' +
              '<br><span style="color:var(--muted)">还可以试试：先想这件事最怕出什么问题，再看哪部法律管的是这件事。</span>';
            return;
          }
          if (selL === L.k) {
            var CL0 = null;
            for (var t = 0; t < CASES.length; t++) { if (CASES[t].k === selL) CL0 = CASES[t]; }
            matched[L.k] = true;
            selL = null;
            out1.className = 'result';
            out1.innerHTML = '<strong>配对成功：' + (CL0 ? CL0.t : '') + ' —— ' + L.n + '</strong>' + L.why;
            var n = Object.keys(matched).length;
            if (n === LAWS.length) {
              out1.innerHTML += '<br><br><strong>五组都配对了。</strong>你会发现，上学、出行、买东西、保护环境、处理日常纠纷，' +
                '背后都有一部法律在守护。法律不是远处的条文，它就在我们每天走过的路上。';
            }
          } else {
            var CL = null;
            for (var i = 0; i < CASES.length; i++) { if (CASES[i].k === selL) CL = CASES[i]; }
            var LL = lawByKey(L.k);
            out1.className = 'result warn';
            out1.innerHTML = '<strong>「' + LL.n + '」管的主要不是这件事。</strong>' +
              '这样可能会：把不同法律管的事情记串了。' + LL.tip +
              '<br><span style="color:var(--muted)">你选的情境是：' + (CL ? CL.t : '') + '</span>';
          }
          render1();
        });
        right.appendChild(b);
      });
      board.textContent = '已经配对 ' + Object.keys(matched).length + ' / ' + LAWS.length + ' 组';
    }
    render1();
  }

  /* ---------- 3. ★「遇到困难该找谁」对照台 ---------- */
  var SEEK = __SEEK_JSON__;
  var POWERS = __POWERS_JSON__;
  var stage2 = document.getElementById('sk-stage');
  if (stage2) {
    var selS = null;
    var done2 = {};
    var out2 = document.getElementById('sk-out');
    var caseBox = document.getElementById('sk-cases');
    var powerBox = document.getElementById('sk-powers');
    var board2 = document.getElementById('sk-board');
    function render2() {
      caseBox.innerHTML = '';
      SEEK.forEach(function (S) {
        var b = document.createElement('button');
        b.className = 'choice' + (done2[S.k] ? ' correct' : (selS === S.k ? ' selected' : ''));
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + S.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + S.case + '</span>' +
          (done2[S.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">已找到守护者：' + S.who + ' ✓</span>' : '');
        b.addEventListener('click', function () {
          if (done2[S.k]) return;
          selS = S.k;
          out2.className = 'result warn';
          out2.innerHTML = '<strong>「' + S.case + '」</strong>现在到右边点一类你认为最该找的保护力量。';
          render2();
        });
        caseBox.appendChild(b);
      });
      powerBox.innerHTML = '';
      POWERS.forEach(function (P) {
        var b = document.createElement('button');
        b.className = 'choice' + (done2[P.k] ? ' correct' : '');
        b.style.textAlign = 'left';
        b.innerHTML = '<strong>' + P.n + '</strong><br><span style="color:var(--muted);font-size:14px">' + P.d + '</span>' +
          (done2[P.k] ? '<br><span style="color:var(--accent-deep);font-size:14px">配对成功 ✓</span>' : '');
        b.addEventListener('click', function () {
          if (done2[P.k]) return;
          if (!selS) {
            out2.className = 'result warn';
            out2.innerHTML = '先到左边点一个情境，再回到右边点保护力量。' +
              '<br><span style="color:var(--muted)">还可以试试：先问自己一句，这件事最该由谁来管。</span>';
            return;
          }
          if (selS === P.k) {
            done2[P.k] = true;
            var S = null;
            for (var i = 0; i < SEEK.length; i++) { if (SEEK[i].k === selS) S = SEEK[i]; }
            selS = null;
            out2.className = 'result';
            out2.innerHTML = '<strong>找到守护者了：' + S.who + '。</strong>' + S.how;
            if (Object.keys(done2).length === SEEK.length) {
              out2.innerHTML += '<br><br><strong>六个情境都找到了守护者。</strong>' +
                '《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，' +
                '家庭保护、学校保护、社会保护、网络保护、政府保护和司法保护，六道保护一起撑着这把伞。';
            }
          } else {
            var SS = null;
            for (var j = 0; j < SEEK.length; j++) { if (SEEK[j].k === selS) SS = SEEK[j]; }
            out2.className = 'result warn';
            out2.innerHTML = '<strong>这件事更该找「' + SS.who + '」。</strong>' +
              '这样可能会：找错了人，事情多绕一圈还耽误时间。' + SS.tip;
          }
          render2();
        });
        powerBox.appendChild(b);
      });
      board2.textContent = '已经找到守护者 ' + Object.keys(done2).length + ' / ' + SEEK.length + ' 个情境';
    }
    render2();
  }

  /* ---------- 4. 「我的守护锦囊」生成台 ---------- */
  var KIT = __KIT_JSON__;
  var stage3 = document.getElementById('gk-stage');
  if (stage3) {
    var pick = { c: null, p: null, w: null };
    var out3 = document.getElementById('gk-out');
    var panel3 = document.getElementById('gk-panel');
    function caseByKey(k) {
      for (var i = 0; i < KIT.cases.length; i++) { if (KIT.cases[i].k === k) return KIT.cases[i]; }
      return null;
    }
    function render3() {
      var html = '<div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 我想先想清楚这个情境</div><div class="grid grid-2">';
      KIT.cases.forEach(function (C) {
        html += '<button class="choice' + (pick.c === C.k ? ' selected' : '') +
          '" data-gk-case="' + C.k + '" style="text-align:left">' + C.n + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 我第一个会找的人</div><div class="grid">';
      KIT.persons.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.p === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-gk-person="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第三步 · 我打算怎么说清楚</div><div class="grid">';
      KIT.words.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.w === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-gk-word="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-gk-case]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.c = b.dataset.gkCase; render3();
          out3.className = 'result warn';
          out3.textContent = '情境选好了，接着选第二步：你第一个会找谁。';
        });
      });
      panel3.querySelectorAll('[data-gk-person]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.p = parseInt(b.dataset.gkPerson, 10);
          var o = KIT.persons[pick.p];
          out3.className = 'result' + (o.ok ? '' : ' warn');
          out3.innerHTML = (o.ok ? '<strong>这一步想得对。</strong>' : '<strong>这一步还可以再想想。</strong>') + o.why;
          render3();
        });
      });
      panel3.querySelectorAll('[data-gk-word]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.w = parseInt(b.dataset.gkWord, 10);
          render3();
          if (pick.c === null || pick.p === null) {
            out3.className = 'result warn';
            out3.textContent = '三步还没选完，先把前面的补齐。';
            return;
          }
          var C = caseByKey(pick.c);
          var P = KIT.persons[pick.p];
          var W = KIT.words[pick.w];
          var okN = (P.ok ? 1 : 0) + (W.ok ? 1 : 0);
          out3.className = 'result' + (okN === 2 ? '' : ' warn');
          out3.innerHTML = '<strong>我的守护锦囊 · ' + C.n + '</strong><br>' +
            '第一步：' + C.n + '<br>第二步：' + P.t + '<br>第三步：' + W.t +
            '<br><span style="color:var(--muted)">' + (okN === 2
              ? '想得清楚，也找对了人。把这张锦囊抄进小本子，再讲给同桌听一遍。'
              : '还可以再想一想：第一个该告诉的人是父母或者老师；说的时候要讲清时间、地点和经过。换一个再试一次。') + '</span>';
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__LAWS_JSON__', json.dumps(LAWS, ensure_ascii=False))
             .replace('__CASES_JSON__', json.dumps(
                 [{"k": "l3", "t": "买到过期的食品，商家不肯处理。"},
                  {"k": "l1", "t": "每天到学校上课，课本和课程都有人管。"},
                  {"k": "l5", "t": "捡到别人丢的钱包，应当归还。"},
                  {"k": "l2", "t": "过马路要看交通信号灯，走斑马线。"},
                  {"k": "l4", "t": "小区的河水变黑了，工厂不该往河里排污。"}], ensure_ascii=False))
             .replace('__SEEK_JSON__', json.dumps(
                 [SEEK[2], SEEK[0], SEEK[5], SEEK[3], SEEK[1], SEEK[4]], ensure_ascii=False))
             .replace('__POWERS_JSON__', json.dumps(
                 [{"k": s["k"], "n": s["who"], "d": d} for s, d in [
                     (SEEK[3], "为我们营造健康的网络环境。"),
                     (SEEK[0], "父母或者其他监护人应当保护我们。"),
                     (SEEK[5], "公安机关、人民法院等依法保护我们。"),
                     (SEEK[1], "学校应当关心、爱护并教育我们。"),
                     (SEEK[4], "有关部门依法履行职责、保护我们。"),
                     (SEEK[2], "全社会都要为我们营造安全的环境。")]], ensure_ascii=False))
             .replace('__KIT_JSON__', json.dumps(KIT, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：法律离我们有多近？", TTS["pretest"], [
        {"q": "下面哪一句话说准了法律的特点？",
         "options": [("法律靠国家强制力保证实施，对全体社会成员都有约束力", True),
                     ("法律只是一种建议，听不听都可以", False),
                     ("法律只约束大人，不约束小学生", False)],
         "explain": "法律是由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力的行为规范。"
                    "靠国家强制力保证实施，正是它区别于道德和纪律的最主要特征。"
                    "<strong>错因提醒：</strong>常见错误是把法律当成建议，或者<strong>误认为</strong>法律只管大人——法律面前人人平等，小学生同样在法律保护之中。",},
        {"q": "在我国众多法律里，宪法处于什么位置？",
         "options": [("宪法是国家的根本法，具有最高的法律效力", True),
                     ("宪法和其他法律一样，只管某一件小事", False),
                     ("宪法是一门建议，其他法律不用听", False)],
         "explain": "宪法是国家的根本法，是治国安邦的总章程，具有最高的法律效力，一切法律、行政法规和地方性法规都不得同宪法相抵触。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>宪法也是一部只管某件事的具体法律，其实它规定的是国家生活中最根本、最重要的问题。",},
        {"q": "遇到自己解决不了的困难，下面哪种做法更合适？",
         "options": [("及时告诉父母、老师，说清楚时间、地点和经过，必要时请其他力量帮助", True),
                     ("谁也不告诉，自己扛着", False),
                     ("自己去找对方算账，把气出回来", False)],
         "explain": "遇到困难及时说出来，找对人、说清楚，才是对自己最好的保护。父母和老师是最先可以依靠的人，情况紧急还可以拨打报警电话一百一十。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>说出来就是「打小报告」，其实求助是为了让自己安全，也让事情不再变糟。",}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "法律就在我们身边：它一直在守护我们", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在过马路、上学、买东西、和同学相处（And）；可要问「法律和我到底有什么关系」，很多同学只能说出模糊的印象（But）；所以这节课先把法律是什么、它凭什么管用弄清（Therefore）。</p>
        </div>
        <p style="font-size:17px;margin:0 0 12px"><strong>法律</strong>是由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力的行为规范。</p>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>由国家制定或认可：</strong>法律不是谁想定就能定，它来自国家。</div></div>
          <div class="step"><span class="n">2</span><div><strong>靠国家强制力保证实施：</strong>这一点把法律和道德、纪律区分开来。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>对全体社会成员有普遍约束力：</strong>法律面前人人平等，没有人可以例外。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="法律就在身边扁平插画：校园门口、斑马线与信号灯、文具店、分类垃圾桶、社区公告栏等抽象几何场景，用立柱与盾牌符号表示法律的守护，附中文标注">
          <figcaption>概念图：从家到学校，从马路到小店，法律就在我们每天经过的地方 · 中性简洁扁平插画</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>生活里，它一直在</strong></p>
          <p style="color:var(--muted)">上学有《中华人民共和国义务教育法》；过马路有《中华人民共和国道路交通安全法》；买东西有《中华人民共和国消费者权益保护法》；保护环境有《中华人民共和国环境保护法》。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>法律离我们很远，只有犯法的人才跟法律打交道；也有的同学把道德和法律<strong>搞混</strong>，觉得违反了道德就等于违法。其实法律是底线，道德是更高的要求，两者都在守护我们，但不是一回事。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同一个路口，红灯亮着，所有人都在等——没有人站在旁边喊，大家却都停下来。这时候起作用的不只是习惯，还有法律。"},
    {"lens": "解释它", "text": "为什么法律说话更算数？因为它背后有国家强制力。道德靠我们心里的认同和大家的评价，法律则由国家保证实施。"},
    {"lens": "迁移它", "text": "这套想法在班里也成立：班规能约束大家，是因为我们一起认同它；而法律无论你认不认同，都必须遵守——这就是它最硬的地方。"},
])}
    ''', tag="概念一"))

    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "动手一：法律就在身边，把情境和法律配起来", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点左边一个<strong>生活情境</strong>，再点右边一部<strong>管这件事的法律</strong>。配对了会连起来，配错了会告诉你错在哪里。</p>
        <div class="lab-panel">
          <div id="lp-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">点击左侧情境，再点右侧法律进行配对</div>
            <div class="grid grid-2">
              <div id="lp-left"></div>
              <div id="lp-right"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">配对进度</span><span class="v" id="lp-board">已经配对 0 / 5 组</span></div>
          </div>
          <p class="result warn" id="lp-out" style="margin-top:12px">先点左边一个情境。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">⚖️</span><div><strong>配完回头看：</strong>五部法律管的事情不一样，但它们做的是同一件事——把「应该怎样」变成「必须怎样」。这就是法律和一般约定的区别。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "宪法是国家的根本法，具有最高的法律效力", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要弄清楚宪法？</strong></p>
          <p style="color:var(--muted)">我们已经知道身边有很多部法律（And）；但这么多法律里，谁说了算、有没有一部总章程（But）；所以这节课要弄清宪法的地位和最高法律效力（Therefore）。</p>
        </div>
        <div class="inner-card">
          <p><strong>宪法是国家的根本法，是治国安邦的总章程</strong></p>
          <p style="color:var(--muted)">它规定的是国家生活中最根本、最重要的问题：国家的性质、根本制度、根本任务、公民的基本权利和义务、国家机构的组织及其职权。</p>
        </div>
        <div class="inner-card">
          <p><strong>宪法具有最高的法律效力</strong></p>
          <p style="color:var(--muted)">一切法律、行政法规和地方性法规都不得同宪法相抵触；任何组织或者个人都不得有超越宪法和法律的特权。</p>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="法律效力层级抽象示意：自上而下分层标注宪法、法律、行政法规、地方性法规，层与层之间有向下箭头与不得抵触提示，旁边用盾牌和天平的抽象符号表示守护，附中文标注">
          <figcaption>示意：宪法在上，一切法律、行政法规和地方性法规都不得同宪法相抵触 · 抽象示意图，不按比例</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>三条可以随身带走的知识</strong></p>
          <p style="color:var(--muted)">① 宪法的制定和修改程序比其他法律更加严格，它的修改要由全国人民代表大会以全体代表的三分之二以上的多数通过。② 一切组织和个人都必须以宪法为根本的活动准则。③ 我国把十二月四日设立为国家宪法日。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>宪法也是一部只管某件小事的具体法律；也有的同学觉得宪法很高很远，跟小学生没关系。其实我们上学、被保护、被尊重，背后都有宪法确立的保障。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "五部不同的法律管五件不同的事，却都写着同样的开头——依据宪法。它们站在同一块地基上。"},
    {"lens": "解释它", "text": "为什么宪法有最高的法律效力？因为如果每部法律都能各说各的，规则就会互相打架。宪法定的是最根本的规则，其他法律都必须与它一致。"},
    {"lens": "迁移它", "text": "这就像一个小组做任务，先定好总目标，再分工写各自的方案；分工可以不一样，但都不能偏离总目标。"},
])}
    ''', tag="概念二"))

    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "★动手二：遇到困难该找谁——守护者对照台", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">先点左边一个<strong>困难情境</strong>，再点右边你认为最该找的那一类<strong>保护力量</strong>。配对了，会告诉你该找谁、可以怎么做。</p>
        <div class="lab-panel">
          <div id="sk-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">点击左侧情境，再点右侧保护力量进行配对</div>
            <div class="grid grid-2">
              <div id="sk-cases"></div>
              <div id="sk-powers"></div>
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">守护者配对</span><span class="v" id="sk-board">已经找到守护者 0 / 6 个情境</span></div>
          </div>
          <p class="result warn" id="sk-out" style="margin-top:12px">先点左边一个情境。</p>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛡️</span><div><strong>记住一句话：</strong>遇到困难不是丢人的事，及时说出去才是保护自己。家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护，六道保护一起撑着这把伞。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：求助方案校对，国家为我们撑起保护伞", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>班里要为同学们做一份求助指引，四位同学写了四条方案。请你当一次校对员，判断哪一条可行、哪一条必须改。</p>
        </div>
        <div class="inner-card">
          <p><strong>《中华人民共和国未成年人保护法》保护谁、保护什么</strong></p>
          <p style="color:var(--muted)">它专门保护未满十八周岁的公民，确立了家庭保护、学校保护、社会保护、网络保护、政府保护和司法保护；保护未成年人是全社会的共同责任，坚持最有利于未成年人的原则。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>方案一（必须改）：</strong>「遇到困难先自己扛着，别告诉任何人。」这样可能会：让事情拖得更久、变得更严重。</div></div>
          <div class="step"><span class="n">2</span><div><strong>方案二（可行）：</strong>把事情告诉父母和老师，说清楚时间、地点和事情的经过。</div></div>
          <div class="step"><span class="n">3</span><div><strong>方案三（可行）：</strong>拨打报警电话一百一十，或者拨打一二三四五政务服务便民热线、一二三五五青少年服务台求助。</div></div>
          <div class="step"><span class="n green">4</span><div><strong>方案四（必须改）：</strong>「自己去找对方算账。」这样可能会：既伤了别人，也伤了自己，还可能让自己从被欺负的一方变成做错事的一方。</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学把《中华人民共和国未成年人保护法》和《中华人民共和国宪法》<strong>搞混</strong>了。宪法是国家的根本法；未成年人保护法是专门保护未满十八周岁公民的一部法律，它把宪法的精神落到了我们的日常生活里。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三句话，藏着三个容易想歪的地方", TTS["conceptest-1"], [
        {"q": "关于法律和道德的关系，下面哪句话说得准确？",
         "options": [("两者都是行为规范，但法律靠国家强制力保证实施", True),
                     ("违反道德就等于违法，两者是一回事", False),
                     ("道德可以代替法律，法律可有可无", False)],
         "explain": "法律和道德都是行为规范，也都约束人的行为；区别在于法律靠国家强制力保证实施，对全体社会成员具有普遍约束力。"
                    "<strong>错因提醒：</strong>常见错误是把道德和法律<strong>搞混</strong>，以为违反道德就等于违法。其实法律是底线，道德是更高的要求。",},
        {"q": "关于宪法，下面哪句话说得准确？",
         "options": [("宪法是国家的根本法，一切法律都不得同宪法相抵触", True),
                     ("宪法和普通法律地位一样，可以互相抵触", False),
                     ("宪法只管国家大事，和小学生没有关系", False)],
         "explain": "宪法是国家的根本法，具有最高的法律效力；一切法律、行政法规和地方性法规都不得同宪法相抵触。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>宪法离自己很远。其实我们能上学、能被保护，背后都有宪法确立的保障。",},
        {"q": "小刚被同学反复起侮辱性外号，他先告诉了班主任，老师出面制止了这件事。这体现了哪一类保护？",
         "options": [("学校保护", True),
                     ("司法保护", False),
                     ("网络保护", False)],
         "explain": "学校应当关心、爱护学生，制止欺负同学的行为，这属于《中华人民共和国未成年人保护法》确立的学校保护。"
                    "<strong>错因提醒：</strong>容易把六类保护<strong>搞混</strong>。可以记住：在家里是家庭保护，在学校是学校保护，在社会上是社会保护。",}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：我的守护锦囊生成台", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步各选一个：<strong>我想先想清楚的情境 → 我第一个会找的人 → 我打算怎么说清楚</strong>。选完，你就有了自己的守护锦囊。</p>
        <div class="lab-panel">
          <div id="gk-stage"></div>
          <div id="gk-panel"></div>
          <p class="result warn" id="gk-out" style="margin-top:12px">从第一步开始选。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来：</strong></p>
          <p style="color:var(--muted)">想一想，如果你真的遇到麻烦，你最先会告诉谁？把那个人的名字和你打算说的第一句话写下来，收在自己的小本子里。</p>
          <textarea id="syn-answer" rows="3" placeholder="我第一个会告诉……，我打算说：……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新情境，方法还用得上吗", TTS["posttest"], [
        {"q": "放学路上，一位陌生的大人一直跟着小丽，还说让她跟着走。小丽最合适的做法是：",
         "options": [("马上走向人多明亮的地方，找可靠的成年人帮忙，并及时告诉父母和老师，情况紧急可拨打报警电话一百一十", True),
                     ("跟他走，看看他到底想做什么", False),
                     ("躲在没人的角落里不吭声", False)],
         "explain": "社会保护要求全社会为未成年人营造安全的环境；遇到这种情况，要先让自己处在大人的视线和人群之中，再及时求助。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>「不理他就没事了」。其实躲起来反而更危险，及时求助才是最有效的办法。",},
        {"q": "小宇的爸爸生气时说不让他上学了。从法律的角度看，下面哪种说法更合适？",
         "options": [("保障未成年人受教育的权利属于家庭保护的要求，可以请老师和学校、社区帮助沟通", True),
                     ("上不上学是家里的事，谁也不能管", False),
                     ("不上学正好，可以在家玩", False)],
         "explain": "父母或者其他监护人应当保护未成年人，也要保障我们受教育的权利，这属于家庭保护的要求；遇到说不通的情况，可以请老师、学校和社区帮助。"
                    "<strong>错因提醒：</strong>常见错误是把「家里的事」和「法律管不着」<strong>搞混</strong>。保护未成年人，全社会都有责任。",},
        {"q": "关于遇到困难该找谁，下面哪句最值得记在心里？",
         "options": [("先告诉父母或者老师，说清时间、地点和经过，必要时还可以拨打公开的求助电话", True),
                     ("谁都不告诉，等事情自己过去", False),
                     ("先在班级群里把对方的信息发出来让大家评理", False)],
         "explain": "把事实说清楚，找对人，是解决问题最快也最稳的路。"
                    "<strong>错因提醒：</strong>把对方的信息公开出去，自己也可能会做错事。还可以试试：先把情况告诉大人，再决定怎么处理。",}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：法律在身边、宪法是根本法、困难找对人", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>法律就在身边：</strong>由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>宪法是根本法：</strong>规定国家生活中最根本、最重要的问题，具有最高的法律效力，一切法律都不得同宪法相抵触。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>国家撑起保护伞：</strong>《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，确立六大保护。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>困难找对人：</strong>先告诉父母或老师，说清时间、地点和经过；必要时拨打公开的求助电话。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>法律身边守，宪法在最高；六道保护伞，一撑就牢靠；遇事别硬扛，说清找人早。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「宪法」和「未成年人保护法」这两个词，给家里人讲一件事，说清楚它们的区别在哪里。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>六类保护各一个身边的例子，做成六行小清单，贴在自己的书桌上。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出法律区别于道德和纪律的最主要特征是什么。",
            "写出宪法在我国法律体系中的地位，以及它的法律效力有什么特点。",
            "写出《中华人民共和国未成年人保护法》专门保护的人群，以及它确立的六类保护。",
        ],
        [
            "把六类保护各举一个身边的例子，写成六行小清单；每一行都要写清楚「谁在保护」和「怎么保护」。",
            "把本课出现的三个名称抄写一遍，注意写全称：《中华人民共和国宪法》《中华人民共和国未成年人保护法》《中华人民共和国义务教育法》。",
        ],
        [
            "为自己做一份守护锦囊：写清楚三个情境、第一个该告诉的人，以及你打算怎么把话说清楚，做完在班里和同学交流。",
            "采访一位家里人：问问他小时候遇到困难会找谁帮忙，和今天的做法比一比，说说你的发现。",
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
    "title": "我们的守护者",
    "name_en": "Our Guardians",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "moral-cultivation",
    "domain_cn": "道德修养",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学六年级的道德与法治课，正对统编六上第 1 单元「我们的守护者」（感受生活中的法律、宪法是根本法），落到三件事上。第一件是感受生活中的法律：法律是由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力的行为规范，其中「靠国家强制力保证实施」是它区别于道德和纪律的最主要特征；上学有《中华人民共和国义务教育法》，过马路有《中华人民共和国道路交通安全法》，买东西有《中华人民共和国消费者权益保护法》，保护环境有《中华人民共和国环境保护法》，日常纠纷有《中华人民共和国民法典》——法律就在我们身边。第二件是宪法是根本法：宪法规定国家生活中最根本、最重要的问题，具有最高的法律效力，一切法律、行政法规和地方性法规都不得同宪法相抵触，任何组织或者个人都不得有超越宪法和法律的特权，它的制定和修改程序比其他法律更加严格，一切组织和个人都必须以宪法为根本的活动准则，十二月四日是国家宪法日。第三件是国家为我们撑起的保护伞：《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，确立了家庭保护、学校保护、社会保护、网络保护、政府保护和司法保护，保护未成年人是全社会的共同责任，坚持最有利于未成年人的原则。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是「法律就在身边」情境配对台（五个生活情境与五部管这件事的法律配对）、动手二是本课核心模拟「遇到困难该找谁」对照台（六个真实情境与六类保护力量配对，配出该找谁与可以怎么做）、综合任务是「我的守护锦囊」生成台（选情境 → 选第一个该找的人 → 选怎么说清楚，合成一张锦囊卡）。全课表述从严：法律名称一律写全称，《中华人民共和国宪法》《中华人民共和国未成年人保护法》两种名称严格区分；不出现任何法律条文编号，不臆造案例细节，求助渠道只用常识层面、社会公认的公开渠道；插图一律为中性简洁扁平教学插画，不使用真人照片风格，不绘制国旗、国徽、宪法文本封面等易失真、不庄重的图形，涉及国家与法律改用立柱、拱门、盾牌、天平、书页线条等抽象符号与地标性建筑抽象剪影。",
    "tags": ["我们的守护者", "感受生活中的法律", "宪法是根本法", "最高法律效力", "未成年人保护法", "六大保护", "六年级", "道德修养"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学「道德修养」——自律自强，孝敬长辈，友善待人，有正确的价值取向；对应统编《道德与法治》六年级上册 第1单元「我们的守护者」：感受生活中的法律、宪法是根本法。",
    "hero_question": "当我们还小的时候，是谁在悄悄守护我们？",
    "hero_alt": "我们的守护者知识结构图：法律就在身边、宪法是国家的根本法、国家撑起的保护伞 三栏，用立柱拱门、盾牌天平、撑开的伞等抽象符号表示，附中文标注，不含国旗国徽与宪法文本图形",
    "hero_caption": "我们的守护者：法律在身边 · 宪法是国家的根本法（最高法律效力）· 未成年人保护法撑起六道保护",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "法律离我们到底有多近？", "d": "从上学、过马路到买东西，法律都在哪里", "v": "法律离我们到底有多近"},
        {"t": "为什么说宪法是国家的根本法？", "d": "最高的法律效力到底是什么意思", "v": "为什么说宪法是国家的根本法"},
        {"t": "遇到困难时，我们该找谁？", "d": "家庭、学校、社会、网络、政府、司法六道保护", "v": "遇到困难时我们该找谁"},
        {"t": "那部专门保护我们的法律都保护了什么？", "d": "《中华人民共和国未成年人保护法》保护谁、怎么保护", "v": "那部专门保护我们的法律都保护了什么"},
    ],
    "objectives": [
        "能说出法律是由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力的行为规范，并举出生活中与法律有关的例子",
        "能说出宪法是国家的根本法、具有最高的法律效力，知道一切法律、行政法规和地方性法规都不得同宪法相抵触，知道十二月四日是国家宪法日",
        "能说出《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，并说出家庭保护、学校保护、社会保护、网络保护、政府保护和司法保护",
        "遇到困难时能找到合适的人和渠道求助，知道要把时间、地点和经过说清楚，不做自己硬扛或者私下算账这样可能让事情变糟的选择",
    ],
    "objectives_plain": [
        "能说出法律是什么，并举出生活中与法律有关的例子",
        "能说出宪法是国家的根本法、具有最高的法律效力",
        "能说出《中华人民共和国未成年人保护法》保护谁，以及它确立的六类保护",
        "遇到困难时知道该找谁，也知道怎么把事情说清楚",
    ],
    "standards": [
        {"content": "自律自强，孝敬长辈，友善待人，有正确的价值取向。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学 道德修养"},
        {"content": "感受生活中的法律；宪法是根本法",
         "source": "统编《道德与法治》六年级上册 第1单元「我们的守护者」"},
    ],
    "prereqs": ["pol-e-g5-u4"],
    "prereqs_name": "骄人祖先 灿烂文化",
    "prereqs_meta": "pol-e-g5-u4",
    "leads_to": ["pol-e-g6-u2"],
    "next_meta": "pol-e-g6-u2",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "三件事：法律离我们多近、宪法为什么是根本法、遇到困难该找谁。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把一件和法律有关的事说清楚。",
        "objectives": "看清四件事：法律是什么、宪法的地位、未成年人保护法保护谁、困难该找谁。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "法律的三个特点里，最关键的是「靠国家强制力保证实施」——它把法律和道德、纪律区分开。",
        "lab-1": "先点情境，再点法律。想一想：这件事最怕出什么问题，哪部法律管的就是这件事。",
        "module-2": "宪法是国家的根本法，具有最高的法律效力；一切法律都不得同宪法相抵触。",
        "lab-2": "本课最重要的台子：先点情境，再点最该找的那类保护力量。遇到困难要及时说出来。",
        "worked-example": "四条求助方案：两条可行、两条必须改。留意未成年人保护法和宪法不能搞混。",
        "conceptest-1": "三句话里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步做锦囊：情境 → 第一个该找的人 → 怎么说清楚。",
        "posttest": "出现了放学路上、家里和网络上的事，看看今天的方法还用不用得上。",
        "summary": "四句话：法律在身边、宪法是根本法、六道保护、困难找对人。",
        "homework": "三层小任务，先做前两层；第二层要把法律名称写全称。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治「道德修养」板块在六年级的空缺，正对统编六上第 1 单元「我们的守护者」（感受生活中的法律、宪法是根本法）。六年级学生已经知道生活中有规则，也听过「法律」「宪法」这些词，但对「法律和我到底有什么关系」「宪法凭什么最高」「遇到困难该找谁」往往只有零碎印象，甚至会把道德和法律、未成年人保护法和宪法混为一谈。所以全课不讲口号、不背条文，而把内容换成能核对、能复述的定位与可操作的活动。第一层是「感受生活中的法律」：给出法律的定义与三个特点——由国家制定或认可、靠国家强制力保证实施、对全体社会成员具有普遍约束力，并明确指出「靠国家强制力保证实施」是它区别于道德和纪律的最主要特征；再用上学、过马路、买东西、保护环境、拾得遗失物五个生活情境，把《中华人民共和国义务教育法》《中华人民共和国道路交通安全法》《中华人民共和国消费者权益保护法》《中华人民共和国环境保护法》《中华人民共和国民法典》一一对上去，让学生看见法律就在每天经过的地方；同时纠正两个高频误解：误认为法律离自己很远、误认为违反道德就等于违法。第二层是「宪法是根本法」：宪法是国家的根本法，是治国安邦的总章程，规定国家生活中最根本、最重要的问题；具有最高的法律效力，一切法律、行政法规和地方性法规都不得同宪法相抵触，任何组织或者个人都不得有超越宪法和法律的特权；它的制定和修改程序比其他法律更加严格，一切组织和个人都必须以宪法为根本的活动准则；十二月四日是国家宪法日。第三层是「国家为我们撑起的保护伞」：《中华人民共和国未成年人保护法》专门保护未满十八周岁的公民，确立了家庭保护、学校保护、社会保护、网络保护、政府保护和司法保护，保护未成年人是全社会的共同责任，坚持最有利于未成年人的原则。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是「法律就在身边」情境配对台，五个生活情境与五部管这件事的法律配对，配错给出错因与下一步提示；动手二是本课核心模拟「遇到困难该找谁」对照台，六个真实情境与六类保护力量配对，配对成功即给出该找谁与可以怎么做；综合任务是「我的守护锦囊」生成台，学生按「情境 → 第一个该找的人 → 怎么说清楚」各选一步，由系统合成一张可以抄进小本子的锦囊卡。全课在表述上从严把关：法律名称一律写全称，《中华人民共和国宪法》与《中华人民共和国未成年人保护法》严格区分；不出现任何法律条文编号，不臆造案例细节与办理流程，求助渠道只用常识层面、社会公认的公开渠道（告诉父母和老师、请学校或社区帮助、一百一十报警电话、一二三四五政务服务便民热线、一二三五五青少年服务台）；插图一律为中性简洁扁平教学插画，不使用真人照片风格，不绘制国旗、国徽、宪法文本封面等易失真、不庄重的图形，涉及国家与法律改用立柱、拱门、盾牌、天平、书页线条等抽象符号与地标性建筑抽象剪影。",
    "plan_table": """| 1 | cover | 我们的守护者 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：法律离我们有多近？ | 起·前测（暴露已有印象与混淆点） |
| 5 | concept | 法律就在我们身边：它一直在守护我们 | 承·概念一（法律的定义与三个特点） |
| 6 | interactive | 动手一：法律就在身边，把情境和法律配起来 | 承·配对台（5 情境 × 5 部法律） |
| 7 | concept | 宪法是国家的根本法，具有最高的法律效力 | 承·概念二（宪法的地位与效力） |
| 8 | interactive | ★动手二：遇到困难该找谁——守护者对照台 | 承·核心模拟（6 情境 × 6 类保护力量） |
| 9 | concept | 例题示范：求助方案校对，国家为我们撑起保护伞 | 转·重难点突破（未成年人保护法 + 方案校对） |
| 10 | quiz | 概念测试：三句话，藏着三个容易想歪的地方 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：我的守护锦囊生成台 | 合·迁移应用（三步合成锦囊卡） |
| 12 | quiz | 后测：换几个新情境，方法还用得上吗 | 合·后测 |
| 13 | summary | 小结：法律在身边、宪法是根本法、困难找对人 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：法律就在身边 / 宪法是国家的根本法 / 国家撑起的保护伞 三栏，用立柱拱门、盾牌天平、撑开的伞等抽象符号表示，附中文标注\n- P5 法律就在身边概念图（已生成）：校园门口、斑马线与信号灯、文具店、分类垃圾桶、社区公告栏等抽象几何场景，附中文标注\n- P7 法律效力层级抽象示意图（已生成）：自上而下分层标注宪法、法律、行政法规、地方性法规，并标注「都不得同宪法相抵触」，另标注「抽象示意图，不按比例」\n- ★ 全课不绘制国旗、国徽、宪法文本封面等易失真、不庄重的图形；涉及国家与法律仅用立柱、拱门、盾牌、天平、书页线条等抽象符号与地标性建筑抽象剪影\n- ★ 表述口径统一：法律名称一律写全称；不出现任何法律条文编号；不臆造案例细节；求助渠道只用公开、公认的常识渠道\n- 三张图均为中性简洁扁平教学插画，不使用真人照片风格，不含可识别的真实人物",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
