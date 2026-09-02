---
name: data-storage-review
description: Review persistent data handling for correctness, growth, retention, integrity, recovery, and maintainability. Use for databases, files, browser/local storage, histories, preferences, caches, sync state, or other durable user data. Does not own migration execution; hand schema/format transitions to data-migration.
---

# Data Storage Review

## Owns
The health of persistent data at rest and in normal read/write use: source of truth, schema clarity, growth, retention, cleanup, indexing/access patterns, corruption handling, recovery expectations, and cache-vs-user-data boundaries.

## Workflow
1. Map what is stored, where, in what format, and who reads/writes it.
2. Identify source-of-truth data vs derived/cache data.
3. Review atomicity, validation, duplicate/stale data, corruption handling, retention, cleanup, indexing, and growth behavior.
4. Check recovery/export/backup expectations when the data has user value.
5. Identify migration needs but hand the transition mechanics to `data-migration`.
6. Recommend the smallest risk-reducing changes.

## Progressive reference
- `references/large-dataset-handling.md` — histories/lists/events/logs/records whose cost grows with volume.

## Rules
- Do not silently delete durable user data.
- Do not choose arbitrary retention limits without product semantics.
- Keep caches and durable source-of-truth data conceptually separate.

## Handoffs
- Persisted schema/format change → `data-migration`.
- Performance symptom requires measurement → `performance-review`.
- Conflicting state across UI/storage/server → `debugging` with state-consistency reference.
- Failure/recovery semantics across multi-step operations → `reliability-review`.

## Output
Storage map, findings, retention/growth risks, integrity/recovery concerns, recommended actions, and handoffs.
