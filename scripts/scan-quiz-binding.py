#!/usr/bin/env python3
"""scan-quiz-binding.py — 全库扫描 quiz 按钮绑定缺失
判定：HTML 有 .tu-opt / .choice[data-diagnosis] / .quiz-option 按钮，
但 script 块内没有对应选择器绑定 → 点击无反应（坏课件）
输出 JSON 明细 + 统计
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

BTN_PATTERNS = {
    "tu-opt": re.compile(r'class="tu-opt"'),
    "choice-diag": re.compile(r'class="choice[^"]*"[^>]*data-diagnosis|data-diagnosis[^>]*class="choice'),
    "quiz-option": re.compile(r'class="quiz-option"'),
}
# script 块内的绑定特征（选择器字符串出现即视为有绑定）
BIND_PATTERNS = {
    "tu-opt": re.compile(r'tu-opt'),
    "choice-diag": re.compile(r"querySelectorAll\(['\"]\.choice|matches\(['\"]\.choice|closest\(['\"]\.choice"),
    "quiz-option": re.compile(r'quiz-option'),
}


def scan_file(p):
    html = p.read_text(encoding="utf-8", errors="replace")
    scripts = "\n".join(re.findall(r"<script\b[^>]*>([\s\S]*?)</script>", html))
    # onclick 内联也算绑定
    issues = []
    for key, pat in BTN_PATTERNS.items():
        if not pat.search(html):
            continue
        if key == "choice-diag":
            # choice 里带 data-diagnosis 的才需要反馈绑定
            if not re.search(r'class="choice[^"]*"[^>]*data-diagnosis', html) and \
               not re.search(r'data-diagnosis[^>]*>', html):
                continue
        bound = bool(BIND_PATTERNS[key].search(scripts))
        # onclick 内联绑定
        if not bound and re.search(r'<button[^>]*class="[^"]*' + key.replace("-diag", "") + r'[^"]*"[^>]*onclick=', html):
            bound = True
        if not bound:
            n = len(pat.findall(html))
            issues.append((key, n))
    return issues


def main():
    bad, good, counts = [], 0, Counter()
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        issues = scan_file(f)
        if issues:
            bad.append({"id": cid, "issues": dict(issues)})
            for k, n in issues:
                counts[k] += 1
        else:
            good += 1
    print(f"扫描 {good + len(bad)} 个课件：{len(bad)} 个 quiz 按钮无绑定")
    for k, v in counts.most_common():
        print(f"  {k}: {v} 个课件")
    out = ROOT / "scripts" / "quiz-binding-scan.json"
    out.write_text(json.dumps(bad, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"明细 → {out}")
    pref = Counter(b["id"].split("-")[0] for b in bad)
    print("前缀分布:", dict(pref.most_common(10)))


if __name__ == "__main__":
    main()
