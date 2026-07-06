# PLAN.md — 欧姆定律：从实验现象到变量关系

- course_id: `phy-m-ohms-law`
- node_id: `phy-m-ohms-law`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：物理
- 课标节点：欧姆定律
- 课标摘录：通过实验，探究电流与电压、电阻的关系。理解欧姆定律。；能运用欧姆定律解决简单的电学问题，解释生活中的有关现象。；在‘电和磁’主题教学中，应注重通过实验探究，引导学生理解欧姆定律等核心规律。

## Phase 1 教学骨架
- 问题锚点：怎样用实验现象和变量关系解释欧姆定律？
- ABT：
  - And：你已经在生活中见过欧姆定律相关现象，也能说出一些直观经验。
  - But：物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。
  - Therefore：所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解欧姆定律。
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-m-ohms-law`
- `python3 scripts/validate-courseware.py phy-m-ohms-law`
- `python3 scripts/rebuild-index.py`
