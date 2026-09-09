#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
platform=""
output=""
state_file=""

usage() {
  cat <<'HELP'
Usage: scripts/compose-config.sh --output <path> [--platform macos|windows] [--mcp-state <path>]

Composes the tracked portable, platform, and optional local Codex layers.
HELP
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --output) output="${2:-}"; shift 2 ;;
    --platform) platform="${2:-}"; shift 2 ;;
    --mcp-state) state_file="${2:-}"; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 1 ;;
  esac
done

[[ -n "$output" ]] || { echo "--output is required" >&2; exit 1; }

if [[ -z "$platform" ]]; then
  case "$(uname -s)" in
    Darwin) platform="macos" ;;
    MINGW*|MSYS*|CYGWIN*) platform="windows" ;;
    *) echo "Unsupported platform for Codex composition: $(uname -s)" >&2; exit 1 ;;
  esac
fi
[[ "$platform" == "macos" || "$platform" == "windows" ]] || { echo "Unsupported platform: $platform" >&2; exit 1; }

host_name="$(hostname -s 2>/dev/null || hostname)"
default_state="$repo_dir/mcp/profiles/default.txt"
state_file="${state_file:-$repo_dir/machines/$host_name/enabled-mcps.txt}"
source_state="$default_state"
[[ -f "$state_file" ]] && source_state="$state_file"

tmp_output="$(mktemp)"
cleanup() { rm -f "$tmp_output"; }
trap cleanup EXIT

append_layer() {
  local path="$1"
  [[ -f "$path" ]] || { echo "Missing configuration layer: $path" >&2; exit 1; }
  printf '\n# Source: %s\n' "${path#$repo_dir/}" >> "$tmp_output"
  cat "$path" >> "$tmp_output"
  printf '\n' >> "$tmp_output"
}

append_layer "$repo_dir/config/portable/base.toml"
append_layer "$repo_dir/config/portable/plugins.toml"

while IFS= read -r server || [[ -n "$server" ]]; do
  server="${server%%#*}"
  server="${server//[[:space:]]/}"
  [[ -n "$server" ]] || continue
  [[ "$server" =~ ^[a-z0-9-]+$ ]] || { echo "Unsafe MCP name in $source_state: $server" >&2; exit 1; }
  append_layer "$repo_dir/mcp/definitions/$server.toml"
done < "$source_state"

append_layer "$repo_dir/config/platform/$platform.toml"
machine_layer="$repo_dir/machines/$host_name/codex.toml"
if [[ -f "$machine_layer" ]]; then
  append_layer "$machine_layer"
fi

if ! awk '/^\[/ { if (seen[$0]++) { print "Duplicate TOML table: " $0 > "/dev/stderr"; failed=1 } } END { exit failed }' "$tmp_output"; then
  echo "Refusing to compose ambiguous Codex configuration." >&2
  exit 1
fi

mkdir -p "$(dirname "$output")"
cp "$tmp_output" "$output"
echo "Composed Codex config: $output"
