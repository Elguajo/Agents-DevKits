---
name: reliability-review
description: Audit how a feature behaves when dependencies fail, time out, return partial data, restart, or execute twice. Use for networked, persistent, transactional, background, or multi-step workflows.
---

# Reliability & Failure-Path Review

## Goal
Ensure failures do not leave the system inconsistent, silently lose data, or create harmful duplicate side effects.

## Use when
- A workflow depends on networks, persistence, transactions, background execution, or multiple steps.
- Retry, restart, duplicate delivery, partial writes, or rollback behavior is undefined.

## Do not use when
- The failure is already observed and needs diagnosis; use `debugging`.
- The concern is whether a failure could be seen at all; use `observability-review`.
- Interleaving of concurrent actors is the mechanism; use `concurrency-review`.

## Workflow
1. Map the workflow and every external or fallible dependency.
2. Inject or reason through timeout, offline, partial response, exception, restart, cancellation, duplicate delivery, and interrupted write cases as relevant.
3. Check error propagation, retries, backoff, idempotency, rollback, partial writes, cleanup, and user-visible state.
4. Identify unrecoverable or ambiguous states.
5. Recommend explicit recovery semantics and tests.

## Rules
- Retries are not automatically safe; verify idempotency.
- Do not swallow errors to make flows appear successful.
- Distinguish transient from permanent failures.

## Handoffs

- Observed failure needs root-cause diagnosis → `debugging`.
- Failures would be invisible in production → `observability-review`.
- Failure semantics depend on persisted data transitions → `data-migration`.
- Coverage for failure paths → `testing`.

## Output
Failure scenarios, current behavior, inconsistency risk, recommended recovery, and verification.
