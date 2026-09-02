> Integrated from the v0.1 prompt/skill prototype `large-dataset-handling`. Load this reference only when its trigger applies.

# Large Dataset Handling
## Goal
Keep correctness and responsiveness as data volume grows.

## Workflow
1. Define expected and worst-case data volume and access patterns.
2. Measure or estimate read/write/query/render costs using project evidence.
3. Check pagination, lazy loading, indexing, batching, incremental processing, caching, compaction, archival, and retention as relevant.
4. Identify operations whose complexity grows poorly.
5. Preserve user-visible semantics while reducing unnecessary work.
6. Define realistic scale tests.

## Rules
- Do not choose limits without product semantics.
- Distinguish hot/recent data from archival data.
- Avoid loading entire datasets when the user only needs a window.

## Output
Scale risks, thresholds, recommended strategy, data-retention implications, and validation plan.
