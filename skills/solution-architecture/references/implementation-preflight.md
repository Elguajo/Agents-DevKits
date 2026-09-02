> Integrated from the v0.1 prompt/skill prototype `implementation-preflight`. Load this reference only when its trigger applies.

# Implementation Preflight
## Goal
Understand enough of the existing system to choose the smallest safe implementation path before touching code.

## Workflow
1. Clarify the requested behavior and constraints from available context.
2. Inspect relevant architecture, existing patterns, APIs, state/data flow, and tests.
3. Identify likely files/components to change.
4. Surface dependencies, migration needs, compatibility concerns, edge cases, and regression surface.
5. Propose the simplest approach that fits the existing architecture.
6. Define verification and rollback considerations.

## Rules
- Do not implement yet.
- Prefer reuse of existing project patterns over introducing new abstractions.
- State assumptions and unknowns explicitly.

## Output
Recommended approach, affected areas, step-by-step plan, risks, open questions, and verification plan.
