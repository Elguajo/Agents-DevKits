---
name: responsive-design
description: Adapt an existing interface across viewport sizes by preserving hierarchy, usability, and design intent while defining layout, typography, navigation, media, density, and interaction behavior for responsive breakpoints. Use when responsive behavior needs deliberate design rather than simple stacking.
---

# Responsive Design

Own **responsive adaptation** of an already-defined UI direction.

## Use when
- A desktop or reference design must work well on tablet/mobile.
- Layout behavior across widths is unspecified or failing.
- Content priority, navigation, media, or density must change responsively.

## Do not use when
- A new visual identity is needed; use `frontend-design`.
- The problem is only implementation parity with supplied Figma; start with `figma-to-code`.
- The task is only checking rendered breakpoints; use `visual-qa`.

## Workflow
1. Read the task brief, `DESIGN.md`, and existing component/layout rules.
2. Preserve content hierarchy and visual identity before changing layout.
3. Identify breakpoint-driven behavior for:
   - containers and grids
   - type scale and line length
   - spacing/density
   - navigation
   - images/media
   - tables/data-heavy UI
   - controls and touch targets
   - overflow and wrapping
4. Prefer fluid rules where possible; use breakpoints when behavior actually changes.
5. Avoid the default solution of merely changing every row to a column.
6. Preserve accessible reading order and interaction semantics.
7. Hand rendered verification to `visual-qa` / `playwright-testing`.

## Output contract
Return:
- Responsive behavior by layout region
- Breakpoints or fluid rules introduced
- Content-priority decisions
- Edge cases to verify
- Handoff checks for QA
