# PLAN.md — 勒夏特列原理：平衡如何回应外界扰动？

- course_id: `chem-h-le-chatelier`
- node_id: `chem-h-le-chatelier`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：勒夏特列原理
- 课标摘录：认识化学变化有一定限度、速率，是可以调控的。能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；能用对立统一、联系发展和动态平衡的观点考察化学反应，预测在一定条件下某种物质可能发生的化学变化。；选择性必修课程中，依据化学学科的基础性研究领域，设置“化学反应原理”模块。

## Phase 1 教学骨架
- 问题锚点：怎样用“减弱外界改变”一句话判断平衡移动方向？
- ABT：
  - And：你已经知道化学平衡是动态平衡，也知道浓度、温度、压强会影响可逆反应。
  - But：面对扰动时，很多判断容易混乱：加压到底向哪边？升温要看正反应还是逆反应？加反应物会不会一定提高产率？
  - Therefore：所以要学习勒夏特列原理：当平衡体系受到扰动时，平衡会向减弱这种扰动的方向移动。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-le-chatelier`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
