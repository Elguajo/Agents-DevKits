---
name: debugging
description: Diagnose and fix reproducible software defects using evidence, isolation, hypotheses, and regression verification. Use when behavior is wrong, unstable, failing, or unexplained and the root cause is not yet known.
---

# Debugging

Own **root-cause diagnosis and targeted correction**.

## Use when
- A bug can be reproduced or observed through logs/tests/runtime behavior.
- The cause is unclear.
- Previous ad-hoc edits have not reliably solved the problem.

## Do not use when
- The task is planned feature development; use `feature-development`.
- The user only wants code cleanup with unchanged behavior; use `refactor`.
- The issue is purely visual comparison; use `visual-qa`.

## Workflow
1. Reproduce the failure or gather the strongest available evidence.
2. Define expected versus actual behavior precisely.
3. Narrow the failing layer before editing code.
4. Form explicit hypotheses ranked by likelihood/evidence.
5. Test the cheapest discriminating hypothesis first.
6. Fix the smallest root cause rather than masking symptoms.
7. Add or update a regression test when practical.
8. Re-run the original reproduction and relevant nearby checks.
9. Record unresolved uncertainty instead of claiming certainty.

## Progressive references

Load only the reference that matches the investigation.

- [`references/root-cause-debugging.md`](references/root-cause-debugging.md) — full evidence-first protocol for a hard defect.
- [`references/related-bug-hunt.md`](references/related-bug-hunt.md) — search for other instances after one root cause is confirmed.
- [`references/duplicate-work-investigation.md`](references/duplicate-work-investigation.md) — repeated requests, renders, jobs, listeners, or reads.
- [`references/state-consistency-audit.md`](references/state-consistency-audit.md) — stale, reset, or conflicting state across boundaries.
- [`references/lifecycle-resource-cleanup-audit.md`](references/lifecycle-resource-cleanup-audit.md) — timers, listeners, subscriptions, workers, object URLs, sockets, or other retained resources.

## Rules
- Do not randomly modify multiple unrelated areas until the bug disappears.
- Do not suppress errors without understanding them.
- Prefer instrumentation, logs, traces, tests, and minimal experiments over guesswork.
- Preserve unrelated behavior and project conventions.

## Handoffs

- Performance is the primary symptom and needs measurement → `performance-review`.
- A plausible concurrent interleaving is the main mechanism → `concurrency-review`.
- Failure, retry, or recovery semantics are the main concern → `reliability-review`.
- The durable data model itself is suspect → `data-storage-review`.
- The defect is invisible in production evidence → `observability-review`.
- Structural cleanup once behavior is correct → `refactor`.

## Output contract
Return:
- Reproduction/evidence
- Root cause (or strongest remaining hypothesis)
- Fix applied
- Regression verification
- Remaining uncertainty or follow-up
