---
name: design-code
description: Implement accessible, token-driven UI code in the project's framework from approved component, design-system, or visual-direction decisions.
---

# Design Code

Implement a real UI artifact after intent is clear. This skill does not invent a replacement product flow or silently replace an approved reference.

## Workflow

1. Identify the target framework, styling system, repository conventions, and the approved source of visual intent.
2. Reuse existing primitives and semantic tokens first. If the project has no system, hand the foundation to `brandkit` or `design-tokens` rather than scattering one-off values.
3. Implement complete states that are relevant to the component: default, hover, focus, active, disabled, loading, error, and selected. Use semantic HTML, appropriate ARIA only where necessary, keyboard support, responsive layout, and reduced-motion behavior.
4. Run the project's declared lint, type, build, browser, or accessibility checks when available. Do not state that a visual, contrast, or interaction check passed unless it was actually observed.
5. Hand rendered fidelity to `visual-qa`, accessibility issues to `accessibility-review`, and behavioral browser coverage to `playwright-testing`.

## Completion evidence

Report changed artifacts, reused tokens/components, checks run with their results, unavailable checks, and remaining UI risks.
