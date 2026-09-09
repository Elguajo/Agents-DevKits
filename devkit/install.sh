#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_serena_config="$repo_dir/serena/serena_config.yml"
target_dir="$HOME/.codex"
target_config="$target_dir/config.toml"
serena_target_dir="$HOME/.serena"
serena_target_config="$serena_target_dir/serena_config.yml"
dry_run=false

if [[ "${1:-}" == "--dry-run" ]]; then
  dry_run=true
elif [[ $# -gt 0 ]]; then
  echo "Usage: ./install.sh [--dry-run]" >&2
  exit 1
fi

if [[ -f "$repo_dir/secrets.local.env" ]]; then
  # shellcheck disable=SC1091
  source "$repo_dir/secrets.local.env"
fi

tmp_config="$(mktemp)"
trap 'rm -f "$tmp_config"' EXIT

replace_placeholder() {
  local placeholder="$1"
  local value="$2"
  [[ -n "$value" ]] || return 0
  # Values land inside TOML basic strings, including JSON-shaped MCP headers.
  PLACEHOLDER="$placeholder" REPLACEMENT="$value" perl -0pi -e '$r=$ENV{REPLACEMENT}; $r =~ s/\\/\\\\/g; $r =~ s/"/\\"/g; $r =~ s/\r?\n/\\n/g; s/\Q$ENV{PLACEHOLDER}\E/$r/g' "$tmp_config"
}

if [[ "$dry_run" == false ]]; then
  mkdir -p "$target_dir"
  if [[ -f "$target_config" ]]; then
    "$repo_dir/backup.sh"
    backup="$target_config.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$target_config" "$backup"
    echo "Backed up existing config to $backup"
  fi
fi

"$repo_dir/scripts/compose-config.sh" --output "$tmp_config" --platform macos
replace_placeholder "__CONTEXT7_API_KEY__" "${CONTEXT7_API_KEY:-}"
replace_placeholder "__ANYTYPE_HEADERS__" "${ANYTYPE_HEADERS:-}"
replace_placeholder "__AFFINE_BASE_URL__" "${AFFINE_BASE_URL:-}"
replace_placeholder "__AFFINE_TOOL_PROFILE__" "${AFFINE_TOOL_PROFILE:-}"
HOME_VALUE="$HOME" perl -0pi -e 's{__HOME__}{$ENV{HOME_VALUE}}g' "$tmp_config"

if [[ "$dry_run" == true ]]; then
  echo "DRY-RUN Would back up and install composed Codex config to $target_config"
  echo "DRY-RUN Would adopt Serena dashboard settings at $serena_target_config"
  exit 0
fi

mv "$tmp_config" "$target_config"
chmod 600 "$target_config"

echo "Installed Codex config to $target_config"

if [[ -f "$source_serena_config" ]]; then
  mkdir -p "$serena_target_dir"

  if [[ -f "$serena_target_config" ]]; then
    backup="$serena_target_config.backup.$(date +%Y%m%d-%H%M%S)"
    cp "$serena_target_config" "$backup"
    echo "Backed up existing Serena config to $backup"

    if grep -q '^web_dashboard:' "$serena_target_config"; then
      perl -0pi -e 's/^web_dashboard:.*$/web_dashboard: true/m' "$serena_target_config"
    else
      printf "\nweb_dashboard: true\n" >> "$serena_target_config"
    fi

    if grep -q '^web_dashboard_open_on_launch:' "$serena_target_config"; then
      perl -0pi -e 's/^web_dashboard_open_on_launch:.*$/web_dashboard_open_on_launch: false/m' "$serena_target_config"
    else
      printf "web_dashboard_open_on_launch: false\n" >> "$serena_target_config"
    fi

    chmod 600 "$serena_target_config"
    echo "Patched Serena dashboard settings in $serena_target_config"
  else
    cp "$source_serena_config" "$serena_target_config"
    chmod 600 "$serena_target_config"
    echo "Installed Serena config to $serena_target_config"
  fi
fi
