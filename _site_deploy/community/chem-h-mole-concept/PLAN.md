# PLAN.md — 物质的量：把微观粒子数变成可称量的宏观量

- course_id: `chem-h-mole-concept`
- node_id: `chem-h-mole-concept`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：物质的量（摩尔）
- 课标摘录：了解物质的量及其相关物理量的含义和应用，体会定量研究对化学科学的重要作用。；能基于物质的量认识物质组成及其化学变化，运用物质的量、摩尔质量、气体摩尔体积、物质的量浓度之间的相互关系进行简单计算。；学生必做实验：配制一定物质的量浓度的溶液。

## Phase 1 教学骨架
- 问题锚点：为什么化学计算不直接数分子，而要引入“1 mol”这个桥梁？
- ABT：
  - And：你会用质量描述一包食盐有多重，也知道化学反应本质上是粒子之间按比例反应。
  - But：原子、分子太小，无法一粒一粒数；只看克数又无法直接知道有多少粒子参与反应。
  - Therefore：所以引入物质的量 n 和摩尔 mol，用阿伏加德罗常数把微观粒子数、质量和化学方程式连接起来。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-mole-concept`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
