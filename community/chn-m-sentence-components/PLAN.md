# PLAN.md — 句子成分分析：从文本证据到表达效果

- course_id: `chn-m-sentence-components`
- node_id: `chn-m-sentence-components`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 7 年级
- 学科：语文
- 课标节点：句子成分分析
- 课标摘录：初中7年级学段目标：理解并掌握「句子成分分析」的基本概念与方法；学业要求：能在真实情境中识别、运用「句子成分分析」解决问题；活动建议：通过观察、实验、练习、讨论等方式深化对「句子成分分析」的理解

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释句子成分分析中的表达效果与思想情感？
- ABT：
  - And：你已经接触过句子成分分析相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握句子成分分析。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-sentence-components`
- `python3 scripts/validate-courseware.py chn-m-sentence-components`
- `python3 scripts/rebuild-index.py`
