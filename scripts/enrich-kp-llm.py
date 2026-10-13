#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""用 OpenRouter LLM 为缺失内容的知识点批量生成「学习包」，回填 kp 卫星文件。

目标：补齐非中国课标（curriculum != 'cn'）知识点的学习指南、习题、易错点、现实联系、扩展片段，
     使其结构对齐中国课标 950 个知识点的「满配」形态。

安全与幂等：
  - 只写衍生/内容字段（supplements / exercises / errors / real_world / _meta），不动元数据。
  - 写前备份到 data/kp/_backups/<run-id>/。
  - 断点续传：进度写入 <progress> 文件；已完成 kp_id 跳过。
  - 幂等：已有 TAG 标记且 exercises 非空则跳过（--force 可重跑）。

用法：
  python3 scripts/enrich-kp-llm.py --limit 10            # 试点 10 个
  python3 scripts/enrich-kp-llm.py --subject math        # 单学科
  python3 scripts/enrich-kp-llm.py --curriculum ap       # 单课程体系
  python3 scripts/enrich-kp-llm.py --all                 # 全量（8682）
  python3 scripts/enrich-kp-llm.py --all --concurrency 16
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KP_ROOT = ROOT / "data" / "kp"

OR_URL = "https://openrouter.ai/api/v1/chat/completions"
OR_KEY = os.environ.get("OPENROUTER_API_KEY", "").strip()
MODEL = os.environ.get("ENRICH_LLM_MODEL", "deepseek/deepseek-chat")
TAG = "kp_llm_enrich_2026-08-19"

CURRICULUM_LABEL = {
    "cn": "中国课标",
    "ap": "AP 美国大学先修课程",
    "ib": "IB 国际文凭课程",
    "cambridge": "剑桥国际课程",
    "us": "美国课程标准",
    None: "开放知识图谱（进阶学科）",
}

SUBJECT_ZH = {
    "math": "数学", "physics": "物理", "chemistry": "化学", "biology": "生物",
    "history": "历史", "geography": "地理", "chinese": "语文", "english": "英语",
    "science": "科学", "info-tech": "信息技术", "cs": "计算机科学",
    "computer-science": "计算机科学", "economics": "经济学", "psychology": "心理学",
    "politics": "政治", "art": "艺术", "design": "设计", "pe": "体育",
    "advanced-math": "高等数学", "advanced-physics": "高等物理",
    "advanced-chemistry": "高等化学", "advanced-biology": "高等生物",
    "engineering": "工程学", "earth-space": "地球与空间科学",
    "formal-sciences": "形式科学", "humanities": "人文学科",
    "aerospace-engineering": "航空航天工程", "agricultural-engineering": "农业工程",
    "chemical-engineering": "化学工程", "civil-engineering": "土木工程",
    "hydraulic-engineering": "水利工程", "naval-engineering": "船舶工程",
    "nuclear-engineering": "核工程", "inquiry": "探究学习", "other": "综合",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def dump_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def collect_targets(args) -> list[tuple[str, str]]:
    """返回 (kp_id, rel_path) 列表，按 args 过滤。"""
    index = load_json(KP_ROOT / "_index.json").get("kps", {})
    targets: list[tuple[str, str]] = []
    for kp_id, rel in sorted(index.items()):
        if "_backups" in rel:
            continue
        path = ROOT / rel
        if not path.is_file():
            continue
        try:
            data = load_json(path)
        except Exception:
            continue
        cur = data.get("curriculum")
        # 中国课标已满配，跳过
        if cur == "cn":
            continue
        if args.curriculum and cur != args.curriculum:
            continue
        subject = data.get("subject") or ""
        if args.subject and subject != args.subject:
            continue
        # 幂等：已含 TAG 且 exercises 非空 且扩展片段非空 → 跳过（除非 --force）
        if not args.force:
            sup = data.get("supplements", {})
            if (data.get("exercises") or []) and sup.get("deep_textbook_snippets") and TAG in (data.get("_meta", {}).get("sources") or []):
                continue
        targets.append((kp_id, rel))
    return targets


def build_prompt(data: dict[str, Any]) -> str:
    name = data.get("name") or data.get("name_en") or data.get("kp_id") or ""
    name_en = data.get("name_en") or ""
    subject = data.get("subject") or ""
    subject_zh = SUBJECT_ZH.get(subject, data.get("subject_name") or subject or "综合")
    cur = data.get("curriculum")
    cur_label = CURRICULUM_LABEL.get(cur, "开放知识图谱")
    stage = data.get("stage") or ""
    grade = data.get("grade") or ""
    domain = data.get("domain_name") or data.get("domain_id") or ""
    cps = data.get("curriculum_points") or []
    cp_text = "\n".join(f"- {c}" for c in cps) if cps else "（无官方课标条款，请依据学科常识与标准定义生成）"

    return f"""你是 K12 与大学先修/进阶学科的资深教研专家。请为下面这个知识点生成一份结构化的中文学习内容包。

【知识点信息】
- 中文名：{name}
- 英文名：{name_en}
- 学科：{subject_zh}
- 课程体系：{cur_label}
- 学段：{stage}；年级/水平：{grade}
- 所属领域：{domain}
- 大纲/课标要点：
{cp_text}

【内容要求】
- 用规范的中文讲解，学科关键术语用「中文（English term）」形式首次标注。
- 内容准确专业，贴合该课程体系的难度水平，不得编造事实。
- 习题必须有明确答案和简洁解析；易错点要真实、具体，不要空话套话。
- **禁止使用 LaTeX 数学公式**：所有公式、符号一律用 Unicode 字符（如 x²、√、∑、∈、⊂、→、∞、π）或中文文字描述（如"a 的平方""x 属于集合 G"）。严禁出现反斜杠（\\）和美元符号（$）等 LaTeX 标记，否则会破坏 JSON 格式。

【输出格式】只输出一个 JSON 对象（不要 markdown 代码块、不要解释），结构如下：
{{
  "learning_guide": "800-1500 字的知识点详解（Markdown，含：核心概念定义、关键性质或方法、与相关知识的联系、典型应用示例）",
  "exercises": [
    {{"stem": "题干", "answer": "答案", "explain": "解析", "type": "concept"}},
    {{"stem": "题干", "answer": "答案", "explain": "解析", "type": "apply"}},
    {{"stem": "题干", "answer": "答案", "explain": "解析", "type": "analyze"}}
  ],
  "errors": [
    {{"description": "具体易错点或常见误解", "type": "conceptual"}},
    {{"description": "具体易错点或常见误解", "type": "procedural"}}
  ],
  "real_world": ["现实联系或应用场景 1", "现实联系或应用场景 2"],
  "knowledge_snippets": ["扩展知识片段 1", "扩展知识片段 2", "扩展知识片段 3"]
}}

请严格按照 JSON 输出。"""


def extract_json(text: str) -> dict[str, Any] | None:
    if not text:
        return None
    text = text.strip()
    # 去掉可能的 markdown 代码块
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    if m:
        text = m.group(1)
    # 找到第一个 { 到最后一个 }
    s = text.find("{")
    e = text.rfind("}")
    if s == -1 or e == -1 or e <= s:
        return None
    try:
        return json.loads(text[s:e + 1])
    except Exception:
        return None


def call_llm(prompt: str) -> str | None:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

    if not OR_KEY:
        raise RuntimeError("缺少 OPENROUTER_API_KEY 环境变量")

    session = requests.Session()
    retry = Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=2.0,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    adapter = HTTPAdapter(max_retries=retry, pool_connections=16, pool_maxsize=16)
    session.mount("https://", adapter)

    last_err: Exception | None = None
    for attempt in range(6):
        try:
            r = session.post(
                OR_URL,
                headers={"Authorization": f"Bearer {OR_KEY}", "Content-Type": "application/json"},
                json={
                    "model": MODEL,
                    "messages": [
                        {"role": "system", "content": "你是严谨的学科教研专家，只输出合法 JSON，不输出任何多余内容。"},
                        {"role": "user", "content": prompt},
                    ],
                    "temperature": 0.5,
                    "max_tokens": 5000,
                },
                timeout=(30, 180),
            )
            if r.status_code == 429:
                time.sleep(10 * (attempt + 1))
                continue
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception as ex:  # noqa: BLE001
            last_err = ex
            time.sleep(6 * (attempt + 1))
    raise RuntimeError(f"LLM 调用失败: {last_err}")


def apply(data: dict[str, Any], g: dict[str, Any]) -> bool:
    """把 LLM 生成结果回填到 data，返回是否有变化。"""
    changed = False
    sup = data.setdefault("supplements", {})

    guide = (g.get("learning_guide") or "").strip()
    if guide and len(guide) >= 80:
        sup["curriculum_md_raw"] = guide
        sup["curriculum_md_source"] = TAG
        changed = True

    snippets = g.get("knowledge_snippets") or []
    if isinstance(snippets, list) and snippets:
        deep = []
        for i, s in enumerate(snippets, 1):
            t = str(s).strip()
            if len(t) >= 20:
                deep.append({
                    "source": f"{TAG}/llm",
                    "text": t[:1600],
                    "score": 90 - i,
                    "match_terms": [],
                    "source_type": "llm_generated",
                })
        if deep:
            sup["deep_textbook_snippets"] = deep
            sup["deep_textbook_source"] = TAG
            sup["deep_textbook_enriched_at"] = utc_now()
            changed = True

    exs = g.get("exercises") or []
    if isinstance(exs, list) and exs:
        out = []
        for i, e in enumerate(exs[:3], 1):
            if not isinstance(e, dict):
                continue
            stem = str(e.get("stem") or "").strip()
            ans = str(e.get("answer") or "").strip()
            if not stem:
                continue
            out.append({
                "id": f"q-llm-{i}",
                "stem": stem,
                "answer": ans,
                "type": e.get("type") or "short_answer",
                "source": TAG,
            })
            if e.get("explain"):
                out[-1]["explain"] = str(e["explain"]).strip()
        if out:
            data["exercises"] = out
            # 例题：取第一题
            sup["deep_worked_example"] = {
                "stem": out[0]["stem"],
                "solution_outline": out[0].get("answer", ""),
                "source": TAG,
            }
            changed = True

    errs = g.get("errors") or []
    if isinstance(errs, list) and errs:
        out = []
        for i, e in enumerate(errs[:2], 1):
            if not isinstance(e, dict):
                continue
            desc = str(e.get("description") or "").strip()
            if not desc:
                continue
            out.append({
                "id": f"err-llm-{i}",
                "description": desc,
                "type": e.get("type") or "conceptual",
                "source": TAG,
            })
        if out:
            data["errors"] = out
            changed = True

    rw = g.get("real_world") or []
    if isinstance(rw, list) and rw:
        items = [str(x).strip() for x in rw if str(x).strip()]
        if items:
            data["real_world"] = items[:2]
            sup["real_world"] = items[:2]
            changed = True

    if changed:
        meta = data.setdefault("_meta", {})
        sources = meta.setdefault("sources", [])
        if isinstance(sources, list) and TAG not in sources:
            sources.append(TAG)
        meta["kp_llm_enrich_at"] = utc_now()
    return changed


def process_one(kp_id: str, rel: str, args, backup_root: Path) -> dict[str, Any]:
    path = ROOT / rel
    data = load_json(path)
    prompt = build_prompt(data)
    # 解析失败/内容不完整多为随机波动（temperature 0.5），失败即重试，最多 3 次
    g = None
    raw = ""
    for _attempt in range(3):
        raw = call_llm(prompt)
        g = extract_json(raw)
        if g is not None:
            exs = g.get("exercises") or []
            snips = g.get("knowledge_snippets") or []
            # 习题与扩展片段必须真正可落库（与 apply 的过滤标准一致），否则视为偷懒输出，重试
            has_ex = any(
                isinstance(e, dict) and str(e.get("stem") or "").strip()
                for e in (exs if isinstance(exs, list) else [])
            )
            has_snip = any(
                len(str(s).strip()) >= 20
                for s in (snips if isinstance(snips, list) else [])
            )
            if has_ex and has_snip:
                break
            g = None
        time.sleep(2)
    if g is None:
        return {"kp_id": kp_id, "status": "parse_fail", "raw_head": (raw or "")[:120]}
    changed = apply(data, g)
    if not changed:
        return {"kp_id": kp_id, "status": "no_change"}
    if not args.dry_run:
        # 备份
        target = backup_root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        dump_json(path, data)
    return {"kp_id": kp_id, "status": "ok", "name": data.get("name") or data.get("name_en")}


def main() -> int:
    ap = argparse.ArgumentParser(description="LLM 批量补充知识点学习包")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--subject", default="")
    ap.add_argument("--curriculum", default="")
    ap.add_argument("--concurrency", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--progress", default="")
    args = ap.parse_args()

    if not OR_KEY:
        print("缺少 OPENROUTER_API_KEY 环境变量，请先 export")
        return 1

    targets = collect_targets(args)
    if args.limit > 0:
        targets = targets[: args.limit]
    print(f"目标知识点数: {len(targets)}（模型 {MODEL}，并发 {args.concurrency}）")

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_root = KP_ROOT / "_backups" / f"llm-enrich-{run_id}"
    progress_path = Path(args.progress) if args.progress else KP_ROOT / "_backups" / f"llm-enrich-progress-{run_id}.jsonl"

    # 断点续传：加载已完成（仅 status==ok 视为完成，失败项下次重试）
    done: set[str] = set()
    if progress_path.exists():
        for line in progress_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                if rec.get("status") == "ok":
                    done.add(rec.get("kp_id", ""))
            except Exception:
                continue
    pending = [(k, r) for k, r in targets if k not in done]
    print(f"已完成: {len(done)}，待处理: {len(pending)}")

    ok = fail = parse_fail = 0
    if args.dry_run:
        # dry-run 只打印前 5 个预览，不调 LLM
        for k, r in pending[:5]:
            print(f"  [dry] {k} -> {r}")
        return 0

    lock = __import__("threading").Lock()

    def run(item):
        k, r = item
        try:
            res = process_one(k, r, args, backup_root)
        except Exception as ex:  # noqa: BLE001
            res = {"kp_id": k, "status": "fail", "err": str(ex)[:200]}
        with lock:
            progress_path.parent.mkdir(parents=True, exist_ok=True)
            with open(progress_path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(res, ensure_ascii=False) + "\n")
        return res

    with ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futs = [pool.submit(run, item) for item in pending]
        for fut in as_completed(futs):
            res = fut.result()
            st = res.get("status")
            if st == "ok":
                ok += 1
            elif st == "parse_fail":
                parse_fail += 1
            else:
                fail += 1
            if (ok + fail + parse_fail) % 20 == 0:
                print(f"  进度: 成功 {ok} / 解析失败 {parse_fail} / 失败 {fail}")

    print(f"\n完成：成功 {ok}，解析失败 {parse_fail}，失败 {fail}")
    print(f"进度文件: {progress_path}")
    print(f"备份目录: {backup_root.relative_to(ROOT)}" if not args.dry_run else "dry-run")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
