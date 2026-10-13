# PLAN.md — bio-h-nervous-regulation（神经调节）

## 0️⃣ 元信息

| 字段 | 值 |
|------|-----|
| node_id | bio-h-nervous-regulation |
| title | 神经调节 |
| subject | biology |
| stage | high |
| grade | 11 |
| curriculum | cn |
| textbook | 选择性必修一 第2章 |
| lesson_type | new-concept |
| duration_min | 45 |
| prerequisites | bio-h-internal-environment, bio-h-atp |
| leads_to | bio-h-humoral-regulation, bio-h-immune-regulation |
| teachany_version | 7.9.11 |

## 1️⃣ 六问

| # | 问题 | 回答 |
|---|------|------|
| 1 | 学生是谁？ | 高二学生，已学完细胞代谢和内环境稳态，有一定生物学概念基础 |
| 2 | 前置知识？ | 内环境与稳态（细胞外液、组织液）；ATP与能量代谢（离子泵耗能）|
| 3 | 学完后能做什么？ | 画出完整反射弧并标注五部分；解释动作电位产生原理；说明突触传递为何单向；区分条件/非条件反射；分析分级调节案例 |
| 4 | 真实场景？ | 膝跳反射、缩手反射、巴甫洛夫条件反射实验、植物人仍有呼吸心跳 |
| 5 | 最常卡在哪？ | ①混淆传导方向（纤维双向vs突触单向）②离子流动方向搞反③以为神经递质只有兴奋性④条件反射消退机制 |
| 6 | 如何验证学会了？ | 前测3 + 即时练习5 + 后测5，Bloom覆盖6层；综合任务L3（设计实验） |

## 2️⃣ 教学模块规划（5模块）

### Module 1：反射与反射弧
- ABT：膝跳反射不受意识控制 → 但为什么？ → 反射弧
- 核心概念：反射定义、反射弧五部分（感受器→传入神经→神经中枢→传出神经→效应器）
- 互动：**Canvas 动画** — 反射弧信号传导（发光点沿通路移动，逐部分高亮）
- Bloom：记忆（辨认五部分）+ 理解（解释功能）+ 应用（判断截断实验结果）
- 易错：混淆传入/传出神经

### Module 2：兴奋在神经纤维上的传导
- ABT：手碰火缩回极快 → 信号怎么跑这么快？ → 电信号（动作电位）
- 核心概念：静息电位（K+外流，外正内负-70mV）→ 动作电位（Na+内流，去极化+30mV）→ 局部电流 → 双向传导
- 互动：**Canvas 动画** — 动作电位传播（膜电位曲线实时绘制 + 兴奋区域沿纤维传播 + Na+/K+离子流动标注）
- Bloom：理解（电位变化原理）+ 分析（为什么双向传导？为什么在体内单向？）

### Module 3：兴奋在突触处的传递
- ABT：兴奋能在纤维上跑 → 但两个神经元之间有间隙 → 突触结构解决
- 核心概念：突触结构（突触小体→前膜→间隙→后膜）；传递过程（合成→囊泡→胞吐→扩散→受体→灭活）；单向传递原因
- 互动：**SVG 拖拽标注** — 突触结构6标签（突触小泡、前膜、间隙、后膜、受体、神经递质）
- Bloom：记忆（结构名称）+ 理解（传递过程）+ 分析（为什么单向？）

### Module 4：神经系统的分级调节
- ABT：植物人没意识但能呼吸 → 不同层级中枢管不同功能 → 分级调节
- 核心概念：大脑皮层（最高级，意识）→ 下丘脑（体温、渗透压、内分泌）→ 脑干（呼吸、心跳）→ 脊髓（排尿、排便、膝跳）
- 互动：SVG 层次结构图（分级金字塔）
- Bloom：理解（各级功能）+ 应用（解释具体案例）

### Module 5：高级神经活动
- ABT：巴甫洛夫的狗听铃声流口水 → 新生儿不会 → 条件反射是后天建立的
- 核心概念：非条件反射（先天、稳定、低级中枢）vs 条件反射（后天、可消退、大脑皮层）；语言中枢（S/W/V/H区）
- 互动：**拖拽分类** — 8个实例分入"条件反射"/"非条件反射"
- Bloom：理解（区分两种反射）+ 评价（判断实例）+ 创造（设计条件反射实验方案）

## 3️⃣ 标准资产清单

| 资产类型 | 要求 | 工具/方法 |
|----------|------|-----------|
| Hero 图 | image-registry.json 查找 → image_gen → SVG 降级 | find-hero / Pillow / inline SVG |
| TTS 旁白 | 5 模块 × 每模块 1 段旁白 mp3 | edge-tts (zh-CN-YunxiNeural) |
| Remotion 视频 | ≥3 场景教学动画（反射弧传导 + 动作电位 + 突触传递） | Remotion + React + TS |
| AI 学伴 | ../../scripts/ai-tutor.{css,js} | 标准引用 |
| 知识图谱 | ../../scripts/teachany-knowledge-graph.{js,css} 或 inline SVG | 标准模块 |
| 连续音频播放器 | Web Speech API fallback（若 mp3 生成失败） | 标准模块 |

## 4️⃣ 输出目录结构

```
community/bio-h-nervous-regulation/
├── index.html              # L1 互动课件（主体）
├── manifest.json           # 元数据
├── PLAN.md                 # 本文件
├── assets/
│   ├── hero/               # Hero 知识结构图
│   └── illustrations/      # SVG/PNG 插图
├── tts/
│   ├── module1.mp3
│   ├── module2.mp3
│   ├── module3.mp3
│   ├── module4.mp3
│   ├── module5.mp3
│   └── narration.json      # 旁白文本索引
└── remotion/               # L2 教学视频（若环境支持）
    └── out/
        └── bio-h-nervous-regulation-animation.mp4
```

## 5️⃣ Completeness Gate 自检项

- [ ] #01 ABT 引入（5/5 模块）
- [ ] #02 前测 ≥3 题
- [ ] #05 后测 ≥5 题
- [ ] #06 Bloom 6 层全覆盖
- [ ] #07 Meta 标签 ≥10 个
- [ ] #08 五镜头法 ≥2 模块使用
- [ ] #09 卡片文字密度 ≤120字
- [ ] #11 前置知识链 meta 标注
- [ ] #13 manifest.json 完整
- [ ] #14 AI 学伴入口
- [ ] #16 可打包（单文件 + assets/tts）
- [ ] #17 记忆锚点
- [ ] #18 易错诊断室
- [ ] #62 Hero 信息图（非纯色占位）
- [ ] #63 Canvas/SVG 真实互动 ≥3 处
- [ ] #64 TTS mp3 ≥5 段
- [ ] #65 教学组件实质内容（非敷衍）
- [ ] #66 Remotion 视频（≥3 场景 / 或标注 L2-skip 原因）
- [ ] #67 知识图谱模块
- [ ] #68 PLAN.md 存在且完整

## 6️⃣ Subagent HARD_RULES

给 subagent 的硬性约束（必须包含在 prompt 中）：

```
HARD_RULES（违反任何一条 = 返工）：
1. Hero 区必须有知识结构信息图（SVG 或 PNG），不接受纯 CSS 渐变背景
2. TTS 必须用 edge-tts 生成真实 mp3，放在 tts/ 目录
3. Canvas 动画必须有 requestAnimationFrame 驱动的真实动画逻辑
4. SVG 互动必须有 Drag & Drop + Touch Events 支持
5. 题目答案必须学科准确（参照课标）
6. 必须引用 ../../scripts/ai-tutor.{css,js}
7. 暗色主题 glassmorphism，高中级 CSS 变量
8. manifest.json 必须与 PLAN.md 元信息一致
9. 文件结构：index.html + manifest.json + tts/ + assets/
10. meta 标签 ≥10 个（含 teachany-* 系列）
```
