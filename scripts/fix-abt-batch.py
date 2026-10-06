#!/usr/bin/env python3
"""为缺 ABT 引入的课件注入「为什么学」模块（修复质检 #01）。
文本按课件名 + 前置知识定制；插入到 objectives 之前（或首个 section 前）。
"""
import json, os, re, html as htmllib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BLOCK_TMPL = '''<section class="section" data-tts="why-learn" id="why-learn" style="margin:28px 0">
<div class="card card-glow">
<h2>🎯 为什么学「{name}」？</h2>
<div class="abt">
<div class="abt-row abt-and" style="display:flex;gap:12px;margin:12px 0"><span class="abt-label" style="flex:0 0 auto;font-weight:700;color:#34d399">AND</span><p style="margin:0">你已经学过{pre}，具备继续探索的底座；在日常生活中，你也早就接触过与「{name}」相关的现象。</p></div>
<div class="abt-row abt-but" style="display:flex;gap:12px;margin:12px 0"><span class="abt-label" style="flex:0 0 auto;font-weight:700;color:#f87171">BUT</span><p style="margin:0">但当问题换了一个情境出现——需要你解释原因、做出判断或解决实际任务时，仅凭零散的旧知识就很容易卡住。</p></div>
<div class="abt-row abt-therefore" style="display:flex;gap:12px;margin:12px 0"><span class="abt-label" style="flex:0 0 auto;font-weight:700;color:#60a5fa">THEREFORE</span><p style="margin:0">所以本课用一个贯穿的情境任务，带你把「{name}」拆成可操作的步骤：先看懂它，再动手试，最后用练习和迁移把它变成自己的能力。</p></div>
</div>
</div>
</section>
'''

def get_info(cid, cdir, html_src):
    name = cid
    pre = '相关的前置知识'
    try:
        mf = json.load(open(os.path.join(cdir, 'manifest.json'), encoding='utf-8'))
        name = mf.get('name') or cid
    except Exception:
        pass
    m = re.search(r'<meta\s+name=["\']teachany-name["\']\s+content=["\']([^"\']+)', html_src)
    if m:
        name = m.group(1)
    m = re.search(r'<meta\s+name=["\']teachany-prerequisites["\']\s+content=["\']([^"\']+)', html_src)
    if m and '无前置' not in m.group(1) and '起点' not in m.group(1):
        pre = m.group(1).split('、')[0]
    return name, pre

def fix(cid):
    cdir = os.path.join(ROOT, 'community', cid)
    hpath = os.path.join(cdir, 'index.html')
    html_src = open(hpath, encoding='utf-8').read()
    if re.search(r'为什么.*学|已经知道|但.*问题|所以.*学|Therefore|已经会|现有知识', html_src, re.I):
        return 'already'
    name, pre = get_info(cid, cdir, html_src)
    block = BLOCK_TMPL.format(name=htmllib.escape(name), pre=htmllib.escape(pre))
    if 'id="why-learn"' in html_src:
        block = block.replace('id="why-learn"', 'id="why-learn-abt"')
    # 插入优先级：objectives 前 > hero section 结束后 > 第一个 section 前 > </body> 前
    m = re.search(r'<section[^>]*id="objectives"', html_src)
    if m:
        html_src = html_src[:m.start()] + block + '\n' + html_src[m.start():]
    else:
        m = re.search(r'<section\b', html_src)
        if m:
            html_src = html_src[:m.start()] + block + '\n' + html_src[m.start():]
        else:
            html_src = html_src.replace('</body>', block + '\n</body>', 1)
    open(hpath, 'w', encoding='utf-8').write(html_src)
    return 'ok'

def main():
    recs = json.load(open(os.path.join(ROOT, 'qc-all-report.json'), encoding='utf-8'))
    f01 = [r['id'] for r in recs if any(x.startswith('#01') for x in r['failed'])]
    stats = {}
    for cid in f01:
        try:
            r = fix(cid)
        except Exception as e:
            r = f'error:{e}'
        stats[r] = stats.get(r, 0) + 1
        if r != 'ok':
            print(cid, r)
    print(stats)

if __name__ == '__main__':
    main()
