# PLAN.md — 离子检验与共存：用证据判断溶液里有什么

- course_id: `chem-h-ion-identification`
- node_id: `chem-h-ion-identification`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：离子检验与共存
- 课标摘录：通过实验事实认识离子反应及其发生的条件，了解常见离子的检验方法。；能根据物质的特征反应和干扰因素选取适当的检验试剂。；常见离子的检验方法（如补铁剂中的铁元素）。

## Phase 1 教学骨架
- 问题锚点：看到一个实验现象时，怎样把它变成可靠的离子证据，而不是猜测？
- ABT：
  - And：你已经知道某些离子相遇会生成沉淀、气体或水，也会写对应的净离子方程式。
  - But：真实实验里，未知溶液可能同时含多种离子；一个白色沉淀不一定只对应一种离子，检验顺序和干扰离子都会影响判断。
  - Therefore：所以要建立“试剂—现象—离子—排除干扰”的证据链，并用反应条件判断离子能否大量共存。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-ion-identification`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
