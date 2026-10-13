# PLAN.md — 分散系：为什么胶体会让光路显形？

- course_id: `chem-h-dispersion-system`
- node_id: `chem-h-dispersion-system`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：分散系（溶液/胶体）
- 课标摘录：认识胶体是一种常见的分散系。；实验及探究活动：胶体的丁达尔实验；

## Phase 1 教学骨架
- 问题锚点：为什么一束光穿过胶体会出现明亮光路，而穿过真正溶液却看不见？
- ABT：
  - And：你已经知道食盐能溶于水，也见过泥水静置后会沉降。
  - But：牛奶、豆浆、雾这些体系既不像食盐水那样完全透明，也不像泥水那样很快沉降，它们到底处在什么中间状态？
  - Therefore：所以要用分散质粒子大小和稳定性认识溶液、胶体、浊液，并用丁达尔效应识别胶体。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-dispersion-system`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
