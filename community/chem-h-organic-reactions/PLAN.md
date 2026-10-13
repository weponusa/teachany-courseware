# PLAN.md — 有机反应类型：看断键和成键，而不是背名字

- course_id: `chem-h-organic-reactions`
- node_id: `chem-h-organic-reactions`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：有机反应类型
- 课标摘录：高中11年级学段目标：理解并掌握「有机反应类型」的基本概念与方法；学业要求：能在真实情境中识别、运用「有机反应类型」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「有机反应类型」的理解

## Phase 1 教学骨架
- 问题锚点：判断有机反应类型时，为什么看结构变化比背反应名称更可靠？
- ABT：
  - And：你已经学过烃、官能团和烃的衍生物，见过加成、取代、氧化、酯化等反应。
  - But：综合题不会直接告诉你反应类型，需要从反应物结构、试剂条件和产物变化中判断断了什么键、形成了什么键。
  - Therefore：所以要用“结构变化”识别加成、取代、消去、氧化、还原、水解、酯化等反应类型。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-organic-reactions`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
