#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
host_name="$(hostname -s 2>/dev/null || hostname)"
state_file="$repo_dir/machines/$host_name/enabled-mcps.txt"
default_file="$repo_dir/mcp/profiles/default.txt"
failures=0

status() { printf '%-8s %s\n' "$1" "$2"; }
source_file="$default_file"; [[ -f "$state_file" ]] && source_file="$state_file"
echo "MCP selection source: $source_file"
has_command() { command -v "$1" >/dev/null 2>&1; }

while IFS= read -r name || [[ -n "$name" ]]; do
  name="${name%%#*}"; name="${name//[[:space:]]/}"
  [[ -n "$name" ]] || continue
  definition="$repo_dir/mcp/definitions/$name.toml"
  if [[ ! -f "$definition" ]]; then status ERROR "missing definition for $name"; failures=$((failures + 1)); continue; fi
  runtime=npx
  case "$name" in serena) runtime=uvx ;; affine) runtime=affine-mcp ;; open-pencil) runtime=openpencil-mcp ;; chrome-devtools) status WARN 'chrome-devtools expects http://localhost:3000/mcp'; continue ;; ideon) status WARN 'ideon expects http://localhost:5353/api/mcp and IDEON_MCP_TOKEN'; continue ;; esac
  if has_command "$runtime"; then status OK "$name ($runtime)"; else status WARN "$name requires $runtime"; fi
done < "$source_file"

for secret in CONTEXT7_API_KEY ANYTYPE_HEADERS AFFINE_BASE_URL AFFINE_TOOL_PROFILE IDEON_MCP_TOKEN; do
  if [[ -n "${!secret:-}" ]]; then status OK "$secret configured"; else status WARN "$secret is unset; placeholder remains"; fi
done
if [[ "$failures" -gt 0 ]]; then status ERROR "MCP doctor found $failures invalid definition(s)"; exit 1; fi
status OK 'MCP doctor completed'
