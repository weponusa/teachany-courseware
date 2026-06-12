# PBL LLM 日志与模型配置

PBL 拆解默认走 **TeachAny 服务端中转**（OpenRouter 付费 `qwen/qwen3-next-80b-a3b-instruct`），用户浏览器不接触 Key。

前端 ⚙️ 可自选：
- **TeachAny 默认**：服务端 OpenRouter Qwen3 Next 80B（无需填 Key）
- **硅基 / 并行超算**：服务端 Key 中转，可选模型
- **OpenRouter**：Key 留空走服务端；填写 Key 则浏览器直连所选模型
- **自定义 API**：填写 Base URL + Key + 模型名

## 服务端模型链（自动降级）

1. `qwen/qwen3-next-80b-a3b-instruct`（OpenRouter）— 默认首选（含 match / 审核 / 调整）
2. `deepseek-ai/DeepSeek-V4-Flash`（硅基流动）— 兜底
3. `GLM-4-Flash`（并行超算）— 兜底

需配置 Pages 加密环境变量：`OPENROUTER_KEY`（主 Key）、`SILICONFLOW_KEY`（兜底）、`PARATERA_KEY`（兜底）。

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

### PBL_LOG_TOKEN 在哪设置

令牌**不会**写在仓库里，只在 Cloudflare Pages 项目 `teachany-courseware` 中配置：

1. Cloudflare Dashboard → **Workers & Pages** → **teachany-courseware**
2. **Settings** → **Environment variables** → **Production**
3. 变量名 `PBL_LOG_TOKEN`，类型 Text 或 Encrypted，值为自定义口令（如 `PBL`）
4. **保存后必须重新部署**（Retry deployment 或向 `main` 推送 commit），新值才会生效

验证：

```bash
curl "https://www.teachany.cn/api/pbl/logs?limit=5&token=你的口令&format=json"
```

返回 `"ok": true` 即配置成功。未配置 `PBL_LOG_TOKEN` 时，日志 API 对所有人开放；配置后无 token 会返回 403。

### 教师看板

```text
/teacher/pbl-logs.html
```

## Cloudflare 配置 checklist

1. D1 执行 `0002_pbl_llm_logs.sql`
2. Pages 加密环境变量：`OPENROUTER_KEY`（PBL 主 Key）、`SILICONFLOW_KEY`（兜底）、`PARATERA_KEY`（兜底）
3. 可选：设置 `PBL_LOG_TOKEN` 保护日志 API
