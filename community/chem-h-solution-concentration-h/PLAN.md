# PLAN.md — 物质的量浓度：怎样配出准确浓度的溶液？

- course_id: `chem-h-solution-concentration-h`
- node_id: `chem-h-solution-concentration-h`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：物质的量浓度
- 课标摘录：了解物质的量及其相关物理量的含义和应用，体会定量研究对化学科学的重要作用。；能基于物质的量认识物质组成及其化学变化，运用物质的量、摩尔质量、气体摩尔体积、物质的量浓度之间的相互关系进行简单计算。；实验及探究活动：配制一定物质的量浓度的溶液。

## Phase 1 教学骨架
- 问题锚点：实验室怎样把“称多少、加多少水”转化成准确的 mol/L 浓度？
- ABT：
  - And：你已经会用物质的量表示粒子数量，也知道溶液由溶质和溶剂组成。
  - But：只说“加了 5 g 溶质”还不够，因为同样的溶质放进 100 mL 和 1 L 水中浓度完全不同。
  - Therefore：所以要用物质的量浓度 c=n/V 精确描述单位体积溶液中含有多少物质的量，并掌握容量瓶配制步骤。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-solution-concentration-h`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
