---
name: brandkit
description: "Create an accessible, reusable visual foundation for a new product: semantic design tokens, typography, spacing, motion, and light/dark theme intent."
---

# Brand Kit

Create a coherent foundation before individual screens. Use this for a new product or a deliberate visual-system reset, not a one-off page palette.

## Workflow

1. Capture the product domain, audience, voice, accessibility target, supported themes, and implementation platforms.
2. Define primitive scales only where needed, then map semantic roles for actions, text, surfaces, borders, feedback, typography, spacing, elevation, radius, and motion.
3. Keep component-specific values scoped to components; do not expose raw palette values as ordinary application choices.
4. Design light and dark modes intentionally at the semantic layer. Verify required contrast pairs with available tools; report unavailable measurements rather than estimating them.
5. Record the token source of truth and hand platform output to `token-build`, component specification to `design-component`, and implementation to `design-code`.

## Completion evidence

Return the token artifact summary, theme modes, measured checks, unresolved brand decisions, and any platform-specific output still required.
