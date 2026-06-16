# PLAN.md — 化学键：原子为什么要连在一起？

- course_id: `chem-h-chemical-bond`
- node_id: `chem-h-chemical-bond`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：化学键
- 课标摘录：认识化学是在原子、分子水平上研究物质的组成、结构、性质、转化及其应用的一门基础学科。；能从元素和原子、分子水平认识物质的组成、结构、性质和变化，形成“结构决定性质”的观念。

## Phase 1 教学骨架
- 问题锚点：怎样从原子得失电子或共用电子判断物质中是什么化学键？
- ABT：
  - And：你已经知道原子有最外层电子，也知道元素会形成离子、分子或晶体。
  - But：物质性质差异巨大：NaCl 是晶体，HCl 是分子，O₂ 是气体。只看元素名称还不够，关键在原子之间如何连接。
  - Therefore：所以要学习离子键、共价键和键的极性，用电子转移或共用解释物质结构与性质。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-chemical-bond`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
