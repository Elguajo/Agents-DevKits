---
name: project-state-change-adoption
description: Reconcile a new audit, specification, implementation plan, or substantial change request into an existing project's declared durable planning state without implementing the findings. Use when the user asks to incorporate such evidence into an established roadmap, specification, decision record, phase plan, or issue tracker.
---

# Project State Change Adoption

Own the reconciliation of new project evidence into an existing project's
declared durable planning state. Incoming audits, specifications, plans, and
recommendations are evidence and proposed work, never automatic truth or an
implementation mandate.

## Use when

- The user asks to incorporate, reconcile, or turn a new audit, specification,
  implementation plan, architecture review, or substantial change request into
  an established project's roadmap, specification, decision record, phase plan,
  or issue tracker.
- The project already identifies its durable sources of truth and current work
  state in instructions, documentation, or its tracker.
- The requested outcome is a classified, updated plan/state without starting
  implementation.

## Do not use when

- The task is to discover defects, risks, or a new backlog; use
  `project-audit` or the relevant specialist audit first.
- The project has no declared durable planning state; report that precondition
  rather than inventing a framework, document hierarchy, or source of truth.
- The user asks to choose a material product, architecture, compatibility, or
  operational direction; use `product-spec` or `solution-architecture`.
- The task only needs a concise factual reference; use `project-knowledge`.
- The task only asks to display established progress; use `roadmap-status`.
- The repository uses Progressive Context Kit; use
  `progressive-context-change-adoption` so PCK-specific ownership and phase
  invariants remain intact.
- The user asks to implement an accepted finding or plan.

## Workflow

1. Inspect repository instructions, worktree status, and the incoming source.
   Record source provenance and distinguish observed facts, proposals,
   assumptions, contradictions, and unsupported claims.
2. Locate the project's declared durable owners for product scope, current
   architecture, decisions, planned work, current work, and completed history.
   Use only owners the project already declares; when none is sufficient,
   report the missing precondition instead of creating a parallel system.
3. Read the smallest state set needed to test material findings against current
   evidence, planned work, decisions, and historical completion records.
4. Give each material finding one disposition: `ACCEPTED`,
   `ALREADY_COVERED`, `MERGED`, `DEFERRED`, `REJECTED`, or `NEEDS_DECISION`.
   Link it to supporting evidence and an owner or reason.
5. Stop for the user when a material product, architecture, compatibility,
   security, operational-cost, or reversibility decision remains. Do not use
   documentation edits to make that decision implicitly.
6. Update only the declared canonical owner affected by accepted evidence.
   Preserve completed history; add new work in the project's existing planning
   vocabulary and dependency order instead of rewriting prior outcomes.
7. Keep long source material cold at its existing path or URL. Retain precise
   references rather than duplicating it across every durable document or
   tracker item.
8. Verify that every accepted finding has one owner, statuses agree across the
   declared state sources, references resolve, and the next planned work is
   actionable. Hand off implementation without starting it.

## Rules

- Never infer a canonical owner from a familiar filename or impose PCK files,
  phase markers, ADRs, or a particular issue tracker on a non-PCK project.
- Existing project instructions and declared state conventions outrank this
  skill. When they conflict or are incomplete, state the limitation plainly.
- `ALREADY_COVERED` and `MERGED` must link to established work. `DEFERRED` and
  `REJECTED` must retain a reason; `NEEDS_DECISION` must name the decision.
- Do not turn desired future architecture into a claim about the current
  system, and do not overwrite completed history to make a new plan appear
  retroactive.
- This skill changes planning/state only under the user's explicit adoption
  request. It does not implement code, advance work as complete, or claim
  validation that was not observed.

## Handoffs

- Discovery or severity evidence still needed → `project-audit` or the
  relevant specialist audit.
- Material product or technical direction unresolved → `product-spec` or
  `solution-architecture`.
- Only a concise recurring factual reference is needed → `project-knowledge`.
- Existing state is only being presented → `roadmap-status`.
- A Progressive Context Kit project needs adoption →
  `progressive-context-change-adoption`.
- After adoption, implementation proceeds through the project's existing
  execution workflow and declared current-work source.

## Output contract

Return:

1. inspected sources and declared state owners;
2. each material finding with disposition, evidence, and owner/reason;
3. durable artifacts changed and why, versus recommendations left unmodified;
4. planning/current-work changes and retained source references;
5. unresolved decisions and deferred/rejected work;
6. consistency checks actually performed; and
7. one implementation handoff, explicitly stating that no implementation was
   performed.
