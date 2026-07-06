# PLAN.md — 铁及其化合物：Fe²⁺ 与 Fe³⁺ 的转化证据链

- course_id: `chem-h-iron-compounds`
- node_id: `chem-h-iron-compounds`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：铁及其化合物
- 课标摘录：结合真实情境中的应用实例或通过实验探究，了解钠、铁及其重要化合物的主要性质，了解这些物质在生产、生活中的应用。；铁及其化合物的性质实验；氢氧化亚铁的制备；

## Phase 1 教学骨架
- 问题锚点：怎样用颜色、沉淀和价态变化判断铁元素处在哪一种状态？
- ABT：
  - And：你已经理解金属活动性、离子反应和氧化还原配平，也知道铁在生产生活中极其常见。
  - But：铁不是只有“生锈”这一种现象。Fe、Fe²⁺、Fe³⁺之间能相互转化，不同价态的沉淀颜色和检验方法也不同。
  - Therefore：所以要用价态转化和特征反应建立铁及其化合物的证据链，解释制备、检验和腐蚀防护。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-iron-compounds`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
