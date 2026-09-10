#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "==> shell syntax"
bash "$repo_dir/../scripts/check_shell_syntax.sh" "$repo_dir"

echo "==> secret guard"
"$repo_dir/scripts/secret-guard.sh" "$repo_dir"

echo "==> MCP doctor"
"$repo_dir/mcp/doctor.sh"

echo "==> deterministic configuration composition"
composed_config="$(mktemp)"
selected_mcps="$(mktemp)"
trap 'rm -f "$composed_config" "$selected_mcps"' EXIT
printf 'context7\n' > "$selected_mcps"
"$repo_dir/scripts/compose-config.sh" --output "$composed_config" --platform macos --mcp-state "$selected_mcps"
grep -q '^\[mcp_servers.context7\]' "$composed_config"
grep -q '^\[plugins."github@openai-curated"\]' "$composed_config"
python3 -c 'import sys, tomllib; tomllib.load(open(sys.argv[1], "rb"))' "$composed_config"

echo "==> bootstrap dry-run defaults"
"$repo_dir/bootstrap.sh" --dry-run --yes >/tmp/agents-devkits-bootstrap-default.log
grep -q 'scripts/auth.sh' /tmp/agents-devkits-bootstrap-default.log

echo "==> bootstrap dry-run all profiles"
"$repo_dir/bootstrap.sh" --dry-run --yes --all >/tmp/agents-devkits-bootstrap-all.log

echo "==> bootstrap rejects unknown profile"
if "$repo_dir/bootstrap.sh" --dry-run --profile does-not-exist >/tmp/agents-devkits-bootstrap-invalid.log 2>&1; then
  echo "Expected unknown profile to fail" >&2
  exit 1
fi

echo "==> snapshot dry run through temp repo copy"
tmp_repo="$(mktemp -d)"
trap 'rm -f "$composed_config" "$selected_mcps"; rm -rf "$tmp_repo"' EXIT
cp -R "$repo_dir"/. "$tmp_repo"/
"$tmp_repo/sync.sh" snapshot >/tmp/agents-devkits-snapshot.log
test -f "$tmp_repo/snapshots/current/brew-formulae.txt"
test -f "$tmp_repo/snapshots/current/git-config.safe.txt"

echo "==> entrypoint and managed Gstack syntax"
for script in "$repo_dir/scripts/export.sh" "$repo_dir/restore.sh" "$repo_dir/sync.sh" "$repo_dir/gstack/manage.sh"; do
  bash -n "$script"
done

echo "tests passed"
