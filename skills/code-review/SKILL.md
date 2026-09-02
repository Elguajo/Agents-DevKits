---
name: code-review
description: Review a concrete code change for correctness, regressions, maintainability, error handling, type/data-flow issues, unnecessary complexity, and project-convention violations. Use after implementation or on a diff/PR; report meaningful defects rather than stylistic preferences.
---

# Code Review

Own **general engineering review of a concrete change**. Do not become a second implementation pass by default.

## Use when
- Reviewing a diff, PR, commit, or recently implemented feature.
- Looking for bugs, regressions, maintainability problems, incorrect assumptions, or missing tests.

## Do not use when
- The task is to design the architecture before implementation; use `solution-architecture`.
- The task is a dedicated security audit; use `security-review`.
- The task is visual or accessibility QA; use the corresponding review skill.

## Workflow
1. Read project instructions and the change context.
2. Inspect the diff plus enough surrounding code to understand behavior.
3. Trace changed control/data flows and relevant callers/callees.
4. Check correctness, edge cases, async/concurrency issues, state transitions, error handling, resource cleanup, and backward compatibility.
5. Check types/contracts, validation boundaries, and persistence/network assumptions.
6. Look for unnecessary duplication or complexity only when it creates real maintenance or correctness risk.
7. Check whether tests meaningfully cover the changed behavior and failure paths.
8. Rank findings by severity and confidence.

## Progressive references

Load at most the one reference that matches the situation; the workflow above
stays authoritative.

- [`references/independent-implementation-review.md`](references/independent-implementation-review.md) — another agent or developer implemented the task and the summary must be verified independently.
- [`references/recent-changes-review.md`](references/recent-changes-review.md) — reviewing a recent commit or session change set rather than a prepared diff.
- [`references/dependency-introduction-review.md`](references/dependency-introduction-review.md) — packages, SDKs, frameworks, or runtime services were added or changed.
- [`references/architecture-fit-review.md`](references/architecture-fit-review.md) — behavior works but layering, ownership, or coupling may be wrong.
- [`references/quick-check.md`](references/quick-check.md) — a small local change where a full review would be disproportionate.

## Review rules
- Do not report personal style preferences as defects.
- Do not request refactors unrelated to the change unless they are necessary for correctness or safe maintainability.
- Prefer specific findings with an actual failure scenario over vague "could be cleaner" comments.
- If a concern is security-specific and requires deeper analysis, hand it to `security-review` rather than overstating certainty.
- If no meaningful defects are found, say so; do not manufacture findings.

## Handoffs

- Security-sensitive surface → `security-review`.
- Concurrency or ordering reasoning is central → `concurrency-review`.
- Failure, retry, or idempotency semantics are central → `reliability-review`.
- Measured performance evidence is needed → `performance-review`.
- The request is repository-wide rather than change-scoped → `project-audit`.

## Output contract
For each finding include:
- Severity
- Location
- What can go wrong
- Evidence/reasoning tied to code behavior
- Minimal recommended fix

Optionally include a short residual-risk/testing note after the findings.

## Completion evidence

State the reviewed artifact (diff/PR/files), the review decision, evidence used,
tests or checks actually inspected, and residual risks. Do not treat a clean
review as evidence that checks outside the review scope passed.
