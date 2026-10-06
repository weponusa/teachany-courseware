# PBL 输入参数

从用户自然语言提取；缺省用默认值，**不必逐项追问**。

| 字段 | CLI | 可选值 / 说明 | 默认 |
|------|-----|---------------|------|
| 项目任务 | `--goal` | 必填，原文 | — |
| 学段 | `--grade` | `any`, `primary`, `junior`, `senior`, `university`, `adult` | `any` |
| 学科 | `--subject` | `cross`, `math`, `physics`, `chemistry`, `biology`, `science`, `chinese`, `english`, `history`, `geography`, `info-tech`, `art` | `cross` |
| 产出 | `--deliverable` | `report`, `decision-table`, `engineering-prototype`, `experiment-report`, `design-proposal`, `presentation`, `app-software`, `handwork-model`, `portfolio`, `plan-schedule`, `other` | `report` |
| 自定义产出 | `--deliverable-custom` | `deliverable=other` 时 | — |
| 受众 | `--audience` | 班级展示、家庭决策… | — |
| 周期 | `--duration` | 4 周、8 课时… | — |
| 约束 | `--constraints` | 预算、设备、评价标准… | — |
| 输出目录 | `-o` | 本地路径 | `.` |

## 学段推断提示

| 用户说法 | `--grade` |
|----------|-----------|
| 小学、四年级 | `primary` |
| 初中、七八九年级 | `junior` |
| 高中 | `senior` |
| 大学、高职 | `university` |
| 成人、家长、职场 | `adult` |
