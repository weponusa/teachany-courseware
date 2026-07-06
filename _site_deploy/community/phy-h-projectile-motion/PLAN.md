# PLAN.md — 抛体运动：把弯曲轨迹拆成两个直线运动

- course_id: `phy-h-projectile-motion`
- node_id: `phy-h-projectile-motion`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：抛体运动
- 课标摘录：通过实验，探究并认识平抛运动的规律。会用运动合成与分解的方法分析平抛运动。；体会将复杂运动分解为简单运动的物理思想。能分析生产生活中的抛体运动。

## Phase 1 教学骨架
- 问题锚点：为什么抛体运动轨迹是曲线，却可以分解成两个方向分别计算？
- ABT：
  - And：你已经会处理匀变速直线运动，也知道矢量可以分解。
  - But：抛体轨迹是曲线，看起来很复杂；如果直接沿轨迹分析，会很难写出运动关系。
  - Therefore：所以要用运动合成与分解，把抛体运动拆成水平方向匀速和竖直方向匀变速。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-projectile-motion`
- `python3 scripts/validate-courseware.py phy-h-projectile-motion`
- `python3 scripts/rebuild-index.py`
