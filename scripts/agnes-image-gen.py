#!/usr/bin/env python3
"""
TeachAny · 生图入口兼容层（Agnes 远程生图已停用，2026-11-22）

用户明确要求：课件 hero 全部改由本地 agent 图像能力生成。
本文件保留旧文件名，避免历史脚本 / 文档引用断裂，但：

  - **不再向 /api/images/agnes 或 /api/images/quota 发任何请求**
  - 只把参数转交给同目录的 local-hero-image.py
  - 缺少本地图片时明确报错，绝不静默回退到远程生图

新用法（agent 先用本地图像能力生成图片）：
  python3 agnes-image-gen.py --course-id <id> \
      --from /abs/generated/hero.png \
      --out "<课件目录>/assets/<id>-hero.png" \
      --prompt "..." --slot hero

历史批量脚本（bulk_image_gen.py / batch-cn-hero-agnes.py / pipeline_upgrade_v2.py）：
  先用本地 agent 批量产出图片到目录，再设置
      TEACHANY_LOCAL_IMAGE_DIR=/abs/generated-images
  本兼容层会按顺序取图，完全离线。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LOCAL = HERE / 'local-hero-image.py'


def main() -> int:
    print('ℹ️  Agnes 远程生图已停用；本命令转交「本地 agent 图像能力」链路。',
          file=sys.stderr)
    ap = argparse.ArgumentParser(
        description='兼容层：转交本地 agent 生图链路（不联网、无额度）')
    ap.add_argument('--course-id', default='', help='课件 ID')
    ap.add_argument('--from', dest='source_file', help='本地 agent 生成的图片路径')
    ap.add_argument('--from-dir', default=os.environ.get('TEACHANY_LOCAL_IMAGE_DIR', ''),
                    help='本地图片目录（也可用环境变量 TEACHANY_LOCAL_IMAGE_DIR）')
    ap.add_argument('--prompt', default='', help='生图提示词（仅记录）')
    ap.add_argument('--size', default='1536x1024', help='已忽略：尺寸由本地脚本固定规范')
    ap.add_argument('--slot', default='hero')
    ap.add_argument('--out', help='输出 PNG 路径')
    ap.add_argument('--batch', help='批量 JSON')
    ap.add_argument('--out-dir', help='批量输出目录')
    ap.add_argument('--quota', action='store_true', help='报告本地能力状态')
    ap.add_argument('--api-base', default='', help='已废弃：不再访问任何远程 API')
    args = ap.parse_args()

    if args.api_base:
        print('⚠️  --api-base 已废弃：本地生图链路不访问远程接口。', file=sys.stderr)

    if not LOCAL.is_file():
        print(f'❌ 缺少本地生图脚本：{LOCAL}', file=sys.stderr)
        return 2

    cmd = [sys.executable, str(LOCAL), '--course-id', args.course_id]
    if args.quota:
        cmd.append('--quota')
        return subprocess.call(cmd)

    if args.source_file:
        cmd += ['--from', args.source_file]
    elif args.from_dir:
        cmd += ['--from-dir', args.from_dir]
    if args.out:
        cmd += ['--out', args.out]
    if args.prompt:
        cmd += ['--prompt', args.prompt]
    if args.slot:
        cmd += ['--slot', args.slot]
    if args.batch:
        cmd += ['--batch', args.batch]
    if args.out_dir:
        cmd += ['--out-dir', args.out_dir]

    if not (args.out or (args.batch and args.out_dir)):
        print('❌ 缺少 --out / --batch+--out-dir，无法落盘。', file=sys.stderr)
        return 2
    if not (args.source_file or args.from_dir):
        print('❌ 缺少本地图片：请先用本地 agent 图像能力生成图片，再传 '
              '--from <路径> 或设置 TEACHANY_LOCAL_IMAGE_DIR。\n'
              '   本兼容层不会调用任何远程生图接口。', file=sys.stderr)
        return 2
    return subprocess.call(cmd)


if __name__ == '__main__':
    sys.exit(main())
