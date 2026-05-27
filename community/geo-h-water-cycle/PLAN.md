# PLAN.md — 水循环：从空间格局到成因机制

- course_id: `geo-h-water-cycle`
- node_id: `geo-h-water-cycle`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / geography-map-lab

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：地理
- 课标节点：水循环
- 课标摘录：运用示意图，说明水循环的过程及其地理意义。；能够运用地球科学的基础知识，说明一些自然现象之间的关系和变化过程（综合思维）。；以认识自然地理要素及其与人类活动的关系为线索组织教学。

## Phase 1 教学骨架
- 问题锚点：怎样用地图、图表和过程证据解释水循环的空间格局与成因？
- ABT：
  - And：你已经能在地图或材料中看到水循环相关的现象，比如位置差异、区域分布或时间变化。
  - But：高质量地理分析不能只描述“哪里多、哪里少”，还要解释为什么这样分布、条件改变后会怎样变化。
  - Therefore：所以本课要用“定位—读图—找因果—评估人地影响”的路径，建立水循环的可迁移分析方法。
- 真实互动：地图图层 Canvas + 投影变形提示 + 前后测反馈
- 评估闭环：前测 → 读图检查表 → 概念拆解 → 地图互动 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 地理互动：使用地图图层 Canvas，显式提示等距圆柱投影高纬面积变形。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/geo-h-water-cycle`
- `python3 scripts/validate-courseware.py geo-h-water-cycle`
- `python3 scripts/rebuild-index.py`
