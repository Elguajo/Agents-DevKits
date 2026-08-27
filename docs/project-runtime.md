# Project Runtime

The project runtime is a thin, cross-platform layer over globally installed
Agents DevKits skills. It creates only project instructions and an optional
declarative manifest; it never copies skills, writes MCP credentials, or stores
execution history.

`project.py` is canonical. `project.sh` remains a Bash compatibility wrapper.

```bash
python3 project.py init --path ../my-project
python3 project.py init --path ../my-ui-project --ui
python3 project.py doctor --path ../my-project
python3 project.py verify --path ../my-project
```

`init` creates `AGENTS.md`, `CLAUDE.md`, and `agents-devkits.yaml` by default.
Existing instructions are left unchanged and receive an integration snippet in
`.agents-devkits/`; `--adopt` first creates a timestamped backup, then appends a
clearly delimited idempotent block. Canonical skills remain installed through
`./bootstrap.sh` under `~/.codex/skills` and `~/.claude/skills`.

For a UI-bearing product, `init --ui` uses the opt-in UI profile and creates a
concise `DESIGN.md` brief. The profile requires `visual-qa` and
`accessibility-review` whenever configured UI paths change. It intentionally
does not invent browser, contrast, token, or lint commands: declare only the
checks that the project's own toolchain can execute in the matching
`verification.conditions` entry. This keeps `verify` evidence honest while
making the final rendered and accessibility reviews explicit.

## Manifest v2

```yaml
schema: 1
platform:
  version: ">=1.0 <2.0"
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

`doctor` validates the manifest, platform-version range, installed skills,
instruction files, required capabilities, and command availability. Capability
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
`invocation` (`user` or `model`) from declarative `triggers`; `SKILL.md` remains
the execution source of truth. Native Codex and Claude Code discovery makes the
final selection—this runtime is a diagnostic helper, not an autonomous
scheduler.

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
