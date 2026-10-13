# PLAN.md — 热化学：化学反应里的能量账本

- course_id: `chem-h-thermochemistry`
- node_id: `chem-h-thermochemistry`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：热化学（焓变）
- 课标摘录：认识化学变化的本质特征是有新物质生成，并伴有能量转化；认识化学变化有一定限度、速率，是可以调控的。；关注化学变化中的能量转化；能用对立统一、联系发展和动态平衡的观点考察化学反应，预测在一定条件下某种物质可能发生的化学变化。；选择性必修课程依据化学学科的基础性研究领域，设置“化学反应原理”模块。

## Phase 1 教学骨架
- 问题锚点：怎样用一个能量图判断反应是放热还是吸热？
- ABT：
  - And：你已经知道化学反应会生成新物质，也见过燃烧放热、溶解吸热或放热的现象。
  - But：只说“热”不够精确。反应到底放出多少能量、能不能用于供热或储能，需要可计算的能量账本。
  - Therefore：所以要学习热化学，用反应热和焓变描述反应中的能量转化，并区分放热与吸热。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-thermochemistry`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
