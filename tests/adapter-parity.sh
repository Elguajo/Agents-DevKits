#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
cmp "$repo_root/adapters/codex/AGENTS.template.md" "$repo_root/templates/project/AGENTS.md.template"
cmp "$repo_root/adapters/claude/CLAUDE.template.md" "$repo_root/templates/project/CLAUDE.md.template"
for phrase in 'canonical `skills/registry.yaml`' 'generated `.agents-devkits/ROUTING.md` snapshot' '`PROPOSE`' 'declared references on demand' 'do not claim unavailable work'; do
  grep -Fq "$phrase" "$repo_root/adapters/codex/AGENTS.template.md"
  grep -Fq "$phrase" "$repo_root/adapters/claude/CLAUDE.template.md"
done
