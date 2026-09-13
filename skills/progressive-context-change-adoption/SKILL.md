---
name: progressive-context-change-adoption
description: Reconcile a new audit, specification, implementation plan, or substantial change request into the canonical durable state of an existing Progressive Context Kit project, without implementing the findings. Use when the user asks to incorporate such evidence into PCK project specs, roadmap, or phases.
---

# Progressive Context Change Adoption

Own the reconciliation of new project evidence into the canonical durable state
of an existing Progressive Context Kit (PCK) project. The incoming material is
evidence and proposed work, not automatically true project state or an
implementation mandate.

This is the PCK-specific adapter for `project-state-change-adoption`. Use the
generic owner only where PCK does not govern project state.

## Use when

- An already-adopted PCK project receives an audit, technical specification,
  implementation plan, architecture review, external recommendation, or
  substantial new change request.
- The user asks to incorporate, reconcile, or turn that material into PCK
  project state, roadmap phases, or the next active phase without starting
  implementation.
- The project needs accepted findings classified against its existing Brief,
  Architecture, Roadmap, active Phase, ADRs, and completed-phase evidence.

## Do not use when

- The task is to discover defects, risks, or a new backlog; use
  `project-audit` or the relevant specialist audit first.
- PCK has not yet been adopted into the repository; use PCK's local
  `existing-project-adoption` workflow first.
- Project state is unclear or internally inconsistent before a new source is
  considered; diagnose it with PCK's local `project-doctor` workflow first.
- The user asks to choose between materially different product, architecture,
  compatibility, or operational directions; use `product-spec` or
  `solution-architecture` for that decision.
- The user asks to implement a phase or finding; this skill stops at a PCK
  implementation handoff.
- The change is tiny and does not materially affect durable project state.

## Workflow

1. Confirm the repository is an existing, ready PCK project from its local
   router/runtime markers. Read its router and exact state locations; do not
   assume a PCK version or copy this skill's wording over project-native rules.
2. Inspect Git/worktree status and preserve unrelated edits. Read the smallest
   PCK default state set: Project Brief, current Architecture, Roadmap,
   NEXT_SESSION when present, the sole active `[>]` Phase, its prior compact
   Completion Record when relevant, and only ADRs/source/code needed to test a
   finding.
3. Inspect each incoming source with provenance (path/URL, author or date when
   available, sections or finding IDs). Separate observed facts, proposals,
   assumptions, contradictions, and unsupported claims. An implementation plan
   is checked against the audit and current repository; it is never copied as
   authority.
4. Build a disposition for every material finding: `ACCEPTED`,
   `ALREADY_COVERED`, `MERGED`, `DEFERRED`, `REJECTED`, or `NEEDS_DECISION`.
   State the evidence and canonical owner or reason for each disposition.
5. Stop for the user when a material product, architecture, compatibility,
   security, operational-cost, or reversibility decision remains. Do not use
   document edits to silently decide it.
6. If durable PCK state is insufficient for a fresh session to resume safely,
   repair only the minimum prerequisite state before planning: Brief when scope
   matters, Architecture for current verified system facts, Roadmap, exactly
   one active Phase, and NEXT_SESSION. If this is initial reconstruction rather
   than a repair, return to PCK adoption instead of broadening this skill.
7. Update only the canonical owner affected by accepted evidence:
   - Brief for accepted product outcome, scope, or constraints;
   - Architecture only for current, verified system reality, never proposed
     future architecture;
   - ADR for consequential chosen rationale;
   - Roadmap for dependency-ordered accepted work and phase status;
   - one current Phase for the smallest executable slice, with concrete scope,
     acceptance criteria, verification, and source references;
   - NEXT_SESSION last, as overwriteable hot navigation.
8. Preserve completed phases and Completion Records as history. If every phase
   is complete, append a change-request sequence; never rewrite old phases to
   imply that the new evidence was always planned. Keep exactly one `[>]`
   phase; remaining accepted work stays `[ ]`.
9. Keep the full audit/spec/plan cold at its source path. Put only the active
   phase's necessary slice, finding IDs/section anchors, and relevant ADR links
   in warm PCK state. Do not create a parallel index or duplicate the source
   across canonical documents.
10. Verify canonical consistency: every accepted item has one owner, planned
    work is dependency ordered, current/future markers are valid, Phase
    acceptance and verification match its scope, references resolve, and
    NEXT_SESSION agrees with the active Phase. Report the next PCK execution
    handoff without implementing it.

## Rules

- Treat source material as evidence, not a source of truth. Retain a source
  reference instead of copying long analysis into Brief, Architecture,
  Roadmap, Phase, and NEXT_SESSION.
- A future design belongs in a decision record and planned work until
  implementation changes current reality. Do not describe it as Architecture
  prematurely.
- Group accepted findings into coherent dependency-ordered phases; do not turn
  each finding into an independent phase or mechanically activate all of them.
- `ALREADY_COVERED` and `MERGED` findings must point to existing roadmap or
  phase work. `DEFERRED` and `REJECTED` findings must retain a reason.
- Do not overwrite a conflicting source, completed history, or project-owned
  policy. Escalate material conflicts or missing authority.
- This workflow changes documentation/state only when the user asked for
  adoption. It never starts implementation, claims completion evidence, or
  advances a phase as though work occurred.

## Handoffs

- Findings still need discovery or severity evidence → `project-audit` or the
  relevant specialist audit.
- A material product or technical direction is unresolved → `product-spec` or
  `solution-architecture`.
- A compact recurring factual reference is the only durable output →
  `project-knowledge`.
- A non-PCK project needs the same reconciliation →
  `project-state-change-adoption`.
- After state adoption, execute only through the PCK-local implementation and
  completion workflows, with the active Phase as their source of truth.

## Output contract

Return:

1. inspected sources and current PCK state;
2. every material finding with its disposition, evidence, and owner/reason;
3. canonical files changed and why, versus recommendations left unmodified;
4. roadmap and single active-Phase changes, including retained source links;
5. unresolved user decisions and deferred/rejected work;
6. canonical-consistency checks actually performed; and
7. one implementation handoff, explicitly stating that no implementation was
   performed.
