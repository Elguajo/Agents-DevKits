#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
host_name="$(hostname -s 2>/dev/null || hostname)"
source_config="$HOME/.codex/config.toml"
machine_dir="$repo_dir/machines/$host_name"
target_config="$machine_dir/codex.toml"

[[ -f "$source_config" ]] || { echo "Missing Codex config: $source_config" >&2; exit 1; }
mkdir -p "$machine_dir"
if [[ -f "$target_config" ]]; then
  backup="$target_config.backup.$(date +%Y%m%d-%H%M%S)"
  cp "$target_config" "$backup"
  echo "Backed up existing local machine layer to $backup"
fi

# Project trust and app integrations are useful but intentionally local. Do not
# copy app settings, auth, sessions, marketplace state, or arbitrary MCP data.
awk '
  /^notify[[:space:]]*=/ { print; next }
  /^\[/ { capture = ($0 ~ /^\[projects\./ || $0 ~ /^\[mcp_servers\.(node_repl|node_repl\.env|computer-use|pencil|illustrator)\]/) }
  capture { print }
' "$source_config" > "$target_config"
if [[ ! -s "$target_config" ]]; then
  printf '# No project trust entries were found in the local Codex config.\n' > "$target_config"
fi
chmod 600 "$target_config"
echo "Saved safe machine-local Codex layer to $target_config (ignored by Git)."
