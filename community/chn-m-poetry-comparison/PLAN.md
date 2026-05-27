# PLAN.md — 古诗词比较阅读：从文本证据到表达效果

- course_id: `chn-m-poetry-comparison`
- node_id: `chn-m-poetry-comparison`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / annotation-lab

## Phase 0 定义与检索
- 学段：初中 9 年级
- 学科：语文
- 课标节点：古诗词比较阅读
- 课标摘录：阅读表现人与社会、人与他人的古今优秀诗歌、散文、小说、戏剧等文学作品，学习欣赏、品味作品的语言、形象等，交流审美体验。；引导学生客观、全面、冷静地思考问题，识别文本隐含的情感、观点、立场，体会作者运用的思维方法，如比较、分析、概括、推理等。；思维能力是指学生在语文学习过程中的联想想象、分析比较、归纳判断等认知表现。

## Phase 1 教学骨架
- 问题锚点：怎样用文本证据解释古诗词比较阅读中的表达效果与思想情感？
- ABT：
  - And：你已经接触过古诗词比较阅读相关题型，也能凭经验说出一些常见答案。
  - But：中考语文不接受空泛感受，答案必须回到文本证据、语境和表达目的。
  - Therefore：所以本课要用“任务识别—圈画证据—解释方法—组织答案”的路径，掌握古诗词比较阅读。
- 真实互动：文本批注 Canvas + AI 多模态批注/作文诊断 + 前后测反馈
- 评估闭环：前测 → 文本检查表 → 概念拆解 → 批注实验 → 后测 → 迁移任务

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 语文互动：Canvas 文本批注 + AI 多模态互动区。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chn-m-poetry-comparison`
- `python3 scripts/validate-courseware.py chn-m-poetry-comparison`
- `python3 scripts/rebuild-index.py`
