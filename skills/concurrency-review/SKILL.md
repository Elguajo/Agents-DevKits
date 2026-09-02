---
name: concurrency-review
description: Audit asynchronous or concurrent code for race conditions, ordering bugs, duplicate execution, stale reads, lost updates, cancellation, reentrancy, or deadlocks. Use for async/await, queues, threads, actors, jobs, event handlers, or shared mutable state.
---

# Concurrency Review

## Goal
Find concurrency bugs with plausible execution sequences, not speculative warnings.

## Use when
- Async/await, threads, actors, queues, background jobs, event handlers, or shared mutable state are the main concern.
- A defect is suspected to depend on timing, ordering, cancellation, or duplicate execution.

## Do not use when
- A defect is observed but no concurrency mechanism is implicated yet; start in `debugging`.
- The concern is retry, idempotency, or recovery semantics rather than interleaving; use `reliability-review`.

## Workflow
1. Map concurrent actors/tasks, shared state, ordering assumptions, and synchronization primitives.
2. Identify read-modify-write sequences, non-atomic operations, callbacks, retries, cancellation, and duplicate triggers.
3. For each suspected issue, construct the concrete interleaving that causes failure.
4. Check state ownership and whether operations are idempotent.
5. Recommend the smallest synchronization or ownership fix.
6. Define deterministic tests where possible.

## Rules
- Do not report a race without a plausible path.
- Avoid solving every problem with a global lock.
- Consider performance and deadlock implications of proposed synchronization.

## Handoffs

- Confirmed defect needs an evidence-based fix → `debugging`.
- Deterministic regression coverage → `testing`.
- Failure and recovery semantics → `reliability-review`.

## Output
Race scenario, triggering interleaving, affected state, severity, fix, and test strategy.
