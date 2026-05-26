# PLAN.md — 生物大分子：糖、蛋白质、核酸的结构与功能

- course_id: `chem-h-biomolecules`
- node_id: `chem-h-biomolecules`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：生物大分子（糖/蛋白质/核酸）
- 课标摘录：高中11年级学段目标：理解并掌握「生物大分子（糖/蛋白质/核酸）」的基本概念与方法；学业要求：能在真实情境中识别、运用「生物大分子（糖/蛋白质/核酸）」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「生物大分子（糖/蛋白质/核酸）」的理解

## Phase 1 教学骨架
- 问题锚点：为什么糖、蛋白质和核酸都是大分子，却承担完全不同的生命功能？
- ABT：
  - And：你已经学习有机官能团和聚合反应，知道小分子可通过化学键连接成长链。
  - But：糖类、蛋白质、核酸不是普通“大分子”名称，它们由不同单体、不同连接键构成，承担不同生命功能。
  - Therefore：所以要从单体、连接方式和功能三个维度认识生物大分子，理解结构怎样服务生命活动。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-biomolecules`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
