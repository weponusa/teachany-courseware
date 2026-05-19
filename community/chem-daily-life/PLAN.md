# 教学设计方案：化学与生产生活（跨学科实践）

**课程 ID**：chem-daily-life
**适用年级**：初中八年级
**学科**：化学
**课型**：special-topic（跨学科实践）
**课时**：1 课时（45 分钟）
**作者**：TeachAny
**版本**：0.1.0
**日期**：2026-05-19

---

## 1. 教学主题与目标

化学与生产生活（跨学科实践）—— 认识化学在日常生活、工业生产、环境保护、农业生产和能源开发等领域的广泛应用，培养学生的科学素养和社会责任感。

### 知识与技能
1. 举例说明化学在日常生活中的应用（洗涤剂、食品添加剂、医药、纺织等）
2. 了解化学在工业生产中的重要应用（合成氨、硫酸、冶金、石油化工、材料科学、电池等）
3. 认识化学在环境保护中的作用（污水处理、大气污染治理、固废处理、绿色化学等）
4. 理解化学在农业生产中的应用价值（化肥、农药、植物激素、土壤改良等）

### 过程与方法
- 通过问题锚点，引导学生主动探究化学与生活生产的关系
- 通过 Canvas 洗涤剂模拟互动，理解乳化原理
- 通过案例分析，了解化学在工农业生产中的实际应用
- 通过综合任务，设计环保洗涤剂配方，培养跨学科实践能力

### 情感态度与价值观
- 认识化学对社会发展的重要贡献，培养科学素养
- 理解绿色化学理念，树立环境保护意识
- 培养跨学科思维，提高解决实际问题的能力

---

## 2. 模块级媒体策划表

| 模块 | 媒体类型 | 来源/说明 |
|---|---|---|
| Hero | hero-infographic.svg + chem-daily-life-hero.png | 知识结构主图 |
| 前测 | 选择题 + 问答题 | 内置交互 |
| 核心概念：日常生活 | Canvas 洗涤剂模拟 + PhET iframe | 自建 Canvas + PhET 嵌入 |
| 核心概念：工业生产 | 案例卡片 | 内置 |
| 概念测试 1 | 选择题 | 内置交互，含诊断性反馈 |
| 核心概念：环境保护 | 步骤列表 | 内置 |
| 核心概念：农业生产 | 应用卡片 | 内置 |
| 概念测试 2 | 选择题 | 内置交互，含诊断性反馈 |
| 五镜头 | 四卡片 | 内置 |
| 三段式练习 | 判断 + 问答 + 设计 | 内置交互 |
| 综合任务 | 开放问答 | 内置 |
| 后测 | 问答 + 多选 | 内置交互，含诊断性反馈 |
| 小结 | 列表 | 内置 |
| 易错点 | 三卡片 | 内置 |
| 知识图谱 | data-teachany-kg | 标准模块自动渲染 |
| AI 学伴 | data-teachany-tutor-card | 标准模块 |
| 教学视频 | teaching-video.mp4 | assets/teaching-video.mp4 |
| TTS 音频 | s01~s06.mp3 | tts/ 目录，edge-tts 生成 |

---

## 3. 五件套自检

- [x] ABT + 情境引入：Hero 区含情境描述
- [x] 前测：前测模块存在，含选择 + 问答
- [x] 互动练习：Canvas 洗涤剂模拟 + PhET iframe + 多组问答交互
- [x] 诊断性反馈：所有选择题含具体错因分析，问答题含针对性提示
- [x] 后测与学习闭环：后测含问答 + 多选，与前测呼应
- [x] Bloom 层级覆盖：remember/understand/apply/analyze/evaluate/create 六层全覆盖
- [x] 知识图谱溯源：data-teachany-kg 属性已设置
- [x] 五镜头深层理解：Why / How / What if / See also 四角度
- [x] 卡片文字密度：所有卡片 ≤ 200 字
- [x] 三段式作业分层：基础（判断）/ 进阶（案例分析）/ 拓展（综合设计）
- [x] 前置知识链：meta 标签已设置（本期无强制前置）
- [x] 真实场景应用：洗涤剂、污水处理、合成氨等真实场景
- [x] Meta 标签完整性：14 项 meta 全部设置
- [x] AI 多模态互动区：非文科课题，可跳过
- [x] 双语版本：中文单版本，符合要求
- [x] 课件打包：manifest.json 存在，字段完整
- [x] 记忆锚点：问题锚点 + 易错点锚定
- [x] 易错点覆盖：3 个易错点，含正确做法
- [x] 本地资源无 404：所有本地资源可访问
- [x] 连续音频质量：6 段 TTS，播放器正常
- [x] 视频模块：teaching-video.mp4 有效，video 标签含 controls/playsinline
- [x] Canvas 真实互动：洗涤剂去污模拟，含滑块交互和实时绘制

---

## 4. Subagent 派遣

本期课件由主 Agent 独立完成，未派遣子 Agent。

| 模块 | 派遣对象 | 任务说明 | 状态 |
|---|---|---|---|
|（无）| — | — | — |

---

## 5. 注册与发布计划

- **node_id**：chem-daily-life
- **注册到知识树**：`python3 scripts/register_node.py --node-id chem-daily-life --subject chemistry --stage middle --grade 8 --name "化学与生产生活（跨学科实践）"`
- **注册到 registry.json**：由 `auto-publish.sh` 自动完成
- **注册到 teachany-kg-manifest.json**：由 `scripts/rebuild-index.py` 重建索引
- **发布目标**：GitHub Pages（weponusa.github.io/teachany）
- **推送**：`git push origin main`

---

## 6. 教学反思（课后填写）

（课后填写）

---

**附录**：
- 课件 HTML：`index.html`
- 元数据：`manifest.json`
- Hero 图：`assets/chem-daily-life-hero.png`
- 知识结构图：`assets/hero-infographic.svg`
- TTS 音频：`tts/s01.mp3` ~ `tts/s06.mp3`
- 教学视频：`assets/teaching-video.mp4`
