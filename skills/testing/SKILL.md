---
name: testing
description: Design, add, and run focused automated tests for software behavior across unit and integration boundaries. Use when a change needs durable regression coverage or when existing tests are insufficient. Browser end-to-end testing belongs to `playwright-testing`.
---

# Testing

Own **automated unit/integration test strategy and implementation**.

## Use when
- New or changed behavior needs regression coverage.
- Existing tests do not adequately protect a bug fix or feature.
- The user asks for unit, integration, contract, or regression tests.

## Do not use when
- The main task is browser/E2E verification; use `playwright-testing`.
- The main task is visual parity; use `visual-qa`.
- The user only asks for review of test quality; `code-review` may be sufficient.

## Workflow
1. Read existing test conventions and identify the behavior contract.
2. Choose the cheapest test layer that gives reliable confidence.
3. Prefer behavior and public contracts over implementation details.
4. Cover meaningful success, failure, boundary, and regression cases.
5. Reuse existing fixtures/helpers before creating new test infrastructure.
6. Avoid mocks that erase the behavior being tested; mock only true external boundaries when useful.
7. Run the narrow relevant tests first, then broader suites when warranted.
8. Report flaky, skipped, or unavailable checks explicitly.

## Progressive references

Load only the reference that matches the request.

- [`references/regression-test-builder.md`](references/regression-test-builder.md) — encode a known bug so it cannot silently return.
- [`references/test-gap-analysis.md`](references/test-gap-analysis.md) — audit which important behavior is currently unprotected.
- [`references/edge-case-hardening.md`](references/edge-case-hardening.md) — select realistic boundary and failure cases for a working feature.

## Rules
- Do not chase arbitrary coverage percentages.
- Do not add brittle snapshots for dynamic behavior without a clear reason.
- A passing test that cannot fail for the bug/behavior under discussion is not useful evidence.
- Keep browser automation in `playwright-testing` to avoid duplicate ownership.

## Handoffs

- Browser-level user flow → `playwright-testing`.
- Visual fidelity → `visual-qa`.
- Unknown defect → `debugging`.
- Deterministic tests for a suspected race → `concurrency-review`.
- Migration coverage against legacy data → `data-migration`.
- Final evidence aggregation → `release-check`.

## Output contract
Return:
- Behaviors protected
- Test layer(s) chosen and why
- Tests added/updated
- Commands/results
- Remaining untested risks
