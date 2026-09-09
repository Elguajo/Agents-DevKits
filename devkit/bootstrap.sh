#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
profiles=()
dry_run=false
assume_yes=false
all_profiles=(base web ai db mobile macos)

usage() {
  cat <<'HELP'
Usage: ./bootstrap.sh [options]

Options:
  --profile <name>  Apply a profile. Can be repeated.
  --all             Apply every tracked profile.
  --dry-run         Print actions without changing the machine.
  --yes             Skip confirmation prompts where possible.
  -h, --help        Show this help.

Profiles:
  base    Core CLI, shell, Git, GitHub, editor support.
  web     Node/web app tooling and browser automation.
  ai      AI coding and MCP-related tooling.
  db      Local database and data tooling.
  mobile  iOS/macOS development tooling.
  macos   macOS defaults for developer ergonomics.
HELP
}

available_profiles() {
  printf '%s\n' "${all_profiles[@]}"
}

run() {
  if [[ "$dry_run" == true ]]; then
    printf 'dry-run:'
    printf ' %q' "$@"
    printf '\n'
    return
  fi

  "$@"
}

require_command() {
  local command_name="$1"
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Missing required command: $command_name" >&2
    return 1
  fi
}

add_profile() {
  local profile="$1"

  if [[ -z "$profile" || "$profile" == --* ]]; then
    echo "--profile requires a profile name" >&2
    exit 1
  fi

  if [[ ! -d "$repo_dir/profiles/$profile" ]]; then
    echo "Unknown profile: $profile" >&2
    echo "Available profiles: ${all_profiles[*]}" >&2
    exit 1
  fi

  if [[ "${#profiles[@]}" -gt 0 ]]; then
    local existing
    for existing in "${profiles[@]}"; do
      [[ "$existing" == "$profile" ]] && return
    done
  fi

  profiles+=("$profile")
}

confirm() {
  local prompt="$1"
  if [[ "$assume_yes" == true || "$dry_run" == true ]]; then
    return 0
  fi

  read -r -p "$prompt [y/N] " answer
  [[ "$answer" == "y" || "$answer" == "Y" ]]
}

apply_brewfile() {
  local brewfile="$1"
  [[ -f "$brewfile" ]] || return 0

  if [[ "$dry_run" != true ]]; then
    require_command brew
  fi

  run brew bundle --file "$brewfile"
}

apply_profile() {
  local profile="$1"
  local profile_dir="$repo_dir/profiles/$profile"

  if [[ ! -d "$profile_dir" ]]; then
    echo "Unknown profile: $profile" >&2
    exit 1
  fi

  echo "==> Applying profile: $profile"
  apply_brewfile "$profile_dir/Brewfile"

  if [[ -x "$profile_dir/apply.sh" ]]; then
    run "$profile_dir/apply.sh"
  fi
}

parse_args() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --profile)
        if [[ $# -lt 2 ]]; then
          echo "--profile requires a profile name" >&2
          exit 1
        fi
        add_profile "$2"
        shift 2
        ;;
      --all)
        profiles=()
        local profile
        for profile in "${all_profiles[@]}"; do
          add_profile "$profile"
        done
        shift
        ;;
      --dry-run)
        dry_run=true
        shift
        ;;
      --yes)
        assume_yes=true
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        echo "Unknown argument: $1" >&2
        usage >&2
        exit 1
        ;;
    esac
  done

  if [[ "${#profiles[@]}" -eq 0 ]]; then
    profiles=()
    add_profile base
    add_profile web
    add_profile ai
  fi
}

parse_args "$@"

if [[ "$(uname -s)" != "Darwin" ]]; then
  echo "This bootstrap is designed for macOS. Current OS: $(uname -s)" >&2
  exit 1
fi

if [[ "$dry_run" != true ]]; then
  if ! command -v brew >/dev/null 2>&1; then
    echo "Homebrew is required before bootstrap can install packages." >&2
    echo "Install it from https://brew.sh, then rerun this script." >&2
    exit 1
  fi
fi

echo "Bootstrap profiles: ${profiles[*]}"

if confirm "Install Homebrew packages and apply local developer settings?"; then
  for profile in "${profiles[@]}"; do
    apply_profile "$profile"
  done

  run "$repo_dir/install.sh"
  run "$repo_dir/scripts/auth.sh"
  run "$repo_dir/doctor.sh"
  "$repo_dir/scripts/manual-steps.sh"
else
  echo "Bootstrap cancelled."
fi
