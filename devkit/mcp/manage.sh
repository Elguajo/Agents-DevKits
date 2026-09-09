#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
host_name="$(hostname -s 2>/dev/null || hostname)"
state_file="$repo_dir/machines/$host_name/enabled-mcps.txt"
default_file="$repo_dir/mcp/profiles/default.txt"
command="${1:-list}"

usage() {
  cat <<'HELP'
Usage: ./devkit.sh mcp <command> [name]

Commands:
  list            Show enabled portable MCP definitions.
  enable <name>   Enable a known MCP locally for this machine.
  disable <name>  Disable an MCP locally for this machine.
  doctor          Validate dependencies for enabled MCPs.
HELP
}

selected_file() {
  [[ -f "$state_file" ]] && printf '%s\n' "$state_file" || printf '%s\n' "$default_file"
}

read_selected() {
  local source
  source="$(selected_file)"
  while IFS= read -r name || [[ -n "$name" ]]; do
    name="${name%%#*}"
    name="${name//[[:space:]]/}"
    [[ -n "$name" ]] && printf '%s\n' "$name"
  done < "$source"
}

validate_name() {
  local name="$1"
  [[ "$name" =~ ^[a-z0-9-]+$ && -f "$repo_dir/mcp/definitions/$name.toml" ]] || {
    echo "Unknown MCP: $name" >&2
    echo "Known MCPs:" >&2
    find "$repo_dir/mcp/definitions" -maxdepth 1 -name '*.toml' -exec basename {} .toml \; | sort >&2
    exit 1
  }
}

write_selected() {
  mkdir -p "$(dirname "$state_file")"
  { echo "# Local MCP selection for $host_name. This file is ignored by Git."; cat; } | awk 'NF && !seen[$0]++' | sort -u > "$state_file"
}

case "$command" in
  list)
    echo "MCP selection source: $(selected_file)"
    read_selected
    ;;
  enable)
    name="${2:-}"
    [[ -n "$name" ]] || { echo "mcp enable requires a name" >&2; exit 1; }
    validate_name "$name"
    { read_selected; echo "$name"; } | write_selected
    echo "Enabled MCP '$name' for $host_name. Run install to regenerate Codex config."
    ;;
  disable)
    name="${2:-}"
    [[ -n "$name" ]] || { echo "mcp disable requires a name" >&2; exit 1; }
    validate_name "$name"
    read_selected | awk -v remove="$name" '$0 != remove' | write_selected
    echo "Disabled MCP '$name' for $host_name. Run install to regenerate Codex config."
    ;;
  doctor)
    shift || true
    "$repo_dir/mcp/doctor.sh" "$@"
    ;;
  help|-h|--help)
    usage
    ;;
  *)
    echo "Unknown MCP command: $command" >&2
    usage >&2
    exit 1
    ;;
esac
