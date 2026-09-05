---
name: ux-usability-audit
description: Audit a real website or application as a human user to find problems in interaction logic, information architecture, navigation, task flow, affordances, states, microcopy, and usability; use relevant production references to guide high-confidence improvements without blindly redesigning the product.
---

# UX & Usability Audit

## Goal
Make an existing interface easier to understand, navigate, and use by identifying evidence-based usability problems in real user journeys, then recommending or implementing the smallest high-confidence improvements.

## Primary ownership
This skill owns **human-centered usability and interaction logic**:
- user journeys and task completion;
- observed navigation and information-architecture problems, reported as usability evidence;
- visual/interaction hierarchy as it affects comprehension;
- affordances and discoverability;
- forms, validation, feedback, empty/loading/error/success states;
- microcopy and decision clarity;
- unnecessary steps, cognitive load, and recovery from mistakes;
- responsive usability, not merely responsive layout;
- reference-guided UX improvement.

It does **not** own visual art direction, pixel fidelity, accessibility compliance, browser automation, responsive implementation, the product's structural model, or a broad UI redesign. Hand those concerns to the relevant specialist skill.

## Workflow

### 1. Understand before judging
Inspect the actual product and repository context before proposing changes.
Determine:
- what the product does;
- likely user groups;
- primary user goals;
- critical journeys and conversion points;
- current navigation/information architecture;
- existing design system and intentional constraints.

Do not review isolated screens as if they were unrelated mockups.

### 2. Walk the product like a real user
Use the real interface when browser access is available. Exercise the important flows from a user's perspective, including relevant variants such as first visit, repeat use, back/cancel/edit, empty/loading/error states, long content, unusual input, and mobile/desktop behavior.

Continuously ask:
- Do I understand where I am and what this screen is for?
- Is the next useful action obvious?
- Does the interface provide timely feedback?
- Can I predict what controls will do?
- Can I recover from mistakes without fear?
- Am I forced to remember information that could be visible?
- Are similar actions and patterns consistent?
- Are there unnecessary steps or choices?
- Is something technically functional but confusing to a human?

If the interface cannot actually be exercised, state that the audit is limited and do not claim behavioral findings that were not observed.

### 3. Audit the experience
Use `references/usability-review-checklist.md` as a compact review guide. Prioritize problems that affect task success, comprehension, confidence, or efficiency over cosmetic preferences.

For accessibility-specific findings, hand off to `accessibility-review` rather than pretending this skill is a full accessibility audit.

### 4. Research references when useful
For substantial UX changes or unclear patterns, use `references/reference-guided-improvement.md`.
Prefer real production products, platform/design-system guidance, or credible UX research. Use references to learn interaction patterns and problem-solving approaches, not to copy another product's visual identity.

### 5. Produce evidence-based findings
For every meaningful issue include:
- **Problem** — what is confusing, inefficient, or fragile;
- **User impact** — what a real user may fail to understand or accomplish;
- **Evidence** — exact screen/flow/state/behavior observed;
- **Principle/reference** — only when it materially supports the finding;
- **Recommended action** — smallest useful change;
- **Severity** — Critical / High / Medium / Low;
- **Confidence** — High / Medium / Low.

Do not invent issues to fill a report.

### 6. Improve only when authorized
If the user asked only for an audit, stop after recommendations.
If the user explicitly asked to improve/fix the interface, implement only high-confidence changes after the audit.

Implementation rules:
- preserve intentional visual identity and product behavior;
- reuse the existing design system/components;
- prefer small changes with large UX impact;
- do not add features merely because reference products have them;
- do not perform a broad redesign when a local interaction fix is enough;
- propose major redesigns before implementing them.

Hand off implementation-specific concerns where appropriate:
- `frontend-design` for new art direction;
- `design-system` for component/token consistency;
- `responsive-design` for cross-viewport implementation;
- `playwright-testing` for browser/E2E verification;
- `visual-qa` for rendered visual regressions;
- `accessibility-review` for accessibility-specific remediation;
- `information-architecture` for a structural navigation change;
- `redesign` for a broad UI rework;
- `ux-writing` for a wider interface-language pass.

### 7. Verify affected journeys
After implementation, repeat the affected user flows. Confirm the original usability problem is resolved and no important flow regressed. Missing verification is **unverified**, not passed.

## Output
1. Overall UX verdict
2. Highest-impact usability problems
3. Findings with evidence, severity, confidence, and action
4. Relevant references used and what was learned from them
5. Changes implemented, if authorized
6. Remaining recommendations
7. Questions requiring real user testing rather than agent assumption

## Rules
- Audit actual behavior before redesigning.
- User impact outranks visual fashion.
- Do not substitute taste for evidence.
- Do not copy reference products blindly.
- Do not claim to represent real users; distinguish observed interface problems from hypotheses that require user research.
- Keep recommendations grounded in the current product, users, and constraints.

## Boundaries
- `frontend-design` owns visual concept/art direction.
- `visual-qa` owns fidelity to approved visual intent.
- `playwright-testing` owns browser functional/E2E correctness.
- `accessibility-review` owns accessibility-specific audit/remediation.
- `responsive-design` owns responsive implementation behavior.
- `product-spec` owns what the product should do; this skill owns whether the current interaction is understandable and usable.
- `information-architecture` owns deciding the navigation and structural model; this skill reports observed structural usability problems and hands a restructure to it.
- `design-review` owns expert critique of UI quality and trade-offs, including designs that cannot be exercised; this skill requires observed behavior in a real interface and reports task-level usability evidence.
- `redesign` owns a broad audit-first UI improvement once the direction is agreed; this skill stays with local, high-confidence interaction fixes and hands larger rework to it.
- `ux-research` owns obtaining or synthesizing real user evidence; this skill must label its own findings as expert observation, not user research.
