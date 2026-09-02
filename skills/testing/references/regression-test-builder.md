> Integrated from the v0.1 prompt/skill prototype `regression-test-builder`. Load this reference only when its trigger applies.

# Regression Test Builder
## Goal
Encode the original failure as a behavior-level test that fails before the fix and passes after it.

## Workflow
1. Reconstruct the smallest reliable reproduction of the original bug.
2. Identify the observable behavior or invariant that was violated.
3. Choose the lowest test level that proves the behavior without over-mocking.
4. Confirm the test would fail against the old behavior when feasible.
5. Add the test using existing project conventions.
6. Ensure it remains meaningful if implementation details are refactored.

## Rules
- Test the bug, not the patch.
- Avoid brittle timing, sleeps, or excessive mocks.
- Do not weaken existing tests.

## Output
Test added, behavior protected, why it would catch the regression, and any remaining untested edge cases.
