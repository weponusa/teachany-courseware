# PLAN.md — 气体摩尔体积：同温同压下气体为什么按体积比反应？

- course_id: `chem-h-gas-molar-volume`
- node_id: `chem-h-gas-molar-volume`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：气体摩尔体积
- 课标摘录：了解物质的量及其相关物理量的含义和应用，体会定量研究对化学科学的重要作用。；能基于物质的量认识物质组成及其化学变化，运用物质的量、摩尔质量、气体摩尔体积、物质的量浓度之间的相互关系进行简单计算。

## Phase 1 教学骨架
- 问题锚点：为什么在标准状况下，1 mol 不同气体都近似占 22.4 L？
- ABT：
  - And：你已经知道 1 mol 代表相同数量的粒子，也会用 n=m/M 计算物质的量。
  - But：气体很难像固体那样直接称量；同样 1 mol 氧气、氢气、二氧化碳质量不同，体积却在同温同压下近似相同。
  - Therefore：所以要学习气体摩尔体积 Vₘ，用温度、压强和物质的量解释气体体积关系。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-gas-molar-volume`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
