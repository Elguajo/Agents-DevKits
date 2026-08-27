---
name: migrate-design-system
description: Plan and execute a compatibility-aware migration between design-token, component, or UI-library systems using an explicit role-by-role crosswalk.
---

# Migrate Design System

Use this skill for intentional interop or migration. It owns the mapping and rollout plan; implementation remains with the relevant code and component skills.

## Workflow

1. Inventory the source and target systems, consumers, supported platforms, and non-negotiable behavior or accessibility constraints.
2. Build a crosswalk by role: actions, text, surfaces, borders, feedback, typography, spacing, radius, elevation, motion, components, and states. Do not map by color name alone.
3. Choose a rollout strategy: aliases/bridge layer, incremental component migration, or coordinated replacement. Preserve backwards compatibility until consumers migrate unless a breaking change is explicitly approved.
4. Validate representative themes, component states, and accessibility-sensitive roles with available project checks.
5. Hand token work to `design-tokens`, component work to `design-component` and `design-code`, and release evidence to `release-check`.

Read [crosswalk.md](references/crosswalk.md) for the required mapping record.

## Completion evidence

Return the source/target inventory, crosswalk, compatibility strategy, observed validation, migration gaps, and rollback considerations.
