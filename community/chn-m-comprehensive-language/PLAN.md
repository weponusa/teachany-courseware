# PLAN.md — 综合性语言运用：从文本证据到表达效果

- course_id: `chn-m-comprehensive-language`
- node_id: `chn-m-comprehensive-language`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：语文
- 课标节点：综合性语言运用
- 课标摘录：学会倾听与表达，初步学会用口头语言文明地进行人际沟通和社会交往。；乐于用口头、书面的方式与人交流沟通，愿意与他人分享，增强表达的自信心。；能主动参与日常生活中的文化活动，根据不同的场合，尝试运用合适的音量和语气与他人交流，有礼貌地请教、回应。

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释综合性语言运用中的表达效果与思想情感？
- ABT：
  - And：你已经接触过综合性语言运用相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握综合性语言运用。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-comprehensive-language`
- `python3 scripts/validate-courseware.py chn-m-comprehensive-language`
- `python3 scripts/rebuild-index.py`
