> Local protocol informed by selected Superpowers execution practices. Load only when a written plan has independently executable tasks that need bounded handoffs, fresh context, safe batching, or compaction recovery.

# Execution Briefs and Recovery

## Goal

Execute a decomposed plan without carrying unnecessary parent context, losing completed work after compaction, or treating coordination artifacts as canonical project state.

## Workflow

1. Confirm that each candidate task has a stable goal, acceptance criteria, scope, dependencies, and verification. Keep tightly coupled or ambiguous work in the current context until the plan is repaired.
2. Create a concise task-owned brief in the project's established workspace or handoff channel: goal, allowed files/surfaces, relevant source paths, constraints, acceptance criteria, and verification required. Link to canonical plans or decisions instead of copying them.
3. Use a fresh executor or reviewer context only when the runtime provides it and the task is sufficiently bounded. Otherwise execute directly with the same brief; do not pretend the context was independent.
4. Batch only same-shape, independent tasks with no shared mutable state, order dependency, conflicting file ownership, or distinct risk profile. Stop batching when evidence invalidates those assumptions.
5. After compaction, resume from the brief, current diff, completed evidence, and source of truth. Re-check the next incomplete task rather than re-running completed work from memory.
6. Record the actual change, checks run, result, and unresolved risk in the handoff. Promote only accepted, durable facts to their existing project owner.

## Rules

- Briefs, progress notes, and review packages are execution scratch, not a second roadmap, ADR, debt ledger, or canonical memory system.
- Do not require subagents, worktrees, commits, or parallelism. They are optional runtime mechanics subject to project instructions and authorization.
- Never hand private repository content to an external agent or service without explicit authorization.
- Fresh context reduces inherited assumptions; it does not replace exact source inspection, validation, or verification.

## Output

Return the bounded task brief, execution method and any unavailable capability, completed evidence, next task or handoff, and residual risk.
