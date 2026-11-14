# NOTICE — 粗粒度图谱增强数据

本目录只保留 `coarse-enhancement.json`，用于 TeachAny 知识地图的**粗粒度骨架增强**。

- **数据来源**：[xiaoyang111222/cn-math-taxonomy](https://github.com/xiaoyang111222/cn-math-taxonomy)（CC BY-NC 4.0 International）
- **本站保存的内容**：课标条目编号、教材章节名、外部知识点 ID、覆盖统计、以及指向对方服务的深链入口。
- **本站不保存的内容**：对方的 `description` / `mastery_criteria` / 先修 `reason` / 题干 / 选项 / 答案等正文。这些内容由**用户主动调用对方服务**获取（`access: user-invoked`），本站不代理、不缓存、不分发。
- **图谱结构不变**：节点数 9667、主边数 15299 均不变；投影关系仅作为可选的叠加参考层。
- **候选关系**：投影粗边按 `support_count` 分级，需教师审核，不得直接作为权威先修关系发布；上游 hard/soft 为 AI 主观判断、未经审核。
- **合规**：单纯深链 + 事实性编号一般不构成 CC BY-NC 数据的再分发；商业上线前仍需法务确认边界（尤其是链接的场景化呈现与调用方式）。
- **免责**：上游数据按 AS-IS 提供，本站仅作本地预览。

> Phase 1 的细粒度 overlay 数据（graph-overlay / mapping / standards）已移至 `_research/cms-taxonomy/overlay-phase1/`，降级为离线研究素材，**不参与站点发布**。
