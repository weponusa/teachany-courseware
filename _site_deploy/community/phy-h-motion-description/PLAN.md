# PLAN.md — 运动的描述：先选参考系，再谈位置和速度

- course_id: `phy-h-motion-description`
- node_id: `phy-h-motion-description`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：运动的描述
- 课标摘录：理解位移、速度和加速度。通过实验，探究匀变速直线运动的特点，能用公式、图像等方法描述匀变速直线运动。；能用位移、速度、加速度等物理量描述物体的直线运动，能用匀变速直线运动的规律解释或解决生活中的具体问题。；通过瞬时速度和加速度概念的建构，体会物理问题研究中的极限方法和抽象思维方法。

## Phase 1 教学骨架
- 问题锚点：为什么讨论运动前必须先问“相对于谁在运动”？
- ABT：
  - And：你已经能用生活语言说一个物体在动，比如汽车前进、同学跑步、列车驶离站台。
  - But：同一个人坐在车里看自己是静止的，站台上的人看他在运动；如果不先约定参考系，运动描述会互相矛盾。
  - Therefore：所以要用参考系、质点、位置、位移、速度和加速度建立一套可测量的运动语言。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-motion-description`
- `python3 scripts/validate-courseware.py phy-h-motion-description`
- `python3 scripts/rebuild-index.py`
