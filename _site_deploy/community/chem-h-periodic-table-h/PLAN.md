# PLAN.md — 元素周期表：用位置预测元素性质

- course_id: `chem-h-periodic-table-h`
- node_id: `chem-h-periodic-table-h`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：元素周期表
- 课标摘录：认识元素可以组成不同种类的物质，根据物质的组成和性质可以对物质进行分类；同类物质具有相似的性质。；能从元素和原子、分子水平认识物质的组成、结构、性质和变化，形成“结构决定性质”的观念。

## Phase 1 教学骨架
- 问题锚点：看到一个元素在周期表中的位置，怎样推断它大概会怎样反应？
- ABT：
  - And：你已经学过原子结构和元素周期律，知道原子序数、电子层和最外层电子会影响性质。
  - But：如果只背每个元素的单独性质，周期表会变成密密麻麻的表格；真正有用的是用位置预测性质。
  - Therefore：所以要把周期、族、分区和性质递变连起来，学会从元素位置推断电子排布、金属性和非金属性。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-periodic-table-h`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
