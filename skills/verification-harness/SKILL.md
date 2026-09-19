---
name: verification-harness
description: Create or maintain a project-specific, agent-readable real-surface verification harness and small feature map. Use when a project lacks a trustworthy repeatable way to launch, drive, observe, isolate, and clean up real behavior.
---

# Verification Harness

Own **the lifecycle of a project-local real-surface verification harness and its concise user-observable feature map**. This is not test implementation, browser automation, or the final release decision.

## Use when
- A repository has no cold-readable, repeatable way to prove behavior on its real surface.
- The user asks to create, repair, or update a project verification harness or feature map.
- A changed real surface makes the existing harness or its mapped proof paths drift.

## Do not use when
- Durable unit, integration, or characterization coverage is the task → `testing`.
- Browser E2E coverage must be implemented → `playwright-testing`.
- Visual fidelity is the primary question → `visual-qa`.
- The product is broken rather than the verification instructions → `debugging`.
- Final readiness must be aggregated → `release-check`.
- Generic durable project facts, rather than verification paths, are being recorded → `project-knowledge`.

## Workflow
1. Read project instructions, the manifest, and existing project-owned launch/verification tooling. Do not invent commands or environment facts.
2. Identify the primary surface and, from repository evidence, its launch, readiness, drive, observable result, isolation, cleanup, and known limitations.
3. Create or maintain `.agents-devkits/verification/HARNESS.md` using the contract reference. Keep `.agents-devkits/verification/features/README.md` as an index and add only user-observable feature records needed for real verification.
4. When the environment permits, run one mapped path end-to-end. Preserve the resulting evidence after cleaning up only resources created by the run.
5. For maintenance, compare the harness and maps to relevant source changes, perform a focused drive, and update only proven harness drift. Classify differences as harness drift, harness capability gap, product defect, or unavailable environment.
6. Report unavailable proof or product defects honestly; do not repair product behavior by rewriting documentation.

## Rules
- `HARNESS.md` must cover Surface, Launch, Readiness / Doctor, Drive, Evidence, Isolation, Cleanup, and Known limitations.
- Prefer stable semantic selectors, routes, commands, or project-owned scripts over coordinates and UI ordering.
- A proof should connect action → observable result → relevant side effect where applicable. Mocks prove only an intentionally mocked boundary.
- Feature records are verification paths, not a second product specification or architecture encyclopedia.
- Isolate ports, profiles, tenants, data, and worktree state where the project supports it. Never kill processes by generic name; track the owned process/session.
- The harness may describe specialist work but must not make `project.py` a browser driver, LLM scheduler, credential manager, or execution-history service.

## Progressive references
- [`references/harness-contract.md`](references/harness-contract.md) — required artifact semantics and honest maintenance classifications.

## Handoffs
- Durable test coverage → `testing` or `playwright-testing`.
- Visual evidence → `visual-qa`; accessibility evidence → `accessibility-review`.
- Confirmed broken behavior → `debugging`.
- Observed, ephemeral evidence → `release-check`.
- A missing harness discovered during multi-step delivery → `feature-development`.

## Output contract
Return the primary surface, exact project-local artifacts created or changed, one attempted proof and its evidence status/source, isolation and cleanup boundaries, classified gaps, and the next owner for any product defect or unavailable capability.
