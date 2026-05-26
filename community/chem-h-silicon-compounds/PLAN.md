# PLAN.md — 硅及其化合物：从石英到玻璃的网络结构

- course_id: `chem-h-silicon-compounds`
- node_id: `chem-h-silicon-compounds`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：硅及其化合物
- 课标摘录：结合真实情境中的应用实例或通过实验探究，了解氯、氮、硫及其重要化合物的主要性质，认识这些物质在生产中的应用和对生态环境的影响。；认识元素可以组成不同种类的物质，根据物质的组成和性质可以对物质进行分类；同类物质具有相似的性质，一定条件下各类物质可以相互转化。；紧密联系生产和生活实际，创设丰富多样的真实问题情境。

## Phase 1 教学骨架
- 问题锚点：为什么同样含硅，石英、玻璃、硅酸盐和晶体硅会表现出不同材料性质？
- ABT：
  - And：你已经知道氧化物、盐和化学键的基本概念，也见过玻璃、陶瓷、水泥、芯片等含硅材料。
  - But：硅材料看起来普通，却有高熔点、耐腐蚀、绝缘或半导体等差异巨大性质；只背化学式解释不了这些性能。
  - Therefore：所以要从 Si-O 网络结构、硅酸盐骨架和材料应用出发，理解结构怎样决定性质和用途。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-silicon-compounds`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
