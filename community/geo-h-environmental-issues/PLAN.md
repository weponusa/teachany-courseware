# PLAN.md — 环境问题：从空间格局到成因机制

- course_id: `geo-h-environmental-issues`
- node_id: `geo-h-environmental-issues`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / geography-map-lab

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：地理
- 课标节点：环境问题
- 课标摘录：运用资料，归纳人类面临的主要环境问题，说明协调人地关系和可持续发展的主要途径及其缘由。；结合实例，说明设立自然保护区对生态安全的意义。；结合实例，说明污染物跨境转移对环境安全的影响。

## Phase 1 教学骨架
- 问题锚点：怎样用地图、图表和过程证据解释环境问题的空间格局与成因？
- ABT：
  - And：你已经能在地图或材料中看到环境问题相关的现象，比如位置差异、区域分布或时间变化。
  - But：高质量地理分析不能只描述“哪里多、哪里少”，还要解释为什么这样分布、条件改变后会怎样变化。
  - Therefore：所以本课要用“定位—读图—找因果—评估人地影响”的路径，建立环境问题的可迁移分析方法。
- 真实互动：地图图层 Canvas + 投影变形提示 + 前后测反馈
- 评估闭环：前测 → 读图检查表 → 概念拆解 → 地图互动 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 地理互动：使用地图图层 Canvas，显式提示等距圆柱投影高纬面积变形。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/geo-h-environmental-issues`
- `python3 scripts/validate-courseware.py geo-h-environmental-issues`
- `python3 scripts/rebuild-index.py`
