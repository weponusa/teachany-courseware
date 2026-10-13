# PLAN.md — 元素周期律：把零散元素排成可预测的地图

- course_id: `chem-h-periodic-law`
- node_id: `chem-h-periodic-law`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：元素周期律
- 课标摘录：主题1：化学科学与实验探究【教学提示】情境素材建议：有关化学发现的故事：元素周期律的发展等。；素养1 宏观辨识与微观探析：能从元素和原子、分子水平认识物质的组成、结构、性质和变化，形成“结构决定性质”的观念。；课程目标1：能从物质的微观层面理解其组成、结构和性质的联系，形成“结构决定性质，性质决定应用”的观念。

## Phase 1 教学骨架
- 问题锚点：怎样不用死记硬背，也能根据元素在周期表中的位置预测它的性质？
- ABT：
  - And：你已经理解原子结构和核外电子排布，知道元素性质与最外层电子有关。
  - But：如果每个元素都孤立记忆，元素越多越混乱；但门捷列夫发现元素性质会随着原子序数递增呈周期性变化。
  - Therefore：所以要学习元素周期律，用周期、族、原子半径、金属性和非金属性趋势预测元素性质。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-periodic-law`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
