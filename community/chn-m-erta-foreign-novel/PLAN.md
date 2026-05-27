# PLAN.md — 外国名著（《海底两万里》等）：从文本证据到表达效果

- course_id: `chn-m-erta-foreign-novel`
- node_id: `chn-m-erta-foreign-novel`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 8 年级
- 学科：语文
- 课标节点：外国名著（《海底两万里》等）
- 课标摘录：独立阅读古今中外诗歌集、中长篇小说、散文集等文学名著，如《钢铁是怎样炼成的》。；根据阅读进度完成读书笔记，针对作品的语言、形象、主题等方面的话题展开研讨。；阅读革命文学作品，体会、评析革命领袖、革命英雄的爱国精神和人格魅力。

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释外国名著（《海底两万里》等）中的表达效果与思想情感？
- ABT：
  - And：你已经接触过外国名著（《海底两万里》等）相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握外国名著（《海底两万里》等）。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-erta-foreign-novel`
- `python3 scripts/validate-courseware.py chn-m-erta-foreign-novel`
- `python3 scripts/rebuild-index.py`
