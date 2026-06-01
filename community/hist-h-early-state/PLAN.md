# PLAN.md — 中华文明的起源与早期国家

- course_id: `hist-h-early-state`
- node_id: `hist-h-early-state`
- 学科/学段：history / high-10
- 执行约束：不做视频占位、不做地图占位；保留可用互动与知识图谱。

## 知识层引用（Phase 0.5）

| 用途 | KCP ID | 来源 |
|------|--------|------|
| 课标 / 卜辞材料依据 | cp-1～cp-5 等 | `knowledge-context.json` → `curriculum_excerpts` |
| 知识上下文文件 | — | `python3 scripts/knowledge_layer.py lookup --node-id hist-h-early-state --emit-kcp` |

缺口：`exercises<1`、`common_errors<1` — 由课标摘录 + 例题讲解页手写补足。

## 生成摘要

- 已生成：`index.html`、`manifest.json`、`knowledge-context.json`、`assets/hist-h-early-state-hero.svg`、`assets/concept-diagram.svg`、`assets/process-diagram.svg`
- 未生成：视频、地图、TTS（按当前用户要求：不做占位）
- 后续：用户确认上传后再统一跑挂树与发布。
