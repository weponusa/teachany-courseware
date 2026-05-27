# PLAN.md — 文言特殊句式：从文本证据到表达效果

- course_id: `chn-m-classical-sentences`
- node_id: `chn-m-classical-sentences`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 8 年级
- 学科：语文
- 课标节点：文言特殊句式
- 课标摘录：能借助工具书阅读浅易文言文。；在理解语句的过程中，体会句号与逗号的不同用法，了解冒号、引号的一般用法。

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释文言特殊句式中的表达效果与思想情感？
- ABT：
  - And：你已经接触过文言特殊句式相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握文言特殊句式。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-classical-sentences`
- `python3 scripts/validate-courseware.py chn-m-classical-sentences`
- `python3 scripts/rebuild-index.py`
