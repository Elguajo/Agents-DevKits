#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
for python_command in python3 python; do
  if command -v "$python_command" >/dev/null 2>&1 && "$python_command" -c 'import sys; sys.exit(sys.version_info < (3, 10))' >/dev/null 2>&1; then
    "$python_command" "$repo_root/project.py" "$@"
    exit
  fi
done
echo "Project runtime requires Python 3.10 or newer (python3 or python)." >&2
exit 1
