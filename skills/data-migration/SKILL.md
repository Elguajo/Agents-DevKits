---
name: data-migration
description: Plan or review a schema, storage, or data-model migration while preserving existing user data and backward compatibility. Use when changing persisted formats, database schemas, identifiers, preferences, or sync contracts.
---

# Data Migration & Backward Compatibility

## Goal
Change persisted data safely across old and new versions without silent loss, corruption, or incompatible states.

## Use when
- A persisted schema, file format, identifier, preference, cache contract, or sync payload changes.
- Existing user data must survive an upgrade, or old and new versions must coexist.

## Do not use when
- Durable data health in normal operation is the concern rather than a transition; use `data-storage-review`.
- Only the release decision remains; use `release-check`.

## Workflow
1. Identify current schema/format, new schema/format, and all producers/consumers.
2. Define migration direction, version detection, idempotency, rollback/failure behavior, and mixed-version scenarios.
3. Inventory existing user data states, including malformed/partial/legacy records.
4. Design the smallest migration with explicit invariants.
5. Add migration tests using representative old data.
6. Verify repeated migration, interrupted migration, empty data, large data, and downgrade/rollback behavior when relevant.

## Rules
- Never assume all users are on the latest schema.
- Avoid destructive migration unless explicitly required and recoverable.
- Do not mark migration complete without tests against legacy data.

## Handoffs

- Storage health, growth, or retention questions → `data-storage-review`.
- Coverage against representative legacy data → `testing`.
- Interrupted or duplicated migration semantics → `reliability-review`.
- Ship decision → `release-check`.

## Output
Migration plan, invariants, compatibility matrix, failure/rollback strategy, tests, and unresolved risks.
