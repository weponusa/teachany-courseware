# PLAN.md — 直线运动综合：用图像把运动过程看清楚

- course_id: `phy-h-kinematics-linear`
- node_id: `phy-h-kinematics-linear`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：直线运动综合
- 课标摘录：理解位移、速度和加速度。通过实验，探究匀变速直线运动的特点，能用公式、图像等方法描述匀变速直线运动。；能用位移、速度、加速度等物理量描述物体的直线运动，能用匀变速直线运动的规律解释或解决生活中的具体问题。；通过瞬时速度和加速度概念的建构，体会物理问题研究中的极限方法和抽象思维方法。

## Phase 1 教学骨架
- 问题锚点：怎样从一张 v-t 图像直接读出速度变化、位移和加速度？
- ABT：
  - And：你已经知道速度、位移和加速度的基本含义，也能读懂简单的时间记录。
  - But：真实题目常同时给文字、表格和图像。只盯公式会漏掉图像斜率、面积和分段运动信息。
  - Therefore：所以要把 x-t、v-t 图像和运动过程联系起来，用斜率、面积和分段分析解决直线运动问题。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-kinematics-linear`
- `python3 scripts/validate-courseware.py phy-h-kinematics-linear`
- `python3 scripts/rebuild-index.py`
