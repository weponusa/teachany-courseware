# PLAN.md — 化学反应速率：怎样让反应快起来或慢下来？

- course_id: `chem-h-reaction-rate`
- node_id: `chem-h-reaction-rate`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：化学反应速率
- 课标摘录：认识化学变化有一定限度、速率，是可以调控的。能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；能从内因与外因、量变与质变等方面较全面地分析物质的化学变化，关注化学变化中的能量转化；能用对立统一、联系发展和动态平衡的观点考察化学反应。

## Phase 1 教学骨架
- 问题锚点：改变浓度、温度和催化剂时，为什么反应速率会改变？
- ABT：
  - And：你已经知道化学反应会发生能量变化，也知道反应需要粒子碰撞。
  - But：同一个反应在不同条件下速度差别很大：铁生锈很慢，燃烧很快，工业反应还要兼顾效率和安全。
  - Therefore：所以要用浓度、温度、压强、催化剂和接触面积解释反应速率，并用有效碰撞模型理解原因。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-reaction-rate`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
