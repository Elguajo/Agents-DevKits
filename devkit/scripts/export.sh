#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export_root="$repo_dir/exports"
timestamp="$(date -u +%Y%m%dT%H%M%SZ)"
artifact_name="agents-devkits-$timestamp"
staging_dir="$(mktemp -d)"
artifact_dir="$staging_dir/$artifact_name"
archive_path="$export_root/$artifact_name.tar.gz"
checksum_path="$export_root/$artifact_name.SHA256SUMS"

cleanup() {
  rm -rf "$staging_dir"
}
trap cleanup EXIT

copy_path() {
  local path="$1"

  if [[ -e "$repo_dir/$path" ]]; then
    mkdir -p "$artifact_dir/$(dirname "$path")"
    cp -R "$repo_dir/$path" "$artifact_dir/$path"
  fi
}

write_manifest() {
  local manifest="$artifact_dir/MANIFEST.txt"

  {
    echo "name=agents-devkits"
    echo "created_at_utc=$timestamp"
    echo "source=$(git -C "$repo_dir" remote get-url origin 2>/dev/null || echo unknown)"
    echo "commit=$(git -C "$repo_dir" rev-parse --short HEAD 2>/dev/null || echo unknown)"
    echo "branch=$(git -C "$repo_dir" branch --show-current 2>/dev/null || echo unknown)"
    echo
    echo "Safe export policy:"
    echo "- includes portable scripts, profiles, sanitized Codex config, Serena config, and MCP checks"
    echo "- excludes .git, exports, secrets.local.env, secrets/, auth state, SSH keys, caches, sessions, and GUI app installs"
    echo
    echo "Restore:"
    echo "1. tar -xzf $artifact_name.tar.gz"
    echo "2. cd $artifact_name"
    echo "3. cp secrets.example.env secrets.local.env"
    echo "4. edit secrets.local.env"
    echo "5. ./restore.sh --profile base --profile web --profile ai"
  } > "$manifest"
}

echo "==> Refreshing portable state"
"$repo_dir/backup.sh"
"$repo_dir/scripts/snapshot.sh"

echo "==> Running validation"
"$repo_dir/scripts/test.sh"
"$repo_dir/scripts/secret-guard.sh" "$repo_dir"

mkdir -p "$artifact_dir" "$export_root"

echo "==> Building allowlist export"
copy_path ".gitignore"
copy_path "Brewfile"
copy_path "config"
copy_path "README.md"
copy_path "backup.sh"
copy_path "bootstrap.sh"
copy_path "doctor.sh"
copy_path "install.sh"
copy_path "mcp"
copy_path "profiles"
copy_path "scripts"
copy_path "secrets.example.env"
copy_path "serena"
copy_path "sync.sh"
copy_path "setup.ps1"
copy_path "restore.sh"
copy_path "gstack"

write_manifest

"$artifact_dir/scripts/secret-guard.sh" "$artifact_dir"

echo "==> Creating archive"
tar -C "$staging_dir" -czf "$archive_path" "$artifact_name"

(
  cd "$export_root"
  shasum -a 256 "$(basename "$archive_path")" > "$(basename "$checksum_path")"
)

echo "Archive: $archive_path"
echo "Checksum: $checksum_path"
