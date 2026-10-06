# PLAN.md — 焓变与反应热：用 ΔH 表达能量变化

- course_id: `chem-h-enthalpy-change`
- node_id: `chem-h-enthalpy-change`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：焓变与反应热
- 课标摘录：认识化学变化的本质特征是有新物质生成，并伴有能量转化；认识化学变化有一定限度、速率，是可以调控的。；关注化学变化中的能量转化；能用对立统一、联系发展和动态平衡的观点考察化学反应，预测在一定条件下某种物质可能发生的化学变化。

## Phase 1 教学骨架
- 问题锚点：为什么同一个反应反向书写时，ΔH 的符号要反过来？
- ABT：
  - And：你已经能从能量图判断放热和吸热，也知道热化学方程式需要写出反应热。
  - But：不同反应、不同物质状态、不同计量系数会让热量数值不同；如果不理解 ΔH 的定义，很容易把符号和倍数搞错。
  - Therefore：所以要用 ΔH = H生成物 - H反应物 统一表达焓变，并理解反应热随方程式方向和系数改变。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-enthalpy-change`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
