# TeachAny Design System

All TeachAny courseware shares a consistent visual language. This document specifies every design token, component pattern, and layout rule.

---

## Color Tokens

### Core Palette

```css
:root {
  /* Backgrounds */
  --bg: #0f172a;                          /* Primary background (slate-900) */
  --bg2: #1e293b;                         /* Secondary background (slate-800) */
  --bg3: #334155;                         /* Tertiary background (slate-700) */

  /* Cards */
  --card: rgba(30, 41, 59, 0.7);         /* Glassmorphism card */
  --border: rgba(148, 163, 184, 0.15);   /* Subtle border */

  /* Text */
  --text: #f8fafc;                        /* Primary text (slate-50) */
  --dim: #94a3b8;                         /* Secondary text (slate-400) */
  --dimmer: #64748b;                      /* Tertiary text (slate-500) */

  /* Accent Colors */
  --primary: #3b82f6;                     /* Blue — main interactive elements */
  --secondary: #8b5cf6;                   /* Purple — insights, deep understanding */
  --accent: #f59e0b;                      /* Yellow/Amber — highlights, emphasis */

  /* Semantic Colors */
  --success: #10b981;                     /* Green — correct answers */
  --danger: #ef4444;                      /* Red — incorrect answers */
  --pink: #ec4899;                        /* Pink — special highlights */
  --cyan: #06b6d4;                        /* Cyan — alternative accent */
}
```

### Color Usage Guide

| Element | Color Token | Purpose |
|:--------|:-----------|:--------|
| Page background | `--bg` | Dark base |
| Card background | `--card` | Semi-transparent glassmorphism |
| Primary text | `--text` | High contrast readable text |
| Secondary text | `--dim` | Supporting information |
| Section title accent | `--accent` | Left border highlight |
| Interactive elements | `--primary` | Buttons, links, hover states |
| Deep understanding boxes | `--secondary` | Insight callouts |
| Correct answer | `--success` | Quiz feedback |
| Incorrect answer | `--danger` | Quiz feedback |
| Highlighted keywords | `--accent` | Important terms, formulas |

---

## Typography

### Font Stack

```css
font-family: -apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif;
```

### Type Scale

| Element | Size | Weight | Line Height | Color |
|:--------|:-----|:-------|:------------|:------|
| Hero title | 44px | 800 | 1.2 | Gradient |
| Section title | 26px | 700 | 1.3 | `--text` |
| Card title (h3) | 19px | 600 | 1.4 | `--text` |
| Body text | 15.5-16px | 400 | 1.75-1.8 | `--dim` |
| Meta tags | 13px | 400 | 1.5 | `--dim` |
| Formula | 20px | 400 | 1.5 | `--accent` |
| Footer | 13px | 400 | 1.5 | `--dimmer` |

### Formula & Code

```css
.formula {
  font-family: 'Times New Roman', serif;
  font-size: 20px;
  color: var(--accent);
}
```

---

## Layout

### Page Structure

```
┌─────────────────────────────────────┐
│  Fixed Navigation Bar (60px height) │
├─────────────────────────────────────┤
│                                     │
│  Container (max-width: 1100px)      │
│  Padding: 80px 24px 60px           │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  Hero Section               │    │
│  │  (centered, 40px top pad)   │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  Section (margin: 46px 0)   │    │
│  │  ┌─────────┐ ┌─────────┐   │    │
│  │  │  Card   │ │  Card   │   │    │
│  │  └─────────┘ └─────────┘   │    │
│  └─────────────────────────────┘    │
│                                     │
│  ┌─────────────────────────────┐    │
│  │  Footer                     │    │
│  └─────────────────────────────┘    │
└─────────────────────────────────────┘
```

### Grid System

```css
/* 2-column responsive grid */
.grid-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
  gap: 20px;
}

/* 3-column responsive grid */
.grid-3 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
}
```

### Spacing

| Element | Value | CSS |
|:--------|:------|:----|
| Between sections | 46px | `margin: 46px 0` |
| Between cards | 20px | `margin-bottom: 20px` |
| Card padding | 26px | `padding: 26px` |
| Grid gap | 20px | `gap: 20px` |
| Nav height | 60px | `height: 60px` |
| Container top padding | 80px | Accounts for fixed nav |

---

## Components

### Card

```css
.card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 26px;
  margin-bottom: 20px;
  backdrop-filter: blur(10px);
  transition: transform 0.2s, box-shadow 0.2s;
}
.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}
```

### Section Title

```css
.section-title {
  font-size: 26px;
  font-weight: 700;
  margin-bottom: 20px;
  padding-left: 16px;
  border-left: 4px solid var(--accent);
}
```

### Quiz Option

```css
.quiz-option {
  display: block;
  padding: 14px 18px;
  margin: 8px 0;
  border-radius: 12px;
  background: rgba(30,41,59,0.5);
  border: 1px solid var(--border);
  cursor: pointer;
  transition: all 0.25s;
}
.quiz-option:hover {
  background: rgba(59,130,246,0.12);
  border-color: var(--primary);
}
.quiz-option.correct {
  background: rgba(16,185,129,0.15);
  border-color: var(--success);
}
.quiz-option.wrong {
  background: rgba(239,68,68,0.15);
  border-color: var(--danger);
}
```

### Insight Box

```css
.insight-box {
  background: linear-gradient(135deg, rgba(139,92,246,0.1), rgba(59,130,246,0.08));
  border-left: 4px solid var(--secondary);
  padding: 18px 22px;
  border-radius: 0 12px 12px 0;
  margin: 16px 0;
}
```

### Hero Gradient Title

```css
.hero h1 {
  font-size: 44px;
  font-weight: 800;
  background: linear-gradient(135deg, var(--primary), var(--secondary), var(--accent));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Meta Tags

```css
.hero .meta span {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 5px 16px;
  font-size: 13px;
  color: var(--dim);
}
```

---

## Interactive Elements

### Canvas Container

```css
.canvas-container {
  width: 100%;
  max-width: 650px;
  margin: 16px auto;
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  background: rgba(15,23,42,0.7);
}
canvas {
  display: block;
  width: 100%;
  height: auto;
}
```

### Drag-and-Drop

```css
.drag-item {
  display: inline-flex;
  align-items: center;
  padding: 9px 16px;
  border-radius: 10px;
  margin: 5px;
  background: rgba(30,41,59,0.7);
  border: 1px solid var(--border);
  cursor: grab;
  user-select: none;
  transition: all 0.2s;
}
.drop-zone {
  min-height: 70px;
  border: 2px dashed var(--border);
  border-radius: 12px;
  padding: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  transition: all 0.2s;
}
.drop-zone.active {
  border-color: var(--primary);
  background: rgba(59,130,246,0.05);
}
```

---

## Responsive Breakpoints

```css
/* Mobile-first approach */
@media (max-width: 768px) {
  .hero h1 { font-size: 32px; }
  .section-title { font-size: 22px; }
  .grid-2, .grid-3 { grid-template-columns: 1fr; }
  .container { padding: 70px 16px 40px; }
  .nav { padding: 0 12px; }
}

@media (max-width: 480px) {
  .hero h1 { font-size: 26px; }
  .card { padding: 18px; }
}
```

---

## Animation

### Standard Transitions

```css
/* Cards */
transition: transform 0.2s, box-shadow 0.2s;

/* Interactive elements */
transition: all 0.25s;

/* Fade in */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-6px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Scroll Behavior

```css
html { scroll-behavior: smooth; }
```

---

## Accessibility Notes

- **Color contrast**: All text meets WCAG AA (4.5:1 ratio minimum)
- **Focus states**: Interactive elements should have visible focus indicators
- **Keyboard navigation**: Quiz options should be keyboard-accessible
- **Screen readers**: Use semantic HTML (`<nav>`, `<section>`, `<h1>`-`<h3>`)
- **Reduced motion**: Respect `prefers-reduced-motion` media query

---

## Layout & Presentation Baseline

所有课件共享同一套**呈现基线**，使不同学科、不同批次生成的课件呈现一致的
产品观感，而不是各写各的版式。

### 1. 呈现形态：单一连续网页

- 所有模块自上而下连续排列，**整页统一滚动**
- ⛔ 严禁分页放映形态：
  - `.slide-page { min-height: 100dvh }`（整屏分页）
  - `.slide-container { height: 100dvh; overflow-y: auto; scroll-snap-type: y proximity }`
    （容器锁视口高度 + 独立滚动）
  - `scroll-snap-align: start`（滚动吸附）
  - 模块之间的 `.page-nav` 前后翻页条
- 导航统一为 **Sticky 顶部导航 + 锚点跳转**，不再提供翻页按钮

### 2. 宽度与对齐

| 项 | 值 |
|:---|:---|
| 主容器 `max-width` | `1080px` |
| 水平对齐 | `margin-left/right: auto`（居中） |
| 左右内边距 | `20px` |
| 模块上下间距 | `34px`（`.slide-page` / `.section`） |
| 窄屏降级 | 视口 ≤ `1120px` 时 `max-width: 100%` |

历史上不同批次写过 `900 / 960 / 920 / 860 / 780 / 1160px`，一律收敛到 `1080px`。

### 3. 标准模块

必选模块及其顺序（缺一不可）：

```
hero-infographic  →  objectives  →  pretest  →
lesson-focus ×N   →  lesson-method  →  deep-understanding  →
worked-example  →  practice  →  posttest  →
knowledge-graph  →  summary
```

每个模块使用统一的 `.section` 容器与 `.panel` / `.card` 组件，
标题层级固定为 `h1`（课件名）→ `h2`（模块名）→ `h3`（小节名）。

### 4. 落地方式

- 规范源文件：`scripts/standardize-layout.py`（注入覆盖样式，可 `--remove` 回退）
- 生成侧约束：skill 规则 #21 + Section 10.2.2（已改为连续网页，禁止分页放映）
