# PLAN.md — 平衡常数：用 K 判断平衡偏向哪里

- course_id: `chem-h-equilibrium-constant`
- node_id: `chem-h-equilibrium-constant`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：平衡常数
- 课标摘录：认识化学变化有一定限度、速率，是可以调控的。能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；能用对立统一、联系发展和动态平衡的观点考察化学反应，预测在一定条件下某种物质可能发生的化学变化。

## Phase 1 教学骨架
- 问题锚点：为什么 K 很大时，平衡通常更偏向生成物？
- ABT：
  - And：你已经理解化学平衡和勒夏特列原理，知道平衡不是停止，而是正逆速率相等。
  - But：只说“向右移动”还不够定量。不同反应平衡偏向程度差别很大，需要一个数字描述平衡中反应物和生成物的相对多少。
  - Therefore：所以要学习平衡常数 K，用平衡浓度幂次之比定量判断反应进行程度，并理解 K 只受温度影响。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-equilibrium-constant`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
