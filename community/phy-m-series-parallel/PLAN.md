# PLAN.md — 串联与并联电路：从实验现象到变量关系

- course_id: `phy-m-series-parallel`
- node_id: `phy-m-series-parallel`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：物理
- 课标节点：串联与并联电路
- 课标摘录：【内容要求】2.4 电和磁：通过实验，了解串、并联电路的特点。能连接简单的串联电路和并联电路。；【内容要求】2.4 电和磁：会使用电流表和电压表。探究并了解串联电路和并联电路中电流、电压的特点。

## Phase 1 教学骨架
- 问题锚点：怎样用实验现象和变量关系解释串联与并联电路？
- ABT：
  - And：你已经在生活中见过串联与并联电路相关现象，也能说出一些直观经验。
  - But：物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。
  - Therefore：所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解串联与并联电路。
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-m-series-parallel`
- `python3 scripts/validate-courseware.py phy-m-series-parallel`
- `python3 scripts/rebuild-index.py`
