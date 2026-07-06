# PLAN.md — 物质的分类：从混乱试剂柜到清晰化学地图

- course_id: `chem-h-substance-classification-h`
- node_id: `chem-h-substance-classification-h`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：物质的分类
- 课标摘录：认识元素可以组成不同种类的物质，根据物质的组成和性质可以对物质进行分类。；能从不同层次认识物质的多样性，并对物质进行分类。

## Phase 1 教学骨架
- 问题锚点：拿到一瓶未知物质时，怎样用“组成—性质”两条线把它快速归类？
- ABT：
  - And：你已经见过空气、水、铁粉、食盐水这些常见物质，也知道它们的外观和用途不同。
  - But：如果只靠名称和外观，面对一柜未知试剂很快会混乱：空气是纯净物吗，氧气和氧化铜为什么都带“氧”？
  - Therefore：所以要用组成和性质建立分类地图，把混合物、纯净物、单质、化合物、氧化物、酸、碱、盐放到正确位置。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-substance-classification-h`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
