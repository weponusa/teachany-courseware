# -*- coding: utf-8 -*-
"""小学道德与法治 · 法律保护我们健康成长（六年级上 · 第4单元）—— 补齐知识树空缺

学科语气（道德与法治）：从学生每天真实会遇到的处境讲起，先给可操作的自护办法，
再讲法律为什么这样规定；结论落在「先做什么、再做什么」，不做条文背诵，不渲染危险。

★ 表述红线（最高优先级，全课统一口径，任何地方不得含糊）：
  · 法律名称一律写规范全称：《中华人民共和国未成年人保护法》《中华人民共和国预防未成年人犯罪法》
    《中华人民共和国家庭教育促进法》。绝不写成「未成年人保护条例」「青少年保护法」「预防法」这类
    凭印象改写或简称当正式名称的写法。
  · 一律不出现任何法律条文编号（不写「第几条」「第几款」，只说「法律规定」「法律规定未成年人享有……」）。
  · 不臆造案件细节、不编造具体案件与处理流程；不涉及任何具体伤亡个案。所有情境一律写成
    「如果遇到……」，只讲假设中的应对办法，不写人名、地名、时间、结果。
  · 不张贴任何标签、不做任何临床或心理诊断式判断；不使用吓唬、恐吓性的表述，语气积极正面。
  · 求助渠道只写社会通行的三个号码：110 报警、120 急救、119 火警，并强调
    「第一时间告诉信任的大人（爸爸妈妈、老师、警察等）」是首要办法。
  · 不绘制国徽、法院徽章、国旗等图形；不出现真人照片风格；插图一律用盾牌、圆环、人物剪影、
    握手的抽象符号与地标性建筑抽象剪影表示。

内容落点（对应统编六上第 4 单元「法律保护我们健康成长」）：
  ① 我们受特殊保护：三部法律各管什么——《中华人民共和国未成年人保护法》保护未成年人身心健康、
     保障未成年人合法权益；《中华人民共和国预防未成年人犯罪法》保障未成年人身心健康、培养良好品行、
     有效预防未成年人违法犯罪；《中华人民共和国家庭教育促进法》明确父母或者其他监护人负责实施家庭教育，
     国家和社会为家庭教育提供指导、支持和服务。未成年人享有生存权、发展权、受保护权、参与权等权利，
     依法受到特殊、优先保护。
  ② 六大保护：家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护——保护未成年人，
     是家庭、学校、社会、网络、政府、司法各方面共同的责任。
  ③ 自我保护三步：先避险（马上离开不安全的地方，走到人多、有工作人员的地方）→ 找可信的大人
     （爸爸妈妈、老师、警察、店员、保安等）→ 记住求助渠道（110 报警、120 急救、119 火警）。
  ④ 知法守法，依法维权：知道法律的规定，不做法律禁止的事；有了不良行为要及时改正；
     自己的合法权益受到侵害时，可以请家长、老师帮助，依法维护自己的权益。

三个互动台子都能真操作（反馈一律写成「这样可能会……，还可以试试……」）：
  动手一 = ★核心模拟「遇到这种情况怎么办」判断台（4 个处境 × 自我保护三步，每步三选一，选对才走下一步）；
  动手二 = 「六大保护归属台」（6 个做法 × 判断属于哪一类保护）；
  综合任务 = 「我的自护卡」生成台（选处境 → 选最要紧的第一步 → 选要记牢的求助对象与渠道 → 合成自护卡）。
"""

import json

from science_builder import (
    p_cover, p_anchor, p_objectives, p_quiz, p_concept, p_interactive, p_summary, p_kg, p_tutor,
    p_homework, insight_box,
)

ID = "pol-e-g6-u4"
F1 = f'./assets/{ID}-fig1.webp'
F2 = f'./assets/{ID}-fig2.webp'

TTS = {
    "hero": "上一节课我们认识了我们的国家机构。这节课要讲的，是离我们自己最近的一件事：法律怎样保护我们健康成长。你有没有想过，为什么大人不能随便让我们辍学，为什么网上不能随便传播伤害我们的内容，为什么遇到危险的时候我们可以理直气壮地去求助？因为有一组专门保护未成年人的法律，一直在我们身边。这节课我们弄清楚三件事：法律为什么给我们特殊的保护，我们享有哪几项受保护的权利，还有——真正遇到危险的时候，第一步到底该做什么。",
    "problem-anchor": "开始之前，先选一个你真正想知道的问题：法律为什么要给我们特殊保护？我们享有哪些受保护的权利？遇到危险的时候我该怎么做？还是——平时怎么做才算知法守法？选好以后，就带着这个问题往下看。",
    "objectives": "这节课有四个小目标。第一，能说出保护我们的三部法律的规范全称，能说出它们各自是为什么制定的。第二，能说出未成年人享有生存权、发展权、受保护权、参与权等权利，依法受到特殊、优先保护；能说出家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护这六个方面。第三，能说清自我保护的三步：先避险，再找可信的大人，最后记住求助渠道，能说出 110 报警、120 急救、119 火警这三个号码分别在什么时候用。第四，能说出知法守法是每个人都要做的事，合法权益受到侵害时可以请家长、老师帮助，依法维护自己的权益。",
    "pretest": "先做三道小题，用你现在的想法选就行。选完马上能看到解释，选得不合适也没关系，正好知道要重点听哪里。",
    "module-1": "第一件事，我们受特殊保护。先记住三部法律的规范全称。第一部，《中华人民共和国未成年人保护法》，它是为了保护未成年人身心健康、保障未成年人合法权益而制定的，它从家庭、学校、社会、网络、政府、司法六个方面，为未成年人织起一张保护的网。第二部，《中华人民共和国预防未成年人犯罪法》，它是为了保障未成年人身心健康、培养未成年人良好品行、有效预防未成年人违法犯罪而制定的。第三部，《中华人民共和国家庭教育促进法》，它明确父母或者其他监护人负责实施家庭教育，国家和社会为家庭教育提供指导、支持和服务。那么，我们未成年人依法享有哪些权利呢？法律保障未成年人享有生存权、发展权、受保护权、参与权等权利，并给予特殊、优先保护。这里有三个容易想歪的地方：有的同学误认为保护未成年人只是家里的事，其实家庭、学校、社会、网络、政府、司法六个方面都有责任；有的同学把法律名称凭印象改写成「未成年人保护条例」，其实规范全称是《中华人民共和国未成年人保护法》，一个字都不能少；也有的同学误认为未成年人保护法只是保护，不讲责任，其实它同时告诉我们应当遵守什么。",
    "lab-1": "现在请你做一次判断。这里有四个可能遇到的处境，每个处境都要走三步：先避险、再找可信的大人、最后记住求助渠道。每一步请你先想一想，再在三个做法里选一个最合适的。选对了才能走下一步，选得不合适我会告诉你这样可能会有什么问题，还可以怎么想。",
    "module-2": "第二件事，自我保护的三步，还有知法守法。先说三步。第一步是先避险：不管遇到什么情况，第一件事都是让自己离开不安全的地方，走到人多、有工作人员的地方去——比如开着门的商店、银行、社区服务中心。第二步是找可信的大人：马上把事情告诉爸爸妈妈、老师，或者警察、店员、保安这些可以信任的大人，不要一个人扛着，也不要觉得这是在麻烦别人。第三步是记住求助渠道：110 是报警电话，遇到危及安全的情况可以拨打；120 是急救电话；119 是火警电话。记住当时的时间、地点和对方的特征，说给大人或者警察听，能帮上很大的忙。再说知法守法：知道法律的规定，我们才能更好地保护自己，也不会因为不懂而做错事。不做法律禁止的事；如果自己有了不良行为，要及时改正，别让它发展成更严重的问题。最后是依法维权：如果自己的合法权益受到侵害，可以请家长和老师帮助，依法维护自己的权益，不要自己冲动地去解决。这里有两个最容易想歪的地方：有的同学误认为自我保护就是自己冲上去跟对方较量，其实第一步永远是先避险，安全第一；也有的同学误认为把遇到的事说出来很丢人，其实及时告诉信任的大人，正是最管用的办法。",
    "lab-2": "接下来请你做一次归属判断。这里有六个做法，每一个都来自我们身边。请你判断它属于家庭保护、学校保护、社会保护、网络保护、政府保护还是司法保护。先读一读，再选一个，然后看解释。判断错了也没关系，正好知道要重点想哪一步。",
    "worked-example": "我们一起来做一次说法校对。班会课上，几位同学写了五条关于法律保护的说明，请你当一次校对员，判断哪一条准确、哪一条必须改。说法一：《中华人民共和国未成年人保护法》保护未成年人身心健康，保障未成年人合法权益。这条正确，注意法律名称要写全称，不能凭印象改写。说法二：保护未成年人只是家里的事，和学校、社会没有关系。这条要改。保护未成年人是家庭、学校、社会、网络、政府、司法各方面共同的责任，六个方面各有各的分工。说法三：遇到危险要先保护自己，及时告诉信任的大人。这条正确，这就是自我保护的第一步和第二步：先避险，再找可信的大人。说法四：只要自己没做坏事，就不用学法律。这条要改。知法守法是每个人都要做的事，知道法律的规定，才能更好地保护自己，也不会因为不懂而做错事。说法五：自己的合法权益受到侵害时，可以请家长和老师帮助，依法维护自己的权益。这条正确，依法维权是法律给我们的办法。这里有一个常见错误要提醒：有的同学把「自我保护」误认为「自己冲上去解决」，一遇到事情就想硬碰硬。记住，第一步永远是先避险，安全第一。",
    "conceptest-1": "接下来用三道题考考你，每道题里都藏着一个容易想歪的地方。请你读一读，选一个你认为合适的，再看解释。",
    "synthesis": "最后一件任务交给你：为自己做一张自护卡。下面分三步：先选一个你最想提前做准备的处境，再选出在这种情况下最要紧的第一步，最后选一选你要记牢的求助对象和求助渠道。三步选完，我会把它们拼成一张自护卡，你可以写上自己的名字，贴在书桌前。",
    "posttest": "最后一轮，换几个新的处境来考考你。这次会遇到一个人在家、网上收到奇怪的邀请，还有关于六大保护的说法，看看今天学的判断还用不用得上。",
    "summary": "这节课我们弄清楚四件事。第一，保护我们的三部法律：《中华人民共和国未成年人保护法》保护未成年人身心健康、保障未成年人合法权益；《中华人民共和国预防未成年人犯罪法》保障未成年人身心健康、培养良好品行、有效预防未成年人违法犯罪；《中华人民共和国家庭教育促进法》明确父母或者其他监护人负责实施家庭教育，国家和社会提供指导、支持和服务。第二，我们依法享有生存权、发展权、受保护权、参与权等权利，受到特殊、优先保护；保护未成年人，是家庭、学校、社会、网络、政府、司法六个方面共同的责任。第三，自我保护三步：先避险，再找可信的大人，最后记住求助渠道——110 报警、120 急救、119 火警。第四，知法守法是每个人都要做的事，合法权益受到侵害时可以请家长、老师帮助，依法维护自己的权益。最后送一句口诀给你：先避险、找大人、记渠道；知法守法，依法维权。",
    "homework": "最后留三项作业，分三个层次。第一层基础巩固，人人要做：写出保护未成年人的三部法律的规范全称，再各写一句话说明它们是为什么制定的。第二层能力应用，动手做：写出自我保护的三步，并写清楚 110、120、119 这三个号码分别在什么时候用；再画出一张自我保护三步的流程图，每一步旁边写上最要紧的一件事。第三层迁移挑战，选做：为自己设计一张自护卡，写清楚你最想提前做好准备的处境、在这种情况下最要紧的第一步、你要记牢的求助对象和求助渠道，做完请家长和你一起看一遍，贴在书桌前。",
    "knowledge-graph": "这张图展示了这节课在道德与法治知识网络里的位置。左边是学它之前可以先看看的，右边是学会以后可以接着探索的，下面是同一个领域里的伙伴知识。可以点一点，看看还有哪些值得继续了解的内容。",
    "ai-tutor": "如果还有没想通的地方，把你的问题写下来问 AI 学伴。它会先帮你找到卡住的地方，再给你一个小小的提示，让你自己往前走一步。",
}

TTS_LABELS = {
    "hero": "开场", "problem-anchor": "问题锚点", "objectives": "学习目标", "pretest": "前测",
    "module-1": "概念一 我们受特殊保护", "lab-1": "动手一 遇到这种情况怎么办",
    "module-2": "概念二 自我保护三步与知法守法", "lab-2": "动手二 六大保护归属台",
    "worked-example": "例题示范 说法校对", "conceptest-1": "概念测试",
    "synthesis": "综合任务 我的自护卡", "posttest": "后测", "summary": "课堂小结",
    "homework": "作业分层", "knowledge-graph": "知识图谱", "ai-tutor": "AI 学伴",
}

# ── 动手一（★核心模拟）：「遇到这种情况怎么办」判断台 ──
# 4 个处境 × 自我保护三步（先避险 → 找可信的大人 → 记住求助渠道），每一步三选一
SCENE = [
    {"k": "s1", "n": "放学路上，有个不认识的人一直跟着我",
     "case": "放学路上，你发现有个不认识的人一直跟着你，还说自己认识你的家人、要带你去找他。",
     "steps": [
         {"q": "第一步 · 先避险。下面哪种做法最合适？",
          "opts": [
              {"t": "往人多的地方走，就近走进开着门的商店、银行或者社区服务中心", "ok": True},
              {"t": "加快脚步往没人的小巷里跑，想办法甩掉他", "ok": False},
              {"t": "停下来跟他讲道理，让他不要再跟着我", "ok": False}],
          "why": "「先避险」的意思是：马上离开不安全的地方，走到人多、有工作人员的地方去。有人的地方，危险就不容易发生。",
          "fix": "这样可能会：把自己带到更危险、更没人能帮你的地方。还可以试试：遇事第一句先问自己——这里人多吗？哪里有人能帮我？然后往那里走。"},
         {"q": "第二步 · 找可信的大人。下面哪种做法最合适？",
          "opts": [
              {"t": "马上告诉店里的工作人员或者就近的保安，请他们帮忙，并打电话告诉爸爸妈妈", "ok": True},
              {"t": "谁也不说，先自己回家，怕说出来会被骂", "ok": False},
              {"t": "自己想办法对付他，尽量不麻烦别人", "ok": False}],
          "why": "可信的大人包括爸爸妈妈、老师，还有警察、店员、保安等等。把事情及时告诉大人，是最管用的办法。",
          "fix": "这样可能会：让危险一直拖下去，也让自己一个人扛着。还可以试试：记住一句话——遇到危险及时告诉信任的大人，不是麻烦别人，而是在保护自己。"},
         {"q": "第三步 · 记住求助渠道。下面哪种做法最合适？",
          "opts": [
              {"t": "尽量记住这个人的体貌特征，如果情况紧急就拨打 110 报警", "ok": True},
              {"t": "什么也不用记，回家就当这件事没有发生过", "ok": False},
              {"t": "把这件事发到班级群里，让同学都来帮我", "ok": False}],
          "why": "110 是报警电话。记住时间、地点和对方的特征，说给大人或者警察听，能帮上很大的忙。",
          "fix": "这样可能会：错过了及时求助的机会，也可能让更多人卷进危险里。还可以试试：把 110 报警、120 急救、119 火警这三个号码记牢，并记住当时的时间、地点和对方的特征。"}],
     },
    {"k": "s2", "n": "一个人在家，有陌生人来敲门",
     "case": "你一个人在家写作业，有人敲门，说自己是来检修水管的。",
     "steps": [
         {"q": "第一步 · 先避险。下面哪种做法最合适？",
          "opts": [
              {"t": "不开门，也不告诉对方家里只有自己一个人", "ok": True},
              {"t": "把门打开，让他进来看看", "ok": False},
              {"t": "隔着门跟他聊很久，把家里的情况都告诉他", "ok": False}],
          "why": "一个人在家时，门就是最重要的一道保护。不给陌生人开门，也不透露「家里只有我一个人」这条信息，是最要紧的一步。",
          "fix": "这样可能会：把危险请进了家门。还可以试试：隔着门说一句「我现在不方便开门」，然后马上做下一步——给信任的大人打电话。"},
         {"q": "第二步 · 找可信的大人。下面哪种做法最合适？",
          "opts": [
              {"t": "马上给爸爸妈妈或者其他信任的大人打电话，把事情告诉他们", "ok": True},
              {"t": "先不管他，等爸爸妈妈回来再说", "ok": False},
              {"t": "在班级群里问同学，看看大家遇到过没有", "ok": False}],
          "why": "遇到让自己不安的事，第一时间告诉信任的大人。大人知道以后，才能及时帮你想办法。",
          "fix": "这样可能会：把不安拖成更长的担心。还可以试试：拿起电话先说三句话——我在哪、发生了什么事、我现在有点害怕。"},
         {"q": "第三步 · 记住求助渠道。下面哪种做法最合适？",
          "opts": [
              {"t": "如果对方一直不走、反复敲门，就拨打 110 报警", "ok": True},
              {"t": "打开门看一眼他到底是不是真的检修人员", "ok": False},
              {"t": "自己出门去楼下躲一躲", "ok": False}],
          "why": "对方长时间不走、反复敲门，就属于需要及时求助的情况。这时候拨打 110 报警，说明地址和情况，是最合适的渠道。",
          "fix": "这样可能会：让自己正面碰上不确定的危险。还可以试试：留在安全的房间里，锁好门，拨打 110，把地址和情况说清楚。"}],
     },
    {"k": "s3", "n": "网上有人让我发照片、说家里的情况",
     "case": "上网时有人加你好友，说只要发几张照片、说出自己家里的情况，就送你礼物。",
     "steps": [
         {"q": "第一步 · 先避险。下面哪种做法最合适？",
          "opts": [
              {"t": "不发送任何个人信息和照片，也不点开对方发来的链接", "ok": True},
              {"t": "先发一张试一下，看看他是不是真的会送礼物", "ok": False},
              {"t": "把自己的学校、班级和家庭住址都告诉他", "ok": False}],
          "why": "个人信息和照片一旦发出去，就很难收回；对方发来的链接也可能是不安全的。不发送、不点开，就是最直接的一步避险。",
          "fix": "这样可能会：把自己的信息交到不认识的人手里。还可以试试：把「先不发、先不点」当成上网时的一条习惯。"},
         {"q": "第二步 · 找可信的大人。下面哪种做法最合适？",
          "opts": [
              {"t": "把聊天记录保存下来，告诉爸爸妈妈或者老师", "ok": True},
              {"t": "继续跟他聊，想办法套出他到底是谁", "ok": False},
              {"t": "觉得很不好意思，谁都不说", "ok": False}],
          "why": "把聊天记录保存下来再告诉信任的大人，大人就能看清情况、及时帮你处理。",
          "fix": "这样可能会：让自己陷进更复杂的来往里，或者错过处理的好时机。还可以试试：先截图保存，再说给爸爸妈妈或者老师听。"},
         {"q": "第三步 · 记住求助渠道。下面哪种做法最合适？",
          "opts": [
              {"t": "用平台的举报功能举报这个账号，请家长一起处理", "ok": True},
              {"t": "把对方的账号转发给同学，让大家一起去骂他", "ok": False},
              {"t": "把聊天记录删掉，就当没有发生过", "ok": False}],
          "why": "平台一般都有举报功能，举报这个账号，再请家长一起处理，既解决了问题，也保护了自己。",
          "fix": "这样可能会：把麻烦转给别人，或者让证据消失。还可以试试：保存记录、点击举报、请家长一起看，这三件事依次做完。"}],
     },
    {"k": "s4", "n": "同学之间闹了矛盾，有人威胁我",
     "case": "你和同学闹了矛盾，对方说放学后要找你麻烦，还让你别告诉老师。",
     "steps": [
         {"q": "第一步 · 先避险。下面哪种做法最合适？",
          "opts": [
              {"t": "不跟对方单独去偏僻的地方，放学和同学结伴、走人多的大路", "ok": True},
              {"t": "放学后一个人绕小路回家，想躲开他", "ok": False},
              {"t": "也叫上几个朋友，准备打回去", "ok": False}],
          "why": "先避险的意思是让自己离开可能发生危险的地方和场合。不单独去偏僻处、结伴走人多的大路，就是最实在的一步。",
          "fix": "这样可能会：把自己放到更难得到帮助的位置上，也可能让矛盾升级。还可以试试：先想清楚「哪些地方、哪些时间我容易被堵住」，然后避开它们。"},
         {"q": "第二步 · 找可信的大人。下面哪种做法最合适？",
          "opts": [
              {"t": "当天就告诉班主任老师和家长，把事情的经过说清楚", "ok": True},
              {"t": "先忍一忍，希望过几天他就忘了", "ok": False},
              {"t": "在班里到处说他坏话，让大家站到自己这一边", "ok": False}],
          "why": "让老师和家长尽早知道，才能及时把矛盾化解掉。把经过说清楚，是对自己最负责的做法。",
          "fix": "这样可能会：让矛盾越拖越大，也让自己一直提心吊胆。还可以试试：把事情按顺序写下来——什么时候、在哪里、发生了什么、对方说了什么。"},
         {"q": "第三步 · 记住求助渠道。下面哪种做法最合适？",
          "opts": [
              {"t": "如果威胁还在继续，请老师和家长一起处理；必要时由家长陪同拨打 110 报警", "ok": True},
              {"t": "自己找人去教训他，让他知道厉害", "ok": False},
              {"t": "把这件事憋在心里，谁也不告诉", "ok": False}],
          "why": "威胁持续存在时，请老师和家长一起出面，必要时由家长陪同拨打 110 报警。这样既保护了自己，也不会让自己做出错事。",
          "fix": "这样可能会：让自己也做出不妥的事，或者让危险一直持续。还可以试试：把「告诉大人」和「拨打 110」当成两条可以随时用上的渠道。"}],
     },
]

# ── 动手二：「六大保护归属台」（6 个做法 × 判断属于哪一类保护） ──
GUARD = [
    {"k": "g1", "n": "爸爸妈妈每天抽时间陪我聊天，关心我在学校过得怎么样",
     "case": "爸爸妈妈每天抽出时间陪我聊天，关心我的身体和情绪，也关心我在学校过得怎么样。",
     "opts": [
         {"t": "这属于学校保护", "ok": False},
         {"t": "这属于家庭保护", "ok": True},
         {"t": "这属于社会保护", "ok": False}],
     "why": "父母或者其他监护人关注未成年人的生理、心理状况和情感需求，关心、爱护未成年人，这就是家庭保护。",
     "mis": "有的同学<strong>误认为</strong>家里的关心只是「家务事」，和保护没关系。其实家庭保护是六大保护里离我们最近的一环。还可以试试：想一想家里人做过的哪一件事，正是为了你的安全和健康。"},
    {"k": "g2", "n": "学校开设安全教育课，老师专门找同学谈心",
     "case": "学校开设了安全教育课，老师还专门找同学谈心，了解大家最近有什么烦恼。",
     "opts": [
         {"t": "这属于学校保护", "ok": True},
         {"t": "这属于家庭保护", "ok": False},
         {"t": "这属于政府保护", "ok": False}],
     "why": "学校关心、爱护未成年学生，开展安全教育和心理健康教育，尊重学生的人格尊严，这就是学校保护。",
     "mis": "容易把学校保护<strong>搞混</strong>成「老师管纪律」。这样可能会：看不到学校在安全、健康这些方面为我们做的事。还可以试试：看看课程表里除了语文数学，还有哪些是为我们的成长专门安排的。"},
    {"k": "g3", "n": "图书馆和青少年活动中心对未成年人免费开放",
     "case": "社区里的图书馆和青少年活动中心，对未成年人免费开放。",
     "opts": [
         {"t": "这属于家庭保护", "ok": False},
         {"t": "这属于司法保护", "ok": False},
         {"t": "这属于社会保护", "ok": True}],
     "why": "全社会关心、爱护未成年人，图书馆、青少年活动中心等场所对未成年人免费开放，这就是社会保护。",
     "mis": "有的同学<strong>误认为</strong>这只是「方便」，和法律没关系。其实这正是法律要求全社会为未成年人做的事情。还可以试试：想一想身边还有哪些地方对未成年人免费或者优惠开放。"},
    {"k": "g4", "n": "网络平台限制未成年人使用时间，不让有害内容传播",
     "case": "网络平台对未成年人使用时间作出限制，也不允许发布、传播危害未成年人身心健康的内容。",
     "opts": [
         {"t": "这属于社会保护", "ok": False},
         {"t": "这属于网络保护", "ok": True},
         {"t": "这属于政府保护", "ok": False}],
     "why": "网络服务提供者依法保护未成年人的个人信息，限制未成年人使用时间，不制作、不传播危害未成年人身心健康的信息，这就是网络保护。",
     "mis": "有的同学<strong>误认为</strong>上网只是自己的事。这样可能会：忽略了网络上的风险。还可以试试：把「不透露个人信息、不点开陌生链接、遇到奇怪的事告诉大人」当成上网的三条习惯。"},
    {"k": "g5", "n": "有关部门对学校周边的食品经营情况进行检查",
     "case": "有关部门对学校周边的食品经营情况进行检查，保障同学们的饮食安全。",
     "opts": [
         {"t": "这属于司法保护", "ok": False},
         {"t": "这属于政府保护", "ok": True},
         {"t": "这属于学校保护", "ok": False}],
     "why": "各级人民政府及其有关部门在自己的职责范围内做好未成年人保护工作，这就是政府保护。",
     "mis": "容易把政府保护<strong>搞混</strong>成学校保护。可以这样记：出面检查的是政府部门的工作人员，所以属于政府保护。还可以试试：想一想学校门口还有哪些事是政府部门在管的。"},
    {"k": "g6", "n": "人民法院办理涉及未成年人的案件时，用适合未成年人的方式",
     "case": "人民法院在办理涉及未成年人的案件时，采用适合未成年人的方式，依法保护未成年人的合法权益。",
     "opts": [
         {"t": "这属于政府保护", "ok": False},
         {"t": "这属于网络保护", "ok": False},
         {"t": "这属于司法保护", "ok": True}],
     "why": "人民法院、人民检察院以及公安机关等，在办理涉及未成年人的案件时，依法保护未成年人的合法权益，这就是司法保护。",
     "mis": "有的同学<strong>误认为</strong>司法保护和自己的日常生活很远。其实它是一条兜底的保护线：真的遇到需要依法处理的事情时，它就在那里。还可以试试：把「人民法院、人民检察院」和「依法保护未成年人」这两组词连在一起记。"},
]

# ── 综合任务：「我的自护卡」生成台 ──
CARD = {
    "scenes": [
        {"k": "c1", "n": "一个人在家的时候"},
        {"k": "c2", "n": "上学、放学路上的时候"},
        {"k": "c3", "n": "上网的时候"},
        {"k": "c4", "n": "和同学相处的时候"},
    ],
    "firsts": [
        {"t": "先离开不安全的地方，走到人多、有大人能帮我的地方", "ok": True,
         "why": "想得准。不管遇到什么情况，第一步永远是先避险，安全第一。"},
        {"t": "先弄清楚对方到底想干什么，再决定怎么做", "ok": False,
         "why": "这样可能会：让自己在危险里多停留了一会儿。还可以试试：把「先避险」放在「弄明白」前面，安全以后再慢慢弄清楚。"},
        {"t": "先自己想办法解决，尽量不去麻烦别人", "ok": False,
         "why": "这样可能会：一个人扛着，错过了最好的求助时机。还可以试试：把求助看成本事，而不是麻烦——会求助的人，才更安全。"},
    ],
    "channels": [
        {"t": "记牢爸爸妈妈和老师的电话，再记牢 110 报警、120 急救、119 火警", "ok": True,
         "why": "这是最实在的一步。把号码记住，紧急的时候才不用现找。"},
        {"t": "和家里人一起约定一个说法，遇到情况先用这句话联系", "ok": True,
         "why": "这也是合适的一步。提前和家人约定好联系方式，真正着急的时候能省下很多时间。"},
        {"t": "不用特意记，真遇到事情的时候临时再想", "ok": False,
         "why": "这样可能会：最需要帮忙的那一刻反而想不起号码。还可以试试：把三个号码写在书桌前，和家人一起念两遍。"},
    ],
}

CUSTOM_JS = r"""
/* ============================================================
   pol-e-g6-u4 互动逻辑
   1) 选择题接线（前测 / 概念测试 / 后测）
   2) ★「遇到这种情况怎么办」判断台：4 个处境 × 三步（先避险 → 找可信的大人 → 记住渠道）
   3) 「六大保护归属台」：6 个做法 × 三选一
   4) 「我的自护卡」生成台：处境 → 最要紧的第一步 → 求助对象与渠道
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

  /* ---------- 2. ★「遇到这种情况怎么办」判断台 ---------- */
  var SCENE = __SCENE_JSON__;
  var STEP_NAME = ['第一步 · 先避险', '第二步 · 找可信的大人', '第三步 · 记住求助渠道'];
  var stage1 = document.getElementById('sf-stage');
  if (stage1) {
    var curS = null;
    var stepIdx = 0;
    var doneS = {};
    var out1 = document.getElementById('sf-out');
    var panel1 = document.getElementById('sf-panel');
    function sceneByKey(k) {
      for (var i = 0; i < SCENE.length; i++) { if (SCENE[i].k === k) return SCENE[i]; }
      return null;
    }
    function render1() {
      document.querySelectorAll('[data-sf-item]').forEach(function (b) {
        var k = b.dataset.sfItem;
        b.classList.toggle('selected', k === curS);
        b.classList.toggle('correct', !!doneS[k]);
      });
      document.getElementById('sf-score').textContent =
        '已经走完 ' + Object.keys(doneS).length + ' / ' + SCENE.length + ' 个处境的完整三步';
      if (!curS) { panel1.innerHTML = ''; return; }
      var S = sceneByKey(curS);
      var html = '<div style="font-weight:700;font-size:14px;margin:14px 0 0">' + S.case + '</div>';
      html += '<div class="flex-row" style="margin-top:10px;flex-wrap:wrap;gap:6px">';
      for (var i = 0; i < S.steps.length; i++) {
        html += '<span class="phase-tag" data-variant="' + (i < stepIdx ? 'success' : 'warn') + '">' +
          STEP_NAME[i] + (i < stepIdx ? ' ✓' : '') + '</span>';
      }
      html += '</div>';
      if (stepIdx >= S.steps.length) {
        html += '<div class="inner-card" style="margin-top:12px;background:var(--warm-soft);border-color:rgba(255,209,102,.7)">' +
          '<p style="margin:0"><strong>你的三步自护路线（' + S.n + '）</strong></p>' +
          '<p style="margin:8px 0 0;color:var(--muted)">' + S.steps[0].opts[0].t + '<br>' +
          '↓ ' + S.steps[1].opts[0].t + '<br>↓ ' + S.steps[2].opts[0].t + '</p></div>';
      } else {
        var st = S.steps[stepIdx];
        html += '<div style="font-weight:700;font-size:14px;margin:14px 0 0">' + st.q + '</div>';
        html += '<div class="grid" style="margin-top:10px">';
        st.opts.forEach(function (o, i) {
          html += '<button class="choice" data-sf-opt="' + i + '" style="text-align:left">' + o.t + '</button>';
        });
        html += '</div>';
      }
      panel1.innerHTML = html;
      panel1.querySelectorAll('[data-sf-opt]').forEach(function (b) {
        b.addEventListener('click', function () { choose(parseInt(b.dataset.sfOpt, 10)); });
      });
    }
    function choose(i) {
      var S = sceneByKey(curS);
      var st = S.steps[stepIdx];
      var o = st.opts[i];
      if (o.ok) {
        stepIdx += 1;
        out1.className = 'result';
        out1.innerHTML = '<strong>' + STEP_NAME[stepIdx - 1] + '选对了。</strong>' + st.why;
        render1();
        if (stepIdx >= S.steps.length) {
          doneS[S.k] = true;
          render1();
          out1.innerHTML += '<br><br><strong>这个处境的三步都走完了。</strong>' +
            '记住：先避险、找可信的大人、记住求助渠道——三步的顺序不能颠倒。';
        } else {
          out1.innerHTML += '<br>接着走下一步。';
        }
      } else {
        out1.className = 'result warn';
        out1.innerHTML = '<strong>这一步可以再想一想：' + o.t + '</strong>' +
          '<br><span style="color:var(--muted)">' + st.fix + '</span>';
      }
    }
    document.querySelectorAll('[data-sf-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        curS = b.dataset.sfItem;
        stepIdx = doneS[curS] ? sceneByKey(curS).steps.length : 0;
        out1.className = 'result warn';
        out1.textContent = '先读完处境，再从第一步开始选。';
        render1();
      });
    });
    render1();
  }

  /* ---------- 3. 「六大保护归属台」 ---------- */
  var GUARD = __GUARD_JSON__;
  var stage2 = document.getElementById('gd-stage');
  if (stage2) {
    var curG = null;
    var done2 = {};
    var out2 = document.getElementById('gd-out');
    var panel2 = document.getElementById('gd-panel');
    function guardByKey(k) {
      for (var i = 0; i < GUARD.length; i++) { if (GUARD[i].k === k) return GUARD[i]; }
      return null;
    }
    function render2() {
      document.querySelectorAll('[data-gd-item]').forEach(function (b) {
        var k = b.dataset.gdItem;
        b.classList.toggle('selected', k === curG);
        b.classList.toggle('correct', !!done2[k]);
      });
      document.getElementById('gd-score').textContent =
        '已经判断 ' + Object.keys(done2).length + ' / ' + GUARD.length + ' 个做法';
      if (!curG) { panel2.innerHTML = ''; return; }
      var G = guardByKey(curG);
      var html = '<div style="font-weight:700;font-size:14px;margin:14px 0 0">' + G.case + '</div>';
      html += '<div class="grid" style="margin-top:10px">';
      G.opts.forEach(function (o, i) {
        var cls = 'choice';
        if (done2[G.k] && o.ok) cls += ' correct';
        html += '<button class="' + cls + '" data-gd-opt="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel2.innerHTML = html;
      panel2.querySelectorAll('[data-gd-opt]').forEach(function (b) {
        b.addEventListener('click', function () { choose2(parseInt(b.dataset.gdOpt, 10)); });
      });
    }
    function rightOf(G) {
      for (var i = 0; i < G.opts.length; i++) { if (G.opts[i].ok) return G.opts[i].t; }
      return '';
    }
    function choose2(i) {
      var G = guardByKey(curG);
      var o = G.opts[i];
      var first = !done2[G.k];
      done2[G.k] = true;
      if (o.ok) {
        out2.className = 'result';
        out2.innerHTML = '<strong>判断得对。</strong>' + G.why;
      } else if (first) {
        out2.className = 'result warn';
        out2.innerHTML = '<strong>再想一想：' + G.case + '</strong>' + G.why +
          '<br><span style="color:var(--muted)"><strong>错因提醒：</strong>' + G.mis + '</span>';
      } else {
        out2.className = 'result';
        out2.innerHTML = '<strong>正确的一类是：' + rightOf(G) + '。</strong>' + G.why;
      }
      render2();
      if (Object.keys(done2).length === GUARD.length) {
        out2.innerHTML += '<br><br><strong>六个做法都判断过了。</strong>' +
          '保护未成年人是家庭、学校、社会、网络、政府、司法六个方面共同的责任。';
      }
    }
    document.querySelectorAll('[data-gd-item]').forEach(function (b) {
      b.addEventListener('click', function () {
        curG = b.dataset.gdItem;
        out2.className = 'result warn';
        out2.textContent = '先读一读这个做法，再在下面三个选项里选一个。';
        render2();
      });
    });
    render2();
  }

  /* ---------- 4. 「我的自护卡」生成台 ---------- */
  var CARD = __CARD_JSON__;
  var stage3 = document.getElementById('cd-stage');
  if (stage3) {
    var pick = { s: null, f: null, c: null };
    var out3 = document.getElementById('cd-out');
    var panel3 = document.getElementById('cd-panel');
    function sceneByKey3(k) {
      for (var i = 0; i < CARD.scenes.length; i++) { if (CARD.scenes[i].k === k) return CARD.scenes[i]; }
      return null;
    }
    function render3() {
      var html = '<div style="font-weight:700;font-size:14px;margin-bottom:6px">第一步 · 我最想提前做好准备的处境</div><div class="grid grid-2">';
      CARD.scenes.forEach(function (C) {
        html += '<button class="choice' + (pick.s === C.k ? ' selected' : '') +
          '" data-cd-scene="' + C.k + '" style="text-align:left">' + C.n + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第二步 · 这种情况下最要紧的第一步</div><div class="grid">';
      CARD.firsts.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.f === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-cd-first="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      html += '<div style="font-weight:700;font-size:14px;margin:16px 0 6px">第三步 · 我要记牢的求助对象与渠道</div><div class="grid">';
      CARD.channels.forEach(function (o, i) {
        var cls = 'choice';
        if (pick.c === i) cls += o.ok ? ' correct' : ' wrong';
        html += '<button class="' + cls + '" data-cd-chan="' + i + '" style="text-align:left">' + o.t + '</button>';
      });
      html += '</div>';
      panel3.innerHTML = html;
      panel3.querySelectorAll('[data-cd-scene]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.s = b.dataset.cdScene; render3();
          out3.className = 'result warn';
          out3.textContent = '处境选好了，接着选第二步：这种情况下最要紧的第一步。';
        });
      });
      panel3.querySelectorAll('[data-cd-first]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.f = parseInt(b.dataset.cdFirst, 10);
          var o = CARD.firsts[pick.f];
          out3.className = 'result' + (o.ok ? '' : ' warn');
          out3.innerHTML = (o.ok ? '<strong>这一步想得对。</strong>' : '<strong>这一步还可以再想想。</strong>') + o.why;
          render3();
        });
      });
      panel3.querySelectorAll('[data-cd-chan]').forEach(function (b) {
        b.addEventListener('click', function () {
          pick.c = parseInt(b.dataset.cdChan, 10);
          render3();
          if (pick.s === null || pick.f === null) {
            out3.className = 'result warn';
            out3.textContent = '三步还没选完，先把前面的补齐。';
            return;
          }
          var S = sceneByKey3(pick.s);
          var F1o = CARD.firsts[pick.f];
          var C1o = CARD.channels[pick.c];
          var okN = (F1o.ok ? 1 : 0) + (C1o.ok ? 1 : 0);
          out3.className = 'result' + (okN === 2 ? '' : ' warn');
          out3.innerHTML = '<strong>我的自护卡 · ' + S.n + '</strong><br>' +
            '处境：' + S.n + '<br>最要紧的第一步：' + F1o.t + '<br>要记牢的求助对象与渠道：' + C1o.t +
            '<br><span style="color:var(--muted)">' + (okN === 2
              ? '记牢这三步：先避险、找可信的大人、记住求助渠道。把它写在书桌前，再和家里人一起看一遍。'
              : '还可以再想一想：第一步永远是先避险；求助渠道要提前记牢，不能等出事的时候再想。换一个再试一次。') + '</span>';
        });
      });
    }
    render3();
  }
})();
"""
CUSTOM_JS = (CUSTOM_JS
             .replace('__SCENE_JSON__', json.dumps(SCENE, ensure_ascii=False))
             .replace('__GUARD_JSON__', json.dumps(GUARD, ensure_ascii=False))
             .replace('__CARD_JSON__', json.dumps(CARD, ensure_ascii=False)))


def build_pages():
    pages = []
    pages.append(p_cover(SPEC))
    pages.append(p_anchor(SPEC))
    pages.append(p_objectives(SPEC))

    pages.append(p_quiz(SPEC, "pre", 3, "pretest", "先测一测：保护我们的法律，你记得哪几部？", TTS["pretest"], [
        {"q": "下面哪一部法律的名称写得准确？",
         "options": [("《中华人民共和国未成年人保护法》", True),
                     ("《未成年人保护条例》", False),
                     ("《青少年保护法》", False)],
         "explain": "保护未成年人的基本法律，规范全称是《中华人民共和国未成年人保护法》。"
                    "<strong>错因提醒：</strong>常见错误是把法律名称凭印象<strong>误认为</strong>成《未成年人保护条例》或者《青少年保护法》。"
                    "法律名称要写全称，一个字都不能少。"},
        {"q": "放学路上，你发现有个不认识的人一直跟着你。下面哪种做法最合适？",
         "options": [("先走到人多的地方，及时告诉信任的大人，情况紧急就拨打 110 报警", True),
                     ("加快脚步往没人的小巷里跑，想办法甩掉他", False),
                     ("停下来跟他讲讲道理，让他别再跟着", False)],
         "explain": "自我保护的第一步永远是先避险——离开不安全的地方，走到人多、有工作人员的地方，再及时告诉信任的大人。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>自我保护就是自己想办法应付。"
                    "这样可能会：把自己带到更没人能帮你的地方。还可以试试：先问自己「这里人多吗、哪里有人能帮我」。"},
        {"q": "保护未成年人，是谁的责任？",
         "options": [("是家庭、学校、社会、网络、政府、司法六个方面共同的责任", True),
                     ("只是爸爸妈妈的责任", False),
                     ("只是学校的责任", False)],
         "explain": "保护未成年人是家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护六个方面共同的责任。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>保护未成年人只是家里的事或者只是学校的事，"
                    "这样就看不到身边还有很多人和很多制度在守护我们。"}
    ], tag="前测"))

    pages.append(p_concept(SPEC, "m1", 4, "module-1", "我们受特殊保护：三部法律在守护我们", TTS["module-1"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们每天都在长大，也天天听到「未成年人」这个词（And）；可到底有哪几部法律在保护我们、它们各自管什么，很多同学说不清（But）；所以这节课先把三部法律和它们的分工弄清楚（Therefore）。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>《中华人民共和国未成年人保护法》</strong>保护未成年人身心健康，保障未成年人合法权益，从家庭、学校、社会、网络、政府、司法六个方面织起保护的网。</div></div>
          <div class="step"><span class="n">2</span><div><strong>《中华人民共和国预防未成年人犯罪法》</strong>保障未成年人身心健康，培养未成年人良好品行，有效预防未成年人违法犯罪。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>《中华人民共和国家庭教育促进法》</strong>明确父母或者其他监护人负责实施家庭教育，国家和社会为家庭教育提供指导、支持和服务。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F1}" alt="六大保护抽象示意图：六个抽象圆环排列成圈，分别标注家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护，用房屋、书本、握手、网络节点、齿轮、天平等抽象符号表示，附中文标注，不含国徽国旗与徽章">
          <figcaption>六大保护示意：保护未成年人是家庭、学校、社会、网络、政府、司法六个方面共同的责任（抽象示意图，不按比例）</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>我们享有的权利</strong></p>
          <p style="color:var(--muted)">法律保障未成年人享有<strong>生存权、发展权、受保护权、参与权</strong>等权利，并给予<strong>特殊、优先保护</strong>。正因为我们是未成年人，法律才格外多照看一层。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>保护未成年人只是家里的事；也有的同学把法律名称<strong>误认为</strong>成《未成年人保护条例》。其实规范全称是《中华人民共和国未成年人保护法》，六大保护缺一不可。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "学校里的一节安全教育课、网上的一条内容限制、社区图书馆的一次免费开放，背后都有一部法律在起作用。"},
    {"lens": "解释它", "text": "为什么法律要给我们「特殊、优先保护」？因为未成年人还在成长，遇到事情时不一定有足够的力量和办法保护自己，所以法律要先把我们护在里面。"},
    {"lens": "迁移它", "text": "这就像过马路时大人会牵住你的手：不是因为你做错了什么，而是因为这一段路需要多一层照看。等你长大了，也要记得回过头照看更小的人。"},
])}
    ''', tag="概念一"))

    scene_btns = "\n".join(
        f'            <button class="choice" data-sf-item="{s["k"]}" style="text-align:left">'
        f'<strong>{s["n"]}</strong></button>'
        for s in SCENE
    )
    pages.append(p_interactive(SPEC, "lab1", 5, "lab-1", "★动手一：遇到这种情况怎么办？", TTS["lab-1"], f'''
        <p style="color:var(--muted);margin:0 0 12px">挑一个处境，然后一步步走：<strong>先避险 → 找可信的大人 → 记住求助渠道</strong>。每一步选一个你认为最合适的做法，选对了才能走下一步。</p>
        <div class="lab-panel">
          <div id="sf-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一个处境</div>
            <div class="grid grid-2">
{scene_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">判断进度</span><span class="v" id="sf-score">已经走完 0 / 4 个处境的完整三步</span></div>
          </div>
          <p class="result warn" id="sf-out" style="margin-top:12px">先点一个处境。</p>
          <div id="sf-panel"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🛡️</span><div><strong>三步的顺序不能颠倒：</strong>先让自己安全，再让大人知道，最后用对求助渠道。记住三个号码——110 报警、120 急救、119 火警。</div></div>
    '''))

    pages.append(p_concept(SPEC, "m2", 6, "module-2", "自我保护三步：先避险、找大人、记渠道", TTS["module-2"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p><strong>为什么要学这一课？</strong></p>
          <p style="color:var(--muted)">我们已经知道法律在保护我们（And）；可真遇到事情的那一刻，很多同学反而不知道该先做什么（But）；所以这节课把自我保护的三步固定下来，练成能立刻用出来的办法（Therefore）。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>先避险：</strong>马上离开不安全的地方，走到人多、有工作人员的地方去。安全第一，其他都可以往后放。</div></div>
          <div class="step"><span class="n">2</span><div><strong>找可信的大人：</strong>马上告诉爸爸妈妈、老师，或者警察、店员、保安这些可以信任的大人。求助不是麻烦别人。</div></div>
          <div class="step"><span class="n green">3</span><div><strong>记住求助渠道：</strong>110 报警、120 急救、119 火警；记住时间、地点和对方的特征，说给大人或者警察听。</div></div>
        </div>
        <figure class="ta-standard-figure">
          <img src="{F2}" alt="自我保护三步抽象流程图：三个圆形依次相连，分别标注先避险、找可信的大人、记住求助渠道，用盾牌、大人与孩子的人物剪影、电话听筒等抽象符号表示，附中文标注">
          <figcaption>自我保护三步：先避险 → 找可信的大人 → 记住求助渠道（抽象示意图，不按比例）</figcaption>
        </figure>
        <div class="inner-card">
          <p><strong>知法守法，依法维权</strong></p>
          <p style="color:var(--muted)">知道法律的规定，才能更好地保护自己，也不会因为不懂而做错事。不做法律禁止的事；有了不良行为要及时改正。合法权益受到侵害时，可以请家长、老师帮助，依法维护自己的权益。</p>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学<strong>误认为</strong>自我保护就是自己冲上去跟对方较量；也有的同学<strong>误认为</strong>把遇到的事说出来很丢人。其实第一步永远是先避险，及时告诉信任的大人正是最管用的办法。</p>
        </div>
{insight_box([
    {"lens": "看见它", "text": "同样一件事，做法的顺序一变，结果就不同：先走到人多的地方、再告诉大人、最后拨打 110，这三步是有先后的。"},
    {"lens": "解释它", "text": "为什么「先避险」要排在第一位？因为只有自己安全了，才有机会去告诉大人、去用求助渠道。顺序颠倒，后面的办法就都用不上了。"},
    {"lens": "迁移它", "text": "这套顺序在其他时候也用得上：闻到家里有煤气味，先离开、再喊大人、最后打电话；遇到身体不舒服，先停下来、再告诉老师、最后联系家长。"},
])}
    ''', tag="概念二"))

    guard_btns = "\n".join(
        f'            <button class="choice" data-gd-item="{g["k"]}" style="text-align:left">'
        f'<strong>{g["n"]}</strong></button>'
        for g in GUARD
    )
    pages.append(p_interactive(SPEC, "lab2", 7, "lab-2", "★动手二：六大保护归属台", TTS["lab-2"], f'''
        <p style="color:var(--muted);margin:0 0 12px">挑一个身边做法，判断它属于<strong>家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护</strong>里的哪一类。选完马上看到解释。</p>
        <div class="lab-panel">
          <div id="gd-stage">
            <div style="font-weight:700;font-size:14px;margin-bottom:6px">① 挑一个做法</div>
            <div class="grid">
{guard_btns}
            </div>
          </div>
          <div class="lab-readout">
            <div class="readout-cell"><span class="k">判断进度</span><span class="v" id="gd-score">已经判断 0 / 6 个做法</span></div>
          </div>
          <p class="result warn" id="gd-out" style="margin-top:12px">先点一个做法。</p>
          <div id="gd-panel"></div>
        </div>
        <div class="kid-note" style="margin-top:14px"><span class="emoji">🤝</span><div><strong>判断的小窍门：</strong>看是谁在做这件事——家里人做的是家庭保护，学校做的是学校保护，全社会做的是社会保护，网络平台做的是网络保护，政府部门做的是政府保护，人民法院、人民检察院等做的是司法保护。</div></div>
    '''))

    pages.append(p_concept(SPEC, "we", 8, "worked-example", "例题示范：说法校对，五条说法哪条要改", TTS["worked-example"], f'''
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>情境：</strong>班会课上，几位同学写了五条关于法律保护的说明。请你当一次校对员，判断哪一条准确、哪一条必须改。</p>
        </div>
        <div class="step-grid">
          <div class="step"><span class="n">1</span><div><strong>说法一（正确）：</strong>「《中华人民共和国未成年人保护法》保护未成年人身心健康，保障未成年人合法权益。」注意法律名称要写全称。</div></div>
          <div class="step"><span class="n">2</span><div><strong>说法二（必须改）：</strong>「保护未成年人只是家里的事，和学校、社会没有关系。」保护未成年人是家庭、学校、社会、网络、政府、司法六个方面共同的责任。</div></div>
          <div class="step"><span class="n">3</span><div><strong>说法三（正确）：</strong>「遇到危险要先保护自己，及时告诉信任的大人。」这就是自我保护的第一、第二步。</div></div>
          <div class="step"><span class="n">4</span><div><strong>说法四（必须改）：</strong>「只要自己没做坏事，就不用学法律。」知法守法是每个人都要做的事，知道法律的规定，才能更好地保护自己。</div></div>
          <div class="step"><span class="n green">5</span><div><strong>说法五（正确）：</strong>「合法权益受到侵害时，可以请家长和老师帮助，依法维护自己的权益。」</div></div>
        </div>
        <div class="misconception">
          <span class="lab">常见错误</span>
          <p style="margin:6px 0 0">有的同学把「自我保护」<strong>误认为</strong>「自己冲上去解决」，一遇到事情就想硬碰硬；也有的同学把法律名称<strong>搞混</strong>，凭印象写成《未成年人保护条例》。记住：第一步永远是先避险，法律名称要写规范全称。</p>
        </div>
    ''', tag="例题示范", bloom="analyze"))

    pages.append(p_quiz(SPEC, "ct", 9, "conceptest-1", "概念测试：三句话，藏着三个容易想歪的地方", TTS["conceptest-1"], [
        {"q": "关于保护我们的法律，下面哪句话说得准确？",
         "options": [("《中华人民共和国预防未成年人犯罪法》是为了保障未成年人身心健康、培养未成年人良好品行、有效预防未成年人违法犯罪而制定的", True),
                     ("保护未成年人只需要《中华人民共和国未成年人保护法》这一部法律", False),
                     ("《中华人民共和国家庭教育促进法》只管学校的事", False)],
         "explain": "三部法律各有分工：未成年人保护法保障未成年人合法权益，预防未成年人犯罪法重在预防，家庭教育促进法明确父母或者其他监护人负责实施家庭教育。"
                    "<strong>错因提醒：</strong>常见错误是把三部法律的作用<strong>搞混</strong>，或者<strong>误认为</strong>一部法律就够了。"},
        {"q": "有同学说：「自我保护就是自己想办法把对方制服。」下面哪种说法更合适？",
         "options": [("自我保护的第一步永远是先避险，再及时告诉信任的大人", True),
                     ("对，遇到事情就该自己冲上去解决", False),
                     ("只要跑得快就行，不用告诉别人", False)],
         "explain": "自我保护的三步是：先避险、找可信的大人、记住求助渠道，顺序不能颠倒。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>自己冲上去才叫勇敢。这样可能会：让自己陷入更大的危险。还可以试试：把「先让自己安全」当成第一句口诀。"},
        {"q": "关于 110、120、119 这三个号码，下面哪种说法准确？",
         "options": [("110 是报警电话，120 是急救电话，119 是火警电话", True),
                     ("三个号码都是报警电话，打哪个都一样", False),
                     ("这三个号码只有大人才能打", False)],
         "explain": "110 报警、120 急救、119 火警，各有各的用处；遇到紧急情况，先让自己安全，再拨打对应的号码，把地址和情况说清楚。"
                    "<strong>错因提醒：</strong>容易把三个号码<strong>搞混</strong>。还可以试试：和家人一起把三个号码念两遍，再说说分别在什么时候用。"}
    ], tag="概念测试"))

    pages.append(p_interactive(SPEC, "syn", 10, "synthesis", "综合任务：我的自护卡，写好了贴在书桌前", TTS["synthesis"], f'''
        <p style="color:var(--muted);margin:0 0 12px">三步各选一个：<strong>最想提前做好准备的处境 → 最要紧的第一步 → 要记牢的求助对象与渠道</strong>。选完，你就有了自己的自护卡。</p>
        <div class="lab-panel">
          <div id="cd-stage"></div>
          <div id="cd-panel"></div>
          <p class="result warn" id="cd-out" style="margin-top:12px">从第一步开始选。</p>
        </div>
        <div class="inner-card" style="margin-top:14px">
          <p><strong>把它写下来：</strong></p>
          <p style="color:var(--muted)">用三句话写清楚：我最想提前做好准备的处境是……；这种情况下最要紧的第一步是……；我要记牢的求助对象和渠道是……。</p>
          <textarea id="syn-answer" rows="3" placeholder="我最想提前做好准备的处境是……；最要紧的第一步是……；我要记牢的求助渠道是……" style="margin-top:8px"></textarea>
        </div>
    ''', tag="综合任务", bloom="create"))

    pages.append(p_quiz(SPEC, "post", 11, "posttest", "后测：换几个新处境，判断还准不准", TTS["posttest"], [
        {"q": "你一个人在家，有人敲门说自己是来检修水管的。下面哪一步最要紧？",
         "options": [("不开门，也不说自己一个人在家，马上打电话告诉信任的大人，必要时拨打 110 报警", True),
                     ("把门打开，让他进来看看是不是真的", False),
                     ("告诉他家里只有自己一个人，请他等一等", False)],
         "explain": "一个人在家时，门就是最重要的一道保护。先不开门、不透露独自在家，再告诉信任的大人，必要时拨打 110 报警。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>问清楚对方是谁再开门更稳妥。"
                    "这样可能会：把危险请进家门。还可以试试：隔着门说一句「我现在不方便开门」，然后马上打电话给大人。"},
        {"q": "上网时有人让你发照片、说出家里的情况，才肯送你礼物。下面哪种做法合适？",
         "options": [("不发送任何个人信息和照片，保存聊天记录，告诉爸爸妈妈或者老师", True),
                     ("先发一张试一下，看看他是不是真的会送", False),
                     ("这是小事，不用告诉任何人", False)],
         "explain": "个人信息一旦发出去就很难收回，这很可能是陷阱。不发送、不点开链接、保存记录并告诉信任的大人，是最合适的做法。"
                    "<strong>错因提醒：</strong>有的同学<strong>误认为</strong>发一张照片不会有事。"
                    "这样可能会：把自己的信息交到不认识的人手里。还可以试试：把「先不发、先不点、告诉大人」当成上网的三条习惯。"},
        {"q": "关于「六大保护」，下面哪句话说得准确？",
         "options": [("保护未成年人是家庭、学校、社会、网络、政府、司法六个方面共同的责任", True),
                     ("只要家庭保护好就够了，其他方面管不管都行", False),
                     ("六大保护只和老师有关，和同学没关系", False)],
         "explain": "家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护，六个方面各有分工、共同负责。"
                    "<strong>错因提醒：</strong>常见错误是<strong>误认为</strong>只要有一方面负责就够了。"
                    "还可以试试：把六个方面各找一件身边的事对上去，看看它们是怎么一起起作用的。"}
    ], tag="后测"))

    pages.append(p_summary(SPEC, 12, "summary", "小结：三部法律、六大保护、自护三步", TTS["summary"], f'''        <div class="grid">
          <div class="summary-item"><span class="num">1</span><div><strong>三部法律：</strong>《中华人民共和国未成年人保护法》保护未成年人身心健康、保障未成年人合法权益；《中华人民共和国预防未成年人犯罪法》重在有效预防未成年人违法犯罪；《中华人民共和国家庭教育促进法》明确父母或者其他监护人负责实施家庭教育。</div></div>
          <div class="summary-item"><span class="num">2</span><div><strong>我们的权利：</strong>依法享有生存权、发展权、受保护权、参与权等权利，受到特殊、优先保护；保护未成年人是家庭、学校、社会、网络、政府、司法六个方面共同的责任。</div></div>
          <div class="summary-item"><span class="num">3</span><div><strong>自护三步：</strong>先避险 → 找可信的大人 → 记住求助渠道（110 报警、120 急救、119 火警），顺序不能颠倒。</div></div>
          <div class="summary-item"><span class="num">4</span><div><strong>知法守法，依法维权：</strong>知道法律的规定，不做法律禁止的事，有了不良行为要及时改正；合法权益受到侵害时，可以请家长、老师帮助，依法维护自己的权益。</div></div>
        </div>
        <div class="inner-card" style="background:var(--warm-soft);border-color:rgba(255,209,102,.7)">
          <p style="margin:0"><strong>一句口诀：</strong>先避险、找大人、记渠道；知法守法，依法维权。</p>
        </div>
        <div class="inner-card">
          <p><strong>给别人讲一遍：</strong>请用「先避险」和「求助渠道」这两个词，把自我保护的三步讲给家里人听，并说说 110、120、119 分别在什么时候用。</p>
          <p style="color:var(--muted)">再动一动手：<strong>写一写</strong>三部法律的规范全称，再写出六大保护的名称，每一个都用一句话说明它在生活里是什么样子。</p>
        </div>
    '''))

    pages.append(p_homework(SPEC, 13, "homework", "作业分层：三层小任务，按自己的节奏来", TTS["homework"], [
        [
            "写出保护未成年人的三部法律的规范全称，再各写一句话说明它们是为什么制定的。",
            "写出自我保护的三步，写清楚每一步要做的最要紧的一件事。",
            "写出 110、120、119 这三个号码分别是什么电话，各在什么时候用。",
        ],
        [
            "写出六大保护的名称（家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护），并各写一件身边对应的事。",
            "写出我们未成年人依法享有的几项权利，并说明为什么法律要给我们特殊、优先保护。",
            "画出一张自我保护三步的流程图，每一步旁边写上最要紧的一件事，再向同桌解释一遍。",
        ],
        [
            "为自己设计一张自护卡：写清楚你最想提前做好准备的处境、这种情况下最要紧的第一步、你要记牢的求助对象和求助渠道；做完请家长和你一起看一遍，贴在书桌前。",
            "和家里人一起做一次演练：约定一个联系的暗号，把爸爸妈妈和老师的电话抄在一张纸上，再一起念一遍 110、120、119。",
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
    "title": "法律保护我们健康成长",
    "name_en": "Law Protects Our Healthy Growth",
    "grade": 6,
    "grade_cn": "六年级",
    "domain": "tradition-culture",
    "domain_cn": "中华优秀传统文化",
    "lesson_type": "situational-inquiry",
    "version": "1.0.0",
    "description": "面向小学六年级的道德与法治课，正对统编六上第 4 单元「法律保护我们健康成长」（我们受特殊保护、知法守法依法维权），落到三件事上。第一件是我们受特殊保护：《中华人民共和国未成年人保护法》保护未成年人身心健康、保障未成年人合法权益，从家庭、学校、社会、网络、政府、司法六个方面织起保护的网；《中华人民共和国预防未成年人犯罪法》保障未成年人身心健康、培养未成年人良好品行、有效预防未成年人违法犯罪；《中华人民共和国家庭教育促进法》明确父母或者其他监护人负责实施家庭教育，国家和社会为家庭教育提供指导、支持和服务；未成年人依法享有生存权、发展权、受保护权、参与权等权利，受到特殊、优先保护。第二件是自我保护三步：先避险（马上离开不安全的地方，走到人多、有工作人员的地方）→ 找可信的大人（爸爸妈妈、老师、警察、店员、保安等）→ 记住求助渠道（110 报警、120 急救、119 火警），三步顺序不能颠倒；同时讲清不提倡自己冲上去硬碰硬。第三件是知法守法，依法维权：知道法律的规定才能更好地保护自己，也不容易因为不懂而做错事；不做法律禁止的事，有了不良行为要及时改正；自己的合法权益受到侵害时，可以请家长、老师帮助，依法维护自己的权益。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是本课核心模拟「遇到这种情况怎么办」判断台（四个处境 × 自我保护三步，每步三选一，选对了才能走下一步，走完生成三步自护路线）、动手二是「六大保护归属台」（六个身边做法 × 判断属于哪一类保护），综合任务是「我的自护卡」生成台（处境 → 最要紧的第一步 → 求助对象与渠道，合成一张可贴在书桌前的自护卡）。全课表述从严：法律名称一律写规范全称；不出现任何法律条文编号；不臆造案件细节、不涉及任何具体伤亡个案，所有情境一律写成「如果遇到……」，只讲假设中的应对办法，不写人名、地名、时间、结果；不做任何标签化或诊断式判断，不使用恐吓性表述；求助渠道只写 110 报警、120 急救、119 火警，并强调及时告诉信任的大人是首要办法；插图一律为中性简洁扁平教学插画，不使用真人照片风格，不绘制国徽、法院徽章、国旗等图形，改用盾牌、圆环、人物剪影、握手等抽象符号与地标性建筑抽象剪影。",
    "tags": ["法律保护我们健康成长", "我们受特殊保护", "中华人民共和国未成年人保护法", "中华人民共和国预防未成年人犯罪法", "中华人民共和国家庭教育促进法", "六大保护", "自我保护三步", "知法守法依法维权", "六年级", "法治观念"],
    "standard_ref": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学：传承中华传统美德，了解革命传统，增强文化自信；对应统编《道德与法治》六年级上册 第4单元「法律保护我们健康成长」：我们受特殊保护；知法守法，依法维权。",
    "hero_question": "遇到危险的时候，第一步该做什么？",
    "hero_alt": "法律保护我们健康成长知识结构图：三栏分别为三部保护我们的法律、六大保护、自我保护三步，用盾牌、圆环、人物剪影、握手、电话听筒等抽象符号表示，附中文标注，不含国徽国旗与徽章",
    "hero_caption": "法律保护我们健康成长：三部法律在守护 · 六大保护共同负责 · 自护三步——先避险、找可信的大人、记住求助渠道",
    "anchor_title": "今天最想弄清楚哪一件事？",
    "anchor_intro": "选一个你真正想知道的问题，后面的活动都会围着它转。",
    "anchor_choices": [
        {"t": "法律为什么要给我们特殊的保护？", "d": "有哪几部法律在守护我们，它们各管什么", "v": "法律为什么要给我们特殊的保护"},
        {"t": "我们未成年人享有哪些受保护的权利？", "d": "生存权、发展权、受保护权、参与权……", "v": "我们未成年人享有哪些受保护的权利"},
        {"t": "遇到危险的时候，我该怎么做？", "d": "自我保护的三步到底是哪三步", "v": "遇到危险的时候我该怎么做"},
        {"t": "平时怎么做才算知法守法？", "d": "为什么说知法守法也是在保护自己", "v": "平时怎么做才算知法守法"},
    ],
    "objectives": [
        "能说出保护我们的三部法律的规范全称，能说出它们各自是为什么制定的",
        "能说出未成年人依法享有生存权、发展权、受保护权、参与权等权利，受到特殊、优先保护，能说出家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护这六个方面",
        "能说清自我保护的三步——先避险、找可信的大人、记住求助渠道，并说出 110 报警、120 急救、119 火警分别在什么时候用",
        "能说出知法守法是每个人都要做的事，合法权益受到侵害时可以请家长、老师帮助，依法维护自己的权益",
    ],
    "objectives_plain": [
        "能说出保护未成年人的三部法律的规范全称和各自的作用",
        "能说出我们享有的权利和六大保护",
        "能说清自我保护的三步和三个求助号码",
        "能说出知法守法、依法维权的意思",
    ],
    "standards": [
        {"content": "传承中华传统美德，了解革命传统，增强文化自信。",
         "source": "《义务教育道德与法治课程标准（2022年版2025年修订）》· 小学"},
        {"content": "我们受特殊保护；知法守法，依法维权",
         "source": "统编《道德与法治》六年级上册 第4单元「法律保护我们健康成长」"},
    ],
    "prereqs": ["pol-e-g6-u3"],
    "prereqs_name": "我们的国家机构",
    "prereqs_meta": "pol-e-g6-u3",
    "leads_to": [],
    "next_meta": "",
    "section_images": [f"assets/{ID}-fig1.webp", f"assets/{ID}-fig2.webp"],
    "tts": TTS,
    "tts_labels": TTS_LABELS,
    "hints": {
        "hero": "三件事：哪三部法律在保护我们、六大保护是什么、遇到危险第一步做什么。",
        "problem-anchor": "先定一个小目标：这节课结束时，你能把自我保护的三步按顺序说出来。",
        "objectives": "看清四件事：三部法律、我们的权利与六大保护、自护三步、知法守法依法维权。",
        "pretest": "凭现在的想法选就好，选得不合适也不扣分，正好知道要重点听哪里。",
        "module-1": "法律名称记全称：《中华人民共和国未成年人保护法》《中华人民共和国预防未成年人犯罪法》《中华人民共和国家庭教育促进法》。",
        "lab-1": "每一步都会给三个做法，选最合适的那个；选对了才能走下一步。",
        "module-2": "三步顺序不能颠倒：先避险 → 找可信的大人 → 记住求助渠道（110 报警、120 急救、119 火警）。",
        "lab-2": "判断窍门：看是谁在做这件事——家里人、学校、全社会、网络平台、政府部门，还是人民法院、人民检察院等。",
        "worked-example": "五条说法：三条正确、两条必须改。留意法律名称的规范全称和「保护不只是家里的事」。",
        "conceptest-1": "三句话里各藏着一个容易想歪的地方，选完把解释读一遍。",
        "synthesis": "三步做自护卡：处境 → 最要紧的第一步 → 要记牢的求助对象与渠道。",
        "posttest": "出现了一个人在家、网上收到奇怪邀请和六大保护的说法，看看今天的判断还用不用得上。",
        "summary": "四句话：三部法律、权利与六大保护、自护三步、知法守法依法维权。",
        "homework": "三层小任务，先做前两层；第三层的自护卡请家长一起看一遍。",
        "knowledge-graph": "看看这节课的前置、后续和同域知识在哪里。",
        "ai-tutor": "卡住了就问学伴：它先找到卡点，再给最小的提示。",
    },
    "custom_js": CUSTOM_JS,
    "build_pages": build_pages,
    "plan_intro": "本课补的是小学道德与法治在六年级的一课，正对统编六上第 4 单元「法律保护我们健康成长」（我们受特殊保护、知法守法依法维权）。六年级学生每天都会用到「未成年人」这个词，也知道遇到危险要「告诉家长」，但对法律层面的保护几乎是空白，容易出现三类典型偏差：把法律名称凭印象改写成《未成年人保护条例》《青少年保护法》；误认为保护未成年人只是家里的事，看不到学校、社会、网络、政府、司法各方面的责任；把「自我保护」误认为「自己冲上去解决」，遇到事情时不知道该先做什么。所以全课不做条文背诵，而把内容落到「哪三部法律—保护什么—遇到事情怎么做」这条链上。第一层是「我们受特殊保护」：给出三部法律的规范全称和各自的作用——未成年人保护法保护未成年人身心健康、保障未成年人合法权益，从家庭、学校、社会、网络、政府、司法六个方面织起保护的网；预防未成年人犯罪法重在保障身心健康、培养良好品行、有效预防未成年人违法犯罪；家庭教育促进法明确父母或者其他监护人负责实施家庭教育，国家和社会提供指导、支持和服务；并说明未成年人依法享有生存权、发展权、受保护权、参与权等权利，受到特殊、优先保护。第二层是「自我保护三步」：先避险（马上离开不安全的地方，走到人多、有工作人员的地方）→ 找可信的大人（爸爸妈妈、老师、警察、店员、保安等）→ 记住求助渠道（110 报警、120 急救、119 火警），强调三步顺序不能颠倒，因为只有自己安全了，后面的办法才用得上；并说明求助不是麻烦别人，而是保护自己。第三层是「知法守法，依法维权」：知道法律的规定才能更好地保护自己，也不容易因为不懂而做错事；不做法律禁止的事，有了不良行为要及时改正；合法权益受到侵害时，可以请家长、老师帮助，依法维护自己的权益。三个互动台子都能真操作，反馈一律写成「这样可能会……，还可以试试……」：动手一是本课核心模拟「遇到这种情况怎么办」判断台——四个处境（放学路上被跟随、一个人在家有人敲门、网上被索要信息、同学之间被威胁），每个处境都要走完三步，每一步给出三个做法，选对了才推进到下一步，错选时给出错因与下一步提示，走完三步后自动生成这个处境的三步自护路线；动手二是「六大保护归属台」——六个身边做法，判断属于哪一类保护，判断窍门是看「是谁在做这件事」；综合任务是「我的自护卡」生成台——学生按「处境 → 最要紧的第一步 → 求助对象与渠道」各选一步，由系统合成一张可以写上名字、贴在书桌前的自护卡。全课在表述上从严把关：法律名称一律写规范全称；不出现任何法律条文编号；不臆造案件细节、不涉及任何具体伤亡个案，所有情境一律写成「如果遇到……」，只讲假设中的应对办法，不写人名、地名、时间、结果；不做任何标签化或诊断式判断，不使用恐吓性表述，语气积极正面；求助渠道只写 110 报警、120 急救、119 火警；插图一律为中性简洁扁平教学插画，不使用真人照片风格，不绘制国徽、法院徽章、国旗等图形，改用盾牌、圆环、人物剪影、握手等抽象符号与地标性建筑抽象剪影。",
    "plan_table": """| 1 | cover | 法律保护我们健康成长 | 定向 |
| 2 | interactive | 今天最想弄清楚哪一件事？ | 起·问题锚点（留白设问，不预置答案） |
| 3 | objectives | 这节课结束时，你应该能做到 | 定向 |
| 4 | quiz | 先测一测：保护我们的法律，你记得哪几部？ | 起·前测（暴露法律名称误写与认识误区） |
| 5 | concept | 我们受特殊保护：三部法律在守护我们 | 承·概念一（三部法律 + 六大保护 + 我们的权利） |
| 6 | interactive | ★动手一：遇到这种情况怎么办？ | 承·核心模拟（4 处境 × 自护三步，选对才推进） |
| 7 | concept | 自我保护三步：先避险、找大人、记渠道 | 承·概念二（三步顺序 + 知法守法依法维权） |
| 8 | interactive | ★动手二：六大保护归属台 | 承·核心模拟（6 做法 × 判断保护类别） |
| 9 | concept | 例题示范：说法校对，五条说法哪条要改 | 转·重难点突破（法律全称 + 六大保护共同责任） |
| 10 | quiz | 概念测试：三句话，藏着三个容易想歪的地方 | 转·干扰项定位误解 |
| 11 | interactive | 综合任务：我的自护卡，写好了贴在书桌前 | 合·迁移应用（三步合成自护卡） |
| 12 | quiz | 后测：换几个新处境，判断还准不准 | 合·后测 |
| 13 | summary | 小结：三部法律、六大保护、自护三步 | 合·小结与复述 |
| 14 | quiz | 作业分层：三层小任务，按自己的节奏来 | 合·三段式作业（⭐/⭐⭐/⭐⭐⭐） |
| 15 | summary | 这节课在知识网络里的位置 | 合·知识图谱 |
| 16 | interactive | AI 学伴 | 收尾·个别化诊断 |""",
    "plan_assets": "- Hero 知识结构图（已生成）：三部保护我们的法律 / 六大保护 / 自我保护三步 三栏，用盾牌、圆环、人物剪影、握手、电话听筒等抽象符号表示，附中文标注\n- P5 六大保护抽象示意图（已生成）：六个抽象圆环排成一圈，分别标注家庭保护、学校保护、社会保护、网络保护、政府保护、司法保护，并标注「抽象示意图，不按比例」\n- P7 自我保护三步抽象流程图（已生成）：三个圆形依次相连，标注先避险、找可信的大人、记住求助渠道，用盾牌、大人与孩子的人物剪影、电话听筒等抽象符号表示\n- ★ 全课不绘制国徽、法院徽章、国旗等图形；不出现真人照片风格；一律用中性简洁扁平教学插画\n- ★ 表述口径统一：法律名称一律写规范全称；不出现任何法律条文编号；不臆造案件细节、不涉及任何具体伤亡个案；所有情境一律写成「如果遇到……」，只讲假设中的应对办法\n- ★ 求助渠道只写 110 报警、120 急救、119 火警，并强调「第一时间告诉信任的大人」是首要办法",
}

if __name__ == "__main__":
    import json as _j
    print(_j.dumps({"id": SPEC["id"], "pages": "see build_pages"}, ensure_ascii=False))
