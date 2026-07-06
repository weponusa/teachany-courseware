# PLAN.md — 电解池：用外电源推动非自发反应

- course_id: `chem-h-electrolysis`
- node_id: `chem-h-electrolysis`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：电解池
- 课标摘录：认识有化合价变化的反应是氧化还原反应，了解氧化还原反应的本质是电子的转移，知道常见的氧化剂和还原剂。；电解质的电离；探究溶液中离子反应的实质及发生条件（测定电流或溶液电导率的变化）。

## Phase 1 教学骨架
- 问题锚点：为什么电解池的阴极发生还原、阳极发生氧化？
- ABT：
  - And：你已经了解原电池能把自发氧化还原反应变成电能，也知道电解质溶液中有可移动离子。
  - But：有些反应不会自发发生，却可以借助外电源强行推动，例如电镀、精炼铜、电解饱和食盐水。
  - Therefore：所以要学习电解池：外电源提供电子流，阴极发生还原，阳极发生氧化，并根据离子放电顺序判断产物。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-electrolysis`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
