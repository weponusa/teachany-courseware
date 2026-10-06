# PLAN.md — 烃的衍生物：骨架不变，性质因官能团而变

- course_id: `chem-h-organic-derivatives`
- node_id: `chem-h-organic-derivatives`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：烃的衍生物
- 课标摘录：在选择性必修课程中，依据化学学科的基础性研究领域，设置“化学反应原理”“物质结构与性质”“有机化学基础”3个模块。；选择性必修课程设置3个模块。

## Phase 1 教学骨架
- 问题锚点：怎样从官能团角度把一串烃的衍生物串成反应网络？
- ABT：
  - And：你已经学习烃和官能团，知道在碳骨架上引入不同原子团会改变性质。
  - But：卤代烃、醇、醛、羧酸、酯之间既有联系又能相互转化，孤立记忆会割裂知识。
  - Therefore：所以要把烃的衍生物看成“碳骨架 + 官能团”的组合，并用官能团转化理解反应网络。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-organic-derivatives`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
