#!/usr/bin/env python3
"""把 community/<course>/tts/ 下的音频同步到自建音频 CDN（Cloudflare Pages 项目 teachany-audio）。

背景
----
课件的语音由 https://audio.teachany.cn/<course>/tts/<file> 提供。
该 CDN 的内容是 community/<course>/tts/ 的**镜像**（保留 tts/ 路径，零碰撞）。
源站项目：Cloudflare Pages `teachany-audio`。
（历史：曾走 jsdelivr 的 gh/weponusa/teachany-audio，因仓库 947MB 超其单包 50MB 上限
 而全站 403，已废弃，勿改回。）

用法
----
    # 1) 组装发布目录（默认 /tmp/teachany-audio-dist）
    python3 scripts/sync-audio-cdn.py --out /tmp/teachany-audio-dist

    # 2) 部署（需先 wrangler 登录）
    wrangler pages deploy /tmp/teachany-audio-dist \
        --project-name teachany-audio --branch main --commit-dirty=true

约定
----
  * 只上传音频/字幕类：mp3 wav ogg m4a srt json；目录里混着的 .py/.js/.txt 不入 CDN。
  * 自动写 _headers（长缓存 + 允许跨域），<audio> 跨域播放与弱网缓存都靠它。
"""
import argparse
import shutil
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
COMMUNITY = ROOT / "community"
KEEP = {".mp3", ".wav", ".ogg", ".m4a", ".srt", ".json"}
DROP_NAMES = {"gen_tts.py", "generate_pinyin_audio.py", "generate.py", "tts-player.js"}


def build(out: Path) -> int:
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    n = total = 0
    courses: set[str] = set()
    t0 = time.time()

    for course in sorted(p for p in COMMUNITY.iterdir() if p.is_dir()):
        out_root = out / course.name
        # 所有名为 tts 的目录（含嵌套，如 assets/tts），按原路径镜像
        for tts in course.rglob("tts"):
            if not tts.is_dir():
                continue
            for f in tts.rglob("*"):
                if not f.is_file() or f.name in DROP_NAMES or f.suffix.lower() not in KEEP:
                    continue
                dst = out_root / f.relative_to(course)
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                n += 1
                total += f.stat().st_size
                courses.add(course.name)
        # 课件根目录下的裸音频
        for f in course.iterdir():
            if f.is_file() and f.suffix.lower() in (".mp3", ".wav", ".ogg", ".m4a"):
                dst = out_root / f.name
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(f, dst)
                n += 1
                total += f.stat().st_size
                courses.add(course.name)

    (out / "_headers").write_text(
        "/*\n  Cache-Control: public, max-age=604800\n  Access-Control-Allow-Origin: *\n",
        encoding="utf-8",
    )
    n += 1

    print(f"课件目录 : {len(courses)}")
    print(f"文件数   : {n}   (Cloudflare Pages 单项目上限 20000)")
    print(f"总体积   : {total / 1048576:.1f} MB")
    print(f"输出目录 : {out}")
    print(f"耗时     : {time.time() - t0:.1f}s")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="/tmp/teachany-audio-dist")
    a = ap.parse_args()
    rc = build(Path(a.out))
    print()
    print("下一步：")
    print(f"  wrangler pages deploy {a.out} --project-name teachany-audio --branch main --commit-dirty=true")
    return rc


if __name__ == "__main__":
    sys.exit(main())
