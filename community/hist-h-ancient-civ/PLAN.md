# PLAN.md — 中华文明起源（史前·新石器）

- course_id: `hist-h-ancient-civ`
- node_id: `hist-h-ancient-civ`
- 学科/学段：history / high-10
- 执行约束：不做视频占位、不做地图占位；保留可用互动与知识图谱。

## 知识层引用（Phase 0.5）

| 用途 | KCP ID | 来源 |
|------|--------|------|
| 课标导入 / 前测依据 | cp-1, cp-2 | `kp-json#curriculum_points` |
| 知识上下文文件 | — | `knowledge-context.json`（`knowledge_layer.py lookup --emit-kcp`） |

已知缺口（`knowledge-context.json` → `gaps`）：`exercises<1`、`common_errors<1` — 例题与易错点由课标摘录改写 + 互动设计补足，非模型空编。

## 生成摘要

- 已生成：`index.html`、`manifest.json`、`assets/hist-h-ancient-civ-hero.svg`、`assets/concept-diagram.svg`、`assets/process-diagram.svg`
- 已生成：`knowledge-context.json`（知识层 P0）
- 未生成：视频、地图、TTS（按当前用户要求：不做占位）
- 后续：用户确认上传后再统一跑挂树与发布。
