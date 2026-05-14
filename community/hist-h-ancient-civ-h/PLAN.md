# PLAN.md — hist-h-ancient-civ-h（古代亚非欧文明）

## 1. 六问

| # | 问题 | 回答 |
|---|------|------|
| 1 | 学生是谁？ | 高二学生（G11），已学过初中世界史基础，对古埃及金字塔、中国夏商周等有初步印象，但缺乏系统比较视角 |
| 2 | 前置知识？ | 初中历史：四大文明的基本名称和地理位置；地理：世界主要河流分布（尼罗河、两河、印度河、黄河长江） |
| 3 | 学完后能做什么？ | 能说出四大文明的发源地河流和时间起点；能解释"大河文明"的共同成因；能用表格对比四者的政治/文字/成就/命运；能分析中华文明延续未中断的原因 |
| 4 | 真实场景？ | 博物馆参观时能看懂不同文明的文物关联；阅读新闻时理解"一带一路"沿线国家的历史渊源；讨论"文明冲突论"时有历史依据 |
| 5 | 最常卡在哪？ | ① 混淆各文明的时间先后顺序 ② 误认为古希腊属于大河文明 ③ 不理解种姓制度与佛教的关系 ④ 对中华文明延续性的原因认识肤浅 |
| 6 | 如何验证学会了？ | 前测3题 + 每节互动练习 + 后测5题；Bloom 覆盖4层（记忆→理解→应用→分析）；综合对比题检验高阶思维 |

## 2. 模块级媒体策划表

| # | 模块名 | 知识点 | 媒体形式 | 资产文件名 | 生成命令 | 校验命令 |
|---|--------|--------|----------|------------|----------|----------|
| #1 | 前测模块 | 大河文明基础认知 | 选择题3道 | index.html 内联 | 手写JS | checkPre() |
| #2 | 概览·四大文明摇篮 | 大河文明定义与共同条件 | Leaflet世界地图+卡片网格 | index.html 内联(Leaflet CDN) | CDN引入+手写JS | initMap() |
| #3 | 古埃及模块 | 尼罗河馈赠/法老专制/象形文字 | 时间轴4节点 | index.html 内联 | 手写时间轴HTML/CSS | tl-item |
| #4 | 古巴比伦模块 | 两河流域/楔形文字/汉谟拉比法典 | 时间轴4节点 | index.html 内联 | 手写时间轴HTML/CSS | tl-item |
| #5 | 古印度模块 | 双源流/种姓制度/佛教诞生 | 时间轴4节点 | index.html 内联 | 手写时间轴HTML/CSS | tl-item |
| #6 | 古中国模块 | 夏商周三代/礼乐文明/延续性 | 时间轴4节点 | index.html 内联 | 手写时间轴HTML/CSS | tl-item |
| #7 | 综合对比模块 | 四大文明异同表/中华文明延续原因 | 对比表格6维度 | index.html 内联 | 手写对比表格HTML/CSS | compare-table |
| #8 | 后测模块 | 综合检验5题覆盖全部知识点 | 选择题5道 | index.html 内联 | 手写JS | checkPost() |
| #9 | 知识图谱模块 | 四大文明知识点关系图 | 标准公共模块（data-teachany-kg） | data-teachany-kg="hist-h-ancient-civ-h" | 引用 ../../scripts/teachany-knowledge-graph.{js,css} | check-knowledge-graph.py |

## 3. 五件套自检清单

- [x] #01 ABT 引入（5/5 内容模块）
- [x] #02 前测 ≥3 题
- [x] #05 后测 ≥5 题
- [x] #06 Bloom 4 层覆盖（记忆、理解、应用、分析）
- [x] #07 Meta 标签 ≥10 个（teachany-author/difficulty/domain/version/grade/subject/node/course-id/node/title/prereqs/next 共12个）
- [ ] #08 五镜头法 ≥2 模块使用
- [x] #09 卡片文字密度 ≤120字
- [x] #11 前置知识链 meta 标注
- [x] #13 manifest.json 完整
- [ ] #14 AI 学伴入口（待引用 ai-tutor.js）
- [ ] #16 可打包（单文件）
- [ ] #17 记忆锚点
- [x] #18 易错诊断室（每节均有 error-predict）
- [x] #62 Hero 信息图（Leaflet 世界地图标注四大文明位置）
- [x] #63 Canvas/SVG 真实互动 ≥3 处（地图点击跳转、判断练习、对比选择）
- [ ] #64 TTS mp3 ≥5 段（待生成）
- [x] #65 教学组件实质内容（非敷衍）
- [ ] #66 Remotion 视频（L2-skip：历史课以史料+地图为主）
- [ ] #67 知识图谱模块
- [x] #68 PLAN.md 存在且完整

## 4. Subagent 派遣

```
HARD_RULES（违反任何一条 = 返工）：
1. Hero 区必须有知识结构信息图（SVG 或 PNG），不接受纯 CSS 渐变背景 → 使用 Leaflet 地图标注四大文明位置
2. TTS 必须用 edge-tts 生成真实 mp3，放在 tts/ 目录
3. Canvas 动画必须有 requestAnimationFrame 驱动的真实动画逻辑（若使用 Canvas）
4. SVG 互动必须有 Drag & Drop + Touch Events 支持（若使用 SVG）
5. 题目答案必须学科准确（参照课标和人教版教材）
6. 必须引用 ../../scripts/ai-tutor.{css,js}
7. 暗色主题 glassmorphism，高中级 CSS 变量
8. manifest.json 必须与 PLAN.md 元信息一致
9. 文件结构：index.html + manifest.json + tts/ + assets/
10. meta 标签 ≥10 个（含 teachany-* 系列）
```

## 5. 输出目录结构

```
examples/hist-h-ancient-civ-h/
├── index.html              # L1 互动课件（主体）✅ 已完成
├── manifest.json           # 元数据 ✅ 已完成
├── PLAN.md                 # 本文件 ✅ 已完成
├── README.md               # 课件说明
├── assets/
│   ├── hero/               # Hero 信息图（可选）
│   └── illustrations/      # SVG/PNG 插图
└── tts/
    ├── module1.mp3         # 待生成
    ├── module2.mp3         # 待生成
    └── narration.json      # 旁白文本索引
```

## 6. HARD_RULES

```
HARD_RULES（违反任何一条 = 返工）：
1. Hero 区必须有知识结构信息图（SVG 或 PNG），不接受纯 CSS 渐变背景
2. TTS 必须用 edge-tts 生成真实 mp3，放在 tts/ 目录
3. Canvas 动画必须有 requestAnimationFrame 驱动的真实动画逻辑（若使用 Canvas）
4. SVG 互动必须有 Drag & Drop + Touch Events 支持（若使用 SVG）
5. 题目答案必须学科准确（参照课标和人教版高中历史教材）
6. 必须引用 ../../scripts/ai-tutor.{css,js}
7. 暗色主题 glassmorphism，高中级 CSS 变量
8. manifest.json 必须与 PLAN.md 元信息一致
9. 文件结构：index.html + manifest.json + tts/ + assets/
10. meta 标签 ≥10 个（含 teachany-* 系列）
```
