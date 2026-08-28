#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"

echo "==> platform contracts"
python3 "$repo_root/scripts/platform.py" capabilities
python3 "$repo_root/scripts/platform.py" evidence
python3 "$repo_root/scripts/validate_registry.py"

echo "==> invalid registry fixture"
fixture_root="$(mktemp -d)"
tmp_home=""
cleanup() {
  rm -rf "$fixture_root"
  [[ -z "$tmp_home" ]] || rm -rf "$tmp_home"
}
trap cleanup EXIT
cp "$repo_root/skills/registry.yaml" "$fixture_root/registry.yaml"
python3 - "$fixture_root/registry.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('name: product-spec', 'name: missing-skill', 1))
PY
if python3 "$repo_root/scripts/platform.py" registry --registry "$fixture_root/registry.yaml" --repo-root "$repo_root" >/tmp/agents-devkits-invalid-registry.log 2>&1; then
  echo "Expected invalid registry to fail" >&2
  exit 1
fi
grep -q 'frontmatter name does not match registry' /tmp/agents-devkits-invalid-registry.log

echo "==> invalid routing policy is rejected"
cp "$repo_root/skills/registry.yaml" "$fixture_root/routing-registry.yaml"
python3 - "$fixture_root/routing-registry.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('model: auto', 'model: invalid', 1))
PY
if python3 "$repo_root/scripts/platform.py" registry --registry "$fixture_root/routing-registry.yaml" --repo-root "$repo_root" >/tmp/agents-devkits-invalid-routing-registry.log 2>&1; then
  echo "Expected invalid routing policy to fail" >&2
  exit 1
fi
grep -q 'routing.defaults uses an unknown tier' /tmp/agents-devkits-invalid-routing-registry.log

echo "==> invalid capability fixture"
cp "$repo_root/capabilities/registry.yaml" "$fixture_root/capabilities.yaml"
python3 - "$fixture_root/capabilities.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('repository:', 'Repository:', 1))
PY
if python3 "$repo_root/scripts/platform.py" capabilities --capabilities "$fixture_root/capabilities.yaml" >/tmp/agents-devkits-invalid-capability-registry.log 2>&1; then
  echo "Expected invalid capability registry to fail" >&2
  exit 1
fi
grep -q 'Invalid capability name' /tmp/agents-devkits-invalid-capability-registry.log

echo "==> vendored provenance requires a local source record"
cp "$repo_root/skills/registry.yaml" "$fixture_root/provenance-registry.yaml"
python3 - "$fixture_root/provenance-registry.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('source_file: skills/frontend-design/SOURCE.md', 'source_file: missing-source.md', 1))
PY
if python3 "$repo_root/scripts/platform.py" registry --registry "$fixture_root/provenance-registry.yaml" --repo-root "$repo_root" >/tmp/agents-devkits-invalid-provenance.log 2>&1; then
  echo "Expected invalid vendored provenance to fail" >&2
  exit 1
fi
grep -q 'source_file does not exist' /tmp/agents-devkits-invalid-provenance.log

echo "==> installer isolated home"
tmp_home="$(mktemp -d)"
HOME="$tmp_home" "$repo_root/bootstrap.sh" >/tmp/agents-devkits-bootstrap.log
test -L "$tmp_home/.codex/skills/product-spec"
test -L "$tmp_home/.claude/skills/product-spec"
for target_skill in "$tmp_home/.codex/skills/product-spec" "$tmp_home/.claude/skills/product-spec"; do
  unlink "$target_skill"
  mkdir "$target_skill"
  touch "$target_skill/sentinel"
done
HOME="$tmp_home" "$repo_root/bootstrap.sh" >/tmp/agents-devkits-bootstrap-repeat.log
test -f "$tmp_home/.codex/skills/product-spec/sentinel"
test -f "$tmp_home/.claude/skills/product-spec/sentinel"
HOME="$tmp_home" "$repo_root/bootstrap.sh" --adopt >/tmp/agents-devkits-bootstrap-adopt.log
test -L "$tmp_home/.codex/skills/product-spec"
test -L "$tmp_home/.claude/skills/product-spec"
find "$tmp_home/.agent-skills-backups" -type f -name sentinel | grep -q .

echo "platform fixtures passed"
