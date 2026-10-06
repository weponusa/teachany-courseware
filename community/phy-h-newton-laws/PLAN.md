# PLAN.md — 牛顿运动定律：合力如何决定加速度

- course_id: `phy-h-newton-laws`
- node_id: `phy-h-newton-laws`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：牛顿运动定律
- 课标摘录：通过实验，探究物体运动的加速度与物体受力、物体质量的关系。理解牛顿运动定律，能用牛顿运动定律解释生产生活中的有关现象、解决有关问题。；能对物体的受力和运动情况进行分析，得出结论。能从物理学的运动与相互作用的视角分析自然与生活中的有关简单问题。；通过探究物体间相互作用与运动状态变化的关系等实验，引导学生运用控制变量等研究方法设计实验方案，学会分析和处理实验数据的方法，提高科学探究能力。

## Phase 1 教学骨架
- 问题锚点：为什么同样的推力推空车和满载车，加速度不同？
- ABT：
  - And：你已经会分析常见力，也能把力分解到运动方向。
  - But：物体受力不一定马上沿力的方向移动；真正直接对应的是合力和加速度，而不是速度。
  - Therefore：所以要理解牛顿三定律，尤其用 F合=ma 连接受力分析和运动变化。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-newton-laws`
- `python3 scripts/validate-courseware.py phy-h-newton-laws`
- `python3 scripts/rebuild-index.py`
