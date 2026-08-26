---
name: figma-to-code
description: Translate a supplied Figma design into repository-native production UI with high visual fidelity while reusing the existing design system and components. Use when Figma frames, nodes, screenshots, or design context are the implementation source of truth.
---

# Figma to Code

Own **translation from supplied Figma intent to code**. Do not independently redesign the interface.

## Use when
- The user supplies Figma context, frames, nodes, screenshots, or a design handoff.
- Existing code must match a design reference accurately.

## Do not use when
- No Figma/reference design exists and visual direction must be invented; use `frontend-design`.
- The task is only a post-implementation comparison; use `visual-qa`.

## Workflow
1. Read project instructions, `DESIGN.md`, and existing component conventions.
2. Obtain available Figma design context and a visual reference/screenshot when tooling permits.
3. Identify layout hierarchy, components, states, tokens, typography, assets, responsive intent, and interactions.
4. Map Figma elements to existing repository components before creating new ones.
5. Implement semantic structure and behavior first, then visual fidelity.
6. Preserve supplied assets and text; do not substitute arbitrary equivalents when exact assets are available.
7. Validate at the reference viewport and relevant responsive widths.
8. Use `visual-qa` for comparison and iterate on measurable discrepancies.

If Figma tooling is unavailable, work from exported frames, screenshots, or
documented component behavior when supplied. Do not claim node-level parity
without access to the source design.

## Conflict rules
- Explicit task instructions override Figma when the user intentionally requests a change.
- Existing design-system semantics should be reused where they can reproduce the design faithfully.
- If Figma and the coded design system materially conflict, flag the mismatch instead of silently inventing a third system.

## Completion criteria
The implementation should be structurally native to the repository, behaviorally correct, and visually close enough that remaining differences are intentional or documented. Report the reference used, verification actually performed, and unresolved mismatches.
