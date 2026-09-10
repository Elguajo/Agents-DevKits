#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -ne 0 ]]; then
  echo "Usage: $0" >&2
  exit 2
fi

git rev-parse --is-inside-work-tree >/dev/null
git rev-parse --verify HEAD >/dev/null

head_tree_before="$(git rev-parse HEAD^{tree})"
index_tree_before="$(git write-tree)"
temporary_index="$(mktemp "${TMPDIR:-/tmp}/agents-devkits-attribution-index.XXXXXX")"
trap 'rm -f "$temporary_index"' EXIT

GIT_INDEX_FILE="$temporary_index" git read-tree HEAD
GIT_INDEX_FILE="$temporary_index" git commit --allow-empty \
  -m "chore: credit OpenAI Codex" \
  -m "Co-authored-by: Codex <noreply@openai.com>"

if [[ "$(git rev-parse HEAD^{tree})" != "$head_tree_before" ]]; then
  echo "Refusing to continue: attribution commit changed the repository tree" >&2
  exit 1
fi

if [[ "$(git write-tree)" != "$index_tree_before" ]]; then
  echo "Refusing to continue: attribution commit changed the caller's index" >&2
  exit 1
fi
