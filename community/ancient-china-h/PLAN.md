# PLAN.md — 中国古代史：文明起源与制度演进总览

- course_id: `ancient-china-h`
- node_id: `ancient-china-h`
- 学科/学段：history / high-10
- 执行约束：不做视频占位、不做地图占位；保留可用互动与知识图谱。

## 知识层引用（Phase 0.5）

| 用途 | KCP ID | 来源 |
|------|--------|------|
| 总览课标 / 子课摘录 | cp-1, cp-2；`from-hist-h-*` | `knowledge-context.json`（卫星 + 子节点合并） |
| 卫星 JSON | ancient-china-h | `data/kp/history/ancient-china-h.json` |
| 重新生成 KCP | — | `python3 scripts/knowledge_layer.py lookup --node-id ancient-china-h --emit-kcp community/ancient-china-h/knowledge-context.json` |

## 生成摘要

- 已生成：`index.html`、`manifest.json`、`knowledge-context.json`、`assets/ancient-china-h-hero.svg`、`assets/concept-diagram.svg`、`assets/process-diagram.svg`
- 未生成：视频、地图、TTS（按当前用户要求：不做占位）
- 后续：用户确认上传后再统一跑挂树与发布。
