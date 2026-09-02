> Integrated from the v0.1 prompt/skill prototype `independent-implementation-review`. Load this reference only when its trigger applies.

# Independent Implementation Review
## Goal
Verify whether the implementation is correct, complete, maintainable, and safe relative to the original requirement.

## Workflow
1. Reconstruct the original requirement and expected behavior.
2. Inspect the actual changed code and enough surrounding architecture to understand it.
3. Challenge correctness, edge cases, regressions, architecture fit, error handling, performance, and tests.
4. Run relevant tests, type checks, builds, or reproduction scenarios where possible.
5. Separate confirmed facts, assumptions, and production risks.
6. Do not modify code unless the user explicitly asks for fixes after the review.

## Rules
- Do not review only the diff if surrounding context matters.
- Do not approve with "looks good" reasoning.
- Do not invent failures without a plausible code path or evidence.
- Do not weaken tests to validate the implementation.

## Output
Verdict: APPROVED / NEEDS IMPROVEMENT / REJECTED.
For each finding include severity, location, problem, impact, recommended fix, and verification status.
