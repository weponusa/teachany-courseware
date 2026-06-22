# 全库课件质量循环计划

更新时间：2026-06-21

## 目标

对 `community/*` 全部课件（约 900+ 门）循环执行：**扫描 → 自动修复 → 再扫描**，直到关键项清零或进入人工队列。

## 检查维度

| 类别 | 检查项 | 自动修复 |
|------|--------|----------|
| 插图 | 缺图、引用 404、hero 过小（<20KB） | `repair-image-refs.py` |
| 插图 | Agnes 图内中文/英文乱码 | `--ocr` 扫描 + 定向 Agnes 重生成（道法/心理专用脚本） |
| 地图 | 历史/地理缺 `data-teachany-map` | `repair-all-courseware.py` |
| 视频 | 占位 mp4（<500KB）、HTML 死链 | 删除 mp4 + 剥离 `<video>` |
| 模块 | 缺知识图谱 / AI 学伴 / 本地 script 路径 | `finalize-courseware.py --shared` |
| 音频 | TTS mp3 < 3 | 标记人工队列（需 TTS 配额） |
| 互动 | 本地资源 404 | `repair-image-refs.py` + 人工 |
| 内容 | `[待补充]` / TODO 占位 | 人工队列 |

## 执行命令

```bash
# 1. 全库扫描（快，约 1–2 分钟）
python3 scripts/courseware-quality-loop.py audit

# 2. 按报告自动修复
python3 scripts/courseware-quality-loop.py fix

# 3. 循环 2 轮（扫描→修复→再扫描）
python3 scripts/courseware-quality-loop.py loop --rounds 2

# 4. 分批（避免长时间占用）
python3 scripts/courseware-quality-loop.py loop --rounds 1 --limit 200

# 5. 含 OCR 的精细扫描（慢，抽样用）
python3 scripts/courseware-quality-loop.py audit --ocr --limit 50
```

## 分波实施

| 波次 | 范围 | 动作 |
|------|------|------|
| W0 | 全库 | `audit` 出基线报告 |
| W1 | 全库 | `fix`：模块路径、地图、占位视频、死链图 |
| W2 | hist/geo | `repair-all-courseware.py` 全量 |
| W3 | 道法/心理 32 门 | `batch-pol-psych-samples.py --quality-pass` + OCR 定向替换 |
| W4 | OCR flagged | `regen-flagged-agnes-images.py` / Agnes vN |
| W5 | 仍 FAIL 基线 | 人工队列 + 按 cn-specs 重建 |

## 门禁

- 单课：`bash ~/.claude/skills/teachany/scripts/check_baseline.sh community/<id>`
- 全库：`python3 scripts/validate-courseware.py`
- 推送前：`scripts/pre-push.sh`

## 产出物

- `reports/courseware-quality-audit.json` — 基线（893/938 有问题）
- `reports/courseware-quality-audit-r6.json` — 最新（247/938，691 门已清零）
- `reports/courseware-quality-fix-w1.log` — W1 修复日志
- `reports/pol-psych-quality-pass.log` — 道法/心理 v1.3 全检（进行中）

## 最新进度（r7）

| 指标 | 基线 | 当前 |
|------|------|------|
| 有问题课件 | 893 | **235**（仅缺 TTS） |
| 已清零 | 45 | **703 (75%)** |
| 结构/图/视频/地图/模块 | 500+ | **0** |

### 进行中（后台）

1. **道法/心理 v1.3** — 20/32 已完成，剩余 12 门 `--quality-pass` 已续跑  
   日志：`reports/pol-psych-quality-pass.log`
2. **TTS 补录 W1** — `batch-tts-fill.py --limit 50`（清 playlist 后 finalize）  
   日志：`reports/batch-tts-w1.log`

### 新增脚本

- `scripts/fix-manual-queue.py` — 16 门人工队列一次性修复
- `scripts/batch-tts-fill.py` — 缺 TTS 批量补录
