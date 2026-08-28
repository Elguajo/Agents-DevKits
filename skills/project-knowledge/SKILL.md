---
name: project-knowledge
description: Extract verified, project-specific technical or design-system facts into a concise knowledge pack that other skills can load on demand. Use when a repository has recurring conventions that agents need without duplicating or inventing a global skill.
---

# Project Knowledge

Own **project-specific factual references**. Do not create a new generic skill,
change the design system, or replace project instructions.

## Use when

- A project has a design system, component library, API surface, or workflow
  whose facts recur across tasks.
- Generic skills need concrete project facts such as token locations, component
  imports, conventions, or generated outputs.
- The project opts in through `agents-devkits.yaml` and a knowledge-pack file.

## Do not use when

- The relevant facts are small, task-local, or already clearly documented in a
  project instruction or source-of-truth document.
- The task asks to invent a design system or change product behavior.
- The sources cannot be inspected; report that limitation instead of guessing.

## Workflow

1. Read project instructions, `agents-devkits.yaml`, and the declared knowledge
   pack before modifying it.
2. Inspect every declared source path. Treat source code, generated artifacts,
   and consumer usage as different kinds of evidence.
3. Record only facts that can be traced to a file path, export, configuration,
   or observed usage. Mark inferences and unresolved questions explicitly.
4. Keep the pack concise and navigable. Prefer links and file paths over copied
   source or broad framework advice.
5. For design systems, cover the token source of truth, component/export entry
   points, styling conventions, generated outputs, and known consumer patterns.
6. Add or update the pack's "Verification" section with the exact files or
   commands inspected. Do not say a generated artifact is current unless that
   was actually verified.
7. Hand implementation work to the owning specialist, such as `design-system`,
   `figma-to-code`, `design-code`, or `solution-architecture`.

## Pack rules

- A pack is durable project documentation, not an execution log or agent memory.
- A pack must not contain credentials, private tokens, or copied third-party
  source that is unnecessary for the factual reference.
- Preserve project-owned wording and existing references; do not silently
  overwrite a pack created by a team member.
- The declared source list is provenance, not proof that every statement is
  still correct. Reinspect it before materially relying on stale facts.

## Output contract

Return:

- Pack path and inspected source paths
- Verified facts added or changed
- Inferences and unresolved questions
- Commands/checks actually run
- Recommended specialist handoff
