#!/usr/bin/env python3
"""批量迁移：备份 → 注外壳 → 结构重排（带内容门禁）→ 出汇总。

用法：
  python3 tools/migrate-batch.py chn-h-idiom-usage-h chn-h-info-reading ...
  python3 tools/migrate-batch.py --list             # 列出剩余可迁移对象
  python3 tools/migrate-batch.py --next 11          # 迁移清单里接下来的 N 门

每一步都会：
  1. 从 **git HEAD** 取原始文件备份到 <workdir>/.workbuddy/migration-backups/
     （不要用 /tmp —— 跨会话会被清理，实测踩过）
  2. tools/migrate-to-v2-shell.py 注入分页外壳
  3. tools/migrate-legacy-blocks.py --verify 重排为 16 页（保留率 <98% 拒绝写入）
  4. 静态复核页数，并打印汇总表

**渲染验收不在这里做**（需要 Playwright，较慢）——
   请用 tools/verify-migration.py 或单独跑浏览器检查：
   #slide-container 直属 .slide-page == 16、.sidenav-dot == 16、
   点第 8 点后 scrollTop > 0、overflowY == 'auto'、pageerror == 0
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKUP = Path.home() / 'WorkBuddy' / '2026-09-19-21-28-58' / '.workbuddy' / 'migration-backups'
PY = sys.executable
CANON = ['cover', 'interactive', 'objectives', 'quiz', 'concept', 'interactive', 'concept',
         'interactive', 'concept', 'quiz', 'interactive', 'quiz', 'summary', 'homework',
         'knowledge-graph', 'ai-tutor']


def sh(args):
    return subprocess.run([PY, str(ROOT / 'tools' / args[0])] + args[1:],
                          capture_output=True, text=True, cwd=ROOT)


def git_orig(cid):
    """从 git HEAD 取原始 index.html（本地改动未提交，HEAD 即迁移前状态）"""
    for base in ('community', 'examples'):
        rel = f'{base}/{cid}/index.html'
        r = subprocess.run(['git', 'show', f'HEAD:{rel}'], capture_output=True, cwd=ROOT)
        if r.returncode == 0 and r.stdout:
            return rel, r.stdout.decode('utf-8', errors='replace')
    return None, None


def backup(cid):
    rel, content = git_orig(cid)
    if not content:
        return None
    BACKUP.mkdir(parents=True, exist_ok=True)
    f = BACKUP / f'{cid}.orig.html'
    if not f.exists():
        f.write_text(content, encoding='utf-8')
    return f


def list_targets(min_pages=6):
    """自己扫仓库，别解析 migrate-to-v2-shell.py --list 的文本输出
    （它只打印前 40 行，会漏掉其余；实测 193 门被截成 40）"""
    out = []
    for base in ('community', 'examples'):
        d = ROOT / base
        if not d.is_dir():
            continue
        for c in sorted(d.iterdir()):
            f = c / 'index.html'
            if not f.is_file():
                continue
            h = f.read_text(encoding='utf-8', errors='ignore')
            pages = len(re.findall(r'class="slide-page', h))
            if pages >= min_pages and 'id="slide-sidenav"' not in h:
                out.append(c.name)
    return out


def check(cid):
    """静态复核：页数 + 页型序（只看容器内，避开外壳 CSS/JS 里的示例串）"""
    h = (ROOT / 'community' / cid / 'index.html')
    if not h.exists():
        h = (ROOT / 'examples' / cid / 'index.html')
    t = h.read_text(encoding='utf-8', errors='ignore')
    i = t.find('id="slide-container"')
    if i < 0:
        return None
    i = t.rfind('<', 0, i)
    seg = t[i:i + 400000]
    types = re.findall(r'<section class="slide-page" data-page-type="([^"]*)"', seg)
    return {'pages': len(types), 'types': types}


def run(cids):
    rows = []
    for cid in cids:
        print(f'─── {cid} ' + '─' * max(0, 46 - len(cid)))
        b = backup(cid)
        print(f'   备份: {b.name if b else "!! git HEAD 里没有该文件，跳过（不冒险）"}')
        if not b:
            rows.append((cid, 'SKIP-无备份', 0, '—'))
            continue
        r1 = sh(['migrate-to-v2-shell.py', cid])
        ok1 = 'slide-sidenav' in (ROOT / 'community' / cid / 'index.html').read_text(
            encoding='utf-8', errors='ignore')
        r2 = sh(['migrate-legacy-blocks.py', cid, '--verify'])
        for line in r2.stdout.splitlines():
            if any(k in line for k in ('内容比对', '已重建', '拒绝', '残留', '展平出')):
                print('   ' + line.strip())
        if r2.returncode != 0:
            print('   ❌ 重排未写入（门禁拦下），需修映射后重试')
            rows.append((cid, '未通过门禁', 0, '—'))
            continue
        c = check(cid)
        good = c and c['pages'] == 16 and c['types'] == CANON
        print(f"   {'✅' if good else '⚠️'} 静态复核: {c['pages']} 页"
              + ('' if good else f"  页型={c['types']}"))
        rows.append((cid, '已重排' if good else '页型需复核', c['pages'] if c else 0,
                     'OK' if good else 'CHECK'))
    print('\n' + '=' * 62)
    print('汇总：')
    for cid, st, n, note in rows:
        print(f'   {note:6s} {cid:40s} {n:2d} 页  {st}')
    ok = sum(1 for r in rows if r[3] == 'OK')
    print(f'\n静态完成 {ok}/{len(rows)} —— 仍需跑渲染验收（Playwright）才算通过')
    return 0 if ok == len(rows) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('course_id', nargs='*')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--next', type=int, default=0)
    a = ap.parse_args()
    if a.list:
        t = list_targets()
        print(f'剩余可迁移 {len(t)} 门：')
        for c in t:
            print('   ', c)
        return 0
    if a.next:
        return run(list_targets()[:a.next])
    if not a.course_id:
        ap.print_help()
        return 1
    return run(a.course_id)


if __name__ == '__main__':
    sys.exit(main())
