# PLAN.md — 功与功率：从真实情境到物理模型

- course_id: `phy-h-work-concept`
- node_id: `phy-h-work-concept`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：功与功率
- 课标摘录：理解功和功率。了解生产生活中常见机械的功率大小及其意义。；分析物体移动的方向与所受力的方向不在一条直线上时，该力所做的功。；分析汽车发动机的功率一定时，牵引力与速度的关系。

## Phase 1 教学骨架
- 问题锚点：怎样用物理模型解释和计算「功与功率」中的关键现象？
- ABT：
  - And：你已经掌握了前置知识，能够识别物体、相互作用、运动状态或能量变化等基本线索。
  - But：一到「功与功率」综合情境，题目会把文字、图像、公式和实验条件混在一起；如果不先建模，很容易套错公式。
  - Therefore：所以本课围绕「功与功率」建立对象—条件—变量—证据的分析链，把真实情境转化为可计算、可解释的物理模型。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-work-concept`
- `python3 scripts/validate-courseware.py phy-h-work-concept`
- `python3 scripts/rebuild-index.py`
