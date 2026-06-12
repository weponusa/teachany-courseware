# TeachAny 课件生图中转（Agnes 免费生图）

Skill 用户**无需**注册 Agnes 或配置 API Key。Agent 调用 `scripts/agnes-image-gen.py` 即可，请求经 `www.teachany.cn` 服务端中转。

## 用户侧（Skill / Agent）

```bash
# 查额度（每课件默认 3 张）
python3 scripts/agnes-image-gen.py --course-id math-linear-function --quota

# 生成 hero 并落盘
python3 scripts/agnes-image-gen.py \
  --course-id math-linear-function \
  --prompt "linear function on coordinate plane, slope triangle, pastel K12 infographic" \
  --out community/math-linear-function/assets/hero.png \
  --slot hero
```

流程建议：

1. `find-hero.py "$COURSE_DIR" --cdn` — L1/L2 命中则直接用 CDN
2. 未命中 → `agnes-image-gen.py`（`--slot hero`，占 1 张额度）
3. 章节插图再调 1–2 次（合计不超过 3 张）
4. 额度用尽 → `gen-hero-svg.py` 或嵌入 PhET/GeoGebra

## 运维部署（Cloudflare Pages）

### 1. 环境变量（加密）

| 变量 | 说明 |
|------|------|
| `AGNES_API_KEY` | Agnes 平台 API Key（仅服务端，勿写入仓库） |
| `TEACHANY_DB` | 已绑定的 D1（与 PBL 日志同库即可） |

可选：

| 变量 | 默认 | 说明 |
|------|------|------|
| `IMAGE_GEN_PER_COURSE_LIMIT` | `3` | 每课件最多生图张数 |
| `IMAGE_GEN_IP_RPM` | `10` | 每 IP 每分钟请求上限 |

### 2. D1 迁移

在 `TEACHANY_DB` 执行：

```text
migrations/0004_courseware_image_gen.sql
```

### 3. API

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/api/images/quota` | 服务状态 |
| `GET` | `/api/images/quota?course_id=xxx` | 课件剩余额度 |
| `POST` | `/api/images/agnes` | 生图，body: `{ course_id, prompt, size?, slot? }` |

### 4. 验证

```bash
curl -s https://www.teachany.cn/api/images/quota | jq .
curl -s "https://www.teachany.cn/api/images/quota?course_id=demo-linear-function" | jq .
```

部署完成且配置 `AGNES_API_KEY` 后，`agnes_configured` 应为 `true`。

若刚在 Pages 添加/修改 `AGNES_API_KEY` 仍显示 `false`，向 `main` 推送任意提交即可触发 Cloudflare Pages 重新部署（GitHub 已连接时自动构建）。

## 限制说明

- **每课件 3 张**：按 `course_id` 计数，含 hero + 所有章节插图
- **无文字插图**：服务端自动追加 `NO TEXT` 约束，标题/公式由 HTML/SVG 叠字
- **临时 URL**：Agnes 返回的图片链接会过期，脚本会立即下载到 `assets/`
- **IP 限流**：防止滥用；正常 Skill 做单门课件不会触发
