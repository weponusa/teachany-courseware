# PLAN.md — 物态变化（熔化/汽化/凝固）：从实验现象到变量关系

- course_id: `phy-m-phase-change`
- node_id: `phy-m-phase-change`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 8 年级
- 学科：物理
- 课标节点：物态变化（熔化/汽化/凝固）
- 课标摘录：1.1.3 经历物态变化的实验探究过程，知道物质的熔点、凝固点和沸点，了解物态变化过程中的吸热和放热现象。能运用物态变化知识说明自然界和生活中的有关现象。；能描述固态、液态和气态的基本特征及在相互转化过程中的特点...能根据这些知识解释有关自然现象，尝试运用这些知识解决日常生活中的有关问题，形成初步的物质观念。；尤其在物态变化特点、规律的实验教学中，引导学生基于证据进行归纳、总结、解释及交流，促进学生科学思维和科学探究能力的发展。

## Phase 1 教学骨架
- 问题锚点：怎样用实验现象和变量关系解释物态变化（熔化/汽化/凝固）？
- ABT：
  - And：你已经在生活中见过物态变化（熔化/汽化/凝固）相关现象，也能说出一些直观经验。
  - But：物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。
  - Therefore：所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解物态变化（熔化/汽化/凝固）。
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-m-phase-change`
- `python3 scripts/validate-courseware.py phy-m-phase-change`
- `python3 scripts/rebuild-index.py`
