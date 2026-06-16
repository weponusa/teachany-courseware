# PLAN.md — 大气压强：从实验现象到变量关系

- course_id: `phy-m-atmospheric-pressure`
- node_id: `phy-m-atmospheric-pressure`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 8 年级
- 学科：物理
- 课标节点：大气压强
- 课标摘录：2.2.8 探究并了解液体压强与哪些因素有关。知道大气压强及其与人类生活的关系。了解流体压强与流速的关系及其在生产生活中的应用。；例9 了解铁路站台上设置安全线的必要性。

## Phase 1 教学骨架
- 问题锚点：怎样用实验现象和变量关系解释大气压强？
- ABT：
  - And：你已经在生活中见过大气压强相关现象，也能说出一些直观经验。
  - But：物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。
  - Therefore：所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解大气压强。
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-m-atmospheric-pressure`
- `python3 scripts/validate-courseware.py phy-m-atmospheric-pressure`
- `python3 scripts/rebuild-index.py`
