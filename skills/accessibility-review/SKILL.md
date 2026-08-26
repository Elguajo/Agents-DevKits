---
name: accessibility-review
description: Review implemented web UI for accessibility problems involving semantics, keyboard use, focus, labels, contrast, motion, forms, and assistive-technology behavior. Use after or during UI implementation for targeted accessibility verification and remediation.
---

# Accessibility Review

Own **accessibility quality**, not broad visual redesign.

## Use when
- Reviewing or fixing accessibility in implemented UI.
- Forms, dialogs, navigation, interactive controls, keyboard flows, focus, or dynamic status messages are involved.

## Do not use when
- The task is general visual design; use `frontend-design`.
- The task is general functional E2E testing; use `playwright-testing`.
- The task is purely performance-related; use `performance-review`.

## Workflow
1. Read project conventions and existing accessibility utilities/tests.
2. Inspect semantic structure before adding ARIA.
3. Verify keyboard reachability, logical tab order, visible focus, and no keyboard traps.
4. Verify names, labels, descriptions, errors, and relationships for controls/forms.
5. Check dialogs, menus, tabs, disclosures, toasts/status updates, and custom widgets for correct interaction patterns.
6. Check contrast and non-color cues when tools or reliable tokens permit.
7. Respect reduced-motion preferences for non-essential animation.
8. Check touch target usability and responsive zoom/reflow issues where relevant.
9. Prefer native HTML semantics over custom ARIA implementations.
10. Re-test affected interactions after remediation.

If browser or assistive-technology tooling is unavailable, inspect semantics and
existing automated coverage without claiming runtime accessibility verification.

## Rules
- Do not add ARIA that duplicates or conflicts with native semantics.
- Do not claim full WCAG conformance from a partial automated check.
- Separate verified defects from recommendations requiring manual assistive-technology testing.

## Output contract
Report the reviewed artifact, concrete issues with severity, affected element/flow, user impact, evidence, and a minimal remediation. State checks actually run, the review decision, and what remains unverified.
