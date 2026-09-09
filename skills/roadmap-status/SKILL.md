---
name: roadmap-status
description: Present an existing project's verified roadmap as a concise nested checkbox list showing completed, in-progress, blocked, and remaining work. Use when the user asks for roadmap status, what is done now, or what remains; do not use to invent a product or implementation plan.
---

# Roadmap Status

Own the **presentation of an existing roadmap's verified state**. Produce a
compact, scannable status view; do not turn missing evidence into completed
work or silently create a new plan.

## Use when

- The user asks for a full roadmap, roadmap status, progress, or a clear view
  of completed, current, and remaining work.
- A canonical roadmap, phase plan, issue tracker, or equivalent project source
  can be inspected.

## Do not use when

- The user needs requirements, scope, or acceptance criteria defined for the
  first time; that belongs to `product-spec`.
- The request is to decide a technical approach or implementation sequence;
  that belongs to `solution-architecture`.
- The user wants a broad health audit or a new backlog derived from discovery;
  that belongs to `project-audit`.

## Workflow

1. Find the project's canonical roadmap and the smallest supporting records
   needed to explain the active item, blockers, and completed claims. Preserve
   repository-specific status vocabulary when it exists.
2. Separate observed facts from inference. A completed checkbox requires
   explicit completion evidence; a blocked item remains incomplete even if work
   has started.
3. Return the result as a nested Markdown checklist. Use this status legend
   when the project has no stronger local convention:
   - `[x]` completed;
   - `[>]` in progress;
   - `[ ]` planned, blocked, or otherwise not complete.
4. Place the current phase in its natural roadmap position and state a material
   blocker or gate directly beneath it. List remaining work in dependency order
   without fabricating dates, estimates, owners, or success claims.
5. Keep completed phases concise, but include their outcome boundaries when a
   reader could otherwise mistake graph, smoke, or unit evidence for production
   parity or release readiness.

## Output contract

Start with `## ROADMAP — <project>`, then use phase-level and task-level
checkboxes. End with one short **Current status** sentence when a phase is
blocked or materially constrained. Include observed validation only when it
helps interpret a completion claim.

## Handoffs

- Missing or contradictory source-of-truth status → `project-knowledge`.
- Request for a new technical roadmap or an architecture decision →
  `solution-architecture`.
- Request to discover risks and generate priorities from a repository →
  `project-audit`.
