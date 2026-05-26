# PLAN.md — 有机化合物入门：先抓碳骨架和官能团

- course_id: `chem-h-organic-intro`
- node_id: `chem-h-organic-intro`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：有机化合物入门
- 课标摘录：在选择性必修课程中，依据化学学科的基础性研究领域，设置“化学反应原理”“物质结构与性质”“有机化学基础”3个模块。；选择性必修课程包括3个模块，每个模块2学分，共6学分。

## Phase 1 教学骨架
- 问题锚点：为什么有机化学入门不能先背名字，而要先看碳骨架和官能团？
- ABT：
  - And：你已经学习化学键、分子结构和元素周期表，知道碳能形成稳定共价键。
  - But：有机物种类极多，若逐个背名称会很快混乱；真正的入口是看碳骨架和官能团。
  - Therefore：所以要建立有机化合物的两层视角：碳链/碳环决定骨架，官能团决定典型性质和反应类型。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-organic-intro`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
