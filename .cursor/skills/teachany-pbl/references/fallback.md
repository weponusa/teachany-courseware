# Playwright 不可用或拆解失败时的兜底

## 1. 返回编辑链接（必做）

链接**不要**带 `auto=1`：

```
https://www.teachany.cn/pbl?goal={urlencode(task)}&grade={grade}&subject={subject}
```

若用户已有 `?handoff=` 或 `?pbl=` 链接，直接打开即为**已拆解完成**的项目页。

无 handoff 时告知用户：打开链接 → 点击 **「拆解项目路径」** → 等待完成 → 页面内导出长图。

## 2. 安装依赖后重试一次

```bash
pip install playwright
playwright install chromium
python3 scripts/pbl-decompose.py --goal "..." -o ./pbl-output
```

成功时 `edit_url` 通常为 `?handoff=<uuid>`。`handoff_source=browser` 为正常情况（浏览器同源创建 handoff）。

## 3. Windows 终端乱码 / 崩溃

若出现 `UnicodeEncodeError`，在运行前设置：

```bash
set PYTHONIOENCODING=utf-8
```

或在 PowerShell：`$env:PYTHONIOENCODING='utf-8'`。新版脚本已内置 stdout UTF-8 重配置。

## 4. teachany.cn 不可达

明确告知用户需可访问 `https://www.teachany.cn`。无法联网时只能提供上述 `?goal=` 链接，由用户在浏览器内手动拆解。

## 5. macOS Playwright 签名问题

报错含 `different Team IDs` 时，用系统 Python 建独立 venv：

```bash
/opt/homebrew/bin/python3 -m venv /tmp/pbl-venv
/tmp/pbl-venv/bin/pip install playwright
/tmp/pbl-venv/bin/playwright install chromium
/tmp/pbl-venv/bin/python3 scripts/pbl-decompose.py --goal "..." -o ./pbl-output
```
