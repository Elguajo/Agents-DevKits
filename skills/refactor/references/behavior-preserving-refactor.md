> Integrated from the v0.1 prompt/skill prototype `behavior-preserving-refactor`. Load this reference only when its trigger applies.

# Behavior-Preserving Refactor
## Goal
Improve internal structure without changing external behavior.

## Workflow
1. Identify observable behavior, contracts, invariants, and current tests.
2. Establish a baseline with relevant tests/checks.
3. Define the smallest structural problems to address.
4. Refactor incrementally: duplication, dead code, unnecessary indirection, oversized responsibilities, confusing naming, or tangled dependencies.
5. Re-run verification after meaningful steps.
6. Add characterization tests first if important behavior is currently unprotected.

## Rules
- Do not mix refactor and feature work.
- Avoid architecture rewrites without evidence they are necessary.
- Preserve APIs and data formats unless change is explicitly part of the task.

## Output
What was simplified, invariants preserved, verification, and any remaining technical debt.
