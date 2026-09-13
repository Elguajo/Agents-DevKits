---
name: roadmap-status
description: Present an existing project's verified roadmap as a basic or detailed nested checkbox list showing completed, in-progress, blocked, and remaining work. Use when the user asks for roadmap status, what is done now, or what remains; do not use to invent a product or implementation plan.
---

# Roadmap Status

Own the **presentation of an existing roadmap's verified state**. Produce a
basic or detailed, scannable status view; do not turn missing evidence into
completed work or silently create a new plan.

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

1. Select the requested output depth before presenting the roadmap:
   - If the user explicitly asks for a *basic*, *brief*, *compact*, *full*, or
     *detailed* roadmap, honour that choice.
   - Otherwise, ask one concise question with two checklist choices:

     ```markdown
     Какую карту подготовить?

     - [ ] Базовую
     - [ ] Подробную
     ```

     Do not produce the roadmap until the user answers.
   - **Basic** is a phase-level progress view with only the current gate and
     immediate remaining work. **Detailed** is a project map: every phase's
     established tasks and acceptance gates, material evidence boundaries,
     linked ADRs/decision records, and every documented unfinished task in
     dependency order.
2. Find the project's canonical roadmap, its declared planned/queued-phase
   source, and the smallest supporting records needed to explain the active
   item, blockers, and completed claims. Preserve repository-specific status
   vocabulary when it exists. In detailed mode, inspect every active, blocked,
   planned, and separately queued phase record, then follow only the ADR and
   planning-record references from those canonical sources. If a canonical
   queue or phase record is unavailable or contradicts the roadmap, state that
   evidence boundary instead of treating the detailed map as exhaustive.
3. Separate observed facts from inference. A completed checkbox requires
   explicit completion evidence; a blocked item remains incomplete even if work
   has started.
4. Return the result as a nested Markdown checklist. Use this status legend
   when the project has no stronger local convention:
   - `[x]` completed;
   - `[>]` in progress;
   - `[ ]` planned, blocked, or otherwise not complete.
5. Place the current phase in its natural roadmap position and state a material
   blocker or gate directly beneath it. List remaining work in dependency order
   without fabricating dates, estimates, owners, or success claims.
6. Keep completed phases concise in basic mode, but include their outcome
   boundaries when a reader could otherwise mistake graph, smoke, or unit
   evidence for production parity or release readiness. In detailed mode,
   include every documented task and acceptance gate for active, blocked, and
   planned phases; group completed tasks compactly when their supporting record
   already supplies the outcome boundary.

## ADRs and planned work

- In detailed mode, add an `ADRs and decisions` subsection for each phase that
  has roadmap- or phase-referenced ADRs. State the ADR identifier, its recorded
  decision, and the roadmap consequence; link or name the canonical record.
- Include all documented unfinished tasks and acceptance gates, including
  optional-adapter sequences, release gates, and separately queued phases.
  Preserve their existing task IDs and status; do not convert a planned item
  into a commitment, invent an ADR, or infer a dependency absent from the
  canonical records.
- In basic mode, mention an ADR only when it changes the active phase's scope,
  blocker, or next action.

## Output contract

Start with `## ROADMAP — <project>`, then use phase-level and task-level
checkboxes. End with one short **Current status** sentence when a phase is
blocked or materially constrained. Include observed validation only when it
helps interpret a completion claim. In detailed mode, include `ADRs and
decisions` and every canonical unfinished task; in basic mode, omit those
details unless they materially determine the current action.

## Handoffs

- Missing or contradictory source-of-truth status → `project-knowledge`.
- Request for a new technical roadmap or an architecture decision →
  `solution-architecture`.
- Request to discover risks and generate priorities from a repository →
  `project-audit`.
