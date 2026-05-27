# PLAN.md — 描写方法与细节：从文本证据到表达效果

- course_id: `chn-m-descriptive-writing`
- node_id: `chn-m-descriptive-writing`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 7 年级
- 学科：语文
- 课标节点：描写方法与细节
- 课标摘录：阅读表现人与自然的优秀文学作品，体会作者通过语言和形象构建的艺术世界，借鉴其中的写作手法。；阅读表现人与社会、人与他人的古今优秀文学作品，学习欣赏、品味作品的语言、形象等，交流审美体验。；能按照童话、寓言等文体样式，运用联想、想象续编或续写故事。

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释描写方法与细节中的表达效果与思想情感？
- ABT：
  - And：你已经接触过描写方法与细节相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握描写方法与细节。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-descriptive-writing`
- `python3 scripts/validate-courseware.py chn-m-descriptive-writing`
- `python3 scripts/rebuild-index.py`
