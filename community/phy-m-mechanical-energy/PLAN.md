# PLAN.md — 机械能（动能/势能）：从实验现象到变量关系

- course_id: `phy-m-mechanical-energy`
- node_id: `phy-m-mechanical-energy`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：物理
- 课标节点：机械能（动能/势能）
- 课标摘录：3.2 机械能：通过实验，认识动能和势能。探究并了解动能、势能的变化与哪些因素有关。；3.1 能量、能量的转化和转移：结合实例，认识能量可以从一个物体转移到另一个物体，不同形式的能量可以互相转化。；3.5 能量守恒：知道机械能守恒定律。能用机械能守恒定律分析生产、生活中的有关问题。

## Phase 1 教学骨架
- 问题锚点：怎样用实验现象和变量关系解释机械能（动能/势能）？
- ABT：
  - And：你已经在生活中见过机械能（动能/势能）相关现象，也能说出一些直观经验。
  - But：物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。
  - Therefore：所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解机械能（动能/势能）。
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-m-mechanical-energy`
- `python3 scripts/validate-courseware.py phy-m-mechanical-energy`
- `python3 scripts/rebuild-index.py`
