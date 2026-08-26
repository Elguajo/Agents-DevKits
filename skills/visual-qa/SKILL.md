---
name: visual-qa
description: Audit implemented UI against a supplied reference or established design intent using browser screenshots and concrete visual evidence. Use after implementation to find layout, spacing, typography, responsive, and state regressions without independently redesigning the product.
---

# Visual QA

Own **visual verification**, not visual art direction.

## Use when
- UI has been implemented and needs comparison against Figma, screenshots, DESIGN.md, or an approved existing page.
- Responsive regressions, overflow, alignment, spacing, typography, or state presentation need checking.

## Do not use when
- The user wants a new visual concept; use `frontend-design`.
- The task is functional browser testing; use `playwright-testing`.
- There is no reference and no established design intent to compare against.

## Workflow
1. Identify the source of truth: reference screenshot/Figma, DESIGN.md, or approved existing UI.
2. Open the real implementation in a browser when tooling permits.
3. Check the reference viewport first, then relevant breakpoints.
4. Compare composition, dimensions, alignment, spacing, typography, color, borders, radii, shadows, imagery, and visible states.
5. Check overflow, clipping, wrapping, sticky/fixed behavior, and responsive reflow.
6. Capture evidence for meaningful discrepancies.
7. Fix only discrepancies supported by the source of truth or clear UI defects.
8. Re-run the comparison after fixes.

If browser rendering or screenshots are unavailable, do not claim visual parity.
Inspect the available source/reference material, report the limitation, and hand
functional browser verification to `playwright-testing` when it becomes available.

## Suggested viewport coverage
Use project-specific breakpoints when known. Otherwise sample a representative desktop, tablet, and mobile width rather than blindly testing arbitrary sizes.

## Conflict rules
- Do not replace deliberate design decisions because another option looks better.
- Do not change product behavior while fixing a purely visual issue.
- Functional failures belong to `playwright-testing`; accessibility findings belong to `accessibility-review`.

## Output contract
Report the reviewed artifact and source of truth, then concrete findings by severity with location, evidence, expected result, actual result, and recommended fix. If the implementation matches the reference within reasonable rendering tolerance, say so explicitly. State rendered checks actually run and remaining visual risks.
