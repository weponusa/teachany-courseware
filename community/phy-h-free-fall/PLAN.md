# PLAN.md — 自由落体运动：只受重力时怎样下落？

- course_id: `phy-h-free-fall`
- node_id: `phy-h-free-fall`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：自由落体运动
- 课标摘录：通过实验，认识自由落体运动规律。结合物理学史的相关内容，认识物理实验与科学推理在物理学研究中的作用。；查阅资料，了解伽利略研究自由落体运动的实验和推理方法。；观察质量相同、大小和形状不同的物体在空气中下落的现象，了解空气阻力对落体运动的影响。

## Phase 1 教学骨架
- 问题锚点：为什么在真空中，轻重不同的物体会同时落地？
- ABT：
  - And：你已经学习匀变速直线运动，知道初速度、加速度和位移之间的关系。
  - But：生活中纸片和石头下落不同，容易让人误以为重物一定下落更快；但空气阻力会干扰我们看到的现象。
  - Therefore：所以要在“只受重力、忽略空气阻力”的理想条件下研究自由落体，理解 g 和运动公式。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-free-fall`
- `python3 scripts/validate-courseware.py phy-h-free-fall`
- `python3 scripts/rebuild-index.py`
