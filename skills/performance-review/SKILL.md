---
name: performance-review
description: Diagnose and improve web application performance using evidence from runtime behavior, bundles, network activity, rendering, images, fonts, data fetching, caching, and Core Web Vitals. Use when performance is a stated concern or before release for targeted performance review.
---

# Performance Review

Own **measured performance diagnosis and remediation**. Do not perform speculative rewrites.

## Use when
- Pages are slow, heavy, janky, or regress performance metrics.
- Bundle, rendering, network, image/font, caching, or data-fetching behavior needs review.
- A release needs targeted performance verification.

## Do not use when
- No performance problem or requirement exists and there is no evidence to inspect.
- The task is general code cleanup; use `code-review` or a refactor workflow.
- The issue is primarily visual correctness; use `visual-qa`.

## Workflow
1. Establish the target scenario and baseline when tooling permits.
2. Inspect the critical path: navigation, server response, data fetching, JS/CSS delivery, hydration/rendering, images/fonts, and third-party code.
3. Identify measured or clearly evidenced bottlenecks before suggesting fixes.
4. Prefer high-impact changes that preserve behavior and architecture.
5. Check caching, request waterfalls, duplicated fetches, over-fetching, unnecessary client work, and avoidable rerenders.
6. Inspect bundle/dependency cost when relevant.
7. Optimize media and font loading without degrading intended quality.
8. Re-measure after changes and compare against the baseline.

If profiling or production-like metrics are unavailable, keep findings clearly
labeled as static observations or hypotheses and do not invent measurements.

## Progressive references

Load only the reference that matches the symptom.

- [`references/performance-degradation-investigation.md`](references/performance-degradation-investigation.md) — performance worsens over time or as stored data grows.
- [`references/startup-initialization-audit.md`](references/startup-initialization-audit.md) — slow startup, screen reopening, or eager and repeated initialization.

## Rules
- Do not recommend memoization, lazy loading, caching, or code splitting by reflex; justify each with evidence.
- Do not trade correctness or accessibility for marginal speed gains.
- Distinguish local-development artifacts from production behavior.
- Do not claim Core Web Vitals improvements without measurements from appropriate tooling/data.

## Handoffs

- Data growth, retention, or schema is the primary issue → `data-storage-review`.
- Repeated work appears causative → `debugging` with the duplicate-work reference.
- Locking or contention dominates → `concurrency-review`.

## Output contract
Report the reviewed artifact/scenario, evidence, bottleneck, likely impact, recommended change, checks actually run, and post-change measurement when available. Clearly label unverified hypotheses and residual risks.
