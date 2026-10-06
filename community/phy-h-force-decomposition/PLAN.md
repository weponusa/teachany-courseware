# PLAN.md — 力的合成与分解：把一个力换成等效分量

- course_id: `phy-h-force-decomposition`
- node_id: `phy-h-force-decomposition`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：力的合成与分解
- 课标摘录：通过实验，了解力的合成与分解，知道矢量和标量。能用共点力的平衡条件分析生产生活中的问题。；能对物体的受力和运动情况进行分析，得出结论。能从物理学的运动与相互作用的视角分析自然与生活中的有关简单问题。

## Phase 1 教学骨架
- 问题锚点：为什么斜向上的拉力，既能向前拉动物体，也能减小地面对物体的压力？
- ABT：
  - And：你已经能识别重力、弹力、摩擦力，也知道力有大小和方向。
  - But：斜面、吊桥、拉索等场景中，力不总沿坐标轴方向。直接用力的大小计算，会忽略方向贡献。
  - Therefore：所以要用矢量平行四边形法则，把力合成或分解到方便分析的方向。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-force-decomposition`
- `python3 scripts/validate-courseware.py phy-h-force-decomposition`
- `python3 scripts/rebuild-index.py`
