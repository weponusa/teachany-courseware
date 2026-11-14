# NOTICE — 统一节点增强索引

`node-enhancement.json` 是 TeachAny 多套图谱按节点 ID 收敛的**统一增强层**，用于让 PBL 拆解与各页面消费同一份关系/内容/质量口径。

- **本地权威源**：`data/trees/**`、`knowledge-map-data.json`、`nodes-metadata.json`、`nodes-selector.json`、`node-enrichment-overlay.json`（均为本站自有数据）。
- **外部来源**：[cn-math-taxonomy](https://github.com/xiaoyang111222/cn-math-taxonomy)（CC BY-NC 4.0）的粗粒度投影。本站只存**课标编号、教材章节、覆盖统计、候选关系 ID 与支持度、以及用户主动调用的深链**；不存 description、mastery_criteria、先修理由、题干、答案等正文。
- **关系策略**：`prerequisites` 为权威先修（树/全局图/overlay 合并）；`candidate_prereqs` 为外部投影候选，带 `support` 且标 `review=candidate`，**不得直接当权威边发布**，需教师审核。
- **用途**：本地非商业研究 / 原型预览。未获作者书面单独授权前不得公开发布或商用；商业上线前需法务确认「编号 + 深链」边界。
- **生成**：`scripts/build-unified-node-enhancement.py`（只读输入、幂等、不修改树、不跑 rebuild-index.py、不导入题库）。
- **目录文件**：`node-enhancement.json`（canonical 全量）、`node-enhancement-pbl.json`（PBL 精简视图，首屏加载）、`review-candidates.csv` / `.md`（support≥3 的候选先修关系教师审核表）、`data/external/cn-math-taxonomy/coarse-enhancement.json`（知识地图兼容视图）。
- **缺口分类**：无权威先修的节点标 `gap_status`：`root`（学科/学段入口，正常）、`candidate_suggestion`（有外部投影建议边，仍待审核）、`ok`。不得把 AI 候选边直接当权威先修发布。
