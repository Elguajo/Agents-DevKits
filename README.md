<div align="center">

# Agents DevKits

**A portable AI development workflow system and opt-in macOS/Codex DevKits.**

[Русская версия](README.ru.md)

</div>


<div align="left">
  
## Contents

<p>
  <a href="#quick-start">Quick start</a><br>
  <a href="#project-runtime">Project runtime</a><br>
  <a href="#developer-machine-devkit">Developer-machine Devkit</a><br>
  <a href="#keep-skills-up-to-date">Update skills</a><br>
  <a href="docs/ai-development-workflow-system.md">Concept</a><br>
  <a href="docs/workflow-maintenance.md">Workflow maintenance</a><br>
  <a href="#workflow-map">Workflow map</a><br>
  <a href="#included-skills">Included skills</a><br>
  <a href="#repository-layout">Repository layout</a><br>
  <a href="docs/agent-architecture.md">Architecture reference</a><br>
  <a href="#safety-and-provenance">Safety & provenance</a>
</p>

</div>

---

## What this project is

Its architectural direction is an **AI Development Workflow System**: we are not primarily building the agents themselves; we are building the system through which AI agents develop software.

That means coordinating:

```text
project intent
    ↓
skill discovery / routing
    ↓
specialist workflows
    ↓
tools and integrations
    ↓
implementation
    ↓
verification and review
    ↓
release evidence
    ↓
SHIP
```

Skills are therefore one layer of the system, not the whole system.

The goal is to make AI-assisted software development more deliberate, reusable, inspectable, conflict-aware, and production-ready without forcing unnecessary process onto simple tasks.

Read the full concept and development roadmap in [`docs/ai-development-workflow-system.md`](docs/ai-development-workflow-system.md).

## Why this repository exists

Useful AI development workflows should be reusable, reviewable, portable, and clearly bounded—not buried inside a chat or copied by hand between computers.

This repository is the single source of truth for the current workflow system and its portable developer-machine layer: skills, routing metadata, responsibility boundaries, provenance, installation logic, safe Codex baseline, and documentation.

Each skill follows the [Agent Skills](https://agentskills.io/) format: a folder with a `SKILL.md`, plus optional scripts, references, and assets. This repository currently ships installation support for Codex Desktop and Claude Code; another agent can reuse the format only when it supports compatible skill discovery.

The system is deliberately **conflict-aware**. Each specialist owns one primary concern and hands work off instead of competing with neighboring skills. See [`docs/skill-boundaries.md`](docs/skill-boundaries.md).

For a broader explanation of skills, agents, tools, MCP, subagents, hooks, permissions, memory, plugins, and automations, see [`docs/agent-architecture.md`](docs/agent-architecture.md).

## Quick start

Run one command from its root:

```bash
git clone https://github.com/Elguajo/Agents-DevKits.git
cd Agents-DevKits
./bootstrap.sh
```

Keep this clone in a permanent location after installation. The installer creates absolute symbolic links to it, so moving or deleting the repository will break the installed skills.

On Windows, run the commands from Git Bash. Creating symbolic links may also require enabling Developer Mode or using an elevated shell.

`bootstrap.sh` validates that skills are present, then links each one into both local agents:

| Agent | Local skill location |
|---|---|
| Codex Desktop | `~/.codex/skills/<skill-name>` |
| Claude Code | `~/.claude/skills/<skill-name>` |

Existing skills are never overwritten. To deliberately replace an existing local copy, use:

```bash
./bootstrap.sh --adopt
```

The prior copy is moved to `~/.agent-skills-backups/`; nothing is deleted. The installer also removes only broken symlinks that were previously managed by this repository, so repository-managed skill renames do not touch unrelated local skills.

Restart Codex or Claude Code if either was already running when new skills were installed.

### Ask an AI agent to set it up

After cloning the repository, paste one of these prompts into Codex or Claude
Code.

**Skills only — safe default**

~~~text
Install only the Agents DevKits skills from this repository. Run ./bootstrap.sh
from the repository root. Do not use --adopt: preserve every existing local
skill, then report which skills were linked or skipped.
~~~

**Full macOS/Codex machine template**

~~~text
Set up this macOS machine with the Agents DevKits template. First run
./devkit.sh doctor, then run ./devkit.sh bootstrap --profile base --profile web
--profile ai. Preserve the current Codex configuration through the Devkit
adoption flow, enable no MCP profiles unless I name them, and report every
system-level change.
~~~

The full template installs Homebrew packages and may change global Git, shell,
and macOS preferences. Read the prompted actions before accepting them.

## Developer-machine Devkit

The optional devkit/ layer prepares a macOS workstation and manages a
host-local Codex configuration. It is separate from the skill installer: use
only the part you need.

On a new Mac:

~~~bash
./devkit.sh bootstrap --profile base --profile web --profile ai
~~~

On an existing Mac, adopt the active Codex config before installing Devkit:

~~~bash
./devkit.sh backup
./devkit.sh install
~~~

install refuses to overwrite an existing Codex config without an ignored
host-local override. MCP profiles are explicit opt-ins:

~~~bash
./devkit.sh mcp list
./devkit.sh mcp enable playwright context7
./devkit.sh mcp doctor
~~~

See [devkit/README.md](devkit/README.md) for all Devkit commands, profiles,
privacy boundaries, and portable exports.

### Start using skills

After restarting the agent, describe the task normally or name a skill explicitly when you want a particular workflow. For example:

```text
Use product-spec to turn this feature idea into acceptance criteria.
Use feature-development to implement this feature through the relevant specialists.
```

Use [`SKILLS.md`](SKILLS.md) to choose an explicit skill, or let an agent with skill routing select one from the task. Each installed `SKILL.md` contains the authoritative execution instructions.

### Verify or reverse an installation

The installer creates links for **both** Codex Desktop and Claude Code, even if only one is currently installed. Confirm an individual link and its target with:

```bash
readlink "$HOME/.codex/skills/product-spec"
readlink "$HOME/.claude/skills/product-spec"
```

To stop managing one skill, remove only its symlink with `unlink "$HOME/.codex/skills/<skill-name>"` or `unlink "$HOME/.claude/skills/<skill-name>"`. If it was replaced with `--adopt`, restore the original folder from the timestamped path under `~/.agent-skills-backups/` after first removing that skill's symlink. The installer never deletes the adopted folder.

### Keep skills up to date

Refresh local links after changing the repository locally:

```bash
./bootstrap.sh
```

Pull and install the latest library version:

```bash
git pull --ff-only
./bootstrap.sh
```

After a repository-managed skill is renamed, the same command removes its stale broken managed link and creates the new one.

## Project runtime

The optional project runtime declares which globally installed skills, agent
targets, portable capabilities, and repository-owned verification commands
apply to one project. It is a thin copied template layer: it does not copy
skills into `.agents/skills` or `.claude/skills`, create project symlinks, or
store execution history.

From this library checkout, initialize an existing project directory:

```bash
python3 project.py init --path ../my-project
python3 project.py doctor --path ../my-project
```

For a project with a material UI surface, initialize the opt-in UI profile:

```bash
python3 project.py init --path ../my-ui-project --ui
```

It creates a short `DESIGN.md` brief, includes UI review specialists, and
requires visual and accessibility review when configured UI paths change. Add
only project-supported objective commands (for example `axe`, token/hardcode
lint, responsive browser checks, or a build) to its manifest; the runtime does
not pretend a generic command can validate every framework.

The default creates both Codex `AGENTS.md` and Claude Code `CLAUDE.md`, plus a
versioned `agents-devkits.yaml`. Existing instruction files are preserved and
receive an integration snippet; `--adopt` creates a timestamped backup before
adding a managed block. Until that snippet is adopted, `doctor` reports the
integration as `pending`; it succeeds only for an active integration with a
current routing snapshot. Checks run only when explicitly requested:

```bash
python3 project.py verify --path ../my-project
python3 project.py verify --path ../my-project --changed src/ui/button.tsx --json
```

`project.sh` remains a compatibility wrapper. Run the platform's own complete
validation with `python3 scripts/gate.py`.

See [`docs/project-runtime.md`](docs/project-runtime.md) for the manifest
schema, safety constraints, and full command reference.

## Workflow map

This is the current software-development workflow model. **It is not a requirement to run every skill for every task.** `feature-development` acts as an orchestrator and should select only the specialists justified by the change.

```text
                                  PRODUCT
                                     │
                                     ▼
                             ┌──────────────┐
                             │ product-spec │
                             └──────┬───────┘
                                    │
                                    ▼
                           codebase-explorer
                                    │
                                    ▼
                         solution-architecture
                                    │
                                    ▼
                         feature-development
                           (orchestration)
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
                FRONTEND                         BACKEND
                    │                               │
         ┌──────────┼──────────┐                    │
         │          │          │                    │
         ▼          ▼          ▼                    │
  frontend-design   │      figma-to-code            │
                    │                               │
             design-system                          │
                    │                               │
            responsive-design                       │
                    │                               │
              motion-design                         │
                    │                               │
                    └───────────────┬───────────────┘
                                    │
                                    ▼
                             IMPLEMENTATION
                                    │
                         debugging / refactor
                                    │
                                    ▼
                                  TEST
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                      testing        playwright-testing
                                               │
                                               ▼
                                           visual-qa
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                    ▼               ▼                ▼
          accessibility-review  performance-review  code-review
                                                     │
                                                     ▼
                                               security-review
                                                     │
                                                     ▼
                                                release-check
                                                     │
                                                     ▼
                                                    SHIP
```

A more accurate way to read the map is:

- **Definition:** what should exist?
- **Understanding:** how does the current system work?
- **Architecture:** how should the change fit?
- **Implementation specialists:** which discipline-specific workflows apply?
- **Verification:** does it work and look right?
- **Review:** is it maintainable, secure, accessible, and performant where relevant?
- **Release gate:** is there enough evidence to ship?
- **Conditional specialists:** the map shows the common path only. `change-impact-analysis`, `data-storage-review`, `data-migration`, `concurrency-review`, `reliability-review`, and `observability-review` join it only when the task shows their trigger, and the two project audits run only on an explicit request.

The long-term direction adds intelligent routing, tool-aware execution, evidence-aware completion, and reusable project bootstrapping. See the [AI Development Workflow System roadmap](docs/ai-development-workflow-system.md#development-direction).

## Included skills

The library now has 47 skills: the original engineering workflow set plus a portable UX/UI extension for visual direction, tokens, components, UI implementation, design QA/review, Figma parity, migrations, prototyping, redesign, token builds, and UX writing. `project-knowledge` adds an opt-in, source-grounded project reference without turning local facts into a global skill. `ux-research`, `information-architecture`, and `journey-mapping` are local adaptations of publicly documented methods, with source notes and no vendored framework catalogues. The extension is adapted from `plugin87/ux-ui-agent-skills` under its declared MIT license; it does not bundle upstream assets, brand libraries, scripts, or provider configuration.

Use [`SKILLS.md`](SKILLS.md) to choose a skill: it is the complete human-readable catalog, including ownership, trigger conditions, provenance, and handoffs. Use the generated [`docs/ROUTING.md`](docs/ROUTING.md) for a compact `AUTO` / `PROPOSE` / `ASK` selection index, and [`skills/registry.yaml`](skills/registry.yaml) for authoritative machine-readable routing metadata. Each `skills/<skill>/SKILL.md` is authoritative for execution instructions.

For a ready [Progressive Context Kit](https://github.com/Elguajo/Progressive-Context-Kit) Runtime, run `project.py init --mode auto --adopt`. Detection uses `.progressive/VERSION`; the bridge is placed in PCK's framework-update-preserved suffix, while PCK keeps ownership of `.progressive/` project memory and context routing. DevKits supplies only on-demand specialist skills and its routing snapshot. See [`docs/project-runtime.md`](docs/project-runtime.md#progressive-context-kit-compatibility).

The v0.2 skills migration adds eight `experimental` owners for concerns that previously had no owner: `change-impact-analysis`, `data-storage-review`, `data-migration`, `concurrency-review`, `reliability-review`, `observability-review`, `project-audit`, and `interdisciplinary-project-audit`. The remaining imported workflows became progressive `references/` under the existing owners instead of new top-level skills, so routing keeps one primary owner per concern. Experimental skills route at `PROPOSE` or `ASK` until real use supports promotion.

All listed skills are intended for Codex and Claude Code unless a skill explicitly documents an agent-specific dependency.

## How the skills avoid conflicts

The key rule is **one primary owner per concern**.

- `codebase-explorer` explains **how the repository works now**; `solution-architecture` decides **how it should change**.
- `project-knowledge` preserves recurring, source-grounded project facts; `codebase-explorer` investigates the smallest area needed for the current task.
- `product-spec` owns product intent and acceptance criteria; `solution-architecture` owns technical structure.
- `ux-research` reduces uncertainty with sourced evidence; `information-architecture` owns navigation and structural flows; `journey-mapping` aligns cross-touchpoint experience without claiming research occurred.
- `frontend-design` owns broad visual concept; `apply-aesthetic` translates an approved direction into reusable UI-system choices; `design-system` owns consistency with the existing system.
- `design-component` owns the reusable component contract; `design-code` owns framework implementation; `design-qa` aggregates evidence while `visual-qa` and `accessibility-review` retain their specialist reviews.
- A supplied Figma/reference overrides aesthetic reinterpretation; `figma-to-code` follows the source of truth.
- `responsive-design` defines responsive behavior; `visual-qa` checks the rendered result.
- `testing` owns unit/integration regression coverage; `playwright-testing` owns browser E2E behavior.
- `debugging` changes behavior to correct a defect; `refactor` preserves behavior.
- `code-review` owns general change quality; `security-review` owns threat-focused analysis.
- `release-check` verifies evidence; it does not redo architecture, design, or implementation.

Full precedence and collision rules: [`docs/skill-boundaries.md`](docs/skill-boundaries.md).

## How it works

```text
Agents-DevKits/skills/<skill>/SKILL.md
                 │
                 ├── ~/.codex/skills/<skill>   → Codex
                 └── ~/.claude/skills/<skill>  → Claude Code
```

The installer creates absolute symbolic links, so an update committed to this repository becomes the canonical local version for both agents after the repository is updated locally.

Do not move or delete the clone while you want to use its installed skills. If you need to relocate it, remove the existing skill symlinks first, then run `./bootstrap.sh` from the new location.

## Use and adopt skills

| Situation | Command | Result |
|---|---|---|
| New computer or no conflicting local skill | `./bootstrap.sh` | Adds missing links and leaves every existing unrelated local skill untouched. |
| An existing local skill should be managed by this repository | `./bootstrap.sh --adopt` | Moves the existing folder to a timestamped backup, then replaces it with a link to this repository. |

Use `--adopt` only when the repository version is the one you want both agents to use. Previous local folders remain recoverable at `~/.agent-skills-backups/`.

Skills can be selected naturally from the request or invoked explicitly when several skills could fit. Project instructions and explicit user requirements always outrank generic skill guidance.

The installer prints an exact summary of newly linked, already linked, skipped, backed-up, and stale links removed skills. A skipped skill is left untouched; use `--adopt` only when you intend to replace it.

## Add a skill

Create an instruction-only skill by default. Add scripts only when they remove repeated, error-prone work.

```text
skills/
└── my-skill/
    └── SKILL.md
```

Before committing a new skill, verify that:

1. The `description` names clear user-facing trigger conditions.
2. Its responsibility does not duplicate an existing skill.
3. `Use when` / `Do not use when` / handoff rules are explicit when overlap is possible.
4. The workflow works in both agents or explicitly documents why it is agent-specific.
5. Bundled scripts are dependency-light, reviewable, and tested.
6. Imported skills retain their original license and provenance.
7. The new skill is added to both [`SKILLS.md`](SKILLS.md) and [`skills/registry.yaml`](skills/registry.yaml).

Then install it locally:

```bash
./bootstrap.sh
```

## Safety and provenance

- `bootstrap.sh` creates links and removes only stale broken symlinks previously managed by this repository. It does not install packages, change global Git settings, or execute a skill's bundled scripts.
- Git does not run the installer automatically during `clone`; installation is a deliberate local action.
- Review third-party instructions and scripts before adding them. Keep provider API keys, tokens, and private context out of this repository.
- Imported and adapted skills carry `SOURCE.md` provenance. The UX/UI extension's pinned upstream revision and MIT declaration are recorded in [`third_party/plugin87-ux-ui-agent-skills/`](third_party/plugin87-ux-ui-agent-skills/); no upstream provider configuration or credentials are copied.

## Repository layout

Treat this section as the **navigation map for both humans and agents**. The file tree shows where information lives; the table below explains which source to use for which question.

```text
Agents-DevKits/
├── README.md                         # Entry point: identity, setup, workflow, repository map
├── SKILLS.md                         # Human catalog + field notes for every skill
├── bootstrap.sh                      # One-command installer entry point
├── project.sh                        # Thin project manifest and adapter templates
├── project.py                        # Cross-platform project runtime
├── devkit.sh                         # Devkit command entry point
├── VERSION                           # Platform compatibility version
│
├── adapters/                         # Thin Codex/Claude adapter templates and notes
├── capabilities/registry.yaml        # Portable capability vocabulary and fallbacks
├── contracts/evidence.yaml            # Ephemeral evidence vocabulary
├── evals/scenarios.yaml               # Routing contract scenarios
├── docs/
│   ├── ai-development-workflow-system.md # Concept, principles and development roadmap
│   ├── agent-architecture.md         # How skills, agents, tools, MCP, hooks, etc. relate
│   ├── project-runtime.md            # Project manifest, adapters and verification commands
│   ├── workflow-maintenance.md        # External research and recurring-failure improvement loop
│   └── skill-boundaries.md           # Precedence, collisions and handoff rules
│
├── scripts/
│   ├── install.sh                    # Safe Codex/Claude symlink installation logic
│   ├── gate.py                       # One-command platform gate
│   ├── platform.py                   # Registry, manifest, routing and evidence contracts
│   ├── project_manifest.py           # Strict manifest and registry validator
│   └── test.sh                       # Portable library validation entry point
│
├── templates/project/                # Codex/Claude instructions and manifest template
├── tests/project-runtime.sh          # Project runtime fixtures
│
├── devkit/                           # macOS/Codex environment layer
│   ├── config/                       # portable Codex baseline and MCP profiles
│   ├── mcp/                          # opt-in MCP manager and doctor
│   ├── profiles/                     # Homebrew and local setup profiles
│   ├── machines/                     # ignored host-specific overrides
│   └── SOURCE.md                     # provenance of the public Devkit port
│
└── skills/
    ├── registry.yaml                 # Machine-readable catalog for AI/tools/routing
    │
    └── <skill>/
        └── SKILL.md                # Authoritative execution instructions
```

### Knowledge map

| Question | Canonical source | What it contains |
|---|---|---|
| **What is the project and where is it going?** | [`docs/ai-development-workflow-system.md`](docs/ai-development-workflow-system.md) | The AI Development Workflow System concept, principles, system layers, and roadmap. |
| **How do I install and use it?** | [`README.md`](README.md) | Setup, installation lifecycle, current workflow map, operating model, and navigation. |
| **How do I prepare or restore a developer machine?** | [`devkit/README.md`](devkit/README.md) | macOS profiles, safe Codex-config adoption, opt-in MCP profiles, diagnostics, and exports. |
| **Which skill should I use and what can I reuse from it?** | [`SKILLS.md`](SKILLS.md) | Human-readable catalog, field notes, origin, useful parts, tooling, pairings, and boundaries. |
| **How should an AI quickly shortlist skills?** | [`docs/ROUTING.md`](docs/ROUTING.md) | Generated compact candidate index with `AUTO`, `PROPOSE`, and `ASK` levels. |
| **How should an AI discover or route to skills?** | [`skills/registry.yaml`](skills/registry.yaml) | Validated metadata: invocation, levels, declarative triggers, inputs/outputs, capabilities, references, verification, relations, and handoffs. |
| **Which portable capability or fallback applies?** | [`capabilities/registry.yaml`](capabilities/registry.yaml) | Provider-neutral capability vocabulary and required/preferred/optional fallback semantics. |
| **How exactly should a skill perform its job?** | `skills/<skill>/SKILL.md` | Authoritative execution instructions for that skill. |
| **How do I add Agents DevKits to one project?** | [`docs/project-runtime.md`](docs/project-runtime.md) | Thin Codex/Claude adapters, `agents-devkits.yaml`, installation checks, and explicit verification. |
| **Where did a vendored skill come from?** | `skills/<skill>/SOURCE.md` | Upstream repository, path, revision, retrieval date, and local modifications when applicable. |
| **What wins if two skills or sources disagree?** | [`docs/skill-boundaries.md`](docs/skill-boundaries.md) | Precedence, collision rules, and responsibility handoffs. |
| **How do skills relate to agents, tools, MCP, hooks, and plugins?** | [`docs/agent-architecture.md`](docs/agent-architecture.md) | Conceptual architecture of the wider agent ecosystem. |

The intended reading path is:

```text
README.md / Repository layout
            │
            ├── Understand the system ───────────→ ai-development-workflow-system.md
            │
            ├── Human choosing a skill ──────────→ SKILLS.md
            │                                      │
            │                                      ▼
            │                                 SKILL.md
            │
            ├── AI choosing a skill ─────────────→ ROUTING.md → registry.yaml
            │                                      │
            │                                      ▼
            │                                 SKILL.md
            │
            └── Conflict / provenance ────────────→ skill-boundaries.md / SOURCE.md
```

`SKILL.md` is authoritative for **execution**. Generated `docs/ROUTING.md` is the compact selection index; `skills/registry.yaml` is the validated routing contract for **invocation, levels, declarative triggers, capability requirements, references, relationships, and handoffs**. `SKILLS.md` is the human catalog. `capabilities/registry.yaml` is the sole portable capability vocabulary. A project's `agents-devkits.yaml` declares selected skills and project-owned verification; it does not replace project instructions. The concept document is authoritative for the **direction of the system**. Project instructions and the explicit user request still outrank generic skill guidance.

## License

Original material in this repository is licensed under the [MIT License](LICENSE). Imported skills retain their own licenses and attribution; in particular, [`frontend-design`](skills/frontend-design/) is licensed under Apache-2.0. Where terms differ, the imported skill's license governs that skill.
