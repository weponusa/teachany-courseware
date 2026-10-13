# PLAN.md — 官能团：醇酚醛酸酯的性质开关

- course_id: `chem-h-functional-groups`
- node_id: `chem-h-functional-groups`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：官能团（醇/酚/醛/酸/酯）
- 课标摘录：高中11年级学段目标：理解并掌握「官能团（醇/酚/醛/酸/酯）」的基本概念与方法；学业要求：能在真实情境中识别、运用「官能团（醇/酚/醛/酸/酯）」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「官能团（醇/酚/醛/酸/酯）」的理解

## Phase 1 教学骨架
- 问题锚点：为什么换一个官能团，有机物的性质就会大变？
- ABT：
  - And：你已经知道有机物的性质不能只看碳骨架，还要看官能团。
  - But：-OH、-CHO、-COOH、-COOR 看起来只是几个原子团，却决定了完全不同的酸性、氧化性、酯化和水解行为。
  - Therefore：所以要把官能团当作有机物的“性质开关”，用结构预测反应类型和实验现象。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-functional-groups`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
