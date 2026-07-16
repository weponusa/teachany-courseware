# 课件去套路升级 · 分批计划

> 目标：去掉 And/But/Therefore 空壳，改成「专属情境 + 真互动 + 真题」。  
> 不做纯 LLM 批量贴题。手写配方在 `scripts/rewrite_physics_authentic.py`。

## 现状（2026-07-17）

| 范围 | 数量 |
|---|---|
| 初中物理 `phy-m-*` 目录升级目标 | 36（B–G 自动目录）+ Batch A 样板等 |
| 自动升级 `quality_v3` 完成 | **36 / 36**（Round 1–7，fail=0） |
| 剩余待自动改 | **0** |

Batch A 手改样板 + B–G 自动多轮已全部跑完。循环哨兵已停止。

## 原则

1. **一门一改**：每课专属情境/互动/真题，禁止角色任务空壳。  
2. **先初中物理，再扩科**：`phy-m` 清完 → `math-m` / `chem-m` / `bio-m`。  
3. **每批 4–5 门**：改完更新 `qc-upgrade.html`，你验收后再下一批。  
4. **幂等**：已含专属 fingerprint 且无 ABT 则跳过。  
5. **发布**：一批验收通过后再统一提交发布（不边改边推）。

## 质量硬标准（2026-07-17 起强制）

### Hero / 插图（对齐道法心理课流水线）
1. **生图**：Agnes **无字**插图（prompt 禁止中英文、禁止「角色任务/学习目标」元文案）；额度用尽可用新 `course_id` 槽位生成后拷入课件。  
2. **加字**：HTML `.ta-figure-labeled` + `.ta-fig-tag` **叠中文知识点标签**（公式/实验/易错）；**禁止**让模型在图里画中文（易乱码）。  
3. **抽检**：OCR 应接近 clean（无 CJK 乱码、无 Flatle/Made 9 类噪声）。  
4. **备选模型**：若走 OpenRouter，用 `google/gemini-3.1-flash-image`（`OPENROUTER_IMAGE_API_KEY` + `openrouter-image2.py` / baoyu-image-gen），同样优先「无字图 + 叠字」。

### 正文结构（禁止空洞）
学习闭环必须完整，且练习够用：
1. 问题锚点（本课专属，非通用三选一）  
2. 真实情境 → 前测 ConcepTest  
3. 核心概念（条件+公式+图像，写清易错）  
4. 专属互动实验（可调变量）  
5. **网络仿真（强制）**：按 `iframe-resources.md` 嵌入 ≥1 个 PhET/GeoGebra 等中文版 iframe，不得只用自绘 Canvas 顶替  
6. 例题拆解（步骤完整）  
7. **三级练习**：L1 巩固 ≥2 题 · L2 应用 ≥2 题（含错因）· L3 迁移 ≥1 题  
8. 小结清单（可勾选）  
禁止：空 slide、通用「证据表/地图」套话、重复「角色任务」元信息、错配无关 PhET（如力学课塞 forces-and-motion 充数）。

## 批次安排（phy-m 剩余 41）

### Batch A · 电学补全 — 5 门 ✅ 质量回修完成，待验收
- `phy-m-simple-machines` 简单机械  
- `phy-m-resistance` 电阻  
- `phy-m-voltage` 电压  
- `phy-m-ohms-law` 欧姆定律  
- `phy-m-series-parallel` 串并联  

### Batch B · 电学进阶 — 5 门
- `phy-m-circuit-calculation`  
- `phy-m-current-measurement`  
- `phy-m-electric-power`  
- `phy-m-joule-law`  
- `phy-m-static-electricity`  

### Batch C · 电磁 — 5 门
- `phy-m-magnetism-basics`  
- `phy-m-electromagnetism-basic`  
- `phy-m-electromagnetic-induction`  
- `phy-m-electric-motor`  
- `phy-m-generator`  

### Batch D · 光学 — 6 门
- `phy-m-light-propagation`  
- `phy-m-light-reflection` / `phy-m-plane-mirror`  
- `phy-m-light-refraction` / `phy-m-refraction` / `phy-m-lens`  
- （合并去重视课程结构后再改）  
- `phy-m-spherical-mirror` · `phy-m-light-dispersion` · `phy-m-eye-vision`  

### Batch E · 声学 — 4 门
- `phy-m-sound-generation`  
- `phy-m-sound-properties`  
- `phy-m-sound-applications`  
- `phy-m-noise-control`  

### Batch F · 力学补全 — 6 门
- `phy-m-mass-density`  
- `phy-m-motion-description`  
- `phy-m-newton-laws`  
- `phy-m-mechanical-energy`  
- `phy-m-energy-conservation`  
- `phy-m-liquid-pressure-buoyancy`  

### Batch G · 热学与其它 — 余下
- `phy-m-specific-heat` · `phy-m-phase-change` · `phy-m-internal-energy`  
- `phy-m-heat-engine` · `phy-m-fluid-flow` · `phy-m-acoustics-cross-disciplinary`  
- 以及列表中其余未归类项  

**节奏建议**：每天 1–2 批（4–10 门），约 **1–2 周** 清完初中物理；然后开数学/化学/生物平行批次。

## 每批验收清单

- [ ] 无 `And 已有经验` / `角色任务：`  
- [ ] 无无关 PhET `forces-and-motion`  
- [ ] 有专属情境标题（非通用「观察现象—控制变量」）  
- [ ] 有专属互动（滑块/示意与本课公式或概念对应）  
- [ ] 有可点击真题 + 错因  
- [ ] 本地 `http://127.0.0.1:8877/qc-upgrade.html` 可打开  

## 跟踪文件

- 配方：`scripts/rewrite_physics_authentic.py`  
- 质检页：`qc-upgrade.html`  
- 本计划：`docs/upgrade-authentic-batch-plan.md`  
- 剩余清单：`data/upgrade-phy-m-remaining.txt`（自动生成）

## 自动多轮（2026-07-17 启）

```bash
# 单轮（默认下 3 门）
python3 scripts/auto_upgrade_phy_m.py --limit 3
python3 scripts/auto_upgrade_phy_m.py --batch B --limit 5
python3 scripts/auto_upgrade_phy_m.py --status

# 目录与状态
# data/phy-m-upgrade-catalog.json  — 36 门配方（B–G）
# data/auto-upgrade-state.json     — 已完成/失败轮次
# data/upgrade-phy-m-remaining.txt — 剩余清单
# qc-upgrade.html                  — 进度页
```

每轮自动：无字 Agnes 生图 → 专属正文(L1/L2/L3) → PhET 中文 iframe → 去 junk → QC。  
Agent 可按 12 分钟循环继续跑，直到 remaining=0。
