> Integrated from the v0.1 prompt/skill prototype `recent-changes-review`. Load this reference only when its trigger applies.

# Recent Changes Review
## Goal
Assess what changed, whether it is correct, and what nearby behavior may have been unintentionally affected.

## Workflow
1. Identify the relevant change set using git history/diff or user-provided scope.
2. Understand the intended task behind the changes.
3. Inspect changed files plus affected callers, tests, contracts, and state/data flows.
4. Check for missing requirements, accidental scope expansion, regressions, dead code, and insufficient tests.
5. Run focused validation.

## Rules
- Review intent and behavior, not formatting alone.
- Do not assume generated code is safe because tests pass.
- Do not propose unrelated cleanup.

## Output
Summary of changes, findings by severity, validation performed, and merge/readiness recommendation.
