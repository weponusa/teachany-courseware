#!/usr/bin/env python3
"""
TeachAny · 本地 agent 生图落盘与规范化（2026-11-22 起为课件 hero 的唯一生成入口）

原则（用户明确要求）：
  - 课件 hero 由 WorkBuddy 本地 agent 的图像生成能力（ImageGen）产出，
    本脚本只负责把产物规范化成课件可用的 1536x1024 PNG + webp 变体。
  - **全程不访问任何远程生图接口**，不需要 API Key、不消耗服务端额度。
  - 不伪造图片：源图必须真实存在；若规范化后仍达不到 150KB 只告警，不塞假数据。

典型流程：
  1) agent 调用本地图像生成能力得到 /abs/generated/hero.png
  2) python3 local-hero-image.py --course-id <id> \
         --from /abs/generated/hero.png \
         --out "<课件目录>/assets/<id>-hero.png" \
         --prompt "..." --slot hero

用法：
  --quota                      报告本地能力状态（永远可用、无额度）
  --from <path> --out <path>   单张规范化
  --from-dir <dir> --out <path> 从本地图片目录顺序取下一张（供历史批量脚本迁移）
  --batch <json> --out-dir <dir> 批量；每项 {name, image|from, prompt, slot}
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

TARGET_SIZE = (1536, 1024)
MIN_PNG_BYTES = 150 * 1024
SOURCE_TAG = 'local-agent-imagegen'
IMAGE_SUFFIXES = {'.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tif', '.tiff'}
STATE_NAME = '.teachany-local-image-index.json'
PROBE_NAME = '.teachany-image-gen-probe.json'


def _pil():
    try:
        from PIL import Image, ImageOps
        return Image, ImageOps
    except ImportError as e:
        raise RuntimeError('需要 Pillow：pip install Pillow') from e


def normalize(src: Path, out: Path, *, prompt: str = '', slot: str = '',
              course_id: str = '') -> dict:
    Image, ImageOps = _pil()
    src, out = Path(src), Path(out)
    if not src.is_file():
        raise RuntimeError(f'本地 agent 生成的图片不存在：{src}')
    out.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(src) as im:
        fitted = ImageOps.fit(im.convert('RGB'), TARGET_SIZE,
                              method=Image.LANCZOS, centering=(0.5, 0.5))
        fitted.save(out, 'PNG', optimize=True)
        webp = out.with_suffix('.webp')
        fitted.save(webp, 'WEBP', quality=88, method=6)
    png_bytes = out.stat().st_size
    webp_bytes = webp.stat().st_size
    probe = {
        'source': SOURCE_TAG,
        'course_id': course_id,
        'slot': slot or 'hero',
        'prompt': prompt,
        'source_image': str(src),
        'generated_at': time.strftime('%Y-%m-%dT%H:%M:%S'),
        'size': list(TARGET_SIZE),
        'png_bytes': png_bytes,
        'webp_bytes': webp_bytes,
        'network': False,
    }
    (out.parent / PROBE_NAME).write_text(
        json.dumps(probe, ensure_ascii=False, indent=2), encoding='utf-8')
    result = {'ok': True, **probe}
    if png_bytes < MIN_PNG_BYTES:
        result['warning'] = (f'PNG 仅 {png_bytes} B，低于课件基线 {MIN_PNG_BYTES} B；'
                             '请换更高细节的生图提示词重生成，不要用人造数据凑体积')
    return result


def next_from_dir(d: Path) -> Path:
    """顺序取目录里下一张未用过的图，供历史批量脚本平滑迁移。"""
    files = sorted(p for p in Path(d).iterdir()
                   if p.is_file() and p.suffix.lower() in IMAGE_SUFFIXES)
    if not files:
        raise RuntimeError(f'本地图片目录为空：{d}')
    state = Path(d) / STATE_NAME
    used = []
    if state.exists():
        try:
            used = json.loads(state.read_text(encoding='utf-8')).get('used', [])
        except Exception:
            used = []
    pick = next((p for p in files if p.name not in used), None)
    if pick is None:
        raise RuntimeError(f'本地图片目录 {d} 的 {len(files)} 张图已全部用过')
    used.append(pick.name)
    state.write_text(json.dumps({'used': used}, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return pick


def quota() -> dict:
    return {
        'ok': True,
        'source': SOURCE_TAG,
        'quota': 'unlimited',
        'network': False,
        'note': '课件 hero 由本地 agent 图像能力生成，不依赖 TeachAny 服务端生图额度',
        'script': str(Path(__file__).resolve()),
    }


def main() -> int:
    ap = argparse.ArgumentParser(
        description='TeachAny 本地 agent 生图落盘与规范化（不联网）')
    ap.add_argument('--course-id', default='', help='课件 ID（写入元数据）')
    ap.add_argument('--from', dest='source_file', help='本地 agent 生成的图片路径')
    ap.add_argument('--from-dir', default=os.environ.get('TEACHANY_LOCAL_IMAGE_DIR', ''),
                    help='本地图片目录，顺序取下一张（也可用环境变量）')
    ap.add_argument('--out', help='输出 PNG 路径，同目录会生成 .webp')
    ap.add_argument('--prompt', default='', help='生图提示词（仅记录，不发起请求）')
    ap.add_argument('--slot', default='hero', help='hero / section1 …（仅日志）')
    ap.add_argument('--batch', help='批量 JSON 文件')
    ap.add_argument('--out-dir', help='批量输出目录')
    ap.add_argument('--quota', action='store_true', help='报告本地能力状态')
    args = ap.parse_args()

    if args.quota:
        print(json.dumps(quota(), ensure_ascii=False, indent=2))
        return 0

    if args.batch and args.out_dir:
        tasks = json.loads(Path(args.batch).read_text(encoding='utf-8'))
        out_dir = Path(args.out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        ok, failed = 0, []
        for i, task in enumerate(tasks, 1):
            name = task.get('name') or f'img_{i:03d}'
            src = task.get('image') or task.get('from')
            try:
                if not src and args.from_dir:
                    src = str(next_from_dir(Path(args.from_dir)))
                if not src:
                    raise RuntimeError('缺少 image/from 字段，也没有 --from-dir')
                r = normalize(Path(src), out_dir / f'{name}.png',
                              prompt=task.get('prompt', ''), slot=task.get('slot', name),
                              course_id=args.course_id)
                print(f'[{i}/{len(tasks)}] ✅ {name}.png ({r["png_bytes"] // 1024} KB)'
                      + (f' ⚠️ {r["warning"]}' if r.get('warning') else ''))
                ok += 1
            except Exception as e:
                print(f'[{i}/{len(tasks)}] ❌ {name}: {e}')
                failed.append({'name': name, 'error': str(e)})
        print(f'完成 {ok}/{len(tasks)}')
        return 1 if ok == 0 and failed else 0

    if args.out:
        src = args.source_file
        try:
            if not src and args.from_dir:
                src = str(next_from_dir(Path(args.from_dir)))
            if not src:
                ap.error('需要 --from <本地图片> 或 --from-dir <目录>；'
                         '本脚本不会调用任何远程生图接口')
            r = normalize(Path(src), Path(args.out), prompt=args.prompt,
                          slot=args.slot, course_id=args.course_id)
        except Exception as e:
            print(f'❌ {e}', file=sys.stderr)
            return 1
        print(json.dumps(r, ensure_ascii=False, indent=2))
        if r.get('warning'):
            print(f'⚠️  {r["warning"]}', file=sys.stderr)
        return 0

    ap.print_help()
    return 1


if __name__ == '__main__':
    sys.exit(main())
