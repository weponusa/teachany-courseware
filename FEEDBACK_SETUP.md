# TeachAny Feedback V1 设置说明

本功能已经包含前端页面和 Cloudflare Pages Function：

- 学生反馈页：`/feedback.html`
- 教师看板：`/teacher/feedback.html`
- API：`/api/feedback`
- 试点课件：`/community/math-linear-function/`

## 还需要在 Cloudflare 配置 D1

Cloudflare Pages Functions 需要绑定 D1 数据库，否则 API 会返回 `D1_NOT_CONFIGURED`。

### 1. 创建 D1 数据库

在 Cloudflare Dashboard：

```text
Workers & Pages → D1 SQL Database → Create database
```

建议名称：

```text
teachany_feedback
```

### 2. 执行建表 SQL

把仓库里的 SQL 执行到 D1：

```text
migrations/0001_feedback_entries.sql
```

也可以在 Cloudflare D1 控制台的 Console 里粘贴执行。

### 3. 给 Pages 项目绑定 D1

进入 Pages 项目：

```text
teachany-courseware → Settings → Functions → D1 database bindings
```

添加绑定：

```text
Variable name: TEACHANY_DB
D1 database: teachany_feedback
```

保存后重新部署一次。

## 验证

打开：

```text
https://www.teachany.cn/feedback.html
```

填一条测试数据。

然后打开：

```text
https://www.teachany.cn/teacher/feedback.html
```

能看到记录就说明成功。

## 反馈密码

做课老师可以在课件的 `manifest.json` 中设置反馈口令。学生提交反馈时必须填写正确口令，数据才会写入 D1。

示例：

```json
"feedback": {
  "require_password": true,
  "password_sha256": "5c898ffd138d7e070107d14bc77b71ffa131478c00a6399055f476f6ad0795a4",
  "password_hint": "试点密码 ta-demo"
}
```

其中 `password_sha256` 是反馈密码的 SHA-256 十六进制。比如试点密码 `ta-demo` 的哈希就是上面这一串。

本仓库的试点课件 `/community/math-linear-function/` 已设置反馈密码：

```text
ta-demo
```

## 注意

- 这是 V1 试点版，暂时没有教师登录保护。
- 反馈密码只是课堂口令，不是高安全账号系统。
- 不要收集身份证、家庭住址、手机号等敏感信息。
- 后续可以加教师口令、课程级任务、AI 分析报告。
<!-- deploy-trigger: 2026-06-01T14:48:21Z -->
