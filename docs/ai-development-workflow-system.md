# AI Development Workflow System

This document defines the architectural direction of **Agents DevKits**.

## Naming

- **Project name:** Agents DevKits
- **Concept / architecture:** AI Development Workflow System
- **Repository slug:** `Agents-DevKits`

The distinction is intentional.

We are **not primarily building agents themselves**. We are building a system through which AI agents develop software: they understand the task, choose the right workflows, use project context and tools, implement changes, verify the result, review risk, and decide whether the work is ready to ship.

In short:

```text
Agents DevKits
        = project / product name

AI Development Workflow System
        = architectural concept
        = how AI agents develop software through the system
```

## Core idea

A collection of skills answers:

> What reusable instructions are available?

An AI Development Workflow System answers a larger set of questions:

> What should happen next?
> Which specialist workflow owns this concern?
> Which source of truth wins?
> Which tools are required?
> How should work be handed off?
> What evidence is required before completion?

The system therefore coordinates more than skills. Skills are one execution layer inside a broader development workflow.

The optional developer-machine layer is a separate execution boundary. It
installs tools and local Codex configuration only after an explicit command; it
does not change the portable skill library or publish host-specific state.

## Target model

```text
                              SOFTWARE TASK
                                   │
                                   ▼
                         Intent / classification
                                   │
                                   ▼
                              product-spec
                                   │
                                   ▼
                           codebase-explorer
                                   │
                                   ▼
                        solution-architecture
                                   │
                                   ▼
                         feature-development
                            orchestration
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
              implementation                specialists
                                             as needed
                    │                             │
                    └──────────────┬──────────────┘
                                   ▼
                              verification
                                   │
                                   ▼
                                 review
                                   │
                                   ▼
                             release-check
                                   │
                                   ▼
                                  SHIP
```

The pipeline is adaptive. A small bug fix should not mechanically invoke every specialist. A complex feature may require product definition, architecture, frontend design, browser QA, accessibility, security, performance, and release verification.

## System layers

### 0. Developer environment

devkit/ prepares a macOS machine, provides a safe portable Codex baseline, and
manages opt-in MCP profiles. Active machine configuration is adopted into an
ignored host-local override before installation. This layer owns local
package/configuration lifecycle; it does not own workflow routing or skill
behavior.

### 1. Project intent and instructions

Examples:

- explicit user request
- `AGENTS.md`
- `CLAUDE.md`
- `agents-devkits.yaml`
- project documentation
- `DESIGN.md`
- API contracts
- approved Figma/screenshots

These define project-specific truth and constraints.

### 2. Discovery and routing

The system should determine which workflows are relevant instead of relying on the human to manually name every skill.

Current building blocks:

- `SKILLS.md` — human discovery
- `skills/registry.yaml` — validated routing metadata for AI/tools
- `docs/ROUTING.md` — generated compact candidate index with `AUTO`, `PROPOSE`, and `ASK` levels
- `docs/skill-boundaries.md` — precedence and collision rules
- `agents-devkits.yaml` — project-selected skills, targets, portable capabilities, and explicit verification declarations

Codex and Claude Code keep their native discovery and explicit-invocation flows.
The registry and project manifest guide that routing but do not replace agent
judgment, project instructions, or the explicit user request.

The portable depth contract is intentionally small: `DIRECT` for clear local
reversible work, `FOCUSED` for normal multi-step work, and `FULL` for security,
payments, migrations, destructive operations, public contracts, cross-system
changes, or material uncertainty. It changes coordination, not the requirement
to report only observed evidence.

### 3. Skills

Skills contain reusable procedural knowledge.

Examples:

- `product-spec`
- `solution-architecture`
- `frontend-design`
- `debugging`
- `visual-qa`
- `security-review`
- `release-check`

A skill owns a bounded concern; it should not grow until it becomes a universal agent prompt.

### 4. Tools and integrations

Skills describe how work should be performed. Tools make the work possible.
The portable layer describes capabilities rather than providers: `repository`,
`shell`, `browser`, `figma`, `database`, and `issue-tracker`. Provider-specific
MCP/plugin configuration and credentials belong to a local agent or Devkit
configuration. Skills use a safe fallback and report the limitation when a
preferred capability is not available.

### 5. Orchestration and handoffs

`feature-development` is the current orchestration layer for non-trivial feature work.

Over time, orchestration should become more explicit:

```text
TASK
 │
 ├── bug ───────→ codebase-explorer → debugging → testing
 │
 ├── UI ────────→ frontend-design / figma-to-code
 │                → design-system → responsive-design
 │                → visual-qa
 │
 ├── feature ───→ product-spec → solution-architecture
 │                → implementation → targeted verification
 │
 └── release ───→ focused reviews → release-check
```

Handoffs matter because several specialists may participate without competing for ownership.

### 6. Verification and evidence

Completion must be evidence-based.

Depending on the change, evidence may include:

- typecheck
- lint
- unit/integration tests
- browser/E2E tests
- visual comparison
- accessibility checks
- performance measurements
- security review
- production build
- migrations/configuration validation

The system must distinguish checks actually performed from checks that were
unavailable or merely assumed. Evidence is reported with the work and command
output; the portable layer does not retain a separate execution-history store.

### 7. Release gate

`release-check` defines the final ship/no-ship boundary.

The key principle is:

```text
code written ≠ task complete
```

Instead:

```text
implementation
    + appropriate verification
    + appropriate review
    + release evidence
    = ready to ship
```

## Precedence model

When instructions conflict, use this order:

```text
1. Explicit user request
2. Project instructions
3. Task-specific source of truth
4. Existing project conventions
5. Generic skill guidance
```

A generic skill must never silently override higher-precedence project intent.

## Design principles

### Bounded ownership

One primary owner per concern.

### Adaptive workflow

Do not invoke every skill for every task.

### Evidence over confidence

Agents should report what they actually inspected, ran, measured, or verified.

### Reuse over duplication

Reuse existing project patterns, design systems, tools, official plugins, and integrations before creating parallel mechanisms.

### Handoffs over overlap

When a concern changes, hand work to the appropriate specialist instead of expanding the current skill's responsibility.

### Human-readable and machine-readable knowledge

The system should remain understandable by a developer while also exposing structured metadata for AI routing and automation.

### Provider portability

Core workflows should remain useful across Codex and Claude Code where practical. Provider-specific capabilities can be integrations around the system rather than contaminating every portable skill.

## Development direction

The repository should evolve in stages.

### Stage 1 — Skill library

Status: implemented.

- focused `SKILL.md` workflows
- portable installation for Codex and Claude Code
- provenance for imported skills

### Stage 2 — Conflict-aware workflow system

Status: implemented / evolving.

- responsibility boundaries
- precedence rules
- handoffs
- human catalog
- machine-readable registry
- release gate

### Stage 3 — Intelligent routing

Status: implemented / evolving.

- `skills/registry.yaml` is validated against every installed skill and records invocation, declarative triggers, inputs, outputs, verification, portable capabilities, references, relationships, handoffs, and routing levels
- `docs/ROUTING.md` is generated from that contract; `project.py init` snapshots it into `.agents-devkits/ROUTING.md` so agent instructions have a compact, reviewable selection aid
- `AUTO` selects a justified boundary, `PROPOSE` announces an orchestration workflow without blocking for approval, and `ASK` requires an explicit request; none of the levels changes safety authorization
- native explicit and implicit discovery in Codex and Claude Code remains the router; registry metadata guides it but is not a scheduler or context compiler
- project instructions and the task retain final routing authority
- skills are still selected only when their specialist boundary is justified

Conceptually:

```text
Task
 ↓
Classifier / router
 ↓
Relevant workflow graph
 ↓
Specialists
```

### Stage 4 — Tool-aware execution

Status: implemented / evolving.

- registry and project manifests use provider-neutral capabilities: `repository`, `shell`, `browser`, `figma`, `database`, and `issue-tracker`
- skills state safe fallbacks when browser or Figma access is unavailable
- provider-specific MCP/plugins and credentials remain outside the portable core, in local agent or Devkit configuration
- capabilities guide justified tool use; they do not claim a provider is available

### Stage 5 — Evidence-aware completion

Status: implemented / evolving.

- orchestration and specialist reviews return decisions, artifact summary, actually performed checks, results, and remaining risks
- `feature-development` passes specialist evidence to `release-check`
- `release-check` accepts only executed or authoritatively observed evidence and returns `SHIP`, `SHIP WITH KNOWN RISKS`, or `NO-SHIP`
- evidence lives in reports and command output; the portable platform keeps no execution history or permanent evidence store

### Stage 6 — Reusable project bootstrap

Status: initial implementation.

`project.py` creates a thin cross-platform project layer without copying skill directories (`project.sh` remains a compatibility wrapper):

- `AGENTS.md`
- `CLAUDE.md`
- versioned `agents-devkits.yaml` with selected skills, targets, portable capabilities, and project-owned verification commands
- safe integration snippets for existing instruction files, or timestamped backup plus managed block with `--adopt`
- `doctor` to check instructions and globally installed canonical skills; `verify` to run only explicitly requested structured checks

This layer is deliberately not a runtime engine, MCP configuration store, or self-contained project distribution. A future self-contained distribution, if needed, must be an explicit separate mode rather than a change to the default global-library model.

Projects may opt into a small, durable knowledge pack when recurring local facts
need to be reused across tasks. A pack records declared source paths and
verified facts; it is loaded on demand, does not become a global skill, and does
not retain execution history. This preserves the boundary between generic
procedure and project-specific truth.

### Stage 7 — Workflow learning and maintenance

Goal:

Use repeated failures and recurring work to improve the system deliberately:

```text
recurring problem
      ↓
identify missing rule / workflow
      ↓
update project instructions OR existing skill
      ↓
create a new skill only when responsibility is genuinely distinct
      ↓
update registry + boundaries + catalog
```

This prevents uncontrolled growth into dozens of overlapping prompts.

## What this system is not

It is not intended to become:

- a giant universal system prompt
- a random prompt collection
- a separate skill for every tiny coding action
- a replacement for project-specific instructions
- a replacement for real tools, tests, or engineering judgment
- a framework that forces every task through the same ceremony

## Canonical project model

```text
                         AGENTS DEVKIT
                              │
                              │ implements
                              ▼
                 AI DEVELOPMENT WORKFLOW SYSTEM
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
     Instructions          Registry             Skills
          │                   │                   │
          └───────────────────┼───────────────────┘
                              ▼
                       Orchestration
                              │
                              ▼
                       Tools / MCP
                              │
                              ▼
                       Implementation
                              │
                              ▼
                    Verification / Review
                              │
                              ▼
                        Release gate
                              │
                              ▼
                            SOFTWARE
```

The long-term goal is simple: **make AI-assisted software development more deliberate, repeatable, inspectable, and production-ready without turning every task into unnecessary process.**
