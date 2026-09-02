> Integrated from the v0.1 prompt/skill prototype `duplicate-work-investigation`. Load this reference only when its trigger applies.

# Duplicate Work / Repeated Calls Investigation
## Goal
Find why an operation executes more often than intended and remove the duplicate trigger at its source.

## Workflow
1. Define the operation and expected execution count.
2. Instrument call sites, event sources, lifecycle hooks, retries, subscriptions, state changes, and cache behavior.
3. Determine whether duplicates come from multiple triggers, remounts, retries, unstable identity, missing deduplication, or intentional concurrency.
4. Fix ownership/triggering rather than hiding visible symptoms.
5. Verify call counts and legitimate update paths.

## Rules
- Do not assume every repeated call is a bug.
- Do not add arbitrary debounce/delay unless timing semantics require it.
- Preserve real refresh/update behavior.

## Output
Duplicate trigger chain, evidence, corrected invariant, verification counts, and remaining cases.
