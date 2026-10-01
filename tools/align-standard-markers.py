#!/usr/bin/env python3
"""标准标记对齐：把**已存在**的教学要素对齐到标准标记（不新增教学内容）。

背景
----
pre-push 钩子对每个变更课件跑 validate-courseware.py，其中若干硬规则是「结构标记」类：
  · 缺少 ConcepTest 检查点（data-conceptest="true"）
  · <title> 不含 "TeachAny v{version}" 标识
实测发现：不少课件**已有**检查点页面（data-page-type="quiz" + 选择题），只是没打标记；
标题也只是漏了版本后缀。本工具只做「对齐」不做「造内容」：

  ConcepTest：在**已有 quiz 页**里挑一个真正的检查点（优先 tsh/tts 含 概念/即时/检查点/
              conceptest/例题演练，其次排除前测/后测后的 quiz 页），页内必须有作答控件
              （data-correct / quiz-option / tu-opt / 选择题），否则跳过。
  标题      ：<title> 补 " · TeachAny v<manifest.teachany_version 或 7.20>"。

每处改动都过 tools/_qa_gate.py 闸门：质检错误数不得增加，否则自动回滚。

用法:
  python3 tools/align-standard-markers.py --only a,b --list
  python3 tools/align-standard-markers.py --from-errlist /tmp/err-cids2.txt --apply
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from _qa_gate import apply_guarded, qa_errors  # noqa: E402

CHECKPOINT_HINT = re.compile(r'概念|即时|检查点|conceptest|例题演练|小测|巩固', re.I)
EXCLUDE_HINT = re.compile(r'前测|pretest|后测|posttest|达标|诊断', re.I)
QUIZ_CONTENT = re.compile(r'data-correct|quiz-option|tu-opt|class="choice"|name="answer"', re.I)


def page_spans(html):
    c = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
    if not c:
        return None
    out, j = [], c.end()
    while True:
        m = re.search(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', html[j:])
        if not m:
            break
        s = j + m.start()
        e = _balanced(html, s, 'section')
        if e is None:
            return None
        out.append((s, e, html[s:e]))
        j = e
    return out


def _balanced(s, start, tag):
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    if not m0:
        return None
    i = start + m0.end()
    d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return i + mm.end()
    return None


def add_conceptest(html):
    if re.search(r'data-conceptest=["\']true["\']', html, re.I):
        return html, 'marker-exists'
    pages = page_spans(html)
    if not pages:
        return html, 'no-container'
    quizzes = [(s, e, b) for (s, e, b) in pages
               if re.search(r'data-page-type="quiz"', b[:200], re.I)]
    if not quizzes:
        return html, 'no-quiz-page'
    def score(item):
        _s, _e, b = item
        head = b[:300]
        tsh = (re.search(r'data-tsh="([^"]*)"', head) or [None, ''])[1] if False else ''
        m = re.search(r'data-tsh="([^"]*)"', head)
        tsh = m.group(1) if m else ''
        m2 = re.search(r'data-tts="([^"]*)"', head)
        tts = m2.group(1) if m2 else ''
        tag = tsh + ' ' + tts
        s = 0
        if CHECKPOINT_HINT.search(tag):
            s += 10
        if EXCLUDE_HINT.search(tag):
            s -= 5
        return s
    quizzes.sort(key=score, reverse=True)
    for (s, e, b) in quizzes:
        if not QUIZ_CONTENT.search(b):
            continue
        m = re.search(r'<section[^>]*data-page-type="quiz"', b)
        if not m:
            continue
        pos = s + m.end()
        new = html[:pos] + ' data-conceptest="true"' + html[pos:]
        return new, 'marked'
    return html, 'no-checkpoint-content'


def add_module_markers(html, need=3):
    """把 data-page-type="concept" 且内容充实的页标注 class="... concept-module"。
    ★ 一次性收集所有插入点，按偏移**逆序**插入，避免旧偏移导致错位。"""
    if len(re.findall(r"class=['\"][^'\"]*concept", html)) >= need:
        return html, 'module-ok'
    pages = page_spans(html)
    if not pages:
        return html, 'no-container'
    targets = []
    for (s, e, b) in pages:
        if len(targets) >= need:
            break
        head = b[:250]
        if 'data-page-type="concept"' not in head:
            continue
        body = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', b, flags=re.S)
        if len(re.findall(r'[一-鿿]', re.sub(r'<[^>]+>', ' ', body))) < 120:
            continue
        m = re.search(r'<section[^>]*class="([^"]*)"', b)
        if not m or 'concept' in m.group(1):
            continue
        targets.append(s + m.end(1))
    if not targets:
        return html, 'no-concept-page'
    for pos in sorted(targets, reverse=True):
        html = html[:pos] + ' concept-module' + html[pos:]
    return html, 'module-marked-%d' % len(targets)


def fix_title(html, manifest):
    m = re.search(r'<title>([^<]*)</title>', html)
    if not m:
        return html, 'no-title'
    t = m.group(1)
    if 'TeachAny v' in t:
        return html, 'title-ok'
    ver = str((manifest or {}).get('teachany_version') or '7.20').strip() or '7.20'
    new_title = t.rstrip() + ' · TeachAny v' + ver
    return html[:m.start()] + '<title>' + new_title + '</title>' + html[m.end():], 'title-fixed'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='')
    ap.add_argument('--from-errlist', default='')
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--list', action='store_true')
    args = ap.parse_args()

    if args.from_errlist:
        cids = Path(args.from_errlist).read_text(encoding='utf-8').split()
    else:
        cids = [x.strip() for x in args.only.split(',') if x.strip()]
    if not cids:
        print('需 --only 或 --from-errlist'); return 1

    rows = []
    for cid in cids:
        d = ROOT / 'community' / cid
        f = d / 'index.html'
        if not f.is_file():
            rows.append({'cid': cid, 'skip': 'no file'}); continue
        html = f.read_text(encoding='utf-8')
        man = {}
        mf = d / 'manifest.json'
        if mf.is_file():
            try:
                man = json.loads(mf.read_text(encoding='utf-8'))
            except Exception:  # noqa: BLE001
                man = {}
        r = {'cid': cid}
        h2, w1 = fix_title(html, man)
        r['title'] = w1
        h3, w2 = add_conceptest(h2)
        r['concepest'] = w2
        h4, w3 = add_module_markers(h3)
        r['modules'] = w3
        h3 = h4
        if h3 == html:
            rows.append(r); continue
        r['before_errors'] = qa_errors(cid)[0]
        if args.apply:
            ok, why = apply_guarded(f, h3, cid)
            r['gate'] = why
            r['applied'] = ok
            r['after_errors'] = qa_errors(cid)[0]
        rows.append(r)

    out = Path('/tmp/align-markers.json')
    out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    done = [r for r in rows if r.get('applied')]
    print(f'处理 {len(rows)} 门：改动 {len(done)} 门（{"已写入" if args.apply else "干跑"}）')
    import collections
    print('ConcepTest:', collections.Counter(r.get('concepest') for r in rows))
    print('module   :', collections.Counter(r.get('modules') for r in rows))
    print('title    :', collections.Counter(r.get('title') for r in rows))
    for r in done[:10]:
        print(f"  {r['cid']:42s} {r.get('gate', '')}")
    print(f'明细 → {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
