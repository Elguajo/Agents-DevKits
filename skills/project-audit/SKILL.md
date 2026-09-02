---
name: project-audit
description: Orchestrate a broad technical health audit of an existing repository. Use when the user wants project-wide engineering risks, defects, architecture debt, verification gaps, data/reliability/performance/security concerns, or expensive rework risks before major work. Do not use for one narrow bug or one completed change.
---

# Project Audit

## Owns
Breadth-first technical audit and prioritization across the repository. It is an orchestrator: it discovers where deeper specialist review is justified instead of pretending to perform every discipline at maximum depth itself.

## Workflow
1. Read repository instructions, architecture/project docs, build/test configuration, and major entry points.
2. Use `codebase-explorer` to establish current structure, data flows, dependencies, persistence, integrations, background work, and test strategy when needed.
3. Identify high-consequence technical surfaces and current evidence.
4. Route selectively:
   - architecture/ownership → `solution-architecture` or `code-review`;
   - broad impact of a proposed change → `change-impact-analysis`;
   - durable data → `data-storage-review` / `data-migration`;
   - async/shared state → `concurrency-review`;
   - failure/recovery/idempotency → `reliability-review`;
   - diagnostic blind spots → `observability-review`;
   - performance evidence → `performance-review`;
   - security surfaces → `security-review`;
   - test gaps → `testing`;
   - observed defects → `debugging`.
5. Synthesize only evidence-backed high-value findings.
6. Prioritize by consequence, confidence, effort, and sequencing.

## Rules
- Do not turn the audit into a generic style/lint report.
- Do not invoke every specialist mechanically.
- Do not implement broad fixes during discovery unless the user explicitly asks afterward.
- Separate confirmed defects, credible risks, and optional improvements.

## Output
Executive technical health summary; findings by severity with evidence; specialist handoffs used; Now/Next/Later technical roadmap; unresolved/untested areas.
