---
name: change-impact-analysis
description: Analyze the blast radius of a proposed code or data change before implementation. Use when modifying shared APIs, schemas, core state, persistence, common components, or behavior with many consumers.
---

# Change Impact / Blast Radius Analysis

## Goal
Identify direct and indirect consumers that could break if the proposed change is made.

## Use when
- A shared API, schema, persisted identifier, event contract, or core component is about to change.
- Consumers of the current behavior are unknown or only partly known.

## Do not use when
- The technical approach itself is the open question; use `solution-architecture`.
- The change is already implemented and needs review; use `code-review`.
- The persisted format transition itself is the task; use `data-migration`.

## Workflow
1. Define the exact proposed change.
2. Trace callers, imports, consumers, shared state, persisted data, API contracts, events, jobs, tests, and external integrations.
3. Identify compatibility assumptions and hidden coupling.
4. Classify affected areas by likelihood and severity.
5. Recommend containment, sequencing, or migration steps.

## Rules
- Do not implement the change.
- Do not infer impact solely from filenames; follow actual references and runtime/data paths.
- Distinguish confirmed dependencies from plausible but unverified risks.

## Handoffs

- Chosen approach and sequencing → `solution-architecture`.
- Persisted format or schema transition → `data-migration`.
- Structure of the current system is unclear → `codebase-explorer`.

## Output
Risk: LOW / MEDIUM / HIGH, affected areas, evidence, mitigation steps, and required verification.
