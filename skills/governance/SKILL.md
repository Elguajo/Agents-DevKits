---
name: governance
description: Govern the evolution of a design system through compatibility-aware token and component changes, deprecations, ownership, and migration communication.
---

# Design-System Governance

Use this skill for durable design-system policy and compatibility decisions. It is not a substitute for repository-wide architecture governance or routine documentation edits.

## Workflow

1. Classify the requested token or component change as additive, corrective, deprecating, or breaking for existing consumers.
2. Confirm ownership, affected consumers, required versioning, and migration documentation before changing a published contract.
3. For deprecations, define the replacement, migration period, and removal condition. Do not silently remove public names.
4. Require evidence that a new primitive or token solves a reusable need rather than a single page's styling preference.
5. Hand implementation to `design-tokens` or `design-component`; use `release-check` when the change affects a release decision.

## Completion evidence

Return the compatibility classification, affected consumers, migration path, version/change-log requirements, and unresolved ownership decisions.
