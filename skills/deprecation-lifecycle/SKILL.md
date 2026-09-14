---
name: deprecation-lifecycle
description: Retire an API, service, feature, or module by proving replacement readiness, migrating consumers, and verifying zero active use before removal. Use for non-persisted system retirement.
---

# Deprecation Lifecycle

Own **retiring a non-persisted API, service, feature, or module and migrating its consumers**. Persisted schema and data transitions remain with `data-migration`.

## Use when

- An old service, public API, feature, module, or implementation must be deprecated and consumers moved to a replacement.
- A removal needs a consumer inventory, migration plan, rollout, and proof that active usage is zero.

## Do not use when

- The change primarily transitions persisted schemas, data formats, identifiers, preferences, or sync payloads; use `data-migration`.
- The task only discovers a proposed change’s consumers; use `change-impact-analysis`.
- The replacement’s failure/retry semantics or final ship decision is the main concern; use `reliability-review` or `release-check`.

## Workflow

1. Define the retirement target, reason, owner, consumer population, and whether deprecation is advisory or has an approved removal deadline.
2. Prove the replacement covers critical use cases before moving consumers. Discover unknown consumers with `change-impact-analysis`.
3. Publish a migration contract: supported path, compatibility window, rollout controls, observability, and rollback conditions.
4. Migrate consumers in independently verifiable increments. Use adapters, flags, or staged routing only where they reduce a concrete compatibility or rollout risk.
5. Validate consumer behavior and measure active usage. If persisted data must change, hand that transition to `data-migration` and coordinate the plan.
6. Remove the retired code, tests, configuration, documentation, and notices only after evidence shows no active consumer remains. Send final evidence to `release-check`.

## Rules

- Never remove an active surface without a proven replacement or explicit user authorization for the break.
- Treat undocumented observable behavior as a possible dependency until consumer evidence says otherwise.
- Keep destructive removal separate from additive replacement/migration work when rollback or mixed-version safety requires it.
- Do not claim zero usage from source search alone when runtime consumers exist.

## Failure modes / anti-rationalization

- “Nobody uses it” → prove it with consumer and, where applicable, runtime evidence.
- “The replacement is obviously equivalent” → verify critical use cases before requiring migration.
- “We can remove it while adding the replacement” → retain a reversible path until consumer migration is proven.
- “A schema rename is part of this cleanup” → hand persisted compatibility to `data-migration` rather than collapsing both lifecycles.

## Handoffs

- Consumer discovery and blast radius → `change-impact-analysis`.
- Persisted data/schema compatibility → `data-migration`.
- Failure, retry, and rollout recovery behavior → `reliability-review`.
- Runtime evidence visibility → `observability-review`.
- Final removal readiness → `release-check`.

## Output contract

Return the target and owner, replacement evidence, consumer inventory, migration/rollback plan, deprecation state, usage evidence, removal checklist, checks run, and residual risks.
