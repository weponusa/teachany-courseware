# PLAN.md — 散文杂文集：从文本证据到表达效果

- course_id: `chn-m-erta-essay-collection`
- node_id: `chn-m-erta-essay-collection`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：语文
- 课标节点：散文杂文集
- 课标摘录：独立阅读古今中外诗歌集、中长篇小说、散文集等文学名著，如《艾青诗选》。根据阅读进度完成读书笔记，针对作品的语言、形象、主题等方面的话题展开研讨。；阅读表现人与社会、人与他人的古今优秀诗歌、散文、小说、戏剧等文学作品，学习欣赏、品味作品的语言、形象等，交流审美体验。；以学生自主阅读活动为主，引导学生了解阅读的多种策略，运用浏览、略读、精读等不同阅读方法。通读整本书，了解主要内容。

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释散文杂文集中的表达效果与思想情感？
- ABT：
  - And：你已经接触过散文杂文集相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握散文杂文集。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-erta-essay-collection`
- `python3 scripts/validate-courseware.py chn-m-erta-essay-collection`
- `python3 scripts/rebuild-index.py`
