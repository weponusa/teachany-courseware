# PLAN.md — 能量转化与守恒定律：从实验现象到变量关系

- course_id: `phy-m-energy-conservation`
- node_id: `phy-m-energy-conservation`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：物理
- 课标节点：能量转化与守恒定律
- 课标摘录：3.5 能量守恒：知道能量守恒定律；列举日常生活中能量守恒的实例；有用能量守恒的观点分析物理现象的意识。；认识机械能、内能、电磁能及能量的转化与守恒；能将所学物理知识与实际情境联系起来，解释有关现象，解决简单的实际问题。初步形成能量观念。；能量主题旨在引导学生了解不同形式的能量，知道能量的转化与转移，认识能量守恒定律，了解能源与可持续发展。

## Phase 1 教学骨架
- 问题锚点：怎样用实验现象和变量关系解释能量转化与守恒定律？
- ABT：
  - And：你已经在生活中见过能量转化与守恒定律相关现象，也能说出一些直观经验。
  - But：物理学习不能停在经验判断，因为经验常被条件影响；换一个材料、尺度或装置，结论可能改变。
  - Therefore：所以本课要用“观察现象—控制变量—建立关系—解释应用”的路径，理解能量转化与守恒定律。
- 真实互动：Canvas 变量实验 + PhET 成熟仿真 + 前后测反馈
- 评估闭环：前测 → 实验检查表 → 概念拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：Canvas 自定义变量互动 + PhET 中文仿真。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-m-energy-conservation`
- `python3 scripts/validate-courseware.py phy-m-energy-conservation`
- `python3 scripts/rebuild-index.py`
