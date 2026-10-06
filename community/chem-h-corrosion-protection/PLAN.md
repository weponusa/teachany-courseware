# PLAN.md — 防腐原理与应用：把腐蚀转移或阻断

- course_id: `chem-h-corrosion-protection`
- node_id: `chem-h-corrosion-protection`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：防腐原理与应用
- 课标摘录：认识有化合价变化的反应是氧化还原反应，了解氧化还原反应的本质是电子的转移，知道常见的氧化剂和还原剂。；能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；紧密联系生产和生活实际，创设丰富多样的真实问题情境。

## Phase 1 教学骨架
- 问题锚点：防腐不是让金属永远不反应，而是怎样让氧化反应变慢、转移或被阻断？
- ABT：
  - And：你已经知道金属腐蚀本质是电化学氧化，也比较过水、氧、电解质对腐蚀的影响。
  - But：真实工程不能只说“刷漆”。涂层破损、海水导电、不同金属接触都会改变腐蚀路径，防护方案必须有原理支撑。
  - Therefore：所以要比较隔绝法、牺牲阳极法、外加电流法和材料选择，理解每种防腐方法到底在阻断哪一步。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-corrosion-protection`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
