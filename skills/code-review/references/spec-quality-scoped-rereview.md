> Local protocol informed by selected Superpowers review practices. Load only when written acceptance criteria and a completed change require separate scope and engineering-quality review.

# Spec, Quality, and Scoped Re-Review

## Goal

Check that a completed change satisfies its written acceptance criteria separately from whether the implementation is correct and maintainable, then re-check only the fixed finding when the repair remains narrow.

## Workflow

1. Identify the authoritative request, specification, acceptance criteria, constraints, completed diff, and executed evidence. If scope is ambiguous, hand the definition question to `product-spec`; do not invent requirements during review.
2. Run a spec-compliance pass: trace each stated acceptance criterion and required state to changed behavior or explicit evidence. Report missing, broadened, or contradicted requirements with the supporting artifact.
3. Run the normal engineering-quality pass: correctness, regressions, contracts, failure paths, maintainability, and required specialist handoffs. Do not collapse specialist security, accessibility, reliability, or performance review into this pass.
4. Re-review a fix only against the original finding, the modified files, and the checks that can be affected by that fix. Escalate to a broader review when the fix changes a contract, broadens scope, alters shared behavior, or introduces unrelated changes.
5. If independent reviewer context is available and justified, use it for one pass; otherwise identify the limitation instead of calling self-review independent.

## Rules

- Spec compliance assesses accepted intent; code quality assesses implementation health. Neither may silently redefine the other.
- A scoped re-review is not a clean bill of health for the whole branch.
- Do not turn an explicit acceptance criterion into optional scope merely to close a finding.
- Do not require a fresh reviewer, extra model, or external service when the runtime cannot provide one.

## Output

Return spec findings, quality findings, evidence for each, scoped re-review scope and result when used, unreviewed surfaces, and the smallest justified handoff.
