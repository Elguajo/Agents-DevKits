---
name: codebase-explorer
description: Inspect an existing repository to map relevant architecture, entry points, data flow, dependencies, conventions, and similar implementations before planning or editing code. Use when the agent needs to understand how the current codebase works.
---

# Codebase Explorer

Own **understanding the existing codebase**. Do not design a new architecture or implement the feature unless explicitly asked after exploration.

## Use when
- A task touches an unfamiliar or non-trivial existing repository.
- The user asks how a feature currently works.
- Another skill needs reliable context before planning changes.

## Do not use when
- The repository is trivial and the relevant files are already known.
- The task is greenfield product definition; use `product-spec`.
- The task is choosing a future architecture; hand off to `solution-architecture`.

## Workflow
1. Read project instructions first (`AGENTS.md`, `CLAUDE.md`, README, architecture docs).
2. Identify likely entry points and affected areas.
3. Trace execution/data flow through the smallest relevant set of files.
4. Find similar features and established patterns before inventing new ones.
5. Record important dependencies, state boundaries, APIs, persistence, tests, and build/runtime constraints.
6. Distinguish facts observed in code from assumptions.
7. Return a compact map of the codebase area plus the files another skill should read next.

## Output contract
Return:
- Relevant entry points
- Execution/data flow
- Existing patterns to reuse
- Key files and responsibilities
- Constraints/risks discovered
- Open questions
- Recommended handoff (`solution-architecture`, `debugging`, etc.)

## Boundary rule
Exploration answers **“how is it built now?”**. Architecture answers **“how should we change it?”**. Keep those responsibilities separate.
