# PLAN.md — 农业区位因素：从空间格局到成因机制

- course_id: `geo-h-agriculture-location`
- node_id: `geo-h-agriculture-location`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / geography-map-lab

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：地理
- 课标节点：农业区位因素
- 课标摘录：结合实例，说明工业、农业和服务业的区位因素。；能够描述人文地理事物的空间现象及其变化，解释不同地方的人们对产业活动进行区位选择的依据（综合思维、区域认知）。；采用案例学习的方法，具体分析体现人类活动与自然环境关系的典型实例，帮助学生理解...掌握分析人文地理问题的思路和方法。

## Phase 1 教学骨架
- 问题锚点：怎样用地图、图表和过程证据解释农业区位因素的空间格局与成因？
- ABT：
  - And：你已经能在地图或材料中看到农业区位因素相关的现象，比如位置差异、区域分布或时间变化。
  - But：高质量地理分析不能只描述“哪里多、哪里少”，还要解释为什么这样分布、条件改变后会怎样变化。
  - Therefore：所以本课要用“定位—读图—找因果—评估人地影响”的路径，建立农业区位因素的可迁移分析方法。
- 真实互动：地图图层 Canvas + 投影变形提示 + 前后测反馈
- 评估闭环：前测 → 读图检查表 → 概念拆解 → 地图互动 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 地理互动：使用地图图层 Canvas，显式提示等距圆柱投影高纬面积变形。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/geo-h-agriculture-location`
- `python3 scripts/validate-courseware.py geo-h-agriculture-location`
- `python3 scripts/rebuild-index.py`
