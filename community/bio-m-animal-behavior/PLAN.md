# PLAN.md — bio-m-animal-behavior (动物行为)

## 课件元信息

| 字段 | 值 |
|:---|:---|
| course-id | bio-m-animal-behavior |
| node_id | bio-m-animal-behavior |
| 标题 | 动物行为 |
| 学科 | biology |
| 年级 | 8 |
| 学段 | middle |
| 领域 | 动物学 |
| 课型 | new-concept |
| 前置 | bio-m-animal-diversity (动物的主要类群) |
| 后续 | bio-m-microorganism (微生物) |

## 教学设计

### 问题锚点（Problem Anchor）
提供 3 个选项：
1. 蜘蛛织网是天生的还是学会的？（先天 vs 学习行为）
2. 蚂蚁怎么分工合作的？（社会行为）
3. 动物为什么要迁徙？（迁徙行为的意义）

### ABT 叙事
- AND：我们已经知道动物种类繁多，形态各异
- BUT：同一种动物为什么有时表现出本能行为，有时又能学习新技能？
- THEREFORE：我们需要区分先天性行为和学习行为，理解不同行为类型的生物学意义

### 核心内容模块
1. **先天性行为与学习行为** — 定义、区分、举例
2. **主要行为类型** — 觅食、防御、繁殖、迁徙
3. **社会行为** — 蚂蚁/蜜蜂分工、等级制度
4. **动物行为的意义** — 适应环境、种族延续

### Canvas 互动
行为分类拖拽游戏：
- 将动物行为卡片拖入"先天性行为"或"学习行为"分类框
- 行为示例：蜘蛛织网、鹦鹉学舌、蜜蜂跳舞、小狗做算术、鸟类迁徙、黑猩猩钓白蚁

### 外部工具
PhET Natural Selection 仿真：
`https://phet.colorado.edu/sims/html/natural-selection/latest/natural-selection_zh_CN.html`

### 评估设计
- **前测**：检测对"本能"的直觉理解
- **ConcepTest**：区分先天性行为与学习行为的判断
- **后测**：迁移到新场景（海龟归巢是什么行为？）

## TTS 音频计划
- `tts/s01-intro.mp3` — 开场 + ABT 叙事
- `tts/s02-behavior-types.mp3` — 先天性行为与学习行为讲解
- `tts/s03-social-behavior.mp3` — 社会行为讲解

## 资源清单
- `assets/hero-infographic.svg` — 动物行为分类知识结构图（暗色主题）
- PhET natural-selection iframe 嵌入
- Canvas 拖拽互动游戏

## 验证清单
- [x] manifest.json
- [x] index.html（五件套）
- [x] PLAN.md
- [x] assets/hero-infographic.svg
- [x] TTS ≥3 文件
- [x] validate-courseware.cjs 通过
