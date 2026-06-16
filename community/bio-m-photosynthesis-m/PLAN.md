# 教学设计计划 · 光合作用

## Phase 0 定义

- **学生画像**：初一/七年级，已学习叶片结构
- **知识点**：光合作用（Photosynthesis）
- **node_id**：`bio-m-photosynthesis-m`
- **课型**：new-concept（新授课）
- **学段**：middle（初中）· G7
- **学科**：biology
- **领域**：植物学
- **前置知识**：bio-m-leaf-structure（叶片结构）
- **后续知识**：bio-m-respiration-m（呼吸作用）
- **课标对应**：阐明绿色植物通过光合作用制造有机物（人教版七年级上册第三单元）

## Phase 1 教学骨架

### 问题锚点（3 选项）

1. 植物不吃饭，它的"食物"从哪里来？
2. 为什么森林被称为"地球之肺"？
3. 大棚种植如何让蔬菜长得更快？

### ABT 叙事

- **And**（已有经验）：我们知道动物靠吃东西获取营养，植物也需要营养才能生长……
- **But**（冲突）：但植物没有嘴，不会进食——它是怎么"制造"自己的食物的？
- **Therefore**（本课任务）：因此，我们需要弄清楚光合作用这一核心过程——它的原料、条件、产物和意义。

### 核心内容模块

1. **光合作用的概念与反应式**：CO₂ + H₂O →(光/叶绿体)→ 有机物(C₆H₁₂O₆) + O₂
2. **光合作用的条件**：光照、叶绿体
3. **经典实验**：海尔蒙特柳树实验、普利斯特利钟罩实验、萨克斯半叶法实验
4. **光合作用的意义**：有机物来源、氧气来源、维持碳氧平衡
5. **影响因素**：光照强度、CO₂浓度、温度

### 互动设计

- **Canvas 交互**：光合速率模拟器——拖动滑块调节光照强度/CO₂浓度/温度，实时观察O₂释放速率变化曲线
- **PhET/3Dmol.js**：嵌入葡萄糖分子 3D 可视化（光合产物）
- **ConcepTest**：概念辨析——判断光合作用与呼吸作用的区别

### 评估设计

- **前测**：3 题选择题，检测先备知识
- **ConcepTest**：光合 vs 呼吸辨析
- **分层练习**：Level 1⭐ / Level 2⭐⭐ / Level 3⭐⭐⭐
- **后测**：4 题综合检测
- **常见错误追踪**：≥3 条

## Phase 2 构建清单

- [x] index.html（从模板构建）
- [x] manifest.json
- [x] assets/hero-infographic.svg
- [x] tts/*.mp3（edge-tts 生成）
- [x] PLAN.md（本文件）

## Phase 3 验证

```bash
node ~/.openclaw/workspace/.skills/teachany/scripts/validate-courseware.cjs ~/teachany-opensource/community/bio-m-photosynthesis-m/
```
