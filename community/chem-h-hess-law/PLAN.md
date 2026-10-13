# PLAN.md — 盖斯定律：反应焓变为什么只看始态和终态？

- course_id: `chem-h-hess-law`
- node_id: `chem-h-hess-law`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：盖斯定律
- 课标摘录：认识化学变化的本质特征是有新物质生成，并伴有能量转化；认识化学变化有一定限度、速率，是可以调控的。；能从内因与外因、量变与质变等方面较全面地分析物质的化学变化，关注化学变化中的能量转化；能用对立统一、联系发展和动态平衡的观点考察化学反应。

## Phase 1 教学骨架
- 问题锚点：为什么把反应分几步走，最终总焓变仍然等于一步完成的焓变？
- ABT：
  - And：你已经知道焓变 ΔH 表示反应前后能量差，也会判断放热和吸热。
  - But：很多反应无法直接测量反应热，或者直接反应太慢、太危险；但可以把目标反应拆成几步可测反应。
  - Therefore：所以要学习盖斯定律：只要始态和终态相同，反应焓变与路径无关，可以把多个热化学方程式相加得到目标反应。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-hess-law`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
