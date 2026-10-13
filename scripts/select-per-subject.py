#!/usr/bin/env python3
"""select-per-subject.py — 每学科选出升级代表课件
评分：真模块资产（objectives/anchor/pretest/module/error-clinic/memory-anchor/posttest
      /lesson-focus 厚度/地图/图谱/音频/tu-quiz 交互数）加权
输出：每学科最佳候选 + 资产清单
"""
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"

SUBJECTS = {
    "bio": "生物", "chem": "化学", "phy": "物理", "math": "数学",
    "chn": "语文", "eng": "英语", "geo": "地理", "sci": "科学",
    "cs": "信息科技", "it": "信息技术",
}


def assets_of(cid, html):
    a = {}
    a["objectives"] = 'id="objectives"' in html
    a["anchor"] = 'id="anchor"' in html
    a["pretest"] = 'id="pretest"' in html
    a["modules"] = len(re.findall(r'id="module-\d+"', html))
    a["error_clinic"] = 'id="error-clinic"' in html
    a["memory_anchor"] = 'id="memory-anchor"' in html
    a["posttest"] = 'id="posttest"' in html
    a["lesson_focus"] = 'id="lesson-focus"' in html
    a["lesson_method"] = 'id="lesson-method"' in html
    a["map"] = "data-teachany-map" in html
    a["kg"] = "data-teachany-kg" in html
    a["audio"] = "data-teachany-audio-playlist" in html
    a["tu_quiz"] = html.count('class="tu-q"')
    a["navmap"] = 'id="navMapCanvas"' in html
    # lesson-focus 厚度
    m = re.search(r'id="lesson-focus"[\s\S]*?</section>', html)
    a["focus_chars"] = len(re.findall(r"[\u4e00-\u9fff]", re.sub(r"<[^>]+>", " ", m.group(0)))) if m else 0
    # 得分
    score = sum([
        10 * a["modules"], 5 * (a["objectives"] and 1 or 0), 5 * (a["anchor"] and 1 or 0),
        5 * (a["pretest"] and 1 or 0), 8 * (a["error_clinic"] and 1 or 0),
        5 * (a["memory_anchor"] and 1 or 0), 8 * (a["posttest"] and 1 or 0),
        6 * (a["lesson_focus"] and 1 or 0), 4 * (a["lesson_method"] and 1 or 0),
        10 * (a["map"] and 1 or 0), 6 * (a["kg"] and 1 or 0), 5 * (a["audio"] and 1 or 0),
        a["tu_quiz"], 4 * (a["navmap"] and 1 or 0), a["focus_chars"] // 100,
    ])
    return a, score


def main():
    rows = defaultdict(list)
    for f in sorted(COMMUNITY.glob("*/index.html")):
        cid = f.parent.name
        html = f.read_text(encoding="utf-8", errors="replace")
        if 'http-equiv="refresh"' in html[:3000]:
            continue
        pref = cid.split("-")[0]
        if pref not in SUBJECTS:
            continue
        a, score = assets_of(cid, html)
        rows[pref].append({"id": cid, "score": score, **a})
    out = {}
    for pref in sorted(rows):
        lst = sorted(rows[pref], key=lambda r: -r["score"])
        best = lst[0]
        out[SUBJECTS[pref]] = best
        on = [k for k, v in best.items() if v is True]
        print(f"{SUBJECTS[pref]:5s}({pref}) → {best['id']:44s} 分{best['score']:4d} | "
              f"模块{best['modules']} 交互{best['tu_quiz']} 地图{int(best['map'])} 图谱{int(best['kg'])} "
              f"音频{int(best['audio'])} 精讲{best['focus_chars']}字")
    (ROOT / "scripts" / "per-subject-selection.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n{len(out)} 个学科候选 → scripts/per-subject-selection.json")


if __name__ == "__main__":
    main()
