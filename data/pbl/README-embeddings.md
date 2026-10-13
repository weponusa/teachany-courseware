# PBL 课标向量索引

`node-embeddings.json` 供 PBL 向量召回使用（filter 之后、propose 之前）。

## 构建

```bash
# 推荐：OpenRouter text-embedding-3-small（需 OPENROUTER_KEY）
OPENROUTER_KEY=sk-... node scripts/build-pbl-embeddings.mjs

# 离线兜底：本地 hash 向量（无需 API，精度较低）
node scripts/build-pbl-embeddings.mjs --local
```

## 运行时

1. 浏览器加载 `node-embeddings.json`
2. 用蓝图 + 目标构造 query 文本
3. `local-hash-v1`：客户端即时算 query 向量；OpenAI embed：调用 `POST /api/pbl/embed`
4. cosine top-K → 与关键词召回合并 → propose index 选配

## 升级

课标树更新后重新运行构建脚本并部署。
