# PLAN.md — 烃类综合：从结构到反应类型的快速判断

- course_id: `chem-h-hydrocarbons`
- node_id: `chem-h-hydrocarbons`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：烃类综合
- 课标摘录：高中11年级学段目标：理解并掌握「烃类综合」的基本概念与方法；学业要求：能在真实情境中识别、运用「烃类综合」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「烃类综合」的理解

## Phase 1 教学骨架
- 问题锚点：拿到一个未知烃，怎样用结构和实验现象判断它是哪一类？
- ABT：
  - And：你已经分别学习烷烃、烯烃、炔烃和芳香烃，知道它们的键类型不同。
  - But：综合题常把燃烧、取代、加成、同分异构和实验鉴别放在一起，只背单个反应很容易混淆。
  - Therefore：所以要建立“结构特征—实验现象—反应类型—方程式”的综合判断链。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-hydrocarbons`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
