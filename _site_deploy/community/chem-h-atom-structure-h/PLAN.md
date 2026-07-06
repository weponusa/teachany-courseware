# PLAN.md — 原子结构：从核电荷数到元素性质

- course_id: `chem-h-atom-structure-h`
- node_id: `chem-h-atom-structure-h`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：原子结构
- 课标摘录：认识化学是在原子、分子水平上研究物质的组成、结构、性质、转化及其应用的一门基础学科，其特征是认识物质和创造物质。；能从元素和原子、分子水平认识物质的组成、结构、性质和变化，形成“结构决定性质”的观念。；有关理论、模型不断发展的史实：苯分子结构、原子结构模型、氧化还原反应理论等。

## Phase 1 教学骨架
- 问题锚点：为什么质子数决定元素种类，而最外层电子决定很多化学性质？
- ABT：
  - And：你已经知道物质由分子、原子、离子构成，也知道元素种类与原子有关。
  - But：只说“原子很小”并不能解释为什么钠容易失电子、氯容易得电子，也不能解释同位素和离子差异。
  - Therefore：所以要用质子数、中子数、核外电子排布和最外层电子理解元素身份、质量数与化学性质。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-atom-structure-h`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
