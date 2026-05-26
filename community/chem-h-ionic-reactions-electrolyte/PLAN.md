# PLAN.md — 电解质与离子反应综合：谁真的参加了反应？

- course_id: `chem-h-ionic-reactions-electrolyte`
- node_id: `chem-h-ionic-reactions-electrolyte`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：电解质与离子反应综合
- 课标摘录：认识酸、碱、盐等电解质在水溶液中或熔融状态下能发生电离。；通过实验事实认识离子反应及其发生的条件，了解常见离子的检验方法。；实验及探究活动：电解质的电离；探究溶液中离子反应的实质及发生条件（测定电流或溶液电导率的变化）。

## Phase 1 教学骨架
- 问题锚点：两种溶液混合后，怎样判断哪些离子真的反应了，哪些只是旁观？
- ABT：
  - And：你已经知道酸、碱、盐溶于水后可能导电，也见过沉淀、气体或水生成的反应现象。
  - But：把两个溶液混合时，烧杯里有很多离子，但并不是每个离子都真的参加反应；有些离子只是旁观者。
  - Therefore：所以要从电解质电离出发，识别沉淀、气体、弱电解质等真正驱动力，判断离子反应能否发生。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-ionic-reactions-electrolyte`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
