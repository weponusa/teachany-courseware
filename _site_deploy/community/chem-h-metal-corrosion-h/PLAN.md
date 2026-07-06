# PLAN.md — 金属腐蚀与防护：铁为什么会悄悄变成铁锈？

- course_id: `chem-h-metal-corrosion-h`
- node_id: `chem-h-metal-corrosion-h`
- 模式：TeachAny v7.14 完整模式
- 课型：experiment / new-concept

## Phase 0 定义与检索
- 学段：高中 11 年级
- 学科：化学
- 课标节点：金属的腐蚀与防护（高中）
- 课标摘录：认识有化合价变化的反应是氧化还原反应，了解氧化还原反应的本质是电子的转移，知道常见的氧化剂和还原剂。；能多角度、动态地分析化学变化，运用化学反应原理解决简单的实际问题。；紧密联系生产和生活实际，创设丰富多样的真实问题情境。

## Phase 1 教学骨架
- 问题锚点：为什么盐水环境会明显加快铁的腐蚀，而镀锌能保护铁？
- ABT：
  - And：你已经理解原电池、电解池和氧化还原反应，知道金属失电子会被氧化。
  - But：钢桥、船体和管道并不是被一口气“烧掉”，而是在水、氧、电解质共同作用下慢慢发生电化学腐蚀。
  - Therefore：所以要从微小原电池角度理解腐蚀，并比较涂层、镀锌、牺牲阳极和外加电流等防护方法。
- 真实互动：Canvas 变量实验 + 分层练习 + 后测反馈
- 评估闭环：前测 → 概念拆解 → 互动实验 → 后测 → 三段式作业

## Phase 2 标准模块
- 已挂载 AI 学伴、导师卡片、TTS narrator、section hints、知识图谱、连续音频播放器。
- 科学仿真：按课题使用 Canvas 或 PhET/3Dmol 类成熟资源；本课无外部资源不可用豁免。

## Phase 3 验证计划
- `node scripts/validate-courseware.cjs community/chem-h-metal-corrosion-h`
- `python3 scripts/rebuild-index.py`
- 抽样检查：本地资源无 404、音频 >= 3 段、视频可控、知识树 status=active。
