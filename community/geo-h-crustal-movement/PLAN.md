# PLAN.md — 地壳运动：从空间格局到成因机制

- course_id: `geo-h-crustal-movement`
- node_id: `geo-h-crustal-movement`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / geography-map-lab

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：地理
- 课标节点：地壳运动
- 课标摘录：结合实例，解释内力和外力对地表形态变化的影响，并说明人类活动与地表形态的关系。；运用示意图，说明岩石圈物质循环过程。；以自然环境系统及其要素发展、演变过程对人类活动的影响为线索组织教学。

## Phase 1 教学骨架
- 问题锚点：怎样用地图、图表和过程证据解释地壳运动的空间格局与成因？
- ABT：
  - And：你已经能在地图或材料中看到地壳运动相关的现象，比如位置差异、区域分布或时间变化。
  - But：高质量地理分析不能只描述“哪里多、哪里少”，还要解释为什么这样分布、条件改变后会怎样变化。
  - Therefore：所以本课要用“定位—读图—找因果—评估人地影响”的路径，建立地壳运动的可迁移分析方法。
- 真实互动：地图图层 Canvas + 投影变形提示 + 前后测反馈
- 评估闭环：前测 → 读图检查表 → 概念拆解 → 地图互动 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 地理互动：使用地图图层 Canvas，显式提示等距圆柱投影高纬面积变形。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/geo-h-crustal-movement`
- `python3 scripts/validate-courseware.py geo-h-crustal-movement`
- `python3 scripts/rebuild-index.py`
