#!/usr/bin/env python3
"""Add substantive core modules to the first P0 physics/chemistry batch.

The selected v7.14 pages already contain the platform shell, assessments,
audio, KG and a lightweight lab. Their teaching gate fails because they do not
have three explicit, readable core knowledge modules. This script inserts
topic-specific modules before Five Lens and adds one mature simulation.

Idempotent: courses already containing id="module-1" are skipped.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_VERSION = "1.1.0"
UPDATED_AT = "2026-08-09"


COURSES = {
    "phy-h-common-forces": {
        "modules": [
            {
                "title": "先隔离研究对象，再寻找力的施力者",
                "body": (
                    "受力分析不是把熟悉的力名全写上，而是先确定研究对象，再逐个寻找与它发生相互作用的物体。"
                    "重力的施力者是地球；支持力、拉力和摩擦力都来自接触物。若找不到施力者，这个力通常就是凭空添加的。"
                    "画图时把力的作用点等效画在物体重心，箭头方向表示力的方向，箭头旁写清符号。"
                ),
                "example": "一本书静放在水平桌面上：研究书，只受竖直向下的重力 G 和桌面竖直向上的支持力 N；“书对桌面的压力”不属于书受到的力。",
                "question": "分析斜面上木块受到的力，第一步最合理的是？",
                "options": ["先写出 mg、N、f 三个力", "隔离木块并列出与它相互作用的物体", "先把重力分解", "先判断木块是否加速"],
                "correct": 1,
                "feedback": "先隔离对象、找施力者，之后才能判断具体有哪些力；不能预设一定有摩擦力。",
            },
            {
                "title": "接触力要看形变与相对运动趋势",
                "body": (
                    "支持力和弹力的共同根源是接触处发生形变，方向通常垂直于接触面或沿绳、弹簧恢复形变的方向。"
                    "摩擦力则要求接触面粗糙且存在相对运动或相对运动趋势。静摩擦力会在零到最大值之间自适应，"
                    "并不总等于 μN；只有滑动摩擦力在给定模型中常写成 f=μN。"
                ),
                "example": "水平推箱子但箱子未动时，静摩擦力与推力等大反向；继续增大推力直到箱子滑动，摩擦力才转为近似恒定的滑动摩擦力。",
                "question": "箱子在 6 N 水平推力下仍静止，若最大静摩擦力为 10 N，此时摩擦力多大？",
                "options": ["0 N", "4 N", "6 N", "10 N"],
                "correct": 2,
                "feedback": "静止意味着水平方向合力为零，静摩擦力自适应为 6 N，而不是直接取最大值 10 N。",
            },
            {
                "title": "受力图到动力学方程：方向与坐标轴统一",
                "body": (
                    "受力图完成后，要选择便于列式的坐标轴。斜面问题通常沿斜面和垂直斜面建轴，"
                    "把重力分解成 mg·sinθ 与 mg·cosθ；不要把一个力及其分力同时写入合力式。"
                    "随后分别列 ΣFx=max、ΣFy=may，并用运动状态检查结果方向是否合理。"
                ),
                "example": "光滑斜面上的物体沿斜面加速度 a=g·sinθ；垂直斜面方向没有运动，故 N=mg·cosθ。θ 增大时 a 增大而 N 减小。",
                "question": "重力已沿斜面分解后，合力式中还应再写 mg 吗？",
                "options": ["应写，重力始终存在", "不应写，否则重复计算同一个力", "只在加速时写", "只在静止时写"],
                "correct": 1,
                "feedback": "分力是原力在坐标轴上的等效表示，原力和分力不能在同一方程里重复计入。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/forces-and-motion-basics/latest/forces-and-motion-basics_zh_CN.html",
        "sim_prompt": "在“摩擦”场景中逐步增大推力，记录静止、将要滑动、滑动三个阶段的摩擦力，并用受力图解释变化。",
    },
    "phy-h-free-fall": {
        "modules": [
            {
                "title": "自由落体是理想模型，不是“向下运动”的同义词",
                "body": (
                    "自由落体要求物体初速度为零，并且下落过程中只受重力。忽略空气阻力后，不同质量物体的加速度都等于当地重力加速度 g。"
                    "纸片和铁球在空气中下落差异明显，是空气阻力相对重力的影响不同；在真空中它们同时落地。"
                ),
                "example": "松手释放的小钢球可近似自由落体；竖直向下抛出的球初速度不为零，属于竖直下抛，不满足自由落体定义。",
                "question": "下列哪种运动可近似看作自由落体？",
                "options": ["雨滴从云层落下", "真空管中由静止释放的小球", "向下投出的篮球", "张开降落伞后的运动员"],
                "correct": 1,
                "feedback": "自由落体同时要求初速度为零且只受重力，真空管中的释放小球最符合模型条件。",
            },
            {
                "title": "三组公式来自同一个匀加速模型",
                "body": (
                    "取竖直向下为正方向，自由落体满足 v=gt、h=½gt²、v²=2gh。三式并非互不相关的口诀："
                    "速度每秒增加约 g，位移是速度—时间图像下的面积。选式时先圈出已知量和未知量，"
                    "再选不含多余未知量的关系式，能显著减少代数错误。"
                ),
                "example": "物体下落 2 s，取 g=10 m/s²，则末速度 20 m/s，下落高度 20 m；第二个 1 s 内位移为 15 m，不是 10 m。",
                "question": "物体自由下落 3 s，取 g=10 m/s²，下落高度是多少？",
                "options": ["15 m", "30 m", "45 m", "90 m"],
                "correct": 2,
                "feedback": "h=½gt²=0.5×10×9=45 m；位移与时间平方成正比。",
            },
            {
                "title": "用图像和逐差法检验重力加速度",
                "body": (
                    "自由落体的 v-t 图像是过原点、斜率为 g 的直线；h-t 图像是开口向上的抛物线。"
                    "实验中用光电门或频闪照片取得等时间间隔位置，可由相邻位移差 Δx=gT² 求 g。"
                    "若数据点明显偏离直线，应检查释放初速度、计时延迟和空气阻力，而不是直接删掉异常点。"
                ),
                "example": "频闪周期 T=0.10 s，相邻两段位移差约 0.098 m，则 g≈0.098/0.01=9.8 m/s²。",
                "question": "自由落体 v-t 图像的斜率代表什么？",
                "options": ["下落高度", "重力加速度", "平均速度", "物体质量"],
                "correct": 1,
                "feedback": "速度—时间图像的斜率就是加速度，自由落体中该斜率为 g。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/projectile-motion/latest/projectile-motion_zh_CN.html",
        "sim_prompt": "把发射角调到 90°、空气阻力关闭，比较不同质量物体的运动；再打开空气阻力，说明模型条件为什么重要。",
    },
    "phy-h-coulomb-law": {
        "modules": [
            {
                "title": "库仑定律先检查点电荷与介质条件",
                "body": (
                    "真空中两个静止点电荷之间的作用力大小 F=k|q₁q₂|/r²，方向沿两电荷连线。"
                    "“点电荷”是相对尺度模型：带电体尺寸远小于它们间距时才可忽略形状。"
                    "距离 r 指两个电荷中心间距，单位必须换成米，电荷量用库仑。"
                ),
                "example": "两同号电荷相距变为原来的 2 倍，电荷量不变，库仑力变为原来的 1/4，方向仍相互排斥。",
                "question": "两点电荷间距离变为原来的 3 倍，作用力变为？",
                "options": ["3 倍", "1/3", "9 倍", "1/9"],
                "correct": 3,
                "feedback": "库仑力与距离平方成反比，距离乘 3，力除以 3²=9。",
            },
            {
                "title": "多个电荷的作用力必须做矢量叠加",
                "body": (
                    "库仑力满足独立作用原理：某电荷受到的总力，等于其余各电荷分别产生的库仑力的矢量和。"
                    "先逐对判断吸引或排斥并画箭头，再按选定坐标轴分解。"
                    "同一直线上可以带正负号代数相加，平面问题则要分别求 Fx、Fy 后合成。"
                ),
                "example": "等量同号电荷位于 x=±a，在原点放试探正电荷，两侧作用力等大反向，总力为零；但原点处平衡并不一定稳定。",
                "question": "三个电荷问题中，可否把三个库仑力大小直接相加？",
                "options": ["总可以", "只有各力同向时可以", "只要电荷同号就可以", "只要距离相等就可以"],
                "correct": 1,
                "feedback": "力是矢量，只有方向相同才可直接相加大小；否则必须先分方向。",
            },
            {
                "title": "从库仑力过渡到电场：分清施力者与场",
                "body": (
                    "库仑定律描述两个具体电荷的相互作用；电场强度 E=F/q 则描述空间某点的场性质。"
                    "点电荷产生的场 E=k|Q|/r²，方向由场源电荷 Q 决定，与试探电荷 q 的正负无关。"
                    "试探负电荷受到的力方向与 E 相反，这是最常见的方向混淆。"
                ),
                "example": "正点电荷周围电场向外；把正试探电荷换成负试探电荷，电场方向不变，但电场力反向。",
                "question": "换用电荷量更小的正试探电荷测同一点，测得 E 会怎样？",
                "options": ["变小", "变大", "不变", "方向反向"],
                "correct": 2,
                "feedback": "E 是场源和位置的性质，F 与 q 同比例变化，所以 F/q 不变。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/coulombs-law/latest/coulombs-law_zh_CN.html",
        "sim_prompt": "固定电荷量，把距离依次设为 1、2、3 个单位，记录力并检验 1/r²；再改电荷正负，观察方向变化。",
    },
    "phy-h-collision-types": {
        "modules": [
            {
                "title": "先选系统，再判断动量是否近似守恒",
                "body": (
                    "碰撞时间很短，若系统所受外力冲量远小于内力冲量，可近似认为总动量守恒。"
                    "写式前必须说明系统包含哪些物体，并规定正方向；速度是有符号的，反向运动要取负。"
                    "动量守恒不意味着每个物体动量不变，而是系统总动量在碰撞前后相等。"
                ),
                "example": "光滑水平面上 m₁ 以 v₁ 撞向静止的 m₂：m₁v₁=m₁v₁′+m₂v₂′。若地面摩擦冲量可忽略，该式成立。",
                "question": "两冰壶碰撞时把两个冰壶作为系统，动量近似守恒的关键是？",
                "options": ["两冰壶质量相等", "碰撞时间短且外力冲量可忽略", "碰撞后速度相等", "动能一定守恒"],
                "correct": 1,
                "feedback": "系统总动量守恒取决于外力冲量，而不是质量是否相等或动能是否守恒。",
            },
            {
                "title": "用动能损失区分弹性、非弹性和完全非弹性",
                "body": (
                    "所有满足条件的碰撞都可用动量守恒，但机械能不一定守恒。弹性碰撞的碰撞前后总动能相等；"
                    "非弹性碰撞有一部分动能转化为内能、声能或形变能；完全非弹性碰撞后两物体粘在一起，"
                    "动能损失在给定初态下最大。"
                ),
                "example": "两等质量小球一动一静发生正碰：理想弹性碰撞后交换速度；若粘在一起，则共同速度为初速度的一半。",
                "question": "完全非弹性碰撞最显著的末态特征是？",
                "options": ["总动能守恒", "两物体交换速度", "两物体具有共同速度", "总动量为零"],
                "correct": 2,
                "feedback": "完全非弹性碰撞后物体粘连、共同运动；总动量仍可守恒，但总动能减少。",
            },
            {
                "title": "恢复系数把“弹不弹”变成可测量指标",
                "body": (
                    "一维碰撞的恢复系数 e=分离相对速度/接近相对速度，取值通常在 0 到 1。"
                    "e=1 对应完全弹性碰撞，e=0 对应完全非弹性碰撞。"
                    "实验中同时使用动量守恒式和恢复系数式，可求两物体末速度，并用总动能变化检查答案。"
                ),
                "example": "球落地前速度大小为 v，反弹速度大小为 v′，地面近似不动时 e=v′/v；由高度可得 e≈√(h反弹/h下落)。",
                "question": "某球从 1.0 m 高处落下，反弹到 0.64 m，近似恢复系数为？",
                "options": ["0.36", "0.64", "0.80", "1.25"],
                "correct": 2,
                "feedback": "速度与高度平方根成正比，e=√(0.64/1.0)=0.80。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/collision-lab/latest/collision-lab_zh_CN.html",
        "sim_prompt": "分别设置弹性与完全非弹性碰撞，记录碰撞前后总动量、总动能；指出哪一个量总保持、哪一个量取决于碰撞类型。",
    },
    "chem-h-atom-structure-h": {
        "modules": [
            {
                "title": "用 Z、A 统一表示原子的身份与质量",
                "body": (
                    "原子序数 Z 等于质子数，也等于原子核的核电荷数，决定元素身份。质量数 A 等于质子数与中子数之和，"
                    "所以中子数 N=A−Z。中性原子的电子数等于 Z；形成离子后，质子数不变，只是得失电子。"
                    "做题时先写“身份看 Z、质量看 A、离子看电子变化”。"
                ),
                "example": "²³₁₁Na 含 11 个质子、12 个中子、11 个电子；Na⁺ 仍有 11 个质子，但失去 1 个电子，电子数为 10。",
                "question": "³⁵₁₇Cl⁻ 中电子数是多少？",
                "options": ["16", "17", "18", "35"],
                "correct": 2,
                "feedback": "氯的 Z=17，中性时 17 个电子；Cl⁻ 多得到 1 个电子，所以有 18 个。",
            },
            {
                "title": "同位素：元素相同，核内中子数不同",
                "body": (
                    "同位素是质子数相同、中子数不同的同一元素原子，因此化学性质通常相近，但质量和部分核性质不同。"
                    "元素的相对原子质量是天然同位素按丰度计算的加权平均，不等于某一种同位素的质量数。"
                    "解丰度题时要用“丰度×同位素相对质量”求和。"
                ),
                "example": "氯主要含 ³⁵Cl 和 ³⁷Cl，平均相对原子质量约 35.5，说明 ³⁵Cl 丰度更高，而不是存在质量数 35.5 的单个原子。",
                "question": "互为同位素的两种原子一定相同的是？",
                "options": ["中子数", "质量数", "质子数", "物理性质"],
                "correct": 2,
                "feedback": "同位素属于同一元素，所以质子数相同；中子数和质量数不同。",
            },
            {
                "title": "电子排布连接原子结构与元素性质",
                "body": (
                    "基态电子按能量由低到高排布，并遵循泡利原理和洪特规则。高中入门阶段最重要的是最外层电子数："
                    "主族元素的价电子决定常见成键数、化合价与得失电子趋势。"
                    "周期表中的周期数对应电子层数，主族序数与最外层电子数相关，由此可预测元素性质的周期性。"
                ),
                "example": "Na 的排布可简写为 2、8、1，易失去 1 个电子形成 Na⁺；Cl 为 2、8、7，易得到 1 个电子形成 Cl⁻。",
                "question": "某主族原子电子层排布为 2、8、2，它最可能？",
                "options": ["得到 2 个电子", "失去 2 个电子", "形成 −1 价离子", "属于稀有气体"],
                "correct": 1,
                "feedback": "最外层 2 个电子，通常失去 2 个达到稳定结构，形成 +2 价离子。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/build-an-atom/latest/build-an-atom_zh_CN.html",
        "sim_prompt": "固定质子数，分别改变中子数和电子数：观察元素名称、质量数、电荷各由什么决定，并整理成三列表。",
    },
    "chem-h-mole-concept": {
        "modules": [
            {
                "title": "物质的量是连接微观粒子与宏观计量的桥",
                "body": (
                    "物质的量 n 的单位是摩尔 mol，1 mol 任何指定粒子都含阿伏伽德罗常数 Nₐ≈6.02×10²³ 个粒子。"
                    "必须写清粒子种类：1 mol O 表示氧原子，1 mol O₂ 表示氧分子，两者包含的氧原子数不同。"
                    "粒子数换算遵循 N=nNₐ。"
                ),
                "example": "0.5 mol H₂O 含 0.5Nₐ 个水分子、Nₐ 个氢原子和 0.5Nₐ 个氧原子。",
                "question": "1 mol CO₂ 中氧原子的物质的量是多少？",
                "options": ["0.5 mol", "1 mol", "2 mol", "3 mol"],
                "correct": 2,
                "feedback": "每个 CO₂ 分子含 2 个氧原子，所以 1 mol CO₂ 含 2 mol 氧原子。",
            },
            {
                "title": "摩尔质量把质量换算成粒子数量",
                "body": (
                    "摩尔质量 M 的单位是 g·mol⁻¹，数值上等于该物质的相对分子质量或相对原子质量。"
                    "质量与物质的量关系为 n=m/M。"
                    "计算前先写单位并检查数量级：克除以克每摩尔得到摩尔；不能把摩尔质量写成没有单位的相对分子质量。"
                ),
                "example": "18 g H₂O 的摩尔质量为 18 g·mol⁻¹，因此 n=1 mol，含 Nₐ 个水分子。",
                "question": "11 g CO₂（M=44 g·mol⁻¹）的物质的量是？",
                "options": ["0.25 mol", "0.5 mol", "2 mol", "4 mol"],
                "correct": 0,
                "feedback": "n=m/M=11/44=0.25 mol。",
            },
            {
                "title": "同是 1 mol，体积关系要看状态与条件",
                "body": (
                    "固体、液体的摩尔体积取决于物质种类，不能直接套 22.4 L·mol⁻¹。"
                    "只有在标准状况下的理想气体，才常用 Vₘ≈22.4 L·mol⁻¹，并满足 n=V/Vₘ。"
                    "溶液则用物质的量浓度 c=n/V，体积必须以升计；稀释前后溶质物质的量不变。"
                ),
                "example": "标准状况下 11.2 L O₂ 约为 0.5 mol；但 11.2 L 液态水绝不能用 22.4 L·mol⁻¹ 换算。",
                "question": "100 mL 1.0 mol/L NaCl 溶液含 NaCl 多少 mol？",
                "options": ["0.01", "0.10", "1.0", "100"],
                "correct": 1,
                "feedback": "V=0.100 L，n=cV=1.0×0.100=0.10 mol。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/molarity/latest/molarity_zh_CN.html",
        "sim_prompt": "改变溶质物质的量和溶液体积，记录浓度；找出两种不同操作却得到相同浓度的方案。",
    },
    "chem-h-chemical-bond": {
        "modules": [
            {
                "title": "离子键与共价键的本质都是静电作用",
                "body": (
                    "离子键是阴、阳离子之间的静电作用，共价键是原子间通过共享电子对形成的强相互作用。"
                    "判断成键类型不能只背“金属+非金属”，还要看实际微粒与结构；含原子团的盐既有离子作用，"
                    "原子团内部又存在共价键。"
                ),
                "example": "NaCl 晶体由 Na⁺、Cl⁻ 构成，主要是离子键；NH₄Cl 中 NH₄⁺ 与 Cl⁻ 间是离子作用，而 N—H 为共价键。",
                "question": "下列物质中既含离子作用又含共价键的是？",
                "options": ["NaCl", "H₂", "NH₄Cl", "金刚石"],
                "correct": 2,
                "feedback": "NH₄⁺ 与 Cl⁻ 间为离子作用，NH₄⁺ 内部 N—H 是共价键。",
            },
            {
                "title": "键的极性不等于分子的极性",
                "body": (
                    "成键原子电负性不同会产生极性共价键，电子云偏向电负性较大的原子。"
                    "分子是否极性还取决于空间构型：各键偶极矩若因对称性抵消，分子可为非极性。"
                    "判断流程应是“先看键极性，再画结构，最后做矢量合成”。"
                ),
                "example": "CO₂ 的两个 C=O 键都有极性，但分子为直线形，两个键偶极矩等大反向，所以 CO₂ 分子整体非极性。",
                "question": "H₂O 含极性 O—H 键，且分子呈折线形，因此 H₂O 分子？",
                "options": ["非极性", "有极性", "一定带负电", "没有共价键"],
                "correct": 1,
                "feedback": "折线形使两个键偶极不能抵消，所以 H₂O 是极性分子。",
            },
            {
                "title": "结构决定性质：先分微粒，再解释熔点与导电",
                "body": (
                    "离子晶体熔点较高，固态离子不能自由移动而不导电，熔融或溶于水后可导电。"
                    "分子晶体熔沸点主要受分子间作用力影响；共价晶体中原子以强共价键形成空间网状结构，通常硬度大、熔点高。"
                    "解释性质时必须说清“克服的是哪种粒子间作用”。"
                ),
                "example": "熔化 NaCl 需要破坏晶格中的强静电作用；熔化冰主要克服水分子间氢键，不是把 O—H 共价键断开。",
                "question": "固态 NaCl 不导电的直接原因是？",
                "options": ["没有带电粒子", "离子被固定在晶格位置", "离子键消失", "电子数太少"],
                "correct": 1,
                "feedback": "NaCl 中有带电离子，但固态时离子不能自由移动，因而不能形成定向电流。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/molecule-shapes/latest/molecule-shapes_zh_CN.html",
        "sim_prompt": "搭建 CO₂、H₂O、NH₃，记录电子域数、空间构型和键偶极能否抵消，解释分子极性差异。",
    },
    "chem-h-reaction-rate": {
        "modules": [
            {
                "title": "反应速率描述单位时间内浓度怎样变化",
                "body": (
                    "化学反应速率常用单位时间内反应物浓度的减少量或生成物浓度的增加量表示：v=Δc/Δt。"
                    "同一反应用不同物质表示的速率数值可能不同，但比值等于化学计量数之比。"
                    "题目若问平均速率，必须使用给定时间段的浓度差，不能把某一时刻浓度直接除以时间。"
                ),
                "example": "2NO₂→2NO+O₂ 中，若 O₂ 生成速率为 0.10 mol·L⁻¹·s⁻¹，则 NO₂ 消耗速率为 0.20 mol·L⁻¹·s⁻¹。",
                "question": "N₂+3H₂→2NH₃ 中，v(H₂)=0.30 mol·L⁻¹·s⁻¹，则 v(NH₃)=？",
                "options": ["0.10", "0.20", "0.30", "0.60"],
                "correct": 1,
                "feedback": "速率比等于计量数比，v(H₂):v(NH₃)=3:2，所以 v(NH₃)=0.20。",
            },
            {
                "title": "碰撞理论解释浓度、温度、压强和催化剂",
                "body": (
                    "反应发生需要粒子有效碰撞，即碰撞能量足够且取向合适。增大浓度或气体压强提高单位体积碰撞次数；"
                    "升高温度既提高碰撞频率，更显著增加达到活化能的粒子比例。催化剂提供活化能更低的新路径，"
                    "但不改变反应热，也不改变平衡常数。"
                ),
                "example": "粉末状 CaCO₃ 与同质量块状 CaCO₃ 相比表面积更大，与酸接触机会更多，所以反应更快，但最终生成 CO₂ 总量相同。",
                "question": "催化剂加快反应的主要原因是？",
                "options": ["提高反应物浓度", "降低反应的焓变", "提供较低活化能路径", "增大生成物总量"],
                "correct": 2,
                "feedback": "催化剂改变反应路径、降低活化能；不改变反应热和平衡组成。",
            },
            {
                "title": "控制变量实验要区分速率与反应限度",
                "body": (
                    "研究某因素对速率的影响时，只改变一个自变量，其余条件保持一致，并选择可连续测量的因变量，"
                    "如气体体积、质量、吸光度或某物质浓度。比较曲线时，初始斜率反映初速率，平台高度反映最终产量。"
                    "“曲线更陡”说明更快；“平台更高”说明最终量更多，两者不能混为一谈。"
                ),
                "example": "两组相同量 CaCO₃ 与等体积酸反应，只改变酸浓度。高浓度组初始曲线更陡；若 CaCO₃ 都完全反应，最终 CO₂ 体积相同。",
                "question": "两条生成气体体积—时间曲线最终平台相同，但一条更早到平台，说明？",
                "options": ["反应更快但最终产量相同", "反应更慢且产量更少", "平衡常数增大", "反应物质量增加"],
                "correct": 0,
                "feedback": "更早到平台表示速率更快；平台相同表示最终生成量相同。",
            },
        ],
        "sim": "https://phet.colorado.edu/sims/html/concentration/latest/concentration_zh_CN.html",
        "sim_prompt": "先用模拟建立“改变溶质与体积会改变浓度”的定量认识，再设计实验检验浓度对反应初速率的影响。",
    },
}


STYLE = """
<style id="p0-core-upgrade-css">
.p0-module .concept-chain{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:16px}
.p0-module .concept-chain>div{padding:16px;border-radius:12px;background:rgba(56,189,248,.08);border:1px solid rgba(56,189,248,.2)}
.p0-module .worked-example{margin:16px 0;padding:16px;border-left:4px solid var(--brand);background:rgba(56,189,248,.08);border-radius:0 12px 12px 0}
.p0-module .module-check{margin-top:18px;padding:16px;border-radius:14px;background:rgba(167,139,250,.08);border:1px solid rgba(167,139,250,.24)}
.p0-module .module-check button{display:block;width:100%;margin:8px 0;text-align:left;border:1px solid var(--line);border-radius:10px;background:#0b1628;color:var(--text);padding:11px 13px;cursor:pointer}
.p0-module .module-check button.correct{border-color:var(--ok);background:rgba(34,197,94,.14)}
.p0-module .module-check button.wrong{border-color:#f87171;background:rgba(248,113,113,.12)}
.p0-feedback{display:none;margin-top:10px;padding:12px;border-radius:10px;background:rgba(56,189,248,.1)}
.p0-sim{position:relative;width:100%;padding-top:62.5%;overflow:hidden;border-radius:14px;background:#020617;border:1px solid var(--line);margin-top:16px}
.p0-sim iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
</style>
"""


CHECK_SCRIPT = """
<script id="p0-core-upgrade-js">
function p0Check(button, isCorrect, feedbackId, explanation) {
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
    feedback.textContent = (isCorrect ? '正确。' : '再检查模型。') + explanation;
  }
}
</script>
"""


def module_html(course_id: str, index: int, module: dict, sim: str | None, sim_prompt: str) -> str:
    feedback_id = f"p0-feedback-{index}"
    options = []
    for option_index, option in enumerate(module["options"]):
        correct = option_index == module["correct"]
        handler = "p0Check(this,{correct},'{feedback_id}',{feedback})".format(
            correct="true" if correct else "false",
            feedback_id=feedback_id,
            feedback=json.dumps(module["feedback"], ensure_ascii=False),
        )
        options.append(
            '<button type="button" data-correct="{flag}" onclick="{handler}">'
            "{letter}. {option}</button>".format(
                flag="1" if correct else "0",
                handler=html.escape(handler, quote=True),
                letter=chr(65 + option_index),
                option=html.escape(option),
            )
        )

    simulation = ""
    if sim:
        simulation = f"""
        <div class="worked-example">
          <strong>成熟仿真任务：</strong>{html.escape(sim_prompt)}
        </div>
        <div class="p0-sim">
          <iframe src="{html.escape(sim, quote=True)}" loading="lazy"
            title="{html.escape(module['title'], quote=True)}仿真实验"
            sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
            allowfullscreen></iframe>
        </div>
        """

    return f"""
<section class="slide-page" data-page-type="content" data-tsh="核心模块 {index}">
  <section class="section p0-module core-knowledge-module" id="module-{index}"
    data-bloom-level="{'understand' if index == 1 else 'apply' if index == 2 else 'analyze'}"
    data-scaffold="{'full' if index == 1 else 'partial'}">
    <div class="card">
      <span class="phase-tag">核心模块 {index}</span>
      <h2>{html.escape(module['title'])}</h2>
      <p>{html.escape(module['body'])}</p>
      <div class="worked-example"><strong>例题拆解：</strong>{html.escape(module['example'])}</div>
      <div class="module-check" data-conceptest="true">
        <h3>马上练：用模型判断</h3>
        <p>{html.escape(module['question'])}</p>
        {''.join(options)}
        <div class="p0-feedback" id="{feedback_id}" role="status"></div>
      </div>
      {simulation}
    </div>
  </section>
</section>
"""


def evidence_task_html(sim_prompt: str) -> str:
    return f"""
<section class="slide-page" data-page-type="content" data-tsh="证据链实验报告">
  <section class="section p0-module core-knowledge-module" id="module-practice"
    data-bloom-level="create" data-scaffold="partial">
    <div class="card">
      <span class="phase-tag">综合实践</span>
      <h2>证据链实验报告：从现象到模型</h2>
      <p><strong>本课任务：</strong>{html.escape(sim_prompt)}</p>
      <div class="concept-chain">
        <div><strong>1. 控制变量</strong><p>写清自变量、因变量和至少两个保持不变的条件，避免同时改变多个因素后无法归因。</p></div>
        <div><strong>2. 记录证据</strong><p>至少记录三组带单位的数据或三个可复查的现象，不用“变大了”“更明显”代替证据。</p></div>
        <div><strong>3. 建立解释</strong><p>用本课公式、粒子模型或受力关系解释趋势，并指出结论成立所依赖的模型条件。</p></div>
        <div><strong>4. 迁移检验</strong><p>换一个参数或真实情境预测结果，再用仿真检验；若不一致，回查变量、单位和边界条件。</p></div>
      </div>
      <div class="worked-example"><strong>达标标准：</strong>报告必须包含“预测—证据—解释—反思”四部分；结论不是复述现象，而要回答为什么会出现这个趋势。</div>
    </div>
  </section>
</section>
"""


def upgrade(course_id: str, config: dict) -> tuple[bool, str]:
    path = ROOT / "community" / course_id / "index.html"
    source = path.read_text(encoding="utf-8")
    original = source
    marker = '<section class="slide-page"'
    deep_pos = source.find(marker, source.find('id="deep-understanding"') - 300)
    if deep_pos < 0:
        return False, "deep-understanding slide marker not found"

    blocks = []
    if 'id="module-1"' not in source:
        for index, module in enumerate(config["modules"], 1):
            blocks.append(
                module_html(
                    course_id,
                    index,
                    module,
                    config["sim"] if index == 3 else None,
                    config["sim_prompt"],
                )
            )
    if 'id="module-practice"' not in source:
        blocks.append(evidence_task_html(config["sim_prompt"]))

    if blocks:
        if 'id="p0-core-upgrade-css"' not in source:
            source = source.replace("</head>", STYLE + "\n</head>", 1)
        source = source[:deep_pos] + "\n".join(blocks) + "\n" + source[deep_pos:]
        if 'id="p0-core-upgrade-js"' not in source:
            source = source.replace("</body>", CHECK_SCRIPT + "\n</body>", 1)

    source = re.sub(
        r'(<meta name="course-version" content=")[^"]+(">)',
        rf"\g<1>{COURSE_VERSION}\g<2>",
        source,
        count=1,
    )
    source = re.sub(
        r'(<span id="course-version-display">)[^<]+(</span>)',
        rf"\g<1>{COURSE_VERSION}\g<2>",
        source,
        count=1,
    )
    source = re.sub(r"[ \t]+\n", "\n", source)

    manifest_path = path.parent / "manifest.json"
    manifest_changed = False
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for key, value in {
            "version": COURSE_VERSION,
            "updated_at": UPDATED_AT,
            "duration": "40-50 min",
        }.items():
            if manifest.get(key) != value:
                manifest[key] = value
                manifest_changed = True
        if manifest_changed:
            manifest_path.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

    if source == original and not manifest_changed:
        return False, "already upgraded"
    if source != original:
        path.write_text(source, encoding="utf-8")
    return True, "3 modules + simulation + evidence task + metadata"


def main() -> int:
    changed = 0
    failed = 0
    for course_id, config in COURSES.items():
        ok, message = upgrade(course_id, config)
        if ok:
            changed += 1
            print(f"OK {course_id}: {message}")
        elif message == "already upgraded":
            print(f"SKIP {course_id}: {message}")
        else:
            failed += 1
            print(f"FAIL {course_id}: {message}")
    print(f"done: changed={changed} failed={failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
