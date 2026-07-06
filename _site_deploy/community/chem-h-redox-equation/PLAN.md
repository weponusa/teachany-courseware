# PLAN.md — 氧化还原方程式配平：用电子守恒抓住反应骨架

- course_id: `chem-h-redox-equation`
- node_id: `chem-h-redox-equation`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：氧化还原方程式配平
- 课标摘录：认识有化合价变化的反应是氧化还原反应，了解氧化还原反应的本质是电子的转移，知道常见的氧化剂和还原剂。；氧化还原反应本质的探究；过氧化氢的氧化性、还原性的探究；

## Phase 1 教学骨架
- 问题锚点：为什么氧化还原方程式配平的核心不是试凑，而是“失电子=得电子”？
- ABT：
  - And：你已经理解氧化还原反应中有化合价变化，也知道氧化剂得电子、还原剂失电子。
  - But：复杂反应里元素多、系数多，单靠试凑容易乱；如果电子数不守恒，方程式即使元素看似配平也不可靠。
  - Therefore：所以要用化合价升降法：标价态、列升降、求最小公倍数、配系数，再检查原子和电荷。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-redox-equation`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
