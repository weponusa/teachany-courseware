#!/usr/bin/env python3
"""给缺分层作业的课件补齐「作业分层」模块（审计口径与 scripts/audit-quality.py 一致）。

背景
----
scripts/audit-quality.py 的 L5 判定：
    has_homework = any(m in html for m in ('作业分层', '基础巩固', '迁移挑战'))
缺一项扣 8 分。2026-10-09 盘点：1043 门中 320 门缺（2026-09-22 时为 463 门，
期间已自行补掉 143 门）。

这件事最容易被做成「塞关键词」——只为了骗过检测而插入三句空话。那不是补内容，
是制造占位内容。所以本脚本走 LLM：先从课件自身抽取标题、目标、核心小节标题、
小结文本，再让模型按布鲁姆三层（识记 / 应用 / 迁移）生成**针对该课件主题**的
真实任务，最后注入统一结构（slot 115）。

用法
----
  # 只看会改哪些、生成什么（dry-run，不落盘）
  python3 scripts/add-layered-homework.py --pilot 2
  python3 scripts/add-layered-homework.py --ids math-congruent-triangles,bio-asexual-repro

  # 真正写入
  python3 scripts/add-layered-homework.py --pilot 2 --apply
  python3 scripts/add-layered-homework.py --all --apply --workers 4
  python3 scripts/add-layered-homework.py --subject chn --apply --workers 4

  # 从清单文件（每行一个课件 id）批量
  python3 scripts/add-layered-homework.py --from-file /tmp/lh-ids.txt --apply

  # 回滚（只删本脚本注入的、带 data-injected="layered-homework" 标记的节）
  python3 scripts/add-layered-homework.py --all --revert

幂等：课件已含三个关键词之一就跳过；已注入过的靠 INJECT_TAG 识别，不会重复。
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

OR_URL = "https://openrouter.ai/api/v1/chat/completions"
OR_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
MODEL = os.environ.get("LAYERED_HW_MODEL", "deepseek/deepseek-chat")

MARKERS = ("作业分层", "基础巩固", "迁移挑战")
INJECT_TAG = 'data-injected="layered-homework"'

# 豁免：外部托管跳转壳（teachany-hosting=external-link / link-shell-1.0）。
# 这类课件本体只有 3~4 KB，真实内容在站外，本地没有可据此出题的知识骨架，
# 强行注入只会造出空话。全站已知 1 门：bio-m-cell-division-junior-6ab0e172。
SKIP_RE = re.compile(r'name=["\']teachany-hosting["\'][^>]*content=["\']external-link|link-shell-1\.0', re.I)

# ---------------------------------------------------------------- 上下文抽取

TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
SEC_RE = re.compile(r"<section\b[^>]*>.*?</section>", re.S | re.I)
HEADING_RE = re.compile(r"<h([23])[^>]*>(.*?)</h\1>", re.S | re.I)
TITLE_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.S | re.I)
OG_RE = re.compile(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']+)', re.I)

# 抽取正文时优先看的节（信息密度最高的几块）
PREFERRED_SEC = (
    "objectives", "lesson-focus", "deep-understanding", "summary",
    "posttest", "practice", "error-clinic", "memory-anchor", "goals",
)


def txt(s: str) -> str:
    return WS_RE.sub(" ", TAG_RE.sub("", s or "")).strip()


def get_title(html: str) -> str:
    m = OG_RE.search(html) or TITLE_RE.search(html)
    return txt(m.group(1)) if m else ""


def section_by_id(html: str, sid: str) -> str:
    m = re.search(r'<section\b[^>]*\bid=["\']%s["\'][^>]*>(.*?)</section>' % re.escape(sid),
                  html, re.S | re.I)
    return m.group(1) if m else ""


def build_context(html: str) -> str:
    """抽取足以让 LLM 写出针对性任务的上下文（控制长度，省 token）。"""
    parts: list[str] = []

    # 1) 目标
    obj = txt(section_by_id(html, "objectives"))
    if obj:
        parts.append("【学习目标】" + obj[:400])

    # 2) 核心小节正文（lesson-focus / deep-understanding / summary）
    for sid in ("lesson-focus", "deep-understanding", "summary", "error-clinic"):
        s = txt(section_by_id(html, sid))
        if s:
            parts.append(f"【{sid}】" + s[:600])

    # 3) 全站 h2/h3 标题串（最能体现本课的知识骨架）
    heads = [txt(m.group(2)) for m in HEADING_RE.finditer(html)]
    heads = [h for h in heads if 2 <= len(h) <= 40]
    # 去重保序
    seen, uniq = set(), []
    for h in heads:
        if h not in seen:
            seen.add(h)
            uniq.append(h)
    if uniq:
        parts.append("【小节标题】" + " / ".join(uniq[:40]))

    # 4) 兜底：靠前的任意 section 正文
    if len(parts) < 2:
        for m in list(SEC_RE.finditer(html))[:24]:
            t = txt(m.group(0))
            if len(t) > 60:
                parts.append("【正文片段】" + t[:300])
            if len(parts) >= 4:
                break

    return "\n".join(parts)[:2200]


# ---------------------------------------------------------------- LLM

SYS = (
    "你是中国中小学各科的资深教研员，擅长按布鲁姆认知层级设计分层作业。"
    "只输出合法 JSON，不要任何解释、不要 Markdown 代码块。"
)

TMPL = """下面是某门课件的信息。请为它设计一套**分层作业**，三层各一条。

课件标题：{title}
{ctx}

要求：
1. 三层分别是：
   - basic（⭐ 基础巩固）：识记与再现层级，题目/任务必须落到本课的**具体概念、公式、术语、事实**上，能当场判对错。
   - apply（⭐⭐ 能力应用）：应用与分析层级，给一个**具体情境**让学生用本课知识解释或求解，情境要真实（生活、实验、史料、语料等，随学科而定）。
   - transfer（⭐⭐⭐ 迁移挑战）：综合与创造层级，要求学生**产出**一件东西（设计方案、实验报告、短文、证明、模型、调查等），并说明评价要点。
2. 严禁写成通用空话（例如"回顾本课内容并总结"、"用自己的话说说收获"、"查找相关资料进一步了解"）——这类不算数，会被判为占位内容。
3. 必须紧扣上面「课件标题」和「小节标题」里的具体知识点；学段难度由标题里的 Gx / 小学 / 初中 / 高中 决定。
4. 每条 20–60 字，是一条可直接布置给学生的任务，不要写答案。
5. 语言：简体中文（英语课件可用中英混排，但任务描述用中文）。

输出 JSON，键为 basic / apply / transfer，值是字符串。"""


def call_llm(prompt: str) -> str | None:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    if not OR_KEY:
        raise RuntimeError("缺少 OPENROUTER_API_KEY 环境变量")

    s = requests.Session()
    retry = Retry(total=5, connect=5, read=5, backoff_factor=2.0,
                  status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["POST"])
    s.mount("https://", HTTPAdapter(max_retries=retry, pool_connections=16, pool_maxsize=16))

    last = None
    for attempt in range(6):
        try:
            r = s.post(OR_URL,
                       headers={"Authorization": f"Bearer {OR_KEY}",
                                "Content-Type": "application/json"},
                       json={"model": MODEL,
                             "messages": [{"role": "system", "content": SYS},
                                          {"role": "user", "content": prompt}],
                             "temperature": 0.5, "max_tokens": 1200},
                       timeout=(30, 180))
            if r.status_code == 429:
                time.sleep(10 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as ex:  # noqa: BLE001
            last = ex
            time.sleep(6 * (attempt + 1))
    raise RuntimeError(f"LLM 调用失败: {last}")


FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)


def gen_tasks(title: str, ctx: str) -> dict[str, str] | None:
    raw = call_llm(TMPL.format(title=title or "(无标题)", ctx=ctx))
    if not raw:
        return None
    raw = raw.strip()
    m = FENCE_RE.search(raw)
    if m:
        raw = m.group(1).strip()
    # 有些模型会先说两句，取第一个 { 到最后一个 }
    if not raw.startswith("{"):
        i, j = raw.find("{"), raw.rfind("}")
        if i >= 0 and j > i:
            raw = raw[i:j + 1]
    try:
        d = json.loads(raw)
    except Exception:
        return None
    out = {}
    for k in ("basic", "apply", "transfer"):
        v = str(d.get(k, "")).strip()
        if len(v) < 8:
            return None
        out[k] = v
    return out


# ---------------------------------------------------------------- 注入

FALLBACK_CSS = """<style data-injected-css="layered-homework">
.lhw-panel{border:1px solid #dbe3ef;border-radius:12px;padding:18px 20px;background:#f8fafd}
.lhw-panel .phase-tag{display:inline-block;font-size:12px;color:#4361a8;background:#eaf1fb;
border-radius:999px;padding:3px 10px;margin-bottom:8px}
.lhw-panel h2{font-size:20px;margin:0 0 14px;color:#1b2a4a}
.lhw-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.lhw-card{background:#fff;border:1px solid #e3e9f2;border-radius:10px;padding:14px 16px}
.lhw-card strong{display:block;font-size:14px;color:#2a3f66;margin-bottom:6px}
.lhw-card p{margin:0;font-size:14px;line-height:1.7;color:#3a4a63}
@media(max-width:640px){.lhw-grid{grid-template-columns:1fr}}
</style>
"""


def render_section(t: dict[str, str]) -> str:
    esc = lambda s: (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return (
        '\n<section class="section text-module" id="tiered-practice" '
        'data-bloom-level="apply" data-scaffold="none" data-slot="115" %s>\n'
        '  <div class="lhw-panel">\n'
        '    <span class="phase-tag">分层作业</span>\n'
        '    <h2>作业分层：从会做到会迁移</h2>\n'
        '    <div class="lhw-grid">\n'
        '      <div class="lhw-card"><strong>⭐ 基础巩固</strong><p>%s</p></div>\n'
        '      <div class="lhw-card"><strong>⭐⭐ 能力应用</strong><p>%s</p></div>\n'
        '      <div class="lhw-card"><strong>⭐⭐⭐ 迁移挑战</strong><p>%s</p></div>\n'
        '    </div>\n'
        '  </div>\n'
        '</section>\n'
    ) % (INJECT_TAG, esc(t["basic"]), esc(t["apply"]), esc(t["transfer"]))


SLOT_RE = re.compile(r'data-slot=["\'](\d+)["\']')


def find_insert_pos(html: str) -> int:
    """分层作业属 slot 115：应落在记忆锚点(98)/小结(97)之后、AI 学伴(130)之前。"""
    secs = list(re.finditer(r"<section\b[^>]*>", html, re.I))
    if not secs:
        return -1

    def close_of(m) -> int:
        e = html.find("</section>", m.end())
        return e + len("</section>") if e >= 0 else m.end()

    slots = []
    for m in secs:
        s = SLOT_RE.search(m.group(0))
        slots.append((int(s.group(1)) if s else -1, m))

    # 优先：slot <= 115 中最大的那个，插在它后面
    cands = [(v, m) for v, m in slots if 0 <= v <= 115]
    if cands:
        return close_of(max(cands, key=lambda x: x[0])[1])
    # 次选：第一个 slot >= 120 的节之前
    for v, m in slots:
        if v >= 120:
            return m.start()
    # 兜底：最后一个 section 之后
    return close_of(secs[-1])


def ensure_css(html: str) -> str:
    if 'data-injected-css="layered-homework"' in html:
        return html
    i = html.rfind("</head>")
    if i < 0:
        return html
    return html[:i] + FALLBACK_CSS + html[i:]


def revert_file(path: Path) -> bool:
    html = path.read_text(encoding="utf-8", errors="ignore")
    if INJECT_TAG not in html:
        return False
    m = re.search(r'\n?<section\b[^>]*%s.*?</section>\n?' % re.escape(INJECT_TAG),
                  html, re.S | re.I)
    if not m:
        return False
    html = html[:m.start()] + "\n" + html[m.end():]
    path.write_text(html, encoding="utf-8")
    return True


# ---------------------------------------------------------------- 主流程

def load_targets(a) -> list[Path]:
    if a.ids:
        ids = [x.strip() for x in a.ids.split(",") if x.strip()]
        dirs = [COMMUNITY / i for i in ids]
    elif a.from_file:
        ids = [l.strip() for l in Path(a.from_file).read_text(encoding="utf-8").splitlines()
               if l.strip() and not l.startswith("#")]
        dirs = [COMMUNITY / i for i in ids]
    else:
        dirs = sorted(p for p in COMMUNITY.iterdir()
                      if p.is_dir() and (p / "index.html").is_file())
        if a.subject:
            dirs = [p for p in dirs if p.name.lower().startswith(a.subject.lower())]

    out = []
    for p in dirs:
        idx = p / "index.html"
        if not idx.is_file():
            continue
        h = idx.read_text(encoding="utf-8", errors="ignore")
        # 幂等检查必须对 --ids / --from-file / --all 三种入口一视同仁。
        # 历史坑（2026-10-09）：检查原先只写在 --all 的扫描分支里，--ids 与
        # --from-file 提前 return 绕过了它。结果批 2 被 SIGTERM 打断后，批 3
        # 拿同一份清单重跑，把已写入的 51 门又注入了一遍（出现 6 个卡片）。
        if not a.revert:
            if INJECT_TAG in h:
                continue      # 本脚本已注入过
            if any(m in h for m in MARKERS):
                continue      # 课件本来就有分层作业
            if SKIP_RE.search(h):
                continue      # 外部托管跳转壳 → 豁免（内容不在本地，注入只会造空话）
        else:
            if INJECT_TAG not in h:
                continue
        out.append(p)
    if a.pilot:
        out = out[: a.pilot]
    return out


def work(path: Path, apply: bool, revert: bool) -> tuple[str, str, str]:
    name = path.name
    try:
        if revert:
            if apply:
                ok = revert_file(path / "index.html")
                return (name, "REVERTED" if ok else "SKIP", "")
            return (name, "WOULD-REVERT", "")

        html = (path / "index.html").read_text(encoding="utf-8", errors="ignore")
        title = get_title(html)
        ctx = build_context(html)
        t = gen_tasks(title, ctx)
        if not t:
            return (name, "LLM-FAIL", title)
        pos = find_insert_pos(html)
        if pos < 0:
            return (name, "NO-POS", title)
        new = ensure_css(html[:pos]) + render_section(t) + html[pos:]
        if apply:
            (path / "index.html").write_text(new, encoding="utf-8")
        return (name, "OK" if apply else "DRYRUN",
                f"{t['basic']} ||| {t['apply']} ||| {t['transfer']}")
    except Exception as ex:  # noqa: BLE001
        return (name, f"ERROR: {ex}", "")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pilot", type=int, default=0)
    ap.add_argument("--ids")
    ap.add_argument("--from-file")
    ap.add_argument("--subject")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out")
    a = ap.parse_args()

    if not any([a.pilot, a.ids, a.from_file, a.all, a.subject]):
        ap.error("需指定 --pilot / --ids / --from-file / --subject / --all 之一")

    targets = load_targets(a)
    print(f"目标 {len(targets)} 门  apply={a.apply} revert={a.revert} model={MODEL}",
          file=sys.stderr)
    if not targets:
        return

    results = []
    with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
        futs = {ex.submit(work, p, a.apply, a.revert): p for p in targets}
        for i, f in enumerate(cf.as_completed(futs), 1):
            r = f.result()
            results.append(r)
            if i % 10 == 0 or i == len(targets):
                print(f"  ... {i}/{len(targets)}", file=sys.stderr)

    ok = sum(1 for r in results if r[1] in ("OK", "REVERTED"))
    dry = sum(1 for r in results if r[1] == "DRYRUN")
    bad = [r for r in results if r[1] not in ("OK", "REVERTED", "DRYRUN", "SKIP")]

    print(f"\n完成：成功 {ok}  预览 {dry}  失败 {len(bad)}")
    if bad:
        print("\n失败明细：")
        for n, s, t in bad[:20]:
            print(f"  {n}: {s}")

    if a.out:
        Path(a.out).write_text(
            json.dumps([{"id": n, "status": s, "tasks": t} for n, s, t in results],
                       ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"明细 -> {a.out}")

    if dry:
        print("\n=== 生成预览 ===")
        for n, s, t in results[:10]:
            if s == "DRYRUN":
                print(f"\n[{n}]")
                for part in t.split(" ||| "):
                    print("   " + part)


if __name__ == "__main__":
    main()
