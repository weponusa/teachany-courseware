# PBL LLM 日志与模型配置

PBL 拆解默认走 **TeachAny 服务端中转**（硅基流动 DeepSeek-V4-Flash），用户浏览器不接触 API Key；可在前端 ⚙️ 自选服务商/模型。

## 服务端模型链（自动降级）

1. `deepseek-ai/DeepSeek-V4-Flash`（硅基流动）— 默认首选（含 match / 审核 / 调整）
2. `deepseek-ai/DeepSeek-V4-Pro`（硅基流动）— 强阶段备选
3. `GLM-4-Flash`（并行超算）— 兜底

需配置 Pages 加密环境变量：`SILICONFLOW_KEY`（主 Key）、`PARATERA_KEY`（兜底）。`OPENROUTER_KEY` 可选。

可选：`PBL_MATCH_MODEL` / `PBL_MODEL_OVERRIDE` 锁定单模型做 A/B。

## D1 日志表

在已绑定的 `TEACHANY_DB` 上执行：

```text
migrations/0002_pbl_llm_logs.sql
```

每次 `/api/pbl/analyze` 调用会写入：

- 阶段 `decompose` / `filter` / `match` / `verify-deps`
- 用户目标 `goal`
- 完整 `messages`（system + user 提示词）
- 模型原始返回 `response_text`
- 使用的 `model` / `backend`、耗时、错误信息

## 查询日志

### API

```text
GET /api/pbl/logs?limit=50&stage=match&goal=食堂&format=json
GET /api/pbl/logs?format=ndjson   # 导出 NDJSON 日志文件
```

若配置了 `PBL_LOG_TOKEN`，请求需带 `?token=...` 或头 `X-PBL-Log-Token`。

### 教师看板

```text
/teacher/pbl-logs.html
```

## Cloudflare 配置 checklist

1. D1 执行 `0002_pbl_llm_logs.sql`
2. Pages 加密环境变量：`SILICONFLOW_KEY`（主 Key）、`PARATERA_KEY`（兜底）；`OPENROUTER_KEY` 可选
3. 可选：设置 `PBL_LOG_TOKEN` 保护日志 API
