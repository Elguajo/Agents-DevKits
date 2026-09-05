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
test -f "$tmp_root/new-project/.agents-devkits/ROUTING.md"
cmp "$repo_root/docs/ROUTING.md" "$tmp_root/new-project/.agents-devkits/ROUTING.md"
test ! -e "$tmp_root/new-project/.agents/skills"
test ! -e "$tmp_root/new-project/.claude/skills"
python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/new-project/agents-devkits.yaml"
grep -q '^knowledge:' "$tmp_root/new-project/agents-devkits.yaml"
grep -q '^  mode: standard$' "$tmp_root/new-project/agents-devkits.yaml"
grep -q '^  provider: agents-devkits$' "$tmp_root/new-project/agents-devkits.yaml"

echo "==> UI profile adds a brief and UI review gate without inventing commands"
mkdir "$tmp_root/ui-project"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/ui-project" --ui >/tmp/agents-devkits-project-ui-init.log
test -f "$tmp_root/ui-project/DESIGN.md"
grep -q 'design-qa' "$tmp_root/ui-project/agents-devkits.yaml"
grep -q 'visual-qa' "$tmp_root/ui-project/agents-devkits.yaml"
python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/ui-project/agents-devkits.yaml"
HOME="$tmp_root/home" python3 "$repo_root/project.py" verify --path "$tmp_root/ui-project" --changed src/ui/button.tsx --json >/tmp/agents-devkits-project-ui-profile.json
grep -q 'visual-qa' /tmp/agents-devkits-project-ui-profile.json
grep -q 'accessibility-review' /tmp/agents-devkits-project-ui-profile.json
if grep -q '"evidence": \[{' /tmp/agents-devkits-project-ui-profile.json; then
  echo 'UI profile must not invent an objective command' >&2
  exit 1
fi

echo "==> adapters expose the same generic routing contract"
grep -q 'canonical `skills/registry.yaml`' "$tmp_root/new-project/AGENTS.md"
grep -q 'canonical `skills/registry.yaml`' "$tmp_root/new-project/CLAUDE.md"
grep -q 'declared references on demand' "$tmp_root/new-project/AGENTS.md"
grep -q 'declared references on demand' "$tmp_root/new-project/CLAUDE.md"
grep -q 'project knowledge packs' "$tmp_root/new-project/AGENTS.md"
grep -q 'project knowledge packs' "$tmp_root/new-project/CLAUDE.md"
grep -q '`PROPOSE`' "$tmp_root/new-project/AGENTS.md"
grep -q '`ASK`' "$tmp_root/new-project/CLAUDE.md"

echo "==> routing snapshots are immutable until explicitly refreshed"
printf '# Local routing note\n' > "$tmp_root/new-project/.agents-devkits/ROUTING.md"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/new-project" >/tmp/agents-devkits-routing-keep.log
grep -q 'Local routing note' "$tmp_root/new-project/.agents-devkits/ROUTING.md"
if HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/new-project" >/tmp/agents-devkits-routing-stale.log 2>&1; then
  echo 'Expected a stale routing snapshot to fail doctor' >&2
  exit 1
fi
grep -q 'integration state: stale' /tmp/agents-devkits-routing-stale.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/new-project" --refresh-routing >/tmp/agents-devkits-routing-refresh.log
cmp "$repo_root/docs/ROUTING.md" "$tmp_root/new-project/.agents-devkits/ROUTING.md"
rm "$tmp_root/new-project/.agents-devkits/ROUTING.md"
if HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/new-project" >/tmp/agents-devkits-routing-missing.log 2>&1; then
  echo 'Expected a missing routing snapshot to fail doctor' >&2
  exit 1
fi
grep -q 'integration state: broken' /tmp/agents-devkits-routing-missing.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/new-project" >/tmp/agents-devkits-routing-recreate.log
cmp "$repo_root/docs/ROUTING.md" "$tmp_root/new-project/.agents-devkits/ROUTING.md"

echo "==> knowledge packs are opt-in, source-bounded, and checked by doctor"
mkdir "$tmp_root/knowledge-project"
mkdir -p "$tmp_root/knowledge-project/packages/design-system" "$tmp_root/knowledge-project/apps/web"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/knowledge-project" >/tmp/agents-devkits-knowledge-init.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" knowledge init --path "$tmp_root/knowledge-project" --source packages/design-system --source apps/web >/tmp/agents-devkits-knowledge-pack.log
test -f "$tmp_root/knowledge-project/.agents-devkits/knowledge/design-system.md"
grep -q 'packages/design-system' "$tmp_root/knowledge-project/agents-devkits.yaml"
python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/knowledge-project/agents-devkits.yaml"
HOME="$tmp_root/home" "$repo_root/bootstrap.sh" >/tmp/agents-devkits-knowledge-bootstrap.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/knowledge-project" >/tmp/agents-devkits-knowledge-doctor.log
grep -q 'knowledge pack' /tmp/agents-devkits-knowledge-doctor.log
if HOME="$tmp_root/home" python3 "$repo_root/project.py" knowledge init --path "$tmp_root/knowledge-project" --source ../outside >/tmp/agents-devkits-invalid-knowledge.log 2>&1; then
  echo 'Expected unsafe knowledge source to fail' >&2
  exit 1
fi
grep -q 'relative to the project root' /tmp/agents-devkits-invalid-knowledge.log
python3 - "$tmp_root/knowledge-project/agents-devkits.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('        - apps/web', '        - packages/design-system'))
PY
if python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/knowledge-project/agents-devkits.yaml" >/tmp/agents-devkits-duplicate-knowledge-source.log 2>&1; then
  echo 'Expected duplicate knowledge source to fail' >&2
  exit 1
fi
grep -q 'sources must not contain duplicates' /tmp/agents-devkits-duplicate-knowledge-source.log

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
if HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/existing-project" >/tmp/agents-devkits-project-pending.log 2>&1; then
  echo 'Expected snippet-only integration to remain pending' >&2
  exit 1
fi
grep -q 'integration state: pending' /tmp/agents-devkits-project-pending.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --agent codex --adopt --path "$tmp_root/existing-project" >/tmp/agents-devkits-project-adopt.log
grep -q '<!-- agents-devkits:codex:start -->' "$tmp_root/existing-project/AGENTS.md"
find "$tmp_root/existing-project/.agents-devkits/backups" -type f -name 'AGENTS.md.*.backup' | grep -q .
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --agent codex --adopt --path "$tmp_root/existing-project" >/tmp/agents-devkits-project-readopt.log
grep -q 'Already adopted' /tmp/agents-devkits-project-readopt.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/existing-project" >/tmp/agents-devkits-project-adopted-doctor.log
grep -q 'integration state: active' /tmp/agents-devkits-project-adopted-doctor.log

echo "==> Progressive Context Kit mode is detected and remains the project-state owner"
mkdir "$tmp_root/progressive-project"
mkdir "$tmp_root/progressive-project/.progressive"
printf '2.0.0\n' > "$tmp_root/progressive-project/.progressive/VERSION"
printf 'standalone\n' > "$tmp_root/progressive-project/.progressive/PROFILE"
printf 'ready\n' > "$tmp_root/progressive-project/.progressive/ADOPTION_STATE"
printf '# PCK router\n' > "$tmp_root/progressive-project/AGENTS.md"
printf '@AGENTS.md\n' > "$tmp_root/progressive-project/CLAUDE.md"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/progressive-project" >/tmp/agents-devkits-progressive-init.log
grep -q 'Project mode: progressive' /tmp/agents-devkits-progressive-init.log
grep -q '^# PCK router$' "$tmp_root/progressive-project/AGENTS.md"
test -f "$tmp_root/progressive-project/.agents-devkits/progressive-integration.md"
test -f "$tmp_root/progressive-project/.agents-devkits/ROUTING.md"
grep -q '^  mode: progressive$' "$tmp_root/progressive-project/agents-devkits.yaml"
if HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/progressive-project" >/tmp/agents-devkits-progressive-pending.log 2>&1; then
  echo 'Expected an unadopted progressive bridge to remain pending' >&2
  exit 1
fi
grep -q 'integration state: pending' /tmp/agents-devkits-progressive-pending.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/progressive-project" --adopt >/tmp/agents-devkits-progressive-adopt.log
grep -q '<!-- agents-devkits:progressive:start -->' "$tmp_root/progressive-project/AGENTS.md"
grep -q '<!-- PROJECT-SPECIFIC-INSTRUCTIONS -->' "$tmp_root/progressive-project/AGENTS.md"
grep -q 'Progressive Context Kit remains the owner' "$tmp_root/progressive-project/AGENTS.md"
grep -q '^@AGENTS.md$' "$tmp_root/progressive-project/CLAUDE.md"
find "$tmp_root/progressive-project/.agents-devkits/backups" -type f -name 'AGENTS.md.*.backup' | grep -q .
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/progressive-project" --adopt >/tmp/agents-devkits-progressive-readopt.log
grep -q 'Already adopted progressive bridge' /tmp/agents-devkits-progressive-readopt.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/progressive-project" >/tmp/agents-devkits-progressive-doctor.log
grep -q 'project mode: progressive' /tmp/agents-devkits-progressive-doctor.log
grep -q 'integration state: active' /tmp/agents-devkits-progressive-doctor.log

echo "==> PCK framework update preserves the DevKits bridge"
python3 - "$tmp_root/progressive-project/AGENTS.md" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
sentinel = '\n\n<!-- PROJECT-SPECIFIC-INSTRUCTIONS -->\n\n'
old = path.read_text()
assert sentinel in old
suffix = old.split(sentinel, 1)[1]
path.write_text('# Updated PCK router\n' + sentinel + suffix)
PY
grep -q '^# Updated PCK router$' "$tmp_root/progressive-project/AGENTS.md"
grep -q '<!-- agents-devkits:progressive:start -->' "$tmp_root/progressive-project/AGENTS.md"
HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/progressive-project" >/tmp/agents-devkits-progressive-updated-doctor.log
grep -q 'integration state: active' /tmp/agents-devkits-progressive-updated-doctor.log

echo "==> legacy progressive bridge placement is migrated into the preserved suffix"
mkdir -p "$tmp_root/progressive-migration/.progressive"
printf '2.0.0\n' > "$tmp_root/progressive-migration/.progressive/VERSION"
printf 'personal\n' > "$tmp_root/progressive-migration/.progressive/PROFILE"
printf 'ready\n' > "$tmp_root/progressive-migration/.progressive/ADOPTION_STATE"
printf '# PCK router\n\n<!-- agents-devkits:progressive:start -->\nlegacy bridge\n<!-- agents-devkits:progressive:end -->\n' > "$tmp_root/progressive-migration/AGENTS.md"
printf '@AGENTS.md\n' > "$tmp_root/progressive-migration/CLAUDE.md"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/progressive-migration" --adopt >/tmp/agents-devkits-progressive-migration.log
grep -q 'Migrated progressive bridge' /tmp/agents-devkits-progressive-migration.log
python3 - "$tmp_root/progressive-migration/AGENTS.md" <<'PY'
from pathlib import Path
import sys

content = Path(sys.argv[1]).read_text()
assert content.index('<!-- PROJECT-SPECIFIC-INSTRUCTIONS -->') < content.index('<!-- agents-devkits:progressive:start -->')
PY

echo "==> explicit standard mode persists even beside PCK metadata"
mkdir -p "$tmp_root/explicit-standard/.progressive"
printf '2.0.0\n' > "$tmp_root/explicit-standard/.progressive/VERSION"
printf 'standalone\n' > "$tmp_root/explicit-standard/.progressive/PROFILE"
printf 'ready\n' > "$tmp_root/explicit-standard/.progressive/ADOPTION_STATE"
printf '# Existing instructions\n' > "$tmp_root/explicit-standard/AGENTS.md"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/explicit-standard" --agent codex --mode standard --adopt >/tmp/agents-devkits-explicit-standard.log
grep -q '^  mode: standard$' "$tmp_root/explicit-standard/agents-devkits.yaml"
HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/explicit-standard" --agent codex >/tmp/agents-devkits-persisted-standard.log
grep -q 'Project mode: standard' /tmp/agents-devkits-persisted-standard.log
HOME="$tmp_root/home" python3 "$repo_root/project.py" doctor --path "$tmp_root/explicit-standard" >/tmp/agents-devkits-explicit-standard-doctor.log
grep -q 'integration state: active' /tmp/agents-devkits-explicit-standard-doctor.log

echo "==> pending PCK adoption is rejected before DevKits writes project files"
mkdir -p "$tmp_root/pending-progressive/.progressive"
printf '2.0.0\n' > "$tmp_root/pending-progressive/.progressive/VERSION"
printf 'standalone\n' > "$tmp_root/pending-progressive/.progressive/PROFILE"
printf 'pending\n' > "$tmp_root/pending-progressive/.progressive/ADOPTION_STATE"
printf '# PCK router\n' > "$tmp_root/pending-progressive/AGENTS.md"
if HOME="$tmp_root/home" python3 "$repo_root/project.py" init --path "$tmp_root/pending-progressive" --adopt >/tmp/agents-devkits-pending-progressive.log 2>&1; then
  echo 'Expected pending PCK adoption to reject DevKits integration' >&2
  exit 1
fi
grep -q 'PCK adoption must be ready' /tmp/agents-devkits-pending-progressive.log
test ! -e "$tmp_root/pending-progressive/agents-devkits.yaml"

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

echo "==> inconsistent integration mode and provider are rejected"
cp "$repo_root/templates/project/agents-devkits.yaml" "$tmp_root/invalid-manifest.yaml"
python3 - "$tmp_root/invalid-manifest.yaml" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
path.write_text(path.read_text().replace('provider: agents-devkits', 'provider: progressive-context-kit'))
PY
if python3 "$repo_root/scripts/platform.py" manifest --manifest "$tmp_root/invalid-manifest.yaml" >/tmp/agents-devkits-project-invalid-integration.log 2>&1; then
  echo 'Expected inconsistent integration metadata to fail' >&2
  exit 1
fi
grep -q 'integration.provider must be agents-devkits' /tmp/agents-devkits-project-invalid-integration.log

echo "==> task facts reach the v0.2 specialist owners without over-triggering"
route_task() {
  python3 "$repo_root/project.py" route --task "$1"
}
route_skills() {
  route_task "$1" | python3 -c 'import json,sys; print(" ".join(json.load(sys.stdin)["skills"]))'
}
has_skill() {
  route_skills "$1" | tr ' ' '\n' | grep -qx "$2"
}
route_task "change the stored schema version and migrate old records" | grep -q '"data-migration"'
route_task "could these two async saves race with each other" | grep -q '"concurrency-review"'
route_task "add a trace id to every outbound request" | grep -q '"observability-review"'
route_task "what will break if I change this persisted identifier" | grep -q '"change-impact-analysis"'
route_task "audit how this app stores a growing history" | grep -q '"data-storage-review"'
route_task "will a restart leave this half written" | grep -q '"reliability-review"'
route_skills "review what personal data our analytics sdk collects" | grep -qw 'privacy-review'
route_skills "the tracking cookie stores an advertising id" | grep -qw 'privacy-review'
route_skills "let users opt out of telemetry" | grep -qw 'privacy-review'
route_skills "we depend on a third-party api with a strict rate limit and cursor pagination" | grep -qw 'api-integration-review'
if route_skills "add a trace id to every outbound request" | grep -qw 'privacy-review'; then
  echo 'A diagnostic identifier alone must not select the privacy owner' >&2
  exit 1
fi
for product_task in "add product analytics for the onboarding funnel" "set up issue tracking for the backlog"; do
  if route_skills "$product_task" | grep -qw 'privacy-review'; then
    echo 'A generic collection term without a personal-data subject must not select the privacy owner' >&2
    exit 1
  fi
done
if route_skills "audit how this app stores a growing history" | grep -qw 'api-integration-review'; then
  echo 'Local storage work must not select the external API owner' >&2
  exit 1
fi
has_skill "do an exploratory qa pass on the staging site" exploratory-qa-audit
has_skill "find bugs nobody has reported yet in the checkout flow" exploratory-qa-audit
has_skill "try to break the signup flow" exploratory-qa-audit
has_skill "run a bug bash on the staging build" exploratory-qa-audit
has_skill "there is a bug on the settings page, find the root cause" debugging
if has_skill "find bugs nobody has reported yet in the checkout flow" debugging; then
  echo 'Discovery of an unknown defect must not also select the root-cause owner' >&2
  exit 1
fi
for known_defect_task in "there is a bug on the settings page, find the root cause" "this page is broken after the last release"; do
  if has_skill "$known_defect_task" exploratory-qa-audit; then
    echo 'A reported defect must stay with debugging instead of the exploratory QA owner' >&2
    exit 1
  fi
done
has_skill "verify the checkout flow end-to-end in a real browser" playwright-testing
has_skill "does this page match the design" visual-qa
has_skill "check the visual regression on the pricing page" visual-qa
has_skill "the settings screen is confusing and hard to use" ux-usability-audit
has_skill "check keyboard navigation and screen reader labels" accessibility-review
has_skill "add unit tests for the browser utils parser" testing
if has_skill "verify the checkout flow end-to-end in a real browser" testing; then
  echo 'A browser flow must select the browser owner instead of the non-browser test owner' >&2
  exit 1
fi
if has_skill "add unit tests for the browser utils parser" playwright-testing; then
  echo 'The word "browser" alone must not select the browser owner' >&2
  exit 1
fi
if has_skill "check the visual regression on the pricing page" debugging; then
  echo 'A visual regression is a fidelity concern, not a reported defect' >&2
  exit 1
fi
has_skill "add structured logging to the worker" observability-review
for prefix_task in "the login page rejects valid users" "the logic here is wrong"; do
  if has_skill "$prefix_task" observability-review; then
    echo 'Whole-word matching must keep "login" and "logic" out of the observability fact' >&2
    exit 1
  fi
done

echo "==> every model-invocable owner is reachable from a task description"
covered_owners="$(mktemp)"
while IFS='|' read -r owner_task owner_skill; do
  [ -n "$owner_task" ] || continue
  if ! has_skill "$owner_task" "$owner_skill"; then
    echo "expected $owner_skill for: $owner_task" >&2
    exit 1
  fi
  echo "$owner_skill" >>"$covered_owners"
done <<'OWNERS'
there is a bug on the settings page, find the root cause|debugging
add regression coverage for the parser|testing
verify the checkout flow end-to-end in a real browser|playwright-testing
does this page match the design|visual-qa
check keyboard navigation and screen reader labels|accessibility-review
do an exploratory qa pass on the staging site|exploratory-qa-audit
audit how this app stores a growing history|data-storage-review
change the stored schema version and migrate old records|data-migration
could these two async saves race with each other|concurrency-review
will a restart leave this half written|reliability-review
add a trace id to every outbound request|observability-review
what will break if I change this persisted identifier|change-impact-analysis
review what personal data our analytics sdk collects|privacy-review
we depend on a third-party api with a strict rate limit and cursor pagination|api-integration-review
rotate the oauth secret for the payment provider|security-review
turn this notion page into an affine edgeless canvas|affine-notion-graph-sync
the requirements are vague, define the scope and acceptance criteria|product-spec
help me understand the codebase before I touch the importer|codebase-explorer
should we build a new feature for saved filters|feature-development
we need a customer journey map for the trial flow|journey-mapping
plan an information architecture for the settings sitemap|information-architecture
how should we structure the module boundaries for sync|solution-architecture
record the conventions in a knowledge pack|project-knowledge
plan the user research and an interview guide for onboarding|ux-research
run a usability audit on the dashboard|ux-usability-audit
set the visual direction and look and feel for the marketing page|frontend-design
this needs a stronger aesthetic and visual character|apply-aesthetic
reuse the existing design system and component library|design-system
extend the semantic design token scale for dark mode|design-tokens
run the token build with style dictionary|token-build
write the component spec with variants and states|design-component
implement the component in react|design-code
do a design review and critique the mockup|design-review
set up a design qa plan with ui evidence|design-qa
fix the responsive breakpoint on mobile layout|responsive-design
add a micro-interaction with easing to the menu|motion-design
polish the interface, it feels unfinished|apple-quality-interface-refinement
rewrite the microcopy and button label|ux-writing
sync figma variables with code connect|figma-integration
implement this screen from the figma file|figma-to-code
the dashboard is slow, check the bundle size|performance-review
code review this change before merge|code-review
are we ready to ship this release|release-check
OWNERS
python3 - "$repo_root" "$covered_owners" <<'CHECK'
import sys
from pathlib import Path

root, covered_path = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(root / "scripts"))
from platform import validate_skill_registry

registry = validate_skill_registry(
    root / "skills/registry.yaml", root, root / "capabilities/registry.yaml"
)
routable = {entry["name"] for entry in registry["skills"] if "model" in entry["invocation"]}
covered = set(covered_path.read_text().split())
missing = sorted(routable - covered)
if missing:
    print(
        "model-invocable owners no task description reaches: " + ", ".join(missing),
        file=sys.stderr,
    )
    raise SystemExit(1)
CHECK
rm -f "$covered_owners"

echo "==> adjacent owners stay separated by phrasing"
while IFS='|' read -r rival_task rival_skill; do
  [ -n "$rival_task" ] || continue
  if has_skill "$rival_task" "$rival_skill"; then
    echo "$rival_skill must not be selected for: $rival_task" >&2
    exit 1
  fi
done <<'RIVALS'
plan an information architecture for the settings sitemap|solution-architecture
plan the user research and an interview guide for onboarding|ux-usability-audit
sync figma variables with code connect|figma-to-code
add product analytics for the onboarding funnel|product-spec
what am i not thinking about as the product owner|product-spec
audit the technical health of this whole repository|codebase-explorer
this page is broken after the last release|release-check
RIVALS
if route_task "add a trace id to every outbound request" | grep -q '"concurrency-review"'; then
  echo 'Whole-word matching must keep "trace" out of the concurrency fact' >&2
  exit 1
fi
if route_task "fix a readme typo" | grep -q '"skills": \[[^]]'; then
  echo 'A documentation typo must not select a specialist skill' >&2
  exit 1
fi
for audit_task in "audit the technical health of this whole repository" "what am i not thinking about as the product owner"; do
  if route_task "$audit_task" | grep -qE '"(project-audit|interdisciplinary-project-audit)"'; then
    echo 'Project audits must require an explicit user request' >&2
    exit 1
  fi
done

echo "project runtime tests passed"
