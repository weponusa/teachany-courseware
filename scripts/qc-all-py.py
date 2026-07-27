#!/usr/bin/env python3
"""validate-courseware.cjs 的 Python 移植版：22 项校验逻辑逐项对齐，
用于在 node 不可用时做全量复检。输出与 qc-all-report.json 同构。
"""
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMUNITY = os.path.join(ROOT, 'community')

SKIP_REF = re.compile(r'^(https?:|data:|blob:|mailto:|tel:|javascript:|about:|chrome:|edge:)', re.I)
REF_RE = re.compile(r'''(?:\b(?:src|href|poster)\s*=\s*['"]([^'"]+)['"]|url\(\s*['"]?([^'")]+)['"]?\s*\))''', re.I)
SCRIPT_RE = re.compile(r'<script\b(?![^>]*type=["\']application/json["\'])[^>]*>[\s\S]*?</script>', re.I)
CARD_RE = re.compile(r'<div[^>]*class="[^"]*card[^"]*"[^>]*>([\s\S]*?)</div>', re.I)
STRIP_RE = re.compile(r'<(script|style|svg|textarea|template|table|details|button)\b[\s\S]*?</\1>', re.I)
META_RE = re.compile(r'<meta\s+name=["\']teachany-(\w+)["\']\s+content=["\']([^"\']*)["\']', re.I)
MP3_RE = re.compile(r'''["']([^"']+\.mp3)["']''', re.I)

def should_skip(ref):
    t = ref.strip()
    return not t or t.startswith('#') or t.startswith('{{') or SKIP_REF.match(t)

def resolve(dir_, clean):
    return os.path.join(ROOT, clean.lstrip('/')) if clean.startswith('/') else os.path.join(dir_, clean)

def missing_assets(dir_, html):
    scan = SCRIPT_RE.sub('', html)
    missing, seen = [], set()
    for m in REF_RE.finditer(scan):
        raw = (m.group(1) or m.group(2) or '').strip()
        if should_skip(raw):
            continue
        clean = raw.split('#')[0].split('?')[0]
        import urllib.parse
        try:
            clean = urllib.parse.unquote(clean)
        except Exception:
            pass
        if not clean:
            continue
        target = resolve(dir_, clean)
        key = (raw, target)
        if key in seen:
            continue
        seen.add(key)
        if not os.path.exists(target):
            missing.append(raw)
    return missing

def get_meta(html):
    return {m.group(1): m.group(2) for m in META_RE.finditer(html)}

def checks(html, meta, dir_):
    failed = []
    # 1 ABT
    if not re.search(r'为什么.*学|已经知道|但.*问题|所以.*学|Therefore|已经会|现有知识', html, re.I):
        failed.append('#01 ABT + 情境引入')
    # 2 pretest
    if not (re.search(r'前测|pre-?test|你已经知道什么|前置.*检测|先来测一测', html, re.I) or re.search(r'id=["\']pretest', html, re.I)):
        failed.append('#02 前测存在')
    # 3 interaction
    q = len(re.findall(r'quiz-option|quiz-opt|handleQuiz|data-conceptest|checkAnswer|onclick.*check|选择题|练习题|马上练', html, re.I))
    it = len(re.findall(r'draggable|ondrop|slider|range|input.*type', html, re.I))
    if q + it < 3:
        failed.append('#03 互动练习')
    # 4 diagnosis
    if not re.search(r'错.*因|为什么错|你.*搞反|你.*搞混|你.*忘记|你.*混淆|常见错误|注意区分|不要.*混|diagnosis|错在|再想想', html, re.I):
        failed.append('#04 诊断性反馈')
    # 5 posttest
    if not (re.search(r'后测|post-?test|学会了吗|学完.*检验|总结.*测试', html, re.I) or re.search(r'id=["\']posttest', html, re.I)):
        failed.append('#05 后测与学习闭环')
    # 6 Bloom
    levels = {
        'remember': r'识别|列举|说出|写出|选出哪个是|下面哪个',
        'understand': r'解释|比较|描述|为什么|区别|含义',
        'apply': r'计算|求解|运用|求.*值|代入|画出',
        'analyze': r'推导|区分|归纳|分析.*原因|判断.*为什么',
        'evaluate': r'判断.*是否正确|验证|评估|评价|哪个更',
        'create': r'设计|构建|提出|编写一个|创造|方案',
    }
    covered = sum(1 for p in levels.values() if re.search(p, html, re.I))
    if covered < 3:
        failed.append('#06 Bloom 层级覆盖')
    # 7 KG
    if not (re.search(r'teachany-node', html, re.I) and re.search(r'teachany-subject', html, re.I)):
        failed.append('#07 知识图谱溯源')
    # 8 deep
    if not (re.search(r'深层理解|five.?lens|五镜头|看见它|拆开它|解释它|比较它|迁移它|insight', html, re.I)
            or re.search(r'insight-box|深层|深入理解|本质|背后的原理', html, re.I)):
        failed.append('#08 五镜头深层理解')
    # 9 card density
    long_cards = 0
    for m in CARD_RE.finditer(html):
        inner_html = re.sub(r'^<div[^>]*>', '', m.group(0), flags=re.I)
        if re.search(r'class="[^"]*card', inner_html, re.I):
            continue
        t = STRIP_RE.sub('', m.group(1))
        t = re.sub(r'<(details|table)\b(?![\s\S]*?</\1>)[\s\S]*$', '', t, flags=re.I)
        t = re.sub(r'<[^>]+>', '', t)
        t = re.sub(r'\s+', '', t)
        cjk = len(re.findall(r'[\u4e00-\u9fff]', t))
        words = len(re.findall(r'[A-Za-z0-9]+', re.sub(r'[\u4e00-\u9fff]', ' ', t)))
        if cjk + words > 200:
            long_cards += 1
    if long_cards:
        failed.append('#09 卡片文字密度')
    # 10 layered
    if not re.search(r'Level\s*[123]|基础巩固|能力应用|迁移挑战|⭐|★|分层|必做|选做', html, re.I):
        failed.append('#10 三段式作业分层')
    # 11 prerequisites
    if not re.search(r'teachany-prerequisites', html, re.I):
        failed.append('#11 前置知识链')
    # 12 real scene
    if not re.search(r'生活|真实|实际|场景|例如.*日常|手机.*话费|出租车|弹簧|温度|购物|旅行|工程|实验', html, re.I):
        failed.append('#12 真实场景应用')
    # 13 meta
    required = ['teachany-node', 'teachany-subject', 'teachany-grade', 'teachany-version']
    miss = [m for m in required if not re.search(r'name=["\']' + m + r'["\']', html, re.I)]
    if miss:
        failed.append('#13 Meta 标签完整性')
    # 14 AI zone
    subject = meta.get('subject', '')
    if re.search(r'chinese|history|english|geography', subject, re.I):
        if not re.search(r'ai.?media|ai.?zone|ai.*互动|多模态|生成.*图|upload.*image', html, re.I):
            failed.append('#14 AI 多模态互动区')
    # 15 bilingual
    has_en = os.path.exists(os.path.join(dir_, 'index_en.html'))
    wants = re.search(r'output_formats[\s\S]*index_en|双语版?(课件|版本)|英文版(课件|版本)|bilingual\s*(courseware|version)', html, re.I)
    if wants and not has_en:
        failed.append('#15 双语版本')
    # 16 manifest
    if not os.path.exists(os.path.join(dir_, 'manifest.json')):
        failed.append('#16 课件打包')
    # 17 memory
    if not re.search(r'口诀|记忆|类比|就像|想象成|比喻|助记|锚点|窍门|秘诀|总结.*规律', html, re.I):
        failed.append('#17 记忆锚点')
    # 18 errors
    if not re.search(r'常见错误|容易.*错|搞反|搞混|混淆|误认为|错误.*类型|注意.*陷阱|易错', html, re.I):
        failed.append('#18 易错点覆盖')
    # 19 404
    if missing_assets(dir_, html):
        failed.append('#19 本地资源无 404')
    # 20 audio
    refs = [r for r in MP3_RE.findall(html) if not SKIP_REF.match(r)]
    valid = 0
    for r in refs:
        t = r.split('?')[0].split('#')[0]
        p = resolve(dir_, t)
        if os.path.exists(p) and os.path.getsize(p) >= 20 * 1024:
            valid += 1
    has_player = re.search(r'data-teachany-audio-playlist|teachany-audio-player\.js|audioPlaylist', html, re.I)
    if not (valid >= 3 and has_player):
        failed.append('#20 连续音频质量')
    # 21 video (optional)
    vrefs = re.findall(r'<(?:video|source)[^>]+src=["\']([^"\']+\.mp4)["\']', html, re.I)
    vtags = re.findall(r'<video\b[^>]*>', html, re.I)
    if vrefs or vtags:
        vvalid = 0
        for r in vrefs:
            t = r.split('?')[0].split('#')[0]
            p = resolve(dir_, t)
            if os.path.exists(p) and os.path.getsize(p) >= 20 * 1024:
                vvalid += 1
        ctrl = bool(vtags) and all(re.search(r'controls', t, re.I) and re.search(r'playsinline', t, re.I) for t in vtags)
        if not (vvalid >= 1 and ctrl):
            failed.append('#21 视频模块可见可控（可选）')
    # 22 canvas
    ok = (re.search(r'<canvas\b', html, re.I)
          and re.search(r'getContext\s*\(|draw\w*\s*\(', html, re.I)
          and re.search(r'addEventListener\s*\(\s*["\'](?:pointer|mouse|touch|click|input|change)', html, re.I)
          and re.search(r'<(?:input|select|button)\b', html, re.I))
    if not ok:
        failed.append('#22 Canvas 真实互动')
    return failed

def run_one(cid):
    cdir = os.path.join(COMMUNITY, cid)
    hpath = os.path.join(cdir, 'index.html')
    try:
        html = open(hpath, encoding='utf-8').read()
    except Exception:
        return {'id': cid, 'passed': 0, 'total': 22, 'failed': ['FATAL no index.html']}
    meta = get_meta(html)
    failed = checks(html, meta, cdir)
    return {'id': cid, 'passed': 22 - len(failed), 'total': 22, 'failed': failed}

def main():
    dirs = sorted(d for d in os.listdir(COMMUNITY)
                  if os.path.isdir(os.path.join(COMMUNITY, d))
                  and not d.startswith(('_', '.')) and d != 'archive'
                  and os.path.exists(os.path.join(COMMUNITY, d, 'index.html')))
    with ThreadPoolExecutor(max_workers=8) as ex:
        recs = list(ex.map(run_one, dirs))
    json.dump(recs, open(os.path.join(ROOT, 'qc-all-report.json'), 'w'), ensure_ascii=False, indent=1)
    import collections
    fail = [r for r in recs if r['failed']]
    print('total:', len(recs), ' with failures:', len(fail),
          ' full pass:', sum(1 for r in recs if r['passed'] == r['total']))
    cnt = collections.Counter()
    for r in fail:
        for x in r['failed']:
            cnt[x] += 1
    for k, v in cnt.most_common(30):
        print(f'{v:5d}  {k}')
    print('--- residual ---')
    for r in fail:
        print(r['id'], '|', '; '.join(r['failed']))

if __name__ == '__main__':
    main()
