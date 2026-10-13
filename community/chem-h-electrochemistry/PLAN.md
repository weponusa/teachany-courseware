# PLAN.md — 电化学基础：把氧化还原反应变成电流

- course_id: `chem-h-electrochemistry`
- node_id: `chem-h-electrochemistry`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：电化学基础
- 课标摘录：认识化学变化有一定限度、速率，是可以调控的。能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；认识化学变化的本质特征是有新物质生成，并伴有能量转化；；了解实验、假说、模型、比较、分类等方法在化学科学研究中的运用。

## Phase 1 教学骨架
- 问题锚点：原电池为什么能把自发氧化还原反应转化成电能？
- ABT：
  - And：你已经知道氧化还原反应本质是电子转移，也会判断氧化剂和还原剂。
  - But：如果电子只在溶液中直接转移，我们看不到可用电流；要让电子走外电路，就需要把氧化和还原分开。
  - Therefore：所以要学习原电池结构：负极氧化、正极还原，电子经外电路流动，离子通过盐桥或电解质维持电荷平衡。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-electrochemistry`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
