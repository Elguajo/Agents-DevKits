#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
fixture_root="$(mktemp -d)"
trap 'rm -rf "$fixture_root"' EXIT

printf '#!/usr/bin/env bash\nprintf ok\n' > "$fixture_root/valid.sh"
printf '#!/usr/bin/env bash\nif then\n' > "$fixture_root/broken.sh"

if "$repo_root/scripts/check_shell_syntax.sh" "$fixture_root" >/tmp/agents-devkits-shell-syntax.log 2>&1; then
  echo "Expected a syntax error in a non-first shell file to fail" >&2
  exit 1
fi

grep -q 'syntax error' /tmp/agents-devkits-shell-syntax.log
echo "shell syntax regression passed"
