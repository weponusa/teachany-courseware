# PLAN.md — 城市化：从空间格局到成因机制

- course_id: `geo-h-urbanization`
- node_id: `geo-h-urbanization`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / geography-map-lab

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：地理
- 课标节点：城市化
- 课标摘录：运用资料，说明不同地区城镇化的过程和特点，以及城镇化的利弊。；以某大都市为例，从区域空间组织的视角出发，说明大都市辐射功能。；结合实例，解释城镇和乡村内部的空间结构，说明合理利用城乡空间的意义。

## Phase 1 教学骨架
- 问题锚点：怎样用地图、图表和过程证据解释城市化的空间格局与成因？
- ABT：
  - And：你已经能在地图或材料中看到城市化相关的现象，比如位置差异、区域分布或时间变化。
  - But：高质量地理分析不能只描述“哪里多、哪里少”，还要解释为什么这样分布、条件改变后会怎样变化。
  - Therefore：所以本课要用“定位—读图—找因果—评估人地影响”的路径，建立城市化的可迁移分析方法。
- 真实互动：地图图层 Canvas + 投影变形提示 + 前后测反馈
- 评估闭环：前测 → 读图检查表 → 概念拆解 → 地图互动 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 地理互动：使用地图图层 Canvas，显式提示等距圆柱投影高纬面积变形。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/geo-h-urbanization`
- `python3 scripts/validate-courseware.py geo-h-urbanization`
- `python3 scripts/rebuild-index.py`
