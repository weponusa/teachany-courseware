# PLAN.md — 离子方程式：把化学反应写成真正发生的净变化

- course_id: `chem-h-ionic-equation`
- node_id: `chem-h-ionic-equation`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 10 年级
- 学科：化学
- 课标节点：离子方程式
- 课标摘录：认识酸、碱、盐等电解质在水溶液中或熔融状态下能发生电离。；通过实验事实认识离子反应及其发生的条件，了解常见离子的检验方法。

## Phase 1 教学骨架
- 问题锚点：怎样从完整化学方程式一步步得到正确的净离子方程式？
- ABT：
  - And：你已经会写化学方程式，也知道可溶强电解质在水中主要以离子形式存在。
  - But：普通化学方程式常把旁观离子也写进去，看不出反应本质；跳步写净离子式又容易漏配平和漏电荷。
  - Therefore：所以要按“写化学方程式—拆强电解质—删旁观离子—查守恒”的流程写离子方程式。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-ionic-equation`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
