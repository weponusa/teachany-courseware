# PLAN.md — 化学平衡：反应停止了吗？其实没有

- course_id: `chem-h-chemical-equilibrium`
- node_id: `chem-h-chemical-equilibrium`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：化学平衡
- 课标摘录：认识化学变化有一定限度、速率，是可以调控的。能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；能用对立统一、联系发展和动态平衡的观点考察化学反应，预测在一定条件下某种物质可能发生的化学变化。；选择性必修课程设置3个模块，包括“化学反应原理”模块。

## Phase 1 教学骨架
- 问题锚点：为什么化学平衡是“动态平衡”，而不是反应完全停止？
- ABT：
  - And：你已经知道可逆反应中正反应和逆反应可以同时发生，也理解反应速率会随条件改变。
  - But：当宏观看起来浓度不再变化时，很多同学以为反应停止了；实际上微观上正逆反应仍在持续进行。
  - Therefore：所以要理解化学平衡的动态本质：一定条件下 v正 = v逆，各组分浓度保持不变但反应没有停止。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-chemical-equilibrium`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
