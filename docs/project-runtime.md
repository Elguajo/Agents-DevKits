# Project Runtime

The project runtime is a thin, cross-platform layer over globally installed
Agents DevKits skills. It creates only project instructions and an optional
declarative manifest; it never copies skills, writes MCP credentials, or stores
execution history.

`project.py` is canonical. `project.sh` remains a Bash compatibility wrapper.

```bash
python3 project.py init --path ../my-project
python3 project.py init --path ../my-ui-project --ui
python3 project.py init --path ../my-progressive-project --mode auto --adopt
python3 project.py doctor --path ../my-project
python3 project.py verify --path ../my-project
```

`init` creates `AGENTS.md`, `CLAUDE.md`, `agents-devkits.yaml`, and a generated
`.agents-devkits/ROUTING.md` snapshot by default. It is a compact candidate and
level index, not a hand-maintained local routing table. Run `init --refresh-routing`
to deliberately replace an existing snapshot after updating Agents DevKits.
Existing instructions are left unchanged and receive an integration snippet in
`.agents-devkits/`; `--adopt` first creates a timestamped backup, then appends a
clearly delimited idempotent block. Canonical skills remain installed through
`./bootstrap.sh` under `~/.codex/skills` and `~/.claude/skills`.

The resolved integration mode is persisted in `agents-devkits.yaml`. A later
`init --mode auto` and `doctor` use that value instead of guessing again. The
canonical generated routing snapshot is part of the active integration
contract: a missing snapshot is `broken`, and a snapshot from another DevKits
version is `stale` until `init --refresh-routing` is run.

## Progressive Context Kit compatibility

`init --mode auto` detects a Progressive Context Kit Runtime by its canonical
`.progressive/VERSION` marker. The Runtime must have a supported version,
`PROFILE` set to `standalone` or `personal`, and `ADOPTION_STATE` set to
`ready`; a pending adoption is rejected before DevKits writes project files.
In progressive mode, Agents DevKits does not create or
replace `AGENTS.md`/`CLAUDE.md`: PCK remains authoritative for progressive
context loading, project memory, roadmap/phase state, and completion records.
The command still creates the DevKits manifest and routing snapshot. Without
`--adopt`, it writes `.agents-devkits/progressive-integration.md` for review.
With `--adopt`, it backs up PCK's `AGENTS.md` and places one idempotent bridge
after PCK's `<!-- PROJECT-SPECIFIC-INSTRUCTIONS -->` preservation sentinel.
This keeps the bridge inside the suffix retained by PCK `--update-framework`.
Older DevKits bridges that were appended outside that suffix are migrated on
the next adopted init.

If a PCK local skill has the same name as a globally installed DevKits skill,
the PCK skill wins. Use `--mode standard` to deliberately treat a directory as
a normal project even if it contains `.progressive/`.

For a UI-bearing product, `init --ui` uses the opt-in UI profile and creates a
concise `DESIGN.md` brief. The profile requires `visual-qa` and
`accessibility-review` whenever configured UI paths change. It intentionally
does not invent browser, contrast, token, or lint commands: declare only the
checks that the project's own toolchain can execute in the matching
`verification.conditions` entry. This keeps `verify` evidence honest while
making the final rendered and accessibility reviews explicit.

## Project knowledge packs

`project.py knowledge init` is an opt-in scaffold for a concise, durable
project-specific reference. It takes only project-relative source paths, creates
`.agents-devkits/knowledge/design-system.md`, and declares that pack in the
manifest. It does not inspect a source tree with a model, generate a global
skill, or claim facts have been verified.

```bash
python3 project.py knowledge init --path ../my-ui-project \
  --source packages/design-system --source apps/web
```

Use `project-knowledge` to fill or maintain the pack. Facts must point back to
the declared source paths and distinguish source code, generated output, and
consumer usage. `doctor` reports missing packs and source paths. Skills load a
relevant pack on demand; it is never an always-loaded replacement for project
instructions.

## Manifest v2

```yaml
schema: 1
platform:
  version: ">=1.0 <2.0"
integration:
  mode: standard
  provider: agents-devkits
agents:
  - codex
  - claude
skills:
  include:
    - codebase-explorer
    - feature-development
    - release-check
capabilities:
  required: [repository]
  preferred: [shell, browser]
  optional: []
knowledge:
  packs:
    - id: design-system
      kind: design-system
      path: .agents-devkits/knowledge/design-system.md
      sources: [packages/design-system, apps/web]
verification:
  baseline:
    - id: unit-tests
      kind: test
      command: npm
      args: ["test"]
  conditions:
    - when:
        paths: ["src/ui/**"]
      run:
        - id: browser-check
          kind: browser
          command: npm
          args: ["run", "test:e2e"]
      require_reviews: [visual-qa, accessibility-review]
```

The manifest is declarative: `init` and `doctor` never run its commands.
`verify` runs baseline checks plus only conditions matching explicit changed
paths, task-derived or explicit risks, and declared available capabilities. Commands are structured
(`command` plus literal `args`), run from the project directory, and cannot be
shell expressions or paths.

`doctor` validates the manifest, persisted mode, integration activation,
routing snapshot, platform-version range, installed skills, instruction files,
required capabilities, and command availability. It reports one integration
state: `active`, `pending`, `stale`, or `broken`, and succeeds only for
`active`. A generated snippet that has not been merged is deliberately
`pending`, not a successful installation. Capability
providers are never configured here. Repository and shell are detected locally;
other capabilities must be declared by `--capability <name>` or the
`AGENTS_DEVKITS_CAPABILITIES` environment variable.

```bash
python3 project.py verify --path ../my-project --changed src/ui/button.tsx --json
python3 project.py doctor --path ../my-project --capability browser
python3 project.py route --task "Fix OAuth callback" --fact task.feature
```

Manifests written in the earlier `schema_version: 1` shape remain readable for
validation and verification. New projects receive the version-compatible form
shown above.

## Routing, depth, and evidence

`skills/registry.yaml` is the canonical routing contract. It separates
`invocation` (`user` or `model`) from declarative `triggers` and declared
selection levels: `AUTO`, `PROPOSE`, and `ASK`. `project.py init` snapshots the
generated index inside the project so Codex and Claude Code can apply the same
short rules. `SKILL.md` remains the execution source of truth. Native Codex and
Claude Code discovery makes the final selection—this runtime is a diagnostic
helper, not an autonomous scheduler.

Workflow depth is `DIRECT`, `FOCUSED`, or `FULL`. `FULL` is selected for
security-sensitive, destructive, migration, public-contract, payment, or other
hard-to-reverse work. Depth changes coordination, not verification honesty.

Verification prints an ephemeral evidence envelope. Each entry has an id, kind,
status, and source; `passed`, `failed`, `unavailable`, `not_applicable`, and
`inferred` are distinct. `release-check` may use only actually executed or
authoritatively observed evidence and must not convert an unavailable check into
a pass.

Portable capability names and their fallback semantics are defined in
[`capabilities/registry.yaml`](../capabilities/registry.yaml). Codex and Claude
adapter notes live in [`adapters/`](../adapters/); neither duplicates skill
workflows or embeds provider credentials.
