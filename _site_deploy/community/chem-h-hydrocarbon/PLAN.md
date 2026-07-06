# PLAN.md — 烃：烷烯炔芳为什么反应性不同？

- course_id: `chem-h-hydrocarbon`
- node_id: `chem-h-hydrocarbon`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：烃（烷/烯/炔/芳）
- 课标摘录：高中11年级学段目标：理解并掌握「烃（烷/烯/炔/芳）」的基本概念与方法；学业要求：能在真实情境中识别、运用「烃（烷/烯/炔/芳）」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「烃（烷/烯/炔/芳）」的理解

## Phase 1 教学骨架
- 问题锚点：为什么乙烯能使溴水褪色，而甲烷通常不能？
- ABT：
  - And：你已经知道有机物要先看碳骨架和官能团，也认识 C-C、C=C、C≡C 等化学键。
  - But：同样只含 C 和 H，甲烷、乙烯、乙炔、苯的结构和反应却完全不同，不能只用元素组成判断。
  - Therefore：所以要按饱和程度和结构特征区分烷烃、烯烃、炔烃和芳香烃，理解取代、加成、燃烧等典型反应。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-hydrocarbon`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
