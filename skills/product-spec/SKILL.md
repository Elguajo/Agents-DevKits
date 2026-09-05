---
name: product-spec
description: Turn an ambiguous product or feature idea into a concise implementation-ready specification with scope, user outcomes, constraints, edge cases, and acceptance criteria. Use before architecture or coding when requirements are unclear or incomplete.
---

# Product Spec

Own the **what and why**, not the technical implementation.

## Use when
- A feature request is vague, broad, or missing acceptance criteria.
- The user wants a PRD, feature brief, product spec, scope, requirements, or implementation-ready definition.
- Engineering work would otherwise require guessing product behavior.

## Do not use when
- The task is already precise enough to implement safely.
- The main question is technical architecture; hand off to `solution-architecture`.
- The main question is visual art direction; defer to `frontend-design` or the project design source of truth.

## Workflow
1. Read project instructions and relevant existing product docs first.
2. Identify the user/problem, intended outcome, and concrete feature behavior.
3. Separate must-haves from optional ideas.
4. Define non-goals to prevent scope drift.
5. Capture constraints already present in the repository or request.
6. Enumerate important states and edge cases: loading, empty, error, permissions, offline/network failure where relevant.
7. Write testable acceptance criteria.
8. Mark assumptions explicitly; do not invent business rules.

## Progressive reference

- [`references/success-metrics.md`](references/success-metrics.md) — the spec must also define how success is measured and which events are worth emitting.

## Output contract
Produce only as much specification as the task needs. Prefer:
- Problem / goal
- Users and primary use cases
- In scope
- Out of scope
- Functional requirements
- Important states and edge cases
- Constraints
- Acceptance criteria
- Open decisions only when they materially block implementation

## Handoff
Once product behavior is sufficiently defined, hand technical decisions to `solution-architecture`. Do not prescribe frameworks, database schemas, component trees, or implementation details unless a requirement explicitly constrains them.
