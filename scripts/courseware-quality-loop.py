#!/usr/bin/env python3
"""全库课件质量循环：扫描 → 分类 → 自动修复 → 再扫描。

检查项（与 TeachAny 基线对齐）：
  - 缺图 / 图引用 404 / 图过小
  - 图内乱码（可选 OCR，--ocr）
  - 历史/地理缺标准地图 data-teachany-map
  - 占位 mp4 / 视频死链
  - 本地 ./assets/scripts 路径（应用 /assets/scripts/）
  - 缺知识图谱 / AI 学伴 / TTS 等标准模块
  - 本地资源 404（互动材料死链）

用法：
  python3 scripts/courseware-quality-loop.py audit
  python3 scripts/courseware-quality-loop.py fix --limit 100
  python3 scripts/courseware-quality-loop.py loop --rounds 2 --limit 50
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"
REPORTS = ROOT / "reports"
SKILL = Path.home() / ".claude/skills/teachany"
FINALIZE = SKILL / "scripts/finalize-courseware.py"
MIN_IMG_BYTES = 20 * 1024
PLACEHOLDER_MP4_MAX = 500 * 1024  # 小于 500KB 的 mp4 视为占位
MIN_IMG_REFS = 3


def resolve_local_ref(d: Path, ref: str) -> Path:
    """Resolve ./assets/foo.png?v=1 style refs to on-disk paths."""
    clean = ref.split("?", 1)[0].split("#", 1)[0]
    if clean.startswith("./"):
        clean = clean[2:]
    return (d / clean).resolve()


def mp4_has_audio(mp4: Path) -> bool | None:
    try:
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "stream=codec_type", "-of", "csv=p=0", str(mp4)],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if r.returncode != 0:
            return None
        return "audio" in r.stdout
    except Exception:
        return None


def is_placeholder_mp4(mp4: Path, html: str = "") -> bool:
    if mp4.stat().st_size >= PLACEHOLDER_MP4_MAX:
        return False
    if mp4.name in html and re.search(rf"<(?:video|source)[^>]+{re.escape(mp4.name)}", html, re.I):
        if mp4_has_audio(mp4):
            return False
    return True


def rewrite_site_root_script_paths(html: str) -> tuple[str, int]:
    """./assets/scripts/ 与 ../../assets/scripts/ → /assets/scripts/（挂树可加载）。"""
    n = 0
    for pat, rep in (
        (r"\./assets/scripts/", "/assets/scripts/"),
        (r"\.\./\.\./assets/scripts/", "/assets/scripts/"),
        (r"\.\./\./assets/scripts/", "/assets/scripts/"),
        (r"\.\./assets/scripts/", "/assets/scripts/"),
    ):
        html, c = re.subn(pat, rep, html)
        n += c
    html, c = re.subn(
        r'((?:href|src)=["\'])assets/scripts/',
        r"\1/assets/scripts/",
        html,
        flags=re.I,
    )
    n += c
    return html, n


def ensure_minimum_images(d: Path, *, dry_run: bool = False) -> list[str]:
    """补全 hero/concept/process 三张标准插图引用。"""
    repair = load_mod("repair_img", ROOT / "scripts/repair-image-refs.py")
    html_path = d / "index.html"
    if not html_path.is_file():
        return []
    html = html_path.read_text(encoding="utf-8", errors="replace")
    refs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
    assets = repair.list_asset_files(d)
    if len(refs) >= MIN_IMG_REFS and len(assets) >= MIN_IMG_REFS:
        return []
    title = repair.course_title(d)
    created = repair.ensure_standard_svgs(d, title)
    assets = repair.list_asset_files(d)
    actions = [f"created_{c}" for c in created]
    inject: list[str] = []
    for name, label in (
        ("hero-infographic.svg", "知识结构"),
        ("concept-diagram.svg", "核心概念"),
        ("process-diagram.svg", "过程示意"),
    ):
        path_ref = f"./assets/{name}"
        if path_ref not in html and name not in html:
            inject.append(
                f'<figure class="course-fig"><img src="{path_ref}" alt="{label}" loading="lazy"></figure>'
            )
    if inject and len(refs) + len(inject) >= MIN_IMG_REFS:
        marker = "</main>"
        block = "\n<section class=\"section course-figures\">\n" + "\n".join(inject) + "\n</section>\n"
        if marker in html:
            html = html.replace(marker, block + marker, 1)
        else:
            html += block
        actions.append("injected_figures")
    if not dry_run and actions:
        html_path.write_text(html, encoding="utf-8")
        repair.update_manifest(d)
    return actions

SKIP_DIRS = {"drafts", "pending", "archived"}
CN_SPECS = ROOT / "scripts" / "cn-specs"
INTL_INFIX = re.compile(r"-ib-|-ap-|-cam-|-igcse-|-a-level-", re.I)
_CN_SPEC_INDEX: dict[str, Path] | None = None


def _build_cn_spec_index() -> dict[str, Path]:
    global _CN_SPEC_INDEX
    if _CN_SPEC_INDEX is not None:
        return _CN_SPEC_INDEX
    idx: dict[str, Path] = {}
    if CN_SPECS.is_dir():
        for p in CN_SPECS.glob("*.json"):
            try:
                spec = json.loads(p.read_text(encoding="utf-8"))
                if not isinstance(spec, dict):
                    idx[p.stem] = p
                    continue
                nid = spec.get("node_id") or p.stem
                if isinstance(nid, list):
                    nid = nid[0] if nid else p.stem
                nid = str(nid)
                idx[nid] = p
                idx[p.stem] = p
            except Exception:
                idx[p.stem] = p
    _CN_SPEC_INDEX = idx
    return idx


def cn_spec_for_course(cid: str) -> Path | None:
    return _build_cn_spec_index().get(cid)


def is_cn_course(d: Path, mf: dict | None = None) -> bool:
    """中国课标课件：含 cn-national / 义务教育课标字段 / 无 curriculum 的非国际课。"""
    if mf is None:
        mf = load_manifest(d)
    if d.name.startswith("ext-"):
        return False
    nid = mf.get("node_id") or d.name
    if INTL_INFIX.search(f"{nid}/{d.name}"):
        return False
    cur = str(mf.get("curriculum") or mf.get("curriculum_id") or "").strip()
    cur_lower = cur.lower()
    if any(kw in cur for kw in ("课标", "义务教育", "课程标准")):
        return True
    if cur_lower in ("cn-national", "cn", "chinese-national"):
        return True
    if not cur:
        return True
    return False


def load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def iter_courses(limit: int = 0, only: list[str] | None = None, *, cn_only: bool = False) -> list[Path]:
    if only:
        out = [COMMUNITY / x for x in only if (COMMUNITY / x).is_dir()]
    else:
        out = []
        for d in sorted(COMMUNITY.iterdir()):
            if not d.is_dir() or d.name in SKIP_DIRS:
                continue
            if (d / "index.html").is_file() and (d / "manifest.json").is_file():
                if cn_only and not is_cn_course(d):
                    continue
                out.append(d)
    if limit:
        out = out[:limit]
    return out


def load_manifest(d: Path) -> dict:
    try:
        return json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def audit_course(d: Path, *, ocr: bool = False, strict: bool = False) -> dict:
    cid = d.name
    mf = load_manifest(d)
    html_path = d / "index.html"
    html = html_path.read_text(encoding="utf-8", errors="replace") if html_path.is_file() else ""
    subj = (mf.get("subject") or "").lower()
    issues: list[str] = []

    # --- 图片 ---
    img_refs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I)
    assets = list((d / "assets").rglob("*")) if (d / "assets").is_dir() else []
    img_files = [p for p in assets if p.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".svg"}]
    if len(img_refs) < 3:
        issues.append("missing_images_ref")
    if len(img_files) < 3:
        issues.append("missing_images_files")
    for ref in img_refs:
        if ref.startswith(("http://", "https://", "/")):
            continue
        if "${" in ref or "{{" in ref:
            continue
        target = resolve_local_ref(d, ref)
        if not target.is_file():
            issues.append("broken_image_ref")
            break
    hero_refs = re.findall(
        r'<img[^>]+src=["\']([^"\']+)["\']', html, re.I
    )
    hero_refs = [r for r in hero_refs if "hero" in r.lower()]
    hero_targets_svg = any(r.endswith(".svg") for r in hero_refs)
    for p in img_files:
        if p.suffix.lower() == ".svg":
            continue
        if p.stat().st_size < MIN_IMG_BYTES and "hero" in p.name.lower():
            if hero_targets_svg and p.name not in {Path(r).name for r in hero_refs}:
                continue
            issues.append("tiny_hero_image")
            break

    # --- OCR 乱码（可选，慢）---
    if ocr:
        try:
            scan = load_mod("scan", ROOT / "scripts/scan-agnes-image-text.py")
            for p in img_files[:6]:
                if p.suffix.lower() != ".png":
                    continue
                text = scan.ocr_image(p)
                level, _ = scan.classify(text)
                if level in ("cjk", "eng"):
                    issues.append(f"image_garbled_{level}")
                    break
        except Exception:
            issues.append("ocr_skipped")

    # --- 历史/地理地图（与 validate-courseware 基线一致）---
    if subj in ("history", "geography"):
        has_tile = bool(re.search(r"L\.tileLayer\s*\(", html))
        has_decl = "data-teachany-map" in html and "teachany-historical-map.js" in html
        has_canvas = (
            'id="map-canvas"' in html
            and "assets/maps/" in html
            and "mLoadGeoBoundaries" in html
        )
        has_fit = bool(re.search(r"fitBounds|setView", html))
        has_leaflet = bool(re.search(r"L\.map\s*\(", html)) and has_fit
        if not (has_tile or has_decl or has_canvas or has_leaflet):
            issues.append("missing_map")
        elif not has_decl and not has_canvas and not has_leaflet and not has_fit:
            issues.append("missing_map_focus")

    # --- 占位/死链视频 ---
    mp4s = list(d.glob("assets/**/*.mp4")) + list(d.glob("videos/**/*.mp4"))
    for mp4 in mp4s:
        if is_placeholder_mp4(mp4, html):
            issues.append("placeholder_video")
            break
    if re.search(r"\.mp4", html):
        for ref in re.findall(r'src=["\']([^"\']+\.mp4[^"\']*)["\']', html, re.I):
            if ref.startswith(("http://", "https://", "/")):
                continue
            target = resolve_local_ref(d, ref)
            if target.is_file() and is_placeholder_mp4(target, html):
                issues.append("placeholder_video_ref")
                break
    for ref in re.findall(r'src=["\']([^"\']+\.mp4)["\']', html, re.I):
        if ref.startswith(("http", "/")):
            continue
        if not (d / ref.lstrip("./")).is_file():
            issues.append("broken_video_ref")
            break

    # --- 标准模块 ---
    if "data-teachany-kg" not in html and "teachany-knowledge-graph.js" not in html:
        issues.append("missing_knowledge_graph")
    if "data-teachany-tutor-card" not in html and "teachany-tutor-card.js" not in html:
        issues.append("missing_ai_tutor")
    if "./assets/scripts/" in html or "../../assets/scripts/" in html:
        issues.append("local_script_paths")
    tts_mp3 = len(list(d.glob("tts/*.mp3"))) + len(list(d.glob("assets/tts/*.mp3")))
    has_tts_infra = "data-tts=" in html or "teachany-audio-playlist" in html
    if has_tts_infra and tts_mp3 < 3:
        issues.append("missing_tts")

    # --- 死链资源（validate-courseware 逻辑）---
    try:
        val = load_mod("val", ROOT / "scripts/validate-courseware.py")
        missing = val.find_missing_local_asset_refs(d, html)
        real_missing = [
            x for x in missing
            if not re.search(r"tts/.*\.mp3$", x[0], re.I)
        ]
        if real_missing:
            issues.append("broken_asset_ref")
    except Exception:
        pass

    # --- 占位正文 ---
    if "[待补充]" in html or "TODO" in html[:8000]:
        issues.append("placeholder_text")

    validate_errors: list[str] = []
    if strict:
        try:
            val = load_mod("val", ROOT / "scripts/validate-courseware.py")
            for lvl, msg in val.validate_one(d, strict_feedback=False):
                if lvl == "error":
                    validate_errors.append(msg.split(":", 1)[-1].strip()[:80])
            if validate_errors:
                issues.append("validate_fail")
        except Exception:
            issues.append("validate_skipped")

    return {
        "course_id": cid,
        "subject": subj,
        "curriculum": "cn-national" if is_cn_course(d, mf) else "other",
        "has_cn_spec": cn_spec_for_course(cid) is not None,
        "issues": sorted(set(issues)),
        "issue_count": len(set(issues)),
        "validate_errors": validate_errors[:8],
        "validate_error_count": len(validate_errors),
    }


def fix_broken_html_refs(d: Path, *, dry_run: bool = False) -> list[str]:
    """修正常见死链：裸模块名、错误相对路径、跨课链接。"""
    html_path = d / "index.html"
    if not html_path.is_file():
        return []
    html = html_path.read_text(encoding="utf-8", errors="replace")
    orig = html
    actions: list[str] = []

    html, n = rewrite_site_root_script_paths(html)
    if n:
        actions.append(f"site_root_scripts({n})")
    html = re.sub(r"\.\./+assets/scripts/", "/assets/scripts/", html)
    html = html.replace("..//assets/scripts/", "/assets/scripts/")
    html = re.sub(
        r'src=["\']\./history-tracker\.js["\']',
        'src="/assets/scripts/history-tracker.js"',
        html,
    )
    html = re.sub(r"\.\./+\.shared-assets/", "/assets/scripts/", html)
    html = re.sub(
        r'((?:href|src)=["\'])(ai-tutor\.(?:css|js)|teachany-[a-z0-9-]+\.(?:css|js))(["\'])',
        r"\1/assets/scripts/\2\3",
        html,
        flags=re.I,
    )
    # 跨课件 index.html 链接改为 teachany.cn 社区路径
    def fix_cross(m: re.Match) -> str:
        ref = m.group(2)
        if re.search(r"community/[^/]+/index\.html$", ref) or ref.count("../") >= 2:
            parts = ref.replace("\\", "/").split("/")
            cid = next((p for p in reversed(parts) if p and p != "index.html"), "")
            if cid:
                actions.append(f"cross_link->{cid}")
                return f'{m.group(1)}/community/{cid}/{m.group(3)}'
        return m.group(0)

    html = re.sub(r'((?:href|src)=["\'])([^"\']+index\.html)(["\'])', fix_cross, html)
    if html != orig and not dry_run:
        html_path.write_text(html, encoding="utf-8")
    return actions


def fix_course(d: Path, issues: list[str], *, dry_run: bool = False) -> list[str]:
    applied: list[str] = []
    cid = d.name

    if "broken_asset_ref" in issues and not dry_run:
        ref_actions = fix_broken_html_refs(d, dry_run=dry_run)
        if ref_actions:
            applied.extend(ref_actions)

    if "placeholder_video" in issues or "placeholder_video_ref" in issues:
        html_path = d / "index.html"
        html = html_path.read_text(encoding="utf-8", errors="replace") if html_path.is_file() else ""
        removed_any = False
        for mp4 in list(d.glob("assets/**/*.mp4")) + list(d.glob("videos/**/*.mp4")):
            if is_placeholder_mp4(mp4, html):
                if not dry_run:
                    mp4.unlink()
                applied.append("removed_placeholder_mp4")
                removed_any = True
        if html_path.is_file() and not dry_run and removed_any:
            html = html_path.read_text(encoding="utf-8")
            html = re.sub(
                r'<video[^>]*>.*?</video>\s*',
                "",
                html,
                flags=re.S | re.I,
            )
            html = re.sub(r'<source[^>]*\.mp4[^>]*>\s*', "", html, flags=re.I)
            html_path.write_text(html, encoding="utf-8")
            applied.append("stripped_video_tags")

    if any(x in issues for x in ("local_script_paths", "missing_knowledge_graph", "missing_ai_tutor")):
        html_path = d / "index.html"
        if html_path.is_file() and not dry_run:
            html = html_path.read_text(encoding="utf-8", errors="replace")
            new_html, n = rewrite_site_root_script_paths(html)
            if n:
                html_path.write_text(new_html, encoding="utf-8")
                applied.append(f"site_root_scripts({n})")
        if FINALIZE.is_file() and not dry_run and (
            "missing_knowledge_graph" in issues or "missing_ai_tutor" in issues
        ):
            r = subprocess.run(
                [sys.executable, str(FINALIZE), str(d), "--shared", "--no-audio"],
                capture_output=True,
                text=True,
            )
            if r.returncode == 0:
                applied.append("finalize_shared")
                html_path = d / "index.html"
                if html_path.is_file():
                    html = html_path.read_text(encoding="utf-8", errors="replace")
                    new_html, n = rewrite_site_root_script_paths(html)
                    if n:
                        html_path.write_text(new_html, encoding="utf-8")
                        applied.append(f"site_root_scripts({n})")

    if any(x in issues for x in ("missing_images_ref", "missing_images_files")) and not dry_run:
        img_actions = ensure_minimum_images(d, dry_run=dry_run)
        if img_actions:
            applied.extend(img_actions)

    if "missing_map" in issues and not dry_run:
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/repair-all-courseware.py"), "--skip-rebuild", "--node-ids", cid],
            capture_output=True,
            text=True,
        )
        if r.returncode == 0:
            applied.append("repair_map_modules")

    if any(
        x in issues
        for x in (
            "missing_images_ref",
            "missing_images_files",
            "tiny_hero_image",
            "broken_image_ref",
            "broken_asset_ref",
        )
    ) and not dry_run:
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts/repair-image-refs.py"), "--course", cid],
            capture_output=True,
            text=True,
        )
        if r.returncode == 0:
            applied.append("repair_image_refs")
        elif "repair_image_refs" not in applied and "repair_asset_refs" not in applied:
            r2 = subprocess.run(
                [sys.executable, str(FINALIZE), str(d), "--shared", "--no-audio"],
                capture_output=True,
                text=True,
            )
            if r2.returncode == 0:
                applied.append("finalize_for_images")

    return applied


def is_generic_template_html(html: str) -> bool:
    if "teachany-brand-bar" in html:
        return False
    if 'id="slide-container"' in html and len(html.splitlines()) < 450:
        return True
    return False


def upgrade_course(d: Path, *, dry_run: bool = False, force: bool = False) -> list[str]:
    """从 cn-spec 重建 HTML/manifest 并 finalize（课标 v7 模板升级）。"""
    cid = d.name
    applied: list[str] = []
    html_path = d / "index.html"
    if html_path.is_file() and not force:
        html = html_path.read_text(encoding="utf-8", errors="replace")
        if not is_generic_template_html(html) and len(html.splitlines()) > 450:
            return ["skip_rich_content"]
        if "teachany-brand-bar" in html:
            return ["skip_branded_rich"]
    spec = cn_spec_for_course(cid)
    if not spec:
        return applied
    if dry_run:
        return ["would_rebuild_cn_spec"]
    r = subprocess.run(
        [sys.executable, str(ROOT / "scripts/build-cn-course.py"), "--spec", str(spec)],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        applied.append("build_failed")
        return applied
    applied.append("rebuild_cn_spec")
    if FINALIZE.is_file():
        subprocess.run(
            [sys.executable, str(FINALIZE), str(d), "--shared", "--no-audio"],
            capture_output=True,
            text=True,
        )
        applied.append("finalize_shared")
    html_path = d / "index.html"
    if html_path.is_file():
        html = html_path.read_text(encoding="utf-8", errors="replace")
        new_html, n = rewrite_site_root_script_paths(html)
        if n:
            html_path.write_text(new_html, encoding="utf-8")
            applied.append(f"site_root_scripts({n})")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/repair-all-courseware.py"),
         "--skip-rebuild", "--node-ids", cid, "--skip-validate"],
        capture_output=True,
        text=True,
    )
    applied.append("repair_map_modules")
    return applied


def cmd_audit(args) -> int:
    courses = iter_courses(args.limit, args.only, cn_only=args.cn_only)
    scope = "中国课标" if args.cn_only else "全库"
    print(f"扫描 {len(courses)} 门{scope}课件…")
    rows = []
    counter: Counter[str] = Counter()
    for i, d in enumerate(courses, 1):
        row = audit_course(d, ocr=args.ocr, strict=args.strict)
        rows.append(row)
        for iss in row["issues"]:
            counter[iss] += 1
        if i % 100 == 0:
            print(f"  …{i}/{len(courses)}")
    bad = [r for r in rows if r["issues"]]
    val_fail = sum(1 for r in rows if "validate_fail" in r["issues"])
    report = {
        "scanned_at": datetime.now(timezone.utc).isoformat(),
        "scope": "cn-national" if args.cn_only else "all",
        "strict": args.strict,
        "total": len(rows),
        "with_issues": len(bad),
        "validate_fail_count": val_fail,
        "issue_counts": dict(counter.most_common()),
        "courses": rows,
    }
    default_name = "courseware-quality-audit-cn.json" if args.cn_only else "courseware-quality-audit.json"
    out = Path(args.out) if args.out else REPORTS / default_name
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n完成：{len(bad)}/{len(rows)} 门有问题", end="")
    if args.strict:
        print(f"（基线 validate 未通过 {val_fail} 门）", end="")
    print(f"\n报告 → {out}")
    for k, v in counter.most_common(15):
        print(f"  {k}: {v}")
    return 0


def cmd_fix(args) -> int:
    audit_path = Path(args.from_audit) if args.from_audit else REPORTS / "courseware-quality-audit.json"
    if audit_path.is_file():
        data = json.loads(audit_path.read_text(encoding="utf-8"))
        targets = [r for r in data["courses"] if r["issues"]]
        if args.issue:
            targets = [r for r in targets if args.issue in r["issues"]]
    else:
        targets = [{"course_id": d.name, "issues": audit_course(d)["issues"]}
                   for d in iter_courses(args.limit, args.only, cn_only=getattr(args, "cn_only", False))]
    if args.limit:
        targets = targets[: args.limit]
    print(f"修复 {len(targets)} 门…")
    fixed = 0
    for i, row in enumerate(targets, 1):
        cid = row["course_id"]
        d = COMMUNITY / cid
        if not d.is_dir():
            continue
        applied = fix_course(d, row["issues"], dry_run=args.dry_run)
        if applied:
            fixed += 1
            print(f"  [{i}] {cid}: {', '.join(applied)}")
    print(f"\n已处理 {fixed}/{len(targets)} 门")
    return 0


def cmd_loop(args) -> int:
    for rnd in range(1, args.rounds + 1):
        print(f"\n{'='*60}\n第 {rnd}/{args.rounds} 轮：扫描\n{'='*60}")
        audit_args = argparse.Namespace(
            limit=args.limit, only=args.only, ocr=args.ocr,
            cn_only=getattr(args, "cn_only", False),
            strict=getattr(args, "strict", False),
            out=str(REPORTS / f"courseware-quality-audit-r{rnd}.json"),
        )
        cmd_audit(audit_args)
        print(f"\n第 {rnd} 轮：修复")
        fix_args = argparse.Namespace(
            from_audit=audit_args.out, limit=args.limit, only=args.only,
            issue=args.issue, dry_run=args.dry_run,
        )
        cmd_fix(fix_args)
        if args.sleep:
            time.sleep(args.sleep)
    return 0


def cmd_upgrade(args) -> int:
    audit_path = Path(args.from_audit) if args.from_audit else REPORTS / "courseware-quality-audit-cn-strict.json"
    if audit_path.is_file() and not args.force:
        data = json.loads(audit_path.read_text(encoding="utf-8"))
        targets = [
            r["course_id"] for r in data["courses"]
            if cn_spec_for_course(r["course_id"])
            and ("validate_fail" in r["issues"] or not r.get("has_cn_spec"))
        ]
    else:
        targets = [
            d.name for d in iter_courses(cn_only=True)
            if cn_spec_for_course(d.name)
        ]
    if args.only:
        targets = [x for x in targets if x in args.only]
    if args.limit:
        targets = targets[: args.limit]
    print(f"课标模板升级 {len(targets)} 门（cn-spec 重建 + finalize）…")
    ok = 0
    for i, cid in enumerate(targets, 1):
        d = COMMUNITY / cid
        applied = upgrade_course(d, dry_run=args.dry_run, force=args.force)
        if applied == ["skip_rich_content"] or applied == ["skip_branded_rich"]:
            print(f"  ⏭️  [{i}] {cid}: 保留精细版（{applied[0]}）")
            continue
        if applied and "build_failed" not in applied:
            ok += 1
            if i % 10 == 0 or i <= 3:
                print(f"  [{i}] {cid}: {', '.join(applied)}")
        elif applied:
            print(f"  ❌ [{i}] {cid}: build_failed")
    print(f"\n升级完成 {ok}/{len(targets)} 门")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="全库课件质量循环")
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("audit", help="全库扫描")
    a.add_argument("--limit", type=int, default=0)
    a.add_argument("--only", nargs="*")
    a.add_argument("--cn-only", action="store_true", help="仅中国课标课件")
    a.add_argument("--strict", action="store_true", help="叠加 validate-courseware 基线")
    a.add_argument("--ocr", action="store_true", help="对 PNG 做 OCR（慢）")
    a.add_argument("--out", default="")

    f = sub.add_parser("fix", help="按审计结果自动修复")
    f.add_argument("--from-audit", default="")
    f.add_argument("--limit", type=int, default=0)
    f.add_argument("--only", nargs="*")
    f.add_argument("--cn-only", action="store_true")
    f.add_argument("--issue", default="", help="只修某一类 issue")
    f.add_argument("--dry-run", action="store_true")

    u = sub.add_parser("upgrade", help="从 cn-spec 重建课标课件（v7 模板）")
    u.add_argument("--from-audit", default="")
    u.add_argument("--limit", type=int, default=0)
    u.add_argument("--only", nargs="*")
    u.add_argument("--force", action="store_true", help="忽略 audit，凡有 spec 均重建")
    u.add_argument("--dry-run", action="store_true")

    l = sub.add_parser("loop", help="扫描→修复 循环")
    l.add_argument("--rounds", type=int, default=2)
    l.add_argument("--limit", type=int, default=0)
    l.add_argument("--only", nargs="*")
    l.add_argument("--cn-only", action="store_true")
    l.add_argument("--strict", action="store_true")
    l.add_argument("--ocr", action="store_true")
    l.add_argument("--issue", default="")
    l.add_argument("--dry-run", action="store_true")
    l.add_argument("--sleep", type=int, default=0)

    args = ap.parse_args()
    if args.cmd == "audit":
        return cmd_audit(args)
    if args.cmd == "fix":
        return cmd_fix(args)
    if args.cmd == "upgrade":
        return cmd_upgrade(args)
    return cmd_loop(args)


if __name__ == "__main__":
    raise SystemExit(main())
