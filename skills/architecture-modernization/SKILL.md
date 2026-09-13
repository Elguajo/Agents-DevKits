---
name: architecture-modernization
description: Plan a safe transition away from legacy-constrained architecture when historical compatibility layers, imports, abstractions, or coupling materially block future development. Use when the task is to separate true requirements from accidental legacy constraints and choose a migration strategy rather than merely patching the current design.
---

# Architecture Modernization

Own **the transition strategy from a legacy-constrained current architecture to a cleaner target architecture**.

This skill exists for cases where continuing to extend the current design would preserve accidental historical constraints and compound complexity. It does not assume that old architecture is bad, and it does not authorize a rewrite for elegance alone.

## Use when
- Legacy imports, compatibility layers, module boundaries, or abstractions materially constrain a required change.
- The user asks how the system should be rebuilt or migrated if historical implementation choices were not treated as permanent requirements.
- A clean target architecture exists, but a safe transition path from the current system is unclear.
- Several migration patterns are plausible: in-place replacement, adapter boundary, strangler, parallel run, shadow comparison, staged cutover, or selective retirement.
- Existing consumers, data, or external contracts must be preserved while obsolete internal constraints are removed.

## Do not use when
- The target technical design itself is still undefined and there is no legacy-transition question. Use `solution-architecture`.
- The main question is only “what can this change affect?” Use `change-impact-analysis`.
- The work is behavior-preserving cleanup with no architecture transition. Use `refactor`.
- The problem is a persisted schema or durable-data format transition. Use `data-migration` for that concern.
- The user merely wants an architecture review or code review without a modernization decision.
- The current design is adequate and the proposed rewrite is motivated only by aesthetic preference.

## Core rule

Never confuse **requirements** with **historical implementation choices**.

Preserve by default only what has evidence that it must survive:
- required product behavior;
- externally relied-upon contracts;
- user data and durable invariants;
- explicit compatibility requirements;
- compliance, safety, operational, or platform constraints;
- proven project conventions that still serve an active purpose.

Challenge rather than automatically preserve:
- obsolete abstraction layers;
- legacy import structures;
- accidental coupling;
- duplicate compatibility paths;
- dead adapters or shims;
- implementation-specific contracts with no confirmed consumer;
- complexity whose only justification is “this is how the old system works.”

## Workflow

### 1. Establish current-state evidence
Inspect the repository and identify the smallest relevant architecture surface. Record current boundaries and ownership, relevant data/control flow, compatibility layers and legacy imports, known consumers, existing migration/deprecation mechanisms, and the objective reason the current architecture blocks change. Use `codebase-explorer` when the current implementation is not already understood.

### 2. Classify constraints
Classify each material constraint as:
1. **Required invariant**
2. **External contract**
3. **Transitional constraint**
4. **Historical constraint**
5. **Unknown**

If consumer ownership is unclear, hand off to `change-impact-analysis` before planning removal.

### 3. Define or confirm the target posture
Describe the minimum target state needed for migration planning: ownership boundaries, dependency direction, compatibility boundary, authoritative source of truth, extension model, and lifecycle of the legacy path. If substantive target-design decisions remain, hand off to `solution-architecture`.

### 4. Compare modernization strategies
Evaluate only realistic options:
- in-place simplification;
- adapter boundary;
- strangler migration;
- parallel run;
- shadow comparison;
- staged consumer migration;
- selective replacement;
- hard cutover only when blast radius, rollback, data compatibility, and downtime are explicitly acceptable.

Choose a pattern because it reduces concrete migration risk, not because it sounds sophisticated.

### 5. Define compatibility and consumer strategy
For every changing contract, state confirmed consumers, current dependency, temporary compatibility mechanism, migration owner or handoff, deprecation condition, and removal condition. No compatibility layer is permanent by default.

### 6. Sequence the migration
Prefer reversible phases with observable checkpoints. Each phase must state:
- change introduced;
- invariant preserved;
- consumers affected;
- verification evidence required;
- rollback or containment path;
- exit criteria before the next phase.

Avoid a long-lived rewrite branch unless incremental transition is genuinely impossible.

### 7. Challenge the modernization itself
Before recommending replacement, answer:
- What concrete cost does the legacy design impose today?
- Could a smaller change remove that cost?
- What new failure modes does migration introduce?
- What evidence would prove the new path equivalent or better?
- What must remain reversible until confidence is earned?
- Which compatibility layers can be deleted, and when?

If the case is weak, recommend keeping the current architecture.

### 8. Handoff for execution
- target architecture decision → `solution-architecture`
- consumer/blast-radius discovery → `change-impact-analysis`
- persisted data transition → `data-migration`
- implementation orchestration → `feature-development`
- final ship/no-ship evidence → `release-check`

## Rules
- Do not treat “legacy” as a synonym for “wrong.”
- Do not recommend a rewrite without a material constraint and an evidence-backed benefit.
- Do not remove compatibility for unverified consumers.
- Do not preserve compatibility forever without an exit criterion.
- Prefer the smallest migration surface that reaches the target architecture.
- Distinguish current facts, assumptions, and recommendations.
- Keep migration steps reversible until evidence justifies irreversible cutover.
- Do not claim parity, safety, or readiness without checks that were actually performed.

## Handoffs
- Unknown current implementation → `codebase-explorer`.
- Unknown consumers or blast radius → `change-impact-analysis`.
- Undefined target architecture → `solution-architecture`.
- Persisted data transition → `data-migration`.
- Multi-phase implementation → `feature-development`.
- Release decision → `release-check`.

## Output contract

Return:
1. **Current constraint** — what the existing architecture prevents or makes materially harder, with repository evidence.
2. **Preservation contract** — classify relevant constraints as required invariant, external contract, transitional, historical, or unknown.
3. **Target posture** — minimum target state needed for transition reasoning; flag decisions owned by `solution-architecture`.
4. **Strategy decision** — compare realistic migration options and select one.
5. **Compatibility and consumers** — confirmed consumers, temporary compatibility, deprecation rules, and removal criteria.
6. **Migration phases** — ordered phases with verification, rollback/containment, and exit criteria.
7. **Risks and unknowns** — material failure modes and assumptions.
8. **Recommendation** — one of `KEEP CURRENT ARCHITECTURE`, `MODERNIZE IN PLACE`, `ISOLATE LEGACY AND MIGRATE`, or `REPLACE WITH STAGED CUTOVER`, plus the next specialist handoff.
