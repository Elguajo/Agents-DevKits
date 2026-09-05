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

The library now has 50 skills: the original engineering workflow set plus a portable UX/UI extension for visual direction, tokens, components, UI implementation, design QA/review, Figma parity, migrations, prototyping, redesign, token builds, and UX writing. `project-knowledge` adds an opt-in, source-grounded project reference without turning local facts into a global skill. `affine-notion-graph-sync` turns a Notion page URL into a verified Edgeless Canvas in self-hosted AFFiNE while preserving existing state. `ux-research`, `information-architecture`, and `journey-mapping` are local adaptations of publicly documented methods, with source notes and no vendored framework catalogues. `ux-usability-audit` is an experimental owner for human-centered usability and interaction logic of a product that was actually exercised. `apple-quality-interface-refinement` is an experimental owner for the preservation-first craft pass on an interface whose direction already exists. The extension is adapted from `plugin87/ux-ui-agent-skills` under its declared MIT license; it does not bundle upstream assets, brand libraries, scripts, or provider configuration.

Use [`SKILLS.md`](SKILLS.md) to choose a skill: it is the complete human-readable catalog, including ownership, trigger conditions, provenance, and handoffs. Use the generated [`docs/ROUTING.md`](docs/ROUTING.md) for a compact `AUTO` / `PROPOSE` / `ASK` selection index, and [`skills/registry.yaml`](skills/registry.yaml) for authoritative machine-readable routing metadata. Each `skills/<skill>/SKILL.md` is authoritative for execution instructions.

For a ready [Progressive Context Kit](https://github.com/Elguajo/Progressive-Context-Kit) Runtime, run `project.py init --mode auto --adopt`. Detection uses `.progressive/VERSION`; the bridge is placed in PCK's framework-update-preserved suffix, while PCK keeps ownership of `.progressive/` project memory and context routing. DevKits supplies only on-demand specialist skills and its routing snapshot. See [`docs/project-runtime.md`](docs/project-runtime.md#progressive-context-kit-compatibility).

The v0.2 skills migration adds eight `experimental` owners for concerns that previously had no owner: `change-impact-analysis`, `data-storage-review`, `data-migration`, `concurrency-review`, `reliability-review`, `observability-review`, `project-audit`, and `interdisciplinary-project-audit`. The remaining imported workflows became progressive `references/` under the existing owners instead of new top-level skills, so routing keeps one primary owner per concern. Experimental skills route at `PROPOSE` or `ASK` until real use supports promotion.

All listed skills are intended for Codex and Claude Code unless a skill explicitly documents an agent-specific dependency.

### Skill map

Same idea as the [knowledge map](#knowledge-map) below, but for picking a skill by situation instead of a doc. The `Use it when` column mirrors the `use_when` field in [`skills/registry.yaml`](skills/registry.yaml), grouped by the same domains as [`SKILLS.md`](SKILLS.md); if the two ever disagree, the registry and the skill's own `SKILL.md` win.

#### Top 10 skills to start with

This is a practical quick-start shortlist, not a universal quality ranking. These skills cover the most common path from an unclear request to a verified change; choose the specialist from the full map whenever its trigger is a closer fit.

| # | Skill | Best first use |
|---:|---|---|
| 1 | [`codebase-explorer`](skills/codebase-explorer/SKILL.md) | Understand an existing repository before changing it. |
| 2 | [`product-spec`](skills/product-spec/SKILL.md) | Turn an ambiguous request into scope and acceptance criteria. |
| 3 | [`solution-architecture`](skills/solution-architecture/SKILL.md) | Decide how a cross-cutting change fits the system. |
| 4 | [`feature-development`](skills/feature-development/SKILL.md) | Coordinate a non-trivial feature from definition through verification. |
| 5 | [`debugging`](skills/debugging/SKILL.md) | Find and fix the root cause of incorrect behavior. |
| 6 | [`testing`](skills/testing/SKILL.md) | Add focused automated coverage for meaningful behavior. |
| 7 | `qa` (gstack) | Test the latest web changes in a browser, fix discovered defects, and verify the fixes. |
| 8 | [`security-review`](skills/security-review/SKILL.md) | Review trust boundaries, sensitive data, and untrusted input. |
| 9 | [`accessibility-review`](skills/accessibility-review/SKILL.md) | Check interactive UI for inclusive, keyboard-friendly behavior. |
| 10 | [`release-check`](skills/release-check/SKILL.md) | Decide whether the available evidence supports shipping. |

`qa` is provided separately by gstack, rather than by this repository's 48-skill library. It is the appropriate choice when a feature branch needs browser-based QA with an iterative test → fix → verify loop; use `qa-only` when fixes must not be made.

| Domain | Skill | Use it when |
|---|---|---|
| Product & architecture | [`product-spec`](skills/product-spec/SKILL.md) | requirements are ambiguous, broad, or incomplete |
| Product & architecture | [`ux-research`](skills/ux-research/SKILL.md) | user needs to reduce product or UX uncertainty with research, usability evidence, or a defensible research plan |
| Product & architecture | [`information-architecture`](skills/information-architecture/SKILL.md) | product or site structure must be defined or revised before detailed UI implementation |
| Product & architecture | [`journey-mapping`](skills/journey-mapping/SKILL.md) | a persona journey, service delivery flow, empathy map, or user story map must inform prioritization or structural decisions |
| Product & architecture | [`codebase-explorer`](skills/codebase-explorer/SKILL.md) | an existing repository must be understood before changing or debugging it |
| Product & architecture | [`project-knowledge`](skills/project-knowledge/SKILL.md) | recurring project facts should be recorded in a source-grounded pack without creating a new generic skill |
| Product & architecture | [`solution-architecture`](skills/solution-architecture/SKILL.md) | a change crosses modules, data flows, integrations, persistence, or architectural boundaries |
| Product & architecture | [`feature-development`](skills/feature-development/SKILL.md) | a feature benefits from definition, exploration, architecture, implementation, verification, and review |
| Product & architecture | [`change-impact-analysis`](skills/change-impact-analysis/SKILL.md) | a shared API, schema, persisted identifier, event contract, or core component is about to change and its consumers are unclear |
| Product & architecture | [`affine-notion-graph-sync`](skills/affine-notion-graph-sync/SKILL.md) | the user provides a Notion page link and asks for an AFFiNE graph, canvas, mind map, flow, or block diagram |
| Data | [`data-storage-review`](skills/data-storage-review/SKILL.md) | durable application data needs review of source of truth, growth, retention, integrity, or recovery |
| Data | [`data-migration`](skills/data-migration/SKILL.md) | a persisted schema, format, identifier, preference, or sync contract changes and existing data must survive |
| Frontend & design | [`frontend-design`](skills/frontend-design/SKILL.md) | visual direction must be invented or significantly shaped |
| Frontend & design | [`apply-aesthetic`](skills/apply-aesthetic/SKILL.md) | visual direction is unresolved |
| Frontend & design | [`brandkit`](skills/brandkit/SKILL.md) | a new product needs an accessible visual foundation |
| Frontend & design | [`design-tokens`](skills/design-tokens/SKILL.md) | token roles or themes must change |
| Frontend & design | [`design-component`](skills/design-component/SKILL.md) | a reusable UI element needs a complete contract |
| Frontend & design | [`design-code`](skills/design-code/SKILL.md) | approved UI intent needs framework code |
| Frontend & design | [`design-qa`](skills/design-qa/SKILL.md) | UI evidence must be planned or consolidated |
| Frontend & design | [`design-review`](skills/design-review/SKILL.md) | independent UI-quality critique is needed |
| Frontend & design | [`figma-integration`](skills/figma-integration/SKILL.md) | Figma/code tokens or variants must stay aligned |
| Frontend & design | [`governance`](skills/governance/SKILL.md) | design-system compatibility or deprecation is at stake |
| Frontend & design | [`image-to-code`](skills/image-to-code/SKILL.md) | a screenshot or mockup is the visual source |
| Frontend & design | [`migrate-design-system`](skills/migrate-design-system/SKILL.md) | systems need a semantic crosswalk and rollout |
| Frontend & design | [`prototype`](skills/prototype/SKILL.md) | a product question should be tested before build |
| Frontend & design | [`redesign`](skills/redesign/SKILL.md) | a working UI needs an audit-first improvement |
| Frontend & design | [`token-build`](skills/token-build/SKILL.md) | token source must produce platform artifacts |
| Frontend & design | [`ux-writing`](skills/ux-writing/SKILL.md) | UI copy needs creation or review |
| Frontend & design | [`design-system`](skills/design-system/SKILL.md) | the repository already has a design system, DESIGN.md, theme tokens, or established UI patterns |
| Frontend & design | [`figma-to-code`](skills/figma-to-code/SKILL.md) | Figma frames, nodes, screenshots, or approved references are the source of truth |
| Frontend & design | [`responsive-design`](skills/responsive-design/SKILL.md) | a UI must adapt across viewport sizes or input modes |
| Frontend & design | [`motion-design`](skills/motion-design/SKILL.md) | motion materially improves interaction or visual communication |
| Frontend & design | [`apple-quality-interface-refinement`](skills/apple-quality-interface-refinement/SKILL.md) | an existing interface keeps its direction but needs a craft, state, and coherence pass |
| Implementation quality | [`debugging`](skills/debugging/SKILL.md) | observed behavior is wrong and the root cause is unknown |
| Implementation quality | [`refactor`](skills/refactor/SKILL.md) | behavior is correct but implementation is unnecessarily complex, duplicated, or difficult to maintain |
| Implementation quality | [`concurrency-review`](skills/concurrency-review/SKILL.md) | async tasks, threads, actors, queues, jobs, event handlers, or shared mutable state create ordering or duplication risk |
| Testing & QA | [`testing`](skills/testing/SKILL.md) | meaningful behavior needs automated non-browser coverage |
| Testing & QA | [`playwright-testing`](skills/playwright-testing/SKILL.md) | navigation, forms, browser state, network interactions, or end-to-end flows must be verified |
| Testing & QA | [`visual-qa`](skills/visual-qa/SKILL.md) | rendered UI must match Figma, screenshots, DESIGN.md, or approved visual intent |
| Testing & QA | [`accessibility-review`](skills/accessibility-review/SKILL.md) | interactive UI needs semantic, keyboard, focus, labels, contrast, touch target, screen-reader, or reduced-motion review |
| Testing & QA | [`ux-usability-audit`](skills/ux-usability-audit/SKILL.md) | a real website or application must be reviewed or improved as a human user would experience it, beyond visual fidelity and functional correctness |
| Testing & QA | [`performance-review`](skills/performance-review/SKILL.md) | performance is a stated concern or measurements indicate a bottleneck |
| Review & release | [`code-review`](skills/code-review/SKILL.md) | a completed change needs independent engineering review |
| Review & release | [`security-review`](skills/security-review/SKILL.md) | a change touches auth, authorization, secrets, untrusted input, uploads, permissions, sensitive APIs, or other security-relevant surfaces |
| Review & release | [`release-check`](skills/release-check/SKILL.md) | implementation and focused reviews are complete and a change may be ready to merge, deploy, or release |
| Review & release | [`reliability-review`](skills/reliability-review/SKILL.md) | a networked, persistent, transactional, background, or multi-step workflow must survive timeouts, restarts, duplicates, or partial failure |
| Review & release | [`observability-review`](skills/observability-review/SKILL.md) | important failures, background jobs, integrations, or async workflows are hard to reproduce or explain |
| Project audits | [`project-audit`](skills/project-audit/SKILL.md) | the user explicitly asks for project-wide engineering risks, debt, or rework exposure rather than one change or one defect |
| Project audits | [`interdisciplinary-project-audit`](skills/interdisciplinary-project-audit/SKILL.md) | the user explicitly asks what they may not realize they should be asking before continuing development |
| Utility | [`credit-codex-contributor`](skills/credit-codex-contributor/SKILL.md) | the user explicitly requests Codex contributor attribution |

For ownership, origin, and pairing notes, see [`SKILLS.md`](SKILLS.md). For the compact `AUTO` / `PROPOSE` / `ASK` selection index agents use, see [`docs/ROUTING.md`](docs/ROUTING.md).

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
- `apple-quality-interface-refinement` preserves the existing visual direction and raises execution quality inside it; `redesign` owns rework that is allowed to change that direction, `frontend-design` owns new art direction, and `visual-qa` owns the final visual evidence.
- `ux-usability-audit` owns whether an exercised interface is understandable and usable; `design-review` owns expert critique of UI quality, `information-architecture` owns the structural model, and `redesign` owns broad rework.
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
