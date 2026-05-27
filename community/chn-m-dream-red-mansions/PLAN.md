# PLAN.md — 《红楼梦》选读：从文本证据到表达效果

- course_id: `chn-m-dream-red-mansions`
- node_id: `chn-m-dream-red-mansions`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：语文
- 课标节点：《红楼梦》选读
- 课标摘录：独立阅读古今中外诗歌集、中长篇小说、散文集等文学名著，根据阅读进度完成读书笔记，针对作品的语言、形象、主题等方面的话题展开研讨。；引导学生了解阅读的多种策略，运用浏览、略读、精读等不同阅读方法；通读整本书，了解主要内容，关注整体与局部、局部与局部之间的关系。；能从多个角度分析作品中的人物行为、人物形象、作品中的优美词语、精彩段落，并根据需要进行摘录。

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释《红楼梦》选读中的表达效果与思想情感？
- ABT：
  - And：你已经接触过《红楼梦》选读相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握《红楼梦》选读。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-dream-red-mansions`
- `python3 scripts/validate-courseware.py chn-m-dream-red-mansions`
- `python3 scripts/rebuild-index.py`
