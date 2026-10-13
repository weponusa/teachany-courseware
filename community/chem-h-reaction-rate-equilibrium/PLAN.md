# PLAN.md — 速率与平衡综合：工业条件为什么要折中？

- course_id: `chem-h-reaction-rate-equilibrium`
- node_id: `chem-h-reaction-rate-equilibrium`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：速率与平衡综合
- 课标摘录：认识化学变化有一定限度、速率，是可以调控的。能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；能用对立统一、联系发展和动态平衡的观点考察化学反应，预测在一定条件下某种物质可能发生的化学变化。；选择性必修课程依据化学学科的基础性研究领域，设置“化学反应原理”模块。

## Phase 1 教学骨架
- 问题锚点：为什么合成氨不用无限高压、无限低温，而要选择合适条件？
- ABT：
  - And：你已经分别学习了反应速率和化学平衡，知道温度、压强、催化剂等条件会影响反应过程。
  - But：工业生产不是只追求“快”，也不是只追求“平衡产率高”。有些条件提高速率却降低产率，有些条件提高产率却成本太高。
  - Therefore：所以要把速率、平衡、成本、安全放在同一个决策框架里，理解工业反应条件为什么常常选择折中方案。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-reaction-rate-equilibrium`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
