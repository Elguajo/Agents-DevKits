> Integrated from the v0.1 prompt/skill prototype `test-gap-analysis`. Load this reference only when its trigger applies.

# Test Gap Analysis
## Goal
Identify important behavior that can fail without being detected by the current test suite.

## Workflow
1. Map the feature/module’s critical behaviors and invariants.
2. Read existing tests and what they actually prove.
3. Check happy paths, boundaries, invalid input, failures, persistence, lifecycle transitions, concurrency, migrations, and regression-prone paths as relevant.
4. Rank missing tests by risk and value.
5. Identify brittle tests that overfit implementation details.

## Rules
- Do not equate line coverage with behavioral coverage.
- Do not propose exhaustive low-value tests.
- Prioritize tests that protect expensive or likely regressions.

## Output
Protected behaviors, missing scenarios, priority, recommended test level, and rationale.
