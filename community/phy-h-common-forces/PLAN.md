# PLAN.md — 常见的力：从受力图开始看世界

- course_id: `phy-h-common-forces`
- node_id: `phy-h-common-forces`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：常见的力
- 课标摘录：认识重力、弹力与摩擦力。通过实验，了解胡克定律。知道滑动摩擦和静摩擦现象，能用动摩擦因数计算滑动摩擦力的大小。；能对物体的受力和运动情况进行分析，得出结论。能从物理学的运动与相互作用的视角分析自然与生活中的有关简单问题。

## Phase 1 教学骨架
- 问题锚点：怎样判断一个物体到底受了哪些力，而不是凭感觉乱加力？
- ABT：
  - And：你已经能描述物体运动，也知道运动状态改变往往来自相互作用。
  - But：题目里常把重力、弹力、摩擦力混在一起，如果不先画受力图，就会把不存在的力也算进去。
  - Therefore：所以要认识重力、弹力、摩擦力和胡克定律，用接触、形变和相对运动趋势判断力。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-common-forces`
- `python3 scripts/validate-courseware.py phy-h-common-forces`
- `python3 scripts/rebuild-index.py`
