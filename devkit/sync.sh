#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
command="${1:-help}"

case "$command" in
  doctor) shift || true; "$repo_dir/doctor.sh" "$@" ;;
  install) shift || true; "$repo_dir/install.sh" "$@" ;;
  auth) shift || true; "$repo_dir/scripts/auth.sh" "$@" ;;
  bootstrap) shift || true; "$repo_dir/bootstrap.sh" "$@" ;;
  backup) shift || true; "$repo_dir/backup.sh" "$@" ;;
  restore) shift || true; "$repo_dir/restore.sh" "$@" ;;
  snapshot) shift || true; "$repo_dir/scripts/snapshot.sh" "$@" ;;
  export) shift || true; "$repo_dir/scripts/export.sh" "$@" ;;
  mcp) shift || true; "$repo_dir/mcp/manage.sh" "$@" ;;
  mcp-doctor) shift || true; "$repo_dir/mcp/doctor.sh" "$@" ;;
  gstack) shift || true; "$repo_dir/gstack/manage.sh" "$@" ;;
  guard) shift || true; "$repo_dir/scripts/secret-guard.sh" "$repo_dir" "$@" ;;
  test) shift || true; "$repo_dir/scripts/test.sh" "$@" ;;
  help|-h|--help)
    cat <<'HELP'
Usage: ./devkit.sh <command>

Commands: doctor, bootstrap, install, backup, restore, snapshot, export, auth,
          mcp, mcp-doctor, gstack, guard, test

On Windows use .\setup.ps1 with the same command names.
HELP
    ;;
  *) echo "Unknown command: $command" >&2; "/sync.sh" help >&2; exit 1 ;;
esac
