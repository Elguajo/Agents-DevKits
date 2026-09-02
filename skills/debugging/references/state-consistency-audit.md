> Integrated from the v0.1 prompt/skill prototype `state-consistency-audit`. Load this reference only when its trigger applies.

# State Consistency Audit
## Goal
Ensure there is a clear source of truth and state transitions cannot silently diverge.

## Workflow
1. Map every copy of the relevant state and who can mutate it.
2. Define ownership, source of truth, synchronization direction, persistence, and invalidation.
3. Trace stale reads, write races, optimistic updates, rollback, rehydration, cache updates, and lifecycle resets.
4. Identify invariants that must hold across boundaries.
5. Recommend a simpler ownership/synchronization model where possible.
6. Add tests for conflicting and delayed updates.

## Rules
- Do not create another state copy to fix synchronization.
- Distinguish derived state from source-of-truth state.
- Make conflict policy explicit.

## Output
State map, broken invariant, failure sequence, recommended ownership model, and verification.
