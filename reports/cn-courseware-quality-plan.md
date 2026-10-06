# 中国课标课件全库质检修复升级计划

## 范围

| 类别 | 数量 | 说明 |
|------|------|------|
| **中国课标课件** | **~911** | 含 cn-national / 义务教育课标字段 / 非国际体系 |
| 有 cn-spec 可重建 | **260** | `scripts/cn-specs` 与 community 目录匹配 |
| 无 spec  legacy | **~651** | 旧模板/手工课，需单独迁移或保留 |
| 道法/心理（课标树） | **32** | v1.3 quality-pass **已完成** |
| 国际课标 | ~300 | 不在本计划范围 |

## 两层质检

### L1 结构质检（已完成）

`courseware-quality-loop.py audit --cn-only`

- 占位视频、缺图、模块路径、地图、死链 → **已清零**
- 全库仅 35 门缺 TTS（有 data-tts 标记）

### L2 课标基线（validate-courseware）

`audit --cn-only --strict` → `reports/courseware-quality-audit-cn-strict.json`

- **513/633** 未通过 TeachAny v7 硬规则
- 主要缺口：Remotion mp4(466)、ConcepTest(362)、课标对齐字段(362)、脚手架/Bloom(361)、TTS(232)

## 修复策略

| 类型 | 手段 | 命令 |
|------|------|------|
| 结构/模块/地图 | 自动 fix | `python3 scripts/courseware-quality-loop.py fix --cn-only` |
| 有 cn-spec 的课 | **模板升级** | `python3 scripts/courseware-quality-loop.py upgrade --from-audit reports/courseware-quality-audit-cn-strict.json` |
| 道法/心理 32 门 | 精细内容+v1.3 | `batch-pol-psych-samples.py --quality-pass` ✅ |
| 无 spec legacy | 人工队列 / 新建 spec | 待建 spec 或标记 deprecated |

## 执行波次

| 波次 | 内容 | 状态 |
|------|------|------|
| W0 | 全库结构 fix（938 门） | ✅ 903 门清零 |
| W1 | 课标 strict 审计 633 门 | ✅ |
| W2 | cn-spec 升级 260 门（分批 80×4） | 🔄 W2-1 进行中 |
| W3 | 升级后再 strict 审计 | 待续 |
| W4 | legacy 373 门评估（合并/弃用/补 spec） | 待续 |
| W5 | Remotion mp4 批量（需渲染队列） | 待续 |

## 命令速查

```bash
# 课标范围审计
python3 scripts/courseware-quality-loop.py audit --cn-only --strict

# 结构自动修复
python3 scripts/courseware-quality-loop.py fix --cn-only

# cn-spec 模板升级（分批）
python3 scripts/courseware-quality-loop.py upgrade --from-audit reports/courseware-quality-audit-cn-strict.json --limit 80

# 全量升级 260 门
python3 scripts/courseware-quality-loop.py upgrade --force
```
