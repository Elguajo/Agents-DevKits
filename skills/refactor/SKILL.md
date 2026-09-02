---
name: refactor
description: Improve the internal structure, clarity, duplication, boundaries, or maintainability of existing code while preserving externally observable behavior. Use for behavior-preserving cleanup and simplification.
---

# Refactor

Own **behavior-preserving structural improvement**.

## Use when
- Code is difficult to understand, duplicated, over-coupled, or unnecessarily complex.
- The user explicitly wants cleanup, simplification, extraction, or reorganization without feature changes.

## Do not use when
- Behavior is currently wrong and the cause is unknown; use `debugging` first.
- Product behavior or architecture must materially change; use `solution-architecture` / `feature-development`.
- The task is only reviewing code; use `code-review`.

## Workflow
1. Establish current behavior with tests, usage, or clear invariants.
2. Identify the concrete maintenance problem rather than rewriting by taste.
3. Choose the smallest refactor that improves the problem.
4. Preserve public contracts, user-visible behavior, and data semantics unless explicitly authorized.
5. Refactor in coherent steps and run relevant tests after each logical change when feasible.
6. Remove dead/duplicated code only when usage is confidently understood.
7. Avoid introducing abstractions without at least two real consumers or a clear boundary need.
8. Compare the final diff against the original goal for unnecessary churn.

## Progressive reference

- [`references/behavior-preserving-refactor.md`](references/behavior-preserving-refactor.md) — detailed behavior-preservation workflow when observable behavior is weakly protected.

## Handoffs

- Behavior is wrong and the cause is unknown → `debugging`.
- Coverage is missing before restructuring → `testing`.
- Architecture fit of a completed change → `code-review`.
- A shared contract or schema is in the blast radius → `change-impact-analysis`.

## Output contract
Return:
- Problem improved
- Structural changes made
- Behavior-preservation evidence
- Complexity/duplication removed
- Any follow-up that should remain separate from this refactor
