> Integrated from the v0.1 prompt/skill prototype `performance-degradation-investigation`. Load this reference only when its trigger applies.

# Performance Degradation Investigation
## Goal
Find the accumulating factor or repeated work that causes performance to degrade and fix it without sacrificing correctness or user data.

## Workflow
1. Define the slow scenario and a measurable baseline.
2. Trace work performed as data/history/session count grows.
3. Measure storage size, query cost, initialization work, memory, network, rendering, or background jobs as relevant.
4. Determine whether the problem is loading too much, processing too much, storing too much, invalidating caches, or retaining resources.
5. Evaluate strategies such as pagination, bounded retention, indexing, lazy loading, batching, compaction, or archival based on evidence.
6. Implement the smallest safe fix and verify before/after behavior.
7. Protect the scenario with a performance or regression test where practical.

## Rules
- Do not choose arbitrary limits without product/data-retention justification.
- Do not delete user data silently.
- Preserve legitimate access to required historical data.

## Output
Bottleneck, evidence/measurements, chosen strategy, trade-offs, verification, and data-retention implications.
