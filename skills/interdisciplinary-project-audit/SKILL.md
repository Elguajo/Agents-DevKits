---
name: interdisciplinary-project-audit
description: Audit an existing software product for blind spots across the relevant engineering, architecture, product, UX, QA, security, reliability, operations, data, and business disciplines. Use when the owner wants to know what they may not realize they should be asking before continuing development.
---

# Interdisciplinary Project Audit

## Goal
Identify important blind spots, risks, weaknesses, unnecessary complexity, and high-value opportunities grounded in the actual product.

## Workflow
1. Understand the existing project first: architecture, functionality, documentation, intended users, constraints, and current maturity.
2. Select only disciplines that are actually relevant: engineering, architecture, product, UX/accessibility, QA, security/privacy, performance/reliability, DevOps/observability, data/analytics, growth/marketing, monetization/business model, support/operations.
3. Identify:
   - missing or fragile foundations;
   - technical debt and architectural risks;
   - important edge cases;
   - security, privacy, performance, reliability, compatibility, or data-loss risks;
   - product/UX problems likely to emerge with growth;
   - high-value capabilities that fit the actual product;
   - things that should not be built yet;
   - concepts/trade-offs the owner should understand;
   - questions the owner may not know to ask.
4. Ground every meaningful recommendation in current-project evidence.
5. Prioritize into Now / Next / Later / Avoid for now.

## Rules
- Do not produce a generic wishlist.
- Do not force every discipline into the review.
- Do not recommend features merely because competitors commonly have them.
- Do not change the project during the audit.
- Prefer blind spots with high consequence or expensive rework potential.

## Output
### Risks & Blind Spots
### Improvements
### Opportunities
### Simplify / Remove
### Things I Should Know
### Questions I Didn't Know to Ask
### Recommended Roadmap

For each recommendation include problem/opportunity, why it matters, evidence, action, priority, effort, and timing.


## Boundary with `project-audit`
Use `project-audit` when the requested outcome is primarily engineering/codebase health. Use this skill when the owner explicitly wants blind spots across product, UX, business, operations, growth, support, data, and engineering, especially questions they may not know to ask. Delegate technical deep dives to specialist skills rather than duplicating them here.
