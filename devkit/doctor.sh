#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
failures=0

status() { printf '%-8s %s\n' "$1" "$2"; }
check_command() {
  local name="$1" required="$2"
  if command -v "$name" >/dev/null 2>&1; then
    status OK "$name: $(command -v "$name")"
  else
    status "$([[ "$required" == true ]] && echo MISSING || echo WARN)" "$name"
    [[ "$required" == true ]] && failures=$((failures + 1))
  fi
}

echo 'Platform'
if [[ "$(uname -s)" == Darwin ]]; then
  status OK "macOS $(sw_vers -productVersion 2>/dev/null || echo unknown) ($(uname -m))"
else
  status ERROR "Unsupported Unix platform: $(uname -s); use setup.ps1 on Windows."
  failures=$((failures + 1))
fi
status OK "shell: ${SHELL:-unknown}"

echo
echo 'Core'
check_command brew false
check_command git true
check_command gh true
check_command node true
check_command npm true
check_command pnpm true
check_command bun true
check_command python3 true
check_command uv true
check_command uvx true
check_command rg true
check_command codex false

if command -v gh >/dev/null 2>&1; then
  if gh auth status >/dev/null 2>&1; then status OK 'gh auth'; else status WARN 'gh auth is not configured'; fi
fi

echo
echo 'Codex'
[[ -f "$repo_dir/config/portable/base.toml" ]] && status OK 'portable config sources' || { status ERROR 'portable config sources missing'; failures=$((failures + 1)); }
[[ -f "$repo_dir/config/platform/macos.toml" ]] && status OK 'macOS config layer' || { status ERROR 'macOS config layer missing'; failures=$((failures + 1)); }
if [[ -f "$HOME/.codex/config.toml" ]]; then
  if rg -q '__[A-Z0-9_]+__' "$HOME/.codex/config.toml"; then status WARN 'installed Codex config contains unresolved placeholders'; else status OK 'installed Codex config'; fi
else
  status WARN 'Codex config not installed'
fi
[[ -d /Applications/Codex.app ]] && status OK 'Codex.app detected' || status WARN 'Codex.app not detected (optional desktop integration)'

echo
echo 'AI'
if [[ -f "$HOME/.serena/serena_config.yml" ]]; then status OK 'Serena config present'; else status WARN 'Serena config not installed'; fi
if "$repo_dir/mcp/doctor.sh"; then :; else failures=$((failures + 1)); fi
if "$repo_dir/gstack/manage.sh" status >/dev/null 2>&1; then status OK 'Gstack pinned revision installed'; else status WARN 'Gstack not installed or differs from pin'; fi

if [[ "$failures" -gt 0 ]]; then status ERROR "doctor found $failures required issue(s)"; exit 1; fi
status OK 'doctor completed without required issues'
