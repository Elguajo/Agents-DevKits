#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"

echo "==> library maintenance requests load skill-authoring"
grep -Fq 'When a user asks in natural language to create, add, change, retire, remove, or' "$repo_root/AGENTS.md"
grep -Fq 'load `skills/skill-authoring/SKILL.md` before making library' "$repo_root/AGENTS.md"
grep -Fq '“создай скилл”' "$repo_root/AGENTS.md"
grep -Fq 'an explicit `$skill-authoring` mention is not' "$repo_root/AGENTS.md"
grep -Fq 'Use before creating, adding, changing, retiring, removing, or turning a prompt/workflow' "$repo_root/skills/skill-authoring/SKILL.md"

echo "==> consumer diagnostic routing excludes skill-authoring"
route="$(python3 "$repo_root/scripts/platform.py" route --registry "$repo_root/skills/registry.yaml" --capabilities "$repo_root/capabilities/registry.yaml" --repo-root "$repo_root" --fact task.skill_authoring)"
python3 - "$route" <<'PY'
import json
import sys

result = json.loads(sys.argv[1])
assert result["skills"] == [], result
PY
