# PLAN.md — 功能关系综合：从真实情境到物理模型

- course_id: `phy-h-work-energy`
- node_id: `phy-h-work-energy`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：功能关系综合
- 课标摘录：理解功和功率。了解生产生活中常见机械的功率大小及其意义。；理解动能和动能定理。能用动能定理解释生产生活中的现象。；理解重力势能，知道重力势能的变化与重力做功的关系。定性了解弹性势能。

## Phase 1 教学骨架
- 问题锚点：怎样用物理模型解释和计算「功能关系综合」中的关键现象？
- ABT：
  - And：你已经掌握了前置知识，能够识别物体、相互作用、运动状态或能量变化等基本线索。
  - But：一到「功能关系综合」综合情境，题目会把文字、图像、公式和实验条件混在一起；如果不先建模，很容易套错公式。
  - Therefore：所以本课围绕「功能关系综合」建立对象—条件—变量—证据的分析链，把真实情境转化为可计算、可解释的物理模型。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-work-energy`
- `python3 scripts/validate-courseware.py phy-h-work-energy`
- `python3 scripts/rebuild-index.py`
