#!/usr/bin/env python3
"""Add topic-specific depth modules to chem-m shell courses.

Middle-school chemistry courses often pass via template sections but lack
topic-specific core teaching. Each course gets 知识精讲 + 方法范例
(worked example + diagnostic + 常见误区). No mp4. Idempotent via id="lesson-focus".
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-11"


def C(ct, cb, mt, mb, ex, q, opts, correct, fb, pit):
    return dict(
        concept_title=ct, concept_body=cb, method_title=mt, method_body=mb,
        example=ex, question=q, options=opts, correct=correct, feedback=fb, pitfall=pit,
    )


COURSES = {
    "chem-m-chemistry-intro": C(
        "走进化学世界",
        "化学研究物质的组成、结构、性质、变化及规律。学习化学要会观察现象、提出问题、设计实验、得出结论。化学变化有新物质生成，物理变化没有；许多变化往往伴随发光、放热、气体、沉淀等现象，但现象不是判断依据的唯一标准。",
        "方法：变化先看有无新物质",
        "判断物理/化学变化：抓住“是否生成新物质”。再联系生活例子，避免只背定义。",
        "纸张撕碎是物理变化；纸燃烧生成二氧化碳等是化学变化。",
        "化学变化的本质特征是？",
        ["发光发热", "生成新物质", "状态改变", "体积变化"],
        1,
        "有新物质生成才是化学变化。",
        "常见误区是把发光、放热等现象当成化学变化的充分条件。",
    ),
    "chem-m-lab-safety": C(
        "实验基本操作与安全",
        "化学实验必须遵守安全规范：正确使用酒精灯、试管加热、药品取用、气体收集等。操作顺序、仪器选择与安全隐患排查是考试与实践的重点。先想“为什么这样操作”，再动手。",
        "方法：仪器—步骤—注意事项三联",
        "每项操作写清：用什么仪器、怎么做、不能怎样。加热液体先预热，试管口不对人。",
        "点燃酒精灯用火柴，禁止用燃着的酒精灯去点另一盏，防止失火。",
        "给试管中液体加热时，试管口应？",
        ["对着自己", "对着别人", "不对着任何人", "随便"],
        2,
        "防止液体喷出伤人。",
        "常见误区是背步骤却说不清安全原因，或药品取用量越大越好。",
    ),
    "chem-m-scientific-inquiry-experiment": C(
        "科学探究方法",
        "科学探究通常包括提出问题、猜想假设、制定计划、进行实验、收集证据、得出结论、反思评价。控制变量、设置对照、多次测量可提高结论可靠性。化学探究要把宏观现象与微观解释联系起来。",
        "方法：变量清晰 + 证据说话",
        "写方案时标明改变什么、控制什么、观察什么。结论必须由实验现象与数据支持。",
        "探究温度对反应快慢的影响：只改温度，浓度、固体颗粒大小等保持相同。",
        "探究实验中设置对照的主要目的是？",
        ["增加工作量", "便于比较，突出自变量作用", "让现象更热闹", "可以不做记录"],
        1,
        "对照帮助判断变化是否由所研究因素引起。",
        "常见误区是一次实验就下绝对结论，或同时改变多个变量。",
    ),
    "chem-m-air-composition": C(
        "空气的组成",
        "空气主要是氮气（约 78%）和氧气（约 21%），还有稀有气体、二氧化碳、其他气体与杂质。氧气支持燃烧与呼吸，氮气化学性质较稳定，稀有气体可作保护气、霓虹灯等。认识空气污染与防治也是本课延伸。",
        "方法：成分—性质—用途对照",
        "先记体积分数，再各举一条性质与用途。实验测氧气含量常用红磷燃烧法，注意装置气密与冷却读数。",
        "红磷燃烧消耗氧气，水面上升约 1/5，说明氧气约占空气体积的 1/5。",
        "空气中体积分数最大的气体是？",
        ["氧气", "氮气", "二氧化碳", "稀有气体"],
        1,
        "氮气约占 78%。",
        "常见误区是把质量分数与体积分数混淆，或认为空气是一种纯净物。",
    ),
    "chem-m-oxygen-preparation": C(
        "氧气的制取",
        "实验室常用过氧化氢在二氧化锰催化下分解，或加热高锰酸钾制氧气。发生装置看反应物状态与反应条件，收集用排水法或向上排空气法。验满：带火星木条放瓶口复燃。",
        "方法：发生—收集—验满三步",
        "先选药品与装置，再选收集方法（氧气不易溶于水、密度比空气略大），最后验满与检验。",
        "双氧水制氧：常温、固液不加热型装置；用排水法收集较纯净。",
        "用带火星木条检验氧气的现象是？",
        ["木条熄灭", "木条复燃", "产生白烟", "溶液变红"],
        1,
        "氧气支持燃烧，带火星木条复燃。",
        "常见误区是验满与检验位置不分，或高锰酸钾试管口向上倾斜。",
    ),
    "chem-m-co2-properties": C(
        "二氧化碳的性质与制取",
        "二氧化碳密度比空气大，不能燃烧也不支持燃烧，能溶于水生成碳酸，可使澄清石灰水变浑浊。实验室用大理石（或石灰石）与稀盐酸反应制取，向上排空气法收集，验满用燃着木条。",
        "方法：性质实验与制取装置对应",
        "灭火、温室效应、碳酸饮料联系性质。制取不用硫酸（微溶物覆盖）与浓盐酸（挥发性杂质）。",
        "通入澄清石灰水变浑浊：CO₂+Ca(OH)₂=CaCO₃↓+H₂O，是检验 CO₂ 的常用方法。",
        "检验二氧化碳最常用的试剂是？",
        ["紫色石蕊", "澄清石灰水", "酚酞", "蒸馏水"],
        1,
        "澄清石灰水变浑浊可检验 CO₂。",
        "常见误区是用燃着木条熄灭就断定一定是二氧化碳（也可能是氮气等）。",
    ),
    "chem-m-co-properties": C(
        "一氧化碳的性质",
        "一氧化碳有毒，能与血红蛋白结合；具有可燃性与还原性，可还原某些金属氧化物。它与二氧化碳在组成上差一个氧原子，性质差异很大。使用煤炉等要注意通风防中毒。",
        "方法：毒性—可燃—还原三条",
        "写性质各配一条实验或用途。强调安全：煤气中毒急救与预防。",
        "CO 还原 CuO：黑色变红，生成 CO₂，体现还原性。",
        "一氧化碳中毒的主要原因是？",
        ["密度太大", "与血红蛋白结合导致缺氧", "易溶于水", "支持燃烧"],
        1,
        "CO 与血红蛋白结合削弱输氧能力。",
        "常见误区是把 CO 与 CO₂ 性质混记，或忽视其毒性。",
    ),
    "chem-m-hydrogen-properties": C(
        "氢气的性质",
        "氢气是最轻的气体，难溶于水，具有可燃性与还原性。点燃前必须验纯，防止爆炸。氢气燃烧产物是水，也可还原某些金属氧化物。它是重要的清洁能源方向之一。",
        "方法：验纯—燃烧—还原",
        "收集用排水法；验纯听声音；燃烧现象淡蓝色火焰，罩冷烧杯有水雾。",
        "氢气还原氧化铜：黑色变红，管口有水珠，体现还原性与氢组成。",
        "点燃氢气前必须？",
        ["加热导管", "验纯", "加入催化剂", "通入氧气"],
        1,
        "不纯氢气点燃可能爆炸，必须验纯。",
        "常见误区是不验纯就点燃，或认为氢气支持燃烧。",
    ),
    "chem-m-water-properties": C(
        "水的组成与净化",
        "水由氢、氧元素组成，电解水可证明：正极产氧气、负极产氢气，体积比约 1:2。天然水含杂质，净化包括沉淀、过滤、吸附、蒸馏等。节约用水与保护水资源是社会责任。",
        "方法：组成实验 + 净化流程",
        "电解水联系元素组成；净化按“由简到繁”选方法，蒸馏可得蒸馏水。",
        "过滤除去不溶性杂质，不能除去可溶性杂质；硬水软化另有方法。",
        "电解水时，生成氢气与氧气的体积比约为？",
        ["1:1", "1:2", "2:1", "1:8"],
        2,
        "氢气体积约为氧气体积的 2 倍。",
        "常见误区是正负极气体记反，或以为过滤能得到纯净蒸馏水。",
    ),
    "chem-m-carbon-allotropes": C(
        "碳的单质：金刚石、石墨与 C₆₀",
        "金刚石、石墨、C₆₀ 都是碳的单质，但原子排列不同，性质差异很大：金刚石坚硬，石墨滑腻导电，C₆₀ 呈足球状结构。这说明结构决定性质。碳还可形成一氧化碳、二氧化碳等化合物。",
        "方法：结构不同→性质不同",
        "比较硬度、导电性、用途。强调它们是单质不是化合物。",
        "石墨作电极、铅笔芯；金刚石作切削工具，用途由性质决定。",
        "金刚石和石墨属于？",
        ["同种化合物", "碳的不同单质（同素异形体）", "混合物", "氧化物"],
        1,
        "它们是碳元素形成的不同单质。",
        "常见误区是认为金刚石含有其他元素，或把煤、焦炭简单等同于纯碳单质。",
    ),
    "chem-m-matter-classification": C(
        "物质的分类",
        "物质可分为纯净物与混合物；纯净物分为单质与化合物；化合物又有氧化物、酸、碱、盐等。分类标准要统一，同一物质在不同标准下归属不同。掌握分类有助于系统记忆性质。",
        "方法：树状分类图",
        "先分纯净/混合，再分单质/化合物，最后到酸碱盐氧化物。举例时避免交叉标准。",
        "空气是混合物；氧气是单质；二氧化碳是化合物（氧化物）。",
        "由两种或多种物质混合而成的是？",
        ["单质", "化合物", "混合物", "纯净物"],
        2,
        "混合物由多种物质组成。",
        "常见误区是把化合物当成混合物，或认为纯净物只有一种元素。",
    ),
    "chem-m-substance-classification": C(
        "纯净物、混合物与化合物",
        "纯净物组成固定，有固定熔点沸点；混合物组成不固定。单质由一种元素组成，化合物由不同元素组成。区分时看“几种物质、几种元素”，不要被外观欺骗。",
        "方法：物质种数 vs 元素种数",
        "先问有几种物质，再问元素种类。合金、溶液、空气常是混合物。",
        "水是化合物（纯净物）；盐水是混合物；铁是单质。",
        "下列属于化合物的是？",
        ["氧气", "氮气", "二氧化碳", "空气"],
        2,
        "二氧化碳由碳、氧两种元素组成，是化合物。",
        "常见误区是看见“含多种元素”就说是混合物，忽略化合物也可以多种元素。",
    ),
    "chem-m-atom-molecule": C(
        "分子与原子",
        "分子是保持物质化学性质的最小粒子，原子是化学变化中的最小粒子。分子可分，原子在化学变化中不可再分（核反应除外）。微粒都在不停运动，粒子间有间隔。用微粒观点解释蒸发、扩散、热胀冷缩。",
        "方法：化学变化看原子重新组合",
        "物理变化分子本身不变；化学变化分子破裂、原子重组成新分子。",
        "水电解：水分子破坏，氢、氧原子重新组合成氢气、氧气分子。",
        "在化学变化中，下列粒子不可再分的是？",
        ["分子", "原子", "物质", "溶液"],
        1,
        "化学变化中原子是最小粒子。",
        "常见误区是认为分子、原子都会“消失”，或把原子说成一定比分子小（不绝对）。",
    ),
    "chem-m-atom-structure": C(
        "原子的结构",
        "原子由原子核与核外电子构成；核内有质子与中子，质子数决定元素种类，核电荷数=质子数=核外电子数（原子）。相对原子质量约等于质子数与中子数之和。初步认识原子结构为离子与化合价打基础。",
        "方法：三相等记住原子电中性",
        "核电荷数=质子数=核外电子数。质量主要集中在核上。",
        "碳原子质子数 6，则核外电子数 6，核电荷数 6。",
        "决定元素种类的是？",
        ["中子数", "质子数", "电子数一定不变", "相对原子质量"],
        1,
        "质子数决定元素种类。",
        "常见误区是把中子数当成元素判据，或认为原子一定不可再分到电子层面讨论。",
    ),
    "chem-m-atomic-structure-demo": C(
        "原子结构模型入门",
        "原子结构可用简单模型理解：核很小却集中几乎全部质量，电子在核外空间运动。不同元素原子的质子数不同。模型帮助想象微观世界，但不等于真实照片。学习时把“质子、中子、电子”职责分清。",
        "方法：模型对应三条信息",
        "看质子数识元素，看电子数想得失，看中子数理解同位素入门概念（初中点到为止）。",
        "画原子结构示意图时，圆圈表示核，弧线分层表示电子。",
        "原子中质量最小的粒子通常是？",
        ["质子", "中子", "电子", "原子核"],
        2,
        "电子质量远小于质子、中子。",
        "常见误区是把模型当成实物比例照片，或核与电子职责记混。",
    ),
    "chem-m-element-concept": C(
        "元素",
        "元素是具有相同核电荷数（质子数）的一类原子的总称。元素只讲种类不讲个数；物质组成用元素描述，构成用分子原子离子描述。元素符号书写规则与元素周期表初识是基本技能。",
        "方法：种类与个数分清",
        "说“水由氢元素和氧元素组成”，不说“由两个氢元素”。写符号注意大小写。",
        "CO₂ 含碳、氧两种元素；一个二氧化碳分子由一个碳原子与两个氧原子构成。",
        "元素强调的是？",
        ["原子个数", "原子种类（核电荷数相同）", "分子质量", "溶液浓度"],
        1,
        "元素是核电荷数相同的一类原子的总称。",
        "常见误区是元素与原子概念混用，或元素符号大小写错误。",
    ),
    "chem-m-ion-concept": C(
        "原子怎样变成离子",
        "原子得失电子后形成离子：得电子形成阴离子，失电子形成阳离子。离子是带电的原子或原子团。钠原子失 1 个电子成 Na⁺，氯原子得 1 个电子成 Cl⁻。离子符号要标电荷数与正负。",
        "方法：得失电子定阴阳",
        "金属原子易失电子变阳离子；非金属原子易得电子变阴离子。电荷数等于得失电子数。",
        "Mg 失 2e⁻ → Mg²⁺；O 得 2e⁻ → O²⁻。",
        "阴离子的形成原因是原子？",
        ["失去电子", "得到电子", "失去质子", "得到中子"],
        1,
        "得电子显负电，成为阴离子。",
        "常见误区是离子电荷正负写反，或把质子得失当成离子形成原因。",
    ),
    "chem-m-chemical-formula": C(
        "化学式与化合价",
        "化学式表示物质的元素组成。化合价有正负，化合物中正负化合价代数和为零。根据化合价可书写化学式，根据化学式可推化合价。读、写、义（意义）是化学式学习三关。",
        "方法：代数和为零写式",
        "先排元素顺序，再交叉约简化合价绝对值写角标。单质化合价为零。",
        "Al 为+3，O 为−2，化学式 Al₂O₃。",
        "化合物中各元素化合价的代数和为？",
        ["+1", "−1", "0", "等于原子数"],
        2,
        "正负化合价代数和为零。",
        "常见误区是角标与化合价直接相等不交叉，或单质也标化合价。",
    ),
    "chem-m-chemical-equation": C(
        "化学方程式",
        "化学方程式用化学式表示化学反应，必须遵循质量守恒定律，配平后各原子种类与数目左右相等。写清反应物、生成物、反应条件与气体沉淀符号。会读含义：质、量、配比。",
        "方法：写式→配平→条件符号",
        "先写正确化学式，再配平，最后注明条件与↑↓。不要改角标来配平。",
        "2H₂+O₂=点燃=2H₂O，说明 2 个氢分子与 1 个氧分子反应生成 2 个水分子。",
        "配平化学方程式时不可改动的是？",
        ["计量数", "化学式中的角标", "条件", "箭头符号"],
        1,
        "角标由化学式决定，只能改计量数。",
        "常见误区是用改角标配平，或漏写条件与气体沉淀号。",
    ),
    "chem-m-mass-conservation": C(
        "质量守恒定律",
        "参加化学反应的各物质质量总和等于反应后生成各物质质量总和。微观原因是反应前后原子种类、数目、质量不变，只是重新组合。可用于推未知物质量、判断能否发生等。",
        "方法：称量思路 + 原子不变",
        "计算时找“反应前后质量差”，注意有气体逸出或进入时装置是否密闭。",
        "镁条在空气中燃烧增重，是因为结合了氧气，不是违背守恒。",
        "质量守恒的微观本质是？",
        ["分子种类不变", "原子种类和数目不变", "物质体积不变", "颜色不变"],
        1,
        "原子重新组合，种类数目质量不变。",
        "常见误区是把体积、分子个数也当成一定守恒。",
    ),
    "chem-m-equation-calculation": C(
        "根据化学方程式计算",
        "根据化学方程式计算是初中化学重要技能：设未知量、列比例、求解、写单位与答。比例来自化学计量数与相对分子质量。注意纯净度、单位统一与过量问题入门。",
        "方法：设—列—算—答",
        "写正确方程式并配平；找出已知与未知质量；按质量比列式。检查有效数字与单位。",
        "若 2Mg+O₂=2MgO，每 48 份质量镁约消耗 32 份质量氧气（用相对原子质量估算）。",
        "化学方程式计算的依据是？",
        ["体积守恒", "质量守恒与计量数关系", "颜色变化", "温度高低"],
        1,
        "质量关系由计量数与式量决定。",
        "常见误区是未配平就计算，或把角标当成计量数。",
    ),
    "chem-m-reaction-types": C(
        "化学反应基本类型",
        "初中常见四种基本反应类型：化合、分解、置换、复分解。化合多变一，分解一变多，置换单质与化合物反应生成新单质新化合物，复分解两种化合物交换成分。氧化还原初步可用得失氧来认识。",
        "方法：看反应物生成物类别",
        "先数物质种类变化，再看有无单质参与。同一反应一般归属一种基本类型。",
        "Fe+CuSO₄=FeSO₄+Cu 是置换；HCl+NaOH=NaCl+H₂O 是复分解（中和）。",
        "一种物质生成两种或多种物质的反应属于？",
        ["化合反应", "分解反应", "置换反应", "复分解反应"],
        1,
        "一变多是分解反应。",
        "常见误区是用现象分类，或把所有有单质生成的反应都叫置换。",
    ),
    "chem-m-catalyst-concept": C(
        "催化剂与催化作用",
        "催化剂能改变反应速率，而本身的质量和化学性质在反应前后不变。催化作用具有选择性。二氧化锰催化过氧化氢分解是典型例子。催化剂不等于反应物，也不等于永远“越多越好”而不考虑实际。",
        "方法：变速率、质与性不变",
        "判断催化剂看反应前后质量和化学性质。加快或减慢都属催化范畴（初中多讲加快）。",
        "H₂O₂ 分解加 MnO₂ 更快产生氧气，MnO₂ 质量反应前后不变。",
        "催化剂在化学反应前后？",
        ["质量一定减少", "质量和化学性质不变", "一定变成生成物", "体积必须不变"],
        1,
        "质量和化学性质不变，但可改变化学反应速率。",
        "常见误区是认为催化剂会“消耗完”，或把加热也当成催化剂。",
    ),
    "chem-m-solution-concept": C(
        "溶液的形成",
        "溶液由溶质和溶剂组成，具有均一、稳定的特征。水是常见溶剂。溶解过程常伴随吸热或放热、体积变化。乳化与溶解不同：乳浊液不稳定可分层，乳化剂帮助乳浊液更稳定。",
        "方法：溶质溶剂 + 均一稳定",
        "指认溶质溶剂；区分溶液、悬浊液、乳浊液。溶解与融化字义不同。",
        "蔗糖水中蔗糖是溶质，水是溶剂；碘酒中碘是溶质，酒精是溶剂。",
        "溶液的基本特征是？",
        ["一定有颜色", "均一、稳定", "一定是混合物中最重的", "一定导电"],
        1,
        "溶液外观均一且长期稳定不分层。",
        "常见误区是认为溶液一定无色，或把乳浊液当成溶液。",
    ),
    "chem-m-solubility": C(
        "溶解度",
        "溶解度表示一定温度下饱和溶液中溶质的溶解能力，通常指 100 g 溶剂中达到饱和所溶解溶质的质量。溶解度曲线可比较物质溶解性、判断降温结晶等。饱和与不饱和是相对状态。",
        "方法：读曲线抓温度",
        "曲线上升表示溶解度随温度增大为主；交叉点溶解度相等。结晶方法：降温或蒸发溶剂。",
        "KNO₃ 溶解度随温度升高明显增大，适合降温结晶提纯。",
        "溶解度的常用表示对应溶剂质量是？",
        ["1 g", "10 g", "100 g", "1000 g"],
        2,
        "通常指 100 g 溶剂中溶解的溶质质量。",
        "常见误区是离开温度谈溶解度，或把饱和溶液当成浓溶液的同义词。",
    ),
    "chem-m-solution-concentration": C(
        "溶液浓度（质量分数）",
        "溶质质量分数=溶质质量/溶液质量×100%。溶液质量=溶质质量+溶剂质量。稀释前后溶质质量不变。会进行配制计算与基本操作（计算、称量、溶解、装瓶贴标签）。",
        "方法：抓住溶质质量不变",
        "稀释：m浓×w浓=m稀×w稀。配制时先算固体与水的质量。",
        "50 g 10% 的溶液含溶质 5 g；稀释到 5% 需溶液总质量 100 g，加水 50 g。",
        "溶质质量分数的公式是？",
        ["溶质/溶剂", "溶质/溶液×100%", "溶剂/溶液", "溶液/溶质"],
        1,
        "质量分数=溶质质量与溶液质量之比。",
        "常见误区是用溶剂质量当分母，或稀释时溶质质量也按比例减少。",
    ),
    "chem-m-acid-base-concept": C(
        "酸和碱",
        "酸在水溶液中解离出的阳离子全部是氢离子；碱解离出的阴离子全部是氢氧根离子。酸有酸性，能使紫色石蕊变红；碱有碱性，能使石蕊变蓝、酚酞变红。常见酸：盐酸、硫酸；常见碱：氢氧化钠、氢氧化钙。",
        "方法：定义—通性—代表物",
        "先背定义抓离子，再记通性与指示剂现象，最后记用途与腐蚀性安全。",
        "盐酸能与碱、某些金属氧化物、某些盐反应，体现酸的通性。",
        "酸的通性来源于溶液中的？",
        ["氧离子", "氢离子", "钠离子", "氯离子一定"],
        1,
        "酸溶液中阳离子全部是 H⁺。",
        "常见误区是看见含氧就叫酸，或把碱与碱性氧化物混淆。",
    ),
    "chem-m-ph-indicators": C(
        "酸碱指示剂与 pH",
        "指示剂可大致判断酸碱性：石蕊、酚酞是常用指示剂。pH 表示酸碱度强弱：pH=7 中性，小于 7 酸性，大于 7 碱性；数值相差 1，酸碱性强弱相差 10 倍（初中定性理解即可）。测定用 pH 试纸等。",
        "方法：指示剂现象 + pH 区间",
        "先看变色判断酸碱，再用 pH 比较强弱。试纸不能直接浸入瓶中试剂。",
        "盐酸使石蕊变红；氢氧化钠使酚酞变红。",
        "pH=5 的溶液显？",
        ["碱性", "酸性", "中性", "无法判断"],
        1,
        "pH＜7 显酸性。",
        "常见误区是 pH 越大酸性越强，或指示剂与 pH 试纸用法不分。",
    ),
    "chem-m-neutralization": C(
        "中和反应",
        "酸与碱作用生成盐和水的反应叫中和反应，属于复分解。生活中用熟石灰改良酸性土壤、用含碱药物治疗胃酸过多等，都是中和应用。中和过程可用指示剂指示终点。",
        "方法：酸+碱→盐+水",
        "写方程式注意盐的组成来自酸碱对应部分。联系实际改土、医药、处理废水。",
        "HCl+NaOH=NaCl+H₂O 是典型中和反应。",
        "中和反应的生成物是？",
        ["只有盐", "盐和水", "只有水", "氧气和盐"],
        1,
        "中和生成盐和水。",
        "常见误区是把所有复分解都叫中和，或忽略中和放热等实际现象。",
    ),
    "chem-m-acid-base-salt": C(
        "酸碱盐综合",
        "酸、碱、盐在溶液中的反应常遵循复分解发生条件：生成沉淀、气体或水。要熟练常见酸碱盐的溶解性、颜色与基本反应规律，形成“谁和谁能反应”的网络。",
        "方法：溶解性表 + 反应条件",
        "先判断是否满足复分解条件，再写方程式。盐的性质常分与酸、碱、盐相互反应几类。",
        "Na₂CO₃+2HCl=2NaCl+H₂O+CO₂↑，因生成气体而能发生。",
        "复分解反应发生的条件是生成？",
        ["单质", "沉淀、气体或水", "只有氧化物", "金属"],
        1,
        "生成沉淀、气体或水是重要条件。",
        "常见误区是不查溶解性就写沉淀，或酸碱盐通性记混。",
    ),
    "chem-m-salt-reactions": C(
        "盐的性质",
        "盐是由金属离子（或铵根）与酸根离子构成的化合物。盐可与某些酸、碱、盐反应，也可与较活泼金属发生置换。学习时结合溶解性表判断能否发生复分解，并关注实际用途（如碳酸盐、盐业）。",
        "方法：分类讨论反应对象",
        "见盐先想：溶不溶？能与谁反应？产物中有无沉淀气体水？",
        "CuSO₄+2NaOH=Cu(OH)₂↓+Na₂SO₄，生成蓝色沉淀。",
        "下列属于盐的是？",
        ["H₂SO₄", "NaOH", "Na₂CO₃", "CaO"],
        2,
        "碳酸钠由钠离子与碳酸根构成，属于盐。",
        "常见误区是把碱性氧化物当成碱，或盐一定是咸的（化学“盐”≠食盐唯一）。",
    ),
    "chem-m-metal-properties": C(
        "金属的物理与化学性质",
        "金属多数有金属光泽、导电导热、延展性；化学上可与氧气、酸、某些盐溶液反应。不同金属活动性不同，决定反应难易与冶炼、防腐方法。合金性能往往优于纯金属。",
        "方法：通性 + 活动性差异",
        "物理通性举用途；化学性质结合活动性顺序判断能否与酸、盐反应。",
        "铜可导电作导线；铝在空气中形成致密氧化膜抗腐蚀。",
        "金属共同的物理性质通常包括？",
        ["都是粉末", "导电、导热、有延展性（多数）", "都不与酸反应", "都无光泽"],
        1,
        "多数金属具有这些物理通性。",
        "常见误区是认为所有金属都能与酸反应放出氢气，或合金一定是化合物。",
    ),
    "chem-m-activity-series": C(
        "金属活动性顺序",
        "金属活动性顺序可判断：能否与酸反应放氢、能否从盐溶液中置换出另一种金属、冶炼难易等。位于前面的金属一般更能把后面的金属从其盐溶液中置换出来。记忆顺序并会应用是关键。",
        "方法：题型对应三条应用",
        "见“酸中放氢”“盐溶液置换”“谁先腐蚀”等，都回到活动性顺序。",
        "Fe 能置换 CuSO₄ 中的 Cu，说明 Fe 比 Cu 活泼。",
        "能否用金属活动性顺序判断？",
        ["金属颜色", "一种金属能否从另一种金属盐溶液中置换出该金属", "金属密度精确值", "熔点绝对大小"],
        1,
        "置换反应能否发生可用活动性顺序判断。",
        "常见误区是顺序背错，或把“活动性强”理解成“一定与所有物质都反应”。",
    ),
    "chem-m-metals-activity": C(
        "金属的活动性",
        "金属活动性强弱体现在与氧气、酸、水、盐溶液反应的难易与剧烈程度。实验比较活动性常观察反应是否发生与剧烈程度。活动性差异解释了为什么有的金属适合作导线外壳、有的需特殊保存。",
        "方法：实验现象比较强弱",
        "控制酸浓度、温度等变量，比较气泡快慢或能否置换。结论用活动性顺序检验。",
        "钾、钙、钠很活泼，与水反应剧烈；金、银很难与酸反应放氢。",
        "比较金属活动性的常用方法是？",
        ["只看颜色", "与酸或盐溶液反应并观察现象", "只称质量", "只看价格"],
        1,
        "通过反应事实比较活动性。",
        "常见误区是不控制变量就比较，或把生锈快慢简单等同于活动性全部内涵。",
    ),
    "chem-m-metal-corrosion": C(
        "金属的锈蚀与防护",
        "铁生锈需要氧气和水共同作用，实质是与空气中氧气、水等发生化学反应。防护：保持干燥、涂油喷漆、镀层、制成合金等。从条件入手，破坏锈蚀条件即可防护。",
        "方法：找条件→破条件",
        "实验对比“干燥/潮湿/隔绝空气”等，得出铁生锈条件，再对应防护措施。",
        "自行车链条涂油防锈；轮船牺牲锌块保护钢铁。",
        "铁生锈的主要条件是？",
        ["只与氮气接触", "与氧气和水同时接触", "必须在真空", "只能在油中"],
        1,
        "氧气和水是铁生锈的重要条件。",
        "常见误区是以为生锈只是物理变化，或防护只靠一种方法万能。",
    ),
    "chem-m-metal-smelting": C(
        "金属冶炼",
        "冶炼是把金属从矿石中还原出来。活动性不同，冶炼方法不同：热分解、热还原（如一氧化碳还原氧化铁）、电解等。初中重点理解还原思想与炼铁主要反应，关注资源与环境。",
        "方法：矿石→还原→提纯思路",
        "写出主要还原反应，说明还原剂作用。联系高炉炼铁原料：铁矿石、焦炭、石灰石。",
        "Fe₂O₃+3CO=高温=2Fe+3CO₂，一氧化碳表现还原性。",
        "从铁矿石炼铁的主要化学过程是？",
        ["金属化合变矿石", "铁的化合物被还原为铁", "铁变成合金只能物理混合", "铁蒸发收集"],
        1,
        "冶炼核心是还原得到金属单质。",
        "常见误区是把焦炭只当燃料，忽视其生成还原性气体的作用。",
    ),
}


STYLE = """
<style id="chemm-depth-css">
.chemm-depth .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand,#38bdf8);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.chemm-depth .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(251,146,60,.08);border:1px solid rgba(251,146,60,.28)}
.chemm-depth .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line,#233);border-radius:10px;background:#0b1628;color:var(--text,#e5e7eb);padding:11px 13px;cursor:pointer}
.chemm-depth .module-check button.correct{border-color:var(--ok,#22c55e);background:rgba(34,197,94,.14)}
.chemm-depth .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.chemm-depth .chemm-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.chemm-depth .chemm-pitfall{margin:14px 0 0;padding:12px;border-radius:10px;background:rgba(248,180,0,.08);border:1px solid rgba(248,180,0,.24)}
</style>
"""

CHECK_SCRIPT = """
<script id="chemm-depth-js">
function chemmDepthCheck(button, isCorrect, feedbackId, explanation) {
  var box = button.closest('.module-check');
  if (!box || box.dataset.answered) return;
  box.dataset.answered = '1';
  box.querySelectorAll('button').forEach(function (item) {
    item.disabled = true;
    if (item.dataset.correct === '1') item.classList.add('correct');
  });
  if (!isCorrect) button.classList.add('wrong');
  var feedback = document.getElementById(feedbackId);
  if (feedback) {
    feedback.style.display = 'block';
    feedback.textContent = (isCorrect ? '正确。' : '再想想。') + explanation;
  }
}
</script>
"""


def build_block(cfg: dict) -> str:
    feedback_id = "chemm-depth-feedback"
    options = []
    for idx, opt in enumerate(cfg["options"]):
        correct = idx == cfg["correct"]
        handler = "chemmDepthCheck(this,{c},'{f}',{e})".format(
            c="true" if correct else "false",
            f=feedback_id,
            e=json.dumps(cfg["feedback"], ensure_ascii=False),
        )
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{h}">{letter}. {opt}</button>'.format(
                flag="1" if correct else "0",
                h=html.escape(handler, quote=True),
                letter=chr(65 + idx),
                opt=html.escape(opt),
            )
        )
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="精讲">
  <section class="section chemm-depth core-knowledge-module text-module" id="lesson-focus"
    data-bloom-level="understand" data-scaffold="full" data-tts="lesson-focus">
    <div class="card">
      <span class="phase-tag">知识精讲</span>
      <h2>{html.escape(cfg['concept_title'])}</h2>
      <p>{html.escape(cfg['concept_body'])}</p>
    </div>
  </section>
</section>
<section class="slide-page" data-page-type="content" data-tsh="方法范例">
  <section class="section chemm-depth core-knowledge-module text-module" id="lesson-method"
    data-bloom-level="apply" data-scaffold="partial" data-tts="lesson-method">
    <div class="card">
      <span class="phase-tag">方法与范例</span>
      <h2>{html.escape(cfg['method_title'])}</h2>
      <p>{html.escape(cfg['method_body'])}</p>
      <div class="worked-example"><strong>范例：</strong>{html.escape(cfg['example'])}</div>
      <p id="lesson-pitfall" class="chemm-pitfall"><strong>常见误区：</strong>{html.escape(cfg['pitfall'])}</p>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：辨析要点</h3>
        <p>{html.escape(cfg['question'])}</p>
        {''.join(options)}
        <div class="chemm-feedback" id="{feedback_id}" role="status"></div>
      </div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, cfg: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    if not path.exists():
        return False, "missing index.html"
    source = path.read_text(encoding="utf-8")
    if 'id="lesson-focus"' in source:
        return False, "already upgraded"
    dpos = -1
    for anchor in ('id="deep-understanding"', 'id="transfer-task"', 'id="posttest"', 'id="summary"'):
        dpos = source.find(anchor)
        if dpos >= 0:
            break
    if dpos < 0:
        return False, "insert anchor not found"
    marker = source.rfind('<section class="slide-page"', 0, dpos)
    insert_at = marker if marker >= 0 else source.rfind("<section", 0, dpos)
    if insert_at < 0:
        return False, "insert marker not found"
    source = source[:insert_at] + build_block(cfg) + "\n" + source[insert_at:]
    if 'id="chemm-depth-css"' not in source:
        source = source.replace("</head>", STYLE + "\n</head>", 1)
    if 'id="chemm-depth-js"' not in source:
        source = source.replace("</body>", CHECK_SCRIPT + "\n</body>", 1)
    source = re.sub(r"[ \t]+\n", "\n", source)
    path.write_text(source, encoding="utf-8")
    manifest_path = path.parent / "manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        changed = False
        for key, value in {"version": COURSE_VERSION, "updated_at": UPDATED_AT}.items():
            if manifest.get(key) != value:
                manifest[key] = value
                changed = True
        if changed:
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
    return True, "2 depth modules + metadata"


def main() -> int:
    changed = failed = 0
    for course_id, cfg in COURSES.items():
        ok, msg = upgrade(course_id, cfg)
        if ok:
            changed += 1
            print(f"OK {course_id}: {msg}")
        elif msg == "already upgraded":
            print(f"SKIP {course_id}: {msg}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {msg}")
    print(f"done: changed={changed} failed={failed} of {len(COURSES)}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
