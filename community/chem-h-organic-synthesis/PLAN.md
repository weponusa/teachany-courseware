# PLAN.md — 有机合成路线设计：从目标倒推反应路径

- course_id: `chem-h-organic-synthesis`
- node_id: `chem-h-organic-synthesis`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：有机合成路线设计
- 课标摘录：在选择性必修课程中，依据化学学科的基础性研究领域，设置“化学反应原理”“物质结构与性质”“有机化学基础”3个模块。；选择性必修课程包括3个模块，每个模块2学分，共6学分。

## Phase 1 教学骨架
- 问题锚点：怎样从目标产物倒推到可行原料，再正向写出合成路线？
- ABT：
  - And：你已经学过官能团、烃的衍生物和常见有机反应类型。
  - But：合成题不是单步反应，而是从原料到目标产物的多步路线；如果只会背单个反应，很难设计路径。
  - Therefore：所以要学会逆合成思维：先看目标官能团，再倒推可由什么前体转化而来，最后正向验证条件和副产物。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-organic-synthesis`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
