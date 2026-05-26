# PLAN.md — 硫和氮及其化合物：价态转化与环境影响

- course_id: `chem-h-sulfur-nitrogen`
- node_id: `chem-h-sulfur-nitrogen`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：硫和氮及其化合物
- 课标摘录：结合真实情境中的应用实例或通过实验探究，了解氯、氮、硫及其重要化合物的主要性质，认识这些物质在生产中的应用和对生态环境的影响。；不同价态含硫物质的转化。；氮氧化物的性质与转化；浓、稀硝酸的性质；氨气的制备及性质；铵盐的性质。

## Phase 1 教学骨架
- 问题锚点：怎样用价态转化解释硫、氮化合物的工业价值和环境风险？
- ABT：
  - And：你已经掌握氧化还原反应、酸碱盐和离子反应，知道化学物质会在空气和水中转化。
  - But：SO₂、NO₂、NH₃、硝酸、硫酸等物质既能服务工业，又可能造成酸雨、尾气污染和安全风险。
  - Therefore：所以要围绕价态变化、典型反应和环境治理理解硫氮化合物，而不是孤立记方程式。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-sulfur-nitrogen`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
