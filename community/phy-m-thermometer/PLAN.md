# PLAN.md — 温度与温度计：从实验现象到变量关系

- course_id: `phy-m-thermometer`
- node_id: `phy-m-thermometer`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 8 年级
- 学科：物理
- 课标节点：温度与温度计
- 课标摘录：了解液体温度计的工作原理。会用常见温度计测量温度。能说出生活环境中常见的温度值。；会正确使用天平、温度计等实验器材，能按实验方案操作，获得实验数据。

## Phase 1 教学骨架
- 问题锚点：怎样用实验现象和变量关系解释温度与温度计？
- ABT：
  - And：你已经在生活中见过温度与温度计相关现象，也能说出一些直观经验。
  - But：物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。
  - Therefore：所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解温度与温度计。
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-m-thermometer`
- `python3 scripts/validate-courseware.py phy-m-thermometer`
- `python3 scripts/rebuild-index.py`
