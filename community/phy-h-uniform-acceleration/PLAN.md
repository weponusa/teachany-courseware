# PLAN.md — 匀变速直线运动：三条公式背后的图像逻辑

- course_id: `phy-h-uniform-acceleration`
- node_id: `phy-h-uniform-acceleration`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：匀变速直线运动
- 课标摘录：通过实验，探究匀变速直线运动的特点，能用公式、图像等方法描述匀变速直线运动，理解匀变速直线运动的规律，能运用其解决实际问题。；能用位移、速度、加速度等物理量描述物体的直线运动，能用匀变速直线运动的规律解释或解决生活中的具体问题。；用打点计时器、频闪照相或其他实验工具研究匀变速直线运动的规律。

## Phase 1 教学骨架
- 问题锚点：为什么匀变速直线运动的位移公式里会出现 1/2at²？
- ABT：
  - And：你已经会从 v-t 图像看速度变化，也知道加速度表示速度变化快慢。
  - But：匀变速公式很多，如果只背 v=v₀+at、x=v₀t+1/2at²、v²-v₀²=2ax，很容易乱套条件。
  - Therefore：所以要从“加速度恒定”这个核心条件出发，用图像面积和斜率推导公式，再按已知量选择公式。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-uniform-acceleration`
- `python3 scripts/validate-courseware.py phy-h-uniform-acceleration`
- `python3 scripts/rebuild-index.py`
