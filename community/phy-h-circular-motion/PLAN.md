# PLAN.md — 圆周运动：速度方向一直变就是有加速度

- course_id: `phy-h-circular-motion`
- node_id: `phy-h-circular-motion`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：圆周运动
- 课标摘录：会用线速度、角速度、周期描述匀速圆周运动。知道匀速圆周运动向心加速度的大小和方向。；通过实验，探究并了解匀速圆周运动向心力大小与半径、角速度、质量的关系。；能用牛顿第二定律分析匀速圆周运动的向心力。了解生产生活中的离心现象及其产生的原因。

## Phase 1 教学骨架
- 问题锚点：为什么匀速圆周运动速率不变，却仍然有加速度？
- ABT：
  - And：你已经知道速度是矢量，速度大小或方向改变都表示运动状态改变。
  - But：匀速圆周运动的速率不变，却仍然需要向心加速度和向心力；这和“速度没变就没有加速度”的直觉冲突。
  - Therefore：所以要理解线速度、角速度、周期、向心加速度和向心力之间的关系。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-circular-motion`
- `python3 scripts/validate-courseware.py phy-h-circular-motion`
- `python3 scripts/rebuild-index.py`
