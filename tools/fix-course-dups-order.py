#!/usr/bin/env python3
"""课件通用修复：① 去重复内容卡 ② 把排在收尾区之后的正文页移回前面。

病灶（用户反馈「还是有重复模块和顺序问题」）
------------------------------------------
早期迁移把遗留区块整块兜底，造成两类问题：
  重复：同一个「知识精讲」卡在 2~3 个页里各出现一次；
  顺序：真正的正文模块（概念/练习/综合任务）被排到了 小结/分层作业/知识图谱/AI学伴 之后。

做法
----
去重：页内**内容卡**（div.card* / section.card*）文本归一化后，若与更早出现的卡完全相同
      （≥20 个汉字），删除后出现的那张；若某页删空则整页删除。
排序：以第一个「收尾页」（summary/homework/knowledge-graph/ai-tutor）为界，
      其后的正文页（concept/quiz/interactive/content）整体前移到该收尾页之前，保持相对顺序。
校验：标签平衡 + 容器闭合仍在末尾 + data-page-index 重排；文本只允许减少到「去重明细」之和。

用法:
  python3 tools/fix-course-dups-order.py --list                 # 干跑，列出会改什么
  python3 tools/fix-course-dups-order.py --only cid1,cid2       # 只处理指定课件
  python3 tools/fix-course-dups-order.py --apply                # 批量写入
  python3 tools/fix-course-dups-order.py --apply --all-migrated # 处理全部已分页课件
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _qa_gate import apply_guarded  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TERMINAL = {'summary', 'homework', 'knowledge-graph', 'ai-tutor'}
# ★ 受保护页型：这些页天生文字少（学伴 0 字、知识图谱 ~14 字），
#   绝不能被「删空页判定」删掉——否则课件缺标准模块（实测踩过：136 门丢 KG 页）
PROTECTED = {'ai-tutor', 'knowledge-graph', 'cover', 'objectives', 'homework', 'summary'}
REORDERABLE = {'concept', 'quiz', 'interactive', 'content'}


# ------------------------------------------------------------------ 工具
def balanced(s, start, tag):
    """返回匹配闭合标签的**结束**位置（含闭合标签）。"""
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    if not m0:
        raise ValueError(f'not <{tag}> at {start}')
    i = start + m0.end()
    d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return i + mm.end()
    raise ValueError(f'unbalanced <{tag}> at {start}')


def balanced_close_start(s, start, tag):
    """返回匹配闭合标签的**起始**位置（用于做「不含闭合标签」的切片边界）。"""
    m0 = re.match(r'<%s\b[^>]*>' % tag, s[start:], re.I)
    if not m0:
        raise ValueError(f'not <{tag}> at {start}')
    i = start + m0.end()
    d = 1
    for mm in re.finditer(r'<(/?)%s\b[^>]*(/?)>' % tag, s[i:], re.I):
        if mm.group(1):
            d -= 1
        elif not mm.group(2):
            d += 1
        if d == 0:
            return i + mm.start()
    raise ValueError(f'unbalanced <{tag}> at {start}')


def norm_text(s):
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S)
    return re.sub(r'\s+', '', re.sub(r'<[^>]+>', '', s))


def cjk_len(s):
    return len(re.findall(r'[一-鿿]', s))


def page_blocks(html):
    """返回 (prefix, [(block, tsh, ptype)], suffix)，以「容器内」为边界。
    用深度平衡切页，保证每块自带正确的闭合；容器闭合固定在 suffix 前。"""
    c = re.search(r'<div[^>]*class="[^"]*slide-container[^"]*"[^>]*>', html)
    if not c:
        raise ValueError('no slide-container')
    cont_open_end = c.end()
    # 容器闭合：取闭合标签的**起始**位置作为切片边界，避免把闭合标签自己包进内容区
    cont_close_start = balanced_close_start(html, c.start(), 'div')
    prefix = html[:cont_open_end]
    inner = html[cont_open_end:cont_close_start]
    suffix = html[cont_close_start:]
    pages = []
    i = 0
    pending = []          # 累积到下一个页面前的残留
    tail_junk = ''
    while True:
        m = re.search(r'<section[^>]*class="[^"]*slide-page[^"]*"[^>]*>', inner[i:])
        if not m:
            tail_junk = inner[i:]
            break
        s = i + m.start()
        if s > i:
            pending.append(inner[i:s])
        e = balanced(inner, s, 'section')
        block = inner[s:e]
        tsh = re.search(r'data-tsh="([^"]*)"', block)
        ptype = re.search(r'data-page-type="([^"]*)"', block)
        pages.append({'block': block, 'tsh': tsh.group(1) if tsh else '',
                      'type': ptype.group(1) if ptype else '',
                      'pre': ''.join(pending)})
        pending = []
        i = e
    # 残留分类：只有注释 / <style> / <script> / <link> 才算「可跟随页面移动」；
    # 出现真实内容标签（未闭合 section 等）就交人工——那类前移会把整页嵌套起来。
    def classify(t):
        t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
        t = re.sub(r'<(style|script|link|meta|noscript)\b.*?</\1>', '', t, flags=re.S | re.I)
        t = re.sub(r'<(style|script|link|meta)\b[^>]*/?>', '', t, flags=re.I)
        return t.strip()
    bad = [(pg['tsh'], classify(pg['pre'])) for pg in pages if classify(pg['pre'])]
    bad += [('(页尾)', classify(tail_junk))] if classify(tail_junk) else []
    if bad:
        c = re.sub(r'\s+', ' ', bad[0][1])[:60]
        raise ValueError(f'页间存在真实内容（需人工）: {c}')
    return prefix, pages, tail_junk, suffix


def top_cards(block):
    """页内内容卡：slide-inner 的顶层 div.card* / section.card*；只有一个 wrapper 时下钻。"""
    mi = re.search(r'<div class="slide-inner">', block)
    if not mi:
        return []
    start = mi.end()
    out = []
    j = start
    stop = balanced(block, block.index('<section'), 'section') if False else len(block)
    while True:
        m = re.search(r'<(div|section)[^>]*class="[^"]*\bcard\b[^"]*"[^>]*>', block[j:])
        if not m:
            break
        s = j + m.start()
        tag = m.group(1)
        e = balanced(block, s, tag)
        out.append((s, e))
        j = e
    return out


def dedup_cards(block, seen):
    """删除与该课件更早卡完全重复的内容卡。返回 (新block, 删除明细list)。"""
    removed = []
    for (s, e) in reversed(top_cards(block)):
        t = norm_text(block[s:e])
        if cjk_len(t) < 20:
            continue
        if t in seen:
            removed.append(block[s:e])
            block = block[:s] + block[e:]
        else:
            seen.add(t)
    return block, removed


def dedup_pages(pages):
    """整页重复：页文本完全相同则删后出现的那页（保留首次）。受保护页型不参与。"""
    seen = {}
    out, removed = [], []
    for p in pages:
        if p['type'] in PROTECTED:
            out.append(p); continue
        t = norm_text(p['block'])
        if cjk_len(t) >= 20 and t in seen:
            removed.append(p['block'])
            continue
        if cjk_len(t) >= 20:
            seen[t] = True
        out.append(p)
    return out, removed


def reorder_leftovers(pages):
    """把第一个收尾页之后的正文页前移到该收尾页之前。"""
    term = next((i for i, p in enumerate(pages) if p['type'] in TERMINAL), None)
    if term is None:
        return pages, 0
    head = pages[:term]
    tail = pages[term:]
    leftovers = [p for p in tail if p['type'] in REORDERABLE]
    rest = [p for p in tail if p['type'] not in REORDERABLE]
    if not leftovers:
        return pages, 0
    # 收尾区内部若还夹着正文页，保持「前移」语义但避免打乱收尾页相对顺序
    return head + leftovers + rest, len(leftovers)


def fix_course(path, apply=False):
    html = path.read_text(encoding='utf-8')
    try:
        prefix, pages, junk, suffix = page_blocks(html)
    except Exception as e:  # noqa: BLE001
        return {'skip': f'结构异常: {e}'}
    if not pages:
        return {'skip': '无页'}
    n_before = len(pages)
    # 1) 去重（先做卡片级，再做整页级）
    seen = set()
    dup_cards = []
    dup_card_raw = []
    new_pages = []
    for p in pages:
        nb, removed = dedup_cards(p['block'], seen)
        dup_cards.extend(removed)
        dup_card_raw.extend(removed)
        p = dict(p, block=nb)
        # 删空页判定：页内无 ≥20 汉字文本（**受保护页型除外**）
        if cjk_len(norm_text(nb)) < 20 and p['type'] not in PROTECTED:
            dup_card_raw.append(nb)          # 整页文本也算「应被删掉的量」
            dup_cards.append('<整页删除: ' + p['tsh'] + '>')
            continue
        new_pages.append(p)
    pages, dup_pages = dedup_pages(new_pages)
    dup_card_raw.extend(dup_pages)
    # 2) 顺序
    pages, moved = reorder_leftovers(pages)
    # 3) 组装 + 重排 index（样式/脚本跟随其后页面；页尾残留放最后）
    inner = ''.join(p.get('pre', '') + p['block'] for p in pages) + junk
    new_html = prefix + inner + suffix
    cnt = [0]
    new_html = re.sub(r'data-page-index="\d+"',
                      lambda m: 'data-page-index="%d"' % (cnt.__setitem__(0, cnt[0] + 1) or cnt[0] - 1),
                      new_html)
    # 4) 校验
    for t in ('section', 'div', 'figure'):
        if len(re.findall(r'<%s\b' % t, new_html)) != len(re.findall(r'</%s>' % t, new_html)):
            return {'skip': f'<{t}> 不平衡'}
    # 页数：重新解析新文件，必须与预期一致（能挡住容器闭合错位/嵌套页）
    try:
        _, pages2, _, _ = page_blocks(new_html)
    except Exception as e:  # noqa: BLE001
        return {'skip': f'新结构无法解析: {e}'}
    if len(pages2) != len(pages):
        return {'skip': f'新结构页数 {len(pages2)} != 预期 {len(pages)}'}
    # 文本损失必须恰好等于「去重删除量」——防止静默丢内容
    removed_text = ''.join(norm_text(c) for c in dup_card_raw)
    old_t, new_t = norm_text(html), norm_text(new_html)
    loss = len(old_t) - len(new_t)
    if abs(loss - len(removed_text)) > 2:
        return {'skip': f'文本损失 {loss} ≠ 去重量 {len(removed_text)}，疑静默丢内容'}
    info = {
        'cid': path.parent.name,
        'pages_before': n_before,
        'pages_after': len(pages),
        'dup_cards': len([d for d in dup_cards if isinstance(d, str) or True]),
        'dup_pages': len(dup_pages),
        'moved': moved,
    }
    if apply and (dup_cards or moved):
        ok, why = apply_guarded(path, new_html, path.parent.name)
        info['gate'] = why
        if not ok:
            info['changed'] = False
            info['gate_blocked'] = True
            return info
    info['changed'] = bool(dup_cards or moved)
    return info


def migrated_courses():
    out = []
    for base in ('community', 'examples'):
        d = ROOT / base
        if not d.is_dir():
            continue
        for c in sorted(d.iterdir()):
            f = c / 'index.html'
            if not f.is_file() or c.name == 'drafts':
                continue
            h = f.read_text(encoding='utf-8', errors='ignore')
            if 'id="slide-container"' in h and 'data-page-type=' in h:
                out.append(f)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--only', default='')
    ap.add_argument('--all-migrated', action='store_true')
    ap.add_argument('--out', default='/tmp/fix-dups-order.json')
    args = ap.parse_args()

    only = set(x for x in args.only.split(',') if x)
    files = migrated_courses()
    if only:
        files = [f for f in files if f.parent.name in only]
    elif not args.all_migrated:
        print('需指定 --only 或 --all-migrated'); return 1

    rows, changed, skipped = [], [], []
    for f in files:
        r = fix_course(f, apply=args.apply)
        rows.append(r)
        if r.get('skip'):
            skipped.append((f.parent.name, r['skip']))
        elif r.get('changed'):
            changed.append(r)
    Path(args.out).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding='utf-8')
    print(f'扫描 {len(files)} 门：需修复 {len(changed)} 门，跳过 {len(skipped)} 门'
          + ('（已写入）' if args.apply else '（干跑，未写入）'))
    total_cards = sum(r['dup_cards'] for r in changed)
    total_moved = sum(r['moved'] for r in changed)
    print(f'去重卡 {total_cards} 处，前移正文页 {total_moved} 页')
    for r in sorted(changed, key=lambda x: -(x['dup_cards'] + x['moved']))[:25]:
        print(f"  {r['cid']:42s} 页 {r['pages_before']}→{r['pages_after']}  去重{r['dup_cards']} 前移{r['moved']}")
    if skipped:
        print('跳过明细（前 10）:')
        for cid, why in skipped[:10]:
            print(f'  {cid}: {why}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
