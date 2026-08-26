#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
tmp_root="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_root"
}
trap cleanup EXIT

echo "==> project init creates thin v2 templates"
mkdir "$tmp_root/new-project"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/new-project" >/tmp/agents-devkits-project-init.log
test -f "$tmp_root/new-project/AGENTS.md"
test -f "$tmp_root/new-project/CLAUDE.md"
test -f "$tmp_root/new-project/agents-devkits.yaml"
test ! -e "$tmp_root/new-project/.agents/skills"
test ! -e "$tmp_root/new-project/.claude/skills"
python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/new-project/agents-devkits.yaml"

echo "==> adapters expose the same generic routing contract"
grep -q 'canonical `skills/registry.yaml`' "$tmp_root/new-project/AGENTS.md"
grep -q 'canonical `skills/registry.yaml`' "$tmp_root/new-project/CLAUDE.md"
grep -q 'declared references on demand' "$tmp_root/new-project/AGENTS.md"
grep -q 'declared references on demand' "$tmp_root/new-project/CLAUDE.md"

echo "==> doctor resolves canonical skills and platform version"
HOME="$tmp_root/home" "$repo_root/bootstrap.sh" >/tmp/agents-devkits-project-bootstrap.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/new-project" >/tmp/agents-devkits-project-doctor.log
grep -q 'Doctor passed' /tmp/agents-devkits-project-doctor.log

echo "==> existing instructions are preserved and adoption is idempotent"
mkdir "$tmp_root/existing-project"
printf '# Existing instructions\n' > "$tmp_root/existing-project/AGENTS.md"
HOME="$tmp_root/home" "$repo_root/project.sh" init --agent codex --path "$tmp_root/existing-project" >/tmp/agents-devkits-project-preserve.log
grep -q '^# Existing instructions$' "$tmp_root/existing-project/AGENTS.md"
test -f "$tmp_root/existing-project/.agents-devkits/codex-integration.md"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --agent codex --adopt --path "$tmp_root/existing-project" >/tmp/agents-devkits-project-adopt.log
grep -q '<!-- agents-devkits:codex:start -->' "$tmp_root/existing-project/AGENTS.md"
find "$tmp_root/existing-project/.agents-devkits/backups" -type f -name 'AGENTS.md.*.backup' | grep -q .
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --agent codex --adopt --path "$tmp_root/existing-project" >/tmp/agents-devkits-project-readopt.log
grep -q 'Already adopted' /tmp/agents-devkits-project-readopt.log

echo "==> task-aware verification resolves only matching checks"
mkdir "$tmp_root/verify-project"
cp "$repo_root/templates/project/agents-devkits.yaml" "$tmp_root/verify-project/agents-devkits.yaml"
python3 - "$tmp_root/verify-project/agents-devkits.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace(
    'baseline: []',
    '''baseline:
    - id: unit-tests
      kind: test
      command: python3
      args: ["-c", "print('unit check')"]''',
).replace(
    'conditions: []',
    '''conditions:
    - when:
        paths: ["src/ui/**"]
      run:
        - id: browser-check
          kind: browser
          command: python3
          args: ["-c", "print('browser check')"]
      require_reviews: ["visual-qa", "accessibility-review"]
    - when:
        risks: ["security"]
      require_reviews: ["security-review"]''',
))
PY
HOME="$tmp_root/home" python3 "$repo_root/project.py" verify --path "$tmp_root/verify-project" --json >/tmp/agents-devkits-project-baseline.json
grep -q 'unit-tests' /tmp/agents-devkits-project-baseline.json
if grep -q 'browser-check' /tmp/agents-devkits-project-baseline.json; then
  echo 'UI verification ran without a matching changed path' >&2
  exit 1
fi
HOME="$tmp_root/home" python3 "$repo_root/project.py" verify --path "$tmp_root/verify-project" --changed src/ui/button.tsx --json >/tmp/agents-devkits-project-ui.json
grep -q 'browser-check' /tmp/agents-devkits-project-ui.json
grep -q 'visual-qa' /tmp/agents-devkits-project-ui.json
HOME="$tmp_root/home" python3 "$repo_root/project.py" verify --path "$tmp_root/verify-project" --task 'Check OAuth callback' --json >/tmp/agents-devkits-project-security.json
grep -q 'security-review' /tmp/agents-devkits-project-security.json

echo "==> failed and unavailable checks remain distinct evidence"
python3 - "$tmp_root/verify-project/agents-devkits.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace("print('unit check')", 'raise SystemExit(1)'))
PY
if HOME="$tmp_root/home" python3 "$repo_root/project.py" verify --path "$tmp_root/verify-project" --json >/tmp/agents-devkits-project-failed.json 2>&1; then
  echo 'Expected failed verification to fail' >&2
  exit 1
fi
grep -q '"failed"' /tmp/agents-devkits-project-failed.json
python3 - "$tmp_root/verify-project/agents-devkits.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('command: python3', 'command: missing-agents-devkits-command', 1))
PY
if HOME="$tmp_root/home" python3 "$repo_root/project.py" verify --path "$tmp_root/verify-project" --json >/tmp/agents-devkits-project-unavailable.json 2>&1; then
  echo 'Expected unavailable verification to fail' >&2
  exit 1
fi
grep -q '"unavailable"' /tmp/agents-devkits-project-unavailable.json

echo "==> doctor detects incompatible platform and missing required capability"
cp "$repo_root/templates/project/agents-devkits.yaml" "$tmp_root/invalid-project.yaml"
python3 - "$tmp_root/invalid-project.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('>=1.0 <2.0', '>=2.0 <3.0').replace('required:\n    - repository', 'required:\n    - browser'))
PY
mkdir "$tmp_root/invalid-project"
cp "$tmp_root/invalid-project.yaml" "$tmp_root/invalid-project/agents-devkits.yaml"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --agent codex --path "$tmp_root/invalid-project" >/tmp/agents-devkits-project-invalid-init.log
if HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/invalid-project" >/tmp/agents-devkits-project-invalid-doctor.log 2>&1; then
  echo 'Expected incompatible project doctor to fail' >&2
  exit 1
fi
grep -q 'platform version' /tmp/agents-devkits-project-invalid-doctor.log
grep -q 'required capability: browser' /tmp/agents-devkits-project-invalid-doctor.log

echo "==> legacy v1 manifest remains readable"
mkdir "$tmp_root/legacy-project"
python3 - "$tmp_root/legacy-project/agents-devkits.yaml" <<'PY'
from pathlib import Path
import sys

Path(sys.argv[1]).write_text('''schema_version: 1
agents:
  - codex
skills:
  - codebase-explorer
capabilities:
  - name: repository
    requirement: required
verification:
  required: []
  conditional: []
''')
PY
python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/legacy-project/agents-devkits.yaml"

echo "==> unknown manifest skill, capability, and shell command are rejected"
cp "$repo_root/templates/project/agents-devkits.yaml" "$tmp_root/invalid-manifest.yaml"
python3 - "$tmp_root/invalid-manifest.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('codebase-explorer', 'missing-skill', 1))
PY
if python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/invalid-manifest.yaml" >/tmp/agents-devkits-project-unknown-skill.log 2>&1; then
  echo 'Expected unknown skill to fail manifest validation' >&2
  exit 1
fi
grep -q 'unknown skills' /tmp/agents-devkits-project-unknown-skill.log
cp "$repo_root/templates/project/agents-devkits.yaml" "$tmp_root/invalid-manifest.yaml"
python3 - "$tmp_root/invalid-manifest.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('repository', 'made-up-capability', 1).replace(
    'baseline: []',
    'baseline:\n    - id: unsafe\n      command: "python3; touch should-not-exist"\n      args: []',
))
PY
if python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/invalid-manifest.yaml" >/tmp/agents-devkits-project-unknown-capability.log 2>&1; then
  echo 'Expected unknown capability to fail manifest validation' >&2
  exit 1
fi
grep -q 'unknown capability' /tmp/agents-devkits-project-unknown-capability.log
cp "$repo_root/templates/project/agents-devkits.yaml" "$tmp_root/invalid-manifest.yaml"
python3 - "$tmp_root/invalid-manifest.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace(
    'baseline: []',
    'baseline:\n    - id: unsafe\n      command: "python3; touch should-not-exist"\n      args: []',
))
PY
if python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/invalid-manifest.yaml" >/tmp/agents-devkits-project-unsafe-command.log 2>&1; then
  echo 'Expected shell expression to fail manifest validation' >&2
  exit 1
fi
grep -q 'simple command name' /tmp/agents-devkits-project-unsafe-command.log

echo "project runtime tests passed"
