# PLAN.md — ext-36f258e（月球土壤资源利用技术）

## 0️⃣ 元信息

| 字段 | 值 |
|:---|:---|
| node_id | ext-36f258e |
| title | 月球土壤（月壤）资源利用技术 |
| subject | space-science |
| stage | high |
| grade | 11 |
| curriculum | cn-national |
| lesson_type | experiment |
| duration | 20-25 min |
| prerequisites | 无 |
| leads_to | 无 |
| teachany_version | 7.14.0 |

## 1️⃣ 六问

| # | 问题 | 回答 |
|:---:|:---|:---|
| 1 | 学生是谁？ | 高一/高二学生，已有化学（氧化还原、金属冶炼）和物理（热学、材料）基础 |
| 2 | 前置知识？ | 化学方程式、氧化还原反应、金属冶炼原理、材料力学基础 |
| 3 | 学完后能做什么？ | 能分析月壤成分→选择提取方法→计算能耗→评估可行性 |
| 4 | 真实场景？ | NASA Artemis 计划、中国嫦娥工程月面基地建设 |
| 5 | 最常卡在哪？ | 混淆地球冶炼和太空冶炼的约束差异；忽略能耗是可行性判据 |
| 6 | 如何验证学会了？ | 能独立设计火星 ISRU 方案并指出与月球的差异 |

## 2️⃣ 教学模块规划

### 模块 A：月壤成分与特性（Bloom: Remember/Understand）
- ABT 引入：月壤不是土
- 核心概念：成分柱状图 + ISRU 定义
- 互动：成分可视化切换

### 模块 B：提取方法与工程约束（Bloom: Apply/Analyze）
- 三种方法对比：氢还原 / 熔融电解 / 碳热还原
- 互动：提氧效率计算器
- 易错点：Si-O 键能 vs Fe-O 键能

### 模块 C：月壤建材与 3D 打印（Bloom: Apply/Create）
- ISRU 流程图
- 互动：3D 打印模拟器
- 迁移任务：火星 ISRU 方案

## 3️⃣ 标准资产清单

- ✅ Hero 信息图 (hero-infographic.svg)
- ✅ TTS 旁白 (s01-s03.mp3)
- ✅ AI 学伴 (teachany-tutor-card.js)
- ✅ 知识图谱 (teachany-knowledge-graph.js)
- ✅ 概念图 + 过程图 (concept-diagram.svg, process-diagram.svg)
- ✅ 2 个 Canvas 互动（提氧计算器 + 3D 打印模拟器）

## 4️⃣ 输出目录结构

```
community/ext-36f258e-lunar-soil/
├── index.html
├── manifest.json
├── PLAN.md
├── assets/
│   ├── hero-infographic.svg
│   ├── concept-diagram.svg
│   └── process-diagram.svg
└── tts/
    ├── s01.mp3
    ├── s02.mp3
    └── s03.mp3
```
