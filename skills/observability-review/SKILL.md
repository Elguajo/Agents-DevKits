---
name: observability-review
description: Audit whether production failures and important behavior can be diagnosed. Use for services, background jobs, integrations, async workflows, or user-reported problems that are hard to reproduce. Focus on useful diagnostics rather than logging volume.
---

# Observability Review

## Goal
Ensure important failures can be understood from production evidence without exposing sensitive data or creating noisy telemetry.

## Use when
- Production failures, background jobs, integrations, or async workflows are hard to reproduce or explain.
- A change would otherwise ship without a way to tell whether it is failing.

## Do not use when
- A specific defect is already reproducible; use `debugging`.
- The concern is recovery behavior rather than diagnosis; use `reliability-review`.

## Workflow
1. Identify critical operations, state transitions, external calls, and failure points.
2. Inspect current logs, metrics, traces, error reporting, identifiers, and diagnostic context.
3. Determine which real failures would be ambiguous or invisible.
4. Recommend the minimum additional observability needed.
5. Check privacy, secret, and personally identifiable data exposure.

## Rules
- More logs are not automatically better.
- Prefer structured, actionable context.
- Do not log secrets or unnecessary personal data.

## Handoffs

- A reproducible defect emerges → `debugging`.
- Recovery and retry semantics → `reliability-review`.
- Sensitive data appears in diagnostic output → `security-review`.

## Output
Diagnostic blind spots, why they matter, recommended signals, and privacy/noise considerations.
