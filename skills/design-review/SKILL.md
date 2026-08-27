---
name: design-review
description: Review a proposed or implemented interface for hierarchy, consistency, usability, responsiveness, accessibility, and performance trade-offs without taking over implementation.
---

# Design Review

Produce a decision-useful expert review of an interface. Use `visual-qa` when exact fidelity to a supplied reference is the question, and `accessibility-review` for a focused compliance audit.

## Workflow

1. Establish the target users, jobs, platform, reference source, and whether the artifact is a proposal or a rendered implementation.
2. Examine hierarchy, comprehension, consistency, interaction feedback, responsive behavior, accessibility implications, and meaningful performance costs.
3. Classify findings by user impact and confidence. Recommend specific changes tied to the current design system instead of redesigning the product from preference.
4. Keep factual measurements separate from expert judgment. Request browser, accessibility, or performance evidence where a claim cannot be judged from the artifact alone.
5. Hand remediation to the owning specialist and provide the resulting review to `release-check` as `expert-review` evidence.

Read [review-rubric.md](references/review-rubric.md) for the review dimensions.

## Completion evidence

Return the examined scope, prioritized findings, positive constraints to preserve, evidence used, and remaining uncertainty.
