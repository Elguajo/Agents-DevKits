#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
fixture_root="$(mktemp -d)"
trap 'rm -rf "$fixture_root"' EXIT

git -C "$fixture_root" init -q
git -C "$fixture_root" config user.name "Agents DevKits test"
git -C "$fixture_root" config user.email "test@example.invalid"
printf 'tracked\n' > "$fixture_root/tracked.txt"
git -C "$fixture_root" add tracked.txt
git -C "$fixture_root" commit -qm "initial"

printf 'staged\n' > "$fixture_root/staged.txt"
git -C "$fixture_root" add staged.txt
printf 'unstaged\n' > "$fixture_root/unstaged.txt"
head_tree_before="$(git -C "$fixture_root" rev-parse HEAD^{tree})"
index_tree_before="$(git -C "$fixture_root" write-tree)"

(
  cd "$fixture_root"
  bash "$repo_root/skills/credit-codex-contributor/scripts/create-attribution-commit.sh"
)

[[ "$(git -C "$fixture_root" rev-parse HEAD^{tree})" == "$head_tree_before" ]]
[[ "$(git -C "$fixture_root" write-tree)" == "$index_tree_before" ]]
test "$(git -C "$fixture_root" diff --cached --name-only)" = "staged.txt"
test -f "$fixture_root/unstaged.txt"
git -C "$fixture_root" log -1 --format=%B | grep -Fxq 'Co-authored-by: Codex <noreply@openai.com>'
echo "credit attribution regression passed"
