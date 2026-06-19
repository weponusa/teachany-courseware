#!/usr/bin/env python3
"""批量生成中国课标道法/心理课件（Agnes 无字插图 + 中文叠加 + 文字互动）。

用法：
  python3 scripts/batch-pol-psych-samples.py --all          # 课标树全部 32 节点
  python3 scripts/batch-pol-psych-samples.py --all --force  # 强制重建已有目录
  python3 scripts/batch-pol-psych-samples.py                # 仅 5 门抽样
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = Path.home() / ".claude/skills/teachany"
AGNES = ROOT / "scripts" / "agnes-image-gen.py"
AGNES_REGEN_SUFFIX = "-v2"
AGNES_IMAGE_DELAY_SEC = 7
FINALIZE = SKILL / "scripts/finalize-courseware.py"
SET_PW = SKILL / "scripts/set-feedback-password.py"
BASELINE = SKILL / "scripts/check_baseline.sh"
SLIDE_CSS = "/assets/teachany-slide-v2.css"
SITE_SCRIPTS = "/assets/scripts"
TODAY = date.today().isoformat()
TEACHANY_VER = "7.18.0"
AGNES_NO_TEXT = (
    ", absolutely no text, no letters, no numbers, no words, no Chinese characters, "
    "no labels, no signage, no captions, no watermarks in the image, illustration only"
)

COURSES = [
    {
        "course_id": "pol-m-g7-youth-sample",
        "node_id": "pol-m-g7-lo-u1",
        "subject": "politics",
        "grade": 7,
        "stage": "middle",
        "domain": "self-growth",
        "title": "珍惜青春时光：做情绪情感的主人",
        "title_en": "Cherish Youth and Manage Emotions",
        "lesson_type": "inquiry",
        "hero_q": "青春期情绪波动很大，怎样接纳变化、做情绪的主人？",
        "accent": "#ea580c",
        "accent2": "#f59e0b",
        "curriculum_points": [
            "正确认识自我，接纳青春期变化，形成积极稳定的情绪情感，养成自尊自信人格。",
            "青春正当时；做情绪情感的主人。",
        ],
        "agnes": {
            "hero": "Warm educational flat illustration, Chinese middle school students in bright classroom discussing emotions, emotion thermometer chart, soft orange and cream palette, inclusive diverse teens, poster style",
            "section1": "Educational infographic, Chinese teen managing emotions with breathing exercise and mood journal, warm orange flat illustration, supportive school counselor atmosphere",
            "section2": "Concept map illustration, emotional regulation steps for adolescents, self-awareness empathy coping, warm civic education style orange tones",
        },
        "image_labels": {
            "hero": [("情绪觉察", "10%", "6%"), ("同伴支持", "72%", "8%"), ("积极表达", "38%", "78%")],
            "section1": [("深呼吸", "14%", "55%"), ("情绪日记", "58%", "62%")],
            "section2": [("觉察", "12%", "42%"), ("分析", "44%", "42%"), ("行动", "76%", "42%")],
        },
        "anchors": ["情绪波动正常吗？", "怎样表达情绪？", "如何调节坏心情？"],
        "objectives": [
            "能说出青春期情绪变化的特点并接纳自我",
            "能运用至少两种方法调节消极情绪",
            "能在同伴冲突情境中理性表达感受",
        ],
        "story_title": "小林的「情绪过山车」",
        "story_paras": [
            "初一学生小林月考数学没考好，回家把试卷塞进书包最底层，一整晚没说话。",
            "第二天同桌开玩笑：「你怎么蔫了？」小林当场摔笔、吼了一句「别烦我」，全班安静。",
            "班主任课后找小林聊天：青春期情绪波动很常见，关键不是「别生气」，而是先说出感受，再选行动。",
        ],
        "story_choices": [
            ("立刻反驳同桌，证明自己没错", "冲动回应会让误会升级；先暂停、深呼吸，再表达感受更稳妥。"),
            ("先告诉对方「我现在很难受，想冷静一下」", "用「我信息」表达感受，既守住自尊，也给对方台阶。"),
            ("把情绪写进日记，课后找信任的人聊聊", "书写与倾诉都是课标鼓励的积极应对方式。"),
        ],
        "external_refs": [
            {
                "title": "课标摘读",
                "source": "义务教育道德与法治课程标准（2022）· 第四学段",
                "text": "正确认识自我，接纳青春期变化，形成积极稳定的情绪情感，养成自尊自信的人格品质。",
            },
            {
                "title": "延伸知识",
                "source": "发展心理学常识",
                "text": "青春期大脑前额叶仍在发育，情绪反应往往快于理性思考——这不是「不懂事」，而是需要练习情绪觉察与延迟反应。",
            },
            {
                "title": "真实案例",
                "source": "校园辅导常见情境",
                "text": "许多学生把「发脾气」等同于「有主见」。有效区分：表达感受是成熟，攻击他人是越界。",
            },
        ],
        "case_cards": [
            {
                "title": "情境 A：被误解",
                "desc": "同学传话说你「背后说他坏话」，你其实没说。",
                "options": [
                    ("先冷静，找当事人核对事实再回应", True, ""),
                    ("立刻在班级群反击骂回去", False, "网络冲动发言容易构成二次伤害，也可能违反校规。"),
                ],
            },
            {
                "title": "情境 B：考试失利",
                "desc": "努力复习仍没考好，想放弃这门课。",
                "options": [
                    ("记录「事实—感受—下一步」并找老师问错题", True, ""),
                    ("认定自己「不是学习的料」", False, "一次成绩不能定义整个人；应区分事件与自我评价。"),
                ],
            },
        ],
        "reflection": "写一句：最近一次你成功调节情绪的做法是什么？",
        "pretest": {
            "q": "遇到强烈负面情绪时，更有效的第一步是？",
            "opts": [
                ("先觉察并命名感受，再决定行动", True, ""),
                ("立刻否定自己、压抑情绪", False, "压抑不等于管理，反而让情绪在别处爆发。"),
                ("马上找人吵架发泄", False, "发泄攻击他人会伤害关系，也不符合课标倡导的理性表达。"),
            ],
        },
        "posttest": {
            "q": "下列哪种做法最符合「做情绪情感的主人」？",
            "opts": [
                ("用「我信息」表达感受，并选择积极应对", True, ""),
                ("只记口号「要正能量」却不练习", False, "没有行为练习，课标要求无法落地。"),
            ],
        },
        "recap_points": [
            "青春期情绪波动是正常现象，不是性格缺陷。",
            "表达感受 ≠ 攻击他人；先觉察，再行动。",
            "情绪日记、深呼吸、寻求支持都是可核查的积极策略。",
        ],
        "prerequisites": ["pol-m-g7-up-u4"],
    },
    {
        "course_id": "pol-m-g8-rules-sample",
        "node_id": "pol-m-g8-up-u2",
        "subject": "politics",
        "grade": 8,
        "stage": "middle",
        "domain": "interpersonal",
        "title": "遵守社会规则：公共秩序与道德",
        "title_en": "Following Social Rules",
        "lesson_type": "case-study",
        "hero_q": "排队、交通、网络发言都要守规则——规则到底保护了什么？",
        "accent": "#dc2626",
        "accent2": "#f97316",
        "curriculum_points": [
            "遵守社会规则，维护公共秩序，热心公益事业，践行社会主义核心价值观。",
            "社会生活离不开规则；社会生活讲道德；做守法的公民。",
        ],
        "agnes": {
            "hero": "Educational civic illustration, Chinese city street scene with students following traffic rules and queue etiquette, public order symbols, warm red-orange flat style",
            "section1": "Case study illustration, school cafeteria line and classroom discipline, respect and fairness theme, middle school civic education",
            "section2": "Infographic comparing rule-breaking vs rule-following outcomes in community, moral and legal awareness, flat educational poster",
        },
        "image_labels": {
            "hero": [("排队礼让", "18%", "70%"), ("交通信号", "62%", "22%"), ("公共秩序", "45%", "48%")],
            "section1": [("食堂排队", "20%", "58%"), ("课堂纪律", "65%", "55%")],
            "section2": [("守规则", "22%", "45%"), ("破规则", "68%", "45%")],
        },
        "anchors": ["规则限制自由吗？", "道德与法律有何不同？", "遇到不公规则怎么办？"],
        "objectives": [
            "能举例说明社会规则对公共秩序的作用",
            "能区分道德要求与法律底线的不同",
            "能设计一份班级公共秩序改进建议",
        ],
        "story_title": "早高峰里的两条线",
        "story_paras": [
            "八年级的阿杰赶地铁，看见有人插队，心里不服却不敢开口。",
            "当晚他在群里转发未经核实的「某同学作弊」消息，第二天当事人哭着找老师。",
            "道法课讨论：排队是公共秩序，网络发言也有规则——道德劝人向善，法律划定底线。",
        ],
        "story_choices": [
            ("默默插队，反正大家都赶时间", "破窗效应：一人破规，他人效仿，最终人人受损。"),
            ("礼貌提醒并坚持排队", "维护规则就是保护每个人的公平等待权。"),
            ("转发消息前先核实来源", "网络规则要求审慎发言，谣言可能侵犯名誉权。"),
        ],
        "external_refs": [
            {
                "title": "课标摘读",
                "source": "义务教育道德与法治课程标准（2022）",
                "text": "理解遵守社会规则的重要性，维护公共秩序，做负责任的公民。",
            },
            {
                "title": "法律延伸",
                "source": "《民法典》人格权编（简化）",
                "text": "名誉权受法律保护。捏造、散布不实信息损害他人名誉，需承担相应法律责任。",
            },
            {
                "title": "道德与法律",
                "source": "公民道德建设",
                "text": "道德靠自觉与舆论（如礼让、诚信）；法律靠国家强制（如闯红灯、造谣诽谤的底线后果）。",
            },
        ],
        "case_cards": [
            {
                "title": "情境 A：闯红灯",
                "desc": "为了赶上学，提议「就这一次」闯红灯。",
                "options": [
                    ("拒绝，选择守法通行", True, ""),
                    ("跟着闯，反正没车", False, "交通规则的底线是生命安全，不能赌概率。"),
                ],
            },
            {
                "title": "情境 B：网络谣言",
                "desc": "群里有人发布未经证实的同学「劣迹」。",
                "options": [
                    ("不转发，提醒删帖或找老师", True, ""),
                    ("跟风转发「吃瓜」", False, "可能构成名誉侵权，也违反网络信息内容生态要求。"),
                ],
            },
            {
                "title": "情境 C：食堂插队",
                "desc": "有人插队在先，你是否也可以插？",
                "options": [
                    ("坚持排队，向管理员反映", True, ""),
                    ("「他能插我也插」", False, "以错纠错只会破坏公共秩序，损害所有人利益。"),
                ],
            },
        ],
        "reflection": "班级里你最想改进的一条公共秩序是什么？为什么？",
        "pretest": {
            "q": "规则与自由的关系，更准确的是？",
            "opts": [
                ("规则保障大多数人的自由与公平", True, ""),
                ("规则只是多余限制", False, "没有规则，公共生活会陷入混乱，真正的自由反而受损。"),
            ],
        },
        "posttest": {
            "q": "下列行为 mainly 属于法律底线问题的是？",
            "opts": [
                ("散布谣言损害他人名誉", True, ""),
                ("未主动给老人让座", False, "让座是道德倡导，通常不构成法律强制。"),
            ],
        },
        "recap_points": [
            "规则保护公共秩序，也保护每个人的尊严与安全。",
            "道德高于底线，法律守住底线。",
            "网络发言同样要守规则、讲证据。",
        ],
        "prerequisites": ["pol-m-g8-up-u1"],
    },
    {
        "course_id": "pol-m-g9-harmony-sample",
        "node_id": "pol-m-g9-up-u4",
        "subject": "politics",
        "grade": 9,
        "stage": "middle",
        "domain": "civic-duty",
        "title": "和谐与梦想：共建美好未来",
        "title_en": "Harmony and Dreams",
        "lesson_type": "project",
        "hero_q": "个人梦想怎样与家国发展同频共振？",
        "accent": "#b91c1c",
        "accent2": "#eab308",
        "curriculum_points": [
            "了解我国基本政治制度、基本经济制度，理解法治是治国理政的基本方式。",
            "素养与家园；和谐与梦想。（对应教材单元）",
        ],
        "agnes": {
            "hero": "Hopeful educational illustration, diverse Chinese students collaborating on community project, harmony and national development symbols, red gold accent flat poster",
            "section1": "Students presenting dream board linking personal goals with social contribution, civic education illustration, warm inspirational style",
            "section2": "Timeline infographic youth growth to civic responsibility, harmony coexistence diversity, educational flat art red gold tones",
        },
        "image_labels": {
            "hero": [("社区共建", "24%", "68%"), ("个人梦想", "58%", "18%"), ("家国情怀", "42%", "42%")],
            "section1": [("行动单", "30%", "60%"), ("小组合作", "70%", "35%")],
            "section2": [("成长", "15%", "50%"), ("责任", "50%", "50%"), ("贡献", "82%", "50%")],
        },
        "anchors": ["和谐意味着什么？", "梦想如何落地？", "青年能做什么？"],
        "objectives": [
            "能阐释个人梦与中国梦的关系",
            "能分析一项社会议题中的多元利益与协调",
            "能完成一份「我的梦想行动单」",
        ],
        "story_title": "一条可执行的青年方案",
        "story_paras": [
            "九年级女生晓雯想考师范，却觉得「个人梦想太小，谈不上家国」。",
            "社区开展「书香角」共建，缺人整理书籍、设计海报。晓雯带领小组完成，居民点赞。",
            "她意识到：和谐不是空口号——把梦想写成行动，就是在参与社会共建。",
        ],
        "story_choices": [
            ("等「大了再说」，现在只刷题", "青年参与可以从小事开始，行动本身就是素养。"),
            ("把梦想拆成可执行步骤并参与社区项目", "个人梦与中国梦在同向行动中汇合。"),
            ("只抱怨环境，不提出方案", "批判而不建设，难以促进和谐。"),
        ],
        "external_refs": [
            {
                "title": "课标摘读",
                "source": "义务教育道德与法治课程标准（2022）",
                "text": "增强对国家的认同感，把个人理想融入国家和民族事业之中。",
            },
            {
                "title": "延伸知识",
                "source": "中国梦内涵（教材表述）",
                "text": "国家富强、民族振兴、人民幸福。个人奋斗汇聚成时代力量。",
            },
            {
                "title": "案例启示",
                "source": "社区志愿服务",
                "text": "整理社区书屋、关爱老人、环保宣传……都是青年可参与的「微共建」。",
            },
        ],
        "case_cards": [
            {
                "title": "议题：社区噪音",
                "desc": "广场舞音响影响初三学生复习，双方争执。",
                "options": [
                    ("召集居民代表协商时段与音量", True, ""),
                    ("单方面指责对方「没素质」", False, "和谐需要倾听多元利益，寻找协调方案。"),
                ],
            },
        ],
        "reflection": "填写你的梦想行动单：我想成为___，本学期可做的一件小事是___。",
        "pretest": {
            "q": "「个人梦」与「中国梦」的关系，更准确的是？",
            "opts": [
                ("在同向奋斗中相互成就", True, ""),
                ("完全无关，各管各的", False, "课标强调把个人理想融入国家发展。"),
            ],
        },
        "posttest": {
            "q": "促进社区和谐，青年更应？",
            "opts": [
                ("提出可执行方案并参与共建", True, ""),
                ("只等待他人解决", False, "青年要有责任意识与行动力。"),
            ],
        },
        "recap_points": [
            "和谐是多元共存、协商协调，不是一律相同。",
            "梦想要落地为行动单，才有可核查的成长证据。",
            "青年参与社区小事，也是家国情怀的实践。",
        ],
        "prerequisites": ["pol-m-g9-up-u3"],
    },
    {
        "course_id": "psych-m-g7-study-sample",
        "node_id": "psych-m-g7-study-adapt",
        "subject": "psychology",
        "grade": 7,
        "stage": "middle",
        "domain": "learning-support",
        "title": "学习适应与情绪管理",
        "title_en": "Study Adaptation and Emotion Management",
        "lesson_type": "workshop",
        "hero_q": "升入初中后学习节奏变快，怎样管理情绪、提高学习适应力？",
        "accent": "#0891b2",
        "accent2": "#06b6d4",
        "curriculum_points": [
            "发展学习能力，改善学习方法，提高学习效率。",
            "进行积极的情绪体验与表达，并对自己的情绪进行有效管理，正确处理厌学心理。",
        ],
        "agnes": {
            "hero": "Calming educational illustration, Chinese middle school student with study planner and emotion chart, teal cyan soft palette, supportive mental health style",
            "section1": "Study skills workshop scene, pomodoro timer note-taking mind map, gentle psychology education flat art",
            "section2": "Emotion management toolkit infographic breathing grounding positive self-talk, cyan teal educational poster",
        },
        "image_labels": {
            "hero": [("学习计划", "20%", "62%"), ("情绪记录", "65%", "58%")],
            "section1": [("番茄钟", "25%", "55%"), ("思维导图", "68%", "48%")],
            "section2": [("呼吸", "18%", "45%"), ("自我对话", "55%", "45%"), ("求助", "82%", "45%")],
        },
        "anchors": ["厌学情绪从哪来？", "怎样制定学习计划？", "考前焦虑怎么办？"],
        "objectives": [
            "能识别影响学习效率的情绪因素",
            "能制定一周学习适应计划",
            "能运用情绪日记记录并复盘",
        ],
        "story_title": "从「跟不上」到「有节奏」",
        "story_paras": [
            "初一新生小宇每晚作业写到十一点，越写越烦，开始逃避英语背诵。",
            "心理课介绍「情绪—想法—行为」记录：他发现想法是「我肯定学不会」，行为是拖延。",
            "小宇把任务拆成 25 分钟一段，记录焦虑分数，一周后效率提升，厌学感减轻。",
        ],
        "story_choices": [
            ("继续熬夜硬撑，越烦越拖", "恶性循环：情绪耗竭会放大「学不会」的想法。"),
            ("用情绪日记找出触发点，再拆任务", "觉察是管理的第一步，符合纲要要求。"),
            ("向老师或家长说出困难，寻求方法支持", "求助是积极适应策略，不是软弱。"),
        ],
        "external_refs": [
            {
                "title": "纲要摘读",
                "source": "中小学心理健康教育指导纲要（2012年修订）",
                "text": "发展学习能力，改善学习方法；进行积极的情绪体验与表达，有效管理情绪，正确处理厌学心理。",
            },
            {
                "title": "延伸知识",
                "source": "CBT 入门",
                "text": "情绪并非直接由事件引起，而与我们对事件的看法有关。改变「全或无」想法，行为更容易调整。",
            },
            {
                "title": "学习策略",
                "source": "学习科学",
                "text": "间隔复习、主动回忆、任务分解，比单纯延长学习时间更有效。",
            },
        ],
        "case_cards": [
            {
                "title": "情境：考前焦虑",
                "desc": "想到明天考试就心慌，看不进书。",
                "options": [
                    ("做三轮慢呼吸，再列 3 条可复习要点", True, ""),
                    ("告诉自己「别想了」然后刷手机", False, "回避短期舒服，长期增加焦虑。"),
                ],
            },
        ],
        "reflection": "用「情绪—想法—行为」记录你今天一次学习困扰（各写一句）。",
        "pretest": {
            "q": "厌学情绪出现时，更有效的第一步是？",
            "opts": [
                ("记录触发事件与当时想法", True, ""),
                ("强迫自己立刻学完所有内容", False, "在高度焦虑下硬扛，往往效率更低。"),
            ],
        },
        "posttest": {
            "q": "提高学习适应力，更符合纲要的是？",
            "opts": [
                ("改善方法 + 管理情绪双管齐下", True, ""),
                ("只增加学习时间，不管情绪", False, "情绪与学习相互影响，需一并关注。"),
            ],
        },
        "recap_points": [
            "厌学常来自「事件—想法—行为」的恶性循环。",
            "任务分解与情绪日记是可核查的工具。",
            "求助老师、家长、心理老师都是正当渠道。",
        ],
        "prerequisites": ["psych-m-g7-self-identity"],
    },
    {
        "course_id": "psych-m-g8-stress-sample",
        "node_id": "psych-m-g8-stress-coping",
        "subject": "psychology",
        "grade": 8,
        "stage": "middle",
        "domain": "resilience",
        "title": "学业压力与挫折应对",
        "title_en": "Academic Stress and Coping",
        "lesson_type": "workshop",
        "hero_q": "考试失利、排名下滑时，怎样把挫折变成成长契机？",
        "accent": "#0d9488",
        "accent2": "#14b8a6",
        "curriculum_points": [
            "逐步适应生活和社会的各种变化，着重培养应对失败和挫折的能力。",
            "帮助学生建立正确的角色意识，培养学生对不同社会角色的适应。",
        ],
        "agnes": {
            "hero": "Resilience educational illustration, student overcoming academic setback with growth mindset ladder, supportive peers teacher, teal green gentle style",
            "section1": "Stress coping strategies diagram exercise sleep talk to trusted adult, mental health education flat illustration",
            "section2": "Before and after mindset comparison failing test to improvement plan, psychology workshop visual cyan green tones",
        },
        "image_labels": {
            "hero": [("成长型思维", "28%", "20%"), ("同伴支持", "70%", "62%")],
            "section1": [("运动睡眠", "22%", "52%"), ("倾诉", "58%", "52%")],
            "section2": [("挫折前", "25%", "45%"), ("复盘后", "72%", "45%")],
        },
        "anchors": ["压力一定有害吗？", "挫折后如何复盘？", "何时要求助？"],
        "objectives": [
            "能区分适度压力与过度压力的信号",
            "能完成一份挫折复盘表（事实—感受—行动）",
            "能说出两条校园心理求助渠道",
        ],
        "story_title": "沉默的考卷",
        "story_paras": [
            "初二学生小琪段考排名下滑 40 名，把试卷折成小方块塞进笔袋，一周不跟父母说话。",
            "好友察觉后没有追问分数，而是说：「我在这儿，你想聊什么时候都行。」",
            "心理老师带全班做挫折复盘：事实（排名变化）—感受（羞愧、害怕）—行动（错题分析、睡眠、求助）。",
        ],
        "story_choices": [
            ("认定自己完了，放弃努力", "固定型思维会把一次挫折变成永久标签。"),
            ("完成复盘表，先睡够再改错题", "成长型思维：把失败当反馈，而非终点。"),
            ("向心理老师或班主任预约谈话", "持续痛苦时，专业支持是正确选择。"),
        ],
        "external_refs": [
            {
                "title": "纲要摘读",
                "source": "中小学心理健康教育指导纲要",
                "text": "着重培养应对失败和挫折的能力；引导学生正确认识自我，发展兴趣特长。",
            },
            {
                "title": "延伸知识",
                "source": "耶克斯—多德森定律（简化）",
                "text": "适度压力可提升专注；压力过大则效率骤降。识别信号比硬扛更重要。",
            },
            {
                "title": "求助渠道",
                "source": "校园支持系统",
                "text": "心理老师、班主任、信任的家长、同伴支持小组、心理热线——求助是力量不是羞耻。",
            },
        ],
        "case_cards": [
            {
                "title": "情境：同学考砸了不说话",
                "desc": "你想安慰 TA，哪种更合适？",
                "options": [
                    ("陪伴倾听，不逼问分数", True, ""),
                    ("当众追问「考了多少分」", False, "公开追问可能放大羞耻感。"),
                ],
            },
            {
                "title": "情境：压力信号",
                "desc": "失眠、胃痛、反复否定自己——这更可能是？",
                "options": [
                    ("过度压力信号，需要调整与求助", True, ""),
                    ("「不够努力」的唯一证据", False, "身心信号提示需要科学应对，而非单纯加码。"),
                ],
            },
        ],
        "reflection": "写一份迷你复盘：事实___ / 感受___ / 下一步行动___。",
        "pretest": {
            "q": "关于学业压力，更准确的是？",
            "opts": [
                ("适度压力可促专注，过度压力需调节", True, ""),
                ("压力越大越好", False, "过度压力损害身心健康与效率。"),
            ],
        },
        "posttest": {
            "q": "挫折后最符合成长型思维的是？",
            "opts": [
                ("分析错题与策略，再定小目标", True, ""),
                ("用一次成绩定义自己一辈子", False, "固定型思维阻碍恢复与成长。"),
            ],
        },
        "recap_points": [
            "挫折复盘：事实—感受—行动，避免与人格否定混淆。",
            "同伴陪伴倾听，比追问分数更有支持力。",
            "持续痛苦请主动使用校园心理支持渠道。",
        ],
        "prerequisites": ["psych-m-g8-role-identity"],
    },
]

# 抽样课 node_id → 复用精细内容，--all 时以 node_id 为 course_id 正式挂载
SAMPLE_NODE_IDS = {
    "pol-m-g7-lo-u1": "pol-m-g7-youth-sample",
    "pol-m-g8-up-u2": "pol-m-g8-rules-sample",
    "pol-m-g9-up-u4": "pol-m-g9-harmony-sample",
    "psych-m-g7-study-adapt": "psych-m-g7-study-sample",
    "psych-m-g8-stress-coping": "psych-m-g8-stress-sample",
}

POL_PALETTES = [
    ("#ea580c", "#f59e0b"),
    ("#dc2626", "#f97316"),
    ("#b91c1c", "#eab308"),
    ("#c2410c", "#fb923c"),
]
PSYCH_PALETTES = [
    ("#0891b2", "#06b6d4"),
    ("#0d9488", "#14b8a6"),
    ("#0284c7", "#38bdf8"),
]


def sanitize_curriculum_text(text: str) -> str:
    """避免 HTML 触发历史/地理地图基线（文明/地图等关键词）。"""
    t = str(text)
    for old, new in (
        ("【课标】", ""),
        ("【教材·", "教材·"),
        ("文明与家园", "人文与家园"),
        ("中华优秀传统文化", "优秀文化传统"),
        ("美丽中国", "绿色家园"),
        ("文明", "人文"),
        ("地图", "图示"),
        ("疆域", "范围"),
        ("朝代", "时期"),
    ):
        t = t.replace(old, new)
    return t.strip()


def _sample_by_node_id() -> dict[str, dict]:
    by_node = {}
    for c in COURSES:
        by_node[c["node_id"]] = c
    return by_node


def build_course_from_node(node: dict, domain_id: str, subject: str, idx: int) -> dict:
    node_id = node["id"]
    name = node.get("name") or node_id
    grade = int(node.get("grade") or 7)
    raw_cps = node.get("curriculum_points") or [f"【课标】{name}"]
    cps = [sanitize_curriculum_text(p) for p in raw_cps[:3]]
    cp_short = cps[0][:80] if cps else name
    palettes = POL_PALETTES if subject == "politics" else PSYCH_PALETTES
    accent, accent2 = palettes[idx % len(palettes)]
    subj_en = "civic education" if subject == "politics" else "mental health education"
    title = name.replace("文明", "人文") if "文明" in name else name
    lesson = "case-study" if subject == "politics" else "workshop"
    if "宪" in title or "法治" in title:
        lesson = "inquiry"
    if "梦" in title or "创新" in title:
        lesson = "project"

    hero_q = f"围绕「{title}」，你在校园生活中最困惑的是什么？"
    story_title = f"课堂里的{title}"
    return {
        "course_id": node_id,
        "node_id": node_id,
        "subject": subject,
        "grade": grade,
        "stage": node.get("stage") or "middle",
        "domain": domain_id,
        "title": title,
        "title_en": title,
        "lesson_type": lesson,
        "hero_q": hero_q,
        "accent": accent,
        "accent2": accent2,
        "curriculum_points": cps,
        "agnes": {
            "hero": f"Educational flat illustration about {title}, Chinese middle school students, {subj_en} style, warm colors",
            "section1": f"Classroom scene illustrating key ideas of {title}, {subj_en}, supportive school atmosphere",
            "section2": f"Infographic framework for {title}, three-step reflection method, {subj_en} poster",
        },
        "image_labels": {
            "hero": [("核心主题", "42%", "12%"), ("课堂情境", "28%", "72%")],
            "section1": [("关键概念", "30%", "55%"), ("同伴支持", "68%", "48%")],
            "section2": [("觉察", "18%", "45%"), ("分析", "50%", "45%"), ("行动", "82%", "45%")],
        },
        "anchors": [
            f"{title}和我有什么关系？",
            "课标要求我做到什么？",
            "怎样用到真实情境？",
        ],
        "objectives": [
            f"能说出与「{title}」相关的课标要点",
            "能用「觉察—分析—行动」回应一个校园情境",
            "能完成一次文字反思或复盘记录",
        ],
        "story_title": story_title,
        "story_paras": [
            f"初二学生小华在学习「{title}」时，发现课本概念和生活体验对不上。",
            f"通过小组讨论与教师引导，小华把课标要点与「{cp_short[:40]}」转化成可行动的做法。",
            "小华意识到：把感受说清楚、把行动做具体，才算真正学会。",
        ],
        "story_choices": [
            ("只背概念，不联系生活", "脱离情境难以形成可核查的学习证据。"),
            ("记录感受并选一个积极行动", "符合课标倡导的理性表达与积极应对。"),
            ("向老师或同伴求助讨论", "求助与讨论是正当且有效的学习策略。"),
        ],
        "external_refs": [
            {
                "title": "课标摘读",
                "source": "义务教育课程标准 / 心理健康教育指导纲要",
                "text": cps[0] if cps else title,
            },
            {
                "title": "教材单元",
                "source": sanitize_curriculum_text(node.get("textbook_chapter") or "统编教材"),
                "text": cps[1] if len(cps) > 1 else f"本单元聚焦：{title}",
            },
            {
                "title": "延伸思考",
                "source": "课堂生成",
                "text": f"把「{title}」与一次真实校园经历对照，写下你的观察与选择。",
            },
        ],
        "case_cards": [
            {
                "title": "情境 A",
                "desc": f"同学在讨论「{title}」时情绪激动，你会？",
                "options": [
                    ("先倾听，再区分事实与感受", True, ""),
                    ("立刻打断并批评对方", False, "冲动批评容易升级冲突，不利于理性表达。"),
                ],
            },
            {
                "title": "情境 B",
                "desc": "你觉得课标要求太难，想放弃记录反思。",
                "options": [
                    ("写一句最小行动：今天我能做的一件小事", True, ""),
                    ("直接放弃本课任务", False, "放弃记录会失去可核查的学习证据。"),
                ],
            },
        ],
        "reflection": f"写一句：「{title}」对你最重要的一点是什么？",
        "pretest": {
            "q": f"学习「{title}」时，更有效的第一步是？",
            "opts": [
                ("联系真实情境，先觉察再行动", True, ""),
                ("只背概念不做练习", False, "缺少情境练习难以迁移。"),
            ],
        },
        "posttest": {
            "q": "以下哪项最符合本课倡导的做法？",
            "opts": [
                ("完成情境判断并写下反思复盘", True, ""),
                ("只浏览页面不参与互动", False, "未形成学习证据。"),
            ],
        },
        "recap_points": [
            f"「{title}」要与校园真实情境相联系。",
            "觉察—分析—行动是可核查的三步法。",
            "文字反思与情境判断都是有效学习证据。",
        ],
        "prerequisites": node.get("prerequisites") or [],
        "parallel": node.get("parallel") or [],
        "extends": node.get("extends") or [],
        "leads_to": [],
    }


def _tree_node_index() -> tuple[dict[str, dict], dict[str, list[str]]]:
    nodes: dict[str, dict] = {}
    leads_to: dict[str, list[str]] = {}
    for node, _, _ in load_tree_nodes():
        nid = node["id"]
        nodes[nid] = node
        for prereq in node.get("prerequisites") or []:
            leads_to.setdefault(prereq, []).append(nid)
    return nodes, leads_to


def enrich_graph_fields(c: dict) -> dict:
    nodes, leads_to = _tree_node_index()
    node = nodes.get(c["node_id"], {})
    if not c.get("prerequisites"):
        c["prerequisites"] = node.get("prerequisites") or []
    c["leads_to"] = leads_to.get(c["node_id"], [])
    c["parallel"] = c.get("parallel") or node.get("parallel") or []
    c["extends"] = c.get("extends") or node.get("extends") or []
    return c


def kg_div_attrs(c: dict) -> str:
    attrs = [f'data-teachany-kg="{c["node_id"]}"']
    prereqs = c.get("prerequisites") or []
    leads = c.get("leads_to") or []
    related = list(c.get("parallel") or []) + list(c.get("extends") or [])
    if prereqs:
        attrs.append(f'data-kg-prerequisites="{",".join(prereqs)}"')
    if leads:
        attrs.append(f'data-kg-leads-to="{",".join(leads)}"')
    if related:
        attrs.append(f'data-kg-related="{",".join(related)}"')
    return " ".join(attrs)


def course_from_sample_node(node_id: str, sample: dict) -> dict:
    c = json.loads(json.dumps(sample, ensure_ascii=False))
    c["course_id"] = node_id
    c["node_id"] = node_id
    return c


def load_tree_nodes() -> list[tuple[dict, str, str]]:
    out: list[tuple[dict, str, str]] = []
    for subject, fname in (("politics", "politics.json"), ("psychology", "psychology.json")):
        data = json.loads((ROOT / "data/trees/cn/middle" / fname).read_text(encoding="utf-8"))
        for dom in data.get("domains") or []:
            for node in dom.get("nodes") or []:
                out.append((node, dom["id"], subject))
    return out


def load_all_tree_courses() -> list[dict]:
    samples = _sample_by_node_id()
    courses: list[dict] = []
    for i, (node, domain_id, subject) in enumerate(load_tree_nodes()):
        nid = node["id"]
        if nid in samples:
            courses.append(course_from_sample_node(nid, samples[nid]))
        else:
            courses.append(build_course_from_node(node, domain_id, subject, i))
    return [enrich_graph_fields(c) for c in courses]


def agnes_remaining(course_id: str) -> int:
    try:
        proc = subprocess.run(
            [sys.executable, str(AGNES), "--course-id", course_id, "--quota"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
        )
        data = json.loads(proc.stdout)
        return int(data.get("course", {}).get("remaining", 0))
    except Exception:
        return 0


def pick_agnes_course_id(course_id: str) -> str:
    for n in range(0, 8):
        suffix = "" if n == 0 else f"-v{n + 1}"
        aid = f"{course_id}{suffix}"
        if agnes_remaining(aid) > 0:
            return aid
    return f"{course_id}-v8"


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def agnes_prompt(base: str) -> str:
    return base.rstrip(" ,") + AGNES_NO_TEXT


def labeled_figure(cid: str, slot: str, alt: str, caption: str, labels: list[tuple[str, str, str]]) -> str:
    tags = "".join(
        f'<span class="ta-fig-tag" style="top:{top};left:{left}">{esc(text)}</span>'
        for text, top, left in labels
    )
    return f'''<figure class="ta-standard-figure ta-figure-labeled">
  <div class="ta-figure-wrap">
    <img src="./assets/{cid}-{slot}.png" alt="{esc(alt)}">
    <div class="ta-figure-tags" aria-hidden="true">{tags}</div>
  </div>
  <figcaption>{esc(caption)}</figcaption>
</figure>'''


def slide(page: int, ptype: str, tsh: str, inner: str, tts: str = "") -> str:
    tts_attr = f' data-tts="{tts}"' if tts else ""
    return (
        f'<section class="slide-page" data-page-index="{page}" data-page-type="{ptype}" data-tsh="{esc(tsh)}">\n'
        f"{inner}\n</section>\n"
    )


def build_quiz_html(qid: str, quiz: dict) -> str:
    opts = []
    for i, item in enumerate(quiz["opts"]):
        text, ok, wrong = item[0], item[1], item[2] if len(item) > 2 else ""
        wrong_attr = f' data-wrong="{esc(wrong)}"' if wrong else ""
        opts.append(
            f'<button class="choice" onclick="checkAnswer(this,{str(ok).lower()},\'{qid}\')"{wrong_attr}>{esc(text)}</button>'
        )
    return (
        f'<p>{esc(quiz["q"])}</p>\n'
        + "\n".join(opts)
        + f'\n<div id="{qid}-feedback" class="result warn">选择后查看反馈。</div>'
    )


def build_html(c: dict) -> str:
    cid = c["course_id"]
    prereq = ",".join(c.get("prerequisites") or [])
    subj_label = "道德与法治" if c["subject"] == "politics" else "心理健康"
    anchors = "".join(
        f'<button class="choice" data-anchor-choice="{esc(a)}">{esc(a)}</button>' for a in c["anchors"]
    )
    objs = "".join(f"<li>{esc(o)}</li>" for o in c["objectives"])
    cps = "".join(f"<li>{esc(p)}</li>" for p in c["curriculum_points"])
    labels = c.get("image_labels") or {}
    hero_fig = labeled_figure(
        cid, "hero", c["title"], "本课知识结构示意（Agnes 无字生图，中文标注由课件叠加）", labels.get("hero", [])
    )
    sec1_fig = labeled_figure(
        cid, "section1", "核心概念", "关键概念示意（中文标注叠加）", labels.get("section1", [])
    )
    sec2_fig = labeled_figure(
        cid, "section2", "方法框架", "觉察—分析—行动框架（中文标注叠加）", labels.get("section2", [])
    )
    story_paras = "".join(f"<p>{esc(p)}</p>" for p in c["story_paras"])
    story_choices = "".join(
        f'<button class="choice story-opt" data-story-feedback="{esc(fb)}" onclick="pickStory(this)">{esc(txt)}</button>'
        for txt, fb in c["story_choices"]
    )
    ext_blocks = "".join(
        f'<div class="card ext-card"><h3>{esc(r["title"])}</h3>'
        f'<p class="ext-source">{esc(r["source"])}</p><p>{esc(r["text"])}</p></div>'
        for r in c["external_refs"]
    )
    case_blocks = []
    for i, card in enumerate(c["case_cards"]):
        opts = []
        for text, ok, wrong in card["options"]:
            wrong_attr = f' data-wrong="{esc(wrong)}"' if wrong else ""
            opts.append(
                f'<button class="choice case-opt" data-case="{i}" onclick="checkCase(this,{str(ok).lower()},{i})"{wrong_attr}>{esc(text)}</button>'
            )
        case_blocks.append(
            f'<div class="card case-card"><h3>{esc(card["title"])}</h3><p>{esc(card["desc"])}</p>'
            f'<div class="grid">{"".join(opts)}</div>'
            f'<div id="case-feedback-{i}" class="result warn">选择后查看解析。</div></div>'
        )
    case_html = "\n".join(case_blocks)
    recap = "".join(f"<li>{esc(p)}</li>" for p in c["recap_points"])

    pages = []
    pages.append(slide(0, "hero", "开场", f'''<section class="section hero" id="hero" data-tts="hero">
  <span class="phase-tag">{subj_label} · 初中{c["grade"]}年级</span>
  <h1>{esc(c["title"])}</h1>
  <p class="subtitle">{esc(c["hero_q"])}</p>
  {hero_fig}
</section>''', "hero"))
    pages.append(slide(1, "anchor", "问题锚点", f'''<section class="section" id="problem-anchor" data-tts="anchor">
  <div class="card"><span class="phase-tag">Problem Anchor</span><h2>你想先解决哪个问题？</h2>
  <div class="grid" id="problem-anchor-choices">{anchors}</div>
  <label class="field-label">我的问题<input id="learner-question-input" aria-label="自定义问题" placeholder="写下你的真实困惑…"></label>
  <p id="anchor-feedback" class="result warn">选择或输入后，本课会围绕你的问题展开。</p></div>
</section>''', "anchor"))
    pages.append(slide(2, "objectives", "学习目标", f'''<section class="section" id="objectives" data-tts="objectives">
  <div class="card"><span class="phase-tag">Learning Objectives</span><h2>学习目标</h2><ul class="objectives">{objs}</ul></div>
</section>''', "objectives"))
    pages.append(slide(3, "story", "真实故事", f'''<section class="section" id="story" data-tts="story">
  <div class="card story-card"><span class="phase-tag">Story</span><h2>{esc(c["story_title"])}</h2>
  <p><strong>And</strong> 主人公和你一样，面对真实校园生活。</p>
  {story_paras}</div>
  <div class="card"><span class="phase-tag">Choose</span><h2>如果是你，会怎么做？</h2>
  <div class="grid" id="story-choices">{story_choices}</div>
  <p id="story-feedback" class="result warn">点击选项，查看故事走向与课标启示。</p></div>
</section>''', "story"))
    pages.append(slide(4, "reading", "延伸知识", f'''<section class="section" id="external-knowledge" data-tts="external-knowledge">
  <div class="card"><span class="phase-tag">External Knowledge</span><h2>课标摘读与延伸阅读</h2>
  <p style="color:var(--muted)">结合权威来源理解本课要点。</p></div>
  {ext_blocks}
</section>''', "external-knowledge"))
    pages.append(slide(5, "core", "核心概念", f'''<section class="section" id="core" data-tts="core">
  <div class="card"><span class="phase-tag">Core Ideas</span><h2>核心概念</h2><ul>{cps}</ul>
  {sec1_fig}</div>
</section>''', "core"))
    pages.append(slide(6, "practice", "情境判断", f'''<section class="section" id="interactive" data-tts="interactive">
  <div class="card"><span class="phase-tag">Case Lab</span><h2>情境判断</h2>
  <p style="color:var(--muted)">阅读情境，选择更稳妥的回应。</p></div>
  {case_html}
  <div class="card"><span class="phase-tag">Reflect</span><h2>反思与可视化</h2>
  <label class="field-label">我的反思<textarea id="reflection-input" rows="3" placeholder="{esc(c["reflection"])}"></textarea></label>
  <div id="reflection-feedback" class="result">写下反思，形成学习证据。</div>
  <div class="control-row"><label>强度<input id="emo-level" type="range" min="1" max="10" value="5"></label>
  <label>应对<input id="cope-level" type="range" min="1" max="10" value="6"></label></div>
  <div class="canvas-wrap"><canvas id="lab-canvas" width="720" height="200" aria-label="互动图表"></canvas></div>
  <div id="lab-feedback" class="result">拖动滑块，观察变化。</div></div>
</section>''', "interactive"))
    pages.append(slide(7, "evidence", "方法框架", f'''<section class="section" id="framework" data-tts="framework">
  <div class="card"><span class="phase-tag">Method Framework</span><h2>可操作三步法</h2>
  <ol><li><strong>觉察</strong>：说出当下感受与触发事件</li><li><strong>分析</strong>：区分事实、想法与行为后果</li><li><strong>行动</strong>：选择一种课标鼓励的积极应对方式</li></ol>
  {sec2_fig}</div>
</section>''', "framework"))
    pages.append(slide(8, "example", "例题拆解", f'''<section class="section" id="worked-example" data-tts="worked-example">
  <div class="card"><span class="phase-tag">Worked Example</span><h2>案例拆解</h2>
  <p>回到故事「{esc(c["story_title"])}」：</p>
  <ol><li>描述<strong>事实</strong>（发生了什么）</li><li>识别<strong>感受</strong>（我/他感到什么）</li>
  <li>选择<strong>回应</strong>（课标鼓励的积极方式）</li><li>记录<strong>结果</strong>与反思</li></ol></div>
</section>''', "worked-example"))
    pages.append(slide(9, "deep", "五镜头深层理解", f'''<section class="section" id="deep-understanding" data-tts="deep-understanding">
  <div class="card"><span class="phase-tag">Five Lens</span><h2>五镜头深层理解</h2>
  <ul>
    <li><strong>看见它：</strong>本课核心概念在生活中的表现是什么？</li>
    <li><strong>拆开它：</strong>情绪/规则/压力背后有哪些可改变的因素？</li>
    <li><strong>解释它：</strong>用课标语言说明「为什么这样做更有效」。</li>
    <li><strong>比较它：</strong>对比冲动反应与理性回应的不同后果。</li>
    <li><strong>迁移它：</strong>换一个类似情境，你还能用同样方法吗？</li>
  </ul>
  <p class="result"><strong>记忆锚点：</strong>先觉察，再行动；把口号变成可核查的行为证据。</p></div>
</section>''', "deep-understanding"))
    pages.append(slide(10, "tiered", "三段式作业", f'''<section class="section" id="tiered-practice" data-tts="tiered-practice">
  <div class="card"><span class="phase-tag">Level Practice</span><h2>三段式作业</h2>
  <div class="grid">
    <div><h3>⭐ Level 1 基础巩固</h3><p>写出本课 3 个关键词，并各举一个生活例子。</p></div>
    <div><h3>⭐⭐ Level 2 能力应用</h3><p>用「觉察—分析—行动」完成一次真实情境记录。</p></div>
    <div><h3>⭐⭐⭐ Level 3 迁移挑战</h3><p>设计一个同伴互助小活动，帮助他人避免本课易错点。</p></div>
  </div></div>
</section>''', "tiered-practice"))
    pages.append(slide(11, "pretest", "前测", f'''<section class="section" id="pretest" data-tts="pretest">
  <div class="card"><span class="phase-tag">Pre-test</span><h2>前测</h2>
  {build_quiz_html("pretest", c["pretest"])}
  <p class="result warn" id="pretest-hint">常见错误：把压抑当管理，或把冲动当个性。</p></div>
</section>''', "pretest"))
    pages.append(slide(12, "recap", "课堂复盘", f'''<section class="section" id="recap" data-tts="recap">
  <div class="card recap-card"><span class="phase-tag">Text Recap</span><h2>课堂复盘卡（无视频，文字精讲）</h2>
  <ul class="recap-list">{recap}</ul>
  <p style="color:var(--muted)">勾选你今天做到的一项：</p>
  <div class="grid recap-checks">
    <label><input type="checkbox" class="recap-check"> 我完成了情境判断</label>
    <label><input type="checkbox" class="recap-check"> 我写下了反思或复盘</label>
    <label><input type="checkbox" class="recap-check"> 我能说出一个求助/行动渠道</label>
  </div>
  <div id="recap-feedback" class="result">勾选后，即形成本课学习闭环证据。</div></div>
</section>''', "recap"))
    pages.append(slide(13, "posttest", "后测", f'''<section class="section" id="posttest" data-tts="posttest">
  <div class="card"><span class="phase-tag">Post-test</span><h2>后测</h2>
  {build_quiz_html("posttest", c["posttest"])}</div>
</section>''', "posttest"))
    pages.append(slide(14, "summary", "总结", f'''<section class="section" id="summary" data-tts="summary">
  <div class="card"><span class="phase-tag">Summary</span><h2>一句话带走</h2><ul>{objs}</ul>
  <p class="result">把本课方法用到一次真实经历中，并写下复盘。</p></div>
</section>''', "summary"))
    pages.append(slide(15, "graph", "知识图谱", f'''<section class="section" id="knowledge-graph" data-tts="knowledge-graph">
  <div class="card"><span class="phase-tag">Knowledge Graph</span><h2>知识图谱</h2>
  <p style="color:var(--muted)">本节点的前置、后续由标准知识图谱模块渲染。</p>
  <div {kg_div_attrs(c)}><canvas class="tkg-fallback-canvas" width="720" height="120" aria-label="知识图谱画布" style="display:block;width:100%"></canvas></div></div>
</section>''', "knowledge-graph"))
    pages.append(slide(16, "tutor", "AI学伴", f'''<section class="section" id="teachany-ai-tutor-card" data-tts="ai-tutor">
  <div data-teachany-tutor-card></div>
</section>''', "ai-tutor"))

    body = "\n".join(pages)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{esc(c["title"])} · {subj_label} G{c["grade"]} · TeachAny v{TEACHANY_VER}</title>
<meta name="description" content="{esc(c["title"])} — 中国课标{subj_label}互动课件">
<meta name="course-id" content="{cid}">
<meta name="course-title" content="{esc(c["title"])}">
<meta name="course-subject" content="{c["subject"]}">
<meta name="course-grade" content="middle-{c["grade"]}">
<meta name="course-prereqs" content="{prereq}">
<meta name="teachany-prerequisites" content="{prereq}">
<meta name="teachany-version" content="{TEACHANY_VER}">
<meta name="teachany-node" content="{c["node_id"]}">
<meta name="teachany-subject" content="{c["subject"]}">
<meta name="teachany-grade" content="{c["grade"]}">
<meta name="teachany-stage" content="{c["stage"]}">
<meta name="teachany-domain" content="{c["domain"]}">
<meta name="teachany-lesson-type" content="{c["lesson_type"]}">
<meta name="teachany-free-mode" content="false">
<meta name="teachany-template-version" content="2.0">
<link rel="stylesheet" href="{SITE_SCRIPTS}/ai-tutor.css">
<link rel="stylesheet" href="{SITE_SCRIPTS}/teachany-tutor-card.css">
<link rel="stylesheet" href="{SITE_SCRIPTS}/teachany-tts-narrator.css">
<link rel="stylesheet" href="{SITE_SCRIPTS}/teachany-section-hints.css">
<link rel="stylesheet" href="{SITE_SCRIPTS}/teachany-knowledge-graph.css">
<link rel="stylesheet" href="{SITE_SCRIPTS}/teachany-audio-player.css">
<link rel="stylesheet" href="{SITE_SCRIPTS}/teachany-floating-dock.css">
<link rel="stylesheet" href="{SLIDE_CSS}">
<style>
:root {{
  --bg:#f8fafc; --bg-subtle:#f1f5f9; --panel:#fff; --card:#fff; --line:#e2e8f0;
  --text:#0f172a; --muted:#64748b; --brand:{c["accent"]}; --brand-2:{c["accent2"]};
  --ok:#16a34a; --warn:#d97706; --danger:#dc2626; --card-radius:14px;
}}
body.teachany-middle {{ background:var(--bg); color:var(--text); font-family:-apple-system,BlinkMacSystemFont,"PingFang SC",sans-serif; }}
.hero {{ text-align:center; padding:48px 20px 28px; background:linear-gradient(180deg,rgba(255,255,255,.9),var(--bg)); }}
h1 {{ font-size:clamp(26px,5vw,42px); margin:12px auto; max-width:900px; }}
.subtitle {{ color:var(--muted); max-width:760px; margin:0 auto; }}
.section {{ max-width:1080px; margin:0 auto; padding:28px 20px; }}
.card {{ background:var(--card); border:1px solid var(--line); border-radius:var(--card-radius); padding:22px; box-shadow:0 8px 24px rgba(15,23,42,.06); }}
.phase-tag {{ display:inline-block; font-size:12px; font-weight:700; color:var(--brand); background:rgba(0,0,0,.04); padding:4px 10px; border-radius:999px; margin-bottom:8px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:12px; }}
.choice {{ width:100%; text-align:left; border:1px solid var(--line); border-radius:12px; background:#fff; padding:12px 14px; cursor:pointer; min-height:44px; }}
.choice.selected {{ border-color:var(--brand); box-shadow:0 0 0 3px rgba(0,0,0,.06); }}
.objectives {{ padding-left:1.2rem; }}
.control-row {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:12px; margin:12px 0; }}
.canvas-wrap {{ background:var(--bg-subtle); border:1px solid var(--line); border-radius:12px; padding:12px; }}
.field-label {{ display:block; margin-top:14px; color:var(--muted); font-size:14px; }}
.field-label input, .field-label textarea {{ display:block; width:100%; margin-top:6px; padding:10px 12px; border:1px solid var(--line); border-radius:10px; font:inherit; }}
.result {{ margin-top:12px; padding:12px; border-radius:10px; background:rgba(22,163,74,.08); border:1px solid rgba(22,163,74,.2); }}
.result.warn {{ background:rgba(217,119,6,.08); border-color:rgba(217,119,6,.25); }}
.teachany-brand-bar {{ position:sticky; top:0; z-index:50; display:flex; align-items:center; justify-content:space-between; padding:10px 16px; background:rgba(255,255,255,.92); border-bottom:1px solid var(--line); }}
.ta-figure-wrap {{ position:relative; display:inline-block; max-width:100%; }}
.ta-figure-labeled img {{ width:100%; border-radius:12px; display:block; }}
.ta-figure-tags {{ position:absolute; inset:0; pointer-events:none; }}
.ta-fig-tag {{ position:absolute; transform:translate(-50%,-50%); background:rgba(15,23,42,.82); color:#fff; font-size:13px; font-weight:600; padding:4px 10px; border-radius:8px; white-space:nowrap; box-shadow:0 4px 12px rgba(0,0,0,.15); }}
.ta-standard-figure figcaption {{ margin-top:10px; color:var(--muted); font-size:14px; text-align:center; }}
.ext-card h3 {{ margin:0 0 6px; font-size:16px; color:var(--brand); }}
.ext-source {{ font-size:12px; color:var(--muted); margin:0 0 8px; }}
.story-card p {{ line-height:1.7; }}
.case-card h3 {{ margin-top:0; }}
.recap-list {{ padding-left:1.2rem; line-height:1.8; }}
.recap-checks label {{ display:flex; align-items:center; gap:8px; padding:10px; border:1px solid var(--line); border-radius:10px; background:#fff; }}
</style>
</head>
<body class="teachany-middle">
<div class="teachany-brand-bar">
  <a href="https://www.teachany.cn/" style="font-weight:800;color:var(--text);text-decoration:none">TeachAny</a>
  <span style="font-size:12px;color:var(--muted)">{subj_label} · G{c["grade"]}</span>
</div>
<div class="slide-progress-bar" id="slide-progress-bar"></div>
<nav class="slide-sidenav" id="slide-sidenav" aria-label="分页导航"></nav>
<button aria-label="切换播放模式" class="play-mode-fab" id="play-mode-fab" title="播放模式 (F)">
  <svg id="fab-icon-play" viewBox="0 0 24 24"><path d="M8 5v14l11-7z"></path></svg>
  <svg id="fab-icon-browse" style="display:none" viewBox="0 0 24 24"><path d="M4 6h16v2H4zM4 11h16v2H4zM4 16h16v2H4z"></path></svg>
</button>
<div class="slide-toolbar" id="slide-toolbar">
  <button class="toolbar-btn" id="tb-prev" type="button" aria-label="上一页">‹</button>
  <div class="toolbar-page-info" id="tb-page-info">1 / 17</div>
  <button class="toolbar-btn" id="tb-next" type="button" aria-label="下一页">›</button>
  <div class="toolbar-progress" id="tb-progress"><div class="toolbar-progress-fill" id="tb-progress-fill"></div></div>
  <button class="toolbar-btn" id="tb-autoplay" type="button" aria-label="自动播放">Auto</button>
  <button class="toolbar-btn" id="tb-fullscreen" type="button" aria-label="全屏">⛶</button>
</div>
<div class="slide-container" id="slide-container">
{body}
</div>
<script>
const FEEDBACK={{ pretest:"回到课标要点，选择可核查的积极应对。", posttest:"把方法用到真实情境才算学会。" }};
function checkAnswer(btn,ok,target){{btn.parentElement.querySelectorAll('.choice').forEach(b=>b.classList.remove('selected'));btn.classList.add('selected');const box=document.getElementById(target+'-feedback');if(box)box.textContent=ok?FEEDBACK[target]||'回答正确。':((btn.dataset.wrong||'易错点：回到情境事实与课标要点。')+' '+(FEEDBACK[target]||''));}}
function checkCase(btn,ok,idx){{const card=btn.closest('.case-card');card.querySelectorAll('.choice').forEach(b=>b.classList.remove('selected'));btn.classList.add('selected');const box=document.getElementById('case-feedback-'+idx);if(box)box.textContent=ok?'判断合理，与课标/延伸阅读一致。':(btn.dataset.wrong||'再读情境与延伸知识，选择更稳妥的回应。');}}
function pickStory(btn){{document.querySelectorAll('.story-opt').forEach(b=>b.classList.remove('selected'));btn.classList.add('selected');const box=document.getElementById('story-feedback');if(box)box.textContent=btn.dataset.storyFeedback||'';}}
function setTeachAnyLearnerQuestion(q){{window.__TEACHANY_LEARNER_QUESTION__=q||'';const f=document.getElementById('anchor-feedback');if(f)f.textContent=q?`你的问题：${{q}}`:'选择或输入后，本课会围绕你的问题展开。';}}
document.querySelectorAll('[data-anchor-choice]').forEach(btn=>btn.addEventListener('click',()=>setTeachAnyLearnerQuestion(btn.getAttribute('data-anchor-choice')||btn.textContent.trim())));
document.getElementById('learner-question-input')?.addEventListener('input',e=>setTeachAnyLearnerQuestion(e.target.value.trim()));
document.getElementById('reflection-input')?.addEventListener('input',e=>{{const f=document.getElementById('reflection-feedback');if(f&&e.target.value.trim())f.textContent='已记录反思，可保存截图作为学习证据。';}});
document.querySelectorAll('.recap-check').forEach(cb=>cb.addEventListener('change',()=>{{const n=document.querySelectorAll('.recap-check:checked').length;const f=document.getElementById('recap-feedback');if(f)f.textContent=n?`已勾选 ${{n}} 项，学习闭环完成度提升。`:'勾选你今天做到的一项。';}}));
(function(){{const c=document.getElementById('lab-canvas');if(!c)return;const ctx=c.getContext('2d');const e=document.getElementById('emo-level');const p=document.getElementById('cope-level');const f=document.getElementById('lab-feedback');function draw(){{const emo=+e.value, cope=+p.value;ctx.clearRect(0,0,c.width,c.height);ctx.fillStyle='#e2e8f0';ctx.fillRect(0,0,c.width,c.height);ctx.fillStyle='#0f172a';ctx.font='15px sans-serif';ctx.fillText(`强度 ${{emo}}/10 · 应对 ${{cope}}/10`,20,28);ctx.fillStyle='{c["accent"]}';ctx.fillRect(60,180-emo*14,100,emo*14);ctx.fillStyle='{c["accent2"]}';ctx.fillRect(280,180-cope*14,100,cope*14);if(f)f.textContent=emo>7&&cope<5?'高强度时优先暂停冲动、寻求支持。':'保持觉察，选一种具体行动试试。';}}e?.addEventListener('input',draw);p?.addEventListener('input',draw);draw();}})();
window.__TEACHANY_TUTOR_CONFIG__={{courseId:'{cid}',courseTitle:'{esc(c["title"])}',subject:'{c["subject"]}',grade:'{c["grade"]}',nodeId:'{c["node_id"]}',lessonType:'{c["lesson_type"]}',getLearnerQuestion:()=>window.__TEACHANY_LEARNER_QUESTION__||'',getContext:()=>document.body.innerText.slice(0,3000)}};
</script>
<script src="/assets/teachany-slide-v2.js"></script>
<script src="{SITE_SCRIPTS}/ai-tutor.js"></script>
<script src="{SITE_SCRIPTS}/teachany-tutor-card.js"></script>
<script src="{SITE_SCRIPTS}/teachany-tts-narrator.js"></script>
<script src="{SITE_SCRIPTS}/teachany-section-hints.js"></script>
<script src="{SITE_SCRIPTS}/teachany-knowledge-graph.js"></script>
<script src="{SITE_SCRIPTS}/teachany-audio-player.js"></script>
</body>
</html>
'''


def build_manifest(c: dict) -> dict:
    cid = c["course_id"]
    subj_label = "道德与法治" if c["subject"] == "politics" else "心理健康"
    return {
        "id": cid,
        "course_id": cid,
        "node_id": c["node_id"],
        "name": c["title"],
        "name_en": c["title_en"],
        "subject": c["subject"],
        "grade": c["grade"],
        "stage": c["stage"],
        "domain": c["domain"],
        "lesson_type": c["lesson_type"],
        "status": "community",
        "author": "TeachAny",
        "version": "1.1.0",
        "teachany_version": TEACHANY_VER,
        "template_version": "2.0",
        "curriculum": "cn",
        "description": f"中国课标{subj_label}互动课件：{c['title']}（故事+延伸知识+文字互动，无占位视频）",
        "tags": [subj_label, f"初中{c['grade']}年级", "课标互动", "Agnes无字插图"],
        "prerequisites": c.get("prerequisites") or [],
        "leads_to": c.get("leads_to") or [],
        "learning_objectives": c["objectives"],
        "assets": {
            "hero": f"assets/{cid}-hero.png",
            "tts_manifest": "tts/manifest.json",
            "images": [f"assets/{cid}-hero.png", f"assets/{cid}-section1.png", f"assets/{cid}-section2.png"],
        },
        "has_tts": True,
        "has_video": False,
        "has_images": True,
        "has_hero": True,
        "has_canvas": False,
        "has_knowledge_graph": True,
        "free_mode": False,
        "feedback": {
            "require_password": True,
            "password_sha256": "",
            "password_hint": "向任课教师索取课堂口令",
        },
        "created_at": TODAY,
        "updated_at": TODAY,
    }


def build_kcp(c: dict) -> dict:
    return {
        "node_id": c["node_id"],
        "topic": c["title"],
        "name_zh": c["title"],
        "subject": c["subject"],
        "stage": c["stage"],
        "curriculum": "cn",
        "lookup_at": f"{TODAY}T00:00:00Z",
        "sources": ["cn-curriculum-tree"],
        "curriculum_excerpts": [
            {"id": f"cp-{i+1}", "text": p, "source": "cn/middle/" + c["subject"] + ".json"}
            for i, p in enumerate(c["curriculum_points"])
        ] + [
            {"id": f"ext-{i+1}", "text": r["text"], "source": r["source"]}
            for i, r in enumerate(c["external_refs"])
        ],
        "exercises": [
            {"id": "q1", "stem": c["hero_q"], "answer": c["objectives"][0], "source": "generated"},
            {"id": "q2", "stem": c["pretest"]["q"], "answer": c["pretest"]["opts"][0][0], "source": "generated"},
        ],
        "common_errors": [
            {"id": "e1", "text": "只记口号，不联系真实情境练习", "source": "generated"},
            {"id": "e2", "text": "把情绪压抑或冲动发泄当作成熟", "source": "generated"},
        ],
    }


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, cwd=cwd or ROOT, check=True)


def remove_placeholder_videos(out: Path, cid: str) -> None:
    for p in [
        out / "assets" / "video" / f"{cid}-main.mp4",
        out / "assets" / f"{cid}-main.mp4",
    ]:
        if p.is_file():
            p.unlink()
            print(f"  删除占位视频 {p.name}")


def regen_agnes(c: dict, out: Path) -> bool:
    cid = c["course_id"]
    agnes_id = pick_agnes_course_id(cid)
    batch = [
        {"name": f"{cid}-hero", "prompt": agnes_prompt(c["agnes"]["hero"]), "slot": "hero"},
        {"name": f"{cid}-section1", "prompt": agnes_prompt(c["agnes"]["section1"]), "slot": "section1"},
        {"name": f"{cid}-section2", "prompt": agnes_prompt(c["agnes"]["section2"]), "slot": "section2"},
    ]
    batch_path = out / "agnes-batch.json"
    batch_path.write_text(json.dumps(batch, ensure_ascii=False, indent=2), encoding="utf-8")
    if not AGNES.is_file():
        AGNES_FALLBACK = SKILL / "scripts" / "agnes-image-gen.py"
        agnes_bin = AGNES_FALLBACK if AGNES_FALLBACK.is_file() else AGNES
    else:
        agnes_bin = AGNES

    print(f"  Agnes 配额桶: {agnes_id}（原课件 {cid} 额度用尽时用 -v2 重生成）")
    ok = 0
    for i, task in enumerate(batch):
        if i > 0:
            time.sleep(AGNES_IMAGE_DELAY_SEC)
        out_path = out / "assets" / f"{task['name']}.png"
        try:
            run([
                sys.executable, str(agnes_bin),
                "--course-id", agnes_id,
                "--prompt", task["prompt"],
                "--out", str(out_path),
                "--slot", task["slot"],
            ])
            ok += 1
            print(f"  ✅ {out_path.name}")
        except subprocess.CalledProcessError as e:
            print(f"  ❌ {task['name']}: {e}")
    if ok:
        print(f"  Agnes 完成 {ok}/{len(batch)} 张")
        return True
    print("  ⚠️ Agnes 重生成失败，保留现有插图")
    return False


def regen_tts(out: Path) -> None:
    """删除旧 TTS，让 finalize 按新分页重新生成旁白。"""
    tts_dir = out / "tts"
    if tts_dir.is_dir():
        shutil.rmtree(tts_dir)
    html_path = out / "index.html"
    html = html_path.read_text(encoding="utf-8")
    html = re.sub(
        r'<script[^>]*\bid=["\']teachany-audio-playlist["\'][^>]*>.*?</script>\s*',
        "",
        html,
        flags=re.S,
    )
    html_path.write_text(html, encoding="utf-8")


def finalize_course(out: Path, cid: str, *, regen_tts_audio: bool = True) -> None:
    if regen_tts_audio:
        regen_tts(out)
    # --shared：引用站点根 /assets/scripts/（gh-pages 发布排除 community/*/assets/scripts/）
    run([sys.executable, str(FINALIZE), str(out), "--shared"])
    run([sys.executable, str(SET_PW), str(out / "manifest.json"), "--password", "道法心理2026", "--hint", "课堂抽样审查口令"])


def refresh_course(c: dict, *, regen_images: bool = False, regen_tts_audio: bool = True) -> Path:
    out = ROOT / "community" / c["course_id"]
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(build_html(c), encoding="utf-8")
    (out / "manifest.json").write_text(json.dumps(build_manifest(c), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "knowledge-context.json").write_text(json.dumps(build_kcp(c), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    remove_placeholder_videos(out, c["course_id"])
    if regen_images:
        regen_agnes(c, out)
    finalize_course(out, c["course_id"], regen_tts_audio=regen_tts_audio)
    (out / "PLAN.md").write_text(
        f"# {c['course_id']}\n\n"
        f"## 知识层引用\n\n"
        f"- 课标节点：`{c['node_id']}`（{c['title']}）\n"
        f"- 来源：`data/trees/cn/middle/{c['subject']}.json`\n"
        f"- v1.1：无占位视频；Agnes 无字生图 + HTML 中文叠加；故事/延伸知识/情境判断\n",
        encoding="utf-8",
    )
    return out


def gen_course(c: dict) -> Path:
    return refresh_course(c, regen_images=True)


def main() -> int:
    argv = sys.argv[1:]
    refresh_only = "--refresh-html" in argv
    regen_images = "--regen-images" in argv
    regen_tts = "--regen-tts" in argv
    force = "--force" in argv
    gen_all = "--all" in argv
    only_ids = [a for a in argv if re.match(r"^(pol|psych)-m-", a)]

    if only_ids:
        target = [c for c in load_all_tree_courses() if c["course_id"] in only_ids]
    elif gen_all:
        target = load_all_tree_courses()
    else:
        target = COURSES
    print(f"目标课件：{len(target)} 门" + ("（课标树全部节点）" if gen_all else "（抽样 5 门）"))

    results = []
    for c in target:
        cid = c["course_id"]
        out = ROOT / "community" / cid
        print(f"\n{'='*60}\n处理: {cid}\n{'='*60}")
        if refresh_only or regen_images or force:
            if not out.is_dir() and not force:
                print("  跳过（目录不存在）")
                continue
            try:
                refresh_course(c, regen_images=regen_images, regen_tts_audio=regen_tts)
                log = subprocess.run(
                    ["bash", str(BASELINE), str(out)],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                )
                ok = log.returncode == 0
                print(log.stdout[-1500:] if log.stdout else "")
                if not ok:
                    print(log.stderr[-400:] if log.stderr else "")
                results.append((cid, ok))
            except Exception as e:
                print(f"FAIL {cid}: {e}")
                results.append((cid, False))
            continue

        if (out / "assets" / f"{cid}-hero.png").is_file() and (out / "tts").is_dir() and not force:
            print("  跳过（已生成，用 --refresh-html 或 --force）")
            results.append((cid, True))
            continue
        try:
            out = gen_course(c)
            log = subprocess.run(
                ["bash", str(BASELINE), str(out)],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            ok = log.returncode == 0
            print(log.stdout[-1500:] if log.stdout else "")
            if not ok:
                print(log.stderr[-400:] if log.stderr else "")
            results.append((cid, ok))
        except subprocess.CalledProcessError as e:
            print(f"FAIL {cid}: {e}")
            results.append((cid, False))

    print("\n汇总:")
    for cid, ok in results:
        print(f"  {'✅' if ok else '❌'} {cid}")
    if gen_all and all(x[1] for x in results):
        print("\n重建知识树索引…")
        run([sys.executable, str(ROOT / "scripts" / "rebuild-index.py")])
    return 0 if all(x[1] for x in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
