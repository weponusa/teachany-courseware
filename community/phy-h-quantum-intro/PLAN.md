# PLAN.md — 量子力学初步：从真实情境到物理模型

- course_id: `phy-h-quantum-intro`
- node_id: `phy-h-quantum-intro`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 12 年级
- 学科：物理
- 课标节点：量子力学初步
- 课标摘录：高中12年级学段目标：理解并掌握「量子力学初步」的基本概念与方法；学业要求：能在真实情境中识别、运用「量子力学初步」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「量子力学初步」的理解

## Phase 1 教学骨架
- 问题锚点：怎样用物理模型解释和计算「量子力学初步」中的关键现象？
- ABT：
  - And：你已经掌握了前置知识，能够识别物体、相互作用、运动状态或能量变化等基本线索。
  - But：一到「量子力学初步」综合情境，题目会把文字、图像、公式和实验条件混在一起；如果不先建模，很容易套错公式。
  - Therefore：所以本课围绕「量子力学初步」建立对象—条件—变量—证据的分析链，把真实情境转化为可计算、可解释的物理模型。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-quantum-intro`
- `python3 scripts/validate-courseware.py phy-h-quantum-intro`
- `python3 scripts/rebuild-index.py`
