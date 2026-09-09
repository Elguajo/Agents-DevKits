#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
config_file="$repo_dir/config/external-tools/gstack.conf"
install_dir="$HOME/.gstack/repos/gstack"
command="${1:-status}"

usage() {
  cat <<'HELP'
Usage: ./devkit.sh gstack <install|update|status>

Gstack is checked out in ~/.gstack/repos/gstack at this repository's pinned
revision. Installation neither enables hooks nor automatic updates.
HELP
}

read_value() { sed -n "s/^$1=//p" "$config_file" | tail -n 1; }
require_command() { command -v "$1" >/dev/null 2>&1 || { echo "Missing required command: $1" >&2; exit 1; }; }

[[ -f "$config_file" ]] || { echo "Missing Gstack config: $config_file" >&2; exit 1; }
remote="$(read_value remote)"
revision="$(read_value revision)"
[[ "$remote" =~ ^https://github\.com/[A-Za-z0-9._-]+/[A-Za-z0-9._-]+\.git$ ]] || { echo "Invalid Gstack remote" >&2; exit 1; }
[[ "$revision" =~ ^[0-9a-f]{40}$ ]] || { echo "Gstack revision must be a full SHA" >&2; exit 1; }

status() {
  echo "Pinned Gstack revision: $revision"
  echo "Installation path: $install_dir"
  if [[ "$(uname -s)" != "Darwin" ]]; then
    echo "Gstack status: native PowerShell installation is unsupported upstream; use macOS or upstream Git Bash/MSYS separately."
    return 0
  fi
  [[ -d "$install_dir/.git" ]] || { echo "Gstack status: not installed"; return 1; }
  actual="$(git -C "$install_dir" rev-parse HEAD 2>/dev/null || true)"
  origin="$(git -C "$install_dir" remote get-url origin 2>/dev/null || true)"
  echo "Installed Gstack revision: ${actual:-invalid checkout}"
  echo "Remote status: $([[ "$origin" == "$remote" ]] && echo verified || echo mismatch)"
  [[ "$actual" == "$revision" && "$origin" == "$remote" ]] && { echo "Gstack status: pinned revision installed"; return 0; }
  echo "Gstack status: update required"
  return 1
}

install_or_update() {
  [[ "$(uname -s)" == "Darwin" ]] || { echo "Gstack install is unavailable: upstream requires Git Bash/MSYS on Windows, not native PowerShell." >&2; exit 1; }
  require_command git
  require_command bun
  if [[ -e "$install_dir" && ! -d "$install_dir/.git" ]]; then
    echo "Refusing to use $install_dir: it is not a Git checkout." >&2
    exit 1
  fi
  if [[ -d "$install_dir/.git" ]]; then
    [[ "$(git -C "$install_dir" remote get-url origin 2>/dev/null || true)" == "$remote" ]] || { echo "Refusing Gstack checkout with an unexpected origin." >&2; exit 1; }
    git -C "$install_dir" diff --quiet && git -C "$install_dir" diff --cached --quiet || { echo "Refusing Gstack update with local changes." >&2; exit 1; }
  else
    mkdir -p "$(dirname "$install_dir")"
    git init --quiet "$install_dir"
    git -C "$install_dir" remote add origin "$remote"
  fi
  git -C "$install_dir" fetch --depth 1 origin "$revision"
  git -C "$install_dir" checkout --detach --quiet FETCH_HEAD
  [[ "$(git -C "$install_dir" rev-parse HEAD)" == "$revision" ]] || { echo "Pinned revision verification failed." >&2; exit 1; }
  [[ -x "$install_dir/setup" ]] || { echo "Pinned Gstack checkout has no executable setup script." >&2; exit 1; }
  GSTACK_SKIP_COREUTILS=1 GSTACK_PLAN_TUNE_HOOKS=no "$install_dir/setup" --host codex --prefix --no-plan-tune-hooks
  status
}

case "$command" in
  install|update) install_or_update ;;
  status) status ;;
  help|-h|--help) usage ;;
  *) echo "Unknown Gstack command: $command" >&2; usage >&2; exit 1 ;;
esac
