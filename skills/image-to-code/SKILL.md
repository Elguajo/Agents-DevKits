---
name: image-to-code
description: Reconstruct the layout and design-system intent of a supplied screenshot or mockup as accessible, repository-native UI without copying protected assets or claiming pixel fidelity without comparison.
---

# Image to Code

Use a visual reference as design evidence, not as permission to copy its identity assets or hidden implementation.

## Workflow

1. Inspect the reference and record observed hierarchy, layout, typography character, spacing, component patterns, color roles, responsive clues, and unknowns.
2. Treat approved project assets, brand guidance, and existing tokens as higher-priority constraints. Replace logos, photographs, proprietary fonts, and copyrighted copy with licensed or project-provided equivalents.
3. Map observed patterns to the current design system, then use `design-component` and `design-code` for reusable implementation.
4. Render and compare the result against the permitted reference when browser capability is available. Separate visual similarity judgment from functional and accessibility checks.
5. Hand visible discrepancies to `visual-qa` and semantic/keyboard concerns to `accessibility-review`.

Read [reference-analysis.md](references/reference-analysis.md) before reconstructing a complex screen.

## Completion evidence

Return the observed design-system mapping, substitutions made for protected assets, rendered comparison evidence, checks run, and residual fidelity limits.
