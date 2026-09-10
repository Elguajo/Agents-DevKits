#!/usr/bin/env bash
set -euo pipefail

root="${1:-.}"

if [[ ! -d "$root" ]]; then
  echo "Shell syntax root does not exist: $root" >&2
  exit 2
fi

while IFS= read -r -d '' script; do
  bash -n "$script"
done < <(find "$root" -type f -name '*.sh' -not -path '*/.git/*' -print0)
