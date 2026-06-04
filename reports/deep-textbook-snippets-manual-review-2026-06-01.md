# deep_textbook_snippets 人工相关性抽样审查

生成时间：2026-06-01 22:14:57

## 审查说明

- 抽样范围：数学、物理、生物、化学、历史，每学科 5 个中国课标节点。
- 审查对象：每个节点的 `supplements.deep_textbook_snippets` 是否与该知识点真实相关。
- 建议人工标记：`相关 / 部分相关 / 不相关`，并填写处理建议。
- 重点看三点：教材片段是否讲本知识点；是否只是目录/通用教学原则；是否可用于课件例题或讲解。
- 样本数量：数学 5 个；物理 5 个；生物 5 个；化学 5 个；历史 5 个。

## 审查判定标准

| 判定 | 标准 | 建议处理 |
|---|---|---|
| 相关 | 片段直接讲该知识点的定义、性质、公式、实验、例题、案例或史实 | 保留 |
| 部分相关 | 片段属于同一章节/大主题，但不够聚焦 | 可降级为参考资料，或替换更精准片段 |
| 不相关 | 片段只是目录、通用教学原则、错学科内容或无关段落 | 删除该 snippet，重新抽取 |

## 抽样清单

## 数学

### 1. 一次函数

- `node_id`：`math-m-linear-function`
- 文件：`data/kp/math/math-m-linear-function.json`
- 学段/年级：`middle` / `8`
- 领域：数与代数
- deep snippet 数量：`4`
- 来源概览：`books/math/OpenStax_CollegeAlgebra.md`（score=83，terms=linear function, linear, function）；`books/math/OpenStax_CollegeAlgebra.md`（score=83，terms=linear function, linear, function）；`books/math/OpenStax_CollegeAlgebra.md`（score=83，terms=linear function, linear, function）；`books/math/OpenStax_CollegeAlgebra.md`（score=83，terms=linear function, linear, function）

**课标点**

- 能根据简单实际问题中的已知条件确定一次函数的表达式；会在不同问题情境中运用待定系数法确定一次函数的表达式。
- 会画出一次函数的图象；会根据一次函数的表达式求其图象与坐标轴的交点坐标；会根据一次函数的图象和表达式 y=kx+b(k≠0)，探索并理解 k 值的变化对函数图象的影响。
- 会根据一次函数的图象解释一次函数与二元一次方程的关系；能在实际问题中列出一次函数的表达式，并结合一次函数的图象与表达式的性质等解决简单的实际问题。

**首条 deep_textbook_snippet 摘录**

- 来源：`books/math/OpenStax_CollegeAlgebra.md`
- 匹配词：`linear function, linear, function`
- 自动分：`83`

> 4.1 Linear Functions Figure 1 Shanghai MagLev Train (credit: “kanegen”/Flickr) Just as with the growth of a bamboo plant, there are many situations that involve constant change over time. Consider, for example, the first commercial maglev train in the world, the Shanghai MagLev Train (Figure 1). It carries passengers comfortably for a 30-kilometer trip from the airport to the subway station in only eight minutes.[7] Suppose a maglev train travels a long distance, and that the train maintains a constant speed of 83 …

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 2. 指数函数

- `node_id`：`math-h-exponential-function`
- 文件：`data/kp/math/math-h-exponential-function.json`
- 学段/年级：`high` / `10`
- 领域：函数
- deep snippet 数量：`3`
- 来源概览：`books/math/OpenStax_CollegeAlgebra.md`（score=83，terms=exponential function, exponential, function）；`books/math/OpenStax_CollegeAlgebra.md`（score=83，terms=exponential function, exponential, function）；`books/math/OpenStax_CollegeAlgebra.md`（score=83，terms=exponential function, exponential, function）

**课标点**

- 内容包括：函数概念与性质、幂函数、指数函数、对数函数、三角函数、函数应用。
- 主题二函数包括幂函数、指数函数、对数函数等内容的学习。

**首条 deep_textbook_snippet 摘录**

- 来源：`books/math/OpenStax_CollegeAlgebra.md`
- 匹配词：`exponential function, exponential, function`
- 自动分：`83`

> Learning Objectives In this section, you will: • Evaluate exponential functions. • Find the equation of an exponential function. • Use compound interest formulas. • Evaluate exponential functions with base e. 6.1 Exponential Functions India is the second most populous country in the world with a population of about 1.25 billion people in 2013. The population is growing at a rate of about 1.2% each year[17]. If this rate continues, the population of India will exceed China’s population by the year 2031. When populat…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 3. 勾股定理

- `node_id`：`math-m-pythagorean-theorem`
- 文件：`data/kp/math/math-m-pythagorean-theorem.json`
- 学段/年级：`middle` / `8`
- 领域：图形与几何
- deep snippet 数量：`1`
- 来源概览：`curriculum-standards/数学/初中/勾股定理.md`（score=33，terms=勾股定理, 并能运用它们解决一些简单, 探索勾股定理及其逆定理, 的实际问题, 三角形）

**课标点**

- 探索勾股定理及其逆定理，并能运用它们解决一些简单的实际问题。
- 能运用相交线、平行线、三角形、四边形的基本性质和判定解决问题。

**首条 deep_textbook_snippet 摘录**

- 来源：`curriculum-standards/数学/初中/勾股定理.md`
- 匹配词：`勾股定理, 并能运用它们解决一些简单, 探索勾股定理及其逆定理, 的实际问题, 三角形`
- 自动分：`33`

> ## 基本信息 - **学科**: 数学 - **学段**: 初中 - **年级**: 八年级 - **章节**: 图形认识 - **知识点**: 勾股定理 - **课标版本**: 义务教育课程标准（2022年版） ### 1.1 内容要求 > **【课标原文·第四学段（7～9年级）·图形的性质·三角形（续）】** > > ⑫ 理解直角三角形的概念，探索并掌握直角三角形的性质定理：直角三角形的两个锐角互余，直角三角形斜边上的中线等于斜边的一半。掌握有两个角互余的三角形是直角三角形。 > > ⑬ 探索勾股定理及其逆定理，并能运用它们解决一些简单的实际问题。 > > ⑭ 了解三角形重心的概念。 > > ⑮ 能用尺规作图：已知三边、两边及其夹角、两角及其夹角作三角形；已知底边及底边上的高线作等腰三角形；已知一直角边和斜边作直角三角形。 ### 1.3 教学提示 > 教学时应注重从学生熟悉的生活情境入手，引导学生通过具体操作、观察、归纳等方式理解勾股定理的概念。注重知识的发生发展过程，帮助学生建立知识之间的联系。 > > **【课标附录 例82 勾股定理的直观证明】** > > 使用动态几何软件设计教学活动，利用面积的不变性帮助学生…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 4. 直线与圆的位置关系

- `node_id`：`math-m-circle-tangent`
- 文件：`data/kp/math/math-m-circle-tangent.json`
- 学段/年级：`middle` / `9`
- 领域：图形与几何
- deep snippet 数量：`4`
- 来源概览：`books/math/OpenStax_CollegeAlgebra.md`（score=31，terms=circle）；`books/math/OpenStax_Prealgebra_2e.md`（score=31，terms=circle）；`books/math/OpenStax_Prealgebra_2e.md`（score=31，terms=circle）；`books/math/OpenStax_Prealgebra_2e.md`（score=31，terms=circle）

**课标点**

- 初中9年级学段目标：理解并掌握「直线与圆的位置关系」的基本概念与方法
- 学业要求：能在真实情境中识别、运用「直线与圆的位置关系」解决问题
- 活动建议：通过观察、实验、练习、讨论等方式深化对「直线与圆的位置关系」的理解

**首条 deep_textbook_snippet 摘录**

- 来源：`books/math/OpenStax_CollegeAlgebra.md`
- 匹配词：`circle`
- 自动分：`31`

> SECTION 7.3 Systems of Nonlinear Equations and Inequalities: Two Variables possible types of solutions for the points of intersection of a circle and an ellipse Figure 6 illustrates possible solution sets for a system of equations involving a circle and an ellipse. • No solution. The circle and ellipse do not intersect. One shape is inside the other or the circle and the ellipse are a distance away from the other. • One solution. The circle and ellipse are tangent to each other, and intersect at exactly one point. …

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 5. 中位数与众数

- `node_id`：`math-e-median-mode`
- 文件：`data/kp/math/math-e-median-mode.json`
- 学段/年级：`elementary` / `5`
- 领域：统计与概率
- deep snippet 数量：`4`
- 来源概览：`books/math/OpenStax_HS_Statistics.md`（score=57，terms=median, mode）；`books/math/OpenStax_HS_Statistics.md`（score=57，terms=median, mode）；`books/math/OpenStax_HS_Statistics.md`（score=57，terms=median, mode）；`books/math/OpenStax_HS_Statistics.md`（score=57，terms=median, mode）

**课标点**

- 小学5年级学段目标：理解并掌握「中位数与众数」的基本概念与方法
- 学业要求：能在真实情境中识别、运用「中位数与众数」解决问题
- 活动建议：通过观察、实验、练习、讨论等方式深化对「中位数与众数」的理解

**首条 deep_textbook_snippet 摘录**

- 来源：`books/math/OpenStax_HS_Statistics.md`
- 匹配词：`median, mode`
- 自动分：`57`

> Table 2.29 What is the best estimate for the mean number of hours spent playing video games? 2.6 | Skewness and the Mean, Median, and Mode Consider the following data set: 4, 5, 6, 6, 6, 7, 7, 7, 7, 7, 7, 8, 8, 8, 9, 10 This data set can be represented by the following histogram. Each interval has width 1, and each value is located in the middle of an interval. Figure 2.18 The histogram displays a symmetrical distribution of data. A distribution is symmetrical if a vertical line can be drawn at some point in the hi…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

## 物理

### 1. 欧姆定律

- `node_id`：`phy-m-ohms-law`
- 文件：`data/kp/physics/phy-m-ohms-law.json`
- 学段/年级：`middle` / `9`
- 领域：电现象与电路
- deep snippet 数量：`4`
- 来源概览：`books/science/OpenStax_HighSchool_Physics.md`（score=68，terms=ohm's law, ohm's, law）；`books/science/OpenStax_HighSchool_Physics.md`（score=57，terms=ohm's law, ohm's, law）；`books/science/OpenStax_HighSchool_Physics.md`（score=51，terms=ohm's law, ohm's, law）；`books/science/OpenStax_HighSchool_Physics.md`（score=45，terms=ohm's law, ohm's, law）

**课标点**

- 通过实验，探究电流与电压、电阻的关系。理解欧姆定律。
- 能运用欧姆定律解决简单的电学问题，解释生活中的有关现象。
- 在‘电和磁’主题教学中，应注重通过实验探究，引导学生理解欧姆定律等核心规律。

**首条 deep_textbook_snippet 摘录**

- 来源：`books/science/OpenStax_HighSchool_Physics.md`
- 匹配词：`ohm's law, ohm's, law`
- 自动分：`68`

> 19.1 Ohm's law • Direct current is constant over time; alternating current alternates smoothly back and forth over time. • Electrical resistance causes materials to extract work from the current that flows through them. • In ohmic materials, voltage drop along a path is proportional to the current that runs through the path. 19.2 Series Circuits • Circuit diagrams are schematic representations of electric circuits. • Resistors in series are resistors that are connected head to tail. • The same current runs through …

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 2. 内能与热量

- `node_id`：`phy-m-internal-energy`
- 文件：`data/kp/physics/phy-m-internal-energy.json`
- 学段/年级：`middle` / `9`
- 领域：热现象
- deep snippet 数量：`4`
- 来源概览：`books/science/OpenStax_HighSchool_Physics.md`（score=31，terms=heat）；`books/science/OpenStax_HighSchool_Physics.md`（score=31，terms=heat）；`books/science/OpenStax_HighSchool_Physics.md`（score=31，terms=heat）；`books/science/OpenStax_HighSchool_Physics.md`（score=31，terms=heat）

**课标点**

- 认识机械能、内能、电磁能及能量的转化与守恒；能将所学物理知识与实际情境联系起来，初步形成能量观念。
- - 国家中小学智慧教育平台：https://www.zxx.edu.cn/

**首条 deep_textbook_snippet 摘录**

- 来源：`books/science/OpenStax_HighSchool_Physics.md`
- 匹配词：`heat`
- 自动分：`31`

> Thermodynamics 12.1 Zeroth Law of Thermodynamics: Thermal Equilibrium 12.2 First law of Thermodynamics: Thermal Energy and Work 12.3 Second Law of Thermodynamics: Entropy 12.4 Applications of Thermodynamics: Heat Engines, Heat Pumps, and Refrigerators Energy can be transferred to or from a system, either through a temperature difference between it and another system (i.e., by heat) or by exerting a force through a distance (work). In these ways, energy can be converted into other forms of energy in other systems. F…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 3. 液体压强与浮力

- `node_id`：`phy-m-liquid-pressure-buoyancy`
- 文件：`data/kp/physics/phy-m-liquid-pressure-buoyancy.json`
- 学段/年级：`middle` / `8`
- 领域：运动和力
- deep snippet 数量：`4`
- 来源概览：`books/science/OpenStax_HighSchool_Physics.md`（score=33，terms=liquid, buoyancy）；`books/science/OpenStax_HighSchool_Physics.md`（score=31，terms=liquid, pressure）；`books/science/OpenStax_HighSchool_Physics.md`（score=31，terms=pressure）；`books/science/OpenStax_HighSchool_Physics.md`（score=29，terms=pressure）

**课标点**

- 探究并了解液体压强与哪些因素有关。知道大气压强及其与人类生活的关系。了解流体压强与流速的关系及其在生产生活中的应用。
- 通过实验，认识浮力。探究并了解浮力大小与哪些因素有关。知道阿基米德原理，能运用物体的浮沉条件说明生产生活中的有关现象。

**首条 deep_textbook_snippet 摘录**

- 来源：`books/science/OpenStax_HighSchool_Physics.md`
- 匹配词：`liquid, buoyancy`
- 自动分：`33`

> In everyday language, the term fluid is usually taken to mean liquid. For example, when you are sick and the doctor tells you to “push fluids,” that only means to drink more beverages—not to breath more air. However, in physics, fluid means a liquid or a gas. Fluids move differently than solid material, and even have their own branch of physics, known as fluid dynamics, that studies how they move. As the temperature of fluids increase, they expand and become less dense. For example, Figure 11.4 could represent the …

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 4. 常见的力

- `node_id`：`phy-h-common-forces`
- 文件：`data/kp/physics/phy-h-common-forces.json`
- 学段/年级：`high` / `10`
- 领域：相互作用与牛顿定律
- deep snippet 数量：`4`
- 来源概览：`science/OpenStax_HighSchool_Physics.md`（score=51，terms=force）；`science/OpenStax_HighSchool_Physics.md`（score=47，terms=force）；`science/OpenStax_HighSchool_Physics.md`（score=43，terms=force）；`science/OpenStax_HighSchool_Physics.md`（score=40，terms=force）

**课标点**

- 认识重力、弹力与摩擦力。通过实验，了解胡克定律。知道滑动摩擦和静摩擦现象，能用动摩擦因数计算滑动摩擦力的大小。
- 能对物体的受力和运动情况进行分析，得出结论。能从物理学的运动与相互作用的视角分析自然与生活中的有关简单问题。

**首条 deep_textbook_snippet 摘录**

- 来源：`science/OpenStax_HighSchool_Physics.md`
- 匹配词：`force`
- 自动分：`51`

> Chapter 4 • Forces and Newton’s Laws of Motion Access for free at openstax.org. Figure 4.2 An object of mass, m, is held up by the force of tension. Figure 4.2 shows the force of tension in the rope acting in the upward direction, opposite the force of gravity. The forces are indicated in the free-body diagram by an arrow pointing up, representing tension, and another arrow pointing down, representing gravity. In a free-body diagram, the lengths of the arrows show the relative magnitude (or strength) of the forces.…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 5. 交变电流

- `node_id`：`phy-h-alternating-current`
- 文件：`data/kp/physics/phy-h-alternating-current.json`
- 学段/年级：`high` / `12`
- 领域：电磁场与电磁感应
- deep snippet 数量：`4`
- 来源概览：`books/science/OpenStax_HighSchool_Physics.md`（score=82，terms=electric current, electric, current）；`books/science/OpenStax_HighSchool_Physics.md`（score=82，terms=electric current, electric, current）；`books/science/OpenStax_HighSchool_Physics.md`（score=82，terms=electric current, electric, current）；`books/science/OpenStax_HighSchool_Physics.md`（score=81，terms=electric current, electric, current）

**课标点**

- 高中12年级学段目标：理解并掌握「交变电流」的基本概念与方法
- 学业要求：能在真实情境中识别、运用「交变电流」解决问题
- 活动建议：通过观察、实验、练习、讨论等方式深化对「交变电流」的理解

**首条 deep_textbook_snippet 摘录**

- 来源：`books/science/OpenStax_HighSchool_Physics.md`
- 匹配词：`electric current, electric, current`
- 自动分：`82`

> Suppose four peas per second pass through a straw. If each pea carried a charge of , what would the electric current be through the straw? a. The electric current would be the pea charge multiplied by . b. The electric current would be the pea current calculated in the lab multiplied by . c. The electric current would be the pea current calculated in the lab. d. The electric current would be the pea charge divided by time. 1This energy is transferred to the wire and becomes thermal energy, which is what makes wires…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

## 生物

### 1. 光合作用

- `node_id`：`bio-m-photosynthesis-m`
- 文件：`data/kp/biology/bio-m-photosynthesis-m.json`
- 学段/年级：`middle` / `7`
- 领域：植物的结构与生理
- deep snippet 数量：`4`
- 来源概览：`books/science/OpenStax_Biology_2e.md`（score=31，terms=photosynthesis）；`books/science/OpenStax_Biology_2e.md`（score=31，terms=photosynthesis）；`books/science/OpenStax_Biology_2e.md`（score=31，terms=photosynthesis）；`books/science/OpenStax_Biology_2e.md`（score=31，terms=photosynthesis）

**课标点**

- 概念 3.1.5 生态系统中的物质和能量通过食物链在生物之间传递
- 通过本主题的学习，学生能够认识到植物分布广泛，直接或间接地为其他生物提供食物和能量；植物参与生物圈中的水循环，维持生物圈中的碳氧平衡。

**首条 deep_textbook_snippet 摘录**

- 来源：`books/science/OpenStax_Biology_2e.md`
- 匹配词：`photosynthesis`
- 自动分：`31`

> energy-storing molecule, it requires an energy input to proceed. The following equation (notice that it is the reverse of the previous equation) describes the synthesis of glucose: During photosynthesis chemical reactions, energy is in the form of a very high-energy molecule scientists call ATP, or adenosine triphosphate. This is the primary energy currency of all cells. Just as the dollar is the currency we use to buy goods, cells use ATP molecules as energy currency to perform immediate work. The sugar (glucose) …

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 2. DNA 分子结构

- `node_id`：`bio-h-dna-structure`
- 文件：`data/kp/biology/bio-h-dna-structure.json`
- 学段/年级：`high` / `10`
- 领域：基因的分子基础
- deep snippet 数量：`4`
- 来源概览：`science/OpenStax_Biology_2e.md`（score=51，terms=dna）；`science/OpenStax_Biology_2e.md`（score=49，terms=dna）；`science/OpenStax_Biology_2e.md`（score=37，terms=dna）；`science/OpenStax_Biology_2e.md`（score=33，terms=dna）

**课标点**

- 概述DNA分子是由四种脱氧核苷酸构成，通常由两条碱基互补配对的反向平行长链形成双螺旋结构，碱基的排列顺序编码了遗传信息
- 亲代传递给子代的遗传信息主要编码在DNA分子上

**首条 deep_textbook_snippet 摘录**

- 来源：`science/OpenStax_Biology_2e.md`
- 匹配词：`dna`
- 自动分：`51`

> ## Chapter 14 DNA Structure and Function 14.1 Historical Basis of Modern Understanding 14.2 DNA Structure and Sequencing 14.3 Basics of DNA Replication 14.4 DNA Replication in Prokaryotes 14.5 DNA Replication in Eukaryotes 14.6 DNA Repair The three letters “DNA” have now become synonymous with crime solving and genetic testing. DNA can be retrieved from hair, blood, or saliva. Each person’s DNA is unique, and it is possible to detect differences between individuals within a species on the basis of these unique feat…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 3. 细胞呼吸

- `node_id`：`bio-h-cellular-respiration`
- 文件：`data/kp/biology/bio-h-cellular-respiration.json`
- 学段/年级：`high` / `10`
- 领域：细胞代谢
- deep snippet 数量：`4`
- 来源概览：`science/OpenStax_Biology_2e.md`（score=91，terms=cellular respiration, cellular, respiration）；`science/OpenStax_Biology_2e.md`（score=89，terms=cellular respiration, cellular, respiration）；`books/science/OpenStax_AP_Biology.md`（score=83，terms=cellular respiration, cellular, respiration）；`books/science/OpenStax_AP_Biology.md`（score=81，terms=cellular respiration, cellular, respiration）

**课标点**

- 说明生物通过细胞呼吸将储存在有机分子中的能量转化为生命活动可以利用的能量
- 从物质与能量视角，探索光合作用与呼吸作用，阐明细胞生命活动过程中贯穿着物质与能量的变化

**首条 deep_textbook_snippet 摘录**

- 来源：`science/OpenStax_Biology_2e.md`
- 匹配词：`cellular respiration, cellular, respiration`
- 自动分：`91`

> ## Chapter 7 Cellular Respiration 7.1 Energy in Living Systems 7.2 Glycolysis 7.3 Oxidation of Pyruvate and the Citric Acid Cycle 7.4 Oxidative Phosphorylation 7.5 Metabolism without Oxygen 7.6 Connections of Carbohydrate, Protein, and Lipid Metabolic Pathways 7.7 Regulation of Cellular Respiration The electrical energy plant in Figure 7.1 converts energy from one form to another form that can be more easily used. This type of generating plant starts with underground thermal energy (heat) and transforms it into ele…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 4. 食物链与食物网

- `node_id`：`bio-m-food-chain`
- 文件：`data/kp/biology/bio-m-food-chain.json`
- 学段/年级：`middle` / `7`
- 领域：生物与环境
- deep snippet 数量：`4`
- 来源概览：`books/science/OpenStax_Biology_2e.md`（score=68，terms=food, chain, web）；`books/science/OpenStax_AP_Biology.md`（score=66，terms=food, chain, web）；`books/science/OpenStax_AP_Biology.md`（score=60，terms=food, chain, web）；`books/science/OpenStax_Biology_2e.md`（score=58，terms=food, chain, web）

**课标点**

- 生态系统中不同生物之间通过捕食关系形成了食物链和食物网
- 运用图示或模型表示生态系统中各生物成分之间的营养关系
- 结合具体实例，引导学生分析生态系统中各成分的作用及其相互关系，并用恰当的形式呈现，发展学生的建模思维

**首条 deep_textbook_snippet 摘录**

- 来源：`books/science/OpenStax_Biology_2e.md`
- 匹配词：`food, chain, web`
- 自动分：`68`

> By the end of this section, you will be able to do the following: • Describe how organisms acquire energy in a food web and in associated food chains • Explain how the efficiency of energy transfers between trophic levels affects ecosystem structure and dynamics • Discuss trophic levels and how ecological pyramids are used to model them All living things require energy in one form or another. Energy is required by most complex metabolic pathways (often in the form of adenosine triphosphate, ATP), especially those r…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 5. 酶

- `node_id`：`bio-h-enzyme`
- 文件：`data/kp/biology/bio-h-enzyme.json`
- 学段/年级：`high` / `10`
- 领域：细胞代谢
- deep snippet 数量：`4`
- 来源概览：`science/OpenStax_Biology_2e.md`（score=49，terms=enzymes）；`science/OpenStax_Biology_2e.md`（score=45，terms=enzymes）；`science/OpenStax_Biology_2e.md`（score=37，terms=enzymes）；`science/OpenStax_Biology_2e.md`（score=33，terms=enzymes）

**课标点**

- 2.2.1 说明绝大多数酶是一类能催化生化反应的蛋白质，酶活性受到环境因素（如pH和温度等）的影响
- 探究酶催化的专一性、高效性及影响酶活性的因素

**首条 deep_textbook_snippet 摘录**

- 来源：`science/OpenStax_Biology_2e.md`
- 匹配词：`enzymes`
- 自动分：`49`

> Mineral Function Deficiencies Can Lead To Sources Iron Required for many proteins and enzymes, notably hemoglobin, to prevent anemia Anemia, which causes poor concentration, fatigue, and poor immune function Red meat, leafy green vegetables, fish (tuna, salmon), eggs, dried fruits, beans, whole grains *Magnesium Required cofactor for ATP formation; bone formation; normal membrane functions; muscle function Mood disturbances, muscle spasms Whole grains, leafy green vegetables Manganese (trace amounts) A cofactor in …

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

## 化学

### 1. 中和反应

- `node_id`：`chem-m-neutralization`
- 文件：`data/kp/chemistry/chem-m-neutralization.json`
- 学段/年级：`middle` / `9`
- 领域：物质的性质与应用
- deep snippet 数量：`4`
- 来源概览：`03_introductory_chemistry.md`（score=39，terms=中和反应）；`03_introductory_chemistry.md`（score=39，terms=中和反应, 变化）；`03_introductory_chemistry.md`（score=39，terms=中和反应, 变化）；`03_introductory_chemistry.md`（score=39，terms=中和反应）

**课标点**

- 探究氢氧化钠溶液和稀盐酸发生中和反应时的温度变化、pH 变化。
- 学会用酸碱指示剂、pH 试纸检验溶液的酸碱性。

**首条 deep_textbook_snippet 摘录**

- 来源：`03_introductory_chemistry.md`
- 匹配词：`中和反应`
- 自动分：`39`

> ## 第 152 页 [2 ess BAIT碱 ARERR COMME), Emtec 了 HERE: 盐酸 HCI AN = NOH eer. 氢省酸 HBr 氧氧化锂 LiOH S 硝酸 HNO} “avr KOH go Zo 硫酸 HSO4 氧氧化钙 Ca(OH), a : Bh i SL HCI0, 所氧化钢 Ba(OH)， fy a mine HC3H30; ay | 5 Mi LACAN A, WT. RR. ARE Ch AT. P 中和反应通常会生成水和一种离子化合物〈称为盐)，这种化合物通 常也溶解在溶液中。许多中和反应的净离子方程式为 se H" (aq) + OH” (ag) —>H,0(0) Fig.) 另一个中和反应是发生在硫酸和氧氧化钾之间的反应; 仅 识别并写出析气反应方程式 0 注意酸和碱反应生成水和盐的模式: 酸 + 碱一水 + 盐《酸碱中和反应) 书写中和反应方程式时, 使用 5.5 节中给出的离子化合物的方程式书 写盐的方程式。 oi 7.11 书写中和反应方程式 写出硝酸水溶液和氧氧化钙水溶液反应的分子和净离子方程式。 和 首先要知道这些物质是酸还是碱，然后 | 解 按照酸加碱产生水和…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 2. 氧气的性质

- `node_id`：`chem-m-oxygen-properties`
- 文件：`data/kp/chemistry/chem-m-oxygen-properties.json`
- 学段/年级：`middle` / `9`
- 领域：物质的性质与应用
- deep snippet 数量：`4`
- 来源概览：`books/science/OpenStax_Chemistry.md`（score=31，terms=properties）；`books/science/OpenStax_Chemistry.md`（score=31，terms=properties）；`books/science/OpenStax_Chemistry.md`（score=30，terms=properties）；`science/OpenStax_Chemistry.md`（score=25，terms=）

**课标点**

- 氧气的实验室制取与性质。
- 能通过实验探究氧气的化学性质，认识氧气是一种化学性质比较活泼的气体

**首条 deep_textbook_snippet 摘录**

- 来源：`books/science/OpenStax_Chemistry.md`
- 匹配词：`properties`
- 自动分：`31`

> Figure 1.17 Almost one-third of naturally occurring elements are used to make a cell phone. (credit: modification of work by John Taylor) 1.3 Physical and Chemical Properties By the end of this section, you will be able to: • Identify properties of and changes in matter as physical or chemical • Identify properties of matter as extensive or intensive The characteristics that enable us to distinguish one substance from another are called properties. A physical property is a characteristic of matter that is not assoc…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 3. 质量守恒定律

- `node_id`：`chem-m-mass-conservation`
- 文件：`data/kp/chemistry/chem-m-mass-conservation.json`
- 学段/年级：`middle` / `9`
- 领域：物质的化学变化
- deep snippet 数量：`4`
- 来源概览：`science/OpenStax_Chemistry.md`（score=43，terms=mass）；`03_introductory_chemistry.md`（score=37，terms=质量守恒定律）；`03_introductory_chemistry.md`（score=34，terms=质量守恒定律）；`03_introductory_chemistry.md`（score=34，terms=质量守恒定律）

**课标点**

- 认识质量守恒定律对资源利用和物质转化的重要意义；能从定性和定量的视角研究物质的组成及变化。
- 化学反应及质量守恒定律：化学变化的特征及化学反应的基本类型；化学反应的定量关系与质量守恒定律。
- 质量守恒定律的发现；通过具体的化学实验探究活动，学习研究物质性质，探究物质组成和反应规律。

**首条 deep_textbook_snippet 摘录**

- 来源：`science/OpenStax_Chemistry.md`
- 匹配词：`mass`
- 自动分：`43`

> Figure 3.13 An oxide of carbon is removed from these fermentation tanks through the large copper pipes at the top. (credit: “Dual Freq”/Wikimedia Commons) Solution Since the scale for percentages is 100, it is most convenient to calculate the mass of elements present in a sample weighing 100 g. The calculation is “most convenient” because, per the definition for percent composition, the mass of a given element in grams is numerically equivalent to the element’s mass percentage. This numerical equivalence results fr…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 4. 溶液的形成

- `node_id`：`chem-m-solution-concept`
- 文件：`data/kp/chemistry/chem-m-solution-concept.json`
- 学段/年级：`middle` / `9`
- 领域：物质的性质与应用
- deep snippet 数量：`4`
- 来源概览：`science/OpenStax_Chemistry.md`（score=41，terms=solutions）；`science/OpenStax_Chemistry.md`（score=37，terms=solutions）；`books/science/OpenStax_Chemistry.md`（score=31，terms=solutions）；`books/science/OpenStax_Chemistry.md`（score=31，terms=solutions）

**课标点**

- 初步学会配制一定溶质质量分数的溶液。
- 测定并比较氯化钠、硝酸铵、氢氧化钠在水中溶解时溶液的温度变化。

**首条 deep_textbook_snippet 摘录**

- 来源：`science/OpenStax_Chemistry.md`
- 匹配词：`solutions`
- 自动分：`41`

> > **[Figure 113, Page 164]** A figure or diagram (650×385px) related to: Dilution, Solutions, process, whereby, concentration, solution. This image appears on page 164 of the textbook. ![Figure 113 - A figure or diagram (650×385px) related to: Dilution, Soluti](OpenStax_Chemistry_images/img_0113_c8551e7f.png) > **[Figure 114, Page 164]** A large illustration or diagram (975×405px) related to: Dilution, Solutions, process, whereby, concentration, solution. This image appears on page 164 of the textbook. ![Figure 114…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 5. 金属的锈蚀与防护

- `node_id`：`chem-m-metal-corrosion`
- 文件：`data/kp/chemistry/chem-m-metal-corrosion.json`
- 学段/年级：`middle` / `9`
- 领域：物质的性质与应用
- deep snippet 数量：`4`
- 来源概览：`science/OpenStax_Chemistry.md`（score=41，terms=metals）；`books/science/OpenStax_Chemistry.md`（score=31，terms=metals）；`books/science/OpenStax_Chemistry.md`（score=31，terms=metals）；`books/science/OpenStax_Chemistry.md`（score=31，terms=metals）

**课标点**

- 常见金属的物理性质和化学性质。
- - **内容来源**: TeachAny 课标知识点卫星文件

**首条 deep_textbook_snippet 摘录**

- 来源：`science/OpenStax_Chemistry.md`
- 匹配词：`metals`
- 自动分：`41`

> Figure 18.28 Before the fleet’s retirement in 2011, liquid hydrogen and liquid oxygen were used in the three main engines of a space shuttle. Two compartments in the large tank held these liquids until the shuttle was launched. (credit: “reynermedia”/Flickr) An uncombined hydrogen atom consists of a nucleus and one valence electron in the 1s orbital. The n = 1 valence shell has a capacity for two electrons, and hydrogen can rightfully occupy two locations in the periodic table. It is possible to consider hydrogen a…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

## 历史

### 1. 工业革命

- `node_id`：`hist-m-industrial-revolution`
- 文件：`data/kp/history/hist-m-industrial-revolution.json`
- 学段/年级：`middle` / `9`
- 领域：世界近现代史
- deep snippet 数量：`4`
- 来源概览：`social_studies/OpenStax_US_History.md`（score=65，terms=industrial revolution, industrial, revolution）；`books/social_studies/OpenStax_US_History.md`（score=53，terms=industrial revolution, industrial, revolution）；`books/social_studies/OpenStax_US_History.md`（score=49，terms=industrial revolution, industrial, revolution）；`books/social_studies/OpenStax_US_History.md`（score=46，terms=industrial revolution, industrial, revolution）

**课标点**

- 世界近代史内容要求：了解资本主义发展、社会主义运动和民族解放运动。
- 课程内容结构示意图显示，世界近代史的主题包括资本主义发展、社会主义运动和民族解放运动。

**首条 deep_textbook_snippet 摘录**

- 来源：`social_studies/OpenStax_US_History.md`
- 匹配词：`industrial revolution, industrial, revolution`
- 自动分：`65`

> ## Figure 18.2 The late nineteenth century was an energetic era of inventions and entrepreneurial spirit. Building upon the mid-century Industrial Revolution in Great Britain, as well as answering the increasing call from Americans for efficiency and comfort, the country found itself in the grip of invention fever, with more people working on their big ideas than ever before. In retrospect, harnessing the power of steam and then electricity in the nineteenth century vastly increased the power of man and machine, th…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 2. 新航路开辟与殖民扩张

- `node_id`：`hist-h-age-of-exploration`
- 文件：`data/kp/history/hist-h-age-of-exploration.json`
- 学段/年级：`high` / `11`
- 领域：世界近现代史
- deep snippet 数量：`4`
- 来源概览：`social_studies/OpenStax_US_History.md`（score=25，terms=）；`social_studies/OpenStax_US_History.md`（score=25，terms=）；`social_studies/OpenStax_US_History.md`（score=25，terms=）；`social_studies/OpenStax_US_History.md`（score=25，terms=）

**课标点**

- 本课程以马克思主义为指导，通过对中外重大历史事件、历史人物和历史现象的叙述，展现人类发展进程中丰富的历史文化遗产，以及人类社会从古至今、从分散到整体、社会形态从低级到高级的发展历程。
- 了解世界历史发展的多样性，理解和尊重世界各国各地区的文化传统，拓宽国际视野，形成开放的世界意识。

**首条 deep_textbook_snippet 摘录**

- 来源：`social_studies/OpenStax_US_History.md`
- 匹配词：``
- 自动分：`25`

> ## My Story 27.2 • The Home Front > **[Figure 486, Page 747]** A figure or diagram (260×335px) related to: FIGURE, Dwight, Eisenhower, rose, quickly, ranks. This image appears on page 747 of the textbook. ![Figure 486 - A figure or diagram (260×335px) related to: FIGURE, Dwight, ](OpenStax_US_History_images/img_0486_a24469da.png) the word. I’m quitting work now, 7:30 p.m. I haven’t the heart to go on tonight. —Dwight D. Eisenhower, The Eisenhower Diaries” What does Eisenhower identify as the most important steps to…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 3. 古代亚非欧文明

- `node_id`：`hist-h-ancient-civ-h`
- 文件：`data/kp/history/hist-h-ancient-civ-h.json`
- 学段/年级：`high` / `11`
- 领域：世界古代中世纪史
- deep snippet 数量：`4`
- 来源概览：`social_studies/OpenStax_US_History.md`（score=25，terms=）；`social_studies/OpenStax_US_History.md`（score=23，terms=）；`social_studies/OpenStax_US_History.md`（score=21，terms=）；`social_studies/OpenStax_US_History.md`（score=21，terms=）

**课标点**

- 本课程以马克思主义为指导，通过对中外重大历史事件、历史人物和历史现象的叙述，展现人类发展进程中丰富的历史文化遗产，以及人类社会从古至今、从分散到整体、社会形态从低级到高级的发展历程。
- 通过学习，学生应了解和掌握唯物史观的基本观点，体会唯物史观的科学性，理解不同时空条件下历史的延续、变迁与发展，学习史料实证的基本方法，能够在此基础上对历史作出正确的解释。
- 深化对中华民族多元一体发展趋势的认识，认同社会主义核心价值观和中华优秀传统文化，了解世界历史发展的多样性，理解和尊重世界各国各地区的文化传统，拓宽国际视野，形成开放的世界意识。

**首条 deep_textbook_snippet 摘录**

- 来源：`social_studies/OpenStax_US_History.md`
- 匹配词：``
- 自动分：`25`

> > **[Figure 9, Page 23]** A figure or diagram (390×448px) related to: FIGURE, shows, extent, major, civilizations, Western. This image appears on page 23 of the textbook. ![Figure 9 - A figure or diagram (390×448px) related to: FIGURE, shows, e](OpenStax_US_History_images/img_0009_a24469da.png) FIGURE 1.4 The Olmec carved heads from giant boulders that ranged from four to eleven feet in height and could weigh up to fifty tons. All these figures have flat noses, slightly crossed eyes, and large lips. These physical …

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 4. 古代经济（农业/手工业/商业）

- `node_id`：`hist-h-ancient-economy`
- 文件：`data/kp/history/hist-h-ancient-economy.json`
- 学段/年级：`high` / `10`
- 领域：中国古代史
- deep snippet 数量：`4`
- 来源概览：`books/social_studies/OpenStax_US_History.md`（score=22，terms=industry）；`books/social_studies/OpenStax_US_History.md`（score=21，terms=industry）；`books/social_studies/OpenStax_US_History.md`（score=21，terms=industry）；`books/social_studies/OpenStax_US_History.md`（score=21，terms=industry）

**课标点**

- 通过了解春秋战国时期的经济发展和政治变动，理解战国时期变法运动的必然性。
- 通过了解明清时期社会经济、思想文化的重要变化；通过了解明清时期封建专制的发展、世界的变化对中国的影响，认识中国社会面临的危机。

**首条 deep_textbook_snippet 摘录**

- 来源：`books/social_studies/OpenStax_US_History.md`
- 匹配词：`industry`
- 自动分：`22`

> While the cattle industry lacked the romance of the Gold Rush, the role it played in western expansion should not be underestimated. For centuries, wild cattle roamed the Spanish borderlands. At the end of the Civil War, as many as five million longhorn steers could be found along the Texas frontier, yet few settlers had capitalized on the opportunity to claim them, due to the difficulty of transporting them to eastern markets. The completion of the first transcontinental railroad and subsequent railroad lines chan…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：

### 5. 冷战格局

- `node_id`：`hist-h-cold-war-h`
- 文件：`data/kp/history/hist-h-cold-war-h.json`
- 学段/年级：`high` / `12`
- 领域：世界近现代史
- deep snippet 数量：`4`
- 来源概览：`social_studies/OpenStax_US_History.md`（score=70，terms=cold war, cold, war）；`social_studies/OpenStax_US_History.md`（score=69，terms=cold war, cold, war）；`social_studies/OpenStax_US_History.md`（score=69，terms=cold war, cold, war）；`social_studies/OpenStax_US_History.md`（score=64，terms=cold war, cold, war）

**课标点**

- 通过了解第二次世界大战后国际格局的变化，理解冷战的发生与发展，认识两极格局的特征及其对世界的影响。
- 了解杜鲁门主义、马歇尔计划、北约与华约的对峙，认识美苏争霸对国际关系的影响。
- 通过对古巴导弹危机、越南战争、阿富汗战争等热点事件的了解，理解冷战中的局部冲突与世界格局的复杂性。

**首条 deep_textbook_snippet 摘录**

- 来源：`social_studies/OpenStax_US_History.md`
- 匹配词：`cold war, cold, war`
- 自动分：`70`

> 31 • From Cold War to Culture Wars, 1980-2000 Access for free at openstax.org. > **[Figure 572, Page 872]** A wide diagram or timeline (585×210px) related to: MIDDLE, EAST, CENTRAL, AMERICA, Reagan, desire. This image appears on page 872 of the textbook. ![Figure 572 - A wide diagram or timeline (585×210px) related to: MIDDLE, E](OpenStax_US_History_images/img_0572_f68e9d4c.jpg) congressional ban on military aid to the anti-Communist guerillas in that Central American nation. Eventually the Senate became aware, and…

**人工审查**

- 相关性：□ 相关  □ 部分相关  □ 不相关
- 问题类型：□ 精准  □ 偏大主题  □ 目录/索引  □ 通用教学原则  □ 错学科  □ 其他
- 处理建议：
- 审查人/日期：
