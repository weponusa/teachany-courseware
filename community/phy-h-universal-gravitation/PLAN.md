# PLAN.md — 万有引力定律：从苹果到行星的同一规律

- course_id: `phy-h-universal-gravitation`
- node_id: `phy-h-universal-gravitation`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：物理
- 课标节点：万有引力定律
- 课标摘录：通过史实，了解万有引力定律的发现过程。知道万有引力定律。认识发现万有引力定律的重要意义。；以万有引力定律为例，了解统一性观念在科学认识中的重要意义。；会计算人造地球卫星的环绕速度。知道第二宇宙速度和第三宇宙速度。

## Phase 1 教学骨架
- 问题锚点：为什么距离变为 2 倍时，万有引力会变为原来的 1/4？
- ABT：
  - And：你已经学习牛顿运动定律和圆周运动，知道合力可以提供向心加速度。
  - But：地面物体下落和月球绕地球运动看起来完全不同，牛顿的关键洞见是它们可能由同一种引力规律解释。
  - Therefore：所以要学习万有引力定律 F=Gm₁m₂/r²，并用它解释天体运动和卫星环绕。
- 真实互动：Canvas 变量实验 + PhET/本地模型 + 前后测反馈
- 评估闭环：前测 → 概念拆解 → 例题拆解 → 互动实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 物理仿真：按课题使用 Canvas + PhET/成熟资源，未使用外部资源的课件由本地 Canvas 完成核心互动。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/phy-h-universal-gravitation`
- `python3 scripts/validate-courseware.py phy-h-universal-gravitation`
- `python3 scripts/rebuild-index.py`
