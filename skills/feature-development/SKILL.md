---
name: feature-development
description: Orchestrate a non-trivial feature from clarified requirements through exploration, architecture, implementation, focused verification, and review. Use for multi-file features that benefit from a structured end-to-end workflow.
---

# Feature Development

Own **workflow orchestration**, not the specialist responsibilities themselves.

## Use when
- Building a non-trivial feature across multiple files or layers.
- Requirements, architecture, implementation, and verification all matter.
- The user wants an end-to-end feature workflow rather than one focused task.

## Do not use when
- The change is a tiny, well-defined fix.
- The user only asks for design, debugging, testing, or review; use that focused skill directly.

## Workflow
1. Clarify product intent with `product-spec` when scope or acceptance criteria are unclear.
2. Use `codebase-explorer` to understand relevant existing patterns.
3. Use `solution-architecture` for material technical decisions.
4. Use `change-impact-analysis` when the proposed change touches shared APIs, schemas, persisted identifiers, or core state with unclear consumers.
5. Use `data-migration`, and `data-storage-review` when durable data health also matters, for persisted format or schema changes.
6. Use `concurrency-review` when async tasks, queues, jobs, or shared mutable state create ordering risk.
7. Use `reliability-review` when the workflow must survive timeouts, restarts, partial failure, or duplicate delivery.
8. Use `observability-review` when the change would otherwise be undiagnosable in production.
9. Use `quality-constraints` when the project needs an enforceable quality bar;
   use `source-driven-implementation` only for version-sensitive choices;
   use `adversarial-decision-review` only for a high-impact decision that needs
   fresh-context challenge; use `deprecation-lifecycle` when retiring a
   non-persisted consumer surface.
10. Immediately before implementation, confirm the approved plan still uses the smallest coherent path: reuse, standard library, native platform, installed dependency, or a direct local change before adding new implementation. If evidence requires a new boundary or invalidates that plan, return to `solution-architecture` rather than silently expanding scope.
11. Implement the approved smallest coherent solution in independently
    verifiable increments where practical. Prefer thin vertical slices; take a
    risk-first slice when an unknown could invalidate later work. Keep each
    increment coherent and rollback-friendly; use a feature flag only when the
    project has an established mechanism and incomplete work must merge safely.
12. For UI work, preserve supplied design intent and coordinate with `frontend-design`, `design-system`, `figma-to-code`, `responsive-design`, and `motion-design` only as relevant.
13. Verify behavior with `testing` and/or `playwright-testing`.
14. Verify visible UI with `visual-qa` when appropriate.
15. Run focused `accessibility-review`, `performance-review`, `code-review`, or `security-review` when the change affects those concerns.
16. Collect each specialist's decision, changed artifact/surface, checks actually run, results, and residual risks.
17. Hand that evidence—not an unsupported completion claim—to `release-check`.

## Orchestration rules
- Do not invoke every skill mechanically; use only specialists justified by the task.
- Steps 4 to 8 are conditional specialists, not a default sequence; select one only when the task shows its trigger.
- Resolve workflow depth before orchestration: `DIRECT` for a clear, local, reversible change; `FOCUSED` for normal feature work; `FULL` for security, migrations, destructive operations, public contracts, cross-system changes, or material uncertainty. Depth changes coordination, never the truthfulness of verification.
- A specialist's explicit boundary overrides this orchestrator.
- Do not reopen settled product/design decisions without evidence of a conflict or defect.
- Keep implementation proportional to the requirement; avoid speculative infrastructure.
- Do not require commits as workflow checkpoints: follow the project’s Git
  conventions and the user’s authorization. Separate unrelated cleanup from the
  feature either way.
- Do not trade required validation, failure/recovery handling, security, accessibility, compatibility, reliability, or data integrity for a smaller diff.
- State what was actually verified versus what remains unchecked.
- If a preferred capability such as browser or Figma access is unavailable, preserve the limitation in the evidence and use the strongest available non-substitute check.
- Record specialist evidence as ephemeral entries with `id`, `kind`, `status`, and `source`. Valid statuses distinguish `passed`, `failed`, `unavailable`, `not_applicable`, and `inferred`; never re-label an unavailable or inferred check as passed.

## Output contract
Return:
- Feature status
- Decisions made
- Files/surfaces changed
- Specialist evidence: decisions, artifacts/surfaces, checks run, and results
- Findings/fixes
- Remaining risks or follow-ups
