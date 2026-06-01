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

## 注意

- 这是 V1 试点版，暂时没有教师登录保护。
- 不要收集身份证、家庭住址、手机号等敏感信息。
- 后续可以加教师口令、课程级任务、AI 分析报告。
