# PBL LLM 日志与模型配置

PBL 拆解**不再提供前端模型选择**，统一走服务端预设的免费模型链。

## 服务端模型链（自动降级）

1. `qwen/qwen3-next-80b-a3b-instruct:free`（OpenRouter）— 中文课标 + 结构化 JSON
2. `meta-llama/llama-3.3-70b-instruct:free`（OpenRouter）— 指令跟随备选
3. `GLM-4-Flash`（并行超算）— 429/503 时快速兜底

需配置环境变量：`OPENROUTER_KEY`、`PARATERA_KEY`（与现有 LLM 代理相同）。

## D1 日志表

在已绑定的 `TEACHANY_DB` 上执行：

```text
migrations/0002_pbl_llm_logs.sql
```

每次 `/api/pbl/analyze` 调用会写入：

- 阶段 `decompose` / `filter` / `match`
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
2. Pages 环境变量：`OPENROUTER_KEY`、`PARATERA_KEY`（已有则跳过）
3. 可选：设置 `PBL_LOG_TOKEN` 保护日志 API
