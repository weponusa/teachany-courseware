# PLAN.md — 高分子合成与应用：从单体到材料性能

- course_id: `chem-h-polymers`
- node_id: `chem-h-polymers`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：高分子合成与应用
- 课标摘录：高中11年级学段目标：理解并掌握「高分子合成与应用」的基本概念与方法；学业要求：能在真实情境中识别、运用「高分子合成与应用」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「高分子合成与应用」的理解

## Phase 1 教学骨架
- 问题锚点：为什么不同单体和聚合方式会得到性能完全不同的高分子材料？
- ABT：
  - And：你已经了解有机小分子、官能团和有机反应类型，也知道小分子可以连接成长链。
  - But：塑料、橡胶、纤维性质差别很大，不能只用“都是高分子”概括；聚合方式、单体结构和链间作用会决定材料性能。
  - Therefore：所以要学习加聚、缩聚和高分子结构，用单体—链结构—性能—应用的路径理解材料。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-polymers`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
