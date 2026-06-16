# PLAN.md — 分子结构与性质：形状怎样改变物质表现？

- course_id: `chem-h-molecular-structure`
- node_id: `chem-h-molecular-structure`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：分子结构与性质
- 课标摘录：认识化学是在原子、分子水平上研究物质的组成、结构、性质、转化及其应用的一门基础学科，其特征是认识物质和创造物质。；能从元素和原子、分子水平认识物质的组成、结构、性质和变化，形成“结构决定性质”的观念。；能认识化学现象与模型之间的联系，能运用多种认知模型来描述和解释物质的结构、性质和变化。

## Phase 1 教学骨架
- 问题锚点：为什么相同元素种类或相似化学键，也可能因为空间形状不同而性质不同？
- ABT：
  - And：你已经知道原子可通过共价键组成分子，也知道化学键有极性。
  - But：只知道有几个键仍不够。CO₂ 和 H₂O 都含氧，但 CO₂ 是直线形、H₂O 是折线形，极性和性质明显不同。
  - Therefore：所以要用电子域、孤电子对、空间构型和分子极性解释分子结构与宏观性质的关系。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-molecular-structure`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
