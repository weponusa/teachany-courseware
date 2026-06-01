#!/usr/bin/env bash
# Backup teachany-courseware, then rewrite Git history to drop junk only.
# Default slim KEEPS community mp3/mp4/png (no media externalization).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="${TEACHANY_BACKUP_DIR:-$(dirname "$REPO_ROOT")/teachany-courseware-backups}"
STAMP="$(date +%Y%m%d-%H%M%S)"

usage() {
  cat <<'EOF'
Usage:
  backup-and-slim-github-history.sh backup-only
      Full git bundle + tarball of tracked community media (safety copy).

  backup-and-slim-github-history.sh slim
      backup-only, then git-filter-repo: remove junk from ALL history.
      Keeps community tts/video/images and assets/maps (except optional physical).

  backup-and-slim-github-history.sh slim --with-physical
      Also purge assets/maps/physical/ from history (~60MB). Not deployed to
      teachany.cn; restore locally via assets/maps/README.md if needed.

  backup-and-slim-github-history.sh gc
      Aggressive git gc after a prior slim (safe, no history rewrite).

Environment:
  TEACHANY_BACKUP_DIR  override backup directory (default: ../teachany-courseware-backups)

After slim:
  git push origin main --force    # GitHub only — do not push Gitee
EOF
}

require_filter_repo() {
  if ! command -v git-filter-repo >/dev/null 2>&1; then
    echo "error: git-filter-repo not found. Install: pip install git-filter-repo" >&2
    exit 1
  fi
}

require_clean_main() {
  cd "$REPO_ROOT"
  if [[ -n "$(git status --porcelain)" ]]; then
    echo "error: working tree not clean. Commit or stash before slim." >&2
    git status -sb
    exit 1
  fi
}

do_backup() {
  mkdir -p "$BACKUP_DIR"
  cd "$REPO_ROOT"

  local bundle="$BACKUP_DIR/git-bundle-${STAMP}.bundle"
  echo "==> Writing git bundle: $bundle"
  git bundle create "$bundle" --all

  local media_tar="$BACKUP_DIR/community-media-${STAMP}.tar.gz"
  local list
  list="$(mktemp)"
  echo "==> Archiving tracked community media: $media_tar"
  git ls-files \
    'community/**/*.mp3' 'community/**/*.mp4' 'community/**/*.png' \
    'community/**/*.jpg' 'community/**/*.webp' >"$list" 2>/dev/null || true
  if [[ ! -s "$list" ]]; then
    echo "warn: no tracked community media files" >&2
    tar -czf "$media_tar" -T /dev/null
  else
    tar -czf "$media_tar" -C "$REPO_ROOT" -T "$list"
  fi
  rm -f "$list"

  echo "Backup complete:"
  ls -lh "$bundle" "$media_tar"
}

filter_junk_paths() {
  local with_physical="${1:-0}"
  local -a args=(--force)

  args+=(
    --path-glob '_archive_*/**' --invert-paths
    --path-glob '**/remotion/out/**' --invert-paths
    --path-glob '**/remotion/.remotion/**' --invert-paths
    --path-glob 'community/archive/duplicates-*/**' --invert-paths
    --path-glob 'community/archive/pending-duplicates-*/**' --invert-paths
    --path-glob 'community/*/*.teachany' --invert-paths
    --path-glob 'community/*/**/.teachany' --invert-paths
  )

  if [[ "$with_physical" == "1" ]]; then
    echo "    + assets/maps/physical/** (not on teachany.cn deploy)"
    args+=(--path-glob 'assets/maps/physical/**' --invert-paths)
  fi

  git filter-repo "${args[@]}"
}

do_gc() {
  cd "$REPO_ROOT"
  echo "==> Expiring reflog + aggressive gc"
  git reflog expire --expire=now --all
  git gc --prune=now --aggressive
  echo ""
  echo "Pack stats:"
  git count-objects -vH
  du -sh .git
}

do_slim() {
  local with_physical=0
  if [[ "${1:-}" == "--with-physical" ]]; then
    with_physical=1
  fi

  require_filter_repo
  require_clean_main
  do_backup
  cd "$REPO_ROOT"

  echo "==> git-filter-repo: junk-only (community media KEPT)"
  filter_junk_paths "$with_physical"
  do_gc

  echo ""
  echo "Slim done. Media remains in repo; teachany.cn paths unchanged."
  echo "Next: git push origin main --force"
}

cmd="${1:-}"
shift || true
case "$cmd" in
  backup-only) do_backup ;;
  slim) do_slim "$@" ;;
  gc) do_gc ;;
  -h|--help|help|"") usage ;;
  *)
    echo "unknown command: $cmd" >&2
    usage
    exit 1
    ;;
esac
